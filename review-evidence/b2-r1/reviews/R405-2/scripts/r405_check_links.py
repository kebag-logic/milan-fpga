#!/usr/bin/env python3
"""Resolve every relative link and #anchor in the given pages (GitHub slug rule).
usage: check_links.py <repo root> <page>..."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); bad = 0
def slugs(p):
    out, seen = set(), {}
    infence = False
    for l in p.read_text().splitlines():
        if l.startswith("```"):
            infence = not infence
        if infence:
            continue
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", l)
        if m:
            s = re.sub(r"[^\w\- ]", "", m[1].replace("`", "").lower()).replace(" ", "-")
            n = seen.get(s, 0); seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
    return out
for page in sys.argv[2:]:
    pg = root / page
    for m in re.finditer(r"\]\(([^)\s]+)\)", pg.read_text()):
        url = m[1]
        if url.startswith("http"):
            continue
        path, _, anc = url.partition("#")
        tgt = (pg.parent / path).resolve() if path else pg
        ok = tgt.exists() and (not anc or anc in slugs(tgt))
        bad += not ok
        print(("OK   " if ok else "FAIL ") + f"{page} -> {url}")
print("FAILURES:", bad)
