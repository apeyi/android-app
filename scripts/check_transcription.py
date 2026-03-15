#!/usr/bin/env python3
"""Check status of transcription workers and download results."""
import json
import os
import sys
import time
import urllib.request

VASTAI_API = "https://console.vast.ai/api/v0"
REPO = "apeyi/freeBuddhistAudio"


def get_keys():
    return os.environ.get("VASTAI_API_KEY", ""), os.environ.get("GH_TOKEN", "")


def check_instances():
    api_key, _ = get_keys()
    req = urllib.request.Request(
        f"{VASTAI_API}/instances/",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    instances = json.load(urllib.request.urlopen(req)).get("instances", [])
    whisper_instances = [i for i in instances if (i.get("label") or "").startswith("whisper-")]
    return whisper_instances


def check_release(tag):
    _, gh_token = get_keys()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases/tags/{tag}",
        headers={"Authorization": f"token {gh_token}"},
    )
    try:
        resp = json.load(urllib.request.urlopen(req))
        return resp.get("assets", [])
    except:
        return []


def download_results(tag, output_dir="./transcripts"):
    _, gh_token = get_keys()
    assets = check_release(tag)
    os.makedirs(output_dir, exist_ok=True)

    for asset in assets:
        name = asset["name"]
        print(f"Downloading {name}...")
        req = urllib.request.Request(
            asset["url"],
            headers={"Authorization": f"token {gh_token}", "Accept": "application/octet-stream"},
        )
        data = urllib.request.urlopen(req).read()
        tar_path = os.path.join(output_dir, name)
        with open(tar_path, "wb") as f:
            f.write(data)
        # Extract
        os.system(f"tar xzf {tar_path} -C {output_dir}")
        os.remove(tar_path)

    # Count results
    txt_files = [f for f in os.listdir(os.path.join(output_dir, "results")) if f.endswith(".txt")]
    print(f"\nDownloaded {len(txt_files)} transcripts to {output_dir}/results/")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Download results")
    parser.add_argument("--output", default="./transcripts", help="Output dir for download")
    args = parser.parse_args()

    # Load launch info
    info_path = "/workspace/scripts/last_launch.json"
    if os.path.exists(info_path):
        info = json.load(open(info_path))
        tag = info["release_tag"]
        print(f"Launch: {info['launched_at']}")
        print(f"Release: {tag}")
        print(f"Workers: {len(info['workers'])}")
    else:
        print("No launch info found")
        return

    # Check running instances
    instances = check_instances()
    running = [i for i in instances if i.get("actual_status") == "running"]
    print(f"\nRunning instances: {len(running)}")
    for i in instances:
        print(f"  {i.get('label')}: {i.get('actual_status')}")

    # Check uploaded results
    assets = check_release(tag)
    print(f"\nUploaded results: {len(assets)} / {len(info['workers'])} workers")
    for a in assets:
        print(f"  {a['name']} ({a['size']/1024:.1f} KB)")

    if len(running) == 0 and len(assets) > 0:
        print(f"\nAll workers finished! {len(assets)} result files ready.")
        if args.download:
            download_results(tag, args.output)
        else:
            print(f"Run with --download to fetch results")

    elif len(running) > 0:
        est_remaining = "unknown"
        print(f"\nStill running. Check again later.")


if __name__ == "__main__":
    main()
