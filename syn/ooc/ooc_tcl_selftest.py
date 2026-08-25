#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive the two OOC .tcl recipes' pre-synthesis refusals, automatically.

pp_shadow_ooc.tcl refuses to synthesize when a `$readmemh` image is missing or
empty, and it takes the source generator's exit status. Both refusals had
manual evidence and no test ([R0] on PR #240): deleting either one left every
hosted check green, which is the definition of a defense that rots.

milan_datapath_ooc.tcl (#246) GENERATES both images into fresh temp targets,
validates their exact geometry against the pinned packages (word count and
width, //-comments stripped, x/z refused), and publishes each by rename only
after it validates, so a stale file plus a no-op generator, a one-token
image, a truncated image and a malformed word are all refusals before
anything is read ([R-parallel] on PR #264 closed those survivors). Its arms
below plant exactly those failures through a dispatching `python3` stub that
hands every other invocation (dp_srcs.py, the other generator) to the real
interpreter.

WHAT IT RUNS IS THE REAL .TCL, not a copy of its logic. `tclsh` sources the
tracked file with the Vivado-only commands stubbed. `read_verilog` RETURNS
(it does not exit), so the run reaches `synth_design`, whose stub is where
the sentinel prints -- after it has validated every `-generic *_HEX_P=...`
it receives: the value must be quoted, absolute, and name an existing
non-empty file, or the stub errors. `set_msg_config` is recorded and echoed
at synth_design as an `OOC-MSGCFG:` line, so the arms can assert the exact
`Synth 8-4445` promotion is (or, on a mutant, is not) in force. Mutation
copies of the datapath recipe itself (promotion deleted, the ucode generic
deleted, the ucode generic redirected at a missing image) prove each of
those assertions can fail.

`tclsh` is the interpreter Vivado embeds, so the guard is exercised by the
language it is written in rather than reimplemented in Python.

    python3 syn/ooc/ooc_tcl_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/dp_srcs.py --selftest.
Needs the protocol-processor and verilog-axis submodules, because both .tcl
files derive their read set (and the datapath one generates and validates
its ROMs) on the way to their refusals.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TCL = os.path.join(HERE, "pp_shadow_ooc.tcl")
DP_TCL = os.path.join(HERE, "milan_datapath_ooc.tcl")
SENTINEL = "OOC-GUARD-PASSED"
PROMOTION = "-id {Synth 8-4445} -new_severity ERROR"
REAL_PYTHON = shutil.which("python3") or sys.executable
GEN_UCODE = os.path.join(REPO, "protocol-processor", "hdl", "aecp", "ucode",
                         "gen_ucode.py")
GEN_LTN = os.path.join(REPO, "protocol-processor", "hdl", "acmp", "rom",
                       "gen_ltn_rom.py")

#: The Vivado commands the .tcl recipes call. `read_verilog` returns, so the
#: script reaches `synth_design`; the sentinel prints THERE, after the stub
#: has validated every `-generic *_HEX_P` it received (quoted, absolute,
#: existing, non-empty) and echoed the recorded `set_msg_config` calls. An
#: arm that expects a refusal fails if the sentinel appears, and the
#: positive arms assert the generic and promotion lines it prints.
STUBS = """
set ::ooc_msgcfg {}
proc read_verilog args {}
proc synth_design args {
  for {set i 0} {$i < [llength $args]} {incr i} {
    if {[lindex $args $i] eq "-generic"} {
      set g [lindex $args [expr {$i + 1}]]
      if {[regexp {^(PP_[A-Z_]+_HEX_P)="(.*)"$} $g -> name val]} {
        if {[file pathtype $val] ne "absolute"} {
          error "SYNTH-GENERIC-NOT-ABSOLUTE: $g"
        }
        if {![file exists $val] || [file size $val] == 0} {
          error "SYNTH-GENERIC-IMAGE-MISSING: $g"
        }
        puts "OOC-GENERIC-OK: $name"
      }
    }
  }
  puts "OOC-MSGCFG: $::ooc_msgcfg"
  puts "%s"
}
proc create_clock args {}
proc get_ports args { return {} }
proc report_utilization args {}
proc report_timing_summary args {}
proc set_msg_config args { lappend ::ooc_msgcfg $args }
source {%s}
"""

#: python3 dispatcher for the milan_datapath arms: sabotage the one script
#: the arm plants a failure in, hand everything else (dp_srcs.py, the other
#: generator) to the real interpreter, so the generation path the positive
#: arm proves is the shipping one. `$out` holds the -o target.
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
ARMS = 18


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


def _mutant(pattern, replacement, label):
    """A copy of the real datapath recipe, in this directory (it derives the
    repo root from its own location), with one substitution applied. The
    pattern MUST hit: a mutation that no longer matches is testing nothing."""
    with open(DP_TCL) as fh:
        text = fh.read()
    mutated, n = re.subn(pattern, replacement, text)
    if n != 1:
        raise AssertionError("mutation %r: pattern hit %d times, expected 1 "
                             "(the recipe moved?)" % (label, n))
    fd, path = tempfile.mkstemp(suffix=".tcl", prefix=".ooc-mut-", dir=HERE)
    with os.fdopen(fd, "w") as fh:
        fh.write(mutated)
    return path


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
                miss = check(d, log)
                if miss:
                    problems.append("SELF-TEST FAILED [%s]: %s\n%s"
                                    % (name, miss, log.strip()))

    def _write(workdir, name, content):
        with open(os.path.join(workdir, name), "w") as fh:
            fh.write(content)

    def images(*names):
        def setup(d):
            for n in names:
                _write(d, n, "" if n.endswith("!") else "00\n")
            for n in names:
                if n.endswith("!"):
                    os.rename(os.path.join(d, n), os.path.join(d, n[:-1]))
        return setup

    # ---- pp_shadow_ooc.tcl: requires, does not generate ------------------

    # Arm 1. Neither image. The first one named is the one reported.
    arm("no-images", "ltn_rom.hex is missing or empty", False)

    # Arm 2. The image the finding document used to name on its own.
    arm("ucode-missing", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex"))

    # Arm 3. Present and zero bytes: `file exists` alone would pass this, and
    # Vivado reads an empty image exactly as it reads an absent one.
    arm("ucode-empty", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex", "ucode.hex!"))

    # Arm 4. ANTI-VACUITY. Both images present and non-empty must reach
    # synthesis. Without this arm a guard that always fires passes arms 1-3.
    arm("both-images-present", None, True, images("ltn_rom.hex", "ucode.hex"))

    # Arm 5. The .tcl must take the generator's exit status (dp_srcs.py here:
    # the read-set generator is the first exec this recipe runs).
    stub = tempfile.mkdtemp(prefix="dp-srcs-fails-")
    with open(os.path.join(stub, "python3"), "w") as fh:
        fh.write("#!/bin/sh\necho 'dp_srcs: planted generator failure' >&2\n"
                 "exit 2\n")
    os.chmod(os.path.join(stub, "python3"), 0o755)
    arm("generator-failure-propagates", "planted generator failure", False,
        images("ltn_rom.hex", "ucode.hex"),
        env={"PATH": stub + os.pathsep + os.environ.get("PATH", "")})
    shutil.rmtree(stub, ignore_errors=True)

    # ---- milan_datapath_ooc.tcl: generates, validates, publishes ---------

    def dp_env(target, action):
        stub = _py_sabotage(target, action)
        return stub, {"PATH": stub + os.pathsep + os.environ.get("PATH", "")}

    def dp_arm(name, want, target, action, expect_rc0=False, setup=None,
               check=None):
        stub, env = dp_env(target, action)
        try:
            arm(name, want, expect_rc0, setup=setup, env=env, tcl=DP_TCL,
                check=check)
        finally:
            shutil.rmtree(stub, ignore_errors=True)

    # Arm 6. A dead microcode generator aborts the script: its exit status
    # is taken by `exec`, never discarded.
    dp_arm("dp-ucode-generator-fail", "planted ucode generator failure",
           "gen_ucode.py",
           "echo 'planted ucode generator failure' >&2\n  exit 3")

    # Arm 7. A generator that exits 0 leaving an empty image: zero words is
    # not the ROM's geometry.
    dp_arm("dp-ucode-empty", "0 words, expected exactly 2048",
           "gen_ucode.py", ": > \"$out\"\n  exit 0")

    # Arm 8. ONE syntactically valid word ([R-parallel]'s exact plant): it
    # is non-empty, and $readmemh would load it and leave 2,047 words X.
    dp_arm("dp-ucode-one-word", "1 words, expected exactly 2048",
           "gen_ucode.py", "printf '000000000000\\n' > \"$out\"\n  exit 0")

    # Arm 9. Truncated: right words, too few of them.
    dp_arm("dp-ucode-truncated", "1000 words, expected exactly 2048",
           "gen_ucode.py",
           "%s %s -o \"$out.full\" > /dev/null && "
           "head -1000 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
           "  exit 0" % (REAL_PYTHON, GEN_UCODE))

    # Arm 10. Malformed word: full depth, one word the wrong shape. `Z` is
    # $readmemh-legal and loads as Z, which is exactly why it is refused.
    dp_arm("dp-ucode-malformed", "not exactly 12 hex digits",
           "gen_ucode.py",
           "%s %s -o \"$out\" > /dev/null && "
           "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
           % (REAL_PYTHON, GEN_UCODE))

    # Arm 11. STALE image + no-op generator ([R-parallel]'s exact plant):
    # the pre-created file must not survive to be measured; the no-op leaves
    # no temp file, which is the refusal, and the stale image is deleted.
    def stale_gone(d, log):
        if os.path.exists(os.path.join(d, "ucode.hex")):
            return "the stale ucode.hex survived the refusal"
        return None
    dp_arm("dp-ucode-stale-noop", "leaving no file", "gen_ucode.py",
           "exit 0", setup=lambda d: _write(d, "ucode.hex", "STALE\n"),
           check=stale_gone)

    # Arm 12. The transition ROM gets the identical geometry contract.
    dp_arm("dp-ltn-one-word", "1 words, expected exactly 128",
           "gen_ltn_rom.py", "printf '00000000\\n' > \"$out\"\n  exit 0")

    # Arm 13. ...and the identical width contract.
    dp_arm("dp-ltn-malformed", "not exactly 8 hex digits", "gen_ltn_rom.py",
           "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
           "  exit 0" % (REAL_PYTHON, GEN_LTN))

    # Arm 14. ...and its generator's exit status.
    dp_arm("dp-ltn-generator-fail", "planted ltn generator failure",
           "gen_ltn_rom.py",
           "echo 'planted ltn generator failure' >&2\n  exit 3")

    # Arm 15. ANTI-VACUITY. From an EMPTY directory the real generators run,
    # both images land in the run directory validated and non-empty, the run
    # reaches synth_design with BOTH absolute ROM generics validated by the
    # stub, and the exact Synth 8-4445 promotion is in force.
    def dp_positive(d, log):
        for img in ("ltn_rom.hex", "ucode.hex"):
            p = os.path.join(d, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run directory" % img
        for name in ("PP_TROM_HEX_P", "PP_UCODE_HEX_P"):
            if ("OOC-GENERIC-OK: %s" % name) not in log:
                return "synth_design did not receive a valid %s generic" % name
        if PROMOTION not in log:
            return "the Synth 8-4445 promotion is not in force at synth_design"
        return None
    arm("dp-empty-dir-generates-and-passes", None, True, tcl=DP_TCL,
        check=dp_positive)

    # Arm 16. MUTATION: the promotion deleted from a copy of the recipe. The
    # detector must distinguish, or arm 15's promotion assertion is vacuous.
    mut = _mutant(r"set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n",
                  "", "promotion-deleted")
    try:
        def promo_gone(d, log):
            if PROMOTION in log:
                return "the mutant still shows the promotion: the detector " \
                       "cannot distinguish"
            return None
        arm("dp-mut-promotion-deleted", None, True, tcl=mut, check=promo_gone)
    finally:
        os.unlink(mut)

    # Arm 17. MUTATION: the ucode generic deleted from synth_design's call.
    mut = _mutant(r" -generic \$UCODE_GENERIC", "", "ucode-generic-deleted")
    try:
        def generic_gone(d, log):
            if "OOC-GENERIC-OK: PP_UCODE_HEX_P" in log:
                return "the mutant still shows the ucode generic: the " \
                       "detector cannot distinguish"
            return None
        arm("dp-mut-ucode-generic-deleted", None, True, tcl=mut,
            check=generic_gone)
    finally:
        os.unlink(mut)

    # Arm 18. MUTATION: the ucode generic redirected at a missing image
    # ([R-parallel]'s exact plant). The synth_design stub itself refuses.
    mut = _mutant(r'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"\[file normalize '
                  r'ucode\.hex\]\\""',
                  'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"[file normalize '
                  'missing-ucode.hex]\\""', "ucode-generic-redirected")
    try:
        arm("dp-mut-ucode-generic-redirected", "SYNTH-GENERIC-IMAGE-MISSING",
            False, tcl=mut)
    finally:
        os.unlink(mut)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), this "
                        "file declares %d." % (ran, ARMS))
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
