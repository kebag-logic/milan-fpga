import hashlib, json, os, subprocess, sys, time
from pathlib import Path
out=Path(__file__).resolve().parent
root=Path("$LANES/545-crf-servo-slew")
here=root/"tb/verilator/milan_dp"
os.environ["PATH"]="$VALIDATION_TOOLS/verilator-v5.050/bin:"+os.environ["PATH"]
os.environ["VERILATOR"]="$VALIDATION_TOOLS/verilator-v5.050/bin/verilator"
os.environ["VERILATOR_JOBS"]="8"
if sys.argv[1]=="plan":
    result=subprocess.run(["make","--no-print-directory","-n","run","VERILATOR_JOBS=8"],cwd=here,capture_output=True,text=True,check=True,timeout=180)
    (out/"sweep-plan.txt").write_text(result.stdout)
    logical=result.stdout.replace("\\\n", " ").splitlines()
    commands=[line for line in logical if line.strip() and not line.startswith("echo ")]
    (out/"sweep-plan.json").write_text(json.dumps(commands,indent=2))
    print(len(commands),"commands",flush=True)
    for i,c in enumerate(commands): print(i,c[:130],flush=True)
else:
    start,end=map(int,sys.argv[1:3])
    commands=json.loads((out/"sweep-plan.json").read_text())
    for i in range(start,min(end,len(commands))):
        t=time.time()
        with (out/f"sweep-{i:02d}.log").open("w") as f:
            result=subprocess.run(["bash","-e","-c",commands[i]],cwd=here,stdout=f,stderr=subprocess.STDOUT,timeout=14400)
        row={"index":i,"command":commands[i],"rc":result.returncode,"seconds":round(time.time()-t,2)}
        with (out/"sweep-results.jsonl").open("a") as f: f.write(json.dumps(row)+"\n")
        print(json.dumps({k:v for k,v in row.items() if k!="command"}),flush=True)
        if result.returncode: sys.exit(result.returncode)
