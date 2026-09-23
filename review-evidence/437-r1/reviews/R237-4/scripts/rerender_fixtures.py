#!/usr/bin/env python3
"""Re-render every committed #437 fixture shape fresh and compare with the
recorded receipt: request bytes as recorded are re-sent verbatim, and the
fresh response bytes and headings are compared with the recorded ones.

Usage: rerender_fixtures.py <head-scripts-dir> <cache-dir> <out.json>
"""
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import headings  # noqa: E402

FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
            "gen_toc_container_walk.json")


def fresh(cache: Path, shape: dict) -> dict:
    request = shape["request_bytes"].encode()
    key = hashlib.sha256(request).hexdigest()
    entry = cache / ("fixture-" + key + ".json")
    if entry.exists():
        rec = json.loads(entry.read_text())
    else:
        proc = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=request,
                              capture_output=True, check=False)
        rec = {"request_sha256": key, "exit": proc.returncode,
               "response_bytes": proc.stdout.decode("utf-8", "surrogateescape"),
               "response_sha256": hashlib.sha256(proc.stdout).hexdigest(),
               "utc": datetime.now(timezone.utc).isoformat()}
        if proc.returncode == 0:
            entry.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return rec


def main() -> int:
    head, cache, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    cache.mkdir(parents=True, exist_ok=True)
    rows = []
    for fixture in FIXTURES:
        shapes = json.loads((head / fixture).read_text())["shapes"]
        with ThreadPoolExecutor(6) as pool:
            recs = list(pool.map(lambda s: fresh(cache, s), shapes))
        for s, rec in zip(shapes, recs):
            req_ok = hashlib.sha256(s["request_bytes"].encode()).hexdigest() == s["request_sha256"]
            page_ok = json.loads(s["request_bytes"]) == {"context": "kebag-logic/milan-fpga",
                                                         "mode": "gfm", "text": s["page"]}
            rows.append({"fixture": fixture, "name": s["name"], "exit": rec["exit"],
                         "request_matches_page": req_ok and page_ok,
                         "response_identical": rec["response_sha256"] == s["response_sha256"],
                         "fresh_headings": headings(rec["response_bytes"]),
                         "recorded_headings": s["headings"],
                         "headings_identical": headings(rec["response_bytes"]) == s["headings"],
                         "fresh_utc": rec["utc"]})
    out.write_text(json.dumps(rows, indent=1))
    n = len(rows)
    print("shapes:", n)
    print("exit 0:", sum(r["exit"] == 0 for r in rows))
    print("request bytes carry the page (context/mode/text) and hash:", sum(r["request_matches_page"] for r in rows))
    print("fresh response byte-identical:", sum(r["response_identical"] for r in rows))
    print("fresh headings identical:", sum(r["headings_identical"] for r in rows))
    for r in rows:
        if not r["response_identical"] or not r["headings_identical"]:
            print("  DIFF", r["fixture"], r["name"], r["recorded_headings"], r["fresh_headings"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
