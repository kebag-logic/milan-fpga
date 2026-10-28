#!/usr/bin/env python3
"""Each change of the function the CPU's sampled PC is in, off a harness log's MS lines.
usage: pc_trace.py <build-dir> <group-log>"""
import json
import sys
from pathlib import Path

build, log = Path(sys.argv[1]), Path(sys.argv[2])
functions = json.loads((build / 'image/functions.json').read_text())


def name(pc: int) -> str:
    """The function holding pc, or the start code below the first function."""
    for fn, start, size in functions:
        if start <= pc < start + size:
            return fn
    return '_start (ctrl_split_start.S)' if pc < functions[0][1] else '?'


last, lines, last_ms = None, 0, '-'
for line in log.read_text().splitlines():
    p = line.split()
    if len(p) == 5 and p[0] == 'MS':
        lines += 1
        last_ms = p[2]
        fn = name(int(p[3], 16))
        if fn != last:
            print(f'{p[2]:>6} ms  pc {p[3]}  {fn}')
            last = fn
print(f'{lines} MS samples; last at {last_ms} ms')
