#!/usr/bin/env python3
"""Check every fragment link in the changed pages resolves to a heading slug
(GitHub rule: lowercase, drop punctuation except '-' and ' ', spaces to '-').

Usage: check_anchors.py <repo root> <page> [...]
"""
import os, re, sys

root = sys.argv[1]


def slugs(path):
    out, seen = set(), {}
    fence = False
    for line in open(path):
        if line.startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            s = m.group(2).strip().lower()
            s = re.sub(r"[`*_]", "", s)
            s = re.sub(r"[^\w\- ]", "", s)
            s = s.replace(" ", "-")
            n = seen.get(s, 0)
            seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
    return out


bad = 0
for page in sys.argv[2:]:
    p = os.path.join(root, page)
    for ln, line in enumerate(open(p), 1):
        for m in re.finditer(r"\]\(([^)\s]*?)#([^)\s]+)\)", line):
            tgt, frag = m.group(1), m.group(2)
            if tgt.startswith("http"):
                continue
            tp = os.path.normpath(os.path.join(os.path.dirname(p), tgt)) if tgt else p
            ok = os.path.exists(tp) and frag in slugs(tp)
            print(f"{page}:{ln} -> {tgt or '(self)'}#{frag}: {'OK' if ok else 'MISSING'}")
            bad += not ok
        for m in re.finditer(r"\]\(([^)#\s]+)\)", line):
            tgt = m.group(1)
            if tgt.startswith("http"):
                continue
            tp = os.path.normpath(os.path.join(os.path.dirname(p), tgt))
            if not os.path.exists(tp):
                print(f"{page}:{ln} -> {tgt}: MISSING FILE"); bad += 1
print("RESULT", "PASS" if bad == 0 else f"FAIL {bad}")
