#!/usr/bin/env python3
"""pool_start.py QUEUE NAME...: start each named queue line (lane 895 round 9's gate queue) as its own unit on the
session pool 96-127, which the owner allows for single legs and campaigns while cpu_ranges.pick8() hands out nothing
(a release hold collecting CPUs), while fewer than POOL_MOST (2) of this round's units run there and MemAvailable is
above 20 GB; a started line leaves the queue. Prints what started."""
import os
import subprocess
import sys
import time
from pathlib import Path

S = Path(__file__).resolve().parents[1]
U = Path('/data-2/milan/tmp/895-a775/r9/units')
POOL, MOST = '96-127', int(os.environ.get('POOL_MOST', '2'))
q, names = Path(sys.argv[1]), sys.argv[2:]


def on_pool() -> int:
    out = subprocess.run(['systemctl', '--user', 'list-units', 'milan-895-a775-r9-*', '--no-legend', '--plain',
                          '--state=active'], capture_output=True, text=True).stdout
    n = 0
    for line in out.splitlines():
        pid = subprocess.run(['systemctl', '--user', 'show', '-p', 'MainPID', '--value', line.split()[0]],
                             capture_output=True, text=True).stdout.strip()
        aff = subprocess.run(['taskset', '-cp', pid], capture_output=True, text=True).stdout.rpartition(': ')[2]
        n += aff.strip() == POOL
    return n


avail = lambda: next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576
lines = [l for l in q.read_text().splitlines() if l.strip()]
left = []
for line in lines:
    name, mem, cmd = line.split(None, 2)
    if name in names and on_pool() < MOST and avail() > 20 and not (U / f'{name}.rc').exists():
        subprocess.run(['bash', str(S / 'unit.sh'), name, POOL, mem, str(U), '--', cmd], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with (U / 'dispatch.txt').open('a') as f:
            f.write(f"{time.strftime('%T')} {name} on {POOL} (the session pool; pick8 none) MemAvailable {avail():.0f} GB\n")
        print(f'{time.strftime("%T")} started {name} on {POOL}')
        time.sleep(5)
        continue
    left.append(line)
q.write_text(''.join(l + '\n' for l in left))
