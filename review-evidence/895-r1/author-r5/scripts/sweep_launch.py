#!/usr/bin/env python3
"""Launch round 5's full Verilator sweep (lane 895) as 4 shard units by native-shards.py, once cpu_ranges.py lists four
free 8-wide ranges (each free 16-block counts as its two halves) and MemAvailable is above 30 GB, the ranges read again
just before the launch. Writes r5/sweep/launched.json; does nothing when it exists."""
import ast, json, subprocess, sys
from pathlib import Path
M = Path('$MANAGEMENT/2026-09-23')
S = Path('/data-2/milan/tmp/895-a775/r5/sweep')
if (S / 'launched.json').exists():
    print('sweep: launched already'); sys.exit(0)


def halves() -> list[str]:
    line = subprocess.run(['python3', str(M / 'cpu_ranges.py'), 'show'], capture_output=True, text=True).stdout
    line = line.strip().splitlines()[-1]
    f16 = ast.literal_eval(line.split('free16 ')[1].split(' free12')[0])
    h8 = ast.literal_eval(line.split('half8 ')[1])
    out = list(h8)
    for r in f16:
        a, b = map(int, r.split('-'))
        out += [f'{a}-{a + 7}', f'{a + 8}-{b}']
    return out


avail = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable')) / 1048576
first = halves()
if len(first) < 4 or avail <= 30:
    print(f'sweep: waiting ({len(first)} free ranges, MemAvailable {avail:.0f} GB)'); sys.exit(0)
again = halves()
cpus = [r for r in first if r in again][:4]
if len(cpus) < 4:
    print('sweep: ranges taken between the two reads'); sys.exit(0)
r = subprocess.run(['python3', str(M / 'native-shards.py'), '895r5sweep', str(S / 'full-native.json'), str(S / 'out'), '4',
                    *cpus], capture_output=True, text=True)
(S / 'launch.log').write_text(r.stdout + r.stderr)
if r.returncode == 0:
    (S / 'launched.json').write_text(json.dumps({'cpus': cpus, 'avail_gb': round(avail), 'out': r.stdout.strip()}) + '\n')
print(f'sweep: native-shards rc {r.returncode} on {cpus}')
