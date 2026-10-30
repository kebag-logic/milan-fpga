#!/usr/bin/env python3
"""Resolve every relative Markdown link with a #fragment against GitHub-style
heading slugs. Usage: check_anchors.py <repo-root> <page>..."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
def slugs(path):
    out, seen = set(), {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m: continue
        s = re.sub(r"[^\w\- ]", "", m.group(2).strip().lower().replace("`", "")).replace(" ", "-")
        n = seen.get(s, 0); seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out
bad = 0; total = 0
for page in sys.argv[2:]:
    p = root / page
    for m in re.finditer(r"\]\(([^)\s]+)\)", p.read_text(encoding="utf-8")):
        url = m.group(1)
        if url.startswith(("http", "mailto")) or "#" not in url: continue
        target, frag = url.split("#", 1)
        t = (p.parent / target).resolve() if target else p
        total += 1
        ok = t.is_file() and frag in slugs(t)
        bad += not ok
        print(("OK  " if ok else "BAD ") + f"{page} -> {url}")
print(f"anchors: {total} checked, {bad} unresolved"); sys.exit(1 if bad else 0)
