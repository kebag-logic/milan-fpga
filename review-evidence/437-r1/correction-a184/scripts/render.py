#!/usr/bin/env python3
"""Render synthetic pages with GitHub's Markdown API and keep exact receipts.

Each page is sent with exactly
    gh api markdown -f mode=gfm -f context=kebag-logic/milan-fpga -f text=<page>
Request bytes are the JSON body gh writes on the wire: compact, sorted keys,
with `<`, `>`, `&`, U+2028 and U+2029 escaped as Go's encoder escapes them.
The reconstruction is checked against the Content-Length gh reports under
GH_DEBUG=api (only that one header is read; nothing else from the debug
stream is kept). Response bytes are gh's stdout, byte for byte.

Usage: render.py IN.json OUT.json
IN is a list of {"id": ..., "page": ...}; OUT adds request/response bytes,
their SHA-256, the rendered heading list, the UTC time and the exit code.
A cache (OUT itself, if present) is reused unless --fresh is given.
"""
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_way import rendered  # noqa: E402

CONTEXT = "kebag-logic/milan-fpga"


def request_bytes(text: str) -> bytes:
    body = json.dumps({"context": CONTEXT, "mode": "gfm", "text": text},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    for char, esc in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                      (" ", "\\u2028"), (" ", "\\u2029")):
        body = body.replace(char, esc)
    return body.encode("utf-8")


def render_one(row: dict) -> dict:
    argv = ["gh", "api", "markdown", "-f", "mode=gfm", "-f", f"context={CONTEXT}",
            "-f", "text=" + row["page"]]
    utc = datetime.now(timezone.utc).isoformat()
    proc = subprocess.run(argv, capture_output=True, env={**__import__("os").environ,
                                                           "GH_DEBUG": "api"})
    length = None
    for line in proc.stderr.decode("utf-8", "replace").splitlines():
        if line.startswith("> Content-Length:"):
            length = int(line.split(":", 1)[1])
            break
    req = request_bytes(row["page"])
    resp = proc.stdout
    html = resp.decode("utf-8")
    return {**row,
            "argv_display": ["gh", "api", "markdown", "-f", "mode=gfm", "-f",
                             f"context={CONTEXT}", "-f", "text=<page>"],
            "request": {"context": CONTEXT, "mode": "gfm", "text": row["page"]},
            "request_bytes": req.decode("utf-8"),
            "request_sha256": hashlib.sha256(req).hexdigest(),
            "wire_content_length": length,
            "request_length_matches_wire": length == len(req),
            "response_bytes": html,
            "response_sha256": hashlib.sha256(resp).hexdigest(),
            "github": rendered(html),
            "utc": utc, "exit": proc.returncode}


def main() -> int:
    src, dst = sys.argv[1], sys.argv[2]
    fresh = "--fresh" in sys.argv
    rows = json.load(open(src))
    cache = {}
    if Path(dst).exists() and not fresh:
        cache = {r["page"]: r for r in json.load(open(dst)) if r.get("exit") == 0}
    todo = [r for r in rows if r["page"] not in cache]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for r in pool.map(render_one, todo):
            cache[r["page"]] = r
    out = [{**cache[r["page"]], "id": r["id"], **{k: v for k, v in r.items() if k != "page"}}
           for r in rows]
    json.dump(out, open(dst, "w"), indent=1, ensure_ascii=False)
    bad = [r["id"] for r in out if r["exit"] != 0 or not r["request_length_matches_wire"]]
    print(f"rendered {len(todo)} new, {len(out)} rows, problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
