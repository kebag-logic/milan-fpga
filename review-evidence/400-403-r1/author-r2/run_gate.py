import json, os, subprocess, sys, time
from pathlib import Path
out=Path(__file__).resolve().parent
name=sys.argv[1]
cmd=sys.argv[2:]
start=time.time()
head=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
print("START",name,cmd,flush=True)
with (out/(name+".log")).open("w") as log:
 log.write("HEAD: "+head+"\nCOMMAND: "+repr(cmd)+"\n"); log.flush()
 result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=14400)
rc=result.returncode
record=dict(name=name,command=cmd,head=head,exit=rc,seconds=round(time.time()-start,2),log=name+".log")
with (out/"gate-results.jsonl").open("a") as f:f.write(json.dumps(record)+"\n")
print(json.dumps(record),flush=True)
print("\n".join((out/(name+".log")).read_text(errors="replace").splitlines()[-30:]))
sys.exit(rc)
