#!/usr/bin/env python3
"""
Scrape all FBA talk catNums and their audio URLs (including multi-track).
Saves to a JSON file that can be split into batches for workers.

Usage:
    python3 scrape_talk_urls.py --output all_talks.json
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


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=30).read().decode()


def get_catnum_list():
    """Get all catNums by scraping the browse-by-year pages."""
    all_catnums = []
    current_year = time.localtime().tm_year

    for year in range(1965, current_year + 1):
        url = f"{BASE_URL}/browse?y={year}&t=audio"
        try:
            html = fetch(url)
        except Exception as e:
            print(f"  {year}: error ({e})")
            continue

        m = re.search(r'"total_items"\s*:\s*(\d+)', html)
        total = int(m.group(1)) if m else 0
        if total == 0:
            continue

        # Get catNums from page
        page_cats = list(dict.fromkeys(re.findall(r'"cat_num"\s*:\s*"([^"]+)"', html)))
        all_catnums.extend(page_cats)

        # Paginate if needed
        if total > len(page_cats):
            api_match = re.search(r'"url"\s*:\s*"(/api/v1/collections/[^"]+)"', html)
            if api_match:
                api_base = BASE_URL + api_match.group(1)
                for idx in range(len(page_cats) + 1, total + 1):
                    try:
                        page_url = f"{api_base}?y={year}&t=audio&page={idx}"
                        page_html = fetch(page_url)
                        page_data = json.loads(page_html)
                        for item in page_data.get("collection", {}).get("items", []):
                            cn = item.get("cat_num", "")
                            if cn and cn not in all_catnums:
                                all_catnums.append(cn)
                    except Exception:
                        pass

        print(f"  {year}: {total} talks → {len(all_catnums)} cumulative")

    return list(dict.fromkeys(all_catnums))  # deduplicate preserving order


def get_audio_urls(catnum):
    """Fetch talk detail page and extract audio track URLs."""
    try:
        html = fetch(f"{BASE_URL}/audio/details?num={catnum}")

        # Try to extract tracks array from JSON
        tracks_match = re.search(r'"tracks"\s*:\s*\[', html)
        if tracks_match:
            # Find the tracks array
            start = tracks_match.start()
            rest = html[start:]
            # Extract balanced brackets
            depth = 0
            for i, c in enumerate(rest):
                if c == '[':
                    depth += 1
                elif c == ']':
                    depth -= 1
                    if depth == 0:
                        tracks_str = rest[:i+1]
                        tracks_str = tracks_str[tracks_str.index('['):]
                        try:
                            tracks = json.loads(tracks_str)
                            urls = []
                            for t in tracks:
                                audio = t.get("audio", {})
                                mp3 = audio.get("mp3", "")
                                if mp3:
                                    if not mp3.startswith("http"):
                                        mp3 = BASE_URL + mp3
                                    urls.append(mp3)
                            if urls:
                                return urls
                        except json.JSONDecodeError:
                            pass
                        break

        # Fallback: use stream URL
        return [f"{BASE_URL}/audio/stream?num={catnum}"]

    except Exception:
        return [f"{BASE_URL}/audio/stream?num={catnum}"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="all_talks.json")
    parser.add_argument("--skip-tracks", action="store_true",
                        help="Skip fetching individual track URLs (use stream URL only)")
    args = parser.parse_args()

    print("Scraping all talk catNums...")
    catnums = get_catnum_list()
    print(f"\nFound {len(catnums)} unique talks")

    talks = []
    if args.skip_tracks:
        # Just use stream URLs (faster, works for single-track talks)
        for cn in catnums:
            talks.append({
                "catNum": cn,
                "audioUrls": [f"{BASE_URL}/audio/stream?num={cn}"],
            })
    else:
        # Fetch track URLs for each talk (slower but handles multi-track)
        print("Fetching audio URLs for each talk...")
        for i, cn in enumerate(catnums):
            urls = get_audio_urls(cn)
            talks.append({"catNum": cn, "audioUrls": urls})
            if (i + 1) % 100 == 0:
                print(f"  {i+1}/{len(catnums)}...")
                time.sleep(0.5)  # Be polite to FBA servers

    with open(args.output, "w") as f:
        json.dump(talks, f, indent=2)

    multi = sum(1 for t in talks if len(t["audioUrls"]) > 1)
    print(f"\nSaved {len(talks)} talks to {args.output}")
    print(f"  Single-track: {len(talks) - multi}")
    print(f"  Multi-track: {multi}")


if __name__ == "__main__":
    main()
