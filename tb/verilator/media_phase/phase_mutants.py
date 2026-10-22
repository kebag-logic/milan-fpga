#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant one defect per term of the #632/#764 phase loop and require its check.

Each mutant is a text substitution on a temporary copy of the RTL (or, for
the synthetic three-interface shape, of pin_wrap.sv, the integration that bench
plays), built through this directory's Makefile and run on the one case that
grades its term (a loop case, the pins, or a detector case of sim_det.cpp,
named det:<case>); it passes only when that case exits 1 with the named [FAIL]
line. A
mutant whose anchor is not found exactly once, or that fails to compile,
counts as a failure of the campaign, never as a kill. The clean build of the
same cases is the positive control and must pass first.
"""

import argparse
import os
import signal
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
HDL = HERE / "../../../hdl/ieee1722/crf"
SERVO = "KL_mmcm_drp_servo.sv"
DOMEV = "KL_media_domain_event.sv"
CRFTX = "KL_crf_tx.sv"
MTTR = "KL_mtt_round.sv"
LATPKG = "KL_media_if_latency_pkg.sv"
I2SCAP = "KL_aaf_capture_i2s.sv"
#: the synthetic three-interface shape's integration (the bench plays it)
PINWRAP = "pin_wrap.sv"
#: the offsets harness's integration, milan_datapath's binding
OFSWRAP = "ofs_wrap.sv"
#: the listener's presentation stage and the two-render-interface shape
RQUEUE = "KL_render_queue.sv"
RENDWRAP = "render_wrap.sv"
SOURCES = {SERVO: HDL / SERVO, DOMEV: HDL / DOMEV, CRFTX: HDL / CRFTX, MTTR: HDL / MTTR,
           LATPKG: HDL / LATPKG, I2SCAP: HDL / "../aaf" / I2SCAP, PINWRAP: HERE / PINWRAP,
           OFSWRAP: HERE / OFSWRAP, RQUEUE: HDL / "../aaf" / RQUEUE, RENDWRAP: HERE / RENDWRAP}
#: Makefile variable that names each mutable source
MAKEVAR = {SERVO: "SERVO_RTL", DOMEV: "DOMEV_RTL", CRFTX: "CRFTX_RTL", MTTR: "MTTR_RTL",
           LATPKG: "LATPKG_RTL", I2SCAP: "I2SCAP_RTL", PINWRAP: "PIN_WRAP", OFSWRAP: "OFS_WRAP",
           RQUEUE: "RQUEUE_RTL", RENDWRAP: "REND_WRAP"}
#: the six harnesses: (build target, objdir variable, executable)
PINS = "pins"
RENDER = "render"
BLEND = "blend"
OFS = "ofs"
DET = "det"
HARNESS = {"cases": ("build", "MDIR", "Vmedia_phase"), PINS: ("pins-build", "PIN_MDIR", "Vpin_wrap"),
           RENDER: ("render-build", "REND_MDIR", "Vrender_wrap"),
           BLEND: ("blend-build", "BLEND_MDIR", "Vblend_wrap"),
           OFS: ("ofs-build", "OFS_MDIR", "Vofs_wrap"), DET: ("det-build", "DET_MDIR", "Vdet")}
#: the harnesses that are one case each
SINGLE = (PINS, RENDER, BLEND, OFS)


def harness_of(case: str) -> str:
    """The harness a case runs on: the pins, the offsets, the detector (det:<case>) or the loop."""
    if case in SINGLE:
        return case
    return DET if case.startswith(DET + ":") else "cases"

#: (name, file, ((anchor, replacement), ...), case, failing check)
MUTANTS = (
    ("phase_term_removed", SERVO,
     (("    + (40'(pp_ph_r) <<< PH_GAIN_LSH_P);", "    + 40'(0);"),),
     "engage", "[engage] phase inside +/-5 % of Ps within 45 s of the event"),
    ("phase_sign_flipped", SERVO,
     (("    + (40'(pp_ph_r) <<< PH_GAIN_LSH_P);",
       "    - (40'(pp_ph_r) <<< PH_GAIN_LSH_P);"),),
     "engage", "[engage] phase held inside +/-5 % of Ps to the end"),
    ("rate_damping_removed", SERVO,
     (("    + (40'(ew_r) <<< (IF_C - KI_SHIFT_P))", "    + 40'(0)"),
      ("            pp_un_r  <= 32'(clamp_u(pp_isum_r)) + (ew_r >>> KP_SHIFT_P);",
       "            pp_un_r  <= 32'(clamp_u(pp_isum_r));")),
     "engage", "[engage] phase inside +/-5 % of Ps within 45 s of the event"),
    ("integrator_floored", SERVO,
     (("    + (40'(ew_r) <<< (IF_C - KI_SHIFT_P))",
       "    + ((40'(ew_r) >>> KI_SHIFT_P) <<< IF_C)"),),
     "carry", "[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)"),
    ("slew_clamp_removed", SERVO,
     (("  localparam int signed   PH_CLAMP_C = (PH_SLEW_NS_P * 128) >> PH_GAIN_LSH_P;",
       "  localparam int signed   PH_CLAMP_C = PH_HALF_C - 1;"),),
     "engage", "[engage] the pull is slew-limited"),
    #: the fold left in [0, Ps): the phase gains the one bit that range needs,
    #: or the upper half would wrap back to nearly the centred reading. The
    #: window's re-fold still pulls the short way, but a sample just below
    #: zero now reads near Ps, outside the band, so nothing settles
    ("fold_not_centred", SERVO,
     (("      (dv_rem_r >= PH_RW_C'(PH_HALF_C)) ? PH_TW_C'($signed({1'b0, dv_rem_r}) - PS_U_C)",
       "      1'b0 ? PH_TW_C'($signed({1'b0, dv_rem_r}) - PS_U_C)"),
      ("  localparam int unsigned PH_TW_C = 16; ", "  localparam int unsigned PH_TW_C = 17; ")),
     "det:inband", "[det inband] settled first reads 1 at the close of the fourth full in-band window"),
    #: #632: each sample summed as folded, no tracking reference, so
    #: samples either side of +/-Ps/2 cancel towards zero
    ("tracking_fold_removed", SERVO,
     (("  wire                      ph_wrap_w   = ph_ref_v_r && (",
       "  wire                      ph_wrap_w   = 1'b0 && ("),),
     "det:balanced", "[det balanced] the window phase reads the half-period phase"),
    #: #632: the hold keeps the tracking reference of the era before it, so
    #: samples either side of +/-Ps/2 after an event cancel towards zero
    ("hold_keeps_ref", SERVO,
     (("        ph_set_cnt_r <= '0;\n        ph_ref_v_r   <= 1'b0;",
       "        ph_set_cnt_r <= '0;"),),
     "det:afterhold", "[det afterhold] after a hold, samples either side of +/-Ps/2 read the half-period phase"),
    #: the window phase left unwrapped: past +Ps/2 it pulls the long way
    ("window_refold_removed", SERVO,
     (("      (ph_wraw_w >= PH_UW_C'(PH_HALF_C))  ? PH_TW_C'(ph_wraw_w - PH_UW_C'(PS_U_C))",
       "      1'b0  ? PH_TW_C'(ph_wraw_w - PH_UW_C'(PS_U_C))"),
      ("    : (ph_wraw_w < -PH_UW_C'(PH_HALF_C))  ? PH_TW_C'(ph_wraw_w + PH_UW_C'(PS_U_C))",
       "    : 1'b0  ? PH_TW_C'(ph_wraw_w + PH_UW_C'(PS_U_C))")),
     "det:cross", "[det cross] past +Ps/2 the window phase re-folds to the short way"),
    #: #632: settled from the window mean alone
    ("settled_on_mean_only", SERVO,
     (("  wire ph_inband_w    = (ph_wmean_w < PH_TW_C'(PH_BAND_C)) && (ph_wmean_w > -PH_TW_C'(PH_BAND_C))\n"
       "                        && ph_allin_r;",
       "  wire ph_inband_w    = (ph_wmean_w < PH_TW_C'(PH_BAND_C)) && (ph_wmean_w > -PH_TW_C'(PH_BAND_C));"),),
     "det:meanin", "[det meanin] settled never asserts with every sample outside the band"),
    #: #632: the snapshot reads only the valid flag the hold clears after it
    ("snapshot_hold_ignored", SERVO,
     (("            pp_ph_r     <= (!ph_theta_v_r || ph_hold_w) ? '0",
       "            pp_ph_r     <= !ph_theta_v_r ? '0"),),
     "det:snap", "[det snap] mr on the closing edge"),
    #: #632: settled is the engaged bit, no band and no four windows
    ("settled_is_engaged", SERVO,
     (("  assign ph_settled_o = ph_theta_v_r &&\n"
       "                        (ph_set_cnt_r == ($bits(ph_set_cnt_r))'(PH_SETTLE_WIN_P));",
       "  assign ph_settled_o = ph_theta_v_r;"),),
     "det:inband", "[det inband] settled first reads 1 at the close of the fourth full in-band window"),
    #: #632: a timestamp outside the fold range sampled anyway
    ("fold_range_guard_removed", SERVO,
     (("        if (dom_fresh_r && ph_d_ok_w && !dv_busy_r) begin",
       "        if (dom_fresh_r && !dv_busy_r) begin"),),
     "det:range", "[det range] a timestamp 2^25 ns from the domain event is not sampled"),
    ("window_cap_removed", SERVO,
     (("        if (ph_cnt_r != PH_CW_C'(PH_CAP_C)) begin",
       "        if (1'b1) begin"),),
     "burst", "[burst] the window the burst filled kept exactly 264 samples, the cap"),
    ("history_hold_removed", SERVO,
     (("                   !ref_rate_valid_i || ptp_jump_r || phc_slew_q_r;",
       "                   ptp_jump_r || phc_slew_q_r;"),),
     "step", "[step] the phase term let go at the reference's history restart"),
    ("mr_hold_removed", SERVO,
     (("  wire ph_hold_w = (state_r != LOCKED_S) || !ph_en_i || ref_restart_p_i ||",
       "  wire ph_hold_w = (state_r != LOCKED_S) || !ph_en_i ||"),),
     "mr", "[mr] the phase term let go at the mr toggle"),
    ("holdover_hold_removed", SERVO,
     (("  wire ph_hold_w = (state_r != LOCKED_S) || !ph_en_i || ref_restart_p_i ||\n"
       "                   !ref_rate_valid_i || ptp_jump_r || phc_slew_q_r;",
       "  wire ph_hold_w = !ph_en_i || ref_restart_p_i ||\n"
       "                   ptp_jump_r || phc_slew_q_r;"),),
     "holdover", "[holdover] the phase term let go at HOLDOVER"),
    ("idle_hold_removed", SERVO,
     (("  wire ph_hold_w = (state_r != LOCKED_S) || !ph_en_i || ref_restart_p_i ||",
       "  wire ph_hold_w = !ph_en_i || ref_restart_p_i ||"),
      ("    if (!rst_n || state_r == IDLE_S) begin\n      dom_ns_r    <= '0;",
       "    if (!rst_n) begin\n      dom_ns_r    <= '0;")),
     "internal", "[internal] the phase term let go at INTERNAL"),
    ("slew_hold_removed", SERVO,
     (("                   !ref_rate_valid_i || ptp_jump_r || phc_slew_q_r;",
       "                   !ref_rate_valid_i || ptp_jump_r;"),),
     "slew", "[slew] the phase term let go at the slew level"),
    #: #632: the local PHC step (#539) left out of the hold
    ("step_hold_removed", SERVO,
     (("                   !ref_rate_valid_i || ptp_jump_r || phc_slew_q_r;",
       "                   !ref_rate_valid_i || phc_slew_q_r;"),),
     "phcstep", "[phcstep] the phase term let go at the PHC step"),
    #: #632: the CRF output stamping its offset as set, not rounded by Eq. 14
    ("crf_rounding_bypassed", MTTR,
     (("      ofs_ns_o[32*row_r +: 32] <= dv_quot_r[31:0];\n      ofs_c_o[row_r]        <= dv_quot_r[32];",
       "      ofs_ns_o[32*row_r +: 32] <= raw_row_w;\n      ofs_c_o[row_r]        <= 1'b0;"),),
     OFS, "[ofs B] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14"),
    #: #632: a conversion past 2^32 - 1 ns loses its bit 32
    ("mtt_carry_dropped", MTTR,
     (("      ofs_c_o[row_r]        <= dv_quot_r[32];",
       "      ofs_c_o[row_r]        <= 1'b0;"),),
     OFS, "[ofs H] the CRF row reads back as applied, rounded up to whole periods by Equation 14, all 33 bits"),
    #: #632: a factory row past 2^32 - 1 ns loads its low word alone
    ("mtt_reset_carry_dropped", MTTR,
     (("        ofs_c_o[k]           <= RESET_RND_C[33*k + 32];",
       "        ofs_c_o[k]           <= 1'b0;"),),
     OFS, "[ofs A] in reset the CRF row reads its factory value rounded up to whole periods, all 33 bits"),
    #: #632: GET_STREAM_INFO reads a row past 32 bits as its low word
    ("readback_saturation_dropped", MTTR,
     (("                 : ofs_c_o[rb_row_i] ? 32'hFFFF_FFFF : ofs_ns_o[32*rb_row_i +: 32];",
       "                 : ofs_ns_o[32*rb_row_i +: 32];"),),
     OFS, "[ofs H] GET_STREAM_INFO reads the CRF row as applied, 0xFFFFFFFF past 32 bits"),
    #: #632: the CRF output adds the rounded offset's low word alone, so it
    #: stamps 2^32 ns early past 2^32 - 1 ns
    ("crf_carry_dropped", CRFTX,
     (("    else        mtt_ofs_r <= DIVW_C'({transit_c_i, transit_ns_i});",
       "    else        mtt_ofs_r <= DIVW_C'(transit_ns_i);"),),
     OFS, "[ofs H] every CRF timestamp, all 64 bits, is a frame instant plus the CRF row rounded by Equation 14"),
    #: the CRF output stamping its row as set while the readback shows it applied
    ("crf_row_raw", OFSWRAP,
     (("    .transit_ns_i (crf_applied_ns_o),",
       "    .transit_ns_i (raw_ns_i[N_AAF_P*32 +: 32]),"),),
     OFS, "[ofs B] every CRF timing point is a frame instant plus the CRF row as read back"),
    #: #632 ruling: the AAF talkers stamping their rows rounded by Eq. 14
    #: (every row through the rounder) instead of as set
    ("aaf_rows_rounded", OFSWRAP,
     (("  KL_aaf_packetizer #(.N_TALKERS_P (N_AAF_P)) u_pkt (",
       "  wire [N_AAF_P*32-1:0] aaf_rnd_w;\n"
       "  KL_mtt_round #(.N_P (N_AAF_P), .BASE_HZ_P (48000)) u_aaf_round (\n"
       "    .clk_i (clk_i), .rst_n (rst_n), .raw_ns_i (raw_ns_i[N_AAF_P*32-1:0]),\n"
       "    .ofs_ns_o (aaf_rnd_w), .ofs_c_o (), .rb_row_i ('0), .rb_ns_o ());\n"
       "  KL_aaf_packetizer #(.N_TALKERS_P (N_AAF_P)) u_pkt ("),
      ("    .transit_ns_i (raw_ns_i[N_AAF_P*32-1:0]),", "    .transit_ns_i (aaf_rnd_w),")),
     OFS, "[ofs A] every AAF timestamp is a frame instant plus its row as set, to the ns"),
    #: #632 ruling: GET_STREAM_INFO reading an AAF row rounded by Eq. 14
    ("aaf_readback_rounded", OFSWRAP,
     (("  //! GET_STREAM_INFO word 3: an AAF row as set, the CRF row as applied",
       "  wire [31:0] aaf_rb_w;\n"
       "  KL_mtt_round #(.N_P (N_AAF_P), .BASE_HZ_P (48000)) u_aaf_round (\n"
       "    .clk_i (clk_i), .rst_n (rst_n), .raw_ns_i (raw_ns_i[N_AAF_P*32-1:0]),\n"
       "    .ofs_ns_o (), .ofs_c_o (), .rb_row_i (rb_row_i[1:0]), .rb_ns_o (aaf_rb_w));"),
      ("                 : (32'(rb_row_i) < N_AAF_P) ? raw_ns_i[32*rb_row_i +: 32] : 32'd0;",
       "                 : (32'(rb_row_i) < N_AAF_P) ? aaf_rb_w : 32'd0;")),
     OFS, "[ofs A] GET_STREAM_INFO reads every AAF row as set"),
    ("domain_event_not_backdated", DOMEV,
     (("  assign mark_ns_o = ptp_ns_i - 64'(MARK_LAT_NS_P);", "  assign mark_ns_o = ptp_ns_i;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    ("crf_output_off_grid", CRFTX,
     (("        ts_r         <= ev_ns_i + 64'(mtt_ofs_r);",
       "        ts_r         <= ev_ns_i + 64'(mtt_ofs_r) + 64'd9583;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    #: #632: the blend's frame closed on its last TDM pair again, its
    #: marker latency the TDM bus's: the I2S pair banked is a frame older
    ("blend_closed_on_tdm_pair", LATPKG,
     (("    return (blend != 0) ? 0 : close_pair(frame_pairs);",
       "    return close_pair(frame_pairs);"),
      ("    return (tdm_slots == 0) || (blend != 0);",
       "    return (tdm_slots == 0);")),
     BLEND, "[blend 0] the I2S pair of every banked frame started at its pins inside +/-5 % of Ps"),
    #: #632: the I2S front end copying rdata on the pop edge again, so
    #: every strobe carries the pair before it
    ("i2s_pair_one_pop_late", I2SCAP,
     (("  always_comb begin : t_pair_out\n"
       "    pair_l_o = cap_pair_w[47:24];\n"
       "    pair_r_o = cap_pair_w[23:0];\n"
       "  end : t_pair_out",
       "  always_ff @(posedge clk_i) begin : t_pair_out\n"
       "    if (cap_ren_r) pair_l_o <= cap_pair_w[47:24];\n"
       "    if (cap_ren_r) pair_r_o <= cap_pair_w[23:0];\n"
       "  end : t_pair_out"),),
     BLEND, "[blend 0] the I2S pair of every banked frame started at its pins inside +/-5 % of Ps"),
    ("pins_b_constant_dropped", PINWRAP,
     (("    .MARK_LAT_NS_P (B_LAT_C),", "    .MARK_LAT_NS_P (0),"),),
     PINS, "[pins B] every stamped frame instant is each slot's MSB pin instant less its offset, "
           "inside +/-5 % of Ps"),
    ("pins_constants_swapped", PINWRAP,
     (("    .MARK_LAT_NS_P (A_LAT_C),", "    .MARK_LAT_NS_P (SWAP_C),"),
      ("    .MARK_LAT_NS_P (B_LAT_C),", "    .MARK_LAT_NS_P (A_LAT_C),"),
      ("    .MARK_LAT_NS_P (SWAP_C),", "    .MARK_LAT_NS_P (B_LAT_C),")),
     PINS, "[pins A] ...and inside the derivation"),
    #: #632: B's out-lead without its hold frame: B's read is A's, a frame
    #: late at B's pins
    ("render_b_lead_dropped", RENDWRAP,
     (("  localparam int unsigned B_LEAD_C = 32'(out_lead_frames(A_LAT_C, B_PIPE_C, FS_C)) + B_HOLD_C;",
       "  localparam int unsigned B_LEAD_C = 32'(out_lead_frames(A_LAT_C, B_PIPE_C, FS_C));"),),
     RENDER, "[render B] every sample's slot-MSB pin instant, less its slot offset, is its presentation "
             "time inside +/-5 % of Ps"),
    #: #632: the queue places each PDU at the first frame every interface
    #: still reads, its timestamp unread: the old fill law's shape
    ("render_read_untimed", RQUEUE,
     (("          f0_r  <= f0_r + FW_C'(ld_r[QW_C-1:0]) + FW_C'(rnd_w);",
       "          f0_r  <= f0_r + FW_C'(KMAX_C + 1);"),),
     RENDER, "[render A] every sample's slot-MSB pin instant, less its slot offset, is its presentation "
             "time inside +/-5 % of Ps"),
    #: #632: every PDU's frame one past its timestamp's
    ("render_frame_off_by_one", RQUEUE,
     (("          f0_r  <= f0_r + FW_C'(ld_r[QW_C-1:0]) + FW_C'(rnd_w);",
       "          f0_r  <= f0_r + FW_C'(ld_r[QW_C-1:0]) + FW_C'(rnd_w) + 1'b1;"),),
     RENDER, "[render A] every sample's slot-MSB pin instant, less its slot offset, is its presentation "
             "time inside +/-5 % of Ps"),
    #: #632: a late event written as if in the window: it lands on the row a
    #: lap later and is presented there
    ("render_late_rule_removed", RQUEUE,
     (("  wire        late0_w  = dr0_w[FW_C-1] || (dr0_w == '0);\n"
       "  wire        late1_w  = dr1_w[FW_C-1] || (dr1_w == '0);\n"
       "  wire        early0_w = !late0_w && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !late1_w && (32'(dr1_w) >= ROWS_C);",
       "  wire        late0_w  = 1'b0;\n"
       "  wire        late1_w  = 1'b0;\n"
       "  wire        early0_w = !dr0_w[FW_C-1] && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !dr1_w[FW_C-1] && (32'(dr1_w) >= ROWS_C);"),),
     RENDER, "[render A] every sample's slot-MSB pin instant, less its slot offset, is its presentation "
             "time inside +/-5 % of Ps"),
    #: #632: an event past the window written: it lands on a row a lap
    #: earlier, over that frame's sample
    ("render_early_rule_removed", RQUEUE,
     (("  wire        early0_w = !late0_w && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !late1_w && (32'(dr1_w) >= ROWS_C);",
       "  wire        early0_w = 1'b0;\n"
       "  wire        early1_w = 1'b0;"),),
     RENDER, "[render A] every sample's slot-MSB pin instant, less its slot offset, is its presentation "
             "time inside +/-5 % of Ps"),
    ("pins_c_closed_at_frame_end", PINWRAP,
     (("  localparam int unsigned C_LAT_C = 32'(mark_lat_ns(pair_end_bits(C_CLOSE_C, 32, C_DD_C),",
       "  localparam int unsigned C_LAT_C = 32'(mark_lat_ns(pair_end_bits(C_SLOTS_C / 2 - 1, 32, C_DD_C),"),),
     PINS, "[pins C] every stamped frame instant is each slot's MSB pin instant less its offset, "
           "inside +/-5 % of Ps"),
)
CLEAN_CASES = sorted({m[3] for m in MUTANTS})
#: at most two Verilator builds at once, however many runs are in flight
BUILDS = threading.BoundedSemaphore(2)


def build(work: Path, name: str, sources: dict[str, str], harness: str = "cases") -> Path | None:
    """Build one harness from the given source texts; None if it fails."""
    target, mvar, exe = HARNESS[harness]
    overrides = []
    for fname, text in sources.items():
        path = work / name / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        overrides.append(f"{MAKEVAR[fname]}={path}")
    mdir = work / name / f"obj_{harness}"
    mdir.mkdir(parents=True, exist_ok=True)
    cmd = ["make", "--no-print-directory", "-s", "-C", str(HERE), target,
           f"{mvar}={mdir}", f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '2')}",
           *overrides]
    with BUILDS:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:], flush=True)
        return None
    return mdir / exe


def run(binary: Path, case: str) -> tuple[int, str]:
    """One case (or the pins harness); its exit status and its whole output."""
    arg = case.split(":", 1)[1] if harness_of(case) == DET else case
    argv = [str(binary)] if case in SINGLE else [str(binary), f"+case={arg}"]
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout + result.stderr


def one_mutant(work: Path, originals: dict[str, str], mutant: tuple) -> bool:
    """Build and run one mutant; True only for its named rejection."""
    name, fname, subs, case, failure = mutant
    text = originals[fname]
    for anchor, replacement in subs:
        if text.count(anchor) != 1:
            print(f"[FAIL] {name}: anchor not found exactly once: {anchor!r}", flush=True)
            return False
        text = text.replace(anchor, replacement)
    binary = build(work, name, {fname: text}, harness_of(case))
    if binary is None:
        print(f"[FAIL] {name}: compilation failed (never a kill)", flush=True)
        return False
    rc, out = run(binary, case)
    killed = rc == 1 and "RESULT: FAIL" in out and f"[FAIL] {failure}" in out
    line = next((ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")), "")
    print(f"[{'PASS' if killed else 'FAIL'}] {name} on {case}: rc={rc} -- {line}", flush=True)
    if not killed:
        print(out[-3000:], flush=True)
    return killed


def main() -> int:
    """The clean cases first, then every mutant; any miss fails the campaign."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=2, help="mutants built and run at once")
    parser.add_argument("--only", default="", help="comma-separated mutant names (default: all)")
    args = parser.parse_args()
    chosen = [m for m in MUTANTS if not args.only or m[0] in args.only.split(",")]
    if args.only and len(chosen) != len(args.only.split(",")):
        print("[FAIL] --only names a mutant this campaign does not have", flush=True)
        return 1
    cases = sorted({m[3] for m in chosen})

    def interrupted(_signum: int, _frame: object) -> None:
        """A TERM ends the campaign with the shell's 143, cleaning its temporary tree."""
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    originals = {f: path.read_text() for f, path in SOURCES.items()}
    results = []
    with tempfile.TemporaryDirectory(prefix="media-phase-mutants-") as directory:
        work = Path(directory)
        clean = {h: build(work, "clean", {}, h) for h in sorted({harness_of(c) for c in cases})}
        if any(b is None for b in clean.values()):
            print("[FAIL] clean: compilation failed", flush=True)
            return 1
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            verdicts = list(pool.map(lambda c: (c, run(clean[harness_of(c)], c)), cases))
        for case, (rc, out) in verdicts:
            ok = rc == 0 and "RESULT: PASS" in out
            print(f"[{'PASS' if ok else 'FAIL'}] clean {case}: rc={rc}", flush=True)
            results.append(ok)
        if not all(results):
            print("== media_phase mutants: the clean control failed; no mutant is graded ==")
            return 1
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results += list(pool.map(lambda m: one_mutant(work, originals, m), chosen))
    failures = sum(not ok for ok in results)
    print(f"== media_phase mutants: checks: {len(results)}   failures: {failures} ==")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
