#!/usr/bin/env python3
"""Retain raw diff/history and the stated validation-base tree comparison."""
import json
import os
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
head = 'af5be4710c3516cc247c353213d6939fa8d23f57'
parent = '72d3780d23a0b96362f8ae64059311b866ff5776'
source = '04e1435a218908d2b12b4053e5dab2c2dcac2ebf'
source_base = '6714181d0c8a16e2983f85b724f4d688f5111835'
dev = '79b086d44eb62d007d38e18f5618b98e8e2a33e6'

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.commitGraph=false', *args], env=env)

for name, a, b in [('candidate.diff', parent, head), ('predecessor.diff', source_base, parent), ('composition-from-source.diff', source, head)]:
    (packet / name).write_bytes(git('diff','--no-ext-diff','--no-textconv','--no-renames',a,b))
(packet / 'history.log').write_bytes(git('log','-25','--format=%H %P %s',head))
trees = {rev:git('rev-parse',rev+'^{tree}').decode().strip() for rev in (head,parent,source,source_base,dev)}
assert trees[parent] == trees[dev]
(packet / 'tree-identities.json').write_text(json.dumps(trees, indent=2) + '\n')
print('Stated live-dev tree equals candidate first-parent tree:', trees[parent])
print('Raw diffs, history and five tree identities retained.')
