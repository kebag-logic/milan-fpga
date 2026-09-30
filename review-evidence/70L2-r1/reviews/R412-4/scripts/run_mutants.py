#!/usr/bin/env python3
"""run_mutants.py <packet> <base-gtree> <commit:mutant>...

One disposable tree per job (copied from base-gtree, a shared clone with its
submodules), checked out at <commit>, one census mutant applied, then gate
function test_baremetal_profile_contract() run alone. At most 8 jobs at once.
Writes mutants/<commit>_<mutant>.log and prints one line per job: RETURNED
(the gate function passed) or FAILED plus the first AssertionError line."""
import subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import os
P, G = Path(sys.argv[1]), Path(sys.argv[2])
TAG = os.environ.get("R412_TAG", "r")

def job(spec):
    commit, mid = spec.split(":")
    t = P / "scratch" / f"m_{TAG}_{commit}_{mid}"
    shutil.rmtree(t, ignore_errors=True)
    subprocess.run(["cp", "-a", str(G), str(t)], check=True)
    subprocess.run(["git", "-C", str(t), "checkout", "-q", "--detach", commit], check=True)
    subprocess.run([sys.executable, str(P / "scripts/census_mutants.py"), str(t), mid],
                   check=True, capture_output=True)
    log = P / "mutants" / f"{TAG}_{commit}_{mid}.log"
    subprocess.run(["timeout", os.environ.get("R412_TIMEOUT", "560"), str(P / "scripts/run_gate.sh"), str(t), str(log)],
                   capture_output=True)
    text = log.read_text(errors="replace")
    if "R412 GATE FUNCTION RETURNED" in text:
        return f"{commit} {mid}: RETURNED (gate function passed)"
    if "R412 STOP AFTER RESOLVED NOTE" in text:
        return f"{commit} {mid}: PASSED through gate 1b's resolved note (stop point)"
    last = [l for l in text.splitlines() if l.startswith("AssertionError")]
    return f"{commit} {mid}: FAILED :: {(last[-1] if last else text[-400:])[:900]}"

with ThreadPoolExecutor(max_workers=8) as ex:
    for line in ex.map(job, sys.argv[3:]):
        print(line, flush=True)
