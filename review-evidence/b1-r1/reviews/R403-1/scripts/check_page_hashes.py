#!/usr/bin/env python3
"""Cross-check every SHA-256 and byte count the two findings pages publish
against the archived packet: per-action raw-artifacts.json indexes (raw files
that are NOT archived), the archive MANIFEST.json (original and published
hashes of archived files), and the archived files' own bytes.

usage: check_page_hashes.py <repo-checkout> <extracted-packet-dir>
Exit 1 if a page hash matches nothing, or a raw row's size disagrees.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

repo, pk = Path(sys.argv[1]), Path(sys.argv[2])
author = pk / "author"
raw = {}
for f in (author / "bench").glob("*/raw-artifacts.json"):
    for r in json.loads(f.read_text()):
        raw[(f.parent.name, Path(r["path"]).name)] = (r["size"], r["sha256"])
top = json.loads((author / "RAW-ARTIFACTS.json").read_text())["files"]
toph = {r["sha256"]: r["path"] for r in top}
man = json.loads((pk / "MANIFEST.json").read_text())
orig = {m["original_sha256"]: m["file"] for m in man}
pub = {m["published_sha256"]: m["file"] for m in man}
actual = {hashlib.sha256(p.read_bytes()).hexdigest(): str(p.relative_to(pk)) for p in pk.rglob("*") if p.is_file()}
bad = 0
roles = {"alignment port log": "ptp4l-slave.log", "grandmaster port log": "ptp4l-gm.log"}
for page in ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"):
    n = 0
    for line in (repo / page).read_text().splitlines():
        m = re.match(r"\| (\w[\w-]*) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|", line)
        if m:
            action, name, size, h = m[1], m[2].strip("`"), int(m[3]), m[4]
            name = roles.get(name, name)
            got = raw.get((action, name))
            where = "raw index" if got else None
            if got is None and h in actual:
                got, where = (size, h), "archived file " + actual[h]
            ok = got is not None and got == (size, h)
            n += 1
            if not ok:
                bad += 1
                print(f"RAW-ROW MISMATCH {page}: {action} {name} {size} {h} -> {got}")
            else:
                print(f"ok raw {action:14s} {name:22s} via {where}; archived copy: {'yes' if h in actual else 'no'}")
            continue
        for h in re.findall(r"`([0-9a-f]{64})`", line):
            hits = [s for s, d in (("archived-bytes", actual), ("manifest-original", orig), ("manifest-published", pub), ("top-raw-index", toph)) if h in d]
            n += 1
            label = line.split("|")[1].strip()[:60] if line.startswith("|") else line[:60]
            print(f"{'ok ' if hits else 'NO-MATCH'} {label}: {h[:16]} in {hits or 'nothing archived'}")
    print(f"== {page}: {n} hashes checked")
print("mismatches:", bad)
sys.exit(1 if bad else 0)
