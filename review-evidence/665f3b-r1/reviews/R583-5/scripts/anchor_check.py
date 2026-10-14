"""R583-5: every Markdown link from the given pages into a .md#anchor must name a heading anchor of the target (GitHub slug rule).
Usage: python3 -I anchor_check.py <repo> <page>... ; prints each link and exits 1 on any unresolved anchor."""
import re, sys
from pathlib import Path

def slug(h):
    h = re.sub(r"[`*]|\[|\]\([^)]*\)", "", h.strip()).lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")

def anchors(p):
    out, seen = set(), {}
    fence = False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"#{1,6}\s+(.*)", line)
        if m:
            s = slug(m.group(1)); n = seen.get(s, 0); seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
        for a in re.findall(r'<a (?:name|id)="([^"]+)"', line):
            out.add(a)
    return out

repo = Path(sys.argv[1]); bad = 0; total = 0
for page in sys.argv[2:]:
    src = repo / page
    for target, frag in re.findall(r"\](?!\(https?:)\(([^)#\s]*\.md)#([^)\s]+)\)", src.read_text(encoding="utf-8")):
        dest = (src.parent / target).resolve() if target else src
        total += 1
        ok = dest.exists() and frag in anchors(dest)
        bad += not ok
        print(("ok  " if ok else "BAD ") + f"{page} -> {target}#{frag}")
print(f"anchor links: {total}, unresolved: {bad}")
sys.exit(1 if bad else 0)
