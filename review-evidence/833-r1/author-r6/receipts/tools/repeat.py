#!/usr/bin/env python3
"""Run one owner control REPS times under each named mutant of a tree, JOBS at once.

usage: python3 -I -B repeat.py <tree> <control> <reps> <jobs> NAME...
Each run is the tree's own run_mutant() on a mutant_tree() copy. Prints every run and,
per mutant, how many runs were red and how many carried the mutant's words.
"""
import concurrent.futures
import sys
import tempfile
from pathlib import Path

tree, control, reps, jobs = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
names = sys.argv[5:]
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

print(open("/proc/loadavg").read().strip(), flush=True)
with tempfile.TemporaryDirectory(prefix="repeat-", dir="$VALIDATION_STORAGE/833-a726f") as scratch, OwnedProcesses():
    trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
    runs = [(name, i) for i in range(reps) for name in names]
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda run: (run, pts.run_mutant(trees[run[0]], control)), runs))
summary = {}
for (name, i), (status, seconds, output) in results:
    lines = [line for line in output.splitlines() if line.strip()]
    words = pts.MUTANTS[name][1]
    print(f"{name} {i} rc {status} {seconds:.1f} s: {lines[-1][:200] if lines else ''}", flush=True)
    red, worded, secs = summary.setdefault(name, [0, 0, []])
    summary[name][0] += bool(status)
    summary[name][1] += bool(status) and words in output
    secs.append(seconds)
for name, (red, worded, secs) in summary.items():
    print(f"SUMMARY {name}: red {red} of {len(secs)}, with its words {worded}, "
          f"{min(secs):.1f}-{max(secs):.1f} s", flush=True)
print(open("/proc/loadavg").read().strip(), flush=True)
