#!/usr/bin/env python3
"""Classify a sweep log's failing runs by scenario, engine timing and the first
check letter of each error. Usage: classify_sweep.py LOG"""
import re, sys, collections
runs = collections.Counter(); kinds = collections.Counter(); ex = {}
cur = None
for line in open(sys.argv[1]):
    m = re.match(r'FAIL (S\d) (?:W=\S+ )?gap=(\d+) run=(\d+)', line)
    if m:
        cur = (m.group(1), int(m.group(2)), int(m.group(3))); runs[cur] += 1; continue
    m = re.match(r'    ([A-F]): ', line)
    if m and cur:
        k = (cur, m.group(1)); kinds[k] += 1; ex.setdefault(k, line.strip())
for k, n in sorted(runs.items()): print('runs', k, n)
for k, n in sorted(kinds.items()): print('err', k, n, '|', ex[k][:150])
