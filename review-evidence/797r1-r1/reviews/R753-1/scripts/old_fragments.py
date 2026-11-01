#!/usr/bin/env python3
"""List old-page fragments absent from the new page. A fragment is a non-empty
table cell or a prose line of the old page, whitespace-normalised, with em dashes
folded to --. Usage: old_fragments.py <old> <new>"""
import re, sys
def norm(s):
    s = s.replace("—", "--").replace("–", "-")
    s = re.sub(r"\.\./\.\./", "", s)
    s = re.sub(r"\]\(\.\./", "](", s)
    s = re.sub(r"\]\(([\w_]+\.md)", r"](\1", s)
    return " ".join(s.split())
old = open(sys.argv[1], encoding="utf-8").read()
new = norm(open(sys.argv[2], encoding="utf-8").read())
frags, fence = [], False
for n, line in enumerate(old.splitlines(), 1):
    if line.startswith("```"):
        fence = not fence
        continue
    t = line.strip()
    if not t or re.fullmatch(r"\|?[-:| ]+\|?", t) or t.startswith("#"):
        continue
    if t.startswith("|"):
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", t.strip("|"))]
        for c in cells:
            if len(c) > 25:
                frags.append((n, c))
    elif len(t) > 25:
        frags.append((n, t))
missing = []
for n, f in frags:
    if norm(f) not in new:
        missing.append((n, f))
print("fragments", len(frags), "absent verbatim", len(missing))
for n, f in missing:
    print(f"{n}: {f}")
