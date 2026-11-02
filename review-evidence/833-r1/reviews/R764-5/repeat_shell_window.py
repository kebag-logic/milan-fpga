#!/usr/bin/env python3
"""owner_shell_window 6 times each, 16 at once: head, two window mutants, and the prior head's tree.

usage: python3 -I repeat_shell_window.py <clone> <packet>  (packet/scratch/base holds `git archive c1b29617 scripts`)
The prior head has no --control option, so its runs are its whole test.
"""
import concurrent.futures, sys, time, subprocess
from pathlib import Path
clone, packet = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts
from owned_process import OwnedProcesses
trees = {}
scratch = packet / "scratch/repeat"; import shutil; shutil.rmtree(scratch, ignore_errors=True); scratch.mkdir()
for name in ("none", "shell-window-one-pass", "shell-window-1s"):
    trees[name] = pts.mutant_tree(scratch, name)
trees["base-c1b29617"] = packet / "scratch/base"
runs = [(n, i) for n in trees for i in range(6)]
with OwnedProcesses():
    with concurrent.futures.ThreadPoolExecutor(16) as pool:
        res = list(pool.map(lambda r: (r, pts.run_mutant(trees[r[0]], "owner_shell_window")), runs))
summary = {}
for (name, i), (status, secs, out) in res:
    last = [l for l in out.splitlines() if l.strip()][-1:]
    print(name, i, "rc", status, f"{secs:.1f} s", last[0][:160] if last else "")
    summary.setdefault(name, []).append(status)
for name, st in summary.items():
    print("SUMMARY", name, "red", sum(1 for s in st if s), "of", len(st))
