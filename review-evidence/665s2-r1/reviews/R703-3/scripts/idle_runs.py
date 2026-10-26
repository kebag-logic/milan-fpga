#!/usr/bin/env python3
"""Idle-pass range per point from the raw IDLE lines (IDLE count min max), with and without
each log's last run (the run the script's end flushes, which holds the pass it cut short).
Usage: idle_runs.py RESULTS_DIR"""
import sys
from pathlib import Path
all_min, all_max, whole_min, whole_max = [], [], [], []
for log in sorted(Path(sys.argv[1]).glob('*.log')):
    runs = [tuple(int(v) for v in l.split()[1:4]) for l in log.read_text().splitlines() if l.startswith('IDLE ')]
    if not runs:
        continue
    last = runs[-1]
    whole = runs[:-1]
    wmax = max((m for _, _, m in whole), default=0)
    if last[2] > wmax:
        print(f'{log.name}: last run max {last[2]:,} (count {last[0]}) exceeds the other runs\' max {wmax:,}')
    all_max.append(max(m for _, _, m in runs)); whole_max.append(wmax)
    all_min += [m for _, m, _ in runs if m]; whole_min += [m for _, m, _ in whole if m]
print(f'with the last runs: {min(all_min):,} to {max(all_max):,}; without them: {min(whole_min):,} to {max(whole_max):,}')
