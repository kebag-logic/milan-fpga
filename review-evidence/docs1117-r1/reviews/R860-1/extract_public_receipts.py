#!/usr/bin/env python3
"""Extract only public author receipts from the immutable evidence commit."""
from pathlib import Path
import subprocess
import sys

root, out = map(Path, sys.argv[1:3])
revision = 'fd6e25a49ad62d606d972c7eeb7ffe5ed7b9f4a0'
prefix = 'review-evidence/docs1117-r1'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
paths = git('ls-tree', '-r', '--name-only', revision, prefix).decode().splitlines()
count = 0
for path in paths:
    if '/receipts/' not in path and path != prefix + '/MANIFEST.json':
        continue
    dest = out/'scratch/archive'/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(git('show', revision + ':' + path))
    count += 1
print('extracted',count,'public receipt and manifest files')
