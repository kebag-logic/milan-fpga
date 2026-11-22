#!/usr/bin/env python3
"""Run ADP integration, base reproduction, walk and nine focused plants."""
import concurrent.futures as cf
import contextlib, io, json, os, pathlib, subprocess, sys
parent = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(__file__).resolve().parent
scratch = packet/'scratch'
logs = packet/'receipts'
sys.path[:0] = [str(parent/'sw/firmware/ctrl/test'), str(parent/'sw/firmware/gtest')]
import ctrl_arms, ctrl_mutants, fw_gtest
from ctrl_build import Tree, PORTABLE, firmware, compile_tests, execute, link
from ctrl_reuse import cut_reuse
base = scratch/'base-stack'
base.mkdir(exist_ok=True)
archive = subprocess.check_output(['git','-C',str(parent/'third_party/tsn-c-stack'),'archive','715589c1db7cf67e2f3259fd7083ebc7f0923376'])
subprocess.run(['tar','-x','-C',str(base)],input=archive,check=True)
def save(name, log, rc):
    log=log.replace(str(packet),'$PACKET')
    (logs/(name+'.log')).write_text(log)
    (logs/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
def baseline(mode):
    work=scratch/('parent-'+mode)
    tree=Tree(parent/'sw/firmware/ctrl',work/'build',work/'reuse',fw_gtest.Build(jobs=4),base if mode=='base' else parent/'third_party/tsn-c-stack')
    cut_reuse(tree.reuse)
    if mode=='base':
        objs=firmware(tree,PORTABLE,'adpfw')+compile_tests(tree,('test_adp.cpp',),'adpfw/tests')
        outcome=execute('adpfw',link(tree,'test_adpfw',objs))
        save('parent-base-reproduction',outcome.log,outcome.rc)
        return
    for arm in ('adp','walk'):
        outcome=getattr(ctrl_arms,'arm_'+arm)(tree)
        save('parent-'+arm,outcome.log,outcome.rc)
with cf.ThreadPoolExecutor(2) as pool: list(pool.map(baseline,('base','head')))
import adp_first_mutants
names={m.name for m in adp_first_mutants.MUTANTS}|{'gm-change-ignored'}
selected=[m for m in ctrl_mutants.MUTANTS if m.name in names]
assert len(selected)==9
work=scratch/'parent-plants'
cut_reuse(work/'reuse')
build=fw_gtest.Build(jobs=4)
results=[]
for m in selected:
    src, stack=ctrl_mutants.plant(m,work/m.name)
    tree=Tree(src,work/m.name/'build',work/'reuse',build,stack)
    for i,(arm,test,needle) in enumerate(m.kills()):
        outcome=getattr(ctrl_arms,'arm_'+arm)(tree)
        caught=ctrl_mutants.caught(test,needle,outcome)
        results.append({'plant':m.name,'arm':arm,'test':test,'needle':needle,'caught':caught,'rc':outcome.rc})
        save('plant-'+m.name+'-'+str(i),outcome.log,outcome.rc)
(logs/'parent-plants.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['caught'] for r in results)
