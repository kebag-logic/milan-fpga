#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #387 pending-restart merge in tkdiag: prove T17 can fail.

sim_main.cpp's T17 asserts that a restart request landing on a PENDING one
merges with it (#387, ruling 5802264260 item 2): the stream puts exactly one
toggle on the wire, never none, and its MEDIA_RESET counts it, while a stream
that already stamped the earlier request gets a toggle of its own. So the real
KL_media_clock_restart is mutated, one defect at a time, and the SAME harness
is rebuilt through the Makefile's own recipe (`make build` with MCR_SRC and
TKDIAG_MDIR overridden) and run. Each mutant must make the harness FAIL by its
OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), and the named check must be among the failures; a
crash or an abort is not a catch. The positive control is the clean harness
that `make` just built (obj_dir), re-run here.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The harness is
cycle-bounded by construction: every case steps a fixed number of cycles and
no loop waits on a DUT output, so a mutant ends at the same cycle as the clean
harness. The host-time bound is the sweep's per-suite guard in
scripts/run_all_suites.sh; the SIGTERM handler turns that kill into an exit
that removes the temporary directory.

Usage: make -C tb/verilator/tkdiag   (or python3 mcr_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MCR_RTL = HERE / "../../../hdl/ieee1722/avtp/KL_media_clock_restart.sv"
CLEAN_MDIR = HERE / "obj_dir"
EXE_NAME = "Vtkdiag_sim"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the one line the merge lives on
MERGE_LINE = "      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;"

# (name, the ONE line it replaces, its replacement, the check it must fail)
MUTATIONS = [
    ("a request flips the target, cancelling a pending restart",
     MERGE_LINE,
     "      if (restart_p_i | src_change_w) tgt_r <= ~tgt_r;",
     "T17 talker 1 puts exactly ONE toggle on the wire, never none"),
    ("one shared target that merges while any stream is pending",
     MERGE_LINE,
     "      if ((restart_p_i | src_change_w) && !(|((tgt_r ^ mr_o) & streaming_i)))\n"
     "        tgt_r <= ~tgt_r;",
     "T17 talker 0 had stamped the disruption: the step is its 2nd toggle"),
]


def build(rtl_path: Path, mdir: Path) -> Path | None:
    """Build the harness against `rtl_path` through the suite's own recipe;
    the executable, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "build", f"MCR_SRC={rtl_path}",
         f"TKDIAG_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of the harness, with no host deadline: it is
    cycle-bounded (module docstring)."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                         text=True, check=False)
    return out.returncode, out.stdout + out.stderr


def failed_checks(out: str) -> list[str]:
    """The names of the checks the harness printed as failed, in order."""
    return [line.strip()[len("[FAIL]"):].split(" got=")[0].strip()
            for line in out.splitlines() if line.strip().startswith("[FAIL]")]


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


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, pattern, replacement, breaks = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {MCR_RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
        return False
    tag = name.replace(" ", "_").replace(",", "")
    mpath = work / f"KL_media_clock_restart_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
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
    src = MCR_RTL.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="mcr-mutants-") as td:
        work = Path(td)
        clean = CLEAN_MDIR / EXE_NAME
        exe = clean if clean.is_file() else build(MCR_RTL, work / "obj_clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated restart engine still passes the tkdiag harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated restart engine does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in MUTATIONS:
            if run_mutant(src, mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
