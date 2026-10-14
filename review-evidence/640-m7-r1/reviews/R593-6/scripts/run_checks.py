#!/usr/bin/env python3
"""Run the three authorized documentation checks concurrently in foreground."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time
p=argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("output", type=Path)
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
checks=[("docs-check",[sys.executable,"scripts/docs_check.py"]),
        ("ci-events-check",[sys.executable,"scripts/ci_events.py","--check"]),
        ("doc-style",[sys.executable,"scripts/check_doc_style.py"])]
def run(item):
    name,cmd=item
    started=time.time()
    with (a.output/(name+".log")).open("wb") as log:
        r=subprocess.run(cmd,cwd=a.repo,stdout=log,stderr=subprocess.STDOUT,
                         env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
    (a.output/(name+".rc")).write_text(str(r.returncode)+"\n")
    return {"name":name,"command":cmd,"rc":r.returncode,"seconds":round(time.time()-started,3)}
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,checks))
(a.output/"focused-checks.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
raise SystemExit(any(r["rc"] for r in results))
