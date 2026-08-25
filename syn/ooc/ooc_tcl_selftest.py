#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive the two OOC .tcl recipes' pre-synthesis refusals, automatically.

pp_shadow_ooc.tcl refuses to synthesize when a `$readmemh` image is missing or
empty, and it takes the source generator's exit status. Both refusals had
manual evidence and no test ([R0] on PR #240): deleting either one left every
hosted check green, which is the definition of a defense that rots.

milan_datapath_ooc.tcl (#246) GENERATES both images into its run directory
and then applies the same missing-or-empty refusal; a ROM generator that
fails, or one that exits 0 leaving an empty image, must abort the script
before anything is read. Its arms below plant exactly those failures through
a dispatching `python3` stub that hands every other invocation (dp_srcs.py,
the other generator) to the real interpreter.

WHAT IT RUNS IS THE REAL .TCL, not a copy of its logic. `tclsh` sources the
tracked file with the Vivado-only commands stubbed, and `read_verilog` -- the
first command after the refusals -- prints a sentinel and exits 0. So an arm
that expects a refusal fails if the sentinel appears, and the positive arm fails
if it does not: removing the guard from the .tcl reddens this, and so does a
guard that fires on a well-formed directory.

`tclsh` is the interpreter Vivado embeds, so the guard is exercised by the
language it is written in rather than reimplemented in Python.

    python3 syn/ooc/ooc_tcl_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/dp_srcs.py --selftest.
Needs the protocol-processor and verilog-axis submodules, because both .tcl
files derive their read set (and the datapath one generates its ROMs) on the
way to their refusals.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TCL = os.path.join(HERE, "pp_shadow_ooc.tcl")
DP_TCL = os.path.join(HERE, "milan_datapath_ooc.tcl")
SENTINEL = "OOC-GUARD-PASSED"
REAL_PYTHON = shutil.which("python3") or sys.executable

#: The Vivado commands the .tcl recipes call after their refusals.
#: `read_verilog` is the first of them, so reaching it means every refusal let
#: the run through.
STUBS = """
proc read_verilog args { puts "%s"; exit 0 }
proc synth_design args {}
proc create_clock args {}
proc get_ports args { return {} }
proc report_utilization args {}
proc report_timing_summary args {}
proc set_msg_config args {}
source {%s}
"""

#: python3 dispatcher for the milan_datapath arms: sabotage the one script the
#: arm plants a failure in, hand everything else (dp_srcs.py, the other
#: generator) to the real interpreter, so the generation path the positive arm
#: proves is the shipping one.
PY_DISPATCH = """#!/bin/sh
out=""
prev=""
hit=0
for a in "$@"; do
  case "$a" in */%(target)s) hit=1 ;; esac
  [ "$prev" = "-o" ] && out="$a"
  prev="$a"
done
if [ "$hit" = 1 ]; then
  %(action)s
fi
exec %(real)s "$@"
"""

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 9


def _run(workdir, env=None, tcl=TCL):
    e = dict(os.environ)
    e.update(env or {})
    # A driver FILE, not tclsh's stdin: reading a script from stdin makes an
    # uncaught error a printed message at exit 0, which would make every arm
    # below agree with a guard that does not exist.
    fd, driver = tempfile.mkstemp(suffix=".tcl", prefix="ooc-driver-")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(STUBS % (SENTINEL, tcl))
        out = subprocess.run(["tclsh", driver], cwd=workdir, env=e,
                             capture_output=True, text=True)
    finally:
        os.unlink(driver)
    return out.returncode, out.stdout + out.stderr


def _py_sabotage(target, action):
    """A scratch bin dir whose python3 dispatches; caller prepends to PATH."""
    stub = tempfile.mkdtemp(prefix="dp-rom-plant-")
    p = os.path.join(stub, "python3")
    with open(p, "w") as fh:
        fh.write(PY_DISPATCH % {"target": target, "action": action,
                                "real": REAL_PYTHON})
    os.chmod(p, 0o755)
    return stub


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

    def arm(name, want, expect_rc0, setup=None, env=None, tcl=TCL,
            check=None):
        nonlocal ran
        ran += 1
        with tempfile.TemporaryDirectory() as d:
            if setup:
                setup(d)
            rc, log = _run(d, env, tcl)
            reached = SENTINEL in log
            if expect_rc0:
                if rc != 0 or not reached:
                    problems.append("SELF-TEST FAILED [%s]: a well-formed run "
                                    "must reach synthesis, got rc=%d, "
                                    "sentinel=%s\n%s"
                                    % (name, rc, reached, log.strip()))
                    return
            elif rc == 0 or reached or want not in log:
                problems.append("SELF-TEST FAILED [%s]: expected a refusal "
                                "naming %r before synthesis, got rc=%d, "
                                "sentinel=%s\n%s"
                                % (name, want, rc, reached, log.strip()))
                return
            if check:
                miss = check(d)
                if miss:
                    problems.append("SELF-TEST FAILED [%s]: %s\n%s"
                                    % (name, miss, log.strip()))

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

    # ---- milan_datapath_ooc.tcl (#246). It GENERATES both images, so its
    # arms plant failures in the generators themselves, not in the directory.

    def dp_env(target, action):
        stub = _py_sabotage(target, action)
        return stub, {"PATH": stub + os.pathsep + os.environ.get("PATH", "")}

    # Arm 6. A dead microcode generator aborts the script: its exit status is
    # taken by `exec`, never discarded. Before #246 nothing ran the generator
    # at all and Vivado priced an all-zero ROM at rc=0.
    stub, env = dp_env("gen_ucode.py",
                       "echo 'planted ucode generator failure' >&2\n  exit 3")
    arm("dp-ucode-generator-fail", "planted ucode generator failure", False,
        env=env, tcl=DP_TCL)
    shutil.rmtree(stub, ignore_errors=True)

    # Arm 7. A generator that exits 0 leaving an empty image is the same
    # refusal: `file exists` alone would pass it, and Vivado reads an empty
    # image exactly as it reads an absent one.
    stub, env = dp_env("gen_ucode.py", ": > \"$out\"\n  exit 0")
    arm("dp-ucode-empty", "ucode.hex is missing or empty", False,
        env=env, tcl=DP_TCL)
    shutil.rmtree(stub, ignore_errors=True)

    # Arm 8. The transition-ROM generator gets the identical treatment.
    stub, env = dp_env("gen_ltn_rom.py",
                       "echo 'planted ltn generator failure' >&2\n  exit 3")
    arm("dp-ltn-generator-fail", "planted ltn generator failure", False,
        env=env, tcl=DP_TCL)
    shutil.rmtree(stub, ignore_errors=True)

    # Arm 9. ANTI-VACUITY. From an EMPTY directory the real generators run,
    # both images land in the run directory non-empty, and the script reaches
    # synthesis. Without this arm a preflight that always refuses passes
    # arms 6-8.
    def dp_images_present(d):
        for img in ("ltn_rom.hex", "ucode.hex"):
            p = os.path.join(d, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run directory" % img
        return None
    arm("dp-empty-dir-generates-and-passes", None, True, tcl=DP_TCL,
        check=dp_images_present)

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
    print("OOC .tcl refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())
