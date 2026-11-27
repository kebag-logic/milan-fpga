#!/usr/bin/env python3
"""pool7.py WORKERS: run the every-arm groups of round 7 from one shared queue, longest first by round 6's cost
(r7/cost.json, the simulated ms each group's finished log reached; a group without one counts as its sim_ms). Each of
WORKERS threads claims the next unclaimed group (an atomic mkdir of r7/claims/<point>__<variant>__<group>) and runs
run.py on that variant's build (r7/b) for that one group, with one job, into r7/arms/<point>/<variant>/s-<group>,
recording budget and share findings as the formal measurement does; the group's DONE holds run.py's exit status.
Several pools (units on different CPU ranges) share the queue. A claim without a DONE is a group in flight, or one a
killed pool left: release it by removing its claim and its output directory, then start a pool again."""
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

T = Path('<scratch>/r7')
C = T / 'meas'
cost = json.loads((T / 'cost.json').read_text())
queue = []
for p in ('1x1', '8x8-1if'):
    for b in sorted((T / 'b' / p).iterdir()):
        for g in json.loads((b / 'groups.json').read_text()):
            queue.append((cost.get(f'{p}/{b.name}', {}).get(g['name'], g['sim_ms']), p, b.name, g['name']))
queue.sort(key=lambda q: -q[0])
(T / 'claims').mkdir(exist_ok=True)
lock = threading.Lock()


def claim():
    with lock:
        for _, p, v, g in queue:
            try:
                (T / 'claims' / f'{p}__{v}__{g}').mkdir()
            except FileExistsError:
                continue
            return p, v, g
    return None


def worker(n):
    while (job := claim()) is not None:
        p, v, g = job
        out = T / 'arms' / p / v / f's-{g}'
        out.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        with open(f'{out}.out', 'w') as fh:
            rc = subprocess.run(['python3', '-B', 'tb/verilator/ctrl_service_budget/run.py', '--point', p,
                                 '--build-dir', str(T / 'b' / p / v), '--reuse-build', '--variant', v, '--groups', g,
                                 '--out', str(out), '--jobs', '1', '--record-budget-findings',
                                 '--record-share-findings'], cwd=C, stdout=fh, stderr=subprocess.STDOUT).returncode
        (out / 'DONE').write_text(f'{rc}\n')
        print(f'{time.strftime("%T")} w{n} {p} {v} {g} rc={rc} {time.time() - t0:.0f} s', flush=True)


n = int(sys.argv[1])
print(f'{time.strftime("%T")} pool of {n} at {subprocess.run(["git", "-C", str(C), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True).stdout.strip()}, {len(queue)} groups queued', flush=True)
threads = [threading.Thread(target=worker, args=(k,)) for k in range(n)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f'{time.strftime("%T")} pool done', flush=True)
