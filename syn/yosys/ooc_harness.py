#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The models and the machinery one arm of the ooc.sh self-test runs on.

Everything here is the fixture, never a test: the pinned digest ledger the
images are checked against, the planted `sv2v`, `yosys`, `git`, `awk` and
`chmod` the run resolves through PATH, the mutated copies of ooc.sh, and the
`Arm` record plus the `Suite` that runs one and records what it failed to
prove. The arms themselves are `ooc_arms.py`; what the suite is FOR, and its
exit status, are `ooc_selftest.py`.

THE STUBS ARE MODELS WITH TEETH, not silence - each one is documented at its
own definition below, and `ooc_selftest.py`'s docstring says what the set of
them proves.
"""
import atexit
import dataclasses
import functools
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


#: Read LAZILY, and once: at module scope this ran before main() could catch
#: anything, so an uninitialised submodule or an unrecorded pin reached the
#: operator as a CalledProcessError traceback rather than as the sentence
#: ooc.sh itself prints for the same condition. The cache is the decorator's,
#: so nothing here rebinds a module global to memoise; a raised AssertionError
#: is not cached, and the next caller asks again.
@functools.lru_cache(maxsize=None)
def ledger():
    return _ledger_digests()


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
  echo "ERROR: YOSYS-RUNDIR-WRITABLE: $(pwd -P) accepts renames, so the" \
       "consuming copies are not immutable for the read interval"
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
    echo "ERROR: YOSYS-IMAGE-BYTES: $img in $(pwd -P) hashes" \
         "${got:-nothing}, the validated ledger digest is ${want:-unset}"
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
#: The honest model plus a record of the allocator it ran under (#290): the
#: preload is applied INSIDE the per-top subshell, so this is the only place
#: that can testify whether it reached yosys - and the sv2v twin below is the
#: only place that can testify it did NOT reach the front end.
YOSYS_ENV = YOSYS_TMPL.replace("@PLANT@",
    'printf \'%s\\n\' "${LD_PRELOAD-<unset>}" >> "$HOME/yosys-env.txt"')
SV2V_ENV = SV2V_OK.replace('exit 0\n',
    'printf \'%s\\n\' "${LD_PRELOAD-<unset>}" >> "$HOME/sv2v-env.txt"\nexit 0\n')


def _preloadable_library():
    """A shared object the loader will preload into any process, for the
    allocator-scoping arms: libc itself, which every dynamically linked
    process already maps. None when no such library can be found or the
    loader complains about it (a static or exotic toolchain).

    CANONICAL, the way select_malloc hands it on: an explicit YOSYS_MALLOC
    goes through abs_path (readlink -f) before it reaches the yosys child
    and the header line, and arm 73 compares both against this value. On a
    merged-/usr layout ldconfig answers `/lib/<triplet>/libc.so.6` while the
    loader is given `/usr/lib/<triplet>/libc.so.6` - the two spellings
    disagreed on the hosted runner and agreed only on a host whose ldconfig
    already speaks the canonical path."""
    cands = []
    try:
        out = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
        cands += [ln.rsplit("=> ", 1)[1].strip() for ln in out.stdout.splitlines()
                  if "libc.so.6" in ln and "=> " in ln]
    except OSError:
        pass
    # ldconfig answers for multiarch layouts; the literal list is only the
    # fallback for a machine whose ldconfig a normal user cannot run.
    cands += ["/usr/lib/libc.so.6", "/lib64/libc.so.6", "/usr/lib64/libc.so.6"]
    true_bin = shutil.which("true")
    for c in cands:
        if not (os.path.isfile(c) and true_bin):
            continue
        c = os.path.realpath(c)
        env = dict(os.environ, LD_PRELOAD=c)
        r = subprocess.run([true_bin], env=env, capture_output=True, text=True)
        if r.returncode == 0 and not r.stderr:
            return c
    return None
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
echo "ERROR: YOSYS-TRANSIENT-SWAP-BLOCKED: the run directory refused the" \
     "rename, so the reviewed bytes cannot be moved aside for the read interval"
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


@functools.lru_cache(maxsize=None)
def pp_population():
    """The authoritative processor population plus the parent's named files:
    what a KL_pp_shadow elaboration must consume, from pp_srcs.py itself.
    Asked once per run, and memoised by the decorator rather than by a global
    the function rebinds."""
    out = subprocess.run(
        [REAL_PYTHON, os.path.join(REPO, "scripts", "pp_srcs.py"),
         "--prefix", os.path.join(REPO, "protocol-processor", "hdl")],
        capture_output=True, text=True, check=True)
    pop = out.stdout.split()
    pop += [os.path.join(REPO, "third_party", "verilog-axis", "rtl",
                         "axis_fifo.v"),
            os.path.join(REPO, "hdl", "milan", "KL_pp_shadow.sv"),
            os.path.join(REPO, "hdl", "milan", "KL_pp_maap_shim.sv")]
    return sorted(pop)


def _read_text(path):
    """The whole text of one file, the handle closed before it returns."""
    with open(path) as fh:
        return fh.read()


def _stub(bindir, name, content):
    p = os.path.join(bindir, name)
    with open(p, "w") as fh:
        fh.write(content)
    os.chmod(p, 0o755)


def _run(script, tops, home, rundir, ooc_tmp, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        for k, v in extra_env.items():
            if v is None:
                env.pop(k, None)
            else:
                env[k] = v
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


@dataclasses.dataclass
class Arm:
    """One planted run of ooc.sh: what is planted, and what must come back.

    A record and not fourteen parameters, so that a call site names every
    plant it makes and inherits the honest model for every plant it does not.
    The four leading fields are the arm itself -- what it is called, which
    tops it asks for, the text a refusal must NAME, and whether this is a
    positive arm; everything after them is a seam of the real script the arm
    rides: the four PATH stubs, the mutated copy of ooc.sh to run instead of
    the tracked one, the state to pre-plant in $OOC_TMP, the environment, and
    the check that reads the log afterwards.
    """

    name: str
    tops: object
    want: object
    expect_rc0: bool
    sv2v: str = SV2V_OK
    yosys: str = YOSYS_OK
    py: object = None
    awk: object = None
    git: object = None
    chmod: object = None
    script: str = OOC
    setup: object = None
    check: object = None
    env: object = None


class Suite:
    """The arms' shared verdict: what failed, and how many arms ran."""

    def __init__(self):
        self.problems = []
        self.ran = 0

    def run(self, a):
        """Run one arm, appending to `problems` whatever it failed to prove."""
        self.ran += 1
        problems = self.problems
        name = a.name
        tops = [a.tops] if isinstance(a.tops, str) else a.tops
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            if a.setup:
                os.makedirs(ooc_tmp, exist_ok=True)
                a.setup(ooc_tmp)
            _stub(bindir, "sv2v", a.sv2v)
            _stub(bindir, "yosys", a.yosys)
            if a.py:
                _stub(bindir, "python3",
                      PY_DISPATCH % {"target": a.py[0], "action": a.py[1],
                                     "real": REAL_PYTHON})
            if a.awk:
                _stub(bindir, "awk", a.awk % {"real": REAL_AWK})
            if a.git:
                _stub(bindir, "git", a.git % {"real": REAL_GIT})
            if a.chmod:
                _stub(bindir, "chmod", a.chmod % {"real": REAL_CHMOD})
            rc, log = _run(a.script, tops, home, rundir, ooc_tmp, a.env)
            litter = os.listdir(rundir)
            if a.expect_rc0:
                if rc != 0:
                    problems.append("SELF-TEST FAILED [%s]: a well-formed run "
                                    "must exit 0, got rc=%d\n%s"
                                    % (name, rc, log.strip()))
                    return
            elif rc == 0 or a.want not in log:
                problems.append("SELF-TEST FAILED [%s]: expected a non-zero "
                                "exit naming %r, got rc=%d\n%s"
                                % (name, a.want, rc, log.strip()))
                return
            if litter:
                problems.append("SELF-TEST FAILED [%s]: the run littered the "
                                "caller's directory with %s (the #191/#192 "
                                "rule)" % (name, litter))
                return
            if a.check:
                miss = a.check(log, ooc_tmp, home)
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
