#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/yosys/ooc.sh's refusals, automatically, on planted failures.

That script's exit status is the gate (#245): a top that fails sv2v or yosys,
a ROM generator that fails or emits an empty image, and a requested top that
matches nothing must each leave a non-zero exit. Before #245 the failure
branches printed and `continue`d, so the script's exit code was whatever its
last cleanup statement left behind: always 0, however many tops died -- and
`ucode.hex` was never generated at all, so `KL_pp_shadow` and `milan_datapath`
could not synthesize without a hand-planted image in the run directory.

WHAT IT RUNS IS THE REAL ooc.sh, not a copy of its logic. The plants ride two
seams the script already has: it resolves `sv2v`, `yosys` and `python3`
through PATH after prepending `$HOME/.local/bin`, so each arm runs it with
HOME pointing at a scratch directory whose `.local/bin` carries the planted
tool (the same directory is also put first on PATH directly, so the arm does
not depend on the prepend surviving). The ROM generators and
scripts/pp_srcs.py run for real through a dispatching `python3` stub, so the
generation path the positive arm proves is the shipping one. Real synthesis is
NOT run here: the positive arm proves the plumbing reaches a row at exit 0,
and the real-toolchain run is recorded on the PR that lands a change.

    python3 syn/yosys/ooc_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/ooc_tcl_selftest.py.
Needs the protocol-processor submodule (pp_srcs.py and both ROM generators
read it); it does not need yosys or sv2v.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OOC = os.path.join(HERE, "ooc.sh")
REAL_PYTHON = shutil.which("python3") or sys.executable

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 7

OK_TOOL = "#!/bin/sh\nexit 0\n"
SV2V_FAIL = "#!/bin/sh\necho 'planted sv2v failure' >&2\nexit 1\n"
YOSYS_FAIL = ("#!/bin/sh\necho 'ERROR: planted yosys elaboration failure'\n"
              "exit 1\n")

#: python3 dispatcher: fail, or truncate the -o target, when the invoked
#: script matches; hand everything else (pp_srcs.py, the other generator) to
#: the real interpreter, so all arms exercise the shipping generation path.
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


def _py_stub(bindir, target, action):
    _stub(bindir, "python3",
          PY_DISPATCH % {"target": target, "action": action,
                         "real": REAL_PYTHON})


def _run(top, home, rundir, ooc_tmp):
    env = dict(os.environ)
    bindir = os.path.join(home, ".local", "bin")
    env["HOME"] = home
    env["PATH"] = bindir + os.pathsep + env.get("PATH", "")
    env["OOC_TMP"] = ooc_tmp
    out = subprocess.run([OOC, top], cwd=rundir, env=env,
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def selftest():
    problems, ran = [], 0

    def arm(name, top, want, expect_rc0, sv2v=OK_TOOL, yosys=OK_TOOL,
            py=None, check=None):
        nonlocal ran
        ran += 1
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            _stub(bindir, "sv2v", sv2v)
            _stub(bindir, "yosys", yosys)
            if py:
                _py_stub(bindir, *py)
            rc, log = _run(top, home, rundir, ooc_tmp)
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

    # Arm 1. ANTI-VACUITY. With every tool succeeding, the run must exit 0,
    # print the requested row, and have generated BOTH control-plane ROMs
    # (by the real generators) into its own tmp dir -- never the caller's.
    def clean_checks(log, ooc_tmp):
        if "\ntcam" not in log:
            return "no row printed for the requested top"
        for img in ("ltn_rom.hex", "ucode.hex"):
            p = os.path.join(ooc_tmp, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run's tmp dir" % img
        return None
    arm("clean", "tcam", None, True, check=clean_checks)

    # Arm 2. A yosys failure must fail the SCRIPT, naming the top and the
    # error, not just print a row-shaped apology and exit 0 (#245's headline).
    arm("yosys-fail", "tcam", "planted yosys elaboration failure", False,
        yosys=YOSYS_FAIL,
        check=lambda log, t: None if "yosys FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 3. Same for the sv2v front end.
    arm("sv2v-fail", "tcam", "planted sv2v failure", False, sv2v=SV2V_FAIL,
        check=lambda log, t: None if "sv2v FAIL" in log
        else "the failure branch did not name the phase")

    # Arm 4. The microcode generator's exit status is taken, not `|| true`d:
    # a dead generator stops the run before any top is priced.
    arm("ucode-generator-fail", "tcam", "gen_ucode.py", False,
        py=("gen_ucode.py",
            "echo 'planted ucode generator failure' >&2\n  exit 3"),
        check=lambda log, t: None if "\ntcam" not in log
        else "a top was priced after the generator failed")

    # Arm 5. Present and zero bytes is the same refusal: `$readmemh` of an
    # empty image is an all-zero ROM and a wrong number, not an error.
    arm("ucode-empty", "tcam", "ucode.hex is empty", False,
        py=("gen_ucode.py", ": > \"$out\"\n  exit 0"))

    # Arm 6. The transition-ROM generator gets the identical treatment; its
    # status was discarded by the same `|| true` (#245).
    arm("ltn-generator-fail", "tcam", "gen_ltn_rom.py", False,
        py=("gen_ltn_rom.py",
            "echo 'planted ltn generator failure' >&2\n  exit 3"))

    # Arm 7. A requested top the list does not carry is a refusal, not an
    # empty header at exit 0.
    arm("unknown-top", "laneA_no_such_top", "unknown top", False)

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
