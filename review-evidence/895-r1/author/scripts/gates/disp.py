#!/usr/bin/env python3
"""Run a queue of gate commands (each line: NAME MEMORY_MAX CMD...), every one as its own transient unit (unit.sh) on
an 8-wide range cpu_ranges.pick8() books, while MemAvailable is above FLOOR_GB and this lane holds fewer than MAX of
them (after #665's dispatcher, without its session pool). A line is taken once; a log line per start and end; a
unit's rc is the file its command writes. usage: disp.py MAX FLOOR_GB QUEUE"""
import os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges  # noqa: E402

T = Path(os.environ.get('GATES_ROOT', '/data-2/milan/tmp/895-a775/gates'))
S = Path('$MANAGEMENT/2026-09-23/895-a775/scripts')
LOG = T / 'dispatch.txt'
RCS = T / 'rc'
MAX, FLOOR, Q = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
RCS.mkdir(parents=True, exist_ok=True)
# units of an earlier dispatcher of this queue that still run count against MAX
mine = {l.split()[0].removeprefix('milan-895-a775-').removesuffix('.service') for l in subprocess.run(
    ['systemctl', '--user', 'list-units', 'milan-895-a775-*', '--no-legend', '--state=active'],
    capture_output=True, text=True).stdout.splitlines() if l.split() and l.split()[0].removeprefix('milan-895-a775-')
    .startswith(('W-', 'lane-', 'harness-', 'X-'))}


def note(text):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def active(name):
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', f'milan-895-a775-{name}.service']).returncode == 0


def avail_gb():
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


while True:
    for name in list(mine):
        if not active(name):
            rc = RCS / f'{name}.rc'
            note(f'{name} ended rc={rc.read_text().strip() if rc.exists() else "none (no rc file)"}')
            mine.discard(name)
    lines = [line for line in Q.read_text().splitlines() if line.strip()]
    if not lines:
        if not mine:
            note(f'queue {Q.name} empty')
            break
        time.sleep(30)
        continue
    name, mem, cmd = lines[0].split(None, 2)
    rng = cpu_ranges.pick8() if avail_gb() > FLOOR and len(mine) < MAX else None
    if rng:
        rc = RCS / f'{name}.rc'
        rc.unlink(missing_ok=True)
        subprocess.run(['bash', str(S / 'unit.sh'), name, rng, mem, '--', '/bin/bash', '-c',
                        f"'{cmd}; echo $? > {rc}'"], check=True)
        mine.add(name)
        note(f'{name} unit on {rng} (MemAvailable {avail_gb():.0f} GB)')
        Q.write_text('\n'.join(lines[1:]) + ('\n' if lines[1:] else ''))
        time.sleep(10)
    else:
        time.sleep(10)
