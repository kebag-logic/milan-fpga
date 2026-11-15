#!/usr/bin/env python3
"""Reach probe for sweep 3 (figure_sweep.py's ROW rule): every two-decimal figure (1-3 digits before the point) in
section 13 of SPLIT_CONTROL_MEMORY.md, FR_NFR.md 3.4.1 and the PR body that the ROW regex's follow-context does NOT
match (so the sweep never sees it), not one of the head's row figures, in a sentence naming a row.
usage: reach_probe.py <repo> <pr-body.md>"""
import re, sys
from pathlib import Path
root, body = Path(sys.argv[1]), Path(sys.argv[2])
HEAD_ROWS = {'13.10', '74.07', '69.86', '14.66', '127.21', '188.48', '28.95', '27.30', '27.42', '33.38', '48.43',
             '44.24', '206.45', '196.31', '20.93', '806.60', '195.76', '67.94', '68.08', '69.13', '98.49', '459.40'}
SENT = re.compile(r'(?<=[.;:])\s+(?=[A-Z`(*\[])')
HIST = re.compile(r"\b(was|were|had|before|then|earlier|previously|first|at round|round \d+'s|since|stated before|"
                  r"before it|at the merge|by then|once|used to|no longer|superseded|history|historical|"
                  r"would|refuted|from \d|beside)\b", re.I)
ROWCTX = re.compile(r'(?<![\d.,])(\d{1,3}\.\d{2})(?= ?ms\b| and \d| within| over|,| ms| \()')
ANY = re.compile(r'(?<![\d.,])(\d{1,3}\.\d{2})(?![\d])')
NAMES = re.compile(r'ms|row|txL|R4L|R4\b|R5|R6|ACMP|ADP|MAAP|notice|tx\b')
def spans():
    s = (root / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text().split('\n')
    a = next(i for i, l in enumerate(s) if l.startswith('## 13.')); b = next(i for i, l in enumerate(s) if l.startswith('## 14.'))
    yield from (('SCM', i + 1, s[i]) for i in range(a, b))
    f = (root / 'docs/reference/FR_NFR.md').read_text().split('\n')
    a = next(i for i, l in enumerate(f) if l.startswith('### 3.4.1')); b = next(i for i, l in enumerate(f) if l.startswith('### 3.4.2'))
    yield from (('FR', i + 1, f[i]) for i in range(a, b))
    yield from (('BODY', i + 1, l) for i, l in enumerate(body.read_text().split('\n')))
n = 0
for src, no, line in spans():
    for s in SENT.split(line):
        if not NAMES.search(s):
            continue
        caught = {m.start() for m in ROWCTX.finditer(s)}
        for m in ANY.finditer(s):
            if m.start() in caught or m.group(1) in HEAD_ROWS:
                continue
            n += 1
            tag = 'HIST' if HIST.search(s) else 'CUR?'
            ctx = s[max(0, m.start() - 70):m.end() + 25].replace('\t', ' ')
            print(f'{src}:{no}\t{tag}\t{m.group(1)}\t{ctx}')
print(f'# {n} two-decimal figures outside ROW\'s follow-context', file=sys.stderr)
