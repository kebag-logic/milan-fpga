#!/usr/bin/env python3
"""Reproduce focused exact-head checks; all children are joined before exit."""
import argparse, concurrent.futures, os, pathlib, subprocess, time
p=argparse.ArgumentParser(); p.add_argument("repo",type=pathlib.Path); p.add_argument("--compiler",required=True); a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent; scratch=root/"scratch"; scratch.mkdir(exist_ok=True)
logs=root/"receipts"; logs.mkdir(exist_ok=True)
def run(name,cmd,cwd):
    start=time.monotonic()
    with (logs/(name+".log")).open("w") as f:
        f.write("COMMAND: "+repr(cmd)+"\n"); f.flush()
        rc=subprocess.call(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    (logs/(name+".rc")).write_text(str(rc)+"\n")
    print(name, "rc",rc,"seconds",round(time.monotonic()-start,1),flush=True)
    return rc
suite=a.repo/"tb/verilator/media_phase"
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    fs=[ex.submit(run,n,["make","-j16",target,"VERILATOR="+a.compiler,"VERILATOR_JOBS=8",var+"="+str(scratch/n)],suite) for n,target,var in [("phase-build","build","MDIR"),("pins-build","pins-build","PIN_MDIR")]]
    if any(f.result() for f in fs): raise SystemExit(1)
cases="engage engage2 step ramp holdover internal mr slew burst carry".split()
with concurrent.futures.ThreadPoolExecutor(max_workers=11) as ex:
    fs=[ex.submit(run,"case-"+c,[str(scratch/"phase-build/Vmedia_phase"),"+case="+c],suite) for c in cases]
    fs.append(ex.submit(run,"pins",[str(scratch/"pins-build/Vpin_wrap")],suite))
    rc=any(f.result() for f in fs)
raise SystemExit(int(rc))
