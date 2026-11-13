#!/usr/bin/env python3
"""Run a queue of gate commands, each line `NAME CMD...`, every one as its own transient unit (unit.sh, MemoryMax 10G)
on the given CPUs, while fewer than MAX of them run and MemAvailable is above FLOOR_GB; a line is taken once, and
each start and end is logged with the unit's rc (the file unit.sh writes). usage: dispatch.py MAX FLOOR_GB CPUS QUEUE"""
import subprocess
import sys
import time
from pathlib import Path

T = Path('/data-2/milan/tmp/894-a773')
MAX, FLOOR, CPUS, Q = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
LOG = T / 'gates-out/dispatch.txt'
LOG.parent.mkdir(parents=True, exist_ok=True)
lines = [l.split(' ', 1) for l in Q.read_text().splitlines() if l.strip() and not l.startswith('#')]
running: list[str] = []


def note(text: str) -> None:
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def avail_gb() -> float:
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def active(name: str) -> bool:
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', f'milan-894-a773-{name}.service']).returncode == 0


note(f'queue {Q.name}: {len(lines)} lines, at most {MAX} at once, floor {FLOOR} GB, CPUs {CPUS}')
while lines or running:
    for name in list(running):
        if not active(name):
            running.remove(name)
            rc = (T / 'units' / f'{name}.rc')
            note(f"{name} ended rc={rc.read_text().strip() if rc.exists() else '?'}")
    while lines and len(running) < MAX and avail_gb() > FLOOR:
        name, cmd = lines.pop(0)
        subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, CPUS, str(T), 'bash', '-c', cmd], check=True)
        running.append(name)
        note(f'{name} started (MemAvailable {avail_gb():.0f} GB)')
        time.sleep(20)
    time.sleep(30)
note('queue done')
