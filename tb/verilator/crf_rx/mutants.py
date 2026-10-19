#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compile isolated CRF receiver and servo-validity mutants; require named harness failures.

The discontinuity mutants run sim_discontinuity.cpp; the #762 STREAM_INTERRUPTED
mutants (a silence, a sequence gap and an unbind, each the cause its check
names) and the #765 subtype mutants (an AAF PDU on this stream_id ignored or
accepted, and a matching CRF PDU rejected) run the counter harness,
sim_main.cpp, through `make unit-build`.

No checkout is edited. Every executable, including the positive control,
is rebuilt from this invocation's source. The harness has bounded loops.
"""

import os
import signal
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/crf/KL_crf_rx.sv"
SERVO = HERE / "../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
MUTANTS = (
    ("validation_error_unlocks", "if (!w_fmt_ok) begin",
     "if (!w_fmt_ok) begin\n          locked_o <= 1'b0;",
     "validation error preserves established lock"),
    ("validation_error_refreshes_timeout", "      if (w_acc_run_w) begin",
     "      if (w_acc_run_w || w_ev_uf_w) begin",
     "reject stream cannot refresh the 100 ms timeout"),
    ("tu_ignored", "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = 1'b0;", "tu edge invalidates before the sampling edge"),
    ("jump_removed", "tu_change_w || ts_jump_w ||", "tu_change_w || 1'b0 ||",
     "unmarked timestamp jump invalidates the rate"),
    ("refill_short", "hfill_r <= 9'd1;", "hfill_r <= 9'd2;",
     "all 255 crossing intervals are withheld"),
    ("accept_edge_late", "!w_bind_rise_w && !rate_break_w;", "!w_bind_rise_w;",
     "tu edge invalidates before the sampling edge"),
)
#: #762 and #765, graded by the counter harness: (name, anchor, replacement, check)
UNIT_MUTANTS = (
    ("silence_not_interrupted", "if (en_i && !stop_i) cnt_intr_o <= cnt_intr_o + 32'd1;",
     "if (1'b0) cnt_intr_o <= cnt_intr_o + 32'd1;",
     "[762-a] silence: STREAM_INTERRUPTED counts the silence once"),
    ("gap_not_interrupted",
     "wire w_ev_si_w = w_ev_sm_w && (w_lost_w >= 8'(INTR_MIN_LOST_C));",
     "wire w_ev_si_w = 1'b0;",
     "[5t-e2] 3 gaps in ONE interval: +3 immediately (per-event)"),
    ("unbind_interrupts",
     "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n        dirty_p_o      <= 1'b1;\n      end\n\n"
     "      //! not-bound -> bound",
     "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n        dirty_p_o      <= 1'b1;\n"
     "        cnt_intr_o     <= cnt_intr_o + 32'd1;\n      end\n\n      //! not-bound -> bound",
     "[UNB-a6] STREAM_INTERRUPTED does not count the unbind"),
    ("unbind_edge_timeout_interrupts",
     "if (en_i && !stop_i) cnt_intr_o <= cnt_intr_o + 32'd1;",
     "if (!stop_i) cnt_intr_o <= cnt_intr_o + 32'd1;",
     "[UNB-d5] ...and no STREAM_INTERRUPTED: the unbind wins the edge (#762)"),
    #: #765: the subtype is part of the CRF input's format
    ("aaf_ignored",
     "  wire w_hit = frame_p_i && en_i && (sid_frame_i == sid_i);",
     "  wire w_hit = frame_p_i && en_i && (subtype_i == CRF_SUBTYPE_C)\n"
     "             && (sid_frame_i == sid_i);",
     "[FMT-b3] ...and counts UNSUPPORTED_FORMAT once"),
    ("aaf_accepted",
     "  wire w_fmt_ok = (subtype_i == CRF_SUBTYPE_C)\n               && (type_i == CRF_TYPE_AS_C)",
     "  wire w_fmt_ok = (type_i == CRF_TYPE_AS_C)",
     "[FMT-b1] an AAF PDU on the CRF stream_id is not accepted"),
    ("crf_rejected",
     "  wire w_fmt_ok = (subtype_i == CRF_SUBTYPE_C)",
     "  wire w_fmt_ok = (subtype_i != CRF_SUBTYPE_C)",
     "[FMT-a1] a matching CRF PDU is accepted"),
)


def run_case(work: Path, name: str, source: str, failure: str | None,
             *, servo: bool = False, unit: bool = False) -> bool:
    """A compiler error or abnormal termination never counts as a kill."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    if servo:
        build = ["make", "-s", "-C", str(HERE / "../mmcm_servo"), "unit-build",
                 f"SERVO_RTL={rtl}", f"UNIT_MDIR={mdir}"]
        executable = "Vservo_sim"
    elif unit:
        build = ["make", "-s", "-C", str(HERE), "unit-build",
                 f"RX_RTL={rtl}", f"UNIT_MDIR={mdir}"]
        executable = "Vcrf_rx_sim"
    else:
        build = ["make", "-s", "-C", str(HERE), "discontinuity-build",
                 f"RX_RTL={rtl}", f"DISC_MDIR={mdir}"]
        executable = "Vdiscontinuity"
    result = subprocess.run(
        [*build, f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}"],
        capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:])
        print(f"FAIL {name}: compilation failed")
        return False
    result = subprocess.run([str(mdir / executable)],
                            capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if failure is None:
        passed = result.returncode == 0 and ("RESULT: PASS" in output or
                                           ((servo or unit) and " 0 failures" in output))
    else:
        passed = (result.returncode == 1 and (servo or unit or "RESULT: FAIL" in output) and
                  f"[FAIL] {failure}" in output)
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: rc={result.returncode}")
    if passed and failure is not None:
        # The sweep judges this campaign's verdict, not expected DUT failures.
        print(f"  named rejection: {failure}")
    elif not passed:
        print(output)
    return passed


def main() -> int:
    """Run all controls and fail if any named defect escapes."""
    def interrupted(_signum: int, _frame: object) -> None:
        """Unwind temporary storage when the caller stops the campaign."""
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    source = RTL.read_text()
    with tempfile.TemporaryDirectory(prefix="crf-step-mutants-") as directory:
        work = Path(directory)
        if not run_case(work, "clean", source, None):
            return 1
        results = [True]
        for name, anchor, replacement, failure in MUTANTS:
            if source.count(anchor) != 1:
                print(f"FAIL {name}: expected exactly one mutation anchor")
                results.append(False)
                continue
            results.append(run_case(work, name, source.replace(anchor, replacement), failure))
        results.append(run_case(work, "unit_clean", source, None, unit=True))
        for name, anchor, replacement, failure in UNIT_MUTANTS:
            if source.count(anchor) != 1:
                print(f"FAIL {name}: expected exactly one mutation anchor")
                results.append(False)
                continue
            results.append(run_case(work, name, source.replace(anchor, replacement), failure,
                                    unit=True))
        servo_source = SERVO.read_text()
        anchor = "\n                           && ref_rate_valid_i;"
        if servo_source.count(anchor) != 1:
            print("FAIL servo_ignores_valid: expected exactly one mutation anchor")
            return 1
        results.append(run_case(work, "servo_clean", servo_source, None, servo=True))
        results.append(run_case(
            work, "servo_ignores_valid", servo_source.replace(anchor, ";"),
            "[U13] invalid remote sample holds trim", servo=True))
        resume_anchor = "  always_ff @(posedge clk_i) begin : servo_engine"
        if servo_source.count(resume_anchor) != 1:
            print("FAIL servo_never_resumes: expected exactly one mutation anchor")
            return 1
        # A sticky invalid sample stops PI forever, while preserving LOCKED.
        resume_latch = """  logic invalid_seen_r;
  always_ff @(posedge clk_i) begin : latch_invalid_sample
    if (!rst_n) invalid_seen_r <= 1'b0;
    else if (!ref_rate_valid_i) invalid_seen_r <= 1'b1;
  end
"""
        never_resumes = servo_source.replace(resume_anchor, resume_latch + resume_anchor)
        never_resumes = never_resumes.replace(anchor, anchor[:-1] + " && !invalid_seen_r;")
        results.append(run_case(
            work, "servo_never_resumes", never_resumes,
            "[U13] valid offset resumes PI trim", servo=True))
    failures = sum(not passed for passed in results)
    print(f"== crf_rx mutants: checks: {len(results)}   failures: {failures} ==")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
