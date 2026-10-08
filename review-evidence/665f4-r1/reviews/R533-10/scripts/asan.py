#!/usr/bin/env python3
import sys,shutil,os,json,argparse,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path.cwd());ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args();r=a.source.resolve();p=a.packet.resolve();sys.path.insert(0,str(r/'sw/firmware/ctrl/test'))
import ctrl_build,ctrl_arms,ctrl_mutants,srp_arms,fw_gtest
m=next(m for m in ctrl_mutants.MUTANTS if m.name=='acmp-init-too-many-sources')
summary=[]
for cc,cxx in [('gcc','g++'),('clang','clang++')]:
 os.environ.update(CC=cc,CXX=cxx,ASAN_OPTIONS='detect_leaks=0:halt_on_error=1')
 out=p/'scratch'/f'asan-{cc}';src=out/'ctrl';build=fw_gtest.Build(jobs=a.jobs,address_sanitizer=True)
 for plant in [False,True]:
  shutil.copytree(ctrl_build.CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
  if plant:
   target=src/m.path;data=target.read_text();assert data.count(m.old)==1;target.write_text(data.replace(m.old,m.new))
  tree=ctrl_build.Tree(src,out/'build',out/'reuse',build)
  from ctrl_reuse import cut_reuse
  cut_reuse(tree.reuse)
  result=ctrl_arms.arm_acmp(tree);label=f'asan-{cc}-a0-'+('plant' if plant else 'control')
  (p/'receipts'/(label+'.log')).write_text(result.log)
  diagnostic='A0 more sources than ACMP_MAX_SOURCES are refused'
  ok=(result.rc==1 and diagnostic in result.log and '[FAIL] AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold:' in result.log) if plant else result.rc==0
  ok=ok and 'ERROR: AddressSanitizer' not in result.log
  summary.append({'name':label,'rc':result.rc,'ok':ok});print(summary[-1],flush=True)
 for i in [1,2]:
  for suite in ['test_acmp_mbx.cpp','srp_app.cpp']:
   tree=ctrl_build.Tree(ctrl_build.CTRL,out/'srp',out/'srp-reuse',build)
   result=srp_arms.arm_srp(tree,r/'third_party/lwSRP',i,test=suite);label=f'asan-{cc}-{suite}-if{i}'
   (p/'receipts'/(label+'.log')).write_text(result.log)
   summary.append({'name':label,'rc':result.rc,'ok':result.rc==0});print(summary[-1],flush=True)
 syms=[]
 for exe in list(out.rglob('suite')) + list(out.rglob('test_acmp')):
  nm=subprocess.run(['nm',str(exe)],capture_output=True,text=True,check=True).stdout
  syms.append({'binary':str(exe.relative_to(out)),'instrumented':'__asan_' in nm})
 (p/'receipts'/f'asan-{cc}-instrumentation.json').write_text(json.dumps(syms,indent=2)+'\n')
 assert syms and all(x['instrumented'] for x in syms)
(p/'receipts/asan-results.json').write_text(json.dumps(summary,indent=2)+'\n');sys.exit(int(not all(x['ok'] for x in summary)))
