#!/usr/bin/env python3
"""Render Markdown pages with GitHub's Markdown API (POST /markdown, mode gfm)
through the `gh` CLI, keep every request and response as a receipt, and read
the heading elements out of the returned HTML.

Library use: `render(page)` -> dict receipt; `rendered_headings(html)`.
CLI use:     gfm.py <pages.json> <out.json>   (pages.json: list of {"name","page"})

Receipts are cached by the SHA-256 of the exact request bytes under
RECEIPTS (default: ../receipts/renders beside this file), so a rerun sends
nothing that was already rendered.
"""
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

CONTEXT = "kebag-logic/milan-fpga"
SPACING = float(os.environ.get("GFM_SPACING", "1.0"))
_PACE = threading.Lock()
RECEIPTS = Path(os.environ.get("GFM_RECEIPTS",
                               Path(__file__).resolve().parent.parent / "receipts" / "renders"))


def request_bytes(page: str) -> bytes:
    """The JSON body: keys sorted, no spaces, <, > and & escaped."""
    body = json.dumps({"context": CONTEXT, "mode": "gfm", "text": page},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return body.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").encode()


def send(body: bytes) -> dict:
    """POST the exact bytes and keep the receipt."""
    digest = hashlib.sha256(body).hexdigest()
    path = RECEIPTS / f"{digest}.json"
    if path.exists():
        return json.loads(path.read_text())
    for attempt in range(10):
        with _PACE:                     # one request at a time, spaced
            time.sleep(SPACING)
            proc = subprocess.run(["gh", "api", "-X", "POST", "markdown", "--input", "-"],
                                  input=body, capture_output=True, timeout=120)
        if proc.returncode == 0:
            break
        time.sleep(90 if b"secondary rate limit" in proc.stderr else 5 + 5 * attempt)
    else:
        raise RuntimeError(f"render failed: {proc.stderr.decode(errors='replace')}")
    response = proc.stdout
    receipt = {"request_bytes": body.decode(), "request_sha256": digest,
               "response_bytes": response.decode(),
               "response_sha256": hashlib.sha256(response).hexdigest(),
               "recorded_utc": datetime.now(timezone.utc).isoformat()}
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(receipt, indent=1, sort_keys=True))
    tmp.replace(path)
    return receipt


def render(page: str) -> dict:
    """The receipt for one page, with its heading elements."""
    receipt = dict(send(request_bytes(page)))
    receipt["headings"] = rendered_headings(receipt["response_bytes"])
    return receipt


class _Headings(HTMLParser):
    """Every h1..h6 element as [level, whitespace-collapsed text]."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == f"h{self.level}":
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def rendered_headings(html: str) -> list:
    parser = _Headings()
    parser.feed(html)
    parser.close()
    return parser.found


def render_all(pages: list, jobs: int = 6) -> list:
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        return list(pool.map(render, pages))


def main() -> int:
    rows = json.loads(Path(sys.argv[1]).read_text())
    receipts = render_all([row["page"] for row in rows])
    out = [dict(row, headings=r["headings"], request_sha256=r["request_sha256"],
                response_sha256=r["response_sha256"]) for row, r in zip(rows, receipts)]
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
