#!/usr/bin/env python3
"""Recreate only the merge tree, using a disposable index and no checkout edits.
Usage: verify_merge.py REPO PACKET
"""
import os
from pathlib import Path
import subprocess
import sys

repo,packet=map(lambda x:Path(x).resolve(),sys.argv[1:3])
def git(*args,env=None,check=True):
    return subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True,
                          env=env,check=check)
merge='e519e31ff55af7dcae253da280baad531a7ad40c'
parents=git('show','-s','--format=%P',merge).stdout.split()
assert len(parents)==2 and parents[0].startswith('30fce4b0a') and parents[1].startswith('291710b1')
r=git('merge-tree','--write-tree',*parents,check=False)
assert r.returncode==1
lines=r.stdout.splitlines()
conflicts=set()
for line in lines[1:]:
    if '\t' in line and line.split('\t')[0].endswith((' 1',' 2',' 3')):
        conflicts.add(line.split('\t',1)[1])
expected={'docs/design/AREA_BUDGET.md','docs/findings/234_PP_SHADOW_AREA_BASELINE.md',
          'docs/findings/README.md','syn/ooc/pp_resource_baseline.json'}
assert conflicts==expected,conflicts
index=packet/'scratch'/'merge.index'
index.unlink(missing_ok=True)
env=dict(os.environ,GIT_INDEX_FILE=str(index))
git('read-tree',lines[0],env=env)
for name in sorted(conflicts):
    meta,path=git('ls-tree',parents[1],'--',name).stdout.strip().split('\t')
    mode,_,oid=meta.split()
    git('update-index','--add','--cacheinfo',mode,oid,path,env=env)
actual=git('write-tree',env=env).stdout.strip()
wanted=git('rev-parse',merge+'^{tree}').stdout.strip()
assert actual==wanted,(actual,wanted)
print('PASS two-parent merge',merge)
print('Parents:',*parents)
print('Only conflict resolutions: four resource files copied exactly from second parent:')
print('\n'.join(sorted(conflicts)))
print('Reconstructed tree equals published merge tree:',wanted)
print('Final rerecord changed:',git('diff','--name-only',merge,'48f12dc1').stdout)
