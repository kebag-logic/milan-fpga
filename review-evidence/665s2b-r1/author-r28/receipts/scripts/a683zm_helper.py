#!/usr/bin/env python3
"""A helper run for a leg (fleg.sh) on the same build: the tail of the leg's rest run, in run.py's own order (the
point's all_groups order), as much of it as SHARE of the rest's simulated time not yet started, run with JOBS jobs into
results-help. While it runs, a simulation the rest run starts of one of the helper's groups is stopped (its Vsim, by
PID, its argument this leg's own results-rest/<group>.txt), so no group runs twice to its end. Once the helper ends,
the leg is merged and regraded again (remerge.sh), whatever the rest run did.
usage: a683zm_helper.py NAME POINT JOBS SHARE CLONE GROUPS [run.py args]"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

name, point, jobs, share, clone, groups = sys.argv[1:7]
extra = sys.argv[7:]
T = Path('<scratch>')
B = T / 'builds' / name
H = Path(clone) / 'tb/verilator/ctrl_service_budget'
LOG = T / f'logs/{name}-helper.txt'
sys.path[:0] = [str(H), str(H / '../../../sw/mailbox')]
os.chdir(H)
import run  # noqa: E402
import scenario  # noqa: E402


def note(text: str) -> None:
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


spec = json.loads((B / 'build.json').read_text())
order = run.all_groups(scenario.point(point, spec), spec)
listed = groups.split(',')
first = listed[0]
alone = set(json.loads((T / 'alone.json').read_text()).get(name, []))
rest = [g for g in order if g.name in listed and g.name != first and g.name not in alone]
started = {g.name for g in rest if (B / 'results-rest' / f'{g.name}.log').exists()}
left = [g for g in rest if g.name not in started]
goal = float(share) * sum(g.sim_ms for g in left)
helper, total = [], 0.0
for g in reversed(left):
    if total >= goal:
        break
    helper.append(g.name)
    total += g.sim_ms
note(f'{name}: rest {len(rest)} groups, {len(started)} started; the helper takes {len(helper)} '
     f'({total / 1000:.1f} of {sum(g.sim_ms for g in left) / 1000:.1f} simulated s): {",".join(helper)}')
env = dict(os.environ, TMPDIR=str(T / f'tmp/{name}-help'), PYTHONUNBUFFERED='1')
(T / f'tmp/{name}-help').mkdir(parents=True, exist_ok=True)
with (T / f'logs/{name}-help.log').open('w') as out:
    proc = subprocess.Popen(['python3', '-B', str(H / 'run.py'), '--point', point, '--build-dir', str(B), '--reuse-build',
                             '--groups', ','.join(helper), '--out', str(B / 'results-help'),
                             '--record-budget-findings', '--record-share-findings', '--jobs', jobs, *extra],
                            stdout=out, stderr=subprocess.STDOUT, env=env)
    stopped = set()
    while proc.poll() is None:
        ps = subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()
        for line in ps:
            pid, _, args = line.strip().partition(' ')
            for g in helper:
                if args.endswith(f'/Vsim {B}/results-rest/{g}.txt -') and pid not in stopped:
                    note(f'stopping the rest run\'s duplicate of {g}: pid {pid}: {args}')
                    subprocess.run(['kill', pid])
                    stopped.add(pid)
        time.sleep(30)
note(f'{name}: helper ended rc={proc.returncode}; {len(stopped)} duplicate(s) stopped')
# the rest run may still have its own groups running, and the leg's own merge and regrade follow it: wait for both
begun = time.time()
rc_file = T / f'logs/{name}.log.rc'
while subprocess.run(['pgrep', '-f', f'--out {B}/results-rest'], capture_output=True).returncode == 0 or \
        not (rc_file.exists() and rc_file.stat().st_mtime > begun - 1e9 and
             'elapsed=' in (T / f'logs/{name}.log').read_text()):
    time.sleep(30)
rc = subprocess.run(['bash', str(T / 'scripts/remerge.sh'), clone, name, point, groups, *extra]).returncode
note(f'{name}: remerge rc={rc}; {(T / f"logs/{name}.log.rc").read_text().strip()}')
