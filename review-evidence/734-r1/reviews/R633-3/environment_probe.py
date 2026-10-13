#!/usr/bin/env python3
"""Reproduce ambient signing and GIT_DIR probes against the complete scope gate."""
import hashlib
import os
from pathlib import Path
import subprocess

W=Path('/work');C=Path('/candidate')
v=W/'victim';v.mkdir();home=W/'caller';home.mkdir()
def git(*args):
    return subprocess.check_output(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','core.hooksPath=/dev/null','-C',str(v),*args],text=True).strip()
git('init','-q');git('commit','--allow-empty','-qm','Victim baseline')
def snapshot():
    return {str(p.relative_to(v)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (v/'.git').rglob('*') if p.is_file()}
(home/'.gitconfig').write_text('[commit]\n gpgsign = true\n[user]\n signingKey = unavailable\n')
for name,poison in [('signing',{}),('gitdir',{'GIT_DIR':str(v/'.git'),'GIT_WORK_TREE':str(v),'GIT_INDEX_FILE':str(v/'.git/index')})]:
    env=dict(os.environ,HOME=str(home),GIT_CONFIG_GLOBAL=str(home/'.gitconfig'),GIT_CONFIG_SYSTEM=str(home/'.gitconfig'),GIT_AUTHOR_NAME='Ambient identity',GIT_COMMITTER_DATE='2003-03-03T00:00:00Z',**poison)
    before=snapshot()
    result=subprocess.run(['python3','scripts/ci_scope.py','--selftest'],cwd=C,env=env,capture_output=True,text=True)
    print('PROBE',name,'rc',result.returncode,flush=True);print(result.stdout);print(result.stderr)
    assert result.returncode==0
    assert snapshot()==before,'victim changed'
    print('PASS',name,'complete scope selftest; victim Git files unchanged')
