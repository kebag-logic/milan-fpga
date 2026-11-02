#!/usr/bin/env python3
"""usage: loop.py <out dir> <spinners> <budget s> <max runs> <worktree> <lifecycle|suite|make-lifecycle|make-suite>

Runs one test repeatedly under make -j spinners inside this unit's own CPU affinity, at
normal niceness, one log and one rc per run. It starts no run after the budget is spent.
"""
import json, os, signal, subprocess, sys, time
from pathlib import Path

out, spinners, budget, runs, tree, test = sys.argv[1:7]
out = Path(out); out.mkdir(parents=True, exist_ok=True)
spinners, budget, runs = int(spinners), float(budget), int(runs)
tree = Path(tree)
HERE = Path(__file__).resolve().parent
COMMANDS = {
    "lifecycle": (["python3", "test_mutant_lifecycle.py"], tree / "tb/verilator/gptp_shadow"),
    "suite": (["python3", "scripts/test_suite_cancellation.py"], tree),
    "make-lifecycle": (["make", "--no-print-directory", "-C", "tb/verilator/gptp_shadow", "lifecycle"], tree),
    "make-suite": (["make", "--no-print-directory", "-C", "tb/verilator/gptp_shadow"], tree),
}
argv, cwd = COMMANDS[test]
env = dict(os.environ, TMPDIR="$VALIDATION_STORAGE/833-a726/tmp", PYTHONDONTWRITEBYTECODE="1")
load = None
if spinners:
    load = subprocess.Popen(["make", "-s", "-j", str(spinners), "-C", str(HERE), f"N={spinners}"],
                            start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
start = time.monotonic()
existing = sorted(int(p.stem) for p in out.glob("*.rc"))
index = existing[-1] + 1 if existing else 0
tally = dict(passed=0, failed=0)
try:
    for _ in range(runs):
        if time.monotonic() - start >= budget:
            break
        began = time.monotonic()
        loadavg = Path("/proc/loadavg").read_text().strip()
        log = out / f"{index:03d}.log"
        with log.open("w") as f:
            f.write(f"# spinners {spinners} affinity {sorted(os.sched_getaffinity(0))[0]}-{sorted(os.sched_getaffinity(0))[-1]} loadavg-before {loadavg}\n")
            f.write(f"# {' '.join(argv)} in {cwd} head {subprocess.run(['git','-C',str(tree),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()}\n")
            f.flush()
            rc = subprocess.run(argv, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
        (out / f"{index:03d}.rc").write_text(f"{rc}\n")
        tally["passed" if rc == 0 else "failed"] += 1
        print(f"run {index} rc={rc} {time.monotonic()-began:.0f}s load {loadavg.split()[0]}", flush=True)
        index += 1
finally:
    if load is not None:
        os.killpg(load.pid, signal.SIGKILL)
        load.wait()
print(json.dumps(tally))
