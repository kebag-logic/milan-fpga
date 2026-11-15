#!/usr/bin/env python3
"""Launch the four-shard sweep (native-shards.py) once four distinct 8-CPU ranges are free in cpu_ranges.py show,
polling every 30 s for at most LIMIT_S; each shard on its own range. It books nothing while it waits: a range is
booked only by the shard unit that runs on it. usage: sweep_when_free.py LABEL SPEC OUT LIMIT_S"""
import ast
import re
import subprocess
import sys
import time

label, spec, out, limit = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
M = '$MANAGEMENT/2026-09-23'
t0 = time.time()
while time.time() - t0 < limit:
    s = subprocess.run(['python3', f'{M}/cpu_ranges.py', 'show'], capture_output=True, text=True).stdout
    half = ast.literal_eval(re.search(r'half8 (\[.*?\])', s)[1])
    full = ast.literal_eval(re.search(r'free16 (\[.*?\])', s)[1])
    ranges = list(half)
    for r in full:
        a, b = map(int, r.split('-'))
        ranges += [f'{a}-{a + 7}', f'{a + 8}-{b}']
    ranges = sorted(set(ranges), key=lambda r: int(r.split('-')[0]))
    if len(ranges) >= 4:
        pick = ranges[:4]
        print(time.strftime('%T'), 'launching on', pick, flush=True)
        r = subprocess.run(['python3', f'{M}/native-shards.py', label, spec, out, '4', *pick])
        sys.exit(r.returncode)
    time.sleep(30)
print(time.strftime('%T'), 'no four ranges freed within the limit', flush=True)
sys.exit(3)
