#!/usr/bin/env python3
"""Resolve every '#fragment' link in the given Markdown pages against GitHub-
style heading slugs of the target page (same page or relative path).
Usage: check_fragments.py <repo> <page> [<page> ...]"""
import re, sys
from pathlib import Path

repo = Path(sys.argv[1])

def slugs(page: Path):
    out, seen, fence = set(), {}, False
    for line in page.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        s = m.group(2).strip().lower()
        s = re.sub(r"[^\w\- ]", "", s).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out

bad = 0
for rel in sys.argv[2:]:
    page = repo / rel
    for m in re.finditer(r"\]\(([^)\s]*)#([^)\s]+)\)", page.read_text(encoding="utf-8")):
        target, frag = m.group(1), m.group(2)
        if target.startswith("http"):
            continue
        tpage = page if target == "" else (page.parent / target).resolve()
        if not tpage.exists() or tpage.suffix != ".md":
            continue
        ok = frag in slugs(tpage)
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {rel} -> {target or '(self)'}#{frag}")
print(f"fragments bad={bad}")
sys.exit(1 if bad else 0)
