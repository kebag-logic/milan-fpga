#!/usr/bin/env python3
"""rows_cmp.py BASE_LOG HEAD_LOG: one group's simulation log on the base image against the head image's, as
distributions. Each PASS record is `PASS <n> <end> <start> <cycles> instr=<i> fetch_rom=<misses>/<miss cycles> ...`,
one service pass (sim_main.cpp), and STEPPASS a save step's. The two runs do not pair pass for pass: the code after
the hold-off sits 4 bytes later, so fetch timing, and with it where passes fall against the inputs, differs. So each
kind is reported as a distribution on each side: the passes, their cycles summed, the median, the 99th percentile and
the largest, the instructions summed, and the fetch misses summed. One line per kind and side."""
import re
import sys

PASS = re.compile(r'^(PASS|STEPPASS) (\d+) (\d+) (\d+) (\d+)(.*)$')


def read(path: str) -> dict[str, list[tuple[int, int, int]]]:
    out: dict[str, list[tuple[int, int, int]]] = {'PASS': [], 'STEPPASS': []}
    with open(path, errors='replace') as f:
        for line in f:
            m = PASS.match(line)
            if not m:
                continue
            i = re.search(r'instr=(\d+)', m.group(6))
            fr = re.search(r'fetch_rom=(\d+)/', m.group(6))
            out[m.group(1)].append((int(m.group(5)), int(i.group(1)) if i else 0, int(fr.group(1)) if fr else 0))
    return out


def pct(xs: list[int], p: float) -> int:
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * (len(xs) - 1) + 0.5))] if xs else 0


sides = {'base': read(sys.argv[1]), 'head': read(sys.argv[2])}
for kind in ('PASS', 'STEPPASS'):
    for side, d in sides.items():
        v = d[kind]
        if not v:
            continue
        c = [x[0] for x in v]
        print(f'{kind:8} {side}: {len(v)} passes, cycles sum {sum(c)}, median {pct(c, 0.5)}, p99 {pct(c, 0.99)}, '
              f'largest {max(c)}; instructions {sum(x[1] for x in v)}; fetch misses {sum(x[2] for x in v)}')
