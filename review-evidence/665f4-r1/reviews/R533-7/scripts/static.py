#!/usr/bin/env python3
"""Focused source and documentation checks with separate receipts."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve();p=Path(__file__).resolve().parents[1]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(p/'scratch'))
commands=[['python3','sw/mailbox/gen_mailbox.py','--check'],['python3','scripts/docs_check.py'],['python3','scripts/check_doc_style.py'],['python3','scripts/check_cpp_idiom.py'],['python3','scripts/check_py_idiom.py'],['python3','scripts/check_submodule_docs.py'],['git','diff','--check','db9aa8c9b135b34ff3d070a979dee70440b37cc6','HEAD']]
def run(item):
 i,cmd=item;r=subprocess.run(cmd,cwd=repo,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=200)
 (p/'receipts'/f'static-{i}.log').write_text(r.stdout.replace(str(repo),'${SOURCE}').replace(str(p),'${PACKET}'))
 print(i,r.returncode,flush=True);return {'command':cmd,'rc':r.returncode,'log':f'static-{i}.log'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,enumerate(commands)))
(p/'receipts/static.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
