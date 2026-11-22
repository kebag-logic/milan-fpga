#!/usr/bin/env python3
"""Focused checks of changed call paths; no synthesis or processor execution.
Usage: focused_delta.py checkout scratch-directory
"""
import contextlib, importlib, io, json, pathlib, subprocess, sys, tarfile
repo, work=map(pathlib.Path,sys.argv[1:]); work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/'syn/resmap')); import soc_sweep as s
assert s.selftest()==0
plan=json.loads((repo/'syn/resmap/sweep_plan.json').read_text())
original=s.yosys_sweep.load_plan
for label,value in [('split','split'),('missing',None)]:
 bad=json.loads(json.dumps(plan))
 if value: bad['soc']['placement']=value
 else: del bad['soc']['placement']
 s.yosys_sweep.load_plan=lambda *a:bad
 assert s.selftest()!=0
 print('CAUGHT plan',label)
s.yosys_sweep.load_plan=original
orig=s.missing_images; s.missing_images=lambda *a:[]
assert s.selftest()!=0; print('CAUGHT missing-image detector disabled'); s.missing_images=orig
# Real builder + prepare call, archival inputs, zero platform images.
# prepare's unrelated source-list Git bootstrap is suppressed: no exporter is run here.
tree=work/'tree'; tree.mkdir(exist_ok=True)
archive=work/'source.tar'
with archive.open('wb') as f: subprocess.run(['git','archive','HEAD'],cwd=repo,stdout=f,check=True)
with tarfile.open(archive) as f: f.extractall(tree,filter='data')
for sub in ('gptp-processor','protocol-processor','third_party/verilog-axis'):
 target=tree/sub; target.mkdir(parents=True,exist_ok=True)
 with archive.open('wb') as f: subprocess.run(['git','archive','HEAD'],cwd=repo/sub,stdout=f,check=True)
 with tarfile.open(archive) as f: f.extractall(target,filter='data')
s.git_listable=lambda tree:None
assert not list(tree.rglob('ctrl_app.elf'))
argv=s.prepare(work,'all-fabric')
assert '--ctrl-mailbox' not in argv and '--ctrl-firmware' not in argv
print('PREPARE all-fabric with no ELF: accepted, no split flags')
try: s.prepare(work,'split')
except s.yosys_sweep.PlanError as e:
 print('PREPARE split refused:',e); assert 'ctrl_app.elf' in str(e)
else: raise AssertionError('missing image accepted')
assert not (work/'soc').exists(); print('No SoC export directory written')
sys.path.insert(0,str(repo/'tb/verilator/ctrl_service_budget')); import selftest as t
rows=t.build_checks(); assert all(ok for _,ok,_ in rows)
print('HARNESS clean:',len(rows),'checks passed')
real=t.build.split_argv
for label,fn in [('append',lambda a,e:[*a,'--ctrl-mailbox','--ctrl-firmware',str(e)]),('keep config',lambda a,e:a)]:
 t.build.split_argv=fn; bad=[n for n,ok,_ in t.build_checks() if not ok]
 assert len(bad)==2; print('CAUGHT',label,'at both shapes:',bad)
t.build.split_argv=real
for args in ([],['--ctrl-mailbox','--ctrl-firmware','old.elf'],['--ctrl-firmware','a','--ctrl-mailbox','--ctrl-firmware','b']):
 result=real(args,pathlib.Path('new.elf'))
 assert result.count('--ctrl-firmware')==1 and result.count('--ctrl-mailbox')==1 and result[-1]=='new.elf'
try: real(['--ctrl-firmware'],pathlib.Path('new.elf'))
except RuntimeError: print('HARNESS dangling firmware flag refused')
else: raise AssertionError('dangling flag accepted')
print('FOCUSED DELTA PASS')
