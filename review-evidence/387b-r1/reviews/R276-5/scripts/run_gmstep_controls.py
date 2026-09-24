#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-5 reviewer probe: run the head's own gmstep_mutants controls, chosen
by index, plus reviewer-added controls, through the head's own runner
functions (plant, build through the Makefile recipe, grade by the leg's own
verdict). Nothing in the tree is edited: planted copies go to a work dir.

Usage: run_gmstep_controls.py <milan_dp dir> <workdir> [--head I ...] [--extra NAME ...]
Prints one line per control and exits 1 if any control survived or the
positive legs fail.
"""
import argparse
import importlib.util
import sys
from pathlib import Path


def load(milan_dp: Path):
    spec = importlib.util.spec_from_file_location("gmstep_mutants", milan_dp / "gmstep_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extras(m):
    """Reviewer-added controls; each must be caught by the named check."""
    dup = ("  logic [11:0] rv_dup_cnt_r;\n"
           "  logic rv_dup_arm_r;\n"
           "  always_ff @(posedge axis_clk) begin : rv_dup\n"
           "    if (!axis_resetn) begin rv_dup_cnt_r <= '0; rv_dup_arm_r <= 1'b0; end\n"
           "    else if (media_rebase_p_w) begin rv_dup_cnt_r <= 12'd3000; rv_dup_arm_r <= 1'b1; end\n"
           "    else if (rv_dup_arm_r && rv_dup_cnt_r != 0) rv_dup_cnt_r <= rv_dup_cnt_r - 1'b1;\n"
           "    else rv_dup_arm_r <= 1'b0;\n"
           "  end : rv_dup\n"
           "  wire rv_dup_p_w = rv_dup_arm_r && (rv_dup_cnt_r == 12'd1);\n")
    anchor = "  wire mcr_restart_p_w = (crf_clk_selected_r\n"
    return {
        # a step that restarts the media clock TWICE (a second request 3000
        # cycles later, after the first toggle's PDUs are out): the exactly-
        # once check must see the upper side, not only "at least one"
        "step_toggles_twice_gmstep": m.Control(
            "R276: the step requests a second restart 3000 cycles later", "datapath",
            anchor + "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))\n"
                     "                       | media_rebase_p_w;",
            dup + anchor + "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))\n"
                  "                       | media_rebase_p_w | rv_dup_p_w;",
            "restart: the outgoing mr toggles exactly once", False),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("milan_dp", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--head", type=int, nargs="*", default=[])
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--positive", nargs="*", default=[], help="legs to re-run clean")
    a = ap.parse_args()
    m = load(a.milan_dp.resolve())
    a.work.mkdir(parents=True, exist_ok=True)
    work = a.work.resolve()
    ok = True
    for key in a.positive:
        leg = m.LEGS[key]
        exe = leg.clean_mdir / leg.exe_name
        if not m.is_fresh(leg, exe):
            print(f"[INFO] {key}: clean binary missing or stale, rebuilt")
            exe = m.build(leg, {}, work / f"obj_pos_{key}")
        ans = m.verdict(*m.run_leg(leg, exe), None) if exe else "did not compile"
        print(f"[{'PASS' if ans == 'pass' else 'FAIL'}] positive {key}: {ans}")
        ok &= ans == "pass"
    ex = extras(m)
    todo = [(f"h{i}", m.CONTROLS[i]) for i in a.head] + [(f"x_{n}", ex[n]) for n in a.extra]
    for tag, c in todo:
        print(f"---- {tag}: {c.name} (leg {c.leg}, must break {c.breaks!r})", flush=True)
        caught = m.run_control(c, work, tag)
        ok &= caught
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
