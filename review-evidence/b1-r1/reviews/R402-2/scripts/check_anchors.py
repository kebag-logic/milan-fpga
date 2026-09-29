#!/usr/bin/env python3
"""Resolve every relative link and #anchor in the two pages against headings at the head
(GitHub slug rule: lowercase, drop punctuation except '-' and '_', spaces to '-').
usage: check_anchors.py <repo-root>"""
import re, sys
from pathlib import Path
R = Path(sys.argv[1]); bad = 0
def slugs(p):
    out = set()
    for l in p.read_text().splitlines():
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", l)
        if m:
            s = re.sub(r"[^\w\- ]", "", m[1].replace("`", "").lower()).replace(" ", "-")
            out.add(s)
    return out
for page in ["docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"]:
    P = R / page
    for tgt in re.findall(r"\]\(([^)\s]+)\)", P.read_text()):
        if tgt.startswith("http"):
            continue
        path, _, frag = tgt.partition("#")
        f = (P.parent / path).resolve() if path else P
        ok = f.exists() and (not frag or frag in slugs(f))
        bad += not ok
        print(("PASS " if ok else "FAIL ") + page + " -> " + tgt)
sys.exit(1 if bad else 0)
