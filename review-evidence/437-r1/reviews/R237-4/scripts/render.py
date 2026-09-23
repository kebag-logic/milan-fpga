#!/usr/bin/env python3
"""Render synthetic pages with GitHub's Markdown API (gfm mode) and cache
the exact request/response bytes by request SHA-256.

Usage: render.py <cache-dir>  < pages.json  > renders.json

Each page is POSTed as {"text": page, "mode": "gfm", "context":
"kebag-logic/milan-fpga"} through `gh api markdown --input -`. Only the
synthetic page text is sent. The answer per page is {"request_sha256",
"response_sha256", "headings": [[level, text], ...], "exit"}; headings are
the h1-h6 elements Python's html.parser reads out of the response.
"""
import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

CONTEXT = "kebag-logic/milan-fpga"
JOBS = 2          # concurrent requests (secondary rate limit)
PACE = 0.7        # seconds before every request, per worker
BACKOFF = 45      # seconds times the attempt number after a refusal
RETRIES = 6


class Headings(HTMLParser):
    """[level, collapsed text] of every h1..h6 element."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == "h%d" % self.level:
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def headings(html: str) -> list:
    parser = Headings()
    parser.feed(html)
    parser.close()
    return parser.found


def render(cache: Path, page: str) -> dict:
    request = json.dumps({"text": page, "mode": "gfm", "context": CONTEXT})
    key = hashlib.sha256(request.encode()).hexdigest()
    entry = cache / (key + ".json")
    if entry.exists():
        record = json.loads(entry.read_text())
    else:
        for attempt in range(RETRIES):
            time.sleep(PACE)
            proc = subprocess.run(["gh", "api", "markdown", "--input", "-"],
                                  input=request.encode(), capture_output=True, check=False)
            if proc.returncode == 0:
                break
            time.sleep(BACKOFF * (attempt + 1))   # secondary rate limit: wait, retry
        record = {"request_bytes": request, "request_sha256": key,
                  "response_bytes": proc.stdout.decode("utf-8", "surrogateescape"),
                  "response_sha256": hashlib.sha256(proc.stdout).hexdigest(),
                  "exit": proc.returncode,
                  "stderr": proc.stderr.decode("utf-8", "replace")[-500:],
                  "utc": datetime.now(timezone.utc).isoformat()}
        if proc.returncode == 0:
            entry.write_text(json.dumps(record, indent=1, sort_keys=True))
    return {"request_sha256": key, "response_sha256": record["response_sha256"],
            "exit": record["exit"], "headings": headings(record["response_bytes"]),
            "response_bytes": record["response_bytes"]}


def main() -> int:
    cache = Path(sys.argv[1])
    cache.mkdir(parents=True, exist_ok=True)
    pages = json.load(sys.stdin)
    with ThreadPoolExecutor(JOBS) as pool:
        out = list(pool.map(lambda p: render(cache, p), pages))
    json.dump(out, sys.stdout)
    return 0 if all(o["exit"] == 0 for o in out) else 1


if __name__ == "__main__":
    sys.exit(main())
