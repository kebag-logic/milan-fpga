#!/usr/bin/env python3
import concurrent.futures as cf,os,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;R=pathlib.Path(sys.argv[1]).resolve()
PYTHON=os.environ.get("REVIEW_DOC_PYTHON",sys.executable)
def run(name,args):
 with (P/(name+".log")).open("w") as f:q=subprocess.run([PYTHON,*args],cwd=R,stdout=f,stderr=f)
 (P/(name+".rc")).write_text(str(q.returncode)+"\n")
 print(name,q.returncode,flush=True);assert q.returncode==0
with cf.ThreadPoolExecutor(max_workers=3) as pool:
 fs=[pool.submit(run,n,a) for n,a in [("docs-check",["scripts/docs_check.py"]),("docs-inventory",["scripts/docs_inventory.py","--check"]),("em-dash",["scripts/check_em_dash.py","--base","15168e14"])]]
 for f in fs:f.result()
