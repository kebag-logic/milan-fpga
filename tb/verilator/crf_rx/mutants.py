#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compile isolated CRF receiver mutants; require named harness failures.

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
MUTANTS = (
    ("tu_ignored", "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = 1'b0;", "tu edge invalidates before the sampling edge"),
    ("jump_removed", "tu_change_w || ts_jump_w ||", "tu_change_w || 1'b0 ||",
     "unmarked timestamp jump invalidates the rate"),
    ("refill_short", "hfill_r <= 9'd1;", "hfill_r <= 9'd2;",
     "all 255 crossing intervals are withheld"),
    ("accept_edge_late", "!w_bind_rise_w && !rate_break_w;", "!w_bind_rise_w;",
     "tu edge invalidates before the sampling edge"),
)


def run_case(work: Path, name: str, source: str, failure: str | None) -> bool:
    """A compiler error or abnormal termination never counts as a kill."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    result = subprocess.run(
        ["make", "-s", "-C", str(HERE), "discontinuity-build",
         f"RX_RTL={rtl}", f"DISC_MDIR={mdir}",
         f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}"],
        capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:])
        print(f"FAIL {name}: compilation failed")
        return False
    result = subprocess.run([str(mdir / "Vdiscontinuity")],
                            capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if failure is None:
        passed = result.returncode == 0 and "RESULT: PASS" in output
    else:
        passed = (result.returncode == 1 and "RESULT: FAIL" in output and
                  f"[FAIL] {failure}" in output)
    print(f"{'PASS' if passed else 'FAIL'} {name}: rc={result.returncode}")
    for line in output.splitlines():
        if "[FAIL]" in line or "checks:" in line:
            print(line)
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
        passed = True
        for name, anchor, replacement, failure in MUTANTS:
            if source.count(anchor) != 1:
                print(f"FAIL {name}: expected exactly one mutation anchor")
                passed = False
                continue
            passed = run_case(work, name, source.replace(anchor, replacement), failure) and passed
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
