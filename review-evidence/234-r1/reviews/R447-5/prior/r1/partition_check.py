#!/usr/bin/env python3
"""Recompute the B-minus-A 1x1 standalone 'blocks B did not change' aggregates.

Usage: partition_check.py <evidence dir holding A/B-record-ooc-1x1.json>
Prints the net and absolute LUT/FF movement, excluding u_pp/u_nvm_port (the one
changed block), under three partitions of the published scopes, to compare with
docs/findings/234_PP_SHADOW_AREA_BASELINE.md:134-135 and docs/design/AREA_BUDGET.md:156.
"""
import json
from pathlib import Path
import sys

ev = Path(sys.argv[1])
a = json.loads((ev / "A-record-ooc-1x1.json").read_text())["scopes"]
b = json.loads((ev / "B-record-ooc-1x1.json").read_text())["scopes"]
CHANGED = "u_pp/u_nvm_port"


def kids(key, scopes):
    if key == "wrapper":
        return [k for k in scopes if k != "wrapper" and "/" not in k]
    return [k for k in scopes if k.startswith(key + "/") and k.count("/") == key.count("/") + 1]


def delta(key, figure, own=False):
    if own and kids(key, a):
        mine = lambda s: s[key][figure] - sum(s[k][figure] for k in kids(key, s))
        return mine(b) - mine(a)
    return b[key][figure] - a[key][figure]


keys = sorted(set(a) | set(b))
leaves = [k for k in keys if k != "wrapper" and not kids(k, a)]
children = [k for k in keys if k.count("/") == 1 and k.startswith("u_pp/")]
pools = [k for k in children if k.startswith("u_pp/g_rx_pool")]
partitions = {
    "leaf scopes (incl. u_nvm, ctl_fifo)": [(k, False) for k in leaves],
    "u_pp direct children, RX pools grouped (excl. u_nvm)": [(k, False) for k in children if k not in pools],
    "every scope's own logic (complete partition of the wrapper)": [(k, True) for k in keys],
}
for name, members in partitions.items():
    members = [(k, own) for k, own in members if k != CHANGED]
    lut = [delta(k, "LUT", own) for k, own in members]
    ff = [delta(k, "FF", own) for k, own in members]
    if name.startswith("u_pp direct"):
        lut.append(sum(delta(k, "LUT") for k in pools))
        ff.append(sum(delta(k, "FF") for k in pools))
    print(f"{name}: net LUT {sum(lut):+d}, abs LUT {sum(map(abs, lut))}, net FF {sum(ff):+d}")
print(f"u_pp own logic: LUT {delta('u_pp', 'LUT', True):+d}, FF {delta('u_pp', 'FF', True):+d}")
print(f"wrapper total: LUT {delta('wrapper', 'LUT'):+d}, FF {delta('wrapper', 'FF'):+d}; "
      f"{CHANGED}: LUT {delta(CHANGED, 'LUT'):+d}, FF {delta(CHANGED, 'FF'):+d}")
print("documented: findings :134-135 net +101 LUT, abs 309 LUT; AREA_BUDGET :156 net 101 LUT and 95 FF")
