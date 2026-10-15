#!/usr/bin/env python3
"""Run bounded offline image controls; all child processes remain foreground."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
scratch=out/'scratch'
env=dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', CI_IMAGE_SHFMT=str(scratch/'shfmt'))
cases={
 'inventory-check':['scripts/ci_tool_inventory.py','--check'],
 'inventory-selftest':['scripts/ci_tool_inventory_selftest.py'],
 'patterns-selftest':['scripts/ci_inventory_patterns_selftest.py'],
 'nodes-selftest':['scripts/ci_inventory_nodes_selftest.py'],
 'exact-selftest':['scripts/ci_inventory_exact_selftest.py'],
 'build-selftest':['ci/image/build_selftest.py'],
 'integrity-selftest':['ci/image/integrity_selftest.py'],
 'privacy-selftest':['ci/image/privacy_selftest.py'],
 'patch-selftest':['ci/image/privacy_patch_selftest.py'],
 'lock-check':['ci/image/build.py','--work',str(scratch/'lock-check'),'--check-lock'],
}
def run(item):
 name,args=item; start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  try: result=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600); rc=result.returncode
  except subprocess.TimeoutExpired: rc=124
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 return dict(name=name,argv=['python3',*args],rc=rc,seconds=round(time.monotonic()-start,3))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,cases.items()))
(out/'controls.json').write_text(json.dumps(results,indent=2)+'\n')
for row in results: print(row)
