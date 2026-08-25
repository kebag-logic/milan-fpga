#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/yosys/ooc.sh's refusals, automatically, on planted failures.

That script's exit status is the gate (#245): a top that fails sv2v or yosys,
a ROM generator that fails or emits an empty, truncated, one-word or
malformed image, a report phase that cannot produce a real row (no stat
block, zero mapped cells, dead awk, missing JSON artifact), and a requested
top that matches nothing must each leave a non-zero exit. Before #245 the
failure branches printed and `continue`d, so the exit code was always 0; the
[R-parallel] round on PR #262 then showed two survivors: a one-word
`ucode.hex` is "non-empty" and priced a plausible wrong row, and the report
phase could be deleted wholesale while this file stayed green because its
yosys stub emitted nothing and the awk END clause manufactured a zero row.

WHAT IT RUNS IS THE REAL ooc.sh, not a copy of its logic. The plants ride
seams the script already has: it resolves `sv2v`, `yosys`, `awk` and
`python3` through PATH after prepending `$HOME/.local/bin`, so each arm runs
it with HOME pointing at a scratch directory whose `.local/bin` carries the
planted tool (the same directory is also put first on PATH directly, so the
arm does not depend on the prepend surviving). The ROM generators and
scripts/pp_srcs.py run for real through a dispatching `python3` stub, so the
generation path the positive arms prove is the shipping one.

THE YOSYS STUB IS A MODEL OF REAL YOSYS OUTPUT, deliberately: it emits a
top-named stat block when the -p command carries `synth_xilinx` (its internal
final statistics) and another when it carries an explicit ` stat;`, mapped
xc7 cells only when `synth_xilinx` ran, and the JSON artifact only when
`write_json` names it. A pristine run therefore shows TWO blocks, exactly as
a real log does, and the report-phase mutation arms below mutate a COPY of
ooc.sh itself (dropping synth_xilinx, both stat sources, or write_json from
its yosys command) and require the report phase to refuse. Real synthesis is
NOT run here; the real-toolchain run is recorded on the PR that lands a
change.

    python3 syn/yosys/ooc_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/ooc_tcl_selftest.py;
the invocation is pinned by scripts/ci_events.py (step removed, neutralised
or reordered = red docs-check). Needs the protocol-processor submodule
(pp_srcs.py, both ROM generators and the geometry packages read it); it does
not need yosys or sv2v.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OOC = os.path.join(HERE, "ooc.sh")
REAL_PYTHON = shutil.which("python3") or sys.executable
REAL_AWK = shutil.which("awk") or "awk"

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 18

SV2V_OK = "#!/bin/sh\nexit 0\n"
SV2V_FAIL = "#!/bin/sh\necho 'planted sv2v failure' >&2\nexit 1\n"
YOSYS_FAIL = ("#!/bin/sh\necho 'ERROR: planted yosys elaboration failure'\n"
              "exit 1\n")

#: The honest yosys model (see the module docstring). $2 is the -p command.
#: Without a -top (a mutant that dropped synth_xilinx), a bare `stat` still
#: prints per-module blocks named by the MODULE, exactly as real yosys does:
#: the fallback derives it from the read_verilog file's basename.
YOSYS_OK = r"""#!/bin/sh
p="$2"
top=$(printf '%s' "$p" | sed -n 's/.*-top \([A-Za-z0-9_]*\).*/\1/p')
[ -n "$top" ] || top=$(printf '%s' "$p" | sed -n 's/.*read_verilog [^;]*\/\([A-Za-z0-9_]*\)\.ooc\.v.*/\1/p')
json=$(printf '%s' "$p" | sed -n 's/.*write_json \([^;"]*\).*/\1/p')
emit_block() {
  echo "=== $top ==="
  echo ""
  if [ "$1" = mapped ]; then
    echo "     8   LUT4"
    echo "     4   FDRE"
    echo "     2   CARRY4"
  fi
}
case "$p" in *synth_xilinx*) emit_block mapped ;; esac
case "$p" in *" stat;"*)
  case "$p" in *synth_xilinx*) emit_block mapped ;; *) emit_block unmapped ;; esac ;;
esac
[ -n "$json" ] && printf '{"modules":{}}' > "$json"
exit 0
"""

#: Two top blocks with DIFFERENT counts: the parse must take the last one,
#: deterministically -- not the first, and not the sum.
YOSYS_TWO_BLOCKS = r"""#!/bin/sh
p="$2"
top=$(printf '%s' "$p" | sed -n 's/.*-top \([A-Za-z0-9_]*\).*/\1/p')
json=$(printf '%s' "$p" | sed -n 's/.*write_json \([^;"]*\).*/\1/p')
echo "=== $top ==="
echo "     8   LUT4"
echo "=== $top ==="
echo "    16   LUT4"
echo "     4   FDRE"
[ -n "$json" ] && printf '{"modules":{}}' > "$json"
exit 0
"""

#: awk dispatcher: the REPORT parse (recognisable by its `top=` -v binding)
#: dies; every other awk (the ROM geometry check) runs for real.
AWK_FAIL_REPORT = """#!/bin/sh
for a in "$@"; do
  case "$a" in top=*) echo 'planted awk report failure' >&2; exit 7 ;; esac
done
exec %(real)s "$@"
"""

#: python3 dispatcher: sabotage one generator, hand everything else
#: (pp_srcs.py, the other generator) to the real interpreter. `$out` holds
#: the -o target when the sabotage wants to write something itself.
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


def _stub(bindir, name, content):
    p = os.path.join(bindir, name)
    with open(p, "w") as fh:
        fh.write(content)
    os.chmod(p, 0o755)


def _run(script, top, home, rundir, ooc_tmp):
    env = dict(os.environ)
    bindir = os.path.join(home, ".local", "bin")
    env["HOME"] = home
    env["PATH"] = bindir + os.pathsep + env.get("PATH", "")
    env["OOC_TMP"] = ooc_tmp
    out = subprocess.run([script, top], cwd=rundir, env=env,
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def _mutant(pattern, replacement, label):
    """A copy of the real ooc.sh, in this directory (it derives the repo
    root from its own location), with one substitution applied. The pattern
    MUST hit: a mutation that no longer matches is testing nothing."""
    with open(OOC) as fh:
        text = fh.read()
    mutated, n = re.subn(pattern, replacement, text)
    if n != 1:
        raise AssertionError("mutation %r: pattern hit %d times, expected 1 "
                             "(ooc.sh's yosys command moved?)" % (label, n))
    fd, path = tempfile.mkstemp(suffix=".sh", prefix=".ooc-mut-", dir=HERE)
    with os.fdopen(fd, "w") as fh:
        fh.write(mutated)
    os.chmod(path, 0o755)
    return path


def selftest():
    problems, ran = [], 0

    def arm(name, top, want, expect_rc0, sv2v=SV2V_OK, yosys=YOSYS_OK,
            py=None, awk=None, script=OOC, setup=None, check=None):
        nonlocal ran
        ran += 1
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            if setup:
                os.makedirs(ooc_tmp)
                setup(ooc_tmp)
            _stub(bindir, "sv2v", sv2v)
            _stub(bindir, "yosys", yosys)
            if py:
                _stub(bindir, "python3",
                      PY_DISPATCH % {"target": py[0], "action": py[1],
                                     "real": REAL_PYTHON})
            if awk:
                _stub(bindir, "awk", awk % {"real": REAL_AWK})
            rc, log = _run(script, top, home, rundir, ooc_tmp)
            litter = os.listdir(rundir)
            if expect_rc0:
                if rc != 0:
                    problems.append("SELF-TEST FAILED [%s]: a well-formed run "
                                    "must exit 0, got rc=%d\n%s"
                                    % (name, rc, log.strip()))
                    return
            elif rc == 0 or want not in log:
                problems.append("SELF-TEST FAILED [%s]: expected a non-zero "
                                "exit naming %r, got rc=%d\n%s"
                                % (name, want, rc, log.strip()))
                return
            if litter:
                problems.append("SELF-TEST FAILED [%s]: the run littered the "
                                "caller's directory with %s (the #191/#192 "
                                "rule)" % (name, litter))
                return
            if check:
                miss = check(log, ooc_tmp)
                if miss:
                    problems.append("SELF-TEST FAILED [%s]: %s\n%s"
                                    % (name, miss, log.strip()))

    def row_of(log):
        for line in log.splitlines():
            if line.startswith("tcam "):
                return line.split()
        return None

    # ---- generation and geometry -----------------------------------------

    # Arm 1. ANTI-VACUITY. With every tool succeeding, the run must exit 0,
    # print the row the stub's LAST stat block defines (8 LUT / 4 FF /
    # 2 CARRY4, never zeros manufactured by an empty parse), and have
    # generated BOTH control-plane ROMs (by the real generators, validated
    # for geometry) into its own tmp dir -- never the caller's.
    def clean_checks(log, ooc_tmp):
        row = row_of(log)
        if row is None:
            return "no row printed for the requested top"
        if row[1:4] != ["8", "0", "8"] or row[4] != "4":
            return "row is not the stub's stat block (got %s)" % (row,)
        for img, size in (("ltn_rom.hex", 128), ("ucode.hex", 2048)):
            p = os.path.join(ooc_tmp, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run's tmp dir" % img
        return None
    arm("clean", "tcam", None, True, check=clean_checks)

    # Arm 2. A yosys failure must fail the SCRIPT, naming the top and the
    # error, not just print a row-shaped apology and exit 0.
    arm("yosys-fail", "tcam", "planted yosys elaboration failure", False,
        yosys=YOSYS_FAIL,
        check=lambda log, t: None if "yosys FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 3. Same for the sv2v front end.
    arm("sv2v-fail", "tcam", "planted sv2v failure", False, sv2v=SV2V_FAIL,
        check=lambda log, t: None if "sv2v FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 4. The microcode generator's exit status is taken, not `|| true`d.
    arm("ucode-generator-fail", "tcam", "gen_ucode.py", False,
        py=("gen_ucode.py",
            "echo 'planted ucode generator failure' >&2\n  exit 3"),
        check=lambda log, t: None if row_of(log) is None
        else "a top was priced after the generator failed")

    # Arm 5. Present and zero bytes is a refusal: an empty image is an
    # all-zero ROM and a wrong number, not an error.
    arm("ucode-empty", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", ": > \"$out\"\n  exit 0"))

    # Arm 6. ONE syntactically valid word ([R-parallel]'s exact plant): it
    # is non-empty, $readmemh loads it and leaves 2,047 words X, and the old
    # -s check priced the X-ROM 4,045 LUT_TOT under the true figure.
    arm("ucode-one-word", "tcam", "1 words, expected exactly 2048", False,
        py=("gen_ucode.py", "printf '000000000000\\n' > \"$out\"\n  exit 0"))

    # Arm 7. Truncated: right words, too few of them.
    arm("ucode-truncated", "tcam", "1000 words, expected exactly 2048", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -1000 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON,
                          os.path.join(REPO, "protocol-processor", "hdl",
                                       "aecp", "ucode", "gen_ucode.py"))))

    # Arm 8. Malformed word: full depth, one word of the wrong shape. `Z` is
    # $readmemh-legal and loads as Z, which is exactly why it is refused.
    arm("ucode-malformed", "tcam", "not exactly 12 hex digits", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out\" > /dev/null && "
            "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
            % (REAL_PYTHON, os.path.join(REPO, "protocol-processor", "hdl",
                                         "aecp", "ucode", "gen_ucode.py"))))

    # Arm 9. The transition ROM gets the identical geometry contract.
    arm("ltn-one-word", "tcam", "1 words, expected exactly 128", False,
        py=("gen_ltn_rom.py", "printf '00000000\\n' > \"$out\"\n  exit 0"))

    # Arm 10. ...and the identical width contract (a 3-digit word among 128).
    arm("ltn-malformed", "tcam", "not exactly 8 hex digits", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
            "  exit 0" % (REAL_PYTHON,
                          os.path.join(REPO, "protocol-processor", "hdl",
                                       "acmp", "rom", "gen_ltn_rom.py"))))

    # Arm 11. The ltn generator's exit status, like the ucode one's.
    arm("ltn-generator-fail", "tcam", "gen_ltn_rom.py", False,
        py=("gen_ltn_rom.py",
            "echo 'planted ltn generator failure' >&2\n  exit 3"))

    # Arm 12. STALE image + no-op generator: OOC_TMP is reusable, so a
    # leftover image plus a generator that writes nothing must refuse, not
    # re-measure last week's ROM. The delete-then-fresh-temp-then-rename
    # publish makes the no-op leave no temp file, which is the refusal, and
    # the stale image must be GONE afterwards, not retained for a next run.
    def stale_gone(log, ooc_tmp):
        if os.path.exists(os.path.join(ooc_tmp, "ucode.hex")):
            return "the stale ucode.hex survived the refusal"
        return None
    arm("ucode-stale-noop", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", "exit 0"),
        setup=lambda t: open(os.path.join(t, "ucode.hex"), "w").write(
            "STALE\n"),
        check=stale_gone)

    # Arm 13. A requested top the list does not carry is a refusal, not an
    # empty header at exit 0.
    arm("unknown-top", "laneA_no_such_top", "unknown top", False)

    # ---- the report phase ([R-parallel] finding 2) -----------------------

    # Arm 14. A dead report awk is a failed top, not a missing row.
    arm("report-awk-fail", "tcam", "planted awk report failure", False,
        awk=AWK_FAIL_REPORT,
        check=lambda log, t: None if "report FAIL" in log
        else "the report phase did not name itself")

    # Arm 15. ooc.sh with synth_xilinx AND the explicit stat dropped from
    # its yosys command: no stat block can exist, and the parse must refuse
    # instead of letting an END clause manufacture an all-zero row.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten; stat;",
                  " ", "no-stat-source")
    try:
        arm("mut-no-stat-block", "tcam", "no stat block", False, script=mut)
    finally:
        os.unlink(mut)

    # Arm 16. synth_xilinx dropped, explicit stat kept: the block exists but
    # maps to zero xc7 cells (real yosys prints $-cells there), and a zero
    # row is never a measurement.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten;",
                  " ", "no-synth")
    try:
        arm("mut-unmapped-stat", "tcam", "zero xc7 cells", False, script=mut)
    finally:
        os.unlink(mut)

    # Arm 17. write_json dropped: the artifact the command names must exist
    # non-empty, or the run refuses.
    mut = _mutant(r"; write_json \$TMP/\$top\.ooc\.json", "", "no-json")
    try:
        arm("mut-no-json", "tcam", "no JSON netlist artifact", False,
            script=mut)
    finally:
        os.unlink(mut)

    # Arm 18. TWO top blocks with different counts (a pristine log really
    # does carry two): the row is the LAST block, deterministically -- 16
    # LUT, not the first block's 8 and not the sum 24.
    def last_block_wins(log, ooc_tmp):
        row = row_of(log)
        if row is None:
            return "no row printed"
        if row[1] != "16" or row[4] != "4":
            return "row is not the last stat block (got %s)" % (row,)
        return None
    arm("two-blocks-last-wins", "tcam", None, True, yosys=YOSYS_TWO_BLOCKS,
        check=last_block_wins)

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
    print("ooc.sh refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())
