#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant one defect per term of the #632/#764 phase loop and require its check.

Each mutant is a text substitution on a temporary copy of the RTL (or, for
the synthetic two-interface shape, of pin_wrap.sv, the integration that bench
plays), built through this directory's Makefile and run on the one case that
grades its term; it passes only when that case exits 1 with the named [FAIL]
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
#: the synthetic two-interface shape's integration (the bench plays it)
PINWRAP = "pin_wrap.sv"
SOURCES = {SERVO: HDL / SERVO, DOMEV: HDL / DOMEV, CRFTX: HDL / CRFTX, PINWRAP: HERE / PINWRAP}
#: Makefile variable that names each mutable source
MAKEVAR = {SERVO: "SERVO_RTL", DOMEV: "DOMEV_RTL", CRFTX: "CRFTX_RTL", PINWRAP: "PIN_WRAP"}
#: the two harnesses: (build target, objdir variable, executable)
PINS = "pins"
HARNESS = {"cases": ("build", "MDIR", "Vmedia_phase"), PINS: ("pins-build", "PIN_MDIR", "Vpin_wrap")}

#: (name, file, ((anchor, replacement), ...), case, failing check)
MUTANTS = (
    ("phase_term_removed", SERVO,
     (("    + (48'(pp_ph_r) <<< PH_GAIN_LSH_P);", "    + 48'(0);"),),
     "engage", "[engage] phase inside +/-5 % of Ps within 45 s of the event"),
    ("phase_sign_flipped", SERVO,
     (("    + (48'(pp_ph_r) <<< PH_GAIN_LSH_P);",
       "    - (48'(pp_ph_r) <<< PH_GAIN_LSH_P);"),),
     "engage", "[engage] phase held inside +/-5 % of Ps to the end"),
    ("rate_damping_removed", SERVO,
     (("    + (48'(ew_r) <<< (IF_C - KI_SHIFT_P))", "    + 48'(0)"),
      ("            pp_un_r  <= 32'(clamp_u(pp_isum_r)) + (ew_r >>> KP_SHIFT_P);",
       "            pp_un_r  <= 32'(clamp_u(pp_isum_r));")),
     "engage", "[engage] phase inside +/-5 % of Ps within 45 s of the event"),
    ("integrator_floored", SERVO,
     (("    + (48'(ew_r) <<< (IF_C - KI_SHIFT_P))",
       "    + ((48'(ew_r) >>> KI_SHIFT_P) <<< IF_C)"),),
     "carry", "[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)"),
    ("slew_clamp_removed", SERVO,
     (("  localparam int signed   PH_CLAMP_C = (PH_SLEW_NS_P * 128) >> PH_GAIN_LSH_P;",
       "  localparam int signed   PH_CLAMP_C = PH_RUN_C - 1;"),),
     "engage", "[engage] the pull is slew-limited"),
    ("fold_not_centred", SERVO,
     (("      (dv_rem_r >= PH_RW_C'(PH_HALF_C)) ? PH_TW_C'($signed({1'b0, dv_rem_r}) - PS_U_C)",
       "      1'b0 ? PH_TW_C'($signed({1'b0, dv_rem_r}) - PS_U_C)"),),
     "engage2", "[engage2] the pull went the short way"),
    ("refold_removed", SERVO,
     (("    if (!rst_n || state_r == IDLE_S) begin\n      dom_ns_r    <= '0;",
       "    if (!rst_n) begin\n      dom_ns_r    <= '0;"),
      ("        ph_trk_r     <= 1'b0;\n", ""),
      ("      end else if (ph_unw_ok_w) begin", "      end else if (1'b1) begin"),
      ("  wire ph_acc_w = dv_done_w && !dv_mean_r && ph_unw_ok_w;",
       "  wire ph_acc_w = dv_done_w && !dv_mean_r;")),
     "internal", "[internal] phase held inside +/-5 % of Ps to the end"),
    ("domain_event_not_backdated", DOMEV,
     (("ev_ns_o <= ptp_now_i - 64'(MARK_LAT_NS_P);", "ev_ns_o <= ptp_now_i;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    ("crf_output_off_grid", CRFTX,
     (("        ts_r         <= evt_ns_r + 64'(mtt_ofs_r);",
       "        ts_r         <= evt_ns_r + 64'(mtt_ofs_r) + 64'd9583;"),),
     "engage", "[engage] every DUT CRF timestamp is a frame instant of its own grid"),
    ("pins_b_constant_dropped", PINWRAP,
     (("    .MARK_LAT_NS_P (B_LAT_C),", "    .MARK_LAT_NS_P (0),"),),
     PINS, "[pins B] every stamped frame instant is each slot's MSB pin instant less its offset, "
           "inside +/-5 % of Ps"),
    ("pins_constants_swapped", PINWRAP,
     (("    .MARK_LAT_NS_P (A_LAT_C),", "    .MARK_LAT_NS_P (SWAP_C),"),
      ("    .MARK_LAT_NS_P (B_LAT_C),", "    .MARK_LAT_NS_P (A_LAT_C),"),
      ("    .MARK_LAT_NS_P (SWAP_C),", "    .MARK_LAT_NS_P (B_LAT_C),")),
     PINS, "[pins A] ...and inside the derivation"),
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
    argv = [str(binary)] if case == PINS else [str(binary), f"+case={case}"]
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout + result.stderr


def one_mutant(work: Path, originals: dict[str, str], mutant) -> bool:
    """Build and run one mutant; True only for its named rejection."""
    name, fname, subs, case, failure = mutant
    text = originals[fname]
    for anchor, replacement in subs:
        if text.count(anchor) != 1:
            print(f"[FAIL] {name}: anchor not found exactly once: {anchor!r}", flush=True)
            return False
        text = text.replace(anchor, replacement)
    binary = build(work, name, {fname: text}, PINS if case == PINS else "cases")
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
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    originals = {f: path.read_text() for f, path in SOURCES.items()}
    results = []
    with tempfile.TemporaryDirectory(prefix="media-phase-mutants-") as directory:
        work = Path(directory)
        clean = build(work, "clean", {})
        clean_pins = build(work, "clean", {}, PINS)
        if clean is None or clean_pins is None:
            print("[FAIL] clean: compilation failed", flush=True)
            return 1
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            verdicts = list(pool.map(lambda c: (c, run(clean_pins if c == PINS else clean, c)),
                                     cases))
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
