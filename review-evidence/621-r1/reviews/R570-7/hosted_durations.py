#!/usr/bin/env python3
"""Tabulate hosted Verilator shard job durations from `gh run view --json jobs` TSV dumps.

Usage: hosted_durations.py <run_ID.jobs.tsv>...  (columns: [sha,] name, status, conclusion, start, end)
"""
import datetime as dt
import sys

def secs(a, b):
    p = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    return int((p(b) - p(a)).total_seconds())

print('run\tsha\tshard0\tshard1\tshard2\tshard3\tshard4')
for path in sys.argv[1:]:
    run = path.rsplit('/', 1)[-1].split('_')[1].split('.')[0]
    sha, row = '', {}
    for line in open(path):
        f = line.rstrip('\n').split('\t')
        if len(f) == 6:
            sha, f = f[0], f[1:]
        name, status, concl, start, end = f
        if name.startswith('Verilator shard'):
            row[name[-3]] = f'{secs(start, end)}' if status == 'completed' else status
    print('\t'.join([run, sha] + [row.get(str(i), '') for i in range(5)]))
