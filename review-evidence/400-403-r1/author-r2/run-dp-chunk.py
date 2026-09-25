import json, os, shlex, subprocess, sys, time
from pathlib import Path
p=Path(__file__).resolve().parent
root=Path("$LANES/400-403-declaration-truth")
env=os.environ.copy();env["PATH"]="$VALIDATION_STORAGE/400-403-a313-tools/bin:"+env["PATH"];env["PYTHONUNBUFFERED"]="1"
commands=json.loads((p/"milan-dp-commands.json").read_text())
for index in range(int(sys.argv[1]),int(sys.argv[2])+1):
 command=commands[index];args=shlex.split(command)
 name=f"milan-dp-{index:02}"
 head=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
 start=time.time();print("START",name,command[:120],flush=True)
 with (p/(name+".log")).open("w") as log:
  log.write("HEAD: "+head+"\nCOMMAND: "+command+"\n");log.flush()
  result=subprocess.run(args,cwd=root/"tb/verilator/milan_dp",env=env,stdout=log,stderr=subprocess.STDOUT,timeout=14400)
 record=dict(name=name,command=command,head=head,exit=result.returncode,seconds=round(time.time()-start,2),log=name+".log")
 with (p/"gate-results.jsonl").open("a") as f:f.write(json.dumps(record)+"\n")
 print(json.dumps({k:v for k,v in record.items() if k!="command"}),flush=True)
 print("\n".join((p/(name+".log")).read_text(errors="replace").splitlines()[-6:]),flush=True)
 if result.returncode:sys.exit(result.returncode)
