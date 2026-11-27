#!/usr/bin/env python3
"""Verify the publication repair changes only the reported decimal timestamps."""
import collections, subprocess, sys
from pathlib import Path
repo, receipt = Path(sys.argv[1]), Path(sys.argv[2])
raw = subprocess.check_output(['git','-C',str(repo),'diff','--no-ext-diff','--unified=0','0cad829e^','0cad829e','--',
    'review-evidence/artysplit-r1/author-r8/receipts/census-extract'])
lines = raw.decode().splitlines()
old = [x[1:].split() for x in lines if x.startswith('-') and not x.startswith('---')]
new = [x[1:].split() for x in lines if x.startswith('+') and not x.startswith('+++')]
assert sum(x.startswith('diff --git ') for x in lines) == 27
assert len(old) == len(new) == 29
changes = []
for before, after in zip(old,new):
    assert len(before) == len(after)
    assert before[0] == after[0] == 'SPAN'
    assert before[3:] == after[3:]
    assert int(after[1]) - int(after[2]) == 64
    changes.extend((x,y) for x,y in zip(before,after) if x != y)
assert len(changes) == 32 and all(y.isdecimal() for x,y in changes)
text = 'PASS 27 observation files, 29 SPAN lines, 32 restored decimal timestamp tokens; no other tokens changed\n'
text += 'PASS each restored SPAN has end - start = 64 cycles\n'
text += '\n'.join(f'{x} -> {y}' for x,y in changes) + '\n'
(receipt/'publication-delta.diff').write_bytes(raw)
(receipt/'publication-delta.log').write_text(text)
print(text)
