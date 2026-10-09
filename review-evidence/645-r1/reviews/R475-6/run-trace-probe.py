#!/usr/bin/env python3
"""Run focused checks concurrently and wait for all children in the foreground."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os, subprocess, sys, time, json
root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
sim=os.environ["REVIEW_SIM"]
env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
def task(name,cwd,commands):
    start=time.monotonic()
    (out/(name+".commands.json")).write_text(json.dumps(commands,indent=2)+"\n")
    rc=0
    with (out/(name+".log")).open("w") as log:
        for cmd in commands:
            log.write("COMMAND "+json.dumps(cmd)+"\n"); log.flush()
            rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
            if rc: break
    (out/(name+".rc")).write_text(str(rc)+"\n")
    (out/(name+".seconds")).write_text(f"{time.monotonic()-start:.3f}\n")
    print(name,"rc",rc,flush=True)
    return rc
scratch=out/"scratch"
shared=["make","-j16", "VERILATOR="+str(out/"sim-cap.py"),"VERILATOR_JOBS=4"]
exe=str(scratch/"follow/Vfollow_ring")
tasks=[("trace-probe",root,[[exe,"--case","pullin","--latency-us","210.42","--after-s","1.5","--trace",str(out/"trace-pdus.csv"),"--servo-trace",str(out/"trace-servo.csv")]])]
with ThreadPoolExecutor(max_workers=1) as pool:
    codes=list(pool.map(lambda t:task(*t),tasks))
if not any(codes):
    codes.append(task("trace-table",root,[["python3","tb/verilator/follow_ring/trace_table.py",str(out/"trace-probe.log"),str(out/"trace-pdus.csv"),str(out/"trace-servo.csv"),"--origin-s","4.6","--from-s","0","--to-s","1.5","--step-s","0.1","--csv",str(out/"trace-table.csv")]]))
sys.exit(int(any(codes)))
