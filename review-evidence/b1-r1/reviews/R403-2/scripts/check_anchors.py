#!/usr/bin/env python3
"""Resolve every relative Markdown link with a #fragment in the two B1 pages
against GitHub-style heading slugs of the target file at the checkout.

usage: check_anchors.py <repo-at-head>
"""
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
PAGES = ["docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"]


def slugs(path):
    out, seen = set(), {}
    for line in path.read_text().splitlines():
        m = re.match(r"^#{1,6} (.*)$", line)
        if not m:
            continue
        s = re.sub(r"[^\w\- ]", "", m.group(1).strip().lower().replace("`", "")).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


bad = 0
for page in PAGES:
    p = repo / page
    for m in re.finditer(r"\]\(([^)\s]*?)#([^)\s]+)\)", p.read_text()):
        target, frag = m.group(1), m.group(2)
        if target.startswith("http"):
            continue
        t = (p.parent / target).resolve() if target else p
        ok = t.exists() and frag in slugs(t)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {page} -> {target or '(self)'}#{frag}")
print(f"unresolved anchors: {bad}")
sys.exit(1 if bad else 0)
