#!/usr/bin/env python3
"""Focused read-only pin, document and evidence checks; no full banks.
Usage: python3 checks.py REPO OUTPUT
"""
import concurrent.futures, os, pathlib, subprocess,sys
repo,out=(pathlib.Path(s).resolve() for s in sys.argv[1:])
checks={
"gptp-docs":["python3","scripts/check_gptp_docs.py"],
"submodule-docs":["python3","scripts/check_submodule_docs.py"],
"boundary-diagram":["python3","docs/diagrams/submodule_boundaries.gen.py","--check"],
"timesync-diagram":["python3","docs/diagrams/timesync_chain.gen.py","--check"],
"whitespace":["git","diff","--check","300da99beed5bb1c77e4b04af0bb4f9369856e0d","HEAD"],
}
def run(item):
 name,args=item
 env=os.environ.copy();env["PYTHONDONTWRITEBYTECODE"]="1"
 r=subprocess.run(args,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,text=True)
 (out/(name+".log")).write_text("COMMAND "+" ".join(args)+"\n"+r.stdout.replace(str(repo),"<source>"))
 (out/(name+".rc")).write_text(str(r.returncode)+"\n")
 return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for result in pool.map(run,checks.items()): print(*result)
