#!/usr/bin/env python3
"""usage: par.py <out> <spinners> <M per tree> <rounds> <lifecycle|suite|shadow> <budget s>
Scratch only. Each round starts M copies of the test in the before tree and M in the after tree at the same moment, under make -j spinners,
in this unit's own CPU affinity at normal niceness. One log and one rc per run. No run is started after the budget is spent."""
import json, os, signal, subprocess, sys, time
from pathlib import Path
out, spinners, m, rounds, test, budget = sys.argv[1:7]
out = Path(out); spinners, m, rounds, budget = int(spinners), int(m), int(rounds), float(budget)
S = Path("$VALIDATION_STORAGE/833-a726")
TREES = {"before": S / "wt-before", "after": S / "wt-after"}
def argv(tree, i):
    if test == "lifecycle":
        return ["make", "--no-print-directory", "-C", "tb/verilator/gptp_shadow", "lifecycle"], tree
    if test == "suite":
        return ["python3", "scripts/test_suite_cancellation.py"], tree
    raise SystemExit("unknown test")
env = dict(os.environ, TMPDIR=str(S / "tmp"), PYTHONDONTWRITEBYTECODE="1")
env.pop("MAKEFLAGS", None)
load = None
if spinners:
    load = subprocess.Popen(["make", "-s", "-j", str(spinners), "-C", str(S / "load"), f"N={spinners}"], start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
start = time.monotonic()
try:
    for r in range(rounds):
        if time.monotonic() - start >= budget:
            print("budget spent before round", r); break
        procs = []
        began = time.monotonic()
        loadavg = Path("/proc/loadavg").read_text().strip()
        for name, tree in TREES.items():
            for i in range(m):
                d = out / name; d.mkdir(parents=True, exist_ok=True)
                existing = sorted(int(p.stem) for p in d.glob("*.rc"))
                n = (existing[-1] + 1 if existing else 0) + i
                a, cwd = argv(tree, i)
                f = (d / f"{n:03d}.log").open("w")
                head = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
                f.write(f"# tree {name} head {head} spinners {spinners} concurrent {2*m} loadavg-before {loadavg}\n# {' '.join(a)}\n"); f.flush()
                procs.append((name, n, subprocess.Popen(a, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL), f))
        for name, n, p, f in procs:
            rc = p.wait(); f.close()
            (out / name / f"{n:03d}.rc").write_text(f"{rc}\n")
        print(f"round {r}: {time.monotonic()-began:.0f}s load {Path('/proc/loadavg').read_text().split()[0]} rcs " + " ".join(f"{name[0]}{n}={p.returncode}" for name, n, p, f in procs), flush=True)
finally:
    if load is not None:
        os.killpg(load.pid, signal.SIGKILL); load.wait()
