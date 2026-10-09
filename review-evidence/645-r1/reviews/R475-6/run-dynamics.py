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
tasks=[
 ("b8",root,[[exe,"--case","b8","--dwell-s","1","--hold-s","55","--switch-hold-s","20"]]),
 ("b8-fast-wide",root,[[exe,"--case","b8","--dwell-s","1","--peer-ppm","0.82","--jitter-us","60","--set-phase","0.4375","--hold-s","55","--switch-hold-s","20","--allow-ungradable"]]),
 ("pullin",root,[[exe,"--case","pullin","--latency-us","210.42","--after-s","1.5"]]),
 ("small-pulls",root/"tb/verilator/follow_ring",[
   shared+["build","CLK_HZ=25000000","FRAME_DIV=64","MDIR="+str(scratch/"fine")],
   ["python3","small_pulls.py","--exe",str(scratch/"fine/Vfollow_ring"),"--out",str(out/"small-pull-receipts"),"--jobs","4"]])]
with ThreadPoolExecutor(max_workers=4) as pool:
    codes=list(pool.map(lambda t:task(*t),tasks))
sys.exit(int(any(codes)))
