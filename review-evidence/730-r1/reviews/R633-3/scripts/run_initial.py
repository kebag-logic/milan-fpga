import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
p=Path(sys.argv[1]); repo=sys.argv[2]
checks={
"selftest": ["python3","-I","scripts/act_ci.py","--selftest"],
"ci-events-check": ["python3","scripts/ci_events.py","--check"],
"ci-events-selftest": ["python3","scripts/ci_events.py","--selftest"],
"slot-proof": ["bash","scripts/act_slot_proof.sh","--selftest"],
"py-idiom": ["python3","scripts/check_py_idiom.py"],
"docs-check": ["python3","scripts/docs_check.py"],
"doc-style": ["python3","scripts/check_doc_style.py"],
"doc-paths": ["python3","scripts/check_doc_paths.py"],
"baremetal": ["python3","scripts/check_baremetal_only.py","--check"],
}
def run(item):
 name,cmd=item; start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as out:
  r=subprocess.run(['sh',str(p/'scripts'/'reviewer_sandbox.sh'),repo,str(p),*cmd],stdout=out,stderr=subprocess.STDOUT,timeout=480)
 (p/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 result={"name":name,"command":cmd,"rc":r.returncode,"seconds":round(time.monotonic()-start,3)}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,checks.items()))
(p/'receipts'/'initial-runs.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(r['rc'] for r in results))
