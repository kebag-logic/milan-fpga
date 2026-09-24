#!/usr/bin/env python3
"""Apply one named mutant to a copy of KL_mmcm_drp_servo.sv; refuse if the
anchor text is not found exactly once (so a mutant can never silently no-op)."""
import sys

MUTANTS = {
    # author-claimed arms, re-derived independently
    "M1_detector_off": ("else        ptp_jump_r <= (ptp_now_i[31:0] - ptp_q_r[31:0]) > STEP_DET_NS_C;",
                        "else        ptp_jump_r <= 1'b0;"),
    "M2_no_abandon": ("          win_valid_r <= 1'b0;\n          disc_run_r  <= '0;\n          if (pp_seq_r == '0) pp_run_r <= 1'b0;",
                      "          disc_run_r  <= '0;\n          if (pp_seq_r == '0) pp_run_r <= 1'b0;"),
    "M3_no_boundary_squash": ("          if (pp_seq_r == '0) pp_run_r <= 1'b0;\n", ""),
    "M4_uncond_squash": ("          if (pp_seq_r == '0) pp_run_r <= 1'b0;", "          pp_run_r <= 1'b0;"),
    "M5_guard_off": ("  wire guard_hit_w = (pp_seq_r == 3'd4) && pp_run_r &&",
                     "  wire guard_hit_w = 1'b0 && (pp_seq_r == 3'd4) && pp_run_r &&"),
    "M6_single_tally": ("n_v = 7'(disc_cnt_r) + 7'(guard_hit_w) + 7'(step_hit_w);",
                        "n_v = 7'(disc_cnt_r) + 7'(guard_hit_w | step_hit_w);"),
    "M7_guard_32ppm": ("localparam int signed   GUARD_THR_C = 32'sd1 << 19;",
                       "localparam int signed   GUARD_THR_C = 32'sd1 << 14;"),
    # reviewer-added mutants
    "M8_no_guard_resync": ("              if (disc_run_r == 2'(DISC_MAX_C - 1)) begin\n                win_valid_r <= 1'b0;",
                           "              if (disc_run_r == 2'(DISC_MAX_C - 1)) begin\n                win_valid_r <= win_valid_r;"),
    "M9_thr_25us": ("STEP_DET_NS_C = 32'd4096;", "STEP_DET_NS_C = 32'd25000;"),
    "M10_signed_detect": ("else        ptp_jump_r <= (ptp_now_i[31:0] - ptp_q_r[31:0]) > STEP_DET_NS_C;",
                          "else        ptp_jump_r <= $signed(ptp_now_i[31:0] - ptp_q_r[31:0]) > $signed(STEP_DET_NS_C);"),
    "M11_late_detect": ("  logic ptp_jump_r;\n  always_ff @(posedge clk_i) begin : ptp_jump_S\n    if (!rst_n) ptp_jump_r <= 1'b0;\n    else        ptp_jump_r <= (ptp_now_i[31:0] - ptp_q_r[31:0]) > STEP_DET_NS_C;",
                        "  logic ptp_jump_r;\n  logic [63:0] ptp_q2_m;\n  always_ff @(posedge clk_i) begin : ptp_q2_m_S\n    ptp_q2_m <= ptp_q_r;\n  end : ptp_q2_m_S\n  always_ff @(posedge clk_i) begin : ptp_jump_S\n    if (!rst_n) ptp_jump_r <= 1'b0;\n    else        ptp_jump_r <= (ptp_q_r[31:0] - ptp_q2_m[31:0]) > STEP_DET_NS_C;"),
    "M12_no_streak_reset": ("          win_valid_r <= 1'b0;\n          disc_run_r  <= '0;\n          if (pp_seq_r == '0)",
                            "          win_valid_r <= 1'b0;\n          if (pp_seq_r == '0)"),
    "M13_ungated_step_hit": ("wire step_hit_w  = ptp_jump_r && win_valid_r;", "wire step_hit_w  = ptp_jump_r;"),
    "M14_tally_wraps": ("disc_cnt_r <= (n_v > 7'h3F) ? 6'h3F : n_v[5:0];", "disc_cnt_r <= n_v[5:0];"),
    "M15_no_tally_step": ("n_v = 7'(disc_cnt_r) + 7'(guard_hit_w) + 7'(step_hit_w);",
                          "n_v = 7'(disc_cnt_r) + 7'(guard_hit_w);"),
}

def main() -> int:
    name, path = sys.argv[1], sys.argv[2]
    old, new = MUTANTS[name]
    src = open(path, encoding="utf-8").read()
    if src.count(old) != 1:
        print(f"REFUSED {name}: anchor found {src.count(old)} times", file=sys.stderr)
        return 2
    open(path, "w", encoding="utf-8").write(src.replace(old, new))
    print(f"APPLIED {name}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print("\n".join(MUTANTS)); sys.exit(0)
    sys.exit(main())
