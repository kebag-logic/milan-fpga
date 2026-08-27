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

Each mutation names the assertion it should break, and the pattern it rewrites
is REQUIRED to be present exactly once. A refactor that moves the priority
encoder does not silently skip its mutant; it fails here, which is the point -
a mutation arm that quietly stops mutating is the defect it exists to catch.

Usage: python3 mutants.py      (run from tb/verilator/tcam)
Exit 0 = every mutant was caught and the clean build still passes.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee8021q/filtering/tcam.sv"

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
    "-CFLAGS", "-std=c++17 -O2",
]


def build_and_run(rtl_path, workdir, tag):
    """Build the harness against `rtl_path` and return its exit status."""
    mdir = workdir / f"obj_{tag}"
    #: verilator resolves -o RELATIVE TO --Mdir, so the name is bare and the
    #: binary is looked up inside that directory
    exe_name = f"Vtcam_{tag}"
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir), str(rtl_path),
         str(HERE / "sim_main.cpp"), "-o", exe_name],
        capture_output=True, text=True)
    if out.returncode != 0:
        return None, out.stderr[-400:]
    exe = mdir / exe_name
    if not exe.is_file():
        return None, f"verilator produced no {exe}"
    run = subprocess.run([str(exe)], capture_output=True, text=True)
    return run.returncode, run.stdout


def main():
    src = RTL.read_text()
    passes = fails = 0

    with tempfile.TemporaryDirectory(prefix="tcam-mutants-") as td:
        work = Path(td)

        # -- positive control: the real RTL must still pass -------------------
        clean = work / "tcam.sv"
        clean.write_text(src)
        rc, _ = build_and_run(clean, work, "clean")
        if rc == 0:
            passes += 1
            print("[PASS] the unmutated RTL still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated RTL does NOT pass (rc={rc}) - every "
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
            mpath = work / f"tcam_{name.replace(' ', '_')}.sv"
            mpath.write_text(src.replace(pattern, replacement))
            rc, _out = build_and_run(mpath, work, name.replace(" ", "_"))
            if rc is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the harness")
            elif rc != 0:
                passes += 1
                print(f"[PASS] mutant caught: {name} — breaks \"{breaks}\"")
            else:
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove \"{breaks}\".")

    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
