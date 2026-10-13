#!/usr/bin/env python3
"""Run focused composition checks concurrently; all children are joined here."""
import argparse, concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,required=True); p.add_argument("--packet",type=Path,required=True)
p.add_argument("--only",nargs="+"); p.add_argument("--python",default="python3"); p.add_argument("--summary",default="checks.json")
a=p.parse_args(); repo=a.repo.resolve(); packet=a.packet.resolve()
(packet/"receipts").mkdir(exist_ok=True); (packet/"scratch"/"tmp").mkdir(parents=True,exist_ok=True)
env={**os.environ,"TMPDIR":str(packet/"scratch"/"tmp"),"PYTHONDONTWRITEBYTECODE":"1","GIT_NO_REPLACE_OBJECTS":"1"}
checks={
 "doc-paths":["python3","scripts/check_doc_paths.py"],
 "doc-style":["python3","scripts/check_doc_style.py"],
 "python-idiom":["python3","scripts/check_py_idiom.py"],
 "docs-check":["python3","scripts/docs_check.py"],
 "toc-check":["python3","scripts/gen_toc.py","--check"],
 "toc-anchors":["python3","scripts/gen_toc.py","--verify-anchors"],
 "em-dash":["python3","scripts/check_em_dash.py","--base","d5858bbee328cf8d2c39a99ec14203f5d0ddd123"],
 "ci-events-check":["python3","scripts/ci_events.py","--check"],
 "ci-events-selftest":["python3","scripts/ci_events.py","--selftest"],
 "ci-scope-selftest":["python3","scripts/ci_scope.py","--selftest"],
 "suite-shards-selftest":["python3","scripts/suite_shards.py","--selftest"],
 "firmware-census":["python3","scripts/ci_events.py","--firmware-census"],
}
checks={name:[a.python,*cmd[1:]] for name,cmd in checks.items() if not a.only or name in a.only}
def run(item):
 name,cmd=item; start=time.monotonic()
 with (packet/"receipts"/(name+".log")).open("w") as f:
  result=subprocess.run(cmd,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=540)
 elapsed=round(time.monotonic()-start,3)
 (packet/"receipts"/(name+".rc")).write_text(str(result.returncode)+"\n")
 row={"name":name,"command":cmd,"rc":result.returncode,"seconds":elapsed}
 print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 rows=list(pool.map(run,checks.items()))
(packet/"receipts"/a.summary).write_text(json.dumps(rows,indent=2)+"\n")
sys.exit(0 if all(r["rc"]==0 for r in rows) else 1)
