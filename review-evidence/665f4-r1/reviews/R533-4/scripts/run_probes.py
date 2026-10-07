#!/usr/bin/env python3
"""Foreground parallel SRP positives and independently planted defect controls."""
import argparse, concurrent.futures, json, os, pathlib, re, shlex, shutil, sys, threading, time, traceback
p=argparse.ArgumentParser(); p.add_argument('--repo',type=pathlib.Path,required=True); p.add_argument('--packet',type=pathlib.Path,required=True); p.add_argument('--jobs',type=int,default=4)
a=p.parse_args(); assert 1<=a.jobs<=4
repo=a.repo.resolve(); packet=a.packet.resolve(); scratch=packet/'scratch/probes'; receipts=packet/'receipts'; scratch.mkdir(parents=True,exist_ok=True)
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'; os.environ['TMPDIR']=str(packet/'scratch')
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, Tree
import fw_gtest, srp_arms, srp_mutants
local=threading.local(); original_run=fw_gtest.run
# Capture command receipts from the compilation workers too, keyed by their output path.
lock=threading.Lock(); commands=[]
def run(argv,**kwargs):
    start=time.monotonic(); r=original_run(argv,**kwargs)
    with lock:commands.append({'argv':list(map(str,argv)),'cwd':str(kwargs.get('cwd') or repo),'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'stdout':r.stdout if r.returncode else '', 'stderr':r.stderr})
    return r
fw_gtest.run=run
# These sites and replacements are reviewer-selected; the campaign catalog is checked separately.
PLANTS=[
 ('RP3','JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves',
  'replacement.declared |= r->declared;', 'if (r == s) { replacement.declared |= r->declared; }','d.event','joining-binding-loses-applicant'),
 ('RP10','ReboundStreamCannotInheritAnotherStreamsReady',
  'if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0)', 'if (true)','ready','applicant-inherited-across-streams'),
 ('RP5','FinalDomainVidUnbindKeepsSrClassMembership',
  'if (old.vid != i->domain.vid && !has_sink(i,&old,false))', 'if (!has_sink(i,&old,false))','d.event','final-unbind-withdraws-domain-vid')]
for _,test,old,new,needle,name in PLANTS:
    d=next(d for d in srp_mutants.DEFECTS if d.name==name)
    assert (d.test,d.old,d.new,d.needle)==(test,old,new,needle)
def work(kind,interfaces):
    tag=f'{kind}-if{interfaces}'; root=scratch/tag; root.mkdir(parents=True,exist_ok=True)
    start=time.monotonic(); src=CTRL; test='srp_mbx.cpp'; needle=None; selected='*'
    try:
        if kind.startswith('RP'):
            _,testname,old,new,needle,_=next(x for x in PLANTS if x[0]==kind)
            src=root/'ctrl'; shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            target=src/'srp/srp_mbx.c'; source=target.read_text(); assert source.count(old)==1
            target.write_text(source.replace(old,new)); selected='Srp.'+testname; test=(test,selected)
        elif kind!='adapter':test='srp_'+kind+'.cpp'
        tree=Tree(src,root/'build',root/'reuse',fw_gtest.Build(jobs=4))
        outcome=srp_arms.arm_srp(tree,repo/'third_party/lwSRP',interfaces,test=test)
        (receipts/(tag+'.log')).write_text(outcome.log+'\n')
        (receipts/(tag+'.rc')).write_text(str(outcome.rc)+'\n')
        ok=outcome.rc==0 if needle is None else srp_mutants.caught(selected,needle,outcome)
        if needle:
            assert fw_gtest.failed_tests(outcome.log)=={selected},'unexpected failure set'
            traces=sorted(set(re.findall(r'srp_mbx.cpp:\d+: ([0-9/]+)',outcome.log)))
            expected={f'{i}/{slot}' for i in range(interfaces) for slot in range(2)} if kind!='RP5' else {f'{i}/{vid}/{slot}' for i in range(interfaces) for vid in (2,7) for slot in range(2)}
            assert expected.issubset(set(traces)),(expected,traces)
        else:traces=[]
        row={'name':tag,'passed':ok,'test_rc':outcome.rc,'selected':selected,'traces':traces,'seconds':round(time.monotonic()-start,3)}
    except Exception as e:
        (receipts/(tag+'.error.log')).write_text(traceback.format_exc());row={'name':tag,'passed':False,'error':str(e)}
    print(json.dumps(row),flush=True); return row
jobs=[(kind,i) for kind in ['adapter','walk','latency','RP3','RP10','RP5'] for i in (1,2)]
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results=list(pool.map(lambda x:work(*x),jobs))
(receipts/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
(receipts/'probe-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
sys.exit(0 if all(x['passed'] for x in results) else 1)
