#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require named failures for isolated policy-slew defects at silicon scale.

Sources and builds are temporary. Compilation failures never count as kills.
The default suite owns this campaign; its outer deadline bounds every run.
"""

import os
import signal
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
MUTANTS = (
    ("discard_removed", "&& !slew_window_w", "&& 1'b1",
     "[S1] overlapped window is discarded"),
    ("level_tied_low", "else phc_slew_q_r <= phc_slew_active_i;",
     "else phc_slew_q_r <= 1'b0;", "[S1] overlapped window is discarded"),
    ("partial_tail_trusted", "wire slew_window_w = win_slew_r || phc_slew_q_r;",
     "wire slew_window_w = phc_slew_q_r;", "[S1] overlapped window is discarded"),
    ("discard_not_counted", " + 7'(slew_hit_w)", "",
     "[S1] discards counted"),
)


def run_case(work: Path, name: str, source: str, failure: str | None) -> bool:
    """Build current sources and accept only the expected harness verdict."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    build = ["make", "--no-print-directory", "-s", "-C", str(HERE), "phc_step_build",
             f"SERVO_RTL={rtl}", f"PHC_MDIR={mdir}",
             f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}"]
    result = subprocess.run(build, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:])
        print(f"FAIL {name}: compilation failed")
        return False
    result = subprocess.run([str(mdir / "Vphc_step"), "+slew_control"],
                            capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if failure is None:
        passed = result.returncode == 0 and "RESULT: PASS" in output
    else:
        passed = (result.returncode == 1 and "RESULT: FAIL" in output and
                  f"[FAIL] {failure}" in output)
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: rc={result.returncode}", flush=True)
    if passed and failure:
        print(f"  named rejection: {failure}", flush=True)
    elif not passed:
        print(output, flush=True)
    return passed


def main() -> int:
    """Every control must fail its own check after a passing clean build."""
    def interrupted(_signum: int, _frame: object) -> None:
        """Unwind temporary storage when the suite deadline stops us."""
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    source = RTL.read_text()
    with tempfile.TemporaryDirectory(prefix="servo-slew-mutants-") as directory:
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
    failures = sum(not passed for passed in results)
    print(f"== mmcm_servo slew mutants: checks: {len(results)}   failures: {failures} ==")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
