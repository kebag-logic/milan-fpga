#!/usr/bin/env python3
"""A helper run for a split harness leg on the same build (lane 895; after #665's a683zm_helper2.py).

usage: helper.py NAME POINT SHARE CLONE TAG [run.py args]

The groups no run of builds/NAME has started (no log in any results-* directory), from the tail of run.py's own order
(the point's all_groups order), as much of them as SHARE of their simulated time, run with 7 jobs into results-TAG.
While it runs, a simulation one of the leg's part runs starts of one of the helper's groups is stopped: its Vsim, by
PID, whose argument is builds/NAME/results-p<k>/<group>.txt under this lane's scratch, so no group runs twice to its
end. The leg is merged and regraded afterwards (merge.py).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

name, point, share, clone, tag = sys.argv[1:6]
extra = sys.argv[6:]
T = Path('<scratch>')
B = T / 'builds' / name
H = Path(clone) / 'tb/verilator/ctrl_service_budget'
LOG = T / f'legs/{name}-{tag}.txt'
sys.path[:0] = [str(H)]
os.chdir(H)
import run  # noqa: E402
import scenario  # noqa: E402


def note(text: str) -> None:
    """One line of the helper's log."""
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


spec = json.loads((B / 'build.json').read_text())
order = run.all_groups(scenario.point(point, spec), spec)
started = {g.name for g in order if any((d / f'{g.name}.log').exists() for d in B.glob('results*'))}
# groups another helper has claimed: only the part runs' duplicates are stopped, so a helper never shares
claimed = {x for f in B.glob('part*.groups') if f.stem not in ('part0', 'part1', f'part{tag}')
           for x in f.read_text().split(',') if x}
started |= claimed
left = [g for g in order if g.name not in started]
goal = float(share) * sum(g.sim_ms for g in left)
helper, total = [], 0.0
for g in reversed(left):
    if total >= goal:
        break
    helper.append(g.name)
    total += g.sim_ms
(B / f'part{tag}.groups').write_text(','.join(helper))
note(f'{name}: {len(order)} groups, {len(started)} started; the helper takes {len(helper)} '
     f'({total / 1000:.1f} of {sum(g.sim_ms for g in left) / 1000:.1f} simulated s): {",".join(helper)}')
env = dict(os.environ, TMPDIR=str(T / f'tmp/{name}-{tag}'), PYTHONUNBUFFERED='1')
(T / f'tmp/{name}-{tag}').mkdir(parents=True, exist_ok=True)
with (T / f'legs/{name}-{tag}.log').open('w') as out:
    proc = subprocess.Popen(['python3', '-B', str(H / 'run.py'), '--point', point, '--build-dir', str(B),
                             '--reuse-build', '--groups', ','.join(helper), '--out', str(B / f'results-{tag}'),
                             '--record-budget-findings', '--record-share-findings', '--jobs', '7', *extra],
                            stdout=out, stderr=subprocess.STDOUT, env=env)
    stopped = set()
    while proc.poll() is None:
        ps = subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()
        for line in ps:
            pid, _, args = line.strip().partition(' ')
            for g in helper:
                for part in ('p0', 'p1'):
                    if args.endswith(f'/Vsim {B}/results-{part}/{g}.txt -') and pid not in stopped:
                        note(f"stopping part {part}'s duplicate of {g}: pid {pid}: {args}")
                        subprocess.run(['kill', pid])
                        stopped.add(pid)
        time.sleep(20)
note(f'{name}: helper ended rc={proc.returncode}; {len(stopped)} duplicate(s) stopped')
(T / f'legs/{name}-{tag}.rc').write_text(f'{proc.returncode}\n')
