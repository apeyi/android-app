#!/usr/bin/env python3
"""
Orchestrator for batch transcription of all FBA talks on Vast.ai.

1. Scrapes all talk audio URLs from FBA website
2. Splits into batches
3. Creates Vast.ai GPU instances, each processing a batch
4. Monitors progress and collects results

Usage:
    export VASTAI_API_KEY=your_key
    python3 transcribe_orchestrator.py --workers 5 --output ./transcripts/

Requirements: requests (or just urllib)
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

BASE_URL = "https://www.freebuddhistaudio.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile Safari/537.36"}
VASTAI_API = "https://console.vast.ai/api/v0"


def get_api_key():
    key = os.environ.get("VASTAI_API_KEY", "")
    if not key:
        print("ERROR: Set VASTAI_API_KEY environment variable")
        sys.exit(1)
    return key


def api_headers():
    return {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
    }


def vast_post(path, data):
    req = urllib.request.Request(
        f"{VASTAI_API}{path}",
        data=json.dumps(data).encode(),
        headers=api_headers(),
        method="POST",
    )
    return json.load(urllib.request.urlopen(req))


def vast_put(path, data):
    req = urllib.request.Request(
        f"{VASTAI_API}{path}",
        data=json.dumps(data).encode(),
        headers=api_headers(),
        method="PUT",
    )
    return json.load(urllib.request.urlopen(req))


def vast_get(path):
    req = urllib.request.Request(f"{VASTAI_API}{path}", headers=api_headers())
    return json.load(urllib.request.urlopen(req))


def vast_delete(path):
    req = urllib.request.Request(f"{VASTAI_API}{path}", headers=api_headers(), method="DELETE")
    return json.load(urllib.request.urlopen(req))


# ── Step 1: Scrape all talk audio URLs ──────────────────────────────────────

def scrape_all_talks():
    """Get catNum and audio stream URL for all talks by year."""
    all_talks = []
    current_year = time.localtime().tm_year

    for year in range(1965, current_year + 1):
        url = f"{BASE_URL}/browse?y={year}&t=audio"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            html = urllib.request.urlopen(req, timeout=15).read().decode()
        except Exception as e:
            print(f"  {year}: error ({e})")
            continue

        # Extract total_items
        m = re.search(r'"total_items"\s*:\s*(\d+)', html)
        total = int(m.group(1)) if m else 0
        if total == 0:
            continue

        # Extract catNums from the page
        cat_nums = re.findall(r'"cat_num"\s*:\s*"([^"]+)"', html)

        for cn in cat_nums:
            all_talks.append({
                "catNum": cn,
                "audioUrl": f"{BASE_URL}/audio/stream?num={cn}",
            })

        # If there are more talks than shown on the page, we need pagination
        # The collection API returns one item per page request
        if total > len(cat_nums):
            # Extract API base URL from collection JSON
            api_match = re.search(r'"url"\s*:\s*"(/api/v1/collections/[^"]+)"', html)
            query_string = f"y={year}&t=audio"
            if api_match:
                api_base = BASE_URL + api_match.group(1)
                for idx in range(len(cat_nums) + 1, total + 1):
                    page_url = f"{api_base}?{query_string}&page={idx}"
                    try:
                        req2 = urllib.request.Request(page_url, headers=HEADERS)
                        page_html = urllib.request.urlopen(req2, timeout=15).read().decode()
                        page_data = json.loads(page_html)
                        items = page_data.get("collection", {}).get("items", [])
                        for item in items:
                            cn = item.get("cat_num", "")
                            if cn and cn not in [t["catNum"] for t in all_talks]:
                                all_talks.append({
                                    "catNum": cn,
                                    "audioUrl": f"{BASE_URL}/audio/stream?num={cn}",
                                })
                    except Exception:
                        pass

        print(f"  {year}: {len(cat_nums)} on page, {total} total → {len(all_talks)} cumulative")

    return all_talks


# ── Step 2: Find GPU offers and create instances ────────────────────────────

def find_offers(gpu_name="RTX 2080 Ti", count=5):
    """Find cheapest available GPU offers."""
    result = vast_post("/bundles/", {
        "limit": count,
        "type": "on-demand",
        "verified": {"eq": True},
        "rentable": {"eq": True},
        "rented": {"eq": False},
        "gpu_name": {"eq": gpu_name},
        "order": [["dph_total", "asc"]],
    })
    return result.get("offers", [])


def create_worker(offer_id, batch_json_url, worker_id, results_webhook_url=""):
    """Create a Vast.ai instance to process a batch of talks."""
    onstart = f"""#!/bin/bash
set -e
pip install -q openai-whisper

# Download batch assignment and worker script
curl -sL "{batch_json_url}" -o /tmp/batch.json
curl -sL "https://raw.githubusercontent.com/apeyi/freeBuddhistAudio/main/scripts/transcribe_batch.py" -o /tmp/transcribe_batch.py

# Run transcription
mkdir -p /results
python3 /tmp/transcribe_batch.py --input /tmp/batch.json --output /results/ --model turbo

echo "WORKER_{worker_id}_COMPLETE"
"""

    result = vast_put(f"/asks/{offer_id}/", {
        "image": "pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime",
        "disk": 30,
        "runtype": "ssh",
        "onstart": onstart,
        "label": f"whisper-worker-{worker_id}",
    })
    return result.get("new_contract")


# ── Step 3: Monitor instances ───────────────────────────────────────────────

def get_instances():
    """Get all current instances."""
    result = vast_get("/instances/")
    return result.get("instances", [])


def get_logs(instance_id, tail=50):
    """Get instance container logs."""
    try:
        result = vast_put(f"/instances/request_logs/{instance_id}/", {"tail": str(tail)})
        url = result.get("result_url", "")
        if url:
            time.sleep(5)  # Wait for S3 upload
            req = urllib.request.Request(url)
            return urllib.request.urlopen(req).read().decode()
    except Exception:
        pass
    return ""


def destroy_instance(instance_id):
    """Destroy an instance."""
    try:
        vast_delete(f"/instances/{instance_id}/")
        print(f"  Destroyed instance {instance_id}")
    except Exception as e:
        print(f"  Error destroying {instance_id}: {e}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Orchestrate FBA transcription on Vast.ai")
    parser.add_argument("--workers", type=int, default=5, help="Number of parallel GPU workers")
    parser.add_argument("--gpu", default="RTX 2080 Ti", help="GPU type to use")
    parser.add_argument("--output", default="./transcripts", help="Local output directory")
    parser.add_argument("--scrape-only", action="store_true", help="Only scrape talk list, don't launch workers")
    parser.add_argument("--talks-file", help="Use pre-scraped talks JSON instead of scraping")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Step 1: Get all talks
    if args.talks_file:
        with open(args.talks_file) as f:
            all_talks = json.load(f)
        print(f"Loaded {len(all_talks)} talks from {args.talks_file}")
    else:
        print("Scraping all FBA talk URLs...")
        all_talks = scrape_all_talks()
        talks_file = os.path.join(args.output, "all_talks.json")
        with open(talks_file, "w") as f:
            json.dump(all_talks, f, indent=2)
        print(f"Scraped {len(all_talks)} talks, saved to {talks_file}")

    if args.scrape_only:
        return

    # Step 2: Split into batches
    batch_size = len(all_talks) // args.workers + 1
    batches = [all_talks[i:i+batch_size] for i in range(0, len(all_talks), batch_size)]
    print(f"Split into {len(batches)} batches of ~{batch_size} talks each")

    # Save batch files (these need to be accessible to the workers)
    # For now, save locally — workers will need a way to access them
    batch_files = []
    for i, batch in enumerate(batches):
        batch_path = os.path.join(args.output, f"batch_{i}.json")
        with open(batch_path, "w") as f:
            json.dump(batch, f)
        batch_files.append(batch_path)
        print(f"  Batch {i}: {len(batch)} talks → {batch_path}")

    print(f"\nBatch files saved to {args.output}/batch_*.json")
    print(f"\nTo run workers, you need to:")
    print(f"1. Upload batch files somewhere accessible (e.g., GitHub, S3)")
    print(f"2. Create Vast.ai instances pointing to each batch")
    print(f"3. Collect results via SSH/SCP when done")
    print(f"\nOr run with --launch to auto-create instances (requires batch files on a public URL)")


if __name__ == "__main__":
    main()
