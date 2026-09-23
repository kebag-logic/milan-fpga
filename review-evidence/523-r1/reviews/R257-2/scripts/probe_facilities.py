#!/usr/bin/env python3
"""Independent reviewer probe: both production entry points on a host whose
process facilities are missing or refused, emulated with a sitecustomize
module loaded through PYTHONPATH before the entry runs.

Usage: probe_facilities.py CLONE SCRATCH OUTPUT_JSON

Modes differ from the author's arms: `pidfd-open-enosys` makes pidfd_open
raise ENOSYS (a seccomp-filtered container), `subreaper-eperm` makes only
PR_SET_CHILD_SUBREAPER fail, `pdeathsig-eperm` makes only PR_SET_PDEATHSIG
fail (inside the forked child). Every mode must print REFUSED, exit 2, show
no traceback and start no suite or mutation build.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SITE = r'''
import ctypes, errno, os, signal
mode = os.environ.get("PROBE_FACILITY")
if mode == "pidfd-open-enosys":
    def _enosys(*a, **k):
        raise OSError(errno.ENOSYS, "Function not implemented")
    os.pidfd_open = _enosys
elif mode in ("subreaper-eperm", "pdeathsig-eperm"):
    _real = ctypes.CDLL(None, use_errno=True)
    fail = 36 if mode == "subreaper-eperm" else 1
    class _Lib:
        def prctl(self, option, *rest):
            if option == fail:
                ctypes.set_errno(errno.EPERM)
                return -1
            return _real.prctl(option, *rest)
    _lib = _Lib()
    ctypes.CDLL = lambda *a, **k: _lib
'''

def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    (scratch / "site").mkdir()
    (scratch / "site/sitecustomize.py").write_text(SITE)
    results = []
    for mode in ("pidfd-open-enosys", "subreaper-eperm", "pdeathsig-eperm"):
        for entry in ("sweep", "campaign"):
            control = scratch / f"{entry}-{mode}"
            control.mkdir()
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(PYTHONPATH=str(scratch / "site"), PROBE_FACILITY=mode, PROBE_CONTROL=str(control),
                       TMPDIR=str(control), PYTHONDONTWRITEBYTECODE="1")
            if entry == "sweep":
                argv = ["bash", str(clone / "scripts/run_all_suites.sh"), str(control / "logs"), "--list"]
            else:
                argv = [sys.executable, str(clone / "tb/verilator/gptp_shadow/mutants.py")]
            done = subprocess.run(argv, cwd=control, env=env, capture_output=True, text=True, timeout=120)
            text = done.stdout + done.stderr
            rec = {"entry": entry, "mode": mode, "exit": done.returncode, "refused": "REFUSED" in text,
                   "traceback": "Traceback" in text, "listed_or_started": bool(done.stdout.strip()) if entry == "sweep"
                   else any(control.glob("gptp-shadow-mutants-*")), "text": text[-400:]}
            results.append(rec)
            print(f"{entry:8s} {mode:18s} exit={rec['exit']} refused={rec['refused']} traceback={rec['traceback']} "
                  f"started={rec['listed_or_started']} :: {text.strip().splitlines()[-1][:110] if text.strip() else ''}")
    output.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
