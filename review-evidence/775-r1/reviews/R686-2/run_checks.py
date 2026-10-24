#!/usr/bin/env python3
"""Concurrent, foreground-owned focused review checks; no checkout edits."""
import concurrent.futures, json, os, subprocess, sys
from pathlib import Path
repo, packet, simulator = map(lambda p:Path(p).resolve(), sys.argv[1:4])
scratch=packet/'scratch'; scratch.mkdir(exist_ok=True)
receipts=packet/'receipts'; receipts.mkdir(exist_ok=True)
wrapper=scratch/'simulator'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j": a[i+1]="2"\nos.execv('+repr(str(simulator))+', ['+repr(str(simulator))+']+a)\n')
wrapper.chmod(0o755)
env=os.environ.copy(); env.update(VERILATOR=str(wrapper),MAKEFLAGS='-j16',TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1')
def run(name,cmd,cwd):
    with (receipts/(name+'.log')).open('w') as log:
        p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    (receipts/(name+'.rc')).write_text(str(p.returncode)+'\n')
    return name,p.returncode
tb=repo/'tb/verilator/avtp_rxmon'
links=[]
for n in (1,8):
    link=tb/f'obj_ls{n}'
    if link.exists() or link.is_symlink():
        raise SystemExit(f'Refusing existing build path: {link}')
    link.symlink_to(scratch/f'ls{n}'); links.append(link)
# A run-target requires relative Mdirs. Run only build targets with absolute
# scratch paths, then invoke the resulting executables directly.
def suite():
    results=[]
    for name,cmd in [
        ('nx-build',['make','-j16','nx-build',f'NX_MDIR={scratch}/nx']),
        ('nx-run',[str(scratch/'nx/Vavtp_rxmon_nx_sim')]),
        ('lockstep-build',['make','-j16','lockstep-build',f'LS_MDIR={scratch}/ls']),
        ('lockstep1',[str(scratch/'ls1/Vavtp_rxmon_lockstep')]),
        ('lockstep8',[str(scratch/'ls8/Vavtp_rxmon_lockstep')]),
        ('format-mutants',['python3','format_mutants.py']),
        ('lockstep-mutants',['python3','lockstep_mutants.py'])]:
        r=run(name,cmd,tb); results.append(r)
        if r[1]: break
    return results
tasks=[
    lambda:suite(),
    lambda:[run('probe-lock-settle',['python3','-I',str(packet/'probe_lock_settle.py'),str(repo),str(scratch/'lock-settle'),str(receipts/'lock-settle')],repo)],
    lambda:[run('behave',['behave','--no-capture','-f','plain'],repo/'tests')],
    lambda:[run('lint',['python3','scripts/lint_rtl.py','--check','--self-test','--jobs','4'],repo)],
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    result=list(pool.map(lambda fn:fn(),tasks))
(packet/'check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
for link in links: link.unlink()
