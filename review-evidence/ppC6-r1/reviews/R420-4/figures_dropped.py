#!/usr/bin/env python3
"""Per round section, list every bare number (1,234 / 12 / 0.5) of an older PR
body's section that appears nowhere in the newer body's same section, with its
context. usage: figures_dropped.py OLD.md NEW.md"""
import re, sys
NUM = re.compile(r"(?<![\w.`])\d{1,3}(?:,\d{3})+(?![\w])|(?<![\w.`])\d+(?:\.\d+)?(?![\w`])")
def sections(path):
    out, cur = {}, "Round 1"
    for line in open(path):
        m = re.match(r"^## (Round 4b|Round 4|Round 3|Round 2)\b", line)
        if m:
            cur = m.group(1)
        out.setdefault(cur, []).append(line)
    return {k: "".join(v) for k, v in out.items()}
old, new = sections(sys.argv[1]), sections(sys.argv[2])
for sec, text in old.items():
    have = set(NUM.findall(new.get(sec, "")))
    seen = set()
    for m in NUM.finditer(text):
        n = m.group(0)
        if n in have or n in seen:
            continue
        seen.add(n)
        ctx = text[max(0, m.start() - 70): m.end() + 40].replace("\n", " ")
        print(f"[{sec}] {n}: ...{ctx}...")
