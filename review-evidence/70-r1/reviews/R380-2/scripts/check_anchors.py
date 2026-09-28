#!/usr/bin/env python3
"""Check every relative Markdown link with a #fragment in the given pages
resolves to a GitHub-style heading slug (or explicit <a id>) in its target.
Run from the repository root. Exit 0 iff all resolve."""
import re, sys, os
def slugs(path):
    out, seen = set(), {}
    txt = open(path, encoding='utf-8').read()
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    for line in txt.splitlines():
        m = re.match(r'^#{1,6}\s+(.*?)\s*#*\s*$', line)
        if m:
            h = re.sub(r'<[^>]+>', '', m.group(1))
            h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
            s = re.sub(r'[^\w\- ]', '', h.lower().replace('`', '')).replace(' ', '-')
            n = seen.get(s, 0); seen[s] = n + 1
            out.add(s if n == 0 else f'{s}-{n}')
        for a in re.findall(r'<a id="([^"]+)"', line):
            out.add(a)
    return out
bad = 0; total = 0
for page in sys.argv[1:]:
    base = os.path.dirname(page)
    for n, line in enumerate(open(page, encoding='utf-8'), 1):
        for tgt in re.findall(r'\]\(([^)\s]+)\)', line):
            if tgt.startswith('http') or '#' not in tgt: continue
            f, frag = tgt.split('#', 1)
            p = os.path.normpath(os.path.join(base, f)) if f else page
            total += 1
            if not os.path.exists(p) or frag not in slugs(p):
                bad += 1; print(f'UNRESOLVED {page}:{n} -> {tgt}')
print(f'checked {total} fragment links, unresolved {bad}')
sys.exit(1 if bad else 0)
