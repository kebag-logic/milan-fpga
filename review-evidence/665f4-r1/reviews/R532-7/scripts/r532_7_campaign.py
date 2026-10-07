#!/usr/bin/env python3
"""R532-7: the head's complete SRP plant campaign, sharded across worker processes.

usage: r532_7_campaign.py ROOT LWSRP OUT JOBS IFS
ROOT is an exported head tree. Each worker plants one srp_mutants.DEFECTS entry in
its own copy of ROOT's sw/firmware/ctrl, exactly as srp_mutants.campaign() does,
builds the named suite at IFS interfaces, and grades with srp_mutants.caught().
Prints one "[ok|ESCAPED] name" line per plant; rc 0 only if every plant is caught.
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, lwsrp, out, jobs, ifs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
WORKER = r'''
import shutil, sys
from pathlib import Path
root, lwsrp, out, index, ifs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import srp_mutants, fw_gtest
from ctrl_build import CTRL, Tree, Refusal
from srp_arms import arm_srp
d = srp_mutants.DEFECTS[index]
src = out / "ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
target = src / d.path
text = target.read_text()
if text.count(d.old) != 1:
    print(f"[ESCAPED] {d.name}: {text.count(d.old)} planting sites"); sys.exit(1)
target.write_text(text.replace(d.old, d.new))
selected = d.test if "." in d.test else "Srp." + d.test
try:
    r = arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=1)), lwsrp, ifs, debug=d.debug,
                test=(d.suite, selected))
except Refusal as e:
    print(f"[ESCAPED] {d.name}: {e}"); sys.exit(1)
(out / "result.log").write_text(r.log)
ok = srp_mutants.caught(selected, d.needle, r)
print(f"[{'ok' if ok else 'ESCAPED'}] {d.name}: {d.test} / {d.needle}")
sys.exit(0 if ok else 1)
'''
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import srp_mutants
n = len(srp_mutants.DEFECTS)
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def one(i):
    o = out / f"{i:03d}"
    if o.exists():
        shutil.rmtree(o)
    o.mkdir(parents=True)
    r = subprocess.run([sys.executable, "-B", "-c", WORKER, str(root), str(lwsrp), str(o), str(i), str(ifs)],
                       env=env, capture_output=True, text=True)
    line = (r.stdout.strip().splitlines() or [f"[ESCAPED] #{i}: no verdict {r.stderr[-300:]}"])[-1]
    shutil.rmtree(o / "ctrl", ignore_errors=True)
    shutil.rmtree(o / "build", ignore_errors=True)
    return i, r.returncode, line


with cf.ThreadPoolExecutor(jobs) as pool:
    rows = sorted(pool.map(one, range(n)))
for i, rc, line in rows:
    print(line)
bad = [line for _, rc, line in rows if rc]
print(f"SRP campaign IF={ifs}: {n - len(bad)}/{n} caught")
sys.exit(1 if bad else 0)
