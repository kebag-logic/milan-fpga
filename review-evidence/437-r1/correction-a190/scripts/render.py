#!/usr/bin/env python3
"""Render synthetic pages with GitHub's Markdown API (POST /markdown, gfm).

Usage: render.py CACHE.jsonl PAGES.json
PAGES.json is a list of page strings or {"page": ...} objects. Pages already
in CACHE.jsonl are skipped. Each new row records the exact request bytes
(keys sorted, no spaces, <, > and & escaped), the exact response bytes, both
SHA-256 values, the UTC time and the heading elements. At most 4 requests run
at once. Only synthetic pages are ever sent.
"""
import hashlib
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

CONTEXT = "kebag-logic/milan-fpga"


class Headings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == f"h{self.level}":
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def headings(html: str) -> list:
    p = Headings()
    p.feed(html)
    p.close()
    return p.found


def request_bytes(page: str) -> bytes:
    body = json.dumps({"context": CONTEXT, "mode": "gfm", "text": page},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return body.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").encode("ascii")


def render(page: str) -> dict:
    req = request_bytes(page)
    last = b""
    for attempt in range(6):
        r = subprocess.run(["gh", "api", "-X", "POST", "/markdown", "--input", "-"],
                           input=req, capture_output=True, timeout=120)
        if r.returncode == 0:
            html = r.stdout.decode("utf-8")
            return {"page": page, "request_bytes": req.decode("ascii"),
                    "request_sha256": hashlib.sha256(req).hexdigest(),
                    "response_bytes": html,
                    "response_sha256": hashlib.sha256(r.stdout).hexdigest(),
                    "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "headings": headings(html)}
        last = r.stderr
        time.sleep(5 + attempt * 10)
    raise SystemExit(f"render failed: {last.decode(errors='replace')}")


def load(cache: Path) -> dict:
    out = {}
    if cache.exists():
        for line in cache.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                out[row["page"]] = row
    return out


def main() -> int:
    cache, pages = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    pages = [p["page"] if isinstance(p, dict) else p for p in pages]
    have = load(cache)
    todo = list(dict.fromkeys(p for p in pages if p not in have))
    print(f"{len(pages)} pages, {len(todo)} to render", flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=4) as pool, cache.open("a") as out:
        for row in pool.map(render, todo):
            out.write(json.dumps(row) + "\n")
            out.flush()
            done += 1
            if done % 100 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    print(f"rendered {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
