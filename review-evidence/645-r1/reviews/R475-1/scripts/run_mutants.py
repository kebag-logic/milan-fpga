#!/usr/bin/env python3
"""Run all five existing follow-ring fault controls with bounded concurrency."""
import os,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
C=P/"scratch/tb/verilator/follow_ring"
V=os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
env=dict(os.environ,VERILATOR=V,VERILATOR_JOBS="2",MAKEFLAGS="-j16",PYTHONDONTWRITEBYTECODE="1")
command=["python3","-B","mutants.py","--mdir",str(P/"scratch/follow-mutants"),"--jobs","1"]
with (P/"receipts/follow-mutants.log").open("w") as log:
 print("COMMAND",command,file=log,flush=True)
 rc=subprocess.run(command,cwd=C,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(P/"receipts/follow-mutants.rc").write_text(str(rc)+"\n")
print("follow-mutants",rc,flush=True)
raise SystemExit(rc)
