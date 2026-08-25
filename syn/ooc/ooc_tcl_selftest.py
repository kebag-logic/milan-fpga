#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/ooc/pp_shadow_ooc.tcl's two pre-synthesis refusals, automatically.

That script refuses to synthesize when a `$readmemh` image is missing or empty,
and it takes the source generator's exit status. Both refusals had manual
evidence and no test ([R0] on PR #240): deleting either one left every hosted
check green, which is the definition of a defense that rots.

WHAT IT RUNS IS THE REAL .TCL, not a copy of its logic. `tclsh` sources the
tracked file with the Vivado-only commands stubbed, and `read_verilog` -- the
first command after both refusals -- prints a sentinel and exits 0. So an arm
that expects a refusal fails if the sentinel appears, and the positive arm fails
if it does not: removing the guard from the .tcl reddens this, and so does a
guard that fires on a well-formed directory.

`tclsh` is the interpreter Vivado embeds, so the guard is exercised by the
language it is written in rather than reimplemented in Python.

    python3 syn/ooc/ooc_tcl_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/dp_srcs.py --selftest.
Needs the protocol-processor and verilog-axis submodules, because the .tcl
derives its read set before it reaches either refusal.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TCL = os.path.join(HERE, "pp_shadow_ooc.tcl")
SENTINEL = "OOC-GUARD-PASSED"

#: The Vivado commands pp_shadow_ooc.tcl calls after its refusals. `read_verilog`
#: is the first of them, so reaching it means every refusal let the run through.
STUBS = """
proc read_verilog args { puts "%s"; exit 0 }
proc synth_design args {}
proc create_clock args {}
proc get_ports args { return {} }
proc report_utilization args {}
proc report_timing_summary args {}
source {%s}
""" % (SENTINEL, TCL)

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 5


def _run(workdir, env=None):
    e = dict(os.environ)
    e.update(env or {})
    # A driver FILE, not tclsh's stdin: reading a script from stdin makes an
    # uncaught error a printed message at exit 0, which would make every arm
    # below agree with a guard that does not exist.
    fd, driver = tempfile.mkstemp(suffix=".tcl", prefix="ooc-driver-")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(STUBS)
        out = subprocess.run(["tclsh", driver], cwd=workdir, env=e,
                             capture_output=True, text=True)
    finally:
        os.unlink(driver)
    return out.returncode, out.stdout + out.stderr


def _write(workdir, name, content):
    with open(os.path.join(workdir, name), "w") as fh:
        fh.write(content)


def selftest():
    problems, ran = [], 0
    if not shutil.which("tclsh"):
        # NOT a skip. A skip here is the false green this file exists to close;
        # the workflow installs tclsh for exactly this reason.
        return ["tclsh is not on PATH, so %s cannot be exercised. Install tcl "
                "(the interpreter Vivado embeds) rather than skipping: an "
                "unexercised refusal is the defect this file tests for."
                % os.path.relpath(TCL, REPO)], 0

    def arm(name, want, expect_rc0, setup=None, env=None):
        nonlocal ran
        ran += 1
        with tempfile.TemporaryDirectory() as d:
            if setup:
                setup(d)
            rc, log = _run(d, env)
        reached = SENTINEL in log
        if expect_rc0:
            if rc != 0 or not reached:
                problems.append("SELF-TEST FAILED [%s]: a well-formed run must "
                                "reach synthesis, got rc=%d, sentinel=%s\n%s"
                                % (name, rc, reached, log.strip()))
            return
        if rc == 0 or reached or want not in log:
            problems.append("SELF-TEST FAILED [%s]: expected a refusal naming "
                            "%r before synthesis, got rc=%d, sentinel=%s\n%s"
                            % (name, want, rc, reached, log.strip()))

    def images(*names):
        def setup(d):
            for n in names:
                _write(d, n, "" if n.endswith("!") else "00\n")
            for n in names:
                if n.endswith("!"):
                    os.rename(os.path.join(d, n), os.path.join(d, n[:-1]))
        return setup

    # Arm 1. Neither image. The first one named is the one reported.
    arm("no-images", "ltn_rom.hex is missing or empty", False)

    # Arm 2. The image the finding document used to name on its own. The AECP
    # microcode ROM is the one it did not, and its absence is a CRITICAL
    # WARNING ending in "ignoring" plus a utilization number 17 % low.
    arm("ucode-missing", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex"))

    # Arm 3. Present and zero bytes: `file exists` alone would pass this, and
    # Vivado reads an empty image exactly as it reads an absent one.
    arm("ucode-empty", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex", "ucode.hex!"))

    # Arm 4. ANTI-VACUITY. Both images present and non-empty must reach
    # synthesis. Without this arm a guard that always fires passes arms 1-3.
    arm("both-images-present", None, True, images("ltn_rom.hex", "ucode.hex"))

    # Arm 5. The .tcl must take the generator's exit status. A consumer that
    # discards it synthesizes whatever a broken generator printed, and an empty
    # source list builds cleanly while proving nothing (CONTRIBUTING.md 3).
    stub = tempfile.mkdtemp(prefix="dp-srcs-fails-")
    with open(os.path.join(stub, "python3"), "w") as fh:
        fh.write("#!/bin/sh\necho 'dp_srcs: planted generator failure' >&2\n"
                 "exit 2\n")
    os.chmod(os.path.join(stub, "python3"), 0o755)
    arm("generator-failure-propagates", "planted generator failure", False,
        images("ltn_rom.hex", "ucode.hex"),
        env={"PATH": stub + os.pathsep + os.environ.get("PATH", "")})
    shutil.rmtree(stub, ignore_errors=True)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), this file "
                        "declares %d." % (ran, ARMS))
    return problems, ran


def main() -> int:
    bad, ran = selftest()
    for b in bad:
        print("  -", b, file=sys.stderr)
    if bad:
        return 2
    print("pp_shadow OOC refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())
