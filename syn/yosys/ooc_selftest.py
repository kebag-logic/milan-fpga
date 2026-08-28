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
  - the yosys model refuses to run anywhere but an exclusive per-top
    `*.run.*` directory under `$OOC_TMP` (the shared `$OOC_TMP` itself is a
    refusal too, [R0] round four), refuses a run directory that is still
    WRITABLE (rename authority is directory write permission, [R0] round
    five), refuses a missing or WRITABLE canonical
    `ucode.hex`/`ltn_rom.hex`/`gptp_ucode.hex` regular file in its cwd, and
    asserts each
    image's sha256 against the pin's ledger row - the exact-byte oracle the
    round-four review required, so consuming unvouched bytes is a red arm
    even if every ooc.sh-side re-hash were deleted;
  - a transient-swap model performs [R0] round five's exact exploit (move
    the reviewed image aside, feed different bytes, restore before the
    post-run hash) and reports whether the rename was POSSIBLE - blocked
    on the shipping script, demonstrated to price wrong bytes on the
    mutant that forgets the directory lock;
  - the ledger pin is the SUPERPROJECT gitlink, and a planted stale
    submodule HEAD (a dispatching git stub) must refuse in normal AND
    record modes ([R0] round five);
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
both processor submodules; it does not need yosys or sv2v.
"""
import atexit
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OOC = os.path.join(HERE, "ooc.sh")
REAL_PYTHON = shutil.which("python3") or sys.executable
REAL_AWK = shutil.which("awk") or "awk"
REAL_GIT = shutil.which("git") or "git"
REAL_CHMOD = shutil.which("chmod") or "chmod"

#: Every scratch file this suite creates, swept on any ordinary exit AND on
#: SIGINT/SIGTERM. The mutants must live under syn/yosys/ (ooc.sh derives the
#: repository root from its own location), so an interrupted run used to
#: strand mode-0755 sabotaged copies of the gate script in a TRACKED
#: directory, one broad `git add` from a commit - the #191/#192 rule this
#: file asserts on the caller's cwd and used to exempt itself from.
#: .gitignore carries the belt to this braces, for the SIGKILL case.
_TEMPS = []


def _track(path):
    _TEMPS.append(path)
    return path


@atexit.register
def _sweep_temps():
    while _TEMPS:
        try:
            os.unlink(_TEMPS.pop())
        except OSError:
            pass


def _sweep_on_signal(signum, _frame):
    _sweep_temps()
    signal.signal(signum, signal.SIG_DFL)
    os.kill(os.getpid(), signum)


for _sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(_sig, _sweep_on_signal)
GEN_UCODE = os.path.join(REPO, "protocol-processor", "hdl", "aecp", "ucode",
                         "gen_ucode.py")
GEN_LTN = os.path.join(REPO, "protocol-processor", "hdl", "acmp", "rom",
                       "gen_ltn_rom.py")
GEN_GPTP = os.path.join(REPO, "gptp-processor", "hdl", "ucode",
                        "gen_gptp_ucode.py")


def _processor_pins():
    """Return each processor's checked-out superproject gitlink."""
    def _rev(args, what):
        out = subprocess.run([REAL_GIT] + args, capture_output=True, text=True)
        if out.returncode != 0:
            raise AssertionError(
                "cannot read %s (git exited %d: %s) - this suite certifies "
                "the ROMs generated from the pinned processors; run "
                "git submodule update --init protocol-processor gptp-processor"
                % (what, out.returncode, out.stderr.strip() or "no message"))
        return out.stdout.strip()

    pins = {}
    for name in ("protocol-processor", "gptp-processor"):
        pin = _rev(["-C", REPO, "rev-parse", ":" + name],
                   "the %s gitlink from the superproject index" % name)
        head = _rev(["-C", os.path.join(REPO, name), "rev-parse", "HEAD"],
                    "the %s checkout's HEAD" % name)
        if head != pin:
            raise AssertionError(
                "the %s checkout (%s) disagrees with the superproject pin "
                "(%s) - run git submodule update before certifying anything "
                "from it" % (name, head, pin))
        pins[name] = pin
    return pins


def _ledger_digests():
    """Return the exact digest for each image at its owning processor pin."""
    pins = _processor_pins()
    expected_pin = {
        "ucode.hex": pins["protocol-processor"],
        "ltn_rom.hex": pins["protocol-processor"],
        "gptp_ucode.hex": pins["gptp-processor"],
    }
    want = {}
    with open(os.path.join(HERE, "rom_digests.tsv")) as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            cols = line.split()
            if len(cols) != 3:
                raise AssertionError(
                    "rom_digests.tsv row %r is not pin<TAB>image<TAB>sha256"
                    % line.strip())
            row_pin, img, sha = cols
            if expected_pin.get(img) == row_pin:
                want[img] = sha
    for img, pin in expected_pin.items():
        if img not in want:
            raise AssertionError(
                "rom_digests.tsv has no %s row for its owning processor pin "
                "%s - record it with ./ooc.sh --record-rom-digests" %
                (img, pin))
    return want


#: Read LAZILY. At module scope this ran before main() could catch anything,
#: so an uninitialised submodule or an unrecorded pin reached the operator as
#: a CalledProcessError traceback rather than as the sentence ooc.sh itself
#: prints for the same condition.
_LEDGER = None


def ledger():
    global _LEDGER
    if _LEDGER is None:
        _LEDGER = _ledger_digests()
    return _LEDGER

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 72

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

#: SV2V_OK plus a timing plant: when invoked for @TOP@, run @ACTION@
#: against the published images in $OOC_TMP first. sv2v runs BETWEEN
#: publication and that top's consumption, which is exactly the seam
#: [R0] round four's eight timing plants rode.
SV2V_PLANT_TMPL = """#!/bin/sh
printf '%s\\n' "$@" >> "$HOME/sv2v-args.txt"
for a in "$@"; do
  case "$a" in
    --top=@TOP@) @ACTION@ ;;
  esac
done
exit 0
"""


def sv2v_plant(top, action):
    return SV2V_PLANT_TMPL.replace("@TOP@", top).replace("@ACTION@", action)
YOSYS_FAIL = ("#!/bin/sh\necho 'ERROR: planted yosys elaboration failure'\n"
              "exit 1\n")

#: The honest yosys model (see the module docstring). $2 is the -p command.
#: @PLANT@ is replaced (literally, no %-formatting: the shell body
#: is full of real percent-free but sed-heavy text) per variant.
YOSYS_TMPL = r"""#!/bin/sh
p="$2"
@PLANT@
if [ -z "${OOC_TMP:-}" ]; then
  echo "ERROR: YOSYS-WRONG-CWD: no OOC_TMP in the environment"
  exit 9
fi
otmp="$(cd "$OOC_TMP" && pwd -P)"
case "$(pwd -P)" in
  "$otmp"/*.run.*) : ;;
  *) echo "ERROR: YOSYS-WRONG-CWD: running in $(pwd -P), not an exclusive per-top run dir under $OOC_TMP"
     exit 9 ;;
esac
if [ -w . ]; then
  echo "ERROR: YOSYS-RUNDIR-WRITABLE: $(pwd -P) accepts renames, so the consuming copies are not immutable for the read interval"
  exit 9
fi
for img in ucode.hex ltn_rom.hex gptp_ucode.hex; do
  if [ ! -f "$img" ] || [ -L "$img" ]; then
    echo "ERROR: YOSYS-IMAGE-NOT-HERE: $img is not a regular file in $(pwd -P)"
    exit 9
  fi
done
for spec in "ucode.hex ${OOC_ST_UCODE_SHA:-}" \
            "ltn_rom.hex ${OOC_ST_LTN_SHA:-}" \
            "gptp_ucode.hex ${OOC_ST_GPTP_SHA:-}"; do
  img=${spec%% *}; want=${spec#* }
  if [ -w "$img" ]; then
    echo "ERROR: YOSYS-IMAGE-WRITABLE: $img in $(pwd -P) is not the read-only consuming copy"
    exit 9
  fi
  got=$(sha256sum < "$img" | sed 's/ .*//')
  if [ "$got" != "$want" ]; then
    echo "ERROR: YOSYS-IMAGE-BYTES: $img in $(pwd -P) hashes ${got:-nothing}, the validated ledger digest is ${want:-unset}"
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

#: A dispatching git: the submodule checkout's HEAD answers a PLANTED
#: stale revision while everything else (the gitlink read included) goes
#: to the real git - [R0] round five's scratch-checkout scenario, made a
#: deterministic seam.
GIT_STALE_HEAD = """#!/bin/sh
prev=""
dir=""
for a in "$@"; do
  [ "$prev" = "-C" ] && dir="$a"
  prev="$a"
done
case "$dir" in
  */protocol-processor)
    case "$*" in
      *"rev-parse HEAD") echo b2effce9b2effce9b2effce9b2effce9b2effce9; exit 0 ;;
    esac ;;
esac
exec %(real)s "$@"
"""
GIT_STALE_GPTP_HEAD = GIT_STALE_HEAD.replace(
    "*/protocol-processor)", "*/gptp-processor)").replace(
        "b2effce9b2effce9b2effce9b2effce9b2effce9",
        "c3f00dc3c3f00dc3c3f00dc3c3f00dc3c3f00dc3")

#: chmod that always fails: every permission the script claims to set must
#: have its status TAKEN, or the hardening is a comment. One stub per guard,
#: because a stub that breaks EVERY chmod plus a want of "read-only" matched
#: three different messages - the arm passed with the a-w guard's status
#: deliberately discarded, proving only that SOME chmod refusal fired.
CHMOD_FAIL = "#!/bin/sh\nexit 1\n"
#: Fails ONLY the run-directory lock, so the u-w guard is exercised alone.
CHMOD_FAIL_DIRLOCK = """#!/bin/sh
case "$1" in u-w) echo 'planted chmod u-w failure' >&2; exit 1 ;; esac
exec %(real)s "$@"
"""

#: [R0] round five's transient swap, as a model: move the reviewed image
#: aside, install correctly shaped wrong bytes, emit a plausible stat
#: block, and RESTORE the reviewed image before exiting 0 - both script
#: hashes would pass. If the run directory refuses the rename, say so and
#: die; the marker file records that a swap actually happened.
YOSYS_TRANSIENT_SWAP = r"""#!/bin/sh
p="$2"
top=$(printf '%s' "$p" | sed -n 's/.*-top \([A-Za-z0-9_]*\).*/\1/p')
json=$(printf '%s' "$p" | sed -n 's/.*write_json \([^;"]*\).*/\1/p')
if mv ucode.hex ucode.hex.aside 2>/dev/null; then
  printf 'SWAPPED\n' > ucode.hex
  : > "$OOC_TMP/transient-swap-succeeded"
  echo "=== $top ==="
  echo ""
  echo "     8   LUT4"
  echo "     2   RAM32M"
  echo "     4   FDRE"
  echo "     3   RAMB36E1"
  echo "     2   RAMB18E1"
  echo "     1   DSP48E1"
  echo "     5   CARRY4"
  [ -n "$json" ] && printf '{"modules":{}}' > "$json"
  mv -f ucode.hex.aside ucode.hex
  exit 0
fi
echo "ERROR: YOSYS-TRANSIENT-SWAP-BLOCKED: the run directory refused the rename, so the reviewed bytes cannot be moved aside for the read interval"
exit 9
"""

#: The consuming copy corrupted DURING the run: the model does its work,
#: then rewrites ucode.hex in its cwd as it exits. Only ooc.sh's post-run
#: re-hash can catch this one.
YOSYS_CORRUPT_MIDRUN = YOSYS_TMPL.replace(
    "@PLANT@",
    "trap 'chmod u+w ucode.hex 2>/dev/null; "
    "printf MUTATED-MID-RUN > ucode.hex' EXIT")

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
    env["OOC_ST_UCODE_SHA"] = ledger()["ucode.hex"]
    env["OOC_ST_LTN_SHA"] = ledger()["ltn_rom.hex"]
    env["OOC_ST_GPTP_SHA"] = ledger()["gptp_ucode.hex"]
    out = subprocess.run([script] + tops, cwd=rundir, env=env,
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def _mutant2(p1, r1, p2, r2, label):
    """Two coupled substitutions in one mutant copy: each pattern must hit
    exactly once, like _mutant."""
    with open(OOC) as fh:
        text = fh.read()
    for pat, rep in ((p1, r1), (p2, r2)):
        text, n = re.subn(pat, rep, text)
        if n != 1:
            raise AssertionError("mutation %r: pattern %r hit %d times, "
                                 "expected 1" % (label, pat, n))
    fd, path = tempfile.mkstemp(suffix=".sh", prefix=".ooc-mut-", dir=HERE)
    with os.fdopen(fd, "w") as fh:
        fh.write(text)
    os.chmod(path, 0o755)
    return _track(path)


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
    return _track(path)


def selftest():
    problems, ran = [], 0

    def arm(name, tops, want, expect_rc0, sv2v=SV2V_OK, yosys=YOSYS_OK,
            py=None, awk=None, git=None, chmod=None, script=OOC, setup=None,
            check=None):
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
            if git:
                _stub(bindir, "git", git % {"real": REAL_GIT})
            if chmod:
                _stub(bindir, "chmod", chmod % {"real": REAL_CHMOD})
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
    # row), all three ROMs generated and digest-verified into the run's own tmp
    # dir, nothing in the caller's directory.
    def clean_checks(log, ooc_tmp, home):
        row = row_of(log)
        if row is None:
            return "no row printed for the requested top"
        if row[1:] != FULL_ROW:
            return "row is not the model's stat block: got %s, want %s" \
                   % (row[1:], FULL_ROW)
        for img in ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex"):
            p = os.path.join(ooc_tmp, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run's tmp dir" % img
        for name in os.listdir(ooc_tmp):
            if ".run." in name:
                return "the exclusive run dir %s survived its top" % name
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
    arm("ucode-generator-fail", "tcam", "ROM generator failed", False,
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
    arm("ltn-generator-fail", "tcam", "ROM generator failed", False,
        py=("gen_ltn_rom.py",
            "echo 'planted ltn generator failure' >&2\n  exit 3"))
    arm("ltn-one-word", "tcam", "1 words, expected exactly 128", False,
        py=("gen_ltn_rom.py", "printf '00000000\\n' > \"$out\"\n  exit 0"))
    arm("ltn-malformed", "tcam", "not exactly 8 hex digits", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_LTN)))
    # 63, not 64: the generator's first line is a `//` header that rom_check
    # strips, which is exactly the kind of detail an unpinned count hides.
    arm("ltn-truncated", "tcam", "63 words, expected exactly 128", False,
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

    # The gPTP microcode is independently generated, shaped and keyed to the
    # gptp-processor pin. Give it the same fail-closed generator boundary.
    arm("gptp-generator-fail", "tcam", "ROM generator failed", False,
        py=("gen_gptp_ucode.py",
            "echo 'planted gptp generator failure' >&2\n  exit 3"))
    arm("gptp-one-word", "tcam", "1 words, expected exactly 1024", False,
        py=("gen_gptp_ucode.py",
            "printf '000000000000\\n' > \"$out\"\n  exit 0"))
    arm("gptp-malformed", "tcam", "not exactly 12 hex digits", False,
        py=("gen_gptp_ucode.py",
            "%s %s -o \"$out\" > /dev/null && "
            "sed -i '2s/.*/00000000000Z/' \"$out\"\n  exit 0"
            % (REAL_PYTHON, GEN_GPTP)))
    arm("gptp-truncated", "tcam", "500 words, expected exactly 1024", False,
        py=("gen_gptp_ucode.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -500 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_GPTP)))
    arm("gptp-empty", "tcam", "gptp_ucode.hex is malformed", False,
        py=("gen_gptp_ucode.py", ": > \"$out\"\n  exit 0"))

    def gptp_stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "gptp_ucode.hex")):
            return "the stale gptp_ucode.hex survived the refusal"
        return None

    arm("gptp-stale-noop", "tcam", "gptp_ucode.hex is malformed", False,
        py=("gen_gptp_ucode.py", "exit 0"),
        setup=lambda t: _write(t, "gptp_ucode.hex", "STALE\n"),
        check=gptp_stale_gone)
    arm("gptp-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_gptp_ucode.py",
            "%s -c \"print('\\\\n'.join(['0'*12]*1024))\" > \"$out\"\n"
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
            if rc1 != 0 or len(rows) != 3 or rc2 != 0 \
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
            if not os.path.isfile(rec):
                return "the sv2v model recorded no arguments"
            got = sorted(a for a in open(rec).read().split()
                         if a.endswith(".sv") or a.endswith(".v"))
            if got == pp_population():
                return "the hand-population mutant equals the record: the " \
                       "detector cannot distinguish"
            planted = sorted([
                os.path.join(REPO, "third_party", "verilog-axis", "rtl",
                             "axis_fifo.v"),
                os.path.join(REPO, "protocol-processor", "hdl", "aecp",
                             "ucpu_pkg.sv"),
                os.path.join(REPO, "protocol-processor", "hdl", "acmp",
                             "pp_acmp_pkg.sv"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_shadow.sv"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_maap_shim.sv")])
            if got != planted:
                return ("the mutant's source set is neither the record nor "
                        "the planted hand list (%d files) - the arm proves "
                        "nothing about the population detector" % len(got))
            return None
        arm("mut-hand-population", "KL_pp_shadow", None, True, script=mut,
            check=hand_pop_detected)
    finally:
        os.unlink(mut)

    # Arm 32. [R0] round two's plant: cd "$rundir" -> cd "$R", restoring the
    # launch-directory dependency #245 exists to kill. The yosys model
    # refuses to run anywhere but an exclusive per-top dir under $OOC_TMP.
    # The anchor tracks ooc.sh's text and moved when the allocator preload was
    # applied inside this subshell (#290). The mutation is unchanged in meaning:
    # it still runs the synthesis somewhere other than the exclusive per-top
    # directory, and must still be caught.
    mut = _mutant(r'\(cd "\$rundir" && apply_malloc_env',
                  '(cd "$R" && apply_malloc_env', "cwd-escape")
    try:
        arm("mut-cwd-escape", "tcam", "YOSYS-WRONG-CWD", False, script=mut)
    finally:
        os.unlink(mut)

    # ---- the geometry parser ([R0] round two, finding 3) -----------------

    def pkg_mutant(pkg_text, label):
        fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
        _track(pkg)
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
    _track(pkg)
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

    # The gPTP ROM geometry is independently sourced from its owning package.
    # A changed live width must invalidate the current 48-bit image.
    fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-gptp-pkg-")
    _track(pkg)
    with os.fdopen(fd, "w") as fh:
        fh.write("localparam int unsigned UCODE_W_C = 52;\n"
                 "localparam int unsigned UPC_W_C = 10;\n")
    mut = _mutant(
        r'GPTP_UCODE_W=\$\(pkg_num "\$GPTP_UCPU_PKG" UCODE_W_C\) \|\| exit 2',
        'GPTP_UCODE_W=$(pkg_num "%s" UCODE_W_C) || exit 2' % pkg,
        "gptp-pkg-width-52")
    try:
        arm("gptp-width-live-package", "tcam", "not exactly 13 hex digits",
            False, script=mut)
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # ---- consumption custody ([R0] round four) ---------------------------

    PLANTS = [
        ("ucode.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/ucode.hex"',
         "ucode.hex changed after publication"),
        ("ucode.hex", "delete", 'rm -f "$OOC_TMP/ucode.hex"',
         "ucode.hex is gone from"),
        ("ltn_rom.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/ltn_rom.hex"',
         "ltn_rom.hex changed after publication"),
        ("ltn_rom.hex", "delete", 'rm -f "$OOC_TMP/ltn_rom.hex"',
         "ltn_rom.hex is gone from"),
        ("gptp_ucode.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/gptp_ucode.hex"',
         "gptp_ucode.hex changed after publication"),
        ("gptp_ucode.hex", "delete", 'rm -f "$OOC_TMP/gptp_ucode.hex"',
         "gptp_ucode.hex is gone from"),
    ]

    # Arms 39-42. The published image swapped or deleted immediately AFTER
    # publication (sv2v runs between publication and the first consumption:
    # the reviewer's exact seam). The consuming copy's re-hash must refuse,
    # and no row may print.
    for img, mode, act, want in PLANTS:
        arm("%s-%s-after-publication" % (img.split(".")[0], mode), "tcam",
            want, False, sv2v=sv2v_plant("tcam", act),
            check=lambda log, t, h: None if row_of(log) is None
            else "a row was priced from unvouched bytes")

    # Arms 43-46. The same four plants BETWEEN two requested tops: the
    # first, unaffected top prices and keeps its row; the second must
    # refuse rather than consume the changed/missing image.
    def between_check(log, ooc_tmp, home):
        if row_of(log, "tcam") is None:
            return "the first (unaffected) top printed no row"
        if row_of(log, "KL_pcm_lpf") is not None:
            return "the second top was priced from unvouched bytes"
        return None
    for img, mode, act, want in PLANTS:
        arm("%s-%s-between-tops" % (img.split(".")[0], mode),
            ["tcam", "KL_pcm_lpf"], want, False,
            sv2v=sv2v_plant("KL_pcm_lpf", act), check=between_check)

    # Arm 47. The consuming copy corrupted DURING the run (the model's own
    # exit trap): the post-run re-hash must discard whatever was measured.
    arm("ucode-corrupt-mid-run", "tcam", "changed under", False,
        yosys=YOSYS_CORRUPT_MIDRUN,
        check=lambda log, t, h: None if row_of(log) is None
        else "a row survived a mid-run byte change")

    # Arm 48. Consumption moved back to the SHARED published directory
    # (cd "$rundir" -> cd "$TMP"): the yosys model refuses $OOC_TMP itself,
    # so the exclusive-run-dir contract cannot silently regress.
    # Same anchor move as arm 47 (#290); the mutation is unchanged in meaning.
    mut = _mutant(r'\(cd "\$rundir" && apply_malloc_env',
                  '(cd "$TMP" && apply_malloc_env', "consume-shared-dir")
    try:
        arm("mut-consume-shared-dir", "tcam", "YOSYS-WRONG-CWD", False,
            script=mut)
    finally:
        os.unlink(mut)

    # Arm 49. BOTH script-side re-hashes blinded (copy_matches always
    # true) plus the swap plant: the model's exact-byte ledger oracle is
    # the last line of defense and must go red on its own.
    mut = _mutant(r'\[ "\$got" = "\$\{ROM_SHA\[\$2\]\}" \]', "true",
                  "blind-copy-hash")
    try:
        arm("mut-blind-copy-hash", "tcam", "YOSYS-IMAGE-BYTES", False,
            script=mut,
            sv2v=sv2v_plant("tcam",
                            'printf \'SWAPPED\\n\' > "$OOC_TMP/ucode.hex"'),
            check=lambda log, t, h: None if row_of(log) is None
            else "a row was priced from unvouched bytes")
    finally:
        os.unlink(mut)

    # Arm 50. chmod a-w dropped: the model refuses a writable consuming
    # copy, so immutability is held by an oracle, not a habit.
    mut = _mutant(r'chmod a-w "\$rundir/\$img"', ":", "writable-copy")
    try:
        arm("mut-writable-copy", "tcam", "YOSYS-IMAGE-WRITABLE", False,
            script=mut)
    finally:
        os.unlink(mut)

    # ---- the read-interval and the pin authority ([R0] round five) -------

    # Arm 51. The transient swap on the SHIPPING script: the locked run
    # directory must refuse the rename outright, and nothing may price.
    def swap_blocked(log, ooc_tmp, home):
        if row_of(log) is not None:
            return "a row was priced around a transient-swap attempt"
        if os.path.exists(os.path.join(ooc_tmp, "transient-swap-succeeded")):
            return "the reviewed image was moved aside despite the lock"
        return None
    arm("transient-swap-blocked", "tcam", "YOSYS-TRANSIENT-SWAP-BLOCKED",
        False, yosys=YOSYS_TRANSIENT_SWAP, check=swap_blocked)

    # Arm 52. The same swap on a mutant that FORGETS the directory lock:
    # the exploit must fully succeed - reviewed bytes moved aside, wrong
    # bytes priced, reviewed bytes restored, both script hashes green, rc
    # 0. This is the reviewer's reproduction as a permanent fixture: it
    # proves arm 51's refusal is the lock's doing, not the stub's.
    mut = _mutant(r'chmod u-w "\$rundir"', "true", "no-dir-lock-swap")
    try:
        def swap_succeeded(log, ooc_tmp, home):
            if row_of(log) is None:
                return "the unlocked mutant did not price the swapped bytes"
            if not os.path.exists(os.path.join(ooc_tmp,
                                               "transient-swap-succeeded")):
                return "the swap never happened, so this arm proves nothing"
            return None
        arm("mut-no-dir-lock-transient-swap", "tcam", None, True,
            yosys=YOSYS_TRANSIENT_SWAP, script=mut, check=swap_succeeded)
    finally:
        os.unlink(mut)

    # Arm 53. The same mutant under the honest model: every green arm's
    # oracle includes the writability refusal, so forgetting the lock is
    # red even when nobody attempts a swap.
    mut = _mutant(r'chmod u-w "\$rundir"', "true", "no-dir-lock-model")
    try:
        arm("mut-no-dir-lock", "tcam", "YOSYS-RUNDIR-WRITABLE", False,
            script=mut)
    finally:
        os.unlink(mut)

    # Arms 54-55. Every chmod status is TAKEN, guard by guard: a chmod that
    # fails must be a named FATAL, never an ignored hardening. `read-only`
    # alone matched three different messages (both ooc.sh guards and the
    # yosys model's own writability refusal), so dropping the a-w status
    # still left the arm green on the u-w guard's message.
    arm("chmod-a-w-status-taken", "tcam",
        "consuming copy of ucode.hex read-only", False, chmod=CHMOD_FAIL,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced with an unenforced permission")
    arm("chmod-u-w-status-taken", "tcam", "run directory read-only", False,
        chmod=CHMOD_FAIL_DIRLOCK,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced with an unlocked run directory")

    # Arms 55-56. A stale submodule checkout (the dispatching git answers a
    # planted HEAD) refuses against the superproject gitlink, in normal AND
    # record mode; record mode must leave the ledger untouched.
    arm("stale-checkout-refused", "tcam",
        "disagrees with the superproject pin", False, git=GIT_STALE_HEAD,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced from a stale checkout")
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "stale-record-ledger")
    try:
        def ledger_untouched(log, ooc_tmp, home):
            with open(os.path.join(ooc_tmp, "scratch-ledger.tsv")) as fh:
                if fh.read() != "# scratch\n":
                    return "record mode wrote rows for a stale checkout"
            return None
        arm("stale-checkout-record-refused", ["--record-rom-digests"],
            "disagrees with the superproject pin", False, script=mut,
            git=GIT_STALE_HEAD,
            setup=lambda t2: _write(t2, "scratch-ledger.tsv", "# scratch\n"),
            check=ledger_untouched)
    finally:
        os.unlink(mut)

    # The independently pinned gPTP processor has the identical authority:
    # neither normal nor record mode may certify a stale checkout.
    arm("stale-gptp-checkout-refused", "tcam",
        "gptp-processor checkout", False, git=GIT_STALE_GPTP_HEAD,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced from a stale gPTP checkout")
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "stale-gptp-record-ledger")
    try:
        def gptp_ledger_untouched(log, ooc_tmp, home):
            with open(os.path.join(ooc_tmp, "scratch-ledger.tsv")) as fh:
                if fh.read() != "# scratch\n":
                    return "record mode wrote rows for a stale gPTP checkout"
            return None
        arm("stale-gptp-checkout-record-refused",
            ["--record-rom-digests"], "gptp-processor checkout", False,
            script=mut, git=GIT_STALE_GPTP_HEAD,
            setup=lambda t2: _write(t2, "scratch-ledger.tsv", "# scratch\n"),
            check=gptp_ledger_untouched)
    finally:
        os.unlink(mut)

    # Arm 57. The round-five false green as a fixture: pin taken from the
    # CHECKOUT (the pre-round-five spelling) plus a ledger carrying rows
    # for the stale revision - the run prices a wrong processor tree with
    # every digest green. Proves the gitlink comparison is what stands
    # between a stale checkout and a valid-looking figure.
    stale_pin = "b2effce9" * 5
    gptp_pin = _processor_pins()["gptp-processor"]
    mut = _mutant2(
        r'PP_PIN=\$\(pp_pin_of_record\) \|\| exit 2',
        'PP_PIN=$(git -C "$R/protocol-processor" rev-parse HEAD) || exit 2',
        r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
        'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
        "pin-from-checkout")
    try:
        def stale_priced(log, ooc_tmp, home):
            if row_of(log) is None:
                return "the checkout-keyed mutant did not price, so this " \
                       "arm proves nothing about the gitlink comparison"
            return None
        arm("mut-pin-from-checkout-false-green", "tcam", None, True,
            script=mut, git=GIT_STALE_HEAD,
            setup=lambda t2: _write(
                t2, "scratch-ledger.tsv",
                "".join("%s\t%s\t%s\n" %
                        (gptp_pin if img == "gptp_ucode.hex" else stale_pin,
                         img, sha)
                        for img, sha in sorted(ledger().items()))),
            check=stale_priced)
    finally:
        os.unlink(mut)

    if ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), this "
                        "file declares %d." % (ran, ARMS))
    return problems, ran


def main() -> int:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        print("ooc.sh refusal self-test: REFUSED - this suite's custody "
              "oracles are mode bits (`test -w`, rename in a u-w directory), "
              "and root bypasses every one of them: the locked run directory "
              "reads as writable and the transient swap succeeds, so the "
              "arms would invert rather than fail. Run it unprivileged.",
              file=sys.stderr)
        return 2
    try:
        bad, ran = selftest()
    except AssertionError as e:
        print("ooc.sh refusal self-test: SETUP REFUSED - %s" % e,
              file=sys.stderr)
        return 2
    for b in bad:
        print("  -", b, file=sys.stderr)
    if bad:
        return 2
    print("ooc.sh refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())
