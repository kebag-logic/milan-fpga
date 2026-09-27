#!/usr/bin/env python3
"""Tabulate ooc_probe.py results: post-map xc7 counts (LUT, LUTRAM, FF, RAM,
DSP, CARRY4) and the pre-LUT-mapping gate netlist, per shape, each variant
against base; and the post-map counts against the executor's published stat
files when a directory of them is given.

Usage: ooc_compare.py <ooc work dir> [published author dir]
"""
import json
import re
import sys
from pathlib import Path

W = Path(sys.argv[1])
PUB = Path(sys.argv[2]) if len(sys.argv) > 2 else None
SHAPES = ["endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"]


def summary(c):
    lut = sum(v for k, v in c.items() if re.fullmatch(r"LUT[1-6]", k))
    lutram = sum(v for k, v in c.items() if k.startswith("RAM") and not k.startswith("RAMB"))
    ff = sum(v for k, v in c.items() if re.fullmatch(r"FD[CPRS]E", k))
    return dict(LUT=lut, LUTRAM_cells=lutram, FF=ff, RAMB36=c.get("RAMB36E1", 0),
                RAMB18=c.get("RAMB18E1", 0), DSP=c.get("DSP48E1", 0), CARRY4=c.get("CARRY4", 0),
                MUXF7=c.get("MUXF7", 0), MUXF8=c.get("MUXF8", 0), INV=c.get("INV", 0))


def load(v, s):
    p = W / f"{v}-{s}.json"
    return json.loads(p.read_text()) if p.exists() else None


def gate_diff(a, b):
    keys = sorted(set(a) | set(b))
    return {k: b.get(k, 0) - a.get(k, 0) for k in keys if b.get(k, 0) != a.get(k, 0)}


for s in SHAPES:
    base = load("base", s)
    print(f"\n## {s}")
    for v in ["base", "head", "c1", "c2"]:
        r = load(v, s)
        if not r:
            print(f"{v:5} (missing)")
            continue
        sm = summary(r["post"])
        line = " ".join(f"{k}={val}" for k, val in sm.items())
        print(f"{v:5} rc={r['rc']} post-map: {line}")
        if v != "base" and base:
            bs = summary(base["post"])
            print(f"      post-map delta vs base: " + " ".join(
                f"{k}{sm[k]-bs[k]:+d}" for k in sm))
            print(f"      pre-LUT-map gate-netlist delta vs base: {gate_diff(base['pre_abc'], r['pre_abc'])}")
    head = load("head", s)
    for v in ["c2"]:
        r = load(v, s)
        if r and head:
            print(f"      c2 vs head post-map: " + " ".join(
                f"{k}{summary(r['post'])[k]-summary(head['post'])[k]:+d}" for k in summary(head["post"])))
            print(f"      c2 vs head pre-LUT-map: {gate_diff(head['pre_abc'], r['pre_abc'])}")
    if PUB:
        for v, tag in (("base", "before"), ("head", "after")):
            r = load(v, s)
            f = PUB / f"ooc-{tag}-{s}-stat.txt"
            if r and f.exists():
                pub = {}
                for line in f.read_text().splitlines():
                    m = re.match(r"\s+(\d+)\s+(\S+)$", line)
                    if m:
                        pub[m.group(2)] = int(m.group(1))
                same = all(pub.get(k) == r["post"].get(k) for k in pub if not k.startswith("$"))
                print(f"      {v} post-map cell counts vs published ooc-{tag}: "
                      f"{'IDENTICAL' if same else 'DIFFER ' + str(gate_diff(pub, r['post']))}")
    if base:
        print("      base pre-LUT-map gate census: " + ", ".join(
            f"{k}={v}" for k, v in sorted(base["pre_abc"].items()) if k.startswith("$_")))
