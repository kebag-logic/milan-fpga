"""Scratch smoke test (not committed): the engine driver's --jobs plumbing.

Stubs build() and run_harness() so each "mutant" takes a random time and is
caught through every check it names; compares --jobs 1 / 4 / 8 stdout and
checks that no two mutants used the same directory.
usage: python3 smoke_order.py <repo>
"""
import contextlib, importlib.util, io, random, re, sys, threading, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
eng = repo / "tb/verilator/engine"
sys.path.insert(0, str(eng))
spec = importlib.util.spec_from_file_location("m", eng / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

by_tag = {"".join(c if c.isalnum() else "_" for c in mu[0]): mu for mu in m.MUTATIONS}
used = []
lock = threading.Lock()
active = [0, 0]


def fake_build(srcdir, work, tag):
    with lock:
        used.append(("build", str(work / f"obj_{tag}")))
    return work / f"obj_{tag}" / "exe"


def fake_run(exe, rundir):
    with lock:
        used.append(("run", str(rundir)))
        active[0] += 1
        active[1] = max(active[1], active[0])
    time.sleep(random.random() * 0.05)
    with lock:
        active[0] -= 1
    tag = rundir.name.removeprefix("run_")
    if tag == "clean":
        return 0, "1 checks: 1 PASS, 0 FAIL\n"
    breaks = by_tag[tag][4]
    fails = "".join(f"FAIL {w} got 0 exp 1\n" for w in breaks.split(" | "))
    n = len(breaks.split(" | "))
    return 1, fails + f"{n + 1} checks: 1 PASS, {n} FAIL\n"


m.build = fake_build
m.run_harness = fake_run
outs = {}
for jobs in (1, 4, 8):
    used.clear(); active[1] = 0
    buf = io.StringIO()
    t0 = time.monotonic()
    with contextlib.redirect_stdout(buf):
        rc = m.main(["--jobs", str(jobs)])
    outs[jobs] = (rc, buf.getvalue())
    dirs = [d for k, d in used if k == "run"]
    print(f"jobs {jobs}: rc {rc}, {len(buf.getvalue())} bytes, "
          f"{sum(l.startswith('[PASS] ') for l in buf.getvalue().splitlines())} PASS lines, "
          f"max concurrent {active[1]}, run dirs {len(dirs)} unique {len(set(dirs))}, "
          f"{time.monotonic() - t0:.1f} s; tally {buf.getvalue().strip().splitlines()[-1]}")
print("1 == 4:", outs[1] == outs[4], " 1 == 8:", outs[1] == outs[8])
print("default jobs:", m.default_jobs())
