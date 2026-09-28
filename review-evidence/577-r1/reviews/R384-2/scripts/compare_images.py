#!/usr/bin/env python3
"""Compare images_{base,r1,head}.txt: every (config, emitter) hash must match
across the three commits, and builder == SoC at each commit.
Also compare with the round-1 packet's builder hashes when given.
Usage: compare_images.py <receipts-dir> [<round-1 images_head.txt>]"""
import sys
from pathlib import Path
d = Path(sys.argv[1])
def load(p):
    out = {}
    for line in Path(p).read_text().splitlines():
        f = line.split()
        if len(f) == 4:
            out[(f[0], f[1])] = (f[2], f[3])
    return out
tabs = {t: load(d / f"images_{t}.txt") for t in ("base", "r1", "head")}
ok = True
keys = sorted(tabs["head"])
for t in ("base", "r1"):
    same = tabs[t] == tabs["head"]; ok &= same
    print(f"{t} vs head, both emitters, five configs: {'IDENTICAL' if same else 'DIFFERENT'} ({len(tabs[t])} vs {len(keys)} entries)")
for t, tab in tabs.items():
    cfgs = sorted({k[0] for k in tab})
    same = all(tab[(c, "builder")] == tab[(c, "soc")] for c in cfgs); ok &= same
    print(f"{t}: builder == SoC for all {len(cfgs)} configs: {same}")
if len(sys.argv) > 2:
    r1 = {}
    for line in Path(sys.argv[2]).read_text().splitlines():
        f = line.split()
        if len(f) == 3 and f[0] != "checker":
            r1[f[0]] = (f[1], f[2])
    same = all(tabs["head"][(c, "builder")] == r1[c] for c in r1) and len(r1) == 5; ok &= same
    print(f"round-1 packet builder hashes == this head: {same}")
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
