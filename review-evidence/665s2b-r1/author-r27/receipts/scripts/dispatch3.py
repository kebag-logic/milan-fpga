#!/usr/bin/env python3
"""Run a queue of gate commands (each line: NAME MEMORY_MAX CMD...), every one as its own transient unit with its own
MemoryMax, never in the session's unit. A line starts only while MemAvailable is above FLOOR_GB: on a range
cpu_ranges.py picks while this lane holds fewer than MAX booked units, else on the shared session pool
(cpu_ranges.session_pool(), which every booking already counts as busy, so it holds nothing from another lane) while
fewer than POOL of this lane's units run there. A line is taken once; a log line per start and end; a unit's rc is
the file its command writes. usage: dispatch3.py MAX POOL FLOOR_GB QUEUE"""
import subprocess, sys, time
from pathlib import Path
sys.path.insert(0, '<management>/2026-09-23')
import cpu_ranges  # noqa: E402

T = Path('<scratch>')
LOG = T / 'logs/dispatch3.txt'
RCS = T / 'logs/rc'
MAX, POOL, FLOOR, Q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
RCS.mkdir(parents=True, exist_ok=True)
mine = {}  # name -> 'booked' | 'pool'


def note(text):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def active(name):
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', f'milan-665s2b-a683zj-{name}.service']).returncode == 0


def avail_gb():
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def start(name, rng, mem, cmd, where):
    rc = RCS / f'{name}.rc'
    rc.unlink(missing_ok=True)
    wrapped = f'{cmd}; echo $? > {rc}'
    subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, rng, mem, '--', '/bin/bash', '-c', wrapped], check=True)
    mine[name] = where
    note(f'{name} unit on {rng} ({where}, MemAvailable {avail_gb():.0f} GB)')


while True:
    for name in list(mine):
        if not active(name):
            rc = RCS / f'{name}.rc'
            note(f'{name} ended rc={rc.read_text().strip() if rc.exists() else "none (no rc file)"}')
            del mine[name]
    lines = [line for line in Q.read_text().splitlines() if line.strip()]
    if not lines:
        if not mine:
            note(f'queue {Q.name} empty')
            break
        time.sleep(30)
        continue
    name, mem, cmd = lines[0].split(None, 2)
    started = False
    if avail_gb() > FLOOR:
        booked = sum(1 for w in mine.values() if w == 'booked')
        pooled = sum(1 for w in mine.values() if w == 'pool')
        rng = cpu_ranges.pick8() if booked < MAX else None
        if rng:
            start(name, rng, mem, cmd, 'booked')
            started = True
        elif pooled < POOL:
            start(name, cpu_ranges.session_pool(), mem, cmd, 'pool')
            started = True
    if started:
        Q.write_text('\n'.join(lines[1:]) + ('\n' if lines[1:] else ''))
        time.sleep(20)
    else:
        time.sleep(45)
