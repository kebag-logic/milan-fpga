"""Resolve in-page fragment links on given lines against GitHub-style heading slugs,
name each target's parent level-2 section, and show that a mutant fragment fails.

Usage: python3 -I anchor_check.py <page> <line> [<line> ...]
"""
import re, sys

page = sys.argv[1]
want = [int(x) for x in sys.argv[2:]]
lines = open(page, encoding="utf-8").read().splitlines()
slugs, parent, h2 = {}, {}, None
fenced = False
for n, raw in enumerate(lines, 1):
    if raw.strip().startswith(("```", "~~~")):
        fenced = not fenced
    if fenced:
        continue
    m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", raw)
    if not m:
        continue
    title = re.sub(r"`", "", m.group(2))
    slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
    base, k = slug, 1
    while slug in slugs:
        slug = f"{base}-{k}"; k += 1
    slugs[slug] = n
    if len(m.group(1)) == 2:
        h2 = (n, m.group(2))
    parent[slug] = h2
for ln in want:
    for frag in re.findall(r"\]\(#([^)]+)\)", lines[ln - 1]):
        if frag in slugs:
            print(f"line {ln} #{frag} RESOLVES -> heading line {slugs[frag]}; level-2 parent: line {parent[frag][0]} '{parent[frag][1]}'")
        else:
            print(f"line {ln} #{frag} MISSING")
mut = "firmware-and-block-ram-ledgerx"
print(f"control #{mut}", "RESOLVES" if mut in slugs else "MISSING")
