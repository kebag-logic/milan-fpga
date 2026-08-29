#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove the rx_filter seam rejects a missing, swapped, tied-off and
direction-wrong binding - the four defect kinds issue #253 names.

The Makefile first runs the unmodified filter as the positive control: a
harness that rejects everything cannot satisfy these arms. Each arm then
applies ONE mutation to a copy of the RTL, builds the same boundary with the
SAME recipe the clean run used - read from the Makefile through
`make -s print-vflags`, never copied here (Rule 3) - and requires the verdict
that mutation must produce:

  - a MISSING binding and a DIRECTION-WRONG port are refused at the build, BY
    NAME: the Makefile's flag list promotes PINMISSING and UNDRIVEN to errors,
    so the refusal is `%Error-PINMISSING` / `%Error-UNDRIVEN` even under
    `-Wno-fatal`, and a build that fails for any other reason FAILS the arm.
    Verilator inlines the child and erases port direction, so a direction
    error has no behavioural signature: review measured a child `lookup_key_i`
    declared `output` building with a warning and running 62/62 under the old
    flags. That is why direction is a build refusal here and not a harness
    verdict, and the guide claims exactly that;
  - a SWAPPED and a TIED-OFF binding are legal SystemVerilog, so they must
    build, and the unmodified harness must return nonzero with its own
    `RESULT: FAIL`. For these two a build failure does not count, because it
    would not prove the behavioural seam is observed.

Every mutant is written under a temporary directory with its own --Mdir;
nothing lands in the tree.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILTER = HERE / "../../../hdl/ieee8021q/filtering/rx_mac_filter.sv"
TCAM = HERE / "../../../hdl/ieee8021q/filtering/tcam.sv"
HARNESS = HERE / "sim_main.cpp"

#: (name, file, text that must occur exactly once, replacement, refusal marker
#: the build must print - or None when the harness verdict is the proof)
ARMS = (
    ("missing lookup binding",
     FILTER, "    .lookup_key_i(dmac),\n", "", "%Error-PINMISSING"),
    ("swapped key and mask bindings",
     FILTER, ".wr_key_i(tcam_wr_key_i),\n    .wr_mask_i(tcam_wr_mask_i),",
     ".wr_key_i(tcam_wr_mask_i),\n    .wr_mask_i(tcam_wr_key_i),", None),
    ("tied-off lookup key",
     FILTER, ".lookup_key_i(dmac),", ".lookup_key_i(48'b0),", None),
    ("child lookup port declared output (direction-wrong binding)",
     TCAM, "input  wire [KEY_WIDTH-1:0]    lookup_key_i,",
     "output wire [KEY_WIDTH-1:0]    lookup_key_i,", "%Error-UNDRIVEN"),
    ("DUT m_tready declared output (direction-wrong boundary)",
     FILTER, "input  wire                     m_tready,",
     "output wire                     m_tready,", "%Error-UNDRIVEN"),
)


def build_recipe():
    """[verilator, flag, ...] exactly as the Makefile builds the clean run."""
    run = subprocess.run(["make", "-s", "-C", str(HERE), "print-vflags"],
                         capture_output=True, text=True, check=True)
    lines = [line for line in run.stdout.splitlines() if line]
    if len(lines) < 2:
        raise RuntimeError("make print-vflags returned no recipe")
    return lines


def run_arm(recipe, path, old, new, marker):
    """(passed, detail) for one mutation."""
    sources = {TCAM: TCAM.read_text(), FILTER: FILTER.read_text()}
    if sources[path].count(old) != 1:
        return False, "the anchor text was not found exactly once"
    sources[path] = sources[path].replace(old, new)
    with tempfile.TemporaryDirectory(prefix="rx-filter-binding-") as tmp:
        work = Path(tmp)
        for src, text in sources.items():
            (work / src.name).write_text(text)
        obj, exe = work / "obj_binding", "Vrx_filter_mutant"
        build = subprocess.run(
            [*recipe, "--Mdir", str(obj), str(work / TCAM.name),
             str(work / FILTER.name), str(HARNESS), "-o", exe],
            capture_output=True, text=True)
        if marker is not None:
            if build.returncode != 0 and marker in build.stderr:
                return True, f"refused at the build with {marker}"
            if build.returncode == 0:
                return False, "the build accepted it"
            return False, f"the build failed without {marker}:\n" + build.stderr[-800:]
        if build.returncode != 0:
            return False, ("did not compile, so the behavioural seam was not "
                           "exercised:\n" + build.stderr[-800:])
        run = subprocess.run([str(obj / exe)], capture_output=True, text=True)
        if run.returncode != 0 and "RESULT: FAIL" in run.stdout:
            tally = [line for line in run.stdout.splitlines() if line.startswith("checks:")]
            return True, "the harness rejected it" + (f" ({tally[-1]})" if tally else "")
        return False, "the harness accepted it:\n" + run.stdout[-800:] + run.stderr[-400:]


def main():
    recipe = build_recipe()
    passed = failed = 0
    for name, path, old, new, marker in ARMS:
        ok, detail = run_arm(recipe, path, old, new, marker)
        passed += ok
        failed += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    print(f"{passed + failed} checks: {passed} PASS, {failed} FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
