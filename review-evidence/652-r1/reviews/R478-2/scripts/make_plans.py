#!/usr/bin/env python3
"""Write the planted sweep plans this review feeds the shapes step, each a
copy of the tracked syn/resmap/sweep_plan.json with one change.
Usage: make_plans.py <clone> <out dir>"""
import json
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]), Path(sys.argv[2])
base = json.loads((clone / "syn/resmap/sweep_plan.json").read_text())
A, B, T = "rm_ax7101_8x8_tdm8", "rm_ax7101_8x8_tdm8_2ch", "rm_ax7101_2x2_tdm8"
FOREIGN = "the board section names no part"


def plan(name, change):
    p = json.loads(json.dumps(base))
    change(p["variants"])
    (out / f"{name}.json").write_text(json.dumps(p, indent=1) + "\n")


plan("p0-tracked-control", lambda v: None)
plan("p1-foreign-cause-both", lambda v: [v[n].update(cause=FOREIGN) for n in (A, B)])
plan("p2-foreign-cause-one", lambda v: v[B].update(cause=FOREIGN))
plan("p3-no-marks", lambda v: [(v[n].pop("expect"), v[n].pop("cause")) for n in (A, B)])
plan("p4-2x2-expected-refused", lambda v: v[T].update(expect="refused", cause="writable names"))
plan("p5-refusal-without-cause", lambda v: v[A].pop("cause"))
plan("p6-cause-on-built", lambda v: v[T].update(cause="writable names"))
plan("p7-empty-cause", lambda v: v[A].update(cause=""))
