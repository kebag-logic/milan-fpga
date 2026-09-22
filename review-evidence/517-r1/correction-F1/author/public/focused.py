#!/usr/bin/env python3
import json,os,subprocess,sys,time
from pathlib import Path
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve();out.mkdir(exist_ok=True)
commands=[("runner",["python3","-B","tb/verilator/milan_dp/test_sim_pool.py"]),("phase",["python3","-B","tb/verilator/milan_dp/test_render_phase_observation.py"]),("policy-check",["python3","-B","scripts/check_baremetal_only.py","--check"]),("policy-selftest",["python3","-B","scripts/check_baremetal_only.py","--selftest"]),("tally-selftest",["python3","-B","scripts/suite_tally.py","--selftest"])]
rows=[]
for name,argv in commands:
    start=time.monotonic()
    with (out/(name+".stdout")).open("wb") as stdout,(out/(name+".stderr")).open("wb") as stderr:
        p=subprocess.run(argv,cwd=root,stdout=stdout,stderr=stderr,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"),timeout=120)
    rows.append({"name":name,"argv":argv,"cwd":str(root),"exit":p.returncode,"elapsed_seconds":time.monotonic()-start})
    (out/"receipts.json").write_text(json.dumps(rows,indent=2)+"\n");print(name,p.returncode,flush=True)
assert all(x["exit"]==0 for x in rows)
