#!/usr/bin/env python3
"""Tabulate link_points.sh output for two trees: needs, plans, flat spans, fill and headroom.

usage: fit_summary.py <links-dir-a> <links-dir-b>

Headroom is the bytes either image could add before ctrl_memory's 56-RAMB36
budget refuses it: whole free RAMB18 granules (2,048 B) up to 112, plus the
unused bytes inside the planned banks.
"""
import json
import re
import sys
from pathlib import Path

POINTS = ("1x1_tdm8_i1", "1x1_tdm8_i2", "8x8_i1", "8x8_i2")
for links in map(Path, sys.argv[1:3]):
    print(f"== {links.name}")
    for p in POINTS:
        d = json.loads((links / f"{p}_split.plan").read_text())
        span = int(re.search(r'"ram_span": (\d+)', (links / f"{p}_flat.log").read_text()).group(1))
        fill = [100 * d[r]["bytes"] / sum(d[r]["banks"]) for r in ("rom", "sram")]
        granules = sum(-(-d[r]["bytes"] // 2048) for r in ("rom", "sram"))
        slack = sum(sum(d[r]["banks"]) - d[r]["bytes"] for r in ("rom", "sram"))
        print(f"{p}: rom {d['rom']['bytes']} {d['rom']['banks']} sram {d['sram']['bytes']} {d['sram']['banks']} "
              f"planned {d['tiles']} flat_span {span} floor {-(-span // 4096)} "
              f"fill rom {fill[0]:.1f}% sram {fill[1]:.1f}% headroom {(112 - granules) * 2048 + slack} B")
