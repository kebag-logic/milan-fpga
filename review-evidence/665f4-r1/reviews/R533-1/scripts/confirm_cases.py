#!/usr/bin/env python3
"""Build independent probes and source mutations exclusively in packet scratch."""
import argparse, pathlib, sys, shutil, json
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);ap.add_argument('--jobs',type=int,default=4);args=ap.parse_args()
repo=args.repo.resolve(); packet=pathlib.Path(__file__).resolve().parents[1]; scratch=packet/'scratch/probes';scratch.mkdir(exist_ok=True)
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import srp_arms, ctrl_arms, fw_gtest
from ctrl_build import Tree, CTRL, C_FLAGS, HOST, HARNESS
lw=repo/'third_party/lwSRP'; ctrl_arms.lwsrp_pin(lw)
build=fw_gtest.Build(jobs=min(args.jobs,4)); results=[]
def run_one(name,test,selected,interfaces=2,plant=None):
    out=scratch/name; out.mkdir(exist_ok=True)
    src=CTRL; lib=lw/'src'
    if plant:
        which,path,old,new=plant
        if which=='ctrl':
            src=out/'ctrl';shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
            target=src/path
        else:
            lib=out/'library-src';shutil.copytree(lw/'src',lib,dirs_exist_ok=True);target=lib/path
        original=target.read_text();assert original.count(old)==1,(name,original.count(old));target.write_text(original.replace(old,new))
        (packet/'receipts'/f'{name}-plant.json').write_text(json.dumps({'path':which+'/'+path,'old':old,'new':new,'test':selected},indent=2)+'\n')
    tree=Tree(src,out/'build',out/'reuse',build)
    variant,inc=srp_arms.prepared(tree,interfaces,out/'prepared',srp_arms.DEFAULT_ENTITY)
    inc += [f'-I{lib/"include"}',f'-I{lib}',f'-I{repo/"sw/firmware/ctrl/test"}']
    objs=fw_gtest.compile_c(build,[*C_FLAGS,'-DNDEBUG'],inc,[(variant if f.startswith('mbx/') else src)/f for f in srp_arms.SRP_SOURCES],out/'objects')
    objs+=fw_gtest.compile_c(build,C_FLAGS,inc,[src/f for f in HOST],out/'host',False)
    objs+=fw_gtest.compile_c(build,C_FLAGS,inc,[lib/f for f in srp_arms.LWSRP_SOURCES],out/'library',False)
    objs+=fw_gtest.compile_tests(build,inc,[test],out/'test')
    objs.append(fw_gtest.main_object(build,out/'main'))
    exe=fw_gtest.link(build,objs,out/'suite')
    ok,log=fw_gtest.run_binary(exe,[f'--gtest_filter={selected}'],cwd=out)
    (packet/'receipts'/f'{name}.log').write_text(log);(packet/'receipts'/f'{name}.rc').write_text('0\n' if ok else '1\n')
    print(name,'PASS' if ok else 'FAIL',flush=True); print(log[-1000:],flush=True)
    results.append({'name':name,'passed':ok,'test':selected,'planted':bool(plant)})
tests=repo/'sw/firmware/ctrl/test'
run_one('independent-cases-final',packet/'scripts/reviewer_cases.cpp','Srp.R533_*')
