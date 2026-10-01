#!/usr/bin/env python3
"""Run the author's b5_attrib.py `figures` on the PUBLISHED inputs.

usage: r425_run_author_figures.py <author-r2 dir> <author (round-1) dir> [--bypass-record-hash]

First runs the tool unmodified. If the published derived record does not hash to
the value in a-long-reads.json, the unmodified run refuses; with
--bypass-record-hash the tool's sha256() is wrapped so that ONLY the record file
reports the hash the JSON expects, every other byte path is untouched, and the
figures are computed from the published (mismatching) bytes.
"""
import hashlib, importlib.util, io, json, sys, contextlib
from pathlib import Path

r2, r1 = Path(sys.argv[1]), Path(sys.argv[2])
bypass = "--bypass-record-hash" in sys.argv
spec = importlib.util.spec_from_file_location("b5_attrib", r2 / "tools/b5_attrib.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
meta = json.load(open(r2 / "receipts/a-long-reads.json"))
rec = r2 / "receipts" / meta["record"]["file"]
actual = hashlib.sha256(rec.read_bytes()).hexdigest()
print(f"record {rec.name}: {rec.stat().st_size} B, published sha256 {actual}")
print(f"expected by a-long-reads.json and the page: {meta['record']['sha256']}")
print(f"match: {actual == meta['record']['sha256']}")
if not bypass:
    try:
        m.figures(r1, r2 / "receipts")
        print("unmodified figures run: completed")
    except AssertionError as e:
        print(f"unmodified figures run: REFUSED (AssertionError {e!r})")
    sys.exit(0)
orig = m.sha256
m.sha256 = lambda p: meta["record"]["sha256"] if Path(p).resolve() == rec.resolve() else orig(p)
print("BYPASS: record-hash check wrapped for the record path only")
m.figures(r1, r2 / "receipts")
