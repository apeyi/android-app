#!/usr/bin/env python3
"""
Batch transcription worker for FBA talks using Whisper.
Uploads each transcript individually to GitHub release as it completes.
Skips talks listed in --skip file.
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


def upload_transcript(cat_num, text, gh_token, release_tag, upload_url_cache={}):
    """Upload a single transcript to GitHub release. Caches the upload URL."""
    if not gh_token or not release_tag:
        return False
    try:
        if "url" not in upload_url_cache:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{REPO}/releases/tags/{release_tag}",
                headers={"Authorization": f"token {gh_token}"}
            )
            resp = json.load(urllib.request.urlopen(req))
            upload_url_cache["url"] = resp["upload_url"].replace("{?name,label}", "")

        data = text.encode("utf-8")
        req2 = urllib.request.Request(
            f"{upload_url_cache['url']}?name={cat_num}.txt",
            data=data,
            headers={"Authorization": f"token {gh_token}", "Content-Type": "text/plain"}
        )
        json.load(urllib.request.urlopen(req2))
        return True
    except Exception as e:
        log(f"    Upload failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="turbo")
    parser.add_argument("--skip", default="", help="JSON file of catNums to skip")
    parser.add_argument("--gh-token", default="")
    parser.add_argument("--release-tag", default="")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Load skip list
    skip_set = set()
    if args.skip and os.path.exists(args.skip):
        skip_data = json.load(open(args.skip))
        if isinstance(skip_data, dict):
            skip_set = {k for k, v in skip_data.items() if v}
        elif isinstance(skip_data, list):
            skip_set = set(skip_data)
        log(f"Skipping {len(skip_set)} talks with existing transcripts")

    gh_token = args.gh_token or os.environ.get("GH_TOKEN", "")
    release_tag = args.release_tag or os.environ.get("RELEASE_TAG", "")

    with open(args.input) as f:
        talks = json.load(f)

    # Filter out skipped talks
    original = len(talks)
    talks = [t for t in talks if t["catNum"] not in skip_set]
    skipped = original - len(talks)
    if skipped:
        log(f"Filtered out {skipped} talks with existing transcripts")

    log(f"Loading whisper model '{args.model}'...")
    import whisper
    model = whisper.load_model(args.model)
    log(f"Model loaded. Processing {len(talks)} talks.")

    ok_count = 0
    err_count = 0
    uploaded_count = 0
    total_seconds = 0

    for i, talk in enumerate(talks):
        cat_num = talk["catNum"]
        audio_urls = talk.get("audioUrls", [])
        output_file = os.path.join(args.output, f"{cat_num}.txt")

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            log(f"[{i+1}/{len(talks)}] {cat_num}: already done, skipping")
            continue

        if not audio_urls:
            audio_urls = get_track_urls(cat_num)
            if not audio_urls:
                log(f"[{i+1}/{len(talks)}] {cat_num}: no audio URLs")
                err_count += 1
                continue

        log(f"[{i+1}/{len(talks)}] {cat_num}: {len(audio_urls)} track(s)")

        try:
            full_text = ""
            total_elapsed = 0

            for ti, url in enumerate(audio_urls):
                tmp = os.path.join(tempfile.gettempdir(), f"{cat_num}_t{ti}.mp3")
                try:
                    download_file(url, tmp)
                    start = time.time()
                    result = model.transcribe(tmp)
                    elapsed = time.time() - start
                    total_elapsed += elapsed
                    text = result["text"].strip()
                    if full_text and text:
                        full_text += "\n\n"
                    full_text += text
                    if len(audio_urls) > 1:
                        log(f"    Track {ti+1}/{len(audio_urls)}: {elapsed:.0f}s, {len(text)} chars")
                finally:
                    if os.path.exists(tmp):
                        os.remove(tmp)

            total_seconds += total_elapsed
            with open(output_file, "w") as f:
                f.write(full_text)

            log(f"  Done: {total_elapsed:.0f}s, {len(full_text)} chars")
            ok_count += 1

            if upload_transcript(cat_num, full_text, gh_token, release_tag):
                uploaded_count += 1
                log(f"  Uploaded {cat_num}.txt")

        except Exception as e:
            log(f"  ERROR: {e}")
            err_count += 1

    log(f"\nBATCH_COMPLETE: {ok_count} done, {err_count} errors, {uploaded_count} uploaded, {total_seconds:.0f}s GPU")


if __name__ == "__main__":
    main()
