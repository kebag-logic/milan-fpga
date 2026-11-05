#!/usr/bin/env python3
"""walk_counts.py <head_dir> <base_dir>: per-shape FAIL counts of every arm log."""
import re, sys, pathlib
def counts(p):
    c = {"1/1": 0, "2/2": 0, "3/5": 0, "9/9": 0}
    for line in p.read_text(errors="replace").splitlines():
        if line.startswith("FAIL:"):
            m = re.search(r"\[(\d+/\d+)\]\s*$", line)
            if m and m.group(1) in c: c[m.group(1)] += 1
    return c
h, b = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
print("| arm | head 1/1 2/2 3/5 9/9 | base 1/1 2/2 3/5 9/9 | moved |")
print("|---|---|---|---|")
for f in sorted(h.glob("*.log")):
    if f.name.startswith("control-"): continue
    ch = counts(f); bf = b / f.name
    cb = counts(bf) if bf.exists() else None
    hs = " ".join(str(ch[k]) for k in ch); bs = " ".join(str(cb[k]) for k in cb) if cb else "-"
    print(f"| {f.stem} | {hs} | {bs} | {'MOVED' if cb and cb != ch else ''} |")
