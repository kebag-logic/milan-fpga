#!/usr/bin/env python3
"""A helper that takes the unstarted tail of a leg's groups whoever claimed them: every group, in run.py's own order,
with no log yet in any run of the leg's build (results*), as much of it from the end as SHARE of their simulated time,
run with JOBS jobs into results-TAG on the same build (run.py --reuse-build). While it runs, a simulation any other run
of the build starts of one of its groups is stopped (its Vsim, by PID), so no group runs twice to its end. The leg's
runs are merged and regraded afterwards (merge_leg.py). usage: HELPER_CLONE=CLONE a683zo_steal.py NAME POINT JOBS SHARE TAG"""
import json, os, subprocess, sys, time
from pathlib import Path
name, point, jobs, share, tag = sys.argv[1:6]
T = Path('/data-2/milan/tmp/665s2b-a683zo')
B = T / 'builds' / name
C = Path(os.environ['HELPER_CLONE'])
H = C / 'tb/verilator/ctrl_service_budget'
LOG = T / f'logs/{name}-helper-{tag}.txt'
sys.path[:0] = [str(H), str(C / 'sw/mailbox')]
os.chdir(H)
import run, scenario  # noqa: E402


def note(t):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {t}\n")


# STEAL_OUTSIDE: write to stolen-TAG, outside results*, where an earlier stealer's duplicate check does not look
out = B / (f'stolen-{tag}' if os.environ.get('STEAL_OUTSIDE') else f'results-{tag}')
runs = lambda: {d for d in B.iterdir() if d.is_dir() and d.name.startswith(('results', 'stolen-'))}
spec = json.loads((B / 'build.json').read_text())
order = run.all_groups(scenario.point(point, spec), spec)
started = {p.stem for d in runs() for p in d.glob('*.log')}
# a group another stealer claimed is its own, started or not: stealers stop each other's duplicates
claimed = set()
for f in (T / 'logs').glob(f'{name}-helper-*.txt'):
    first = f.read_text().split('\n')[0]
    keep = os.environ.get('STEAL_EXCLUDE', '').split(',')   # stealers whose claims stay theirs even so
    if f != LOG and 'not started by any run' in first and '): ' in first and \
            (not os.environ.get('STEAL_FROM_STEALERS') or f.stem.rsplit('-', 1)[1] in keep):
        claimed |= set(first.split('): ', 1)[1].split(','))
if os.environ.get('STEAL_UNFINISHED'):
    # STEAL_UNFINISHED: a group is free unless a run has finished it or a simulation of it is running now
    def finished(g):
        for d in runs():
            f = d / f'{g.name}.log'
            if f.exists():
                with open(f, 'rb') as x:
                    x.seek(0, 2)
                    x.seek(max(0, x.tell() - 5000))
                    if b'SUMMARY' in x.read():
                        return True
        return False
    live = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    running = {g.name for g in order if any(f' {d}/{g.name}.txt -' in live for d in runs())}
    started = {g.name for g in order if finished(g)} | running
rest = [g for g in order if g.name not in started and g.name not in claimed]
goal = float(share) * sum(g.sim_ms for g in rest)
mine, total = [], 0.0
for g in reversed(rest):
    if total >= goal:
        break
    mine.append(g.name)
    total += g.sim_ms
note(f'{name}: {len(rest)} groups not started by any run; the helper {tag} takes {len(mine)} ({total / 1000:.1f} of '
     f'{sum(g.sim_ms for g in rest) / 1000:.1f} simulated s): {",".join(mine)}')
env = dict(os.environ, TMPDIR=str(T / f'tmp/{name}-{tag}'), PYTHONUNBUFFERED='1')
Path(env['TMPDIR']).mkdir(parents=True, exist_ok=True)
with (T / f'logs/{name}-{tag}.log').open('w') as log:
    proc = subprocess.Popen(['python3', '-B', str(H / 'run.py'), '--point', point, '--build-dir', str(B), '--reuse-build',
                             '--groups', ','.join(mine), '--out', str(out), '--record-budget-findings',
                             '--record-share-findings', '--jobs', jobs],
                            stdout=log, stderr=subprocess.STDOUT, env=env)
    stopped = set()
    while proc.poll() is None:
        others = sorted(d for d in runs() if d != out)
        for line in subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()[1:]:
            pid, _, args = line.strip().partition(' ')
            if '/native/Vsim ' not in args or pid in stopped:
                continue
            for g in mine:
                if any(args.endswith(f' {d}/{g}.txt -') for d in others):
                    note(f"stopping another run's duplicate of {g}: pid {pid}: {args.split()[-2]}")
                    subprocess.run(['kill', pid])
                    stopped.add(pid)
        time.sleep(20)
note(f'{name}: helper {tag} ended rc={proc.returncode}; {len(stopped)} duplicate(s) stopped')
sys.exit(proc.returncode)
