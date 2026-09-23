#!/usr/bin/env python3
"""GitHub's rendering of synthetic pages (POST /markdown, mode gfm), cached.

The request body is built as the committed fixtures record it: keys sorted,
no spaces, and <, > and & escaped. Each render is cached under
receipts/renders/<request sha256>.json with the exact request and response
bytes, both SHA-256 values and the UTC time."""
import datetime
import hashlib
import json
import subprocess
import sys
import time
from html.parser import HTMLParser
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
CACHE = PACKET / "receipts" / "renders"
CONTEXT = "kebag-logic/milan-fpga"


class _Headings(HTMLParser):
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


def headings_of(html: str) -> list:
    p = _Headings()
    p.feed(html)
    p.close()
    return p.found


def request_bytes(page: str) -> str:
    body = json.dumps({"context": CONTEXT, "mode": "gfm", "text": page},
                      sort_keys=True, separators=(",", ":"))
    return body.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def render(page: str) -> dict:
    req = request_bytes(page)
    key = hashlib.sha256(req.encode()).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    CACHE.mkdir(parents=True, exist_ok=True)
    for attempt in range(8):
        res = subprocess.run(["gh", "api", "markdown", "--input", "-"],
                             input=req.encode(), capture_output=True)
        if res.returncode == 0:
            break
        time.sleep(20 * (attempt + 1))
    else:
        raise RuntimeError(res.stderr.decode())
    resp = res.stdout.decode()
    rec = {"page": page, "request_bytes": req, "request_sha256": key,
           "response_bytes": resp,
           "response_sha256": hashlib.sha256(resp.encode()).hexdigest(),
           "headings": headings_of(resp),
           "recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    path.write_text(json.dumps(rec, indent=1))
    return rec


if __name__ == "__main__":
    for page in json.loads(Path(sys.argv[1]).read_text()):
        r = render(page)
        print(json.dumps(page), r["headings"])
