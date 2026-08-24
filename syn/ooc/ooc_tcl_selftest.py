#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive the two OOC .tcl recipes' pre-synthesis refusals, automatically.

pp_shadow_ooc.tcl refuses to synthesize when a `$readmemh` image is missing or
empty, and it takes the source generator's exit status. Both refusals had
manual evidence and no test ([R0] on PR #240): deleting either one left every
hosted check green, which is the definition of a defense that rots.

milan_datapath_ooc.tcl (#246) derives its read set from dp_srcs.py, finds its
geometry packages IN that record, reads each geometry number from the ONE
live declaration (comments stripped, name boundary-anchored), GENERATES all
three images into fresh temp targets, validates their exact geometry, and publishes
by rename only after validation. Stale+no-op, one-token, truncated and
malformed images, commented-out or duplicated declarations, and a record
without the packages are all refusals before anything is read ([R-parallel]
and [R0] on PR #264 closed those survivors, round by round).

WHAT IT RUNS IS THE REAL .TCL, not a copy of its logic. `tclsh` sources the
tracked file with the Vivado-only commands stubbed. `read_verilog` RETURNS
(it does not exit) and RECORDS every file it is handed; the sentinel prints
at `synth_design`, whose stub is the observation point for the synthesis
safeguards:

  - every `-generic *_HEX_P=...` it receives must be quoted, absolute, an
    existing non-empty file, carry the CANONICAL basename for its parameter
    (PP_UCODE_HEX_P -> ucode.hex, PP_TROM_HEX_P -> ltn_rom.hex,
    GPTP_UCODE_HEX_P -> gptp_ucode.hex), and hold
    that ROM's geometry, or the stub errors -- an existing-but-wrong file
    opens cleanly, so Synth 8-4445 never protects that case;
  - `set_msg_config` is MODELLED, not transcribed: the stub keeps the final
    severity per message id, and the positive arm requires the EFFECTIVE
    severity of Synth 8-4445 at synth_design to be ERROR -- a downgrade
    applied after the promotion is the same defect as never promoting;
  - the recorded read set is written out and the positive arm requires it to
    EQUAL what dp_srcs.py derives, so a hand-written list cannot stand in
    for the record while the suite stays green.

Mutation copies of the recipe prove every one of those detectors can fail.

`tclsh` is the interpreter Vivado embeds, so the guard is exercised by the
language it is written in rather than reimplemented in Python. What tclsh
cannot prove is Vivado's own semantics; the real-Vivado negative control for
the promotion (a missing image at synthesis with the preflight removed must
abort, not warn) is recorded on the PR that lands a change.

    python3 syn/ooc/ooc_tcl_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/dp_srcs.py --selftest.
Needs the protocol-processor and verilog-axis submodules and sv2v, because
the datapath recipe derives its read set before anything else, so every arm
pays one dp_srcs.py run (~5 minutes total).
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
EFFECTIVE_OK = "OOC-EFFECTIVE-SEV: {Synth 8-4445} = ERROR"
READ_LIST = "ooc-read-list.txt"
REAL_PYTHON = shutil.which("python3") or sys.executable
GEN_UCODE = os.path.join(REPO, "protocol-processor", "hdl", "aecp", "ucode",
                         "gen_ucode.py")
GEN_LTN = os.path.join(REPO, "protocol-processor", "hdl", "acmp", "rom",
                       "gen_ltn_rom.py")
GEN_GPTP = os.path.join(REPO, "gptp-processor", "hdl", "ucode",
                        "gen_gptp_ucode.py")

#: The Vivado commands the .tcl recipes call, stubbed as the docstring
#: describes. The canonical-image map in synth_design is TEST knowledge: the
#: recipe under test must arrive at the same binding on its own.
STUBS = """
set ::ooc_read {}
set ::ooc_sev [dict create]
proc read_verilog args {
  foreach a $args {
    if {$a eq "-sv"} continue
    foreach f $a { lappend ::ooc_read $f }
  }
}
proc set_msg_config args {
  set id ""; set sev ""
  for {set i 0} {$i < [llength $args]} {incr i} {
    switch -- [lindex $args $i] {
      -id           { set id  [lindex $args [incr i]] }
      -new_severity { set sev [lindex $args [incr i]] }
    }
  }
  if {$id ne "" && $sev ne ""} { dict set ::ooc_sev $id $sev }
}
proc synth_design args {
  set expect [dict create PP_TROM_HEX_P {ltn_rom.hex 8 128} \\
                          PP_UCODE_HEX_P {ucode.hex 12 2048} \\
                          GPTP_UCODE_HEX_P {gptp_ucode.hex 12 1024}]
  for {set i 0} {$i < [llength $args]} {incr i} {
    if {[lindex $args $i] ne "-generic"} continue
    set g [lindex $args [expr {$i + 1}]]
    if {![regexp {^((?:PP|GPTP)_[A-Z_]+_HEX_P)="(.*)"$} $g -> name val]} continue
    if {[file pathtype $val] ne "absolute"} {
      error "SYNTH-GENERIC-NOT-ABSOLUTE: $g"
    }
    if {![file exists $val] || [file size $val] == 0} {
      error "SYNTH-GENERIC-IMAGE-MISSING: $g"
    }
    if {[dict exists $expect $name]} {
      lassign [dict get $expect $name] tail digits words
      if {[file tail $val] ne $tail} {
        error "SYNTH-GENERIC-WRONG-IMAGE: $name -> [file tail $val] (canonical $tail)"
      }
      set fh [open $val r]; set text [read $fh]; close $fh
      set n 0
      foreach line [split $text "\\n"] {
        regsub {//.*$} $line "" line
        foreach tok [split $line] {
          if {$tok eq ""} continue
          incr n
          if {![regexp {^[0-9a-fA-F]+$} $tok] || [string length $tok] != $digits} {
            error "SYNTH-GENERIC-BAD-GEOMETRY: $name word $n at [file tail $val]"
          }
        }
      }
      if {$n != $words} {
        error "SYNTH-GENERIC-BAD-GEOMETRY: $name $n words at [file tail $val], want $words"
      }
    }
    puts "OOC-GENERIC-OK: $name"
  }
  foreach id [dict keys $::ooc_sev] {
    puts "OOC-EFFECTIVE-SEV: [list $id] = [dict get $::ooc_sev $id]"
  }
  set fh [open %s w]
  foreach f $::ooc_read { puts $fh $f }
  close $fh
  puts "%s"
}
proc create_clock args {}
proc get_ports args { return {} }
proc report_utilization args {}
proc report_timing_summary args {}
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
ARMS = 40

_DERIVED = None


def derived_sources():
    """dp_srcs.py's own answer, cached: the record the recipe must consume."""
    global _DERIVED
    if _DERIVED is None:
        out = subprocess.run(
            [REAL_PYTHON, os.path.join(HERE, "dp_srcs.py")],
            capture_output=True, text=True, check=True)
        _DERIVED = sorted(l for l in out.stdout.splitlines() if l.strip())
    return _DERIVED


def _run(workdir, env=None, tcl=TCL):
    e = dict(os.environ)
    e.update(env or {})
    # A driver FILE, not tclsh's stdin: reading a script from stdin makes an
    # uncaught error a printed message at exit 0, which would make every arm
    # below agree with a guard that does not exist.
    fd, driver = tempfile.mkstemp(suffix=".tcl", prefix="ooc-driver-")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(STUBS % (READ_LIST, SENTINEL, tcl))
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

    # ---- milan_datapath_ooc.tcl: derives, generates, validates -----------

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

    # Arm 15. ANTI-VACUITY, and the observation point for every synthesis
    # safeguard: from an EMPTY directory the real generators run, both
    # validated images land in the run directory, synth_design receives BOTH
    # canonical absolute ROM generics (the stub has rechecked basename and
    # geometry), the EFFECTIVE severity of Synth 8-4445 there is ERROR, and
    # the read set the stubs recorded EQUALS what dp_srcs.py derives.
    def dp_positive(d, log):
        for img in ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex"):
            p = os.path.join(d, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run directory" % img
        for name in ("PP_TROM_HEX_P", "PP_UCODE_HEX_P", "GPTP_UCODE_HEX_P"):
            if ("OOC-GENERIC-OK: %s" % name) not in log:
                return "synth_design did not receive a valid %s generic" % name
        if EFFECTIVE_OK not in log:
            return ("the EFFECTIVE severity of Synth 8-4445 at synth_design "
                    "is not ERROR")
        rl = os.path.join(d, READ_LIST)
        if not os.path.isfile(rl):
            return "the stubs recorded no read set"
        got = sorted(l.strip() for l in open(rl) if l.strip())
        if got != derived_sources():
            return ("the read set (%d files) is not the dp_srcs.py record "
                    "(%d files): the derived-source connection is broken"
                    % (len(got), len(derived_sources())))
        return None
    arm("dp-empty-dir-generates-and-passes", None, True, tcl=DP_TCL,
        check=dp_positive)

    # Arm 16. MUTATION: the promotion deleted. The detector must distinguish,
    # or arm 15's effective-severity assertion is vacuous.
    mut = _mutant(r"set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n",
                  "", "promotion-deleted")
    try:
        arm("dp-mut-promotion-deleted", None, True, tcl=mut,
            check=lambda d, log: None if EFFECTIVE_OK not in log
            else "the mutant still shows an ERROR effective severity")
    finally:
        os.unlink(mut)

    # Arm 17. MUTATION: the promotion followed by a DOWNGRADE of the same id
    # ([R0]'s exact plant). Historical text still contains the ERROR
    # spelling; only the effective-severity model can tell them apart.
    mut = _mutant(r"(set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n)",
                  "\\1set_msg_config -id {Synth 8-4445} -new_severity "
                  "{CRITICAL WARNING}\n", "promotion-downgraded-after")
    try:
        def downgraded(d, log):
            if EFFECTIVE_OK in log:
                return "the downgrade-after-promotion mutant still reads as " \
                       "an ERROR effective severity"
            if "OOC-EFFECTIVE-SEV: {Synth 8-4445} = CRITICAL WARNING" not in log:
                return "the effective-severity model did not record the " \
                       "downgrade"
            return None
        arm("dp-mut-promotion-downgraded-after", None, True, tcl=mut,
            check=downgraded)
    finally:
        os.unlink(mut)

    # Arm 18. MUTATION: the ucode generic deleted from synth_design's call.
    mut = _mutant(r" -generic \$UCODE_GENERIC", "", "ucode-generic-deleted")
    try:
        arm("dp-mut-ucode-generic-deleted", None, True, tcl=mut,
            check=lambda d, log: None
            if "OOC-GENERIC-OK: PP_UCODE_HEX_P" not in log
            else "the mutant still shows the ucode generic")
    finally:
        os.unlink(mut)

    # Arm 19. MUTATION: the ucode generic redirected at a MISSING image.
    mut = _mutant(r'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"\[file normalize '
                  r'ucode\.hex\]\\""',
                  'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"[file normalize '
                  'missing-ucode.hex]\\""', "ucode-generic-redirected")
    try:
        arm("dp-mut-ucode-generic-redirected", "SYNTH-GENERIC-IMAGE-MISSING",
            False, tcl=mut)
    finally:
        os.unlink(mut)

    # Arm 20. MUTATION: the ucode generic CROSS-WIRED at the OTHER image
    # ([R0]'s exact plant). The file exists and opens, so Synth 8-4445 never
    # fires; only the canonical-basename binding refuses it.
    mut = _mutant(r'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"\[file normalize '
                  r'ucode\.hex\]\\""',
                  'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"[file normalize '
                  'ltn_rom.hex]\\""', "ucode-cross-wired")
    try:
        arm("dp-mut-ucode-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut)
    finally:
        os.unlink(mut)

    # Arm 21. MUTATION: the transition-ROM generic cross-wired the other way.
    mut = _mutant(r'set TROM_GENERIC  "PP_TROM_HEX_P=\\"\[file normalize '
                  r'ltn_rom\.hex\]\\""',
                  'set TROM_GENERIC  "PP_TROM_HEX_P=\\"[file normalize '
                  'ucode.hex]\\""', "trom-cross-wired")
    try:
        arm("dp-mut-trom-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut)
    finally:
        os.unlink(mut)

    # ---- the geometry parser ([R0] round three, finding 2) ---------------

    def pkg_mutant(pkg_text, label, which="ucpu"):
        """The recipe with one geometry package pointed at a synthetic file."""
        fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
        with os.fdopen(fd, "w") as fh:
            fh.write(pkg_text)
        if which == "ucpu":
            mut = _mutant(
                r"set UCPU_PKG \[one_source \$SRC_LINES ucpu_pkg\.sv\]",
                "set UCPU_PKG {%s}" % pkg, label)
        elif which == "acmp":
            mut = _mutant(
                r"set ACMP_PKG \[one_source \$SRC_LINES pp_acmp_pkg\.sv\]",
                "set ACMP_PKG {%s}" % pkg, label)
        else:
            mut = _mutant(
                r"set GPTP_PKG \[one_source \$SRC_LINES gptp_ucpu_pkg\.sv\]",
                "set GPTP_PKG {%s}" % pkg, label)
        return pkg, mut

    # Arm 22. [R0]'s exact plant: a stale value in a line comment above a
    # live declaration of 52. The LIVE value must win; with 52 the real
    # 48-bit generator output no longer fits, and THAT refusal is the proof
    # the comment did not win (had it won, the run would have passed).
    pkg, mut = pkg_mutant(
        "// stale example: UCODE_W_C = 48\n"
        "localparam int unsigned UCODE_W_C = 52;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-comment-shadow")
    try:
        arm("dp-pkg-comment-shadow-live-wins", "not exactly 13 hex digits",
            False, tcl=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 23. Block comments are stripped and prefixed identifiers do not
    # match: a /* UCODE_W_C = 40; */ and an XUCODE_W_C = 99 beside the live
    # 48/11 must leave the run WELL-FORMED (the real image fits 48).
    pkg, mut = pkg_mutant(
        "/* stale block:\n   localparam int unsigned UCODE_W_C = 40;\n*/\n"
        "localparam int unsigned XUCODE_W_C = 99;\n"
        "localparam int unsigned UCODE_W_C  = 48;\n"
        "localparam int unsigned UPC_W_C    = 11;\n", "pkg-block-and-prefix")
    try:
        arm("dp-pkg-block-comment-and-prefix", None, True, tcl=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 24. TWO live declarations: a refusal, never a pick.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UCODE_W_C = 52;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-duplicate")
    try:
        arm("dp-pkg-duplicate", "expected exactly one live declaration",
            False, tcl=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 25. ZERO live declarations (only a commented one): same refusal.
    pkg, mut = pkg_mutant(
        "// localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-missing")
    try:
        arm("dp-pkg-missing", "expected exactly one live declaration", False,
            tcl=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arms 25a-25f. NON-NIBBLE widths refuse outright ([R-parallel] round
    # three): 50/4 truncates to 12 digits and the exact probe showed the
    # stale 2,048x48 image satisfying a declared width of 50. Widths 49-51
    # (microcode) and 33-35 (transition ROM) must each refuse BEFORE any
    # image can validate; the supported widths keep their behavior (48/32
    # pristine in arm 15, and 52 correctly demanding 13 digits in arm 22).
    for w in (49, 50, 51):
        pkg, mut = pkg_mutant(
            "localparam int unsigned UCODE_W_C = %d;\n"
            "localparam int unsigned UPC_W_C = 11;\n" % w,
            "pkg-width-%d" % w)
        try:
            arm("dp-pkg-width-%d-not-nibble" % w,
                "not a positive nibble-aligned", False, tcl=mut)
        finally:
            os.unlink(mut)
            os.unlink(pkg)
    for w in (33, 34, 35):
        pkg, mut = pkg_mutant(
            "localparam int unsigned TROM_W_C = %d;\n"
            "localparam int unsigned TROM_DEPTH_C = 128;\n" % w,
            "pkg-trom-width-%d" % w, which="acmp")
        try:
            arm("dp-pkg-trom-width-%d-not-nibble" % w,
                "not a positive nibble-aligned", False, tcl=mut)
        finally:
            os.unlink(mut)
            os.unlink(pkg)

    # ---- the derived-source connection ([R0] round three, finding 5) -----

    # Arm 26. MUTATION: dp_srcs.py's record replaced by [R0]'s exact plant, a
    # hand list of the two packages. Geometry still resolves and the run
    # still reaches synthesis, which is exactly why the read-set-equality
    # detector exists: it must distinguish, or arm 15 is vacuous. The plant's
    # paths are COMPOSED here, not spelled: the contiguous submodule-source
    # path exists only in the untracked mutant, which is the planted defect
    # under test -- a tracked spelling would rightly trip
    # scripts/pp_srcs.py --check, and that trip is itself part of what this
    # plant is shown to hit on the real tree (PR #264 evidence).
    pp_root = "$REPO/protocol-processor" + "/hdl"
    gp_root = "$REPO/gptp-processor" + "/hdl"
    mut = _mutant(
        r"set SRC_LINES \[split \[string trim \[exec python3 "
        r"\$REPO/syn/ooc/dp_srcs\.py\]\] \"\\n\"\]",
        "set SRC_LINES [list %s/aecp/ucpu_pkg.sv %s/acmp/pp_acmp_pkg.sv"
        " %s/ucpu/gptp_ucpu_pkg.sv]"
        % (pp_root, pp_root, gp_root),
        "srcs-hand-list")
    try:
        def hand_list_detected(d, log):
            rl = os.path.join(d, READ_LIST)
            if not os.path.isfile(rl):
                return "the stubs recorded no read set"
            got = sorted(l.strip() for l in open(rl) if l.strip())
            if got == derived_sources():
                return "the hand-list mutant read set equals the record: " \
                       "the detector cannot distinguish"
            return None
        arm("dp-mut-srcs-hand-list", None, True, tcl=mut,
            check=hand_list_detected)
    finally:
        os.unlink(mut)

    # Arm 27. MUTATION: the dp_srcs.py invocation DELETED. Nothing downstream
    # may quietly supply a list: the recipe must die on its first consumer.
    mut = _mutant(
        r"set SRC_LINES \[split \[string trim \[exec python3 "
        r"\$REPO/syn/ooc/dp_srcs\.py\]\] \"\\n\"\]\n",
        "", "srcs-deleted")
    try:
        arm("dp-mut-srcs-deleted", "SRC_LINES", False, tcl=mut)
    finally:
        os.unlink(mut)

    # ---- the integrated gPTP engine's image (#116: default-on fabric) ----

    # Arms 28-31. The third $readmemh image gets the identical contract:
    # generator exit status taken, zero/one-word/malformed images refused
    # against the geometry derived from gptp_ucpu_pkg.sv (1,024x48 at the
    # pin), before anything is read.
    dp_arm("dp-gptp-generator-fail", "planted gptp generator failure",
           "gen_gptp_ucode.py",
           "echo 'planted gptp generator failure' >&2\n  exit 3")
    dp_arm("dp-gptp-empty", "0 words, expected exactly 1024",
           "gen_gptp_ucode.py", ": > \"$out\"\n  exit 0")
    dp_arm("dp-gptp-one-word", "1 words, expected exactly 1024",
           "gen_gptp_ucode.py", "printf '000000000000\\n' > \"$out\"\n  exit 0")
    dp_arm("dp-gptp-malformed", "not exactly 12 hex digits",
           "gen_gptp_ucode.py",
           "%s %s -o \"$out\" > /dev/null && "
           "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
           % (REAL_PYTHON, GEN_GPTP))

    # Arm 32. MUTATION: the gptp generic deleted from synth_design's call.
    mut = _mutant(r" \\\n  -generic \$GUCODE_GENERIC", "",
                  "gptp-generic-deleted")
    try:
        arm("dp-mut-gptp-generic-deleted", None, True, tcl=mut,
            check=lambda d, log: None
            if "OOC-GENERIC-OK: GPTP_UCODE_HEX_P" not in log
            else "the mutant still shows the gptp generic")
    finally:
        os.unlink(mut)

    # Arm 33. MUTATION: the gptp generic cross-wired at the AECP image. It
    # exists and opens; only the canonical-basename binding refuses it.
    mut = _mutant(r'set GUCODE_GENERIC "GPTP_UCODE_HEX_P=\\"\[file normalize '
                  r'gptp_ucode\.hex\]\\""',
                  'set GUCODE_GENERIC "GPTP_UCODE_HEX_P=\\"[file normalize '
                  'ucode.hex]\\""', "gptp-cross-wired")
    try:
        arm("dp-mut-gptp-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut)
    finally:
        os.unlink(mut)

    # Arm 34. The gptp package width gets the same non-nibble refusal.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 50;\n"
        "localparam int unsigned UPC_W_C = 10;\n", "pkg-gptp-width-50",
        which="gptp")
    try:
        arm("dp-pkg-gptp-width-50-not-nibble",
            "not a positive nibble-aligned", False, tcl=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

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
