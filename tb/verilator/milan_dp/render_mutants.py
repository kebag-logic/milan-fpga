#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #386 render law in milan_dp: prove the checks can fail.

sim_aclk.cpp asserts, on the elaborated shipping shape, that every accepted
PDU's first event renders SETPOINT media ticks after its accept, that a PHC
step recentres the fill once (from a short queue and from a long one), and
that a clock-source change under the running stream recentres it once the
grid has settled. Issue #386's acceptance asks for the negative controls by
name: a deliberately wrong prefill must fail the law check, and a disabled
recentre must fail the recentre check; the round-5 review added the recentre
that counts but does not snap, and the clock-source trigger. So the real
KL_render_setpoint, or the real milan_datapath, is mutated, one defect at a
time, and the SAME leg is rebuilt through the Makefile's own recipe (`make
aclk-build` with RSP_SRC or DP_SRC, and ACLK_MDIR, overridden) and run in
the short mode that holds the check: `--render-only` for the stage's
defects, `--live-only` for the datapath's trigger. Each mutant must make the
leg FAIL by its OWN verdict (a `[FAIL]` line or a tally with failures, read
by scripts/suite_tally.py), and the named check must be among the failures;
a crash or an abort is not a catch. The positive control is the clean leg
the sweep just ran (obj_aclk): it is re-run here in both short modes so the
verdicts come from the same binary shape.

What bounds a livelocking mutant. This driver sets no host-time deadline
on a run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item
4). Both short legs of sim_aclk.cpp are cycle-bounded by construction, not
by a cap constant: each steps a fixed count out of reset, binds listener 0
through fixed step loops and an AXI4-Lite BFM whose every handshake gives
up after kAxiGuardCycles (2048 cycles), injects each frame through inject()
(at most 1500 cycles), and runs its windows through run_fed (a fixed cycle
target each; the feed's slot-boundary wait is bounded by the PDU period);
no loop on either path waits on a DUT output without a cycle bound, so a
leg ends at the same cycle whatever the mutated gateware does. The
host-time bound is the sweep's: scripts/run_all_suites.sh runs this suite's
`make` (whose `run` recipe ends with `python3 render_mutants.py`) under its
per-suite guard, suite_timeout = 1800 s, and reports a kill as TIMEOUT, an
UNKNOWN result (exit 92), never a pass or a fail. The SIGTERM handler in
main() turns that kill into an exit that removes the temporary directory
and the leg's own process group. Run by hand, outside the sweep, nothing
but the cycle bound limits a run.

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
STAGE_RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
CLEAN_EXE = HERE / "obj_aclk/Vmilan_dp_aclk"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the two sources a mutant may plant into: (path, the Makefile override)
SOURCES = {
    "stage": (STAGE_RTL, "RSP_SRC"),
    "datapath": (DP_RTL, "DP_SRC"),
}

#: (name, source, pattern, replacement, the leg's short mode, the check this
#: defect must break)
MUTATIONS = [
    ("prefill target three events high", "stage",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P;",
     "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P + 3;",
     "--render-only",
     "RENDER-INT: every PDU's first event inside the law band"),
    ("recentre pulse ignored", "stage",
     "if (recentre_p_i && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "if (1'b0 && !prefill_r[s]) pend_r[s] <= 1'b1;",
     "--render-only",
     "RENDER-RC-INT: the recentre restored the law (fill at accept = setpoint) (late)"),
    ("recentre counted and cleared but not snapped", "stage",
     "              if (enough_w) begin\n"
     "                rptr_r[s]    <= snap_rptr_w;\n"
     "                prefill_r[s] <= 1'b0;\n"
     "                pend_r[s]    <= 1'b0;\n",
     "              if (enough_w) begin\n"
     "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : rptr_r[s];\n"
     "                prefill_r[s] <= 1'b0;\n"
     "                pend_r[s]    <= 1'b0;\n",
     "--render-only",
     "RENDER-RC-INT: the recentre restored the law (fill at accept = setpoint) (early)"),
    ("clock-source trigger dropped from the recentre set", "datapath",
     "       | src_recentre_p_r;",
     "       | 1'b0;",
     "--live-only",
     "RENDER-LIVE-CRF: the fill at accept is the setpoint for every PDU"),
]


def build(override: str, rtl_path: Path, mdir: Path) -> Path | None:
    """Build the leg against `rtl_path` through the suite's own recipe."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "aclk-build", f"{override}={rtl_path}",
         f"ACLK_MDIR={mdir}"],
        capture_output=True, text=True)
    exe = mdir / "Vmilan_dp_aclk"
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path, mode: str) -> tuple[int, str]:
    """(rc, stdout) of one short-mode run, waited for with no host deadline:
    the leg is cycle-bounded (module docstring). The leg is its own session,
    so the sweep's kill reaches it only through the SIGTERM handler in
    main(), whose exit runs the kill below."""
    proc = subprocess.Popen([str(exe), mode], cwd=str(HERE),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate()
        return proc.returncode, out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
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
    """Run the positive controls and every mutant; 1 if any mutant survived."""
    sources = {key: path.read_text() for key, (path, _) in SOURCES.items()}
    passes = fails = 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    with tempfile.TemporaryDirectory(prefix="render-mutants-") as td:
        work = Path(td)
        exe = CLEAN_EXE if CLEAN_EXE.is_file() else build("RSP_SRC", STAGE_RTL, work / "obj_clean")
        for mode in sorted({m[4] for m in MUTATIONS}):
            answer = verdict(*run_leg(exe, mode), None) if exe else "did not compile"
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the render-law leg ({mode})")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass ({mode}: {answer}) - "
                      f"every mutant result in that mode is meaningless")
        for name, source, pattern, replacement, mode, breaks in MUTATIONS:
            src = sources[source]
            path, override = SOURCES[source]
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s) in {path.name}, expected exactly 1. "
                      f"The RTL moved and this mutant is no longer mutating "
                      f"anything - fix the pattern, do not delete the arm.")
                continue
            tag = name.replace(" ", "_").replace("-", "_")
            mpath = work / f"{path.stem}_{tag}.sv"
            mpath.write_text(src.replace(pattern, replacement))
            exe = build(override, mpath, work / f"obj_{tag}")
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the leg")
                continue
            answer = verdict(*run_leg(exe, mode), breaks)
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught ({mode}): {name} - breaks \"{breaks}\"")
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
