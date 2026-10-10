#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Supplementary reviewer control for PR #172, round 2 (graded like reviewer_controls_r2.py).

R_name_walk_one_short in reviewer_controls_r2.py edits the default branch of
the writer's sel_cnt_f, which only bounds scalar groups (chg_sel 0..5 each have
an explicit case), so it is an equivalent mutant and is not graded. This
replacement makes the restore walk end one record early in both passes: the
record of the table's last entry is never read or replayed, invisible at 128
entries and fatal at the bound capacity (ordinal 38 at 39, 106 at 107).

usage: reviewer_controls_r2b.py --root CLONE --output NEWDIR --verilator PATH
"""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "rc2", Path(__file__).resolve().parent / "reviewer_controls_r2.py")
rc2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc2)

CONTROL = ("R_restore_walk_one_short", rc2.WRITER,
           "          if (rec_r == RW_C'(N_REC_C - 1)) begin\n",
           "          if (rec_r == RW_C'(N_REC_C - 2)) begin\n",
           (r"N5 restored ordinal 38(?!\d)", r"N5 restored ordinal 106(?!\d)"), True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    a = ap.parse_args()
    a.output.mkdir(parents=True)
    rec = rc2.judge(CONTROL, a.root.resolve(), a.output.resolve(), a.verilator)
    (a.output / "results.json").write_text(json.dumps([rec], indent=2) + "\n")
    return 0 if rec["verdict"] == "KILLED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
