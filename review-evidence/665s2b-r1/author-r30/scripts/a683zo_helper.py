#!/usr/bin/env python3
"""A helper run for a leg on the same build (run.py --reuse-build): the tail of the leg's groups, in run.py's own order,
that neither the leg's own run (results/) nor an earlier helper of this leg (logs/NAME-helper-*.txt) has started, as
much of it as SHARE of their simulated time, run with JOBS jobs into results-TAG. While it runs, a simulation the leg's
own run starts of one of the helper's groups is stopped (its Vsim, by PID, its argument the leg's results/<group>.txt),
so no group runs twice to its end. The leg's runs are merged and regraded afterwards (merge_leg.py, head32.sh).
usage: [HELPER_CLONE=CLONE] a683zo_helper.py NAME POINT JOBS SHARE TAG [run.py args]"""
import json, os, subprocess, sys, time
from pathlib import Path
name, point, jobs, share, tag = sys.argv[1:6]
extra = sys.argv[6:]
T = Path('/data-2/milan/tmp/665s2b-a683zo')
B = T / 'builds' / name
C = Path(os.environ.get('HELPER_CLONE', str(T / f'L32-{name}')))
H = C / 'tb/verilator/ctrl_service_budget'
LOG = T / f'logs/{name}-helper-{tag}.txt'
sys.path[:0] = [str(H), str(C / 'sw/mailbox')]
os.chdir(H)
import run, scenario  # noqa: E402


def note(t):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {t}\n")


taken = set()
for f in (T / 'logs').glob(f'{name}-helper-*.txt'):
    if f != LOG:
        first = f.read_text().split('\n')[0]
        if '): ' in first:
            taken |= set(first.split('): ', 1)[1].split(','))
spec = json.loads((B / 'build.json').read_text())
order = run.all_groups(scenario.point(point, spec), spec)
own = B / 'results'
rest = [g for g in order if g.name not in taken and not (own / f'{g.name}.log').exists()]
goal = float(share) * sum(g.sim_ms for g in rest)
helper, total = [], 0.0
for g in reversed(rest):
    if total >= goal:
        break
    helper.append(g.name)
    total += g.sim_ms
note(f'{name}: {len(rest)} groups not started; the helper {tag} takes {len(helper)} ({total / 1000:.1f} of '
     f'{sum(g.sim_ms for g in rest) / 1000:.1f} simulated s): {",".join(helper)}')
out = B / f'results-{tag}'
env = dict(os.environ, TMPDIR=str(T / f'tmp/{name}-{tag}'), PYTHONUNBUFFERED='1')
Path(env['TMPDIR']).mkdir(parents=True, exist_ok=True)
with (T / f'logs/{name}-{tag}.log').open('w') as log:
    proc = subprocess.Popen(['python3', '-B', str(H / 'run.py'), '--point', point, '--build-dir', str(B), '--reuse-build',
                             '--groups', ','.join(helper), '--out', str(out), '--record-budget-findings',
                             '--record-share-findings', '--jobs', jobs, *extra],
                            stdout=log, stderr=subprocess.STDOUT, env=env)
    stopped = set()
    while proc.poll() is None:
        for line in subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()[1:]:
            pid, _, args = line.strip().partition(' ')
            for g in helper:
                if args.endswith(f' {own}/{g}.txt -') and '/native/Vsim ' in args and pid not in stopped:
                    note(f"stopping the leg's own duplicate of {g}: pid {pid}")
                    subprocess.run(['kill', pid])
                    stopped.add(pid)
        time.sleep(20)
note(f'{name}: helper {tag} ended rc={proc.returncode}; {len(stopped)} duplicate(s) stopped')
sys.exit(proc.returncode)
