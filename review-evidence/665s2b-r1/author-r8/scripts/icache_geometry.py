#!/usr/bin/env python3
"""Scratch: round 6's fetch L1 model (icache.py: 64-byte lines, a miss on each committed PC whose line is not held)
with its geometry as a parameter: SETS sets of WAYS ways, least recently used replaced. 64x1 is the product's
4 KiB direct-mapped fetch L1, the geometry round 6 validated against the traces' FETCH lines.

usage: icache_geometry.py TRACE START END [TRACE START END ...]
- TRACE: a harness log run with BUDGET_TRACE_AFTER/BUDGET_TRACE_PCS (PC lines: `PC <bus cycle> <pc>`, FETCH lines:
  each refill the simulated cache made);
- START, END: a composed row's window in bus cycles (the results JSON's first service record's start_sys and the
  row's end_sys). Only the PCs inside the window are modelled; the cache is warmed by the PCs before it.
Prints, per trace, the refills each geometry makes in the window, the 64x1 model against the trace's own FETCH
count in the window, and the change against 64x1."""
import sys
from collections import OrderedDict

LINE = 64
GEOMETRIES = ((64, 1), (128, 1), (256, 1), (32, 2), (64, 2), (128, 2), (64, 4), (16, 4))


def load(path: str, start: int, end: int):
    warm, inside, fetches = [], [], 0
    for line in open(path):
        if line.startswith('PC '):
            _, cyc, pc = line.split()
            cyc = int(cyc)
            if cyc < start:
                warm.append(int(pc, 16))
            elif cyc <= end:
                inside.append(int(pc, 16))
        elif line.startswith('FETCH '):
            f = line.split()
            if len(f) > 1 and f[1].isdigit() and start <= int(f[1]) <= end:
                fetches += 1
    return warm, inside, fetches


def refills(warm, inside, sets: int, ways: int) -> int:
    held = [OrderedDict() for _ in range(sets)]
    n = 0
    last = -1
    for counting, pcs in ((False, warm), (True, inside)):
        for pc in pcs:
            line = pc // LINE
            if line == last:
                continue
            last = line
            s = held[line % sets]
            if line in s:
                s.move_to_end(line)
                continue
            if counting:
                n += 1
            s[line] = True
            if len(s) > ways:
                s.popitem(last=False)
    return n


def main() -> int:
    args = sys.argv[1:]
    for k in range(0, len(args), 3):
        path, start, end = args[k], int(args[k + 1]), int(args[k + 2])
        warm, inside, fetches = load(path, start, end)
        base = refills(warm, inside, 64, 1)
        cells = []
        for sets, ways in GEOMETRIES:
            r = base if (sets, ways) == (64, 1) else refills(warm, inside, sets, ways)
            cells.append(f'{sets * ways * LINE // 1024} KiB {sets}x{ways}: {r} ({100.0 * (r - base) / base:+.1f} %)')
        print(f'{path.rsplit("/", 1)[-1]}: window {len(inside)} PCs; trace FETCH in window {fetches}; '
              f'model 64x1 {base}; ' + '; '.join(cells))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
