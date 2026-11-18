#!/usr/bin/env python3
"""Run focused review gates; usage: run_gates.py CHECKOUT PACKET."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time
root=Path(sys.argv[1]).resolve()
packet=Path(sys.argv[2]).resolve()
logs=packet/'gates'; logs.mkdir(exist_ok=True)
scratch=packet/'scratch'; scratch.mkdir(exist_ok=True)
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
gates={
 'trace-events':['sw/trace/gen_trace_events.py','--check'],
 'inventory':['scripts/docs_inventory.py','--check'],
 'inventory-selftest':['scripts/docs_inventory.py','--selftest'],
 'docs-check':['scripts/docs_check.py'],
 'toc':['scripts/gen_toc.py','--check'],
 'anchors':['scripts/gen_toc.py','--verify-anchors'],
 'em-dash-delta':['scripts/check_em_dash.py','--base','73272666'],
 'em-dash-train':['scripts/check_em_dash.py','--base','cb96336d'],
 'doc-style':['scripts/check_doc_style.py'],
 'doc-paths':['scripts/check_doc_paths.py'],
 'hygiene':['scripts/check_hygiene.py','--check'],
 'py-idiom':['scripts/check_py_idiom.py'],
 'module-matrix':['docs/traceability/gen_module_matrix.py','--check'],
 'register-reference':['scripts/gen_register_reference.py','--check'],
 'feature-status':['scripts/check_feature_status.py'],
 'mailbox-contract':['sw/mailbox/gen_mailbox.py','--check','--crosscheck'],
 'diff-check':['GIT','diff','--check','cb96336d..b1f1161b'],
}
def run(item):
 name,args=item
 cmd=['git',*args[1:]] if args[0]=='GIT' else [sys.executable,'-B',*args]
 start=time.monotonic()
 with (logs/(name+'.log')).open('w') as out:
  out.write('$ '+ ' '.join(cmd[1:] if cmd[0]==sys.executable else cmd)+'\n');out.flush()
  r=subprocess.run(cmd,cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
 (logs/(name+'.rc')).write_text(str(r.returncode)+'\n')
 result={'name':name,'command':cmd,'rc':r.returncode,'seconds':round(time.monotonic()-start,2)}
 print(json.dumps(result),flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 selected={k:v for k,v in gates.items() if len(sys.argv)<4 or k in sys.argv[3:]}
 results=list(pool.map(run,selected.items()))
existing=json.loads((logs/'results.json').read_text()) if (logs/'results.json').exists() else []
merged={r['name']:r for r in existing}
merged.update({r['name']:r for r in results})
(logs/'results.json').write_text(json.dumps(list(merged.values()),indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in results))
