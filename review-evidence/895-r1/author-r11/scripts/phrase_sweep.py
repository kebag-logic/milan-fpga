#!/usr/bin/env python3
"""phrase_sweep.py TREE: R835-5-S2's sweep (lane 895 round 11). Every "at this head", "at the head", "this head's" and
"now" in SPLIT_CONTROL_MEMORY.md section 13's marked subsections (those titled (#895), round 5's "SRP's Talker
declarations on THE TIERS" and #894's "The final pass's restatements"), in FR_NFR.md 3.4.1, and in every README the
PR touches, each printed with its sentence for a disposition."""
import re
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
PAT = re.compile(r"\bat this head\b|\bat the head\b|\bthis head's\b|\bnow\b", re.I)


def regions():
    scm = (tree / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text().splitlines()
    marked, on = [], False
    for k, l in enumerate(scm, 1):
        if l.startswith('### ') or l.startswith('## '):
            on = l.startswith('### ') and ('(#895)' in l or "SRP's Talker declarations on THE TIERS" in l
                                          or "The final pass's restatements" in l)
        if on:
            marked.append(('docs/design/SPLIT_CONTROL_MEMORY.md', k, l))
    fr = (tree / 'docs/reference/FR_NFR.md').read_text().splitlines()
    on = False
    for k, l in enumerate(fr, 1):
        if l.startswith('### '):
            on = l.startswith('### 3.4.1')
        if on:
            marked.append(('docs/reference/FR_NFR.md', k, l))
    files = subprocess.run(['git', '-C', str(tree), 'diff', '--name-only', 'cec88385', 'HEAD', '--', '*README.md'],
                           capture_output=True, text=True).stdout.split()
    for f in files:
        for k, l in enumerate((tree / f).read_text().splitlines(), 1):
            marked.append((f, k, l))
    return marked


n = 0
for f, k, l in regions():
    for m in PAT.finditer(l):
        s = l.rfind('. ', 0, m.start()); s = 0 if s < 0 else s + 2
        e = l.find('. ', m.end()); e = len(l) if e < 0 else e + 1
        n += 1
        print(f'{n}\t{f}:{k}\t{m.group(0)}\t{l[s:e][:500]}')
