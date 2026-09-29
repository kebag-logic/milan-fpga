#!/usr/bin/env python3
"""Check the round-2 retention manifest against the pages' raw-artifact rows
and the round-1 raw index, and the pages' tool rows against the redaction
record. Private storage is not read: this checks the public claims' closure.

usage: check_retention.py <repo-at-head> <author-r2-dir>
"""
import json
import re
import sys
from pathlib import Path

repo, pk = Path(sys.argv[1]), Path(sys.argv[2])
ROLE = {"alignment port log": "ptp4l-slave.log", "grandmaster port log": "ptp4l-gm.log"}
ROW = re.compile(r"^\| (\w[\w-]*) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|$", re.M)
TOOLROW = re.compile(r"^\| ([^|]+?) \| `([0-9a-f]{64})` \|$", re.M)
pages = {p: (repo / "docs/findings" / p).read_text() for p in ("599_394_E1_LINK_CYCLES.md", "387_SOFTWARE_GM_STEP.md")}
rows = {}
for p, t in pages.items():
    for m in ROW.finditer(t):
        a, art, n, h = m.groups()
        rows[f"{a}/{ROLE.get(art, art.strip('`'))}"] = (int(n), h, f"{p}:{t.count(chr(10), 0, m.start()) + 1}")
idx = {f["path"]: (f["bytes"], f["sha256"]) for f in json.loads((pk / "r1/RAW-ARTIFACTS.json").read_text())["files"]}
tsv = [x.split("\t") for x in (pk / "retention/MANIFEST.tsv").read_text().splitlines()[1:] if x.strip()]
ret = {r[0]: (int(r[1]), r[2], r[3]) for r in tsv}
s256 = {p.removeprefix("raw/"): h for h, p in (x.split(None, 1) for x in (pk / "retention/MANIFEST.sha256").read_text().splitlines() if x.strip())}
bad = 0
print(f"page raw rows {len(rows)}; raw index {len(idx)}; retention tsv {len(ret)}; retention sha256 {len(s256)}")
for k, (n, h, where) in rows.items():
    r = ret.get(k)
    if r is None or (r[0], r[1]) != (n, h) or idx.get(k) != (n, h) or r[2] != where:
        bad += 1
        print("  ROW MISMATCH", k, where, r, idx.get(k))
for k, v in idx.items():
    r = ret.get(k)
    if r is None or (r[0], r[1]) != v or s256.get(k) != v[1]:
        bad += 1
        print("  INDEX MISMATCH", k, v, r, s256.get(k))
extra = set(ret) - set(idx)
print(f"retention entries not in the raw index: {sorted(extra)}")
tagged = {k for k, r in ret.items() if r[2] != "-"}
print(f"retention entries tagged with a page row: {len(tagged)}; page rows: {len(rows)}; same set: {tagged == set(rows)}")
print(f"raw/retention/page closure mismatches: {bad}")
red = json.loads((pk / "r1/REDACTION.json").read_text())
orig = {x["original_sha256"]: x for x in red}
pub = {x.get("published_sha256"): x for x in red if x.get("published_sha256")}
print("\ntool and configuration rows (pages' Item/Tool tables) against the redacted packet:")
for p, t in pages.items():
    for m in TOOLROW.finditer(t):
        name, h = m.groups()
        if name.startswith(("Action", "Tool", "Item")):
            continue
        if h in pub:
            state = f"published byte-identical as r1/{pub[h]['file']}"
        elif h in orig:
            x = orig[h]
            state = (f"REDACTED in the packet: r1/{x['file']} now {str(x.get('published_sha256'))[:12]}; "
                     f"original hash only in REDACTION.json")
        elif h in {v[1] for v in idx.values()}:
            state = "raw-index file (private retention)"
        else:
            state = "not in the packet (external identity)"
        print(f"  {p}: {name.strip()[:60]:60s} {h[:12]} {state}")
sys.exit(1 if bad else 0)
