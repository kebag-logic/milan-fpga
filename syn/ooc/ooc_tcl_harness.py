#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The models and the machinery one arm of the OOC .tcl self-test runs on.

Everything here is the fixture, never a test: the Vivado commands stubbed for
`tclsh` (the observation point for every synthesis safeguard), the record
`dp_srcs.py` derives, the mutated copies of the recipes, the shared checks a
positive arm reads its log with, and the `Arm` record plus the `Suite` that
runs one and records what it failed to prove. The arms themselves are
`ooc_tcl_arms.py`; what the suite is FOR, and its exit status, are
`ooc_tcl_selftest.py`, whose docstring says what the set of these stubs
proves.
"""
import dataclasses
import functools
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
set ::ooc_sv_files {}
set ::ooc_synthed 0
set ::ooc_sev [dict create]
proc read_verilog args {
  set sv 0
  foreach a $args {
    if {$a eq "-sv"} { set sv 1; continue }
    foreach f $a {
      lappend ::ooc_read $f
      if {$sv} { lappend ::ooc_sv_files $f }
    }
  }
}
proc set_msg_config args {
  set id ""; set sev ""
  for {set i 0} {$i < [llength $args]} {incr i} {
    set opt [lindex $args $i]
    switch -- $opt {
      -id           { set id  [lindex $args [incr i]] }
      -new_severity { set sev [lindex $args [incr i]] }
      -suppress     { set sev SUPPRESSED }
      default {
        # Fail CLOSED. A rule spelled with an option this model does not
        # know may move the effective severity in a direction the model
        # cannot see, and "silently ignored" is the exact defect the
        # effective-severity model exists to catch.
        error "OOC-MSG-CONFIG-UNMODELLED: $opt"
      }
    }
  }
  if {$id ne "" && $sev ne ""} { dict set ::ooc_sev $id $sev }
}
proc synth_design args {
  # Everything the recipe hands the tool is recorded, not only -generic.
  # -top / -part / -mode / -include_dirs / -verilog_define decide WHICH
  # design is measured, and an unobserved include path is precisely how the
  # recipe came to elaborate a different entity shape than the portability
  # gate while all 40 arms stayed green.
  #
  # The canonical image map below is TEST knowledge and duplicates the
  # pinned packages' geometry: bump it when ucpu_pkg.sv / pp_acmp_pkg.sv /
  # gptp_ucpu_pkg.sv move, or a COHERENT ROM change fails here and the
  # message will blame the recipe.
  set ::ooc_top {}; set ::ooc_part {}; set ::ooc_mode {}
  set ::ooc_incs {}; set ::ooc_defs {}; set ::ooc_generics {}
  set expect [dict create PP_TROM_HEX_P {ltn_rom.hex 8 128} \\
                          PP_UCODE_HEX_P {ucode.hex 12 2048} \\
                          GPTP_UCODE_HEX_P {gptp_ucode.hex 12 1024}]
  for {set i 0} {$i < [llength $args]} {incr i} {
    set opt [lindex $args $i]
    switch -- $opt {
      -top            { set ::ooc_top  [lindex $args [incr i]]; continue }
      -part           { set ::ooc_part [lindex $args [incr i]]; continue }
      -mode           { set ::ooc_mode [lindex $args [incr i]]; continue }
      -include_dirs   { set ::ooc_incs [lindex $args [incr i]]; continue }
      -verilog_define { lappend ::ooc_defs [lindex $args [incr i]]; continue }
      -generic        { }
      default {
        error "SYNTH-OPTION-UNMODELLED: $opt -- an option that can move the\
 number (-max_bram, -no_lc, -flatten_hierarchy) must be modelled here\
 before it is passed, not silently accepted."
      }
    }
    set g [lindex $args [incr i]]
    # Fail CLOSED, like the option parser above. Discarding a generic this
    # model does not know is how -generic GPTP_PLANE_EN_P=0 -- which removes
    # a whole plane from the synthesized design -- rode through a green
    # suite. A generic is either modelled here or refused.
    if {![regexp {^([A-Za-z_][A-Za-z0-9_]*)=(.*)$} $g -> gname gval]} {
      error "SYNTH-GENERIC-MALFORMED: $g"
    }
    # Two modelled families: the ROM images validated by geometry below,
    # and pp_shadow_ooc.tcl's shape generics, which carry no image and are
    # recorded only. Anything else is refused.
    set shaped {N_STREAM_IN_P N_STREAM_OUT_P}
    if {![dict exists $expect $gname]
        && [lsearch -exact $shaped $gname] < 0} {
      error "SYNTH-GENERIC-UNMODELLED: $gname -- a generic that can change\
 which design is synthesized must be modelled here before it is passed."
    }
    if {[lsearch -exact $::ooc_generics $gname] >= 0} {
      error "SYNTH-GENERIC-DUPLICATE: $gname"
    }
    lappend ::ooc_generics $gname
    if {![dict exists $expect $gname]} continue
    if {![regexp {^((?:PP|GPTP)_[A-Z_]+_HEX_P)="(.*)"$} $g -> name val]} {
      error "SYNTH-GENERIC-NOT-QUOTED: $g (UG901: a string generic's value\
 must reach -generic wrapped in literal double quotes)"
    }
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
      # $readmemh accepts both comment forms, and so does the recipe's
      # rom_check; a stub stricter than the tool it models refuses images
      # Vivado would read.
      regsub -all {/\\*.*?\\*/} $text "" text
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
  set ::ooc_synthed 1
  puts "OOC-TOP: $::ooc_top"
  puts "OOC-PART: $::ooc_part"
  puts "OOC-MODE: $::ooc_mode"
  set fs [open ooc-sv-files.txt w]
  foreach f $::ooc_sv_files { puts $fs $f }
  close $fs
  set fi [open ooc-incdirs.txt w]
  foreach d $::ooc_incs { puts $fi $d }
  close $fi
  set fd2 [open ooc-defines.txt w]
  foreach d $::ooc_defs { puts $fd2 $d }
  close $fd2
  set fh [open %s w]
  foreach f $::ooc_read { puts $fh $f }
  close $fh
  puts "%s"
}
proc create_clock args {}
#: The top's port names are TEST knowledge, like the geometry map above:
#: bump this when milan_datapath.sv renames a port. Empty until
#: synth_design has run -- Vivado has no design to query before that, so a
#: constraint hoisted above synthesis must look as broken here as it is.
set ::ooc_ports {axis_clk}
proc get_ports args {
  if {!$::ooc_synthed} { return {} }
  set want [lindex $args end]
  if {[lsearch -exact $::ooc_ports $want] >= 0} { return $want }
  return {}
}
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


class SelfTestPrereq(Exception):
    """A prerequisite of the suite itself is unavailable. Distinct from an arm
    failure: it means nothing was proven, so it must NAME itself rather than
    unwind as a traceback that also discards the arms already run."""


@functools.lru_cache(maxsize=None)
def derived_sources():
    """dp_srcs.py's own answer, cached: the record the recipe must consume."""
    return sorted(derived_record()["src"])


@functools.lru_cache(maxsize=None)
def derived_record():
    """The WHOLE record dp_srcs.py hands the recipe -- top/define/incdir/src.
    The recipe must consume every half of it: the sources decide what is read,
    the include path and defines decide which entity shape is elaborated.

    Asked ONCE per run, and memoised by the decorator: a self-test that
    rebinds its own module globals to cache leaves the module mutated, and a
    refusal must stay askable, so a raised SelfTestPrereq is not cached."""
    out = subprocess.run(
        [REAL_PYTHON, os.path.join(HERE, "dp_srcs.py"), "--record"],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise SelfTestPrereq(
            "dp_srcs.py --record exited %d. Every datapath arm derives "
            "the record it holds the recipe to, so no arm can run: check "
            "the submodules (protocol-processor, gptp-processor) and "
            "sv2v.\n%s" % (out.returncode, (out.stderr or "").strip()))
    rec = {"top": [], "define": [], "incdir": [], "src": []}
    for line in out.stdout.splitlines():
        if not line.strip():
            continue
        key, _, val = line.partition("=")
        if key not in rec:
            raise SelfTestPrereq(
                "dp_srcs.py --record emitted an unrecognized key %r; the "
                "suite and the recipe would consume different records."
                % key)
        rec[key].append(val)
    return rec


def _read_text(path):
    """The whole text of one file, the handle closed before it returns."""
    with open(path) as fh:
        return fh.read()


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
        raise SelfTestPrereq(
            "mutation %r: pattern hit %d times, expected 1. The recipe moved "
            "under this arm, so the arm is testing nothing -- retarget it. "
            "(A mutation that no longer matches must never read as a pass.)"
            % (label, n))
    fd, path = tempfile.mkstemp(suffix=".tcl", prefix=".ooc-mut-", dir=HERE)
    with os.fdopen(fd, "w") as fh:
        fh.write(mutated)
    return path


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


def unpublished(img):
    """A refused image must not be left in the run directory: the recipe
    renames into place only AFTER rom_check passes."""
    def check(d, log):
        if os.path.exists(os.path.join(d, img)):
            return ("%s was published to the run directory despite "
                    "failing validation -- the publish-after-validate "
                    "ordering is gone" % img)
        return None
    return check


def dp_env(target, action):
    stub = _py_sabotage(target, action)
    return stub, {"PATH": stub + os.pathsep + os.environ.get("PATH", "")}


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


@dataclasses.dataclass
class Arm:
    """One planted run of an OOC recipe: what is planted, and what must come
    back.

    A record and not eight parameters, so that a call site names every plant
    it makes and inherits the default for every plant it does not. `want` is
    the text a refusal must NAME; `post_synth` says the refusal under test is
    AFTER synth_design (the clock constraint), so the sentinel is legitimately
    present -- every other refusal must still beat synthesis to the run.
    """

    name: str
    want: object
    expect_rc0: bool = False
    setup: object = None
    env: object = None
    tcl: str = TCL
    check: object = None
    post_synth: bool = False


class Suite:
    """The arms' shared verdict: what failed, and how many arms ran.

    `problems` is the caller's list, mutated in place, so a prerequisite that
    fails part-way through still reports the arms that ran before it.
    """

    def __init__(self, problems):
        self.problems = problems
        self.ran = 0

    def run(self, a):
        """Run one arm, appending to `problems` whatever it failed to prove."""
        self.ran += 1
        problems = self.problems
        with tempfile.TemporaryDirectory() as d:
            if a.setup:
                a.setup(d)
            rc, log = _run(d, a.env, a.tcl)
            reached = SENTINEL in log
            if a.expect_rc0:
                if rc != 0 or not reached:
                    problems.append("SELF-TEST FAILED [%s]: a well-formed run "
                                    "must reach synthesis, got rc=%d, "
                                    "sentinel=%s\n%s"
                                    % (a.name, rc, reached, log.strip()))
                    return
            elif rc == 0 or reached != a.post_synth or a.want not in log:
                problems.append("SELF-TEST FAILED [%s]: expected a refusal "
                                "naming %r %s synthesis, got rc=%d, "
                                "sentinel=%s\n%s"
                                % (a.name, a.want,
                                   "after" if a.post_synth else "before",
                                   rc, reached, log.strip()))
                return
            if a.check:
                miss = a.check(d, log)
                if miss:
                    problems.append("SELF-TEST FAILED [%s]: %s\n%s"
                                    % (a.name, miss, log.strip()))

    def dp_arm(self, a, target, action):
        """One datapath arm, run against a python3 whose `target` generator is
        sabotaged with `action` for the length of the run."""
        stub, env = dp_env(target, action)
        try:
            self.run(dataclasses.replace(a, env=env, tcl=DP_TCL))
        finally:
            shutil.rmtree(stub, ignore_errors=True)


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
    got = [l.strip() for l in _read_text(rl).splitlines() if l.strip()]
    want = derived_record()["src"]
    if got != want:
        if sorted(got) == sorted(want):
            first = next(i for i, (a, b) in enumerate(zip(got, want))
                         if a != b)
            return ("the read set is the record's files in a DIFFERENT "
                    "ORDER -- first divergence at index %d: read %s, "
                    "record %s. Vivado compiles Non-Project sources in "
                    "read_* order (UG895), so compilation-unit scope and "
                    "macro visibility move with it."
                    % (first, os.path.basename(got[first]),
                       os.path.basename(want[first])))
        return ("the read set (%d files) is not the dp_srcs.py record "
                "(%d files): the derived-source connection is broken"
                % (len(got), len(want)))
    # Which design gets measured is decided by the REST of the call, and
    # none of it was observed until this review: -include_dirs was a hand
    # list whose ORDER selected a different entity shape than the gate.
    rec = derived_record()
    svf = os.path.join(d, "ooc-sv-files.txt")
    got_sv = (set(l.strip() for l in _read_text(svf).splitlines()
                  if l.strip())
              if os.path.isfile(svf) else set())
    want_sv = set(f for f in derived_record()["src"] if f.endswith(".sv"))
    if got_sv != want_sv:
        return ("the files read as SystemVerilog are not the .sv half of "
                "the record (%d read with -sv, %d .sv in the record): the "
                "remainder would go to the Verilog-2001 parser"
                % (len(got_sv), len(want_sv)))
    if ("OOC-TOP: %s" % rec["top"][0]) not in log:
        return ("synth_design was not given the record's own top (%s): "
                "the module this recipe reads and the module it "
                "synthesizes must not be two different strings (#235)"
                % rec["top"][0])
    if "OOC-MODE: out_of_context" not in log:
        return "synth_design was not run -mode out_of_context"
    if "OOC-PART: xc7a100tfgg484-2" not in log:
        return "synth_design was not given the ship part"
    inc = os.path.join(d, "ooc-incdirs.txt")
    if not os.path.isfile(inc):
        return "synth_design received no include path at all"
    got_inc = [l for l in _read_text(inc).splitlines() if l.strip()]
    if got_inc != rec["incdir"]:
        return ("the include path is not the record's, IN ORDER.\n"
                "  record: %s\n  passed: %s\n"
                "Order decides which gen/adp_shape_defaults.svh wins: "
                "hdl/common/csr/gen/ and configs/generated/*/gen/ both "
                "carry one, so a reordered path silently elaborates a "
                "different entity shape than the portability gate proves."
                % (rec["incdir"], got_inc))
    dfn = os.path.join(d, "ooc-defines.txt")
    got_def = ([l for l in _read_text(dfn).splitlines() if l.strip()]
               if os.path.isfile(dfn) else [])
    if got_def != rec["define"]:
        return ("the defines are not the record's (record %s, passed %s): "
                "KL_gptp_engine.sv gates simulation-only $error blocks on "
                "`ifndef SYNTHESIS, so the define is not cosmetic"
                % (rec["define"], got_def))
    return None


def fires(needle, what):
    """The mutant must be caught by the assertion this arm NAMES. Any
    detector firing would satisfy a bare `if dp_positive(...)`, so the
    arm would survive the deletion of the very check it exists to pin."""
    def check(d, log):
        got = dp_positive(d, log) or ""
        if needle in got:
            return None
        return ("the %s mutant was not caught by its own detector "
                "(got: %s)" % (what, got or "no detector fired at all"))
    return check
