#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe: exercise every clause of fixture_guards.main()'s docstring
against stub tools, at BASE and at HEAD, and require identical behaviour.

Usage: contract_probes.py PP_BASE_CHECKOUT PP_HEAD_CHECKOUT WORKDIR

Each scenario runs `python3 <checkout>/tb/pp_top/fixture_guards.py ...` in a
fresh directory under WORKDIR with a stub Verilator and a stub C++ compiler
(written by this script). The stub compiler is locale-sensitive: it prints the
English static-assertion diagnostics only when LC_ALL=C, and French ones
otherwise, so a scenario run with the caller at LC_ALL=fr_FR.UTF-8 passes only
if the compiler really receives LC_ALL=C. Both stubs log argv and LC_ALL.

Compared between BASE and HEAD: exit status, stdout bytes, stub logs, and the
final exception line (temporary-directory names normalised). Traceback line
numbers are not compared: HEAD's docstring shifts main()'s body by 10 lines.
Exit 0 when every scenario matches its docstring expectation at both revisions
and BASE == HEAD for every scenario; 1 otherwise.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

WIRE = "SRP VID fixture must differ from product default 2 in the 16-bit wire value"
CLASS_D = "SRP VID fixture must differ from product default 2 in the 12-bit class-D value"

STUB_VERILATOR = r'''#!/usr/bin/env python3
import os, sys
log = os.environ["STUB_LOG"]
mode = os.environ.get("STUB_VERILATOR_MODE", "ok")
with open(log, "a") as fh:
    fh.write("verilator LC_ALL=%r argv=%r\n" % (os.environ.get("LC_ALL"),
             [a if not a.startswith(os.environ.get("TMPDIR", "/tmp") + "/pp-top-vid-guards-") else "<TMP>"
              for a in sys.argv[1:]]))
if sys.argv[1:] == ["--getenv", "VERILATOR_ROOT"]:
    if mode == "getenv-fail":
        sys.exit(3)
    print("/stub/verilator-root")
    sys.exit(0)
sys.exit(4 if mode == "model-fail" else 0)
'''

STUB_CXX = r'''#!/usr/bin/env python3
import os, sys
WIRE = %r
CLASS_D = %r
log = os.environ["STUB_LOG"]
mode = os.environ.get("STUB_CXX_MODE", "correct")
define = [a for a in sys.argv[1:] if a.startswith("-DPP_TOP_SRP_DOM_DEF_VID=")]
value = define[0].split("=0x")[1] if define else None
with open(log, "a") as fh:
    fh.write("cxx LC_ALL=%%r value=%%r argv_tail=%%r\n" %% (os.environ.get("LC_ALL"), value,
             [a for a in sys.argv[1:] if not a.startswith("-I")]))
english = os.environ.get("LC_ALL") == "C"
def diag(msg):
    if english:
        return "sim_main.cpp:1:1: error: static assertion failed: " + msg
    return "sim_main.cpp:1:1: erreur: l'assertion statique a echoue: " + msg
expected = {None: [], "5A3C": [], "0002": [WIRE, CLASS_D], "1002": [CLASS_D]}[value]
if mode == "always-ok":
    sys.exit(0)
if mode == "wire-only" and value == "0002":
    expected = [WIRE]
lines = [diag(m) for m in expected]
if mode == "extra-error" and value == "0002":
    lines.append("sim_main.cpp:2:1: error: unrelated failure")
if mode == "error-on-5A3C" and value == "5A3C":
    lines.append("sim_main.cpp:2:1: error: unrelated failure")
for line in lines:
    print(line)
sys.exit(1 if lines else 0)
''' % (WIRE, CLASS_D)

# name -> (extra argv before --, verilator mode, cxx mode, caller LC_ALL, expectation)
SCENARIOS = {
    "S01-all-pass-caller-french": ("ok", "correct", "fr_FR.UTF-8", "exit0"),
    "S02-all-pass-caller-unset": ("ok", "correct", None, "exit0"),
    "S03-compiler-always-succeeds": ("ok", "always-ok", None, "exit1"),
    "S04-unrelated-error-on-5A3C": ("ok", "error-on-5A3C", None, "exit1"),
    "S05-0002-wire-diagnostic-only": ("ok", "wire-only", None, "exit1"),
    "S06-0002-extra-unrelated-error": ("ok", "extra-error", None, "exit1"),
    "S07-root-query-fails": ("getenv-fail", "correct", None, "CalledProcessError"),
    "S08-model-generation-fails": ("model-fail", "correct", None, "CalledProcessError"),
    "S09-verilator-absent": ("absent", "correct", None, "FileNotFoundError"),
    "S10-compiler-absent": ("ok", "absent", None, "FileNotFoundError"),
    "S11-no-double-dash": ("ok", "correct", None, "record"),
    "S12-help": ("ok", "correct", None, "record"),
}


def run(checkout: Path, work: Path, name: str) -> dict:
    """Run one scenario against one checkout and collect its observables."""
    vmode, cmode, lc_all, _ = SCENARIOS[name]
    case = work / name
    shutil.rmtree(case, ignore_errors=True)
    case.mkdir(parents=True)
    tools = case / "tools"
    tools.mkdir()
    (tools / "verilator").write_text(STUB_VERILATOR)
    (tools / "cxx").write_text(STUB_CXX)
    (tools / "verilator").chmod(0o755)
    (tools / "cxx").chmod(0o755)
    log = case / "stub.log"
    log.write_text("")
    env = {"PATH": os.environ["PATH"], "STUB_LOG": str(log),
           "STUB_VERILATOR_MODE": vmode, "STUB_CXX_MODE": cmode,
           "LANG": "fr_FR.UTF-8", "TMPDIR": "/tmp"}
    if lc_all is not None:
        env["LC_ALL"] = lc_all
    verilator = str(tools / "verilator") if vmode != "absent" else str(tools / "no-such-verilator")
    cxx = (str(tools / "cxx") + " --stub-driver-flag") if cmode != "absent" else str(tools / "no-such-cxx")
    script = str(checkout / "tb/pp_top/fixture_guards.py")
    if name == "S11-no-double-dash":
        argv = [script, "--verilator", verilator, "--cxx", cxx, "wrap.sv", "--cc"]
    elif name == "S12-help":
        argv = [script, "--help"]
    else:
        argv = [script, "--verilator", verilator, "--cxx", cxx, "--", "--cc", "-j", "0", "wrap.sv"]
    proc = subprocess.run([sys.executable, "-B", *argv], cwd=case, env=env,
                          capture_output=True, text=True)
    err = proc.stderr.strip().splitlines()
    last = err[-1] if err else ""
    last = re.sub(r"pp-top-vid-guards-[A-Za-z0-9_]+", "pp-top-vid-guards-<TMP>", last)
    last = last.replace(str(tools), "<TOOLS>")
    stub = re.sub(r"pp-top-vid-guards-[A-Za-z0-9_]+", "pp-top-vid-guards-<TMP>", log.read_text())
    stub = stub.replace(str(tools), "<TOOLS>")
    return {"exit": proc.returncode, "stdout": proc.stdout.replace(str(checkout), "<CHECKOUT>"),
            "stderr_last": last, "stub_log": stub}


def meets(name: str, obs: dict) -> bool:
    """Docstring expectation for one scenario's observables."""
    want = SCENARIOS[name][3]
    if want == "exit0":
        return (obs["exit"] == 0 and obs["stdout"].endswith("fixture guards: 4 cases PASS\n")
                and obs["stub_log"].count("cxx LC_ALL='C'") == 4
                and "verilator LC_ALL='C'" not in obs["stub_log"])
    if want == "exit1":
        return obs["exit"] == 1 and "FAIL: fixture" in obs["stdout"] and obs["stderr_last"] == ""
    if want in ("CalledProcessError", "FileNotFoundError"):
        return obs["exit"] == 1 and want in obs["stderr_last"]
    return True


def main() -> int:
    """Run every scenario at both checkouts; 0 = docstring met and BASE == HEAD."""
    base, head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    ok = True
    report = {}
    for name in SCENARIOS:
        b = run(base, work / "base", name)
        h = run(head, work / "head", name)
        same = b == h
        met = meets(name, b) and meets(name, h)
        ok = ok and same and met
        report[name] = {"expectation": SCENARIOS[name][3], "base_equals_head": same,
                        "expectation_met": met, "head": h,
                        **({} if same else {"base": b})}
        print(f"{name:34s} expect={SCENARIOS[name][3]:18s} exit={h['exit']} "
              f"met={met} base==head={same} | {h['stderr_last'][:110]}")
    (work / "contract-probes.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
