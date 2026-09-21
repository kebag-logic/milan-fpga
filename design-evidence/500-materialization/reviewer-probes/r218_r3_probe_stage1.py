# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R218's round-three six-case reproduction, ADAPTED to run against the
revision-d evidence.

The original is the Python snippet in review-evidence/503-round3/reviews/
R218/REVIEW.md at commit 3d790bc1 (R3-F1, "R3-F1 can be reproduced after
that build using the immutable runner's public Python API"). It crafts the
selector-only slot (configuration 0x00 = 0000, clock source 0x0a = 0001,
presentation offset 0x50 = 1500000, every other record erased) and runs
V21_desc_late_after_apply, V21b_desc_debt_outlasts_the_store and
V20b_desc_error_once_after_apply on the full run's base-1x1 and
mut-R03_rollback_skips_desc_store binaries. The adaptations, and the only
ones:

1. PATH CONSTANTS come from the environment: PROBE_OUT (a scratch directory,
   required), FULL_OUT (the full run's D3_OUT, whose build/ it reads) and
   EVIDENCE (the proposal-evidence directory, default this file's sibling).
2. TWO MORE BUILDS, the ones revision d adds for the finding: the stage-1
   base (base-1x1-stage1: stage 1's roll-back scope, the dynamic-state store
   and the descriptor store, without the map plane) and its deletion mutant
   mut-ST1_stage1_rollback_skips_desc_store (the round-three stage-1 scope).

Every case, slot value and reading is the reviewer's. It writes
stage1-probe.json under PROBE_OUT/r218r3; r218_r3_check.py grades it.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys

scratch = Path(os.environ["PROBE_OUT"]) / "r218r3"
full = Path(os.environ["FULL_OUT"])
ev = Path(os.environ.get("EVIDENCE", Path(__file__).resolve().parents[1] / "proposal-evidence"))
os.environ["D3_OUT"] = str(scratch / "d3")
spec = importlib.util.spec_from_file_location("r218_r3_d3", ev / "run.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
s = m.prep_shape("1x1")
slots = m.crafted(s, "stage1-only", {
    0x00: bytes.fromhex("0000"),
    0x0a: bytes.fromhex("0001"),
    0x50: (1500000).to_bytes(4, "big"),
})
rows = []
for name in ("base-1x1", "mut-R03_rollback_skips_desc_store", "base-1x1-stage1",
             "mut-ST1_stage1_rollback_skips_desc_store"):
    b = m.Build(name, "1x1", binary=full / "build" / name / "obj/d3sim")
    for case in ("V21_desc_late_after_apply", "V21b_desc_debt_outlasts_the_store", "V20b_desc_error_once_after_apply"):
        r = m.run_case(b, s, case, slots=slots)
        g = m.Grade(r, s)
        t = r.obs.get("terminal", {})
        row = {"build": name, "case": case, "rc": r.rc, "done": r.done, "terminal": g.boot().get("terminal"),
               "enable": g.boot().get("enable"), "abort": g.boot().get("abort"), "rb_end": g.boot().get("rb_end"),
               "late_beat": g.boot().get("desc_delay_beat"), "accepted": g.boot().get("desc_delay_acc"),
               "d3_done": t.get("d3_done"), "d3_fail": t.get("d3_fail"), "d3_rb": t.get("d3_rb"),
               "d3_closed": t.get("d3_closed"), "own": t.get("own"),
               "mismatches": g.mismatches(r.snaps.get("terminal"), {})}
        rows.append(row)
        print(json.dumps(row), flush=True)
(scratch / "stage1-probe.json").write_text(json.dumps(rows, indent=2))
