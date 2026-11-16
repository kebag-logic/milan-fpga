#!/usr/bin/env python3
"""Record both-parent composition diffs and verify the declared pin moves."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), '--no-replace-objects', *args])
def pins(rev):
    return {name: oid for line in git('ls-tree', '-r', rev).decode().splitlines()
            for mode, kind, oid, name in [line.split()] if mode == '160000'}

head = '6ceed75374210935cff4f10d014b9a5ef137615e'
states = {r:pins(r) for r in ('659d7687','6b66f66d','62625941','70f4056f','10b2fe21',head)}
for path, oid in states['659d7687'].items():
    expected = states['6b66f66d'][path] if path in ('gptp-processor','protocol-processor') else oid
    assert states[head][path] == expected
assert states['62625941'] == states['10b2fe21'] == states[head]
for sub in ('gptp-processor','protocol-processor'):
    subprocess.run(['git','-C',str(root/sub),'merge-base','--is-ancestor',
                    states['659d7687'][sub],states[head][sub]],check=True)
subprocess.run(['git','-C',str(root/'third_party/tsn-c-stack'),'merge-base','--is-ancestor',
                states['6b66f66d']['third_party/tsn-c-stack'],states[head]['third_party/tsn-c-stack']],check=True)
out = {'pins':states,'merges':[]}
for merge in ('62625941','10b2fe21'):
    parents = git('show','-s','--format=%P',merge).decode().split()
    remerge = git('show','--format=','--remerge-diff',merge)
    paths = [line.split(' b/',1)[1] for line in remerge.decode().splitlines() if line.startswith('diff --git ')]
    details=[]
    for path in paths:
        comparisons=[]
        for parent in parents:
            diff=git('diff','--no-ext-diff','--no-textconv',parent,merge,'--',path)
            comparisons.append({'parent':parent,'diff_bytes':len(diff),'diff_sha256':hashlib.sha256(diff).hexdigest()})
        details.append({'path':path,'comparisons':comparisons})
    out['merges'].append({'merge':merge,'parents':parents,'conflict_paths':details,
                          'remerge_hunks':sum(l.startswith(b'@@ ') for l in remerge.splitlines())})
assert len(out['merges'][0]['conflict_paths']) == 10
assert len(out['merges'][1]['conflict_paths']) == 2
print(json.dumps(out,indent=2))
print('PASS declared pins, fast-forwards, and both-parent conflict census')
