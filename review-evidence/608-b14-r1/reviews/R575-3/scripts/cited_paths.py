#!/usr/bin/env python3
"""List every backticked packet path cited by the B14 page and check it exists
under an extracted review-evidence/608-b14-r1/author/ tree.
usage: cited_paths.py <page.md> <author-dir>"""
import glob, os, re, sys
page, au = sys.argv[1], sys.argv[2]
PREFIX = ("item", "soak/", "restore/", "maap/", "round2-recompute/", "raw-index/", "tools/")
toks = []
for n, line in enumerate(open(page, encoding="utf-8"), 1):
    for t in re.findall(r"`([^`]+)`", line):
        if t.startswith(PREFIX) and ("/" in t or "." in t):
            toks.append((n, t))
bad = 0
seen = set()
for n, t in toks:
    if t in seen:
        continue
    seen.add(t)
    pat = t.replace("NNN", "[0-9][0-9][0-9]")
    hits = glob.glob(os.path.join(au, pat))
    ok = bool(hits)
    bad += not ok
    print(f"{'OK  ' if ok else 'MISS'} line {n:4d} {t} ({len(hits)} match)")
# bare file names cited in a record row next to a cited directory, e.g. `acmp.tsv`
print(f"distinct cited paths {len(seen)}; missing {bad}")
sys.exit(1 if bad else 0)
