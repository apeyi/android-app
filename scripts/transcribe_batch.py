#!/usr/bin/env python3
"""
Batch transcription worker for FBA talks using Whisper.
Runs on a Vast.ai GPU instance.

Usage:
    python3 transcribe_batch.py --input batch.json --output /results/

batch.json format:
    [{"catNum": "116", "audioUrls": ["https://...", ...]}, ...]
    - audioUrls: list of track/chapter URLs (usually 1, but can be multiple)
    - If audioUrls is empty or missing, fetches from FBA detail page

Output: one .txt file per talk, named {catNum}.txt
Uploads each transcript to a GitHub release as it completes (if GH_TOKEN and RELEASE_TAG are set).
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import tempfile
import re

BASE_URL = "https://www.freebuddhistaudio.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) Chrome/120.0 Mobile Safari/537.36"}
REPO = "apeyi/freeBuddhistAudio"


def log(msg):
    print(msg, flush=True)


def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=30).read().decode()


def get_track_urls(cat_num):
    try:
        html = fetch_html(f"{BASE_URL}/audio/details?num={cat_num}")
        m = re.search(r'"tracks"\s*:\s*\[', html)
        if m:
            rest = html[m.start():]
            depth = 0
            for i, c in enumerate(rest):
                if c == "[": depth += 1
                elif c == "]":
                    depth -= 1
                    if depth == 0:
                        try:
                            tracks = json.loads(rest[rest.index("["):i+1])
                            urls = []
                            for t in tracks:
                                mp3 = t.get("audio", {}).get("mp3", "")
                                if mp3:
                                    if not mp3.startswith("http"):
                                        mp3 = BASE_URL + urllib.parse.quote(mp3)
                                    urls.append(mp3)
                            if urls:
                                return urls
                        except:
                            pass
                        break
    except Exception as e:
        log(f"    Error fetching tracks for {cat_num}: {e}")
    return []


def download_file(url, dest_path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
    return os.path.getsize(dest_path)


def upload_transcript(cat_num, text, gh_token, release_tag):
    """Upload a single transcript to the GitHub release."""
    if not gh_token or not release_tag:
        return
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases/tags/{release_tag}",
            headers={"Authorization": f"token {gh_token}"}
        )
        resp = json.load(urllib.request.urlopen(req))
        upload_url = resp["upload_url"].replace("{?name,label}", "")
        data = text.encode("utf-8")
        req2 = urllib.request.Request(
            f"{upload_url}?name={cat_num}.txt",
            data=data,
            headers={"Authorization": f"token {gh_token}", "Content-Type": "text/plain"}
        )
        json.load(urllib.request.urlopen(req2))
        log(f"    Uploaded {cat_num}.txt")
    except Exception as e:
        log(f"    Upload failed for {cat_num}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Batch transcribe FBA talks")
    parser.add_argument("--input", required=True, help="JSON file with talk assignments")
    parser.add_argument("--output", required=True, help="Output directory for transcripts")
    parser.add_argument("--model", default="turbo", help="Whisper model name")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # GitHub upload config from env
    gh_token = os.environ.get("GH_TOKEN", "")
    release_tag = os.environ.get("RELEASE_TAG", "")

    with open(args.input) as f:
        talks = json.load(f)

    log(f"Loading whisper model '{args.model}'...")
    import whisper
    model = whisper.load_model(args.model)
    log(f"Model loaded. Processing {len(talks)} talks.")
    if gh_token and release_tag:
        log(f"Will upload each transcript to release '{release_tag}'")

    summary = []
    total_transcribe_seconds = 0

    for i, talk in enumerate(talks):
        cat_num = talk["catNum"]
        audio_urls = talk.get("audioUrls", [])
        output_file = os.path.join(args.output, f"{cat_num}.txt")

        # Skip if already done
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            log(f"[{i+1}/{len(talks)}] {cat_num}: already done, skipping")
            summary.append({"catNum": cat_num, "status": "skipped"})
            continue

        # Fetch track URLs from detail page if not provided
        if not audio_urls:
            log(f"  Fetching track URLs from detail page...")
            audio_urls = get_track_urls(cat_num)
            if not audio_urls:
                log(f"  No audio URLs found, skipping")
                summary.append({"catNum": cat_num, "status": "error", "error": "no audio URLs"})
                continue

        log(f"[{i+1}/{len(talks)}] {cat_num}: {len(audio_urls)} track(s)")

        try:
            full_text = ""
            total_elapsed = 0
            total_size = 0

            for track_idx, url in enumerate(audio_urls):
                tmp_audio = os.path.join(tempfile.gettempdir(), f"{cat_num}_t{track_idx}.mp3")

                try:
                    size = download_file(url, tmp_audio)
                    total_size += size

                    start = time.time()
                    result = model.transcribe(tmp_audio)
                    elapsed = time.time() - start
                    total_elapsed += elapsed

                    text = result["text"].strip()
                    if full_text and text:
                        full_text += "\n\n"
                    full_text += text

                    if len(audio_urls) > 1:
                        log(f"    Track {track_idx+1}/{len(audio_urls)}: {elapsed:.0f}s, {len(text)} chars")
                finally:
                    if os.path.exists(tmp_audio):
                        os.remove(tmp_audio)

            total_transcribe_seconds += total_elapsed

            # Save transcript locally
            with open(output_file, "w") as f:
                f.write(full_text)

            log(f"  Done in {total_elapsed:.0f}s, {len(full_text)} chars, {total_size/1024/1024:.1f}MB audio")

            # Upload immediately
            upload_transcript(cat_num, full_text, gh_token, release_tag)

            summary.append({
                "catNum": cat_num,
                "status": "ok",
                "seconds": round(total_elapsed, 1),
                "chars": len(full_text),
                "tracks": len(audio_urls),
                "audioBytes": total_size,
            })

        except Exception as e:
            log(f"  ERROR: {e}")
            summary.append({"catNum": cat_num, "status": "error", "error": str(e)})

    # Write summary
    summary_path = os.path.join(args.output, "summary.json")
    with open(summary_path, "w") as f:
        json.dump({
            "totalTalks": len(talks),
            "completed": sum(1 for s in summary if s["status"] == "ok"),
            "errors": sum(1 for s in summary if s["status"] == "error"),
            "skipped": sum(1 for s in summary if s["status"] == "skipped"),
            "totalTranscribeSeconds": round(total_transcribe_seconds, 1),
            "talks": summary,
        }, f, indent=2)

    ok = sum(1 for s in summary if s["status"] == "ok")
    err = sum(1 for s in summary if s["status"] == "error")
    log(f"\nBATCH_COMPLETE: {ok} transcribed, {err} errors, {total_transcribe_seconds:.0f}s GPU time")


if __name__ == "__main__":
    main()
