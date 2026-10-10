#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects for the CSR read-path lockstep: prove each named check can fail.

sim_lock.cpp runs the current milan_csr beside the frozen e8454e27 block and
grades five named checks (its banner). This driver plants ONE defect at a time
into a copy of hdl/common/csr/milan_csr.sv, rebuilds the 1x1 lockstep leg
through the Makefile's own recipe (`make lock1`, or `make lock8` for a defect
only an extra context can reach, with LOCK_SRC and the leg's build directory
overridden) and runs it. A mutant is caught only when the harness fails by its
own verdict AND the check named for that defect class is among the failures;
a crash, an abort or a failure of some other check is not a catch. The
positive control is the clean leg `make` just built (obj_lock1), re-run here,
or rebuilt when it is older than any input of its recipe.

The classes are the lane's (issue #640, lane M5): a wrong address decode, a
torn multi-word snapshot, a stale snapshot after an update and a reset-value
drift. Two more defects land in the lane's own stage-1/stage-2 change.

What bounds a run. The harness is cycle-bounded by construction (every AXI
wait has a cycle guard) and this driver sets no host-time deadline; the
sweep's per-suite guard in scripts/run_all_suites.sh is the host-time bound,
and the SIGTERM handler turns that kill into an exit that removes the
temporary directory.

Usage: make -C tb/verilator/csr   (or python3 lock_mutants.py from there)
Exit 0 = every mutant was caught and the clean leg still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSR_RTL = HERE / "../../../hdl/common/csr/milan_csr.sv"
CLEAN_MDIR = HERE / "obj_lock1"
EXE_NAME = "Vcsr_lock"
#: every input of the clean recipe: a clean binary older than any is stale
CLEAN_INPUTS = [CSR_RTL, HERE / "milan_csr_ref.sv", HERE / "gen_lockstep.py",
                HERE / "sim_lock.cpp", HERE / "Makefile",
                HERE / "../../common/verilator_harness.hpp"]
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

# (name, the ONE text it replaces, its replacement, the check it must fail,
#  the leg that can reach it)
MUTATIONS = [
    ("wrong address decode: IRQ_RAW's live word answers at IRQ_MASK",
     "      A_IRQ_RAW:    live_mux = irq_status;",
     "      A_IRQ_MASK:   live_mux = irq_status;",
     "decode", "lock1"),
    ("torn snapshot: window CNT3 reads its live counter, not the SNAP word",
     "              SK_RAW_C:    strm_mux = snap_shadow_r[1 + 32'(coff[5:2])];",
     "              SK_RAW_C:    strm_mux = (coff[5:2] == 4'd3) ? i_avtprx_cnt10[3*32 +: 32]\n"
     "                                      : snap_shadow_r[1 + 32'(coff[5:2])];",
     "snapshot-coherence", "lock1"),
    ("stale snapshot: a listener SNAP after a talker SNAP keeps the POISON kind",
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_RAW_C;\n",
     "",
     "snapshot-freshness", "lock1"),
    ("stale snapshot: an extra listener's burst word keeps its previous kind",
     "                snap_kind_r[snap_wi_r]   <= SK_RAW_C;\n",
     "",
     "snapshot-freshness", "lock8"),
    ("reset-value drift: the CNT kinds reset to POISON instead of zero",
     "      for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_ZERO_C;\n    end else begin",
     "      for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_POISON_C;\n    end else begin",
     "reset-values", "lock1"),
    ("stage 1: the shadow word is not zeroed under a live or window claim",
     "    if (!aresetn || (rd_pend && !shadow_rd_w))",
     "    if (!aresetn)",
     "decode", "lock1"),
    ("stage 1: the window's range leaf answers 0 instead of the window's word",
     "          live_mux = strm_mux;",
     "          live_mux = 32'h0;",
     "decode", "lock1"),
]


def build(rtl_path: Path, mdir: Path, leg: str = "lock1") -> Path | None:
    """Build a lockstep leg against `rtl_path` through the suite's own recipe;
    the executable, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), leg, f"LOCK_SRC={rtl_path}",
         f"{leg.upper()}_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def is_fresh(exe: Path) -> bool:
    """True when `exe` exists and is no older than any input of its recipe."""
    return exe.is_file() and all(exe.stat().st_mtime >= src.stat().st_mtime
                                 for src in CLEAN_INPUTS)


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of the harness, with no host deadline: it is
    cycle-bounded (module docstring)."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                         text=True, check=False)
    return out.returncode, out.stdout + out.stderr


def failed_checks(out: str) -> list[str]:
    """The names of the checks the harness printed as failed, in order."""
    return [line.strip()[len("[FAIL]"):].split(":")[0].strip()
            for line in out.splitlines() if line.strip().startswith("[FAIL]")]


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and must_fail not in failed_checks(out):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def run_mutant(src: str, mutation: tuple[str, str, str, str, str], work: Path,
               n: int) -> bool:
    """Plant one mutation, build and run its leg; True when it was caught."""
    name, pattern, replacement, breaks, leg = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {CSR_RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
        return False
    mpath = work / f"m{n}" / "milan_csr.sv"
    mpath.parent.mkdir()
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"m{n}" / "obj", leg)
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught ({leg}): {name} - fails \"{breaks}\"")
        print(f"    it failed {', '.join(failed_checks(out))}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = CSR_RTL.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="csr-lock-mutants-") as td:
        work = Path(td)
        exe = CLEAN_MDIR / EXE_NAME
        if not is_fresh(exe):
            print(f"[INFO] {exe.relative_to(HERE)} is missing or older than its "
                  f"sources: the positive control is rebuilt")
            exe = build(CSR_RTL.resolve(), work / "clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated block still passes the lockstep leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated block does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for n, mutation in enumerate(MUTATIONS):
            if run_mutant(src, mutation, work, n):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
