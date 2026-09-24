#!/usr/bin/env python3
"""Apply one named, exact-string mutation to a disposable copy (probe.sh).

Each edit must match exactly once, or the probe refuses (exit 3), so a mutant
that silently fails to apply can never be read as "survived".
BASE_TREE (env) names the base-revision tree for the two cross-revision swaps.
"""
import os
import shutil
import sys

RTL = "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
DET = "ptp_jump_r <= (ptp_now_i[31:0] - ptp_q_r[31:0]) > STEP_DET_NS_C;"

MUTANTS = {
    # the author's seven, re-derived independently
    "det_off": [(RTL, DET, "ptp_jump_r <= 1'b0;")],
    "no_abandon": [(RTL, "if (step_hit_w) begin\n          win_valid_r <= 1'b0;\n",
                    "if (step_hit_w) begin\n")],
    "no_squash": [(RTL, "          if (pp_seq_r == '0) pp_run_r <= 1'b0;\n", "")],
    "uncond_squash": [(RTL, "if (pp_seq_r == '0) pp_run_r <= 1'b0;", "pp_run_r <= 1'b0;")],
    "guard_off": [(RTL, "wire guard_hit_w = (pp_seq_r == 3'd4) && pp_run_r &&",
                   "wire guard_hit_w = 1'b0 && (pp_seq_r == 3'd4) && pp_run_r &&")],
    "single_tally": [(RTL, "7'(guard_hit_w) + 7'(step_hit_w)", "7'(guard_hit_w | step_hit_w)")],
    "guard32": [(RTL, "GUARD_THR_C = 32'sd1 << 19", "GUARD_THR_C = 32'sd1 << 14")],
    # reviewer-owned additions
    "no_resync": [(RTL, "if (disc_run_r == 2'(DISC_MAX_C - 1)) begin", "if (1'b0) begin")],
    "late_verdict": [
        (RTL, DET, "ptp_jump_r <= (ptp_q_r[31:0] - ptp_q2_r[31:0]) > STEP_DET_NS_C;"),
        (RTL, "  logic ptp_jump_r;\n",
         "  logic [31:0] ptp_q2_r;\n  always_ff @(posedge clk_i) ptp_q2_r <= ptp_q_r[31:0];\n"
         "  logic ptp_jump_r;\n")],
    "early_verdict": [(RTL, "wire step_hit_w  = ptp_jump_r && win_valid_r;",
                       "wire step_hit_w  = ((ptp_now_i[31:0] - ptp_q_r[31:0]) > STEP_DET_NS_C)"
                       " && win_valid_r;")],
    "thr_25us": [(RTL, "STEP_DET_NS_C = 32'd4096", "STEP_DET_NS_C = 32'd25000")],
    "fwd_only": [(RTL, DET, "ptp_jump_r <= $signed(ptp_now_i[31:0] - ptp_q_r[31:0]) > "
                            "$signed(STEP_DET_NS_C);")],
    "step_ignores_valid": [(RTL, "wire step_hit_w  = ptp_jump_r && win_valid_r;",
                            "wire step_hit_w  = ptp_jump_r;")],
    "no_streak_reset": [(RTL, "          disc_run_r  <= '0;\n          if (pp_seq_r == '0)",
                         "          if (pp_seq_r == '0)")],
    "no_saturate": [(RTL, "disc_cnt_r <= (n_v > 7'h3F) ? 6'h3F : n_v[5:0];",
                     "disc_cnt_r <= n_v[5:0];")],
    "base_guard_no_resync": [(RTL, "if (disc_run_r == 2'(DISC_MAX_C - 1)) begin", "if (1'b0) begin")],
}

SWAPS = {
    # the base revision's unit harness (old U10, no U11) against this RTL
    "tb_base_unit": "tb/verilator/mmcm_servo/sim_main.cpp",
    # this revision's unit harness against the base RTL
    "rtl_base": RTL,
}


def main() -> int:
    wd, mut = sys.argv[1], sys.argv[2]
    if mut in SWAPS:
        rel = SWAPS[mut]
        shutil.copyfile(os.path.join(os.environ["BASE_TREE"], rel), os.path.join(wd, rel))
        print(f"mutate: {mut}: copied base {rel}")
        return 0
    for rel, old, new in MUTANTS[mut]:
        path = os.path.join(wd, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n = text.count(old)
        if n != 1:
            print(f"mutate: {mut}: pattern matched {n} times in {rel}", file=sys.stderr)
            return 3
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(old, new))
    print(f"mutate: {mut}: applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
