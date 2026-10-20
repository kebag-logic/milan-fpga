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
SOURCES = {SERVO: HDL / SERVO, DOMEV: HDL / DOMEV, CRFTX: HDL / CRFTX, MTTR: HDL / MTTR,
           LATPKG: HDL / LATPKG, I2SCAP: HDL / "../aaf" / I2SCAP, PINWRAP: HERE / PINWRAP,
           OFSWRAP: HERE / OFSWRAP}
#: Makefile variable that names each mutable source
MAKEVAR = {SERVO: "SERVO_RTL", DOMEV: "DOMEV_RTL", CRFTX: "CRFTX_RTL", MTTR: "MTTR_RTL",
           LATPKG: "LATPKG_RTL", I2SCAP: "I2SCAP_RTL", PINWRAP: "PIN_WRAP", OFSWRAP: "OFS_WRAP"}
#: the five harnesses: (build target, objdir variable, executable)
PINS = "pins"
BLEND = "blend"
OFS = "ofs"
DET = "det"
HARNESS = {"cases": ("build", "MDIR", "Vmedia_phase"), PINS: ("pins-build", "PIN_MDIR", "Vpin_wrap"),
           BLEND: ("blend-build", "BLEND_MDIR", "Vblend_wrap"),
           OFS: ("ofs-build", "OFS_MDIR", "Vofs_wrap"), DET: ("det-build", "DET_MDIR", "Vdet")}
#: the harnesses that are one case each
SINGLE = (PINS, BLEND, OFS)


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
    #: R678-1-F3: each sample summed as folded, no tracking reference, so
    #: samples either side of +/-Ps/2 cancel towards zero
    ("tracking_fold_removed", SERVO,
     (("  wire signed [PH_UW_C-1:0] ph_unw_w = ph_ref_v_r ? PH_UW_C'(ph_ref_r) + PH_UW_C'(ph_dxf_w)",
       "  wire signed [PH_UW_C-1:0] ph_unw_w = 1'b0 ? PH_UW_C'(ph_ref_r) + PH_UW_C'(ph_dxf_w)"),),
     "det:balanced", "[det balanced] the window phase reads the half-period phase"),
    #: the window phase left unwrapped: past +Ps/2 it pulls the long way
    ("window_refold_removed", SERVO,
     (("      (ph_wraw_w >= PH_UW_C'(PH_HALF_C))  ? PH_TW_C'(ph_wraw_w - PH_UW_C'(PS_U_C))",
       "      1'b0  ? PH_TW_C'(ph_wraw_w - PH_UW_C'(PS_U_C))"),
      ("    : (ph_wraw_w < -PH_UW_C'(PH_HALF_C))  ? PH_TW_C'(ph_wraw_w + PH_UW_C'(PS_U_C))",
       "    : 1'b0  ? PH_TW_C'(ph_wraw_w + PH_UW_C'(PS_U_C))")),
     "det:cross", "[det cross] past +Ps/2 the window phase re-folds to the short way"),
    #: R678-1-F3: settled from the window mean alone
    ("settled_on_mean_only", SERVO,
     (("  wire ph_inband_w    = (ph_wmean_w < PH_TW_C'(PH_BAND_C)) && (ph_wmean_w > -PH_TW_C'(PH_BAND_C))\n"
       "                        && ph_allin_r;",
       "  wire ph_inband_w    = (ph_wmean_w < PH_TW_C'(PH_BAND_C)) && (ph_wmean_w > -PH_TW_C'(PH_BAND_C));"),),
     "det:meanin", "[det meanin] settled never asserts with every sample outside the band"),
    #: R678-1-F4: the snapshot reads only the valid flag the hold clears after it
    ("snapshot_hold_ignored", SERVO,
     (("            pp_ph_r     <= (!ph_theta_v_r || ph_hold_w) ? '0",
       "            pp_ph_r     <= !ph_theta_v_r ? '0"),),
     "det:snap", "[det snap] mr on the closing edge"),
    #: R677-1-F3: settled is the engaged bit, no band and no four windows
    ("settled_is_engaged", SERVO,
     (("  assign ph_settled_o = ph_theta_v_r &&\n"
       "                        (ph_set_cnt_r == ($bits(ph_set_cnt_r))'(PH_SETTLE_WIN_P));",
       "  assign ph_settled_o = ph_theta_v_r;"),),
     "det:inband", "[det inband] settled first reads 1 at the close of the fourth full in-band window"),
    #: R677-1-F3: a timestamp outside the fold range sampled anyway
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
    #: R677-1-F2: the local PHC step (#539) left out of the hold
    ("step_hold_removed", SERVO,
     (("                   !ref_rate_valid_i || ptp_jump_r || phc_slew_q_r;",
       "                   !ref_rate_valid_i || phc_slew_q_r;"),),
     "phcstep", "[phcstep] the phase term let go at the PHC step"),
    #: R678-1-F2: the offsets stamped as set, not in whole periods
    ("offset_rounding_bypassed", MTTR,
     (("      ofs_ns_o[32*row_r +: 32] <= dv_quot_r[31:0];",
       "      ofs_ns_o[32*row_r +: 32] <= raw_row_w;"),),
     OFS, "[ofs A] every AAF output stamps whole periods from the CRF timing points"),
    #: the CRF output stamping its row as set while the readback shows it applied
    ("crf_row_raw", OFSWRAP,
     (("    .transit_ns_i (applied_ns_o[N_AAF_P*32 +: 32]),",
       "    .transit_ns_i (raw_ns_i[N_AAF_P*32 +: 32]),"),),
     OFS, "[ofs A] every CRF timing point is a frame instant plus the CRF row as read back"),
    ("domain_event_not_backdated", DOMEV,
     (("  assign mark_ns_o = ptp_ns_i - 64'(MARK_LAT_NS_P);", "  assign mark_ns_o = ptp_ns_i;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    ("crf_output_off_grid", CRFTX,
     (("        ts_r         <= ev_ns_i + 64'(mtt_ofs_r);",
       "        ts_r         <= ev_ns_i + 64'(mtt_ofs_r) + 64'd9583;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    #: R677-1-F1: the blend's frame closed on its last TDM pair again, its
    #: marker latency the TDM bus's: the I2S pair banked is a frame older
    ("blend_closed_on_tdm_pair", LATPKG,
     (("    return (blend != 0) ? 0 : close_pair(frame_pairs);",
       "    return close_pair(frame_pairs);"),
      ("    return (tdm_slots == 0) || (blend != 0);",
       "    return (tdm_slots == 0);")),
     BLEND, "[blend 0] the I2S pair of every banked frame started at its pins inside +/-5 % of Ps"),
    #: R677-1-F1: the I2S front end copying rdata on the pop edge again, so
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
