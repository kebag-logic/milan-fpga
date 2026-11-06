#!/usr/bin/env python3
"""Wait, up to SECONDS, until every named file exists; print what is still missing and the host's memory.

usage: waitfor.py SECONDS FILE...
Exit 0 when all exist, 3 when the wait ran out. A foreground wait, kept under the ten-minute command limit.
"""
import sys
import time
from pathlib import Path

limit = float(sys.argv[1])
files = [Path(a) for a in sys.argv[2:]]
end = time.monotonic() + limit
while time.monotonic() < end:
    missing = [f for f in files if not f.exists()]
    if not missing:
        break
    time.sleep(min(15, max(1, end - time.monotonic())))
missing = [f for f in files if not f.exists()]
mem = next(line for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable'))
print(f'{len(files) - len(missing)} of {len(files)} present; {mem.split()[1] and int(mem.split()[1]) // 1048576} GiB available')
for f in missing:
    print(f'  waiting: {f.name}')
sys.exit(3 if missing else 0)
