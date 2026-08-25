#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/yosys/ooc.sh's refusals, automatically, on planted failures.

That script's exit status is the gate (#245): a top that fails sv2v or yosys,
a ROM generator that fails or emits an empty, truncated, one-word, malformed
or WRONG-CONTENT image (sha256 against the pin-keyed rom_digests.tsv), a
staging or publication step that fails, a report phase that cannot produce a
real row, and a requested top that matches nothing must each leave a
non-zero exit - and one failed top stays failed however many later tops
pass. Three review rounds shaped this file; each one's counterexamples are
arms below, named for what they plant.

WHAT IT RUNS IS THE REAL ooc.sh, not a copy of its logic. The plants ride
seams the script already has: it resolves `sv2v`, `yosys`, `awk` and
`python3` through PATH after prepending `$HOME/.local/bin`, so each arm runs
it with HOME pointing at a scratch directory whose `.local/bin` carries the
planted tool (the same directory is also put first on PATH directly). The
ROM generators, the geometry packages and scripts/pp_srcs.py run for real
through a dispatching `python3` stub, so the generation path the positive
arms prove is the shipping one.

THE STUBS ARE MODELS WITH TEETH, not silence:

  - the sv2v model RECORDS every argument it is handed, and the positive
    `KL_pp_shadow` arm requires the source set to EQUAL the authoritative
    population (pp_srcs.py's own answer plus the parent's named files) - so
    a recipe whose processor list stops being derived cannot stay green;
  - the yosys model refuses to run anywhere but `$OOC_TMP` and refuses a
    missing canonical `ucode.hex`/`ltn_rom.hex` regular file in its cwd - so
    restoring the launch-directory dependency #245 exists to kill is a red
    arm, not a silent pass;
  - its mapped stat block carries EVERY cell class the parser reports
    (LUT, LUTRAM via RAM32M, FF, RAMB36, RAMB18, DSP, CARRY4), and the
    clean arm compares EVERY column of the printed row, so a zeroed
    accumulator in any column is caught;
  - stat blocks appear only when the -p command carries their source,
    mapped cells only from `synth_xilinx`, JSON only from `write_json`, and
    an empty JSON artifact is its own arm.

Mutation copies of ooc.sh itself (report-phase deletions, the population
replaced by a hand list, `cd "$TMP"` -> `cd "$R"`, the digest ledger
detached, the geometry source swapped for planted packages) prove each
detector can fail. Real synthesis is NOT run here; the real-toolchain run is
recorded on the PR that lands a change.

    python3 syn/yosys/ooc_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/ooc_tcl_selftest.py;
the invocation AND its step keys are pinned by scripts/ci_events.py. Needs
the protocol-processor submodule; it does not need yosys or sv2v.
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
GEN_UCODE = os.path.join(REPO, "protocol-processor", "hdl", "aecp", "ucode",
                         "gen_ucode.py")
GEN_LTN = os.path.join(REPO, "protocol-processor", "hdl", "acmp", "rom",
                       "gen_ltn_rom.py")

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 38

#: The clean row the full-cell yosys model must produce for any top:
#: 8 LUT4, 2 RAM32M (= 8 LUTRAM-LUT), 4 FDRE, 3 RAMB36E1, 2 RAMB18E1,
#: 1 DSP48E1, 5 CARRY4 -> LUT 8, LUTRAM 8, LUT_TOT 16, FF 4, R36 3, R18 2,
#: DSP 1, C4 5. Every column is asserted, so no accumulator can be zeroed.
FULL_ROW = ["8", "8", "16", "4", "3", "2", "1", "5"]

SV2V_OK = """#!/bin/sh
printf '%s\\n' "$@" >> "$HOME/sv2v-args.txt"
exit 0
"""
SV2V_FAIL = "#!/bin/sh\necho 'planted sv2v failure' >&2\nexit 1\n"
YOSYS_FAIL = ("#!/bin/sh\necho 'ERROR: planted yosys elaboration failure'\n"
              "exit 1\n")

#: The honest yosys model (see the module docstring). $2 is the -p command.
#: @PLANT@ is replaced (literally, no %-formatting: the shell body
#: is full of real percent-free but sed-heavy text) per variant.
YOSYS_TMPL = r"""#!/bin/sh
p="$2"
@PLANT@
if [ -z "${OOC_TMP:-}" ] || [ "$(pwd -P)" != "$(cd "$OOC_TMP" && pwd -P)" ]; then
  echo "ERROR: YOSYS-WRONG-CWD: running in $(pwd -P), not the run tmp dir"
  exit 9
fi
for img in ucode.hex ltn_rom.hex; do
  if [ ! -f "$img" ] || [ -L "$img" ]; then
    echo "ERROR: YOSYS-IMAGE-NOT-HERE: $img is not a regular file in $(pwd -P)"
    exit 9
  fi
done
top=$(printf '%s' "$p" | sed -n 's/.*-top \([A-Za-z0-9_]*\).*/\1/p')
[ -n "$top" ] || top=$(printf '%s' "$p" | sed -n 's/.*read_verilog [^;]*\/\([A-Za-z0-9_]*\)\.ooc\.v.*/\1/p')
json=$(printf '%s' "$p" | sed -n 's/.*write_json \([^;"]*\).*/\1/p')
emit_block() {
  echo "=== $top ==="
  echo ""
  if [ "$1" = mapped ]; then
    echo "     8   LUT4"
    echo "     2   RAM32M"
    echo "     4   FDRE"
    echo "     3   RAMB36E1"
    echo "     2   RAMB18E1"
    echo "     1   DSP48E1"
    echo "     5   CARRY4"
  fi
}
case "$p" in *synth_xilinx*) emit_block mapped ;; esac
case "$p" in *" stat;"*)
  case "$p" in *synth_xilinx*) emit_block mapped ;; *) emit_block unmapped ;; esac ;;
esac
[ -n "$json" ] && printf '{"modules":{}}' > "$json"
exit 0
"""
YOSYS_OK = YOSYS_TMPL.replace("@PLANT@", "")
#: A planted failure for ONE top of a multi-top run.
YOSYS_FAIL_TCAM = YOSYS_TMPL.replace("@PLANT@",
    'case "$p" in *"-top tcam "*) '
    "echo 'ERROR: planted tcam-only failure'; exit 1 ;; esac")
#: JSON written EMPTY: `-e` would pass it, `-s` must not.
YOSYS_EMPTY_JSON = YOSYS_TMPL.replace("@PLANT@",
    'json=$(printf \'%s\' "$p" | sed -n \'s/.*write_json \\([^;"]*\\).*/\\1/p\')\n'
    '[ -n "$json" ] && : > "$json"\n'
    'p=$(printf \'%s\' "$p" | sed \'s/; write_json [^;"]*//\')')
#: Two top blocks with DIFFERENT counts: the parse must take the last one.
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

AWK_FAIL_REPORT = """#!/bin/sh
for a in "$@"; do
  case "$a" in top=*) echo 'planted awk report failure' >&2; exit 7 ;; esac
done
exec %(real)s "$@"
"""

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

_POPULATION = None


def pp_population():
    """The authoritative processor population plus the parent's named files:
    what a KL_pp_shadow elaboration must consume, from pp_srcs.py itself."""
    global _POPULATION
    if _POPULATION is None:
        out = subprocess.run(
            [REAL_PYTHON, os.path.join(REPO, "scripts", "pp_srcs.py"),
             "--prefix", os.path.join(REPO, "protocol-processor", "hdl")],
            capture_output=True, text=True, check=True)
        pop = out.stdout.split()
        pop += [os.path.join(REPO, "third_party", "verilog-axis", "rtl",
                             "axis_fifo.v"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_shadow.sv"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_maap_shim.sv")]
        _POPULATION = sorted(pop)
    return _POPULATION


def _stub(bindir, name, content):
    p = os.path.join(bindir, name)
    with open(p, "w") as fh:
        fh.write(content)
    os.chmod(p, 0o755)


def _run(script, tops, home, rundir, ooc_tmp):
    env = dict(os.environ)
    bindir = os.path.join(home, ".local", "bin")
    env["HOME"] = home
    env["PATH"] = bindir + os.pathsep + env.get("PATH", "")
    env["OOC_TMP"] = ooc_tmp
    out = subprocess.run([script] + tops, cwd=rundir, env=env,
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
                             "(ooc.sh moved?)" % (label, n))
    fd, path = tempfile.mkstemp(suffix=".sh", prefix=".ooc-mut-", dir=HERE)
    with os.fdopen(fd, "w") as fh:
        fh.write(mutated)
    os.chmod(path, 0o755)
    return path


def selftest():
    problems, ran = [], 0

    def arm(name, tops, want, expect_rc0, sv2v=SV2V_OK, yosys=YOSYS_OK,
            py=None, awk=None, script=OOC, setup=None, check=None):
        nonlocal ran
        ran += 1
        if isinstance(tops, str):
            tops = [tops]
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            if setup:
                os.makedirs(ooc_tmp, exist_ok=True)
                setup(ooc_tmp)
            _stub(bindir, "sv2v", sv2v)
            _stub(bindir, "yosys", yosys)
            if py:
                _stub(bindir, "python3",
                      PY_DISPATCH % {"target": py[0], "action": py[1],
                                     "real": REAL_PYTHON})
            if awk:
                _stub(bindir, "awk", awk % {"real": REAL_AWK})
            rc, log = _run(script, tops, home, rundir, ooc_tmp)
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
                miss = check(log, ooc_tmp, home)
                if miss:
                    problems.append("SELF-TEST FAILED [%s]: %s\n%s"
                                    % (name, miss, log.strip()))

    def row_of(log, top="tcam"):
        for line in log.splitlines():
            if line.startswith(top + " ") and "FAIL" not in line:
                return line.split()
        return None

    def _write(d, name, content):
        with open(os.path.join(d, name), "w") as fh:
            fh.write(content)

    # ---- generation, geometry, content, staging --------------------------

    # Arm 1. ANTI-VACUITY, full-width: every column of the printed row must
    # equal the model's stat block (no zeroed accumulator, no manufactured
    # row), both ROMs generated and digest-verified into the run's own tmp
    # dir, nothing in the caller's directory.
    def clean_checks(log, ooc_tmp, home):
        row = row_of(log)
        if row is None:
            return "no row printed for the requested top"
        if row[1:] != FULL_ROW:
            return "row is not the model's stat block: got %s, want %s" \
                   % (row[1:], FULL_ROW)
        for img in ("ltn_rom.hex", "ucode.hex"):
            p = os.path.join(ooc_tmp, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run's tmp dir" % img
        return None
    arm("clean-full-columns", "tcam", None, True, check=clean_checks)

    # Arm 2. A yosys failure fails the SCRIPT, naming the top and the error.
    arm("yosys-fail", "tcam", "planted yosys elaboration failure", False,
        yosys=YOSYS_FAIL,
        check=lambda log, t, h: None if "yosys FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 3. Same for the sv2v front end.
    arm("sv2v-fail", "tcam", "planted sv2v failure", False, sv2v=SV2V_FAIL,
        check=lambda log, t, h: None if "sv2v FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 4. The microcode generator's exit status is taken, not `|| true`d.
    arm("ucode-generator-fail", "tcam", "gen_ucode.py", False,
        py=("gen_ucode.py",
            "echo 'planted ucode generator failure' >&2\n  exit 3"),
        check=lambda log, t, h: None if row_of(log) is None
        else "a top was priced after the generator failed")

    # Arms 5-8. Shape mutations for the microcode image.
    arm("ucode-empty", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", ": > \"$out\"\n  exit 0"))
    arm("ucode-one-word", "tcam", "1 words, expected exactly 2048", False,
        py=("gen_ucode.py", "printf '000000000000\\n' > \"$out\"\n  exit 0"))
    arm("ucode-truncated", "tcam", "1000 words, expected exactly 2048", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -1000 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_UCODE)))
    arm("ucode-malformed", "tcam", "not exactly 12 hex digits", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out\" > /dev/null && "
            "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
            % (REAL_PYTHON, GEN_UCODE)))

    # Arm 9. STALE image + no-op generator; the stale image must be GONE.
    def stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ucode.hex")):
            return "the stale ucode.hex survived the refusal"
        return None
    arm("ucode-stale-noop", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", "exit 0"),
        setup=lambda t: _write(t, "ucode.hex", "STALE\n"), check=stale_gone)

    # Arm 10. [R0] round two's BLOCKER plant: a correctly SHAPED corrupt
    # image - 2,048 valid all-zero words from a "successful" generator. It
    # passes every shape gate and once priced KL_pp_shadow 4,045 LUT_TOT
    # low; only the pin-keyed content digest refuses it.
    arm("ucode-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_ucode.py",
            "%s -c \"print('\\\\n'.join(['0'*12]*2048))\" > \"$out\"\n"
            "  exit 0" % REAL_PYTHON),
        check=lambda log, t, h: None if row_of(log) is None
        else "a top was priced from a corrupt-content ROM")

    # Arms 11-17. The transition ROM gets the SAME set, symmetrically.
    arm("ltn-generator-fail", "tcam", "gen_ltn_rom.py", False,
        py=("gen_ltn_rom.py",
            "echo 'planted ltn generator failure' >&2\n  exit 3"))
    arm("ltn-one-word", "tcam", "1 words, expected exactly 128", False,
        py=("gen_ltn_rom.py", "printf '00000000\\n' > \"$out\"\n  exit 0"))
    arm("ltn-malformed", "tcam", "not exactly 8 hex digits", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_LTN)))
    arm("ltn-truncated", "tcam", "words, expected exactly 128", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -64 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_LTN)))
    arm("ltn-empty", "tcam", "ltn_rom.hex is malformed", False,
        py=("gen_ltn_rom.py", ": > \"$out\"\n  exit 0"))
    def ltn_stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ltn_rom.hex")):
            return "the stale ltn_rom.hex survived the refusal"
        return None
    arm("ltn-stale-noop", "tcam", "ltn_rom.hex is malformed", False,
        py=("gen_ltn_rom.py", "exit 0"),
        setup=lambda t: _write(t, "ltn_rom.hex", "STALE\n"),
        check=ltn_stale_gone)
    arm("ltn-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_ltn_rom.py",
            "%s -c \"print('\\\\n'.join(['0'*8]*128))\" > \"$out\"\n"
            "  exit 0" % REAL_PYTHON))

    # Arm 18. A requested top the list does not carry refuses.
    arm("unknown-top", "laneA_no_such_top", "unknown top", False)

    # Arm 19. A directory squatting the publish target: cleanup must be
    # CHECKED, not assumed ([R0] round two).
    arm("target-dir-squat", "tcam", "cannot remove the previous ucode.hex",
        False, setup=lambda t: os.makedirs(os.path.join(t, "ucode.hex")))

    # Arm 20. [R0] round two's staging plant: files squatting predictable
    # staging names plus a no-op generator. mktemp's exclusive random name
    # ignores them; the empty stage refuses; nothing stale is published.
    def preplant_stages(t):
        _write(t, "ucode.hex.gen.%d" % os.getpid(), "STALE-STAGE\n")
        _write(t, "ucode.hex.stage.AAAAAAAA", "STALE-STAGE\n")
    def no_stale_published(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ucode.hex")):
            return "a stale staging file was published as ucode.hex"
        return None
    arm("stale-stage-preplant", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", "exit 0"), setup=preplant_stages,
        check=no_stale_published)

    # Arm 21. The ledger without this pin's rows: refuse, do not guess.
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/planted-empty-ledger.tsv"',
                  "digest-ledger-detached")
    try:
        arm("digest-unrecorded-pin", "tcam", "no recorded content digest",
            False, script=mut,
            setup=lambda t: _write(t, "planted-empty-ledger.tsv", "# empty\n"))
    finally:
        os.unlink(mut)

    # Arm 22. The record mode round-trips: --record-rom-digests writes this
    # pin's rows into the (detached, scratch) ledger, and the very next run
    # against that ledger passes. Proves the pin-bump procedure works and
    # that arm 21's refusal is about the ledger's CONTENT, not a broken mode.
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "digest-ledger-scratch")
    try:
        ran += 1
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            os.makedirs(ooc_tmp)
            _write(ooc_tmp, "scratch-ledger.tsv", "# scratch\n")
            _stub(bindir, "sv2v", SV2V_OK)
            _stub(bindir, "yosys", YOSYS_OK)
            rc1, log1 = _run(mut, ["--record-rom-digests"], home, rundir,
                             ooc_tmp)
            rows = [l for l in
                    open(os.path.join(ooc_tmp, "scratch-ledger.tsv"))
                    if l.strip() and not l.startswith("#")]
            rc2, log2 = _run(mut, ["tcam"], home, rundir, ooc_tmp)
            if rc1 != 0 or len(rows) != 2 or rc2 != 0 \
                    or row_of(log2) is None:
                problems.append("SELF-TEST FAILED [record-mode-roundtrip]: "
                                "record rc=%d rows=%d, rerun rc=%d\n%s\n%s"
                                % (rc1, len(rows), rc2, log1.strip(),
                                   log2.strip()))
    finally:
        os.unlink(mut)

    # ---- the report phase ------------------------------------------------

    # Arm 23. A dead report awk is a failed top, not a missing row.
    arm("report-awk-fail", "tcam", "planted awk report failure", False,
        awk=AWK_FAIL_REPORT,
        check=lambda log, t, h: None if "report FAIL" in log
        else "the report phase did not name itself")

    # Arm 24. Both stat sources dropped from ooc.sh's yosys command.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten; stat;",
                  " ", "no-stat-source")
    try:
        arm("mut-no-stat-block", "tcam", "no stat block", False, script=mut)
    finally:
        os.unlink(mut)

    # Arm 25. synth_xilinx dropped, stat kept: an unmapped stat block maps
    # to zero xc7 cells, and a zero row is never a measurement.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten;",
                  " ", "no-synth")
    try:
        arm("mut-unmapped-stat", "tcam", "zero xc7 cells", False, script=mut)
    finally:
        os.unlink(mut)

    # Arm 26. write_json dropped: the artifact must exist.
    mut = _mutant(r"; write_json \$TMP/\$top\.ooc\.json", "", "no-json")
    try:
        arm("mut-no-json", "tcam", "JSON netlist artifact", False,
            script=mut)
    finally:
        os.unlink(mut)

    # Arm 27. The artifact written EMPTY: `-e` would pass it; the run must
    # refuse ([R0] round two weakened `-s` to `-e` behind green arms).
    arm("empty-json", "tcam", "JSON netlist artifact", False,
        yosys=YOSYS_EMPTY_JSON)

    # Arm 28. TWO top blocks with different counts: last wins, no sum.
    def last_block_wins(log, ooc_tmp, home):
        row = row_of(log)
        if row is None:
            return "no row printed"
        if row[1] != "16" or row[4] != "4":
            return "row is not the last stat block (got %s)" % (row,)
        return None
    arm("two-blocks-last-wins", "tcam", None, True, yosys=YOSYS_TWO_BLOCKS,
        check=last_block_wins)

    # Arm 29. STICKY EXIT across tops ([R0] round two): the first top fails,
    # the second passes and prints its row, and the script still exits
    # non-zero. A later success must never launder an earlier failure.
    def both_outcomes(log, ooc_tmp, home):
        if "planted tcam-only failure" not in log:
            return "the failing top did not fail"
        if row_of(log, "KL_pcm_lpf") is None:
            return "the passing top printed no row"
        return None
    arm("multi-top-fail-then-pass", ["tcam", "KL_pcm_lpf"],
        "planted tcam-only failure", False, yosys=YOSYS_FAIL_TCAM,
        check=both_outcomes)

    # ---- the affected tops consume the authoritative inputs ([R0] r2) ----

    # Arm 30. POSITIVE KL_pp_shadow: the sv2v model recorded exactly the
    # authoritative processor population (pp_srcs.py's own answer) plus the
    # parent's named files; the yosys model already refused to run outside
    # $OOC_TMP or without both canonical regular images in its cwd.
    def population_ok(log, ooc_tmp, home):
        rec = os.path.join(home, "sv2v-args.txt")
        if not os.path.isfile(rec):
            return "the sv2v model recorded no arguments"
        got = sorted(a for a in open(rec).read().split()
                     if a.endswith(".sv") or a.endswith(".v"))
        if got != pp_population():
            return ("KL_pp_shadow's source set (%d files) is not the "
                    "authoritative population (%d files)"
                    % (len(got), len(pp_population())))
        if row_of(log, "KL_pp_shadow") is None:
            return "no row printed"
        return None
    arm("pp-shadow-population", "KL_pp_shadow", None, True,
        check=population_ok)

    # Arm 31. [R0] round two's plant: the derived population replaced by a
    # hand list of the two geometry packages. Geometry still resolves; the
    # population detector must distinguish, or arm 30 is vacuous. (On the
    # real tree this plant ALSO trips scripts/pp_srcs.py --check, since no
    # PROSE_OK exemption exists any more; the paths here are composed so
    # THIS tracked file is not the plant.)
    dollar_pp = "$" + "PP"
    mut = _mutant(
        r'PP_DERIVED="\$\(python3 "\$R/scripts/pp_srcs\.py" --prefix "\$PP"\)" \|\| exit 2',
        'PP_DERIVED="%s/aecp/ucpu_pkg.sv %s/acmp/pp_acmp_pkg.sv"'
        % (dollar_pp, dollar_pp), "hand-population")
    try:
        def hand_pop_detected(log, ooc_tmp, home):
            rec = os.path.join(home, "sv2v-args.txt")
            got = sorted(a for a in open(rec).read().split()
                         if a.endswith(".sv") or a.endswith(".v"))
            if got == pp_population():
                return "the hand-population mutant equals the record: the " \
                       "detector cannot distinguish"
            return None
        arm("mut-hand-population", "KL_pp_shadow", None, True, script=mut,
            check=hand_pop_detected)
    finally:
        os.unlink(mut)

    # Arm 32. [R0] round two's plant: cd "$TMP" -> cd "$R", restoring the
    # launch-directory dependency #245 exists to kill. The yosys model
    # refuses to run anywhere but $OOC_TMP.
    mut = _mutant(r'\(cd "\$TMP" && yosys', '(cd "$R" && yosys', "cwd-escape")
    try:
        arm("mut-cwd-escape", "tcam", "YOSYS-WRONG-CWD", False, script=mut)
    finally:
        os.unlink(mut)

    # ---- the geometry parser ([R0] round two, finding 3) -----------------

    def pkg_mutant(pkg_text, label):
        fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
        with os.fdopen(fd, "w") as fh:
            fh.write(pkg_text)
        mut = _mutant(
            r'UCODE_W=\$\(pkg_num "\$UCPU_PKG" UCODE_W_C\)  \|\| exit 2',
            'UCODE_W=$(pkg_num "%s" UCODE_W_C)  || exit 2' % pkg, label)
        return pkg, mut

    # Arm 33. [R0]'s plant: a stale value in a comment above a live 52. The
    # LIVE value must win; with 52 the real 48-bit image no longer fits, and
    # THAT refusal proves the comment lost.
    pkg, mut = pkg_mutant(
        "// stale example: UCODE_W_C = 48\n"
        "localparam int unsigned UCODE_W_C = 52;\n", "pkg-comment-shadow")
    try:
        arm("pkg-comment-shadow-live-wins", "tcam",
            "not exactly 13 hex digits", False, script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 34. Block comments stripped and prefixed identifiers ignored: the
    # run stays WELL-FORMED at the live 48.
    pkg, mut = pkg_mutant(
        "/* stale block:\n   localparam int unsigned UCODE_W_C = 40;\n*/\n"
        "localparam int unsigned XUCODE_W_C = 99;\n"
        "localparam int unsigned UCODE_W_C  = 48;\n", "pkg-block-and-prefix")
    try:
        arm("pkg-block-comment-and-prefix", "tcam", None, True, script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 35. TWO live declarations: a refusal, never a pick.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UCODE_W_C = 52;\n", "pkg-duplicate")
    try:
        arm("pkg-duplicate", "tcam", "exactly one live declaration", False,
            script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 36. An EXPRESSION initialiser is unsupported: refuse, not guess.
    pkg, mut = pkg_mutant(
        "localparam int unsigned OTHER_C = 12;\n"
        "localparam int unsigned UCODE_W_C = OTHER_C * 4;\n",
        "pkg-expression")
    try:
        arm("pkg-expression", "tcam", "exactly one live declaration", False,
            script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 37. A NON-NIBBLE width refuses outright ([R-parallel] round three
    # on PR #264; this script shared the truncating digit arithmetic): a
    # declared 50 would truncate to 12 digits and accept the stale 48-bit
    # image. Same guard, both scripts.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 50;\n", "pkg-width-50")
    try:
        arm("pkg-width-50-not-nibble", "tcam", "not a positive nibble-aligned",
            False, script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 38. The transition ROM's width gets the identical guard (34 would
    # truncate to 8 digits and accept the stale 32-bit image).
    fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
    with os.fdopen(fd, "w") as fh:
        fh.write("localparam int unsigned TROM_W_C = 34;\n"
                 "localparam int unsigned TROM_DEPTH_C = 128;\n")
    mut = _mutant(r'ACMP_PKG=\$\(one_pp_source pp_acmp_pkg\.sv\)  \|\| exit 2',
                  'ACMP_PKG="%s"' % pkg, "acmp-pkg-width-34")
    try:
        arm("ltn-width-34-not-nibble", "tcam", "not a positive nibble-aligned",
            False, script=mut)
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
    print("ooc.sh refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())
