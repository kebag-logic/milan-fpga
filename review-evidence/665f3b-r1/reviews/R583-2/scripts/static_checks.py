import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
repo,packet=map(lambda v:Path(v).resolve(),sys.argv[1:3])
commands={"mailbox-generator":["python3","sw/mailbox/gen_mailbox.py","--check","--crosscheck","--selftest"],"submodule-docs":["python3","scripts/check_submodule_docs.py"],"diagram":["python3","docs/diagrams/submodule_boundaries.gen.py","--check"],"docs":["python3","scripts/docs_check.py"],"ci-scope-classification":["python3","scripts/ci_scope.py","docs/design/MAILBOX_SPLIT.md"]}
def run(item):
 name,cmd=item;t=time.monotonic()
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(packet/"scratch"))
 with (packet/"receipts"/(name+".log")).open("wb") as log:r=subprocess.run(cmd,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
 (packet/"receipts"/(name+".rc")).write_text(str(r.returncode)+"\n")
 return {"name":name,"command":cmd,"rc":r.returncode,"seconds":round(time.monotonic()-t,2)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,commands.items()))
(packet/"receipts/static-results.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2));sys.exit(any(r["rc"] for r in results))
