"""Spot sweep: every occurrence of a superseded #894 tier-model figure in tracked docs/, sw/ and tb/ text, with a
window of context, for manual classification (history / beside the head's / current).
Usage: python3 -I spot_sweep.py <checkout> > out.txt"""
import re
import subprocess
import sys

ROOT = sys.argv[1]
FIGS = ['48.09', '188.39', '49.69', '125.84', '97.06', '29.78', '33.01', '0.513', '0.692', '446.92', '195.74',
        '46.58', '135.64', '132.71', '47.98', '173.37', '49.99', '158.34', '187.91', '39.61', '28.00', '89.01',
        '29.80', '98 ms', '30 and 98', '44 ms', '176 ms']
pat = '|'.join(re.escape(f) for f in FIGS)
files = subprocess.run(['git', '-C', ROOT, 'grep', '-l', '-E', pat, '--', 'docs', 'sw', 'tb'], capture_output=True,
                       text=True).stdout.split()
for f in files:
    for n, line in enumerate(open(f'{ROOT}/{f}', encoding='utf-8', errors='replace'), 1):
        for m in re.finditer(r'(?<![\d.])(' + pat + r')(?![\d])', line):
            a, b = max(0, m.start() - 110), m.end() + 60
            print(f'{f}:{n}: {m.group(1)} :: {line[a:b].strip()}')
