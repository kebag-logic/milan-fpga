#!/usr/bin/env python3
"""Focused round-9 checks; all disposable outputs stay beneath packet/scratch."""
import argparse, os, shutil, sys
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--packet',type=Path,required=True)
ap.add_argument('--mode',choices=['native','plants','a0'],required=True)
ap.add_argument('--interfaces',type=int,default=1)
ap.add_argument('--compiler',choices=['gcc','clang','asan'],default='gcc')
ap.add_argument('--jobs',type=int,default=4)
a=ap.parse_args(); repo=a.repo.resolve(); packet=a.packet.resolve()
sys.dont_write_bytecode=True
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_build as cb, ctrl_arms, srp_arms, srp_mutants, ctrl_mutants, fw_gtest
work=packet/'scratch'/f'{a.mode}-if{a.interfaces}-{a.compiler}'
work.mkdir(parents=True,exist_ok=True)
if a.compiler=='clang': os.environ.update(CC='clang',CXX='clang++')
else: os.environ.update(CC='gcc',CXX='g++')
print(fw_gtest.toolchain(),flush=True)
build=fw_gtest.Build(jobs=a.jobs,address_sanitizer=a.compiler=='asan')
tree=cb.Tree(cb.CTRL,work/'build',work/'reuse',build)
if a.mode=='native':
    failed=False
    for suite in ('srp_mbx.cpp','srp_rx_retry.cpp','srp_app.cpp','test_acmp_mbx.cpp','srp_latency.cpp','srp_walk.cpp'):
        result=srp_arms.arm_srp(tree,repo/'third_party/lwSRP',a.interfaces,test=suite)
        print(result.arm,result.rc,result.log,flush=True)
        failed |= result.rc != 0
    sys.exit(int(failed))
if a.mode=='plants':
    srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(('binding-','srp-bound-','four-way-')))
    sys.exit(int(srp_mutants.campaign(work/'campaign',repo/'third_party/lwSRP',a.jobs,a.interfaces)))
if a.mode=='a0':
    # Build only the actual A0 case, with both pristine and planted C11 cores.
    mutant=next(m for m in ctrl_mutants.MUTANTS if m.name=='acmp-init-too-many-sources')
    for plant in (False,True):
        src=work/('mutant' if plant else 'pristine')/'ctrl'
        shutil.copytree(cb.CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
        if plant:
            target=src/mutant.path; text=target.read_text(); assert text.count(mutant.old)==1
            target.write_text(text.replace(mutant.old,mutant.new))
        t=cb.Tree(src,src.parent/'build',work/'reuse',build)
        objs=cb.compile_c(t,cb.sources(t,cb.PORTABLE),'acmp',ctrl_arms.REENTRY_ASSERT)
        objs+=cb.compile_c(t,cb.sources(t,cb.HOST),'host',measured=False)
        objs+=cb.compile_tests(t,('test_acmp.cpp',),'tests')
        exe=cb.link(t,'a0',objs)
        ok,log=fw_gtest.run_binary(exe,['--gtest_filter=AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold'])
        print('MUTANT' if plant else 'PRISTINE',log,flush=True)
        assert 'AddressSanitizer:' not in log and 'runtime error:' not in log
        if plant:
            assert not ok and ctrl_mutants.caught(mutant.test,mutant.needle,cb.Outcome('acmp',1,log))
        else: assert ok
    print('A0 pristine PASS; acmp-init-too-many-sources CAUGHT by named A0 assertion; no memory diagnostic',flush=True)
