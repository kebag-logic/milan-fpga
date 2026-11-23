#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Count every mutation anchor of the two existing presentation-stage
campaigns against the base and head sources, exactly as each campaign's own
refusal does (`src.count(pattern) != 1` is a [FAIL] arm).

Usage: anchor_counts.py <exported head tree> <git checkout> <base rev> <head rev>
Imports only the campaigns' mutation tables; builds nothing.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

tree, checkout, base_rev, head_rev = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def show(rev, rel):
    return subprocess.check_output(["git", "-C", checkout, "show", f"{rev}:{rel}"], text=True)


bad = 0
rq = load(tree / "tb/verilator/render_queue/mutants.py", "rq_mutants")
rq_rel = "hdl/ieee1722/aaf/KL_render_queue.sv"
table = [m for m in vars(rq).values() if isinstance(m, (list, tuple)) and m and isinstance(m[0], tuple)
         and len(m[0]) >= 2 and isinstance(m[0][0], str) and isinstance(m[0][1], tuple)]
for entry in table[0]:
    name, edits = entry[0], entry[1]
    for old, _new in edits:
        b, h = show(base_rev, rq_rel).count(old), show(head_rev, rq_rel).count(old)
        flag = "" if h == 1 else "   <-- arm refuses at head"
        bad += h != 1
        print(f"render_queue/mutants.py  {name!r}: base {b}, head {h}{flag}")
dp = load(tree / "tb/verilator/milan_dp/render_mutants.py", "dp_render_mutants")
for name, source, pattern, _replacement, _mode, _breaks in dp.MUTATIONS:
    path, _override = dp.SOURCES[source]
    rel = str(Path(path).resolve().relative_to(tree.resolve()))
    b, h = show(base_rev, rel).count(pattern), show(head_rev, rel).count(pattern)
    flag = "" if h == 1 else "   <-- arm refuses at head"
    bad += h != 1
    print(f"milan_dp/render_mutants.py {name!r} ({rel}): base {b}, head {h}{flag}")
print("ANCHORS", "BROKEN" if bad else "INTACT", bad)
