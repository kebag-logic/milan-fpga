#!/usr/bin/env python3
"""Run a queue of gate commands (each line: NAME MEMORY_MAX CMD...), each started only while MemAvailable is above
FLOOR_GB: on a free booked range as its own unit when cpu_ranges.py offers one and this lane has fewer than MAX
active units, else in this session, at most LOCAL at once. A line is taken once; a log line per start and end.
usage: dispatch2.py MAX LOCAL FLOOR_GB QUEUE"""
import subprocess, sys, time
from pathlib import Path
T = Path('<scratch>')
LOG = T / 'logs/dispatch.txt'
MAX, LOCAL, FLOOR, Q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
local = {}


def note(text):
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {text}\n")


def active_units():
    out = subprocess.run(['systemctl', '--user', 'list-units', 'milan-665s2b-a683ze-*', '--no-legend', '--state=active',
                          '--plain'], capture_output=True, text=True).stdout
    return sum(1 for line in out.splitlines() if '.service' in line)


def avail_gb():
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


while True:
    for name, p in list(local.items()):
        if p.poll() is not None:
            note(f'{name} local done rc={p.returncode}')
            del local[name]
    lines = [line for line in Q.read_text().splitlines() if line.strip()]
    if not lines:
        if not local:
            note(f'queue {Q.name} empty')
            break
        time.sleep(30)
        continue
    name, mem, cmd = lines[0].split(None, 2)
    started = False
    if avail_gb() > FLOOR:
        if active_units() < MAX:
            pick = subprocess.run(['python3', '<management>/2026-09-23/cpu_ranges.py', 'pick'],
                                  capture_output=True, text=True)
            if pick.returncode == 0 and pick.stdout.strip():
                rng = pick.stdout.strip()
                subprocess.run(['bash', str(T / 'scripts/unit.sh'), name, rng, mem, '--', '/bin/bash', '-c', cmd])
                note(f'{name} on {rng} (MemAvailable {avail_gb():.0f} GB)')
                started = True
        if not started and len(local) < LOCAL:
            local[name] = subprocess.Popen(['/bin/bash', '-c', cmd])
            note(f'{name} locally in the session unit (MemAvailable {avail_gb():.0f} GB)')
            started = True
    if started:
        Q.write_text('\n'.join(lines[1:]) + ('\n' if lines[1:] else ''))
        time.sleep(30)
    else:
        time.sleep(60)
