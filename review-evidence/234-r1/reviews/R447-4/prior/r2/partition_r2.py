#!/usr/bin/env python3
"""Re-derive the round-2 'own logic of every instance outside u_nvm_port' partition.

Usage: partition_r2.py <evidence dir holding A/B-record-ooc-1x1.json>
Own logic of a listed instance = its figure minus its listed direct children.
Prints the term count, net and absolute LUT/FF over every listed instance
except u_pp/u_nvm_port and its listed descendants, the processor top's own
term, and whether the partition sums to the wrapper total minus u_nvm_port.
"""
import json
from pathlib import Path
import sys

ev = Path(sys.argv[1])
a, b = (json.loads((ev / f"{x}-record-ooc-1x1.json").read_text())["scopes"] for x in "AB")
CHANGED = "u_pp/u_nvm_port"


def parent(key):
    return "wrapper" if "/" not in key else key.rsplit("/", 1)[0]


def own(scopes, key, figure):
    kids = [k for k in scopes if k != "wrapper" and parent(k) == key]
    return scopes[key][figure] - sum(scopes[k][figure] for k in kids)


keys = sorted(set(a) | set(b))
assert set(a) == set(b), "instance sets differ"
nvm_kids = [k for k in keys if k.startswith(CHANGED + "/")]
terms = [k for k in keys if k != CHANGED and not k.startswith(CHANGED + "/")]
lut = {k: own(b, k, "LUT") - own(a, k, "LUT") for k in terms}
ff = {k: own(b, k, "FF") - own(a, k, "FF") for k in terms}
print(f"listed instances {len(keys)}; u_nvm_port listed descendants {nvm_kids}; terms {len(terms)}")
print(f"net LUT {sum(lut.values()):+d}, abs LUT {sum(map(abs, lut.values()))}; "
      f"net FF {sum(ff.values()):+d}, abs FF {sum(map(abs, ff.values()))}")
print(f"processor top own logic (u_pp): LUT {lut['u_pp']:+d}, FF {ff['u_pp']:+d}")
whole = {f: b["wrapper"][f] - a["wrapper"][f] for f in ("LUT", "FF")}
nvm = {f: b[CHANGED][f] - a[CHANGED][f] for f in ("LUT", "FF")}
print(f"wrapper {whole}, {CHANGED} {nvm}; wrapper - nvm = LUT {whole['LUT'] - nvm['LUT']:+d}, FF {whole['FF'] - nvm['FF']:+d}")
print("nonzero terms:", ", ".join(f"{k} {lut[k]:+d}/{ff[k]:+d}" for k in terms if lut[k] or ff[k]))
