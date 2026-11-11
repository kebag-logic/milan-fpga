#!/usr/bin/env python3
"""Wait until four distinct 8-wide CPU ranges are free (cpu_ranges.pick8, each pick counted as taken for the next)
and MemAvailable is above 30 GB, then run native-shards.py once; the shard holding capture_coherence (2 of 4) gets
the first 4 CPUs of its range. Books nothing while waiting."""
import subprocess, sys, time
from pathlib import Path
M = '<management>/2026-09-23'
sys.path.insert(0, M)
import cpu_ranges  # noqa: E402
G = Path('<scratch>/gates/sweep')
log = open(G / 'launch2.txt', 'a', buffering=1)
while True:
    avail = int(next(l for l in open('/proc/meminfo') if l.startswith('MemAvailable')).split()[1])
    taken, picks = cpu_ranges.busy(), []
    if avail > 30 * 1024 * 1024:
        for _ in range(4):
            r = cpu_ranges.pick8(taken)
            if r is None:
                break
            picks.append(r)
            taken |= cpu_ranges.expand(r)
    if len(picks) == 4:
        break
    log.write(f'{time.strftime("%T")} waiting: MemAvailable {avail} kB, free 8-wide ranges {picks}\n')
    time.sleep(120)
a = int(picks[2].split('-')[0])
picks[2] = f'{a}-{a + 3}'
log.write(f'{time.strftime("%T")} launching on {picks} (MemAvailable {avail} kB)\n')
rc = subprocess.run(['/usr/bin/python3', f'{M}/native-shards.py', '665s11-a761c-sx', str(G / 'full-native.json'),
                     str(G / 'out2'), '4', *picks], stdout=log, stderr=subprocess.STDOUT).returncode
log.write(f'{time.strftime("%T")} native-shards rc={rc}\n')
