#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #386 render law in milan_dp: prove the checks can fail.

sim_aclk.cpp asserts, on the elaborated shipping shape, that every accepted
PDU's first event renders SETPOINT media ticks after its accept and that a
PHC step recentres the fill once. Issue #386's acceptance asks for the two
negative controls by name: a deliberately wrong prefill must fail the law
check, and a disabled recentre must fail the recentre check. So the real
KL_render_setpoint is mutated, one defect at a time, and the SAME leg is
rebuilt through the Makefile's own recipe (`make aclk-build` with RSP_SRC and
ACLK_MDIR overridden) and run with `--render-only`, the half of the leg those
checks live in. Each mutant must make the leg FAIL by its OWN verdict (a
`[FAIL]` line or a tally with failures, read by scripts/suite_tally.py), and
the named check must be among the failures; a crash or a hang is not a
catch. The positive control is the clean leg the sweep just ran (obj_aclk):
it is re-run here in the same short mode so the two verdicts come from the
same binary shape.

Usage: python3 render_mutants.py      (run from tb/verilator/milan_dp)
Exit 0 = every mutant was caught and the clean leg still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"
CLEAN_EXE = HERE / "obj_aclk/Vmilan_dp_aclk"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the short leg simulates ~13 M datapath cycles; a run still going after
#: this many seconds is livelocked, not slow (the guard, never the oracle)
MUTANT_RUN_TIMEOUT_S = 3600

#: (name, pattern, replacement, the check this defect must break)
MUTATIONS = [
    ("prefill target three events high",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P;",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P + 3;",
     "RENDER-INT: every PDU's first event inside the law band"),
    ("recentre pulse ignored",
     "if (recentre_p_i && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "if (1'b0 && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "RENDER-RC-INT: the recentre restored the law (fill at accept = setpoint)"),
]


def build(rtl_path: Path, mdir: Path) -> Path | None:
    """Build the leg against `rtl_path` through the suite's own recipe."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "aclk-build", f"RSP_SRC={rtl_path}",
         f"ACLK_MDIR={mdir}"],
        capture_output=True, text=True)
    exe = mdir / "Vmilan_dp_aclk"
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path) -> tuple[int | str, str]:
    """(rc, stdout) of one --render-only run; rc is "TIMEOUT" when killed."""
    proc = subprocess.Popen([str(exe), "--render-only"], cwd=str(HERE),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=MUTANT_RUN_TIMEOUT_S)
        return proc.returncode, out
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        out, _ = proc.communicate()
        return "TIMEOUT", out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def verdict(rc: int | str, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == "TIMEOUT":
        return f"TIMEOUT after {MUTANT_RUN_TIMEOUT_S}s - a hang is not a catch"
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]") and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    src = RTL.read_text()
    passes = fails = 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    with tempfile.TemporaryDirectory(prefix="render-mutants-") as td:
        work = Path(td)
        exe = CLEAN_EXE if CLEAN_EXE.is_file() else build(RTL, work / "obj_clean")
        answer = verdict(*run_leg(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated stage still passes the render-law leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated stage does NOT pass ({answer}) - every "
                  f"mutant result below is meaningless")
        for name, pattern, replacement, breaks in MUTATIONS:
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s), expected exactly 1. The "
                      f"RTL moved and this mutant is no longer mutating "
                      f"anything - fix the pattern, do not delete the arm.")
                continue
            tag = name.replace(" ", "_")
            mpath = work / f"KL_render_setpoint_{tag}.sv"
            mpath.write_text(src.replace(pattern, replacement))
            exe = build(mpath, work / f"obj_{tag}")
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the leg")
                continue
            answer = verdict(*run_leg(exe), breaks)
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The leg does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
