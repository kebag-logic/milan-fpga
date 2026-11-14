#!/usr/bin/env python3
"""One pass of round 5's gate dispatcher (lane 895, after scripts/gates/disp.py, which loops): each queue line
`NAME MEMORY_MAX CMD...` in order is started as its own transient unit (round5/scripts/unit.sh, units in
r5/units, its rc there) on a range cpu_ranges.pick8() books, while MemAvailable is above FLOOR_GB and this lane holds
fewer than MAX gate units; a started line leaves the queue. Prints what started and each gate unit's state.
usage: disp_once.py MAX FLOOR_GB QUEUE"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges  # noqa: E402

S = Path(__file__).resolve().parents[1]
U = Path('/data-2/milan/tmp/895-a775/r5/units')
LOG = U / 'dispatch.txt'
MAX, FLOOR, Q = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
PREFIXES = ('W-', 'lane-', 'harness-', 'X-', 'sweep')


def avail_gb() -> float:
    return next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576


def mine() -> set[str]:
    out = subprocess.run(['systemctl', '--user', 'list-units', 'milan-895-a775-r5-*', '--no-legend', '--plain',
                          '--state=active'], capture_output=True, text=True).stdout
    names = {l.split()[0].removeprefix('milan-895-a775-r5-').removesuffix('.service') for l in out.splitlines()
             if l.split()}
    return {n for n in names if n.startswith(PREFIXES)}


U.mkdir(parents=True, exist_ok=True)
running = mine()
lines = [l for l in Q.read_text().splitlines() if l.strip()]
left = []
for line in lines:
    name, mem, cmd = line.split(None, 2)
    if (U / f'{name}.rc').exists() or name in running:
        print(f'{name}: already started')
        continue
    rng = cpu_ranges.pick8() if avail_gb() > FLOOR and len(running) < MAX else None
    if not rng:
        left.append(line)
        continue
    subprocess.run(['bash', str(S / 'unit.sh'), name, rng, mem, str(U), '--', cmd], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    running.add(name)
    with LOG.open('a') as f:
        f.write(f"{time.strftime('%T')} {name} on {rng} (MemAvailable {avail_gb():.0f} GB)\n")
    print(f'{time.strftime("%T")} started {name} on {rng}')
    time.sleep(3)
Q.write_text(''.join(l + '\n' for l in left))
for n in sorted(p.stem for p in U.glob('*.log') if p.stem.startswith(PREFIXES)):
    rc = U / f'{n}.rc'
    print(f'{n}:{rc.read_text().strip() if rc.exists() else "run"}', end=' ')
print(f'\nqueued {len(left)}')
