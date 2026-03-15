#!/usr/bin/env python3
"""
Launch transcription workers on Vast.ai.

Usage:
    export VASTAI_API_KEY=... GH_TOKEN=...
    python3 launch_transcription.py [--workers 20] [--dry-run]
"""
import argparse
import json
import os
import sys
import time
import urllib.request

VASTAI_API = "https://console.vast.ai/api/v0"
REPO = "apeyi/freeBuddhistAudio"
BRANCH = "main"


def get_keys():
    api_key = os.environ.get("VASTAI_API_KEY", "")
    gh_token = os.environ.get("GH_TOKEN", "")
    if not api_key or not gh_token:
        print("ERROR: Set VASTAI_API_KEY and GH_TOKEN")
        sys.exit(1)
    return api_key, gh_token


def vast_request(method, path, data=None):
    api_key, _ = get_keys()
    req = urllib.request.Request(
        f"{VASTAI_API}{path}",
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method=method,
    )
    return json.load(urllib.request.urlopen(req))


def find_offers(gpu_name, count):
    return vast_request("POST", "/bundles/", {
        "limit": count,
        "type": "on-demand",
        "verified": {"eq": True},
        "rentable": {"eq": True},
        "rented": {"eq": False},
        "gpu_name": {"eq": gpu_name},
        "inet_down": {"gte": 500},
        "order": [["dph_total", "asc"]],
    }).get("offers", [])


def make_onstart(worker_id, gh_token, vast_key, release_tag):
    batch_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/scripts/batches/batch_{worker_id:02d}.json"
    script_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/scripts/transcribe_batch.py"
    label = f"whisper-{worker_id:02d}"
    return f"""#!/bin/bash
set -e
echo "=== WORKER {worker_id:02d} START ==="
pip install -q openai-whisper
echo "Installed. Downloading batch..."
curl -sL "{batch_url}" -o /tmp/batch.json
curl -sL "{script_url}" -o /tmp/worker.py
echo "Running transcription..."
python3 /tmp/worker.py --input /tmp/batch.json --output /results/ --model turbo
echo "Uploading results..."
tar czf /tmp/results.tar.gz -C / results/
python3 -c "
import json,urllib.request,time
gh='{gh_token}'
tag='{release_tag}'
r=urllib.request.Request('https://api.github.com/repos/{REPO}/releases/tags/'+tag,headers={{'Authorization':'token '+gh}})
resp=json.load(urllib.request.urlopen(r))
u=resp['upload_url'].replace('{{?name,label}}','')
with open('/tmp/results.tar.gz','rb') as f: d=f.read()
r2=urllib.request.Request(u+'?name=worker-{worker_id:02d}.tar.gz',data=d,headers={{'Authorization':'token '+gh,'Content-Type':'application/gzip'}})
print('UPLOAD:',json.load(urllib.request.urlopen(r2))['browser_download_url'])
"
echo "Self-destructing..."
MYID=$(curl -s "{VASTAI_API}/instances/" -H "Authorization: Bearer {vast_key}" | python3 -c "
import json,sys
for i in json.load(sys.stdin).get('instances',[]):
    if i.get('label')=='{label}': print(i['id']); break
")
curl -s -X DELETE "{VASTAI_API}/instances/$MYID/" -H "Authorization: Bearer {vast_key}"
echo "=== WORKER {worker_id:02d} DONE ==="
"""


def create_release(tag, name, gh_token):
    data = json.dumps({"tag_name": tag, "name": name, "draft": False}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases",
        data=data,
        headers={"Authorization": f"token {gh_token}", "Content-Type": "application/json"},
    )
    try:
        return json.load(urllib.request.urlopen(req))["id"]
    except urllib.error.HTTPError:
        req2 = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases/tags/{tag}",
            headers={"Authorization": f"token {gh_token}"},
        )
        return json.load(urllib.request.urlopen(req2))["id"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--gpu", default="RTX 2080 Ti")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    api_key, gh_token = get_keys()
    release_tag = f"transcripts-{int(time.time())}"

    print(f"Finding {args.workers}+ offers for {args.gpu}...")
    offers = find_offers(args.gpu, args.workers + 5)
    print(f"Found {len(offers)} offers")
    if len(offers) < args.workers:
        print(f"WARNING: Only {len(offers)} available, need {args.workers}")
    if not offers:
        sys.exit(1)

    est_cost = sum(o["dph_total"] for o in offers[:args.workers]) * 3
    print(f"Estimated cost (3h): ${est_cost:.2f}")

    if args.dry_run:
        for i, o in enumerate(offers[:args.workers]):
            print(f"  Worker {i:02d}: offer {o['id']} ${o['dph_total']:.3f}/hr {o['inet_down']:.0f}Mbps")
        print("DRY RUN — not launching")
        return

    print(f"\nCreating GitHub release '{release_tag}'...")
    release_id = create_release(release_tag, f"Transcripts {time.strftime('%Y-%m-%d %H:%M')}", gh_token)
    print(f"Release: {release_id}")

    instances = []
    for i in range(min(args.workers, len(offers))):
        offer = offers[i]
        onstart = make_onstart(i, gh_token, api_key, release_tag)

        try:
            result = vast_request("PUT", f"/asks/{offer['id']}/", {
                "image": "pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime",
                "disk": 30,
                "runtype": "ssh",
                "onstart": onstart,
                "label": f"whisper-{i:02d}",
            })
            iid = result.get("new_contract")
            if iid:
                instances.append({"worker": i, "instance": iid, "offer": offer["id"], "cost": offer["dph_total"]})
                print(f"  Worker {i:02d}: instance {iid} (${offer['dph_total']:.3f}/hr)")
            else:
                print(f"  Worker {i:02d}: failed ({result})")
        except Exception as e:
            print(f"  Worker {i:02d}: error ({e})")

    info = {
        "release_tag": release_tag,
        "release_id": release_id,
        "workers": instances,
        "launched_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    with open("/workspace/scripts/last_launch.json", "w") as f:
        json.dump(info, f, indent=2)

    print(f"\n{'='*50}")
    print(f"Launched {len(instances)} workers")
    print(f"Release: {release_tag}")
    print(f"Cost: ~${sum(w['cost'] for w in instances) * 3:.2f} for 3h")
    print(f"\nCheck status: python3 scripts/check_transcription.py")
    print(f"Workers self-destruct when done.")


if __name__ == "__main__":
    main()
