#!/usr/bin/env python3
"""Render synthetic pages with GitHub's Markdown API (mode gfm).

Usage: render_gfm.py <pages.json> <render-dir> <out.json>
Each page's exact request body and response bytes are kept under
<render-dir>/<sha256-of-request>.{req.json,html}; a page already rendered
is not sent again. out.json maps each page id to the request and response
SHA-256 and the headings GitHub rendered ([[level, text], ...]).
At most two requests run at once, throttled; a page GitHub refuses
after eight back-offs is left out of out.json.
"""
import concurrent.futures
import hashlib
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HEADING_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.S)
TAG_RE = re.compile(r"<[^>]*>")


def rendered_headings(body: str) -> list:
    return [[int(lvl), html.unescape(TAG_RE.sub("", inner)).strip()]
            for lvl, inner in HEADING_RE.findall(body)]


def render(text: str, cache: Path) -> tuple[str, str]:
    req = json.dumps({"text": text, "mode": "gfm"}, sort_keys=True).encode()
    key = hashlib.sha256(req).hexdigest()
    req_path, html_path = cache / f"{key}.req.json", cache / f"{key}.html"
    if not html_path.exists():
        req_path.write_bytes(req)
        for attempt in range(8):
            res = subprocess.run(
                ["gh", "api", "-X", "POST", "/markdown", "--input",
                 str(req_path)], capture_output=True)
            if res.returncode == 0:
                html_path.write_bytes(res.stdout)
                break
            time.sleep(30 * (attempt + 1))  # secondary rate limit: back off
        else:
            return key, None
        time.sleep(0.6)
    return key, html_path.read_text()


def main() -> None:
    pages_path, cache_dir, out_path = sys.argv[1:4]
    pages = json.load(open(pages_path))
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(render, text, cache): key
                   for key, text in pages.items()}
        for fut in concurrent.futures.as_completed(futures):
            key = futures[fut]
            req_sha, body = fut.result()
            if body is None:
                continue                # not rendered: left out, not guessed
            out[key] = {
                "request_sha256": req_sha,
                "response_sha256": hashlib.sha256(body.encode()).hexdigest(),
                "headings": rendered_headings(body),
            }
    json.dump(out, open(out_path, "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
