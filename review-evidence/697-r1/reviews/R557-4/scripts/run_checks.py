#!/usr/bin/env python3
"""Run independent source checks with bounded concurrent workers and saved receipts."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=pathlib.Path,required=True); ap.add_argument('--packet',type=pathlib.Path,required=True); a=ap.parse_args()
r=a.repo.resolve(); p=a.packet.resolve(); work=p/'scratch/checks'; work.mkdir(parents=True,exist_ok=True)
receipts=p/'receipts/checks'; receipts.mkdir(parents=True,exist_ok=True)
tmp=work/'tmp'; tmp.mkdir(exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith('GTEST_')}; env.update(TMPDIR=str(tmp),PYTHONDONTWRITEBYTECODE='1',ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1')
results=[]
def run(name,cmd):
 start=time.time()
 with (receipts/(name+'.log')).open('w') as f:
  f.write('COMMAND '+json.dumps(cmd)+'\n'); f.flush()
  try: rc=subprocess.run(cmd,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=540).returncode
  except subprocess.TimeoutExpired: rc=124
 (receipts/(name+'.rc')).write_text(str(rc)+'\n'); row={'name':name,'rc':rc,'seconds':round(time.time()-start,2)}; results.append(row); print(json.dumps(row),flush=True); return rc

def native(name,cc,cxx,options):
 b=work/name
 if run(name+'-configure',['cmake','-S',str(r),'-B',str(b),'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_C_COMPILER='+cc,'-DCMAKE_CXX_COMPILER='+cxx,*options]): return
 if run(name+'-build',['cmake','--build',str(b),'-j4']): return
 if run(name+'-test',['ctest','--test-dir',str(b),'--output-on-failure','-j4']): return
 if name=='gcc':
  run('coverage',['python3','scripts/coverage.py',str(b)])
  run('traceability',['python3','scripts/traceability.py','--selftest','--build',str(b),'--jobs','4'])
  run('test-inventory',['python3','scripts/test_inventory.py','--build',str(b),'--jobs','4'])
def small():
 run('rv32',['python3','scripts/baremetal.py','--work',str(work/'rv32'),'--jobs','1'])
 run('boundary',['python3','scripts/check_boundary.py','--selftest','--work',str(work/'boundary'),'--jobs','2'])
 for script in ['check_comments','needle_audit','check_port_contracts','check_license']:
  run(script,['python3','scripts/'+script+'.py','--selftest'])
 for script in ['coverage_selftest','check_privacy']:
  run(script,['python3','scripts/'+script+'.py'])
 run('registration-controls',['python3','scripts/registration_selftest.py','--work',str(work/'registration-controls')])
 run('mutation-controls',['python3','scripts/mutation_selftest.py','--work',str(work/'mutation-controls'),'--jobs','2'])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(native,'gcc','gcc','g++',['-DTSN_COVERAGE=ON']),pool.submit(native,'clang','clang','clang++',['-DTSN_SANITIZERS=ON']),pool.submit(run,'mutation',['python3','scripts/mutation.py','--work',str(work/'mutations'),'--jobs','6']),pool.submit(small)]
 for f in futures: f.result()
run('static-analysis',['python3','scripts/static_analysis.py'])
(receipts/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(x['rc'] for x in results))
