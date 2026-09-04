#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the tcam suite: prove its assertions are load-bearing.

Why this exists. `sim_main.cpp` checks exact match, ternary match, priority,
the multi-hit vector, add/remove/update and a clean miss - and nothing proved
any of those checks could fail. A harness whose assertions never fail is
indistinguishable from a harness that asserts nothing, and the TCAM is the
match engine behind the receive shield: a silently vacuous test here is a
silently unguarded filter.

So the real RTL is mutated, one defect at a time, and the SAME harness is run
against each mutant. Every mutant must make it FAIL. The unmutated build must
still PASS - without that control the arm would be satisfied by a harness that
fails on everything.

"Caught" means the harness's OWN verdict says so: a `[FAIL]` line or a tally
with a non-zero failure count in its stdout, read by the same reader the sweep
uses (scripts/suite_tally.py). A non-zero exit on its own is not a catch: a
mutant that makes the DUT abort or the process die by a signal has told us
nothing about the assertions, and is reported as exactly that. A mutant that
hangs is killed after MUTANT_RUN_TIMEOUT_S and reported TIMEOUT - not caught,
so the arm fails in seconds instead of hanging the sweep.

Each mutation names the assertion it should break, and the pattern it rewrites
is REQUIRED to be present exactly once. A refactor that moves the priority
encoder does not silently skip its mutant; it fails here, which is the point -
a mutation arm that quietly stops mutating is the defect it exists to catch.

Usage: python3 mutants.py      (run from tb/verilator/tcam)
Exit 0 = every mutant was caught and the clean build still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee8021q/filtering/tcam.sv"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: The harness runs in well under a second; a mutant still running after this
#: many seconds is livelocked (a loop that no longer advances), not slow.
MUTANT_RUN_TIMEOUT_S = 60

#: (name, pattern, replacement, the assertion this defect should break)
MUTATIONS = [
    ("priority inverted",
     "for (p = NUM_ENTRIES-1; p >= 0; p = p - 1) begin",
     "for (p = 0; p < NUM_ENTRIES; p = p + 1) begin",
     "lowest matching index wins (index 0 = highest priority)"),
    ("care mask ignored",
     "(((lookup_key_i ^ ent_key[m]) & ent_mask[m]) == {KEY_WIDTH{1'b0}})",
     "((lookup_key_i ^ ent_key[m]) == {KEY_WIDTH{1'b0}})",
     "a wildcard entry matches a range, not just its exact key"),
    ("entry validity ignored",
     "hit[m] = ent_valid[m] && ",
     "hit[m] = 1'b1 && ",
     "a removed entry stops matching"),
]

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "0", "--top-module", "tcam",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
    "-CFLAGS", "-std=c++17 -O2 -Wall -Wextra",
]


def build(rtl_path: Path, workdir: Path, tag: str) -> Path | None:
    """Build the harness against `rtl_path`; the executable path, or None."""
    mdir = workdir / f"obj_{tag}"
    #: verilator resolves -o RELATIVE TO --Mdir, so the name is bare and the
    #: binary is looked up inside that directory
    exe_name = f"Vtcam_{tag}"
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir), str(rtl_path),
         str(HERE / "sim_main.cpp"), "-o", exe_name],
        capture_output=True, text=True)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(exe: Path) -> tuple[int | str, str]:
    """(rc, stdout) of one harness run; rc is "TIMEOUT" when it was killed.

    The harness is its own process group, so the kill on timeout reaches
    anything it spawned, and nothing outlives the temporary directory.
    """
    proc = subprocess.Popen([str(exe)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=MUTANT_RUN_TIMEOUT_S)
        return proc.returncode, out
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        out, _ = proc.communicate()
        return "TIMEOUT", out
    finally:
        #: also on SIGTERM from the sweep's wall clock: no orphaned mutant
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def verdict(rc: int | str, out: str) -> str:
    """How the harness answered: 'pass', 'caught', or why it is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == "TIMEOUT":
        return f"TIMEOUT after {MUTANT_RUN_TIMEOUT_S}s - a hang is not a catch"
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived.

    A surviving mutant and a control that stopped passing are the same
    verdict here: the harness has stopped proving what it claims to prove.
    """
    src = RTL.read_text()
    passes = fails = 0

    #: The context manager removes the directory on any exception, and the
    #: SIGTERM handler turns the sweep's `timeout` kill into one, so a killed
    #: run leaves no tcam-mutants-* directory behind either.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    with tempfile.TemporaryDirectory(prefix="tcam-mutants-") as td:
        work = Path(td)

        # -- positive control: the real RTL must still pass -------------------
        clean = work / "tcam.sv"
        clean.write_text(src)
        exe = build(clean, work, "clean")
        answer = verdict(*run_harness(exe)) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated RTL still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated RTL does NOT pass ({answer}) - every "
                  f"mutant result below is meaningless")

        # -- each mutant must be caught ---------------------------------------
        for name, pattern, replacement, breaks in MUTATIONS:
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s), expected exactly 1. The "
                      f"RTL moved and this mutant is no longer mutating "
                      f"anything - fix the pattern, do not delete the arm.")
                continue
            tag = name.replace(" ", "_")
            mpath = work / f"tcam_{tag}.sv"
            mpath.write_text(src.replace(pattern, replacement))
            exe = build(mpath, work, tag)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the harness")
                continue
            answer = verdict(*run_harness(exe))
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} — breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")

    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
