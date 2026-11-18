#!/usr/bin/env python3
"""Rehydrate only the public author receipts used by the audits into packet/scratch.

Run from a clone containing public archive commit 66fea879135dec78ecfb2410d5dc2115c1a29077.
If needed, first fetch that exact public commit from origin. No other review reports are read.
"""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parents[1]
COMMIT='66fea879135dec78ecfb2410d5dc2115c1a29077'
PREFIX='review-evidence/train1117-r1/author-r5/receipts/'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',COMMIT,'--',PREFIX],text=True).splitlines()
assert paths
for name in paths:
    dest=P/'scratch/evidence'/name;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(subprocess.check_output(['git','show',f'{COMMIT}:{name}']))
print('Restored',len(paths),'public receipt files under scratch/evidence')
