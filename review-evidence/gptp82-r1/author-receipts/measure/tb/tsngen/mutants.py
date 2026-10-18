#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the tsngen suite: prove its checks are load-bearing.

Why this exists. `run_tsngen.py` drives the engine with frames an INDEPENDENT
generator builds, and checks BMCA outcomes, Announce contents, Sync/Follow_Up
pairing, Pdelay responses and the published offsets - the widest behavioural
net in this repository. Nothing proved any of it could fail. A harness whose
assertions never fail is indistinguishable from a harness that asserts
nothing, and this one is the independent judge the engine is measured by.

So the real engine RTL is mutated, one defect at a time, and the SAME harness
is run against each mutant. Every mutant must make it FAIL. The unmutated
build must still PASS - without that control the arm would be satisfied by a
harness that fails on everything.

The suite is staged into a temporary directory, mutated sources and all, so
nothing is written into the tree and the tracked microcode image is held
constant: only the RTL under test varies between runs.

What this arm found the suite does NOT prove: a parser that accepts a foreign
domainNumber survives every check, because the generator only ever builds
domain-0 frames, and a discarded received stepsRemoved survives too. Both are
recorded rather than hidden - the value of a mutation arm is the map of what
it cannot reach - and both need new SCENARIOS, not new mutants.

This arm SKIPS exactly when the suite skips. `run_tsngen.py` exits 0 with a
`SKIP:` line when the tsn-gen checkout is absent, so on a host without it
there is nothing to prove and the arm says so rather than inventing a pass.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = (HERE / "../../hdl").resolve()
sys.path.insert(0, str((HERE / "../").resolve()))

from mutation_verdict import verdict  # noqa: E402

#: the engine sources the suite elaborates, in the Makefile's order
SOURCES = (
    "ucpu/gptp_ucpu_pkg.sv", "ucpu/KL_gptp_ucpu.sv",
    "wire/KL_gptp_rx_parser.sv", "wire/KL_gptp_tx_slot.sv",
    "common/KL_gptp_timer.sv", "top/KL_gptp_engine.sv",
)

#: (name, file, pattern, replacement, the assertion this defect should break)
MUTATIONS = [
    ("received sequenceId zeroed", "wire/KL_gptp_rx_parser.sv",
     "bank_wdata_o <= {8'd0, 4'd0, mtype_r, seq_r, DOMAIN_C,",
     "bank_wdata_o <= {8'd0, 4'd0, mtype_r, 16'd0, DOMAIN_C,",
     "a Follow_Up is paired with its Sync by the sequenceId that arrived, "
     "not by a constant"),
    ("announce grandmasterIdentity discarded", "wire/KL_gptp_rx_parser.sv",
     "gm_r         <= acc_nxt_w;",
     "gm_r         <= '0;",
     "the grandmasterIdentity an Announce carries is the identity BMCA "
     "compares, so a better master is recognised as one"),
    ("transmit end of frame one byte early", "wire/KL_gptp_tx_slot.sv",
     "assign tx_eof_o   = ser_run_r && (ser_left_r == 11'd1);",
     "assign tx_eof_o   = ser_run_r && (ser_left_r == 11'd2);",
     "a transmitted frame carries every byte the slot holds"),
]

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "0", "--top-module", "KL_gptp_engine",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
    "-GUCODE_HEX_P=\"gptp_ucode.hex\"", "-GCLK_HZ_P=2000000",
]


def stage(work: Path, tag: str,
          mutate: tuple[str, str, str] | None = None) -> Path:
    """A self-contained copy of the suite, with at most one source mutated.

    `mutate` is the (source, pattern, replacement) triple of MUTATIONS; the
    replacement is applied to that one source as it is copied, so the staged
    tree differs from the tree under test in exactly one place. The returned
    directory holds the harness, its microcode image and the RTL, and nothing
    outside it is written.
    """
    suite = work / f"suite_{tag}"
    (suite / "rtl").mkdir(parents=True)
    for rel in SOURCES:
        text = (RTL / rel).read_text()
        if mutate is not None and mutate[0] == rel:
            text = text.replace(mutate[1], mutate[2])
        dst = suite / "rtl" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text)
    for name in ("run_tsngen.py", "tsngen_main.cpp", "gptp_ucode.hex"):
        shutil.copy2(HERE / name, suite / name)
    # `tsngen_main.cpp` includes the shared model owner as
    # `../common/verilator_harness.hpp` (Core Guidelines R.11, and the copy
    # `check_cpp_idiom.py` refuses to let drift). That header lives one
    # directory up from the suite, so the staged tree needs it at the same
    # relative place. Without it every build below fails to compile, and a
    # build that fails is reported as a mutant that proves nothing -- four
    # red checks on a host whose only real answer is the skip below.
    common = suite.parent / "common"
    common.mkdir(exist_ok=True)
    shutil.copy2(HERE.parent / "common" / "verilator_harness.hpp",
                 common / "verilator_harness.hpp")
    return suite


def build(suite: Path) -> bool:
    """Build the staged suite into its own obj_dir; True when it produced one."""
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(suite / "obj_dir"),
         "-CFLAGS", f"-std=c++17 -O2 -I{suite}",
         *[str(suite / "rtl" / rel) for rel in SOURCES],
         str(suite / "tsngen_main.cpp"), "-o", "Vtsngen"],
        capture_output=True, text=True, cwd=suite)
    return (suite / "obj_dir" / "Vtsngen").is_file() and out.returncode == 0


def run_harness(suite: Path) -> tuple[int, str]:
    """(rc, stdout) of the staged run_tsngen.py.

    No host deadline: tsngen_main.cpp puts an explicit tick ceiling on every
    wait, so a mutant that stops the engine advancing still returns a verdict
    rather than hanging.
    """
    out = subprocess.run([sys.executable, "run_tsngen.py"], cwd=suite,
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr



def main() -> int:
    """Run the control and every mutant, and report the arm's exit status.

    0 when the unmutated engine passes and every mutant is caught, or when
    the suite skips because there is no tsn-gen checkout to judge against;
    1 when any mutant survived, failed to build, or no longer matches its
    pattern - each of which is printed with the assertion it was defending.
    """
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="tsngen-mutants-") as td:
        work = Path(td)

        # -- positive control: the real RTL must still pass -------------------
        suite = stage(work, "clean")
        answer = verdict(*run_harness(suite)) \
            if build(suite) else "did not compile"
        if answer == "skipped":
            print("SKIP: the suite itself skips here (no tsn-gen checkout), "
                  "so there is nothing for a mutation arm to prove")
            return 0
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated engine RTL still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated engine RTL does NOT pass ({answer}) - "
                  f"every mutant result below is meaningless")

        # -- each mutant must be caught ---------------------------------------
        for name, rel, pattern, replacement, breaks in MUTATIONS:
            src = (RTL / rel).read_text()
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s) in {rel}, expected "
                      f"exactly 1. The RTL moved and this mutant is no longer "
                      f"mutating anything - fix the pattern, do not delete "
                      f"the arm.")
                continue
            tag = name.replace(" ", "_")
            suite = stage(work, tag, (rel, pattern, replacement))
            if not build(suite):
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant "
                      f"that cannot build proves nothing about the harness")
                continue
            answer = verdict(*run_harness(suite))
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
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
