#!/usr/bin/env python3
"""The whole scripts/test_suite_cancellation.py, 4 times each at the head and the prior head, 8 at once.

usage: python3 -I preflight_cost.py <clone> <packet>  (packet/scratch/base holds `git archive c1b29617 scripts`)
"""
import concurrent.futures, shutil, sys
from pathlib import Path
clone, packet = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts
from owned_process import OwnedProcesses
scratch = packet / "scratch/preflight"; shutil.rmtree(scratch, ignore_errors=True); scratch.mkdir()
trees = {"head-a67eaf66": pts.mutant_tree(scratch, "none"), "base-c1b29617": packet / "scratch/base"}
runs = [(n, i) for i in range(4) for n in trees]
print(open("/proc/loadavg").read().strip())
with OwnedProcesses():
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        res = list(pool.map(lambda r: (r, pts.run_mutant(trees[r[0]], None)), runs))
for (name, i), (status, secs, out) in res:
    print(name, i, "rc", status, f"{secs:.1f} s")
for name in trees:
    t = [s for (n, _i), (_st, s, _o) in res if n == name]
    print("MEAN", name, f"{sum(t)/len(t):.1f} s over {len(t)}", "all rc 0:", all(st == 0 for (n, _i), (st, _s, _o) in res if n == name))
print(open("/proc/loadavg").read().strip())
