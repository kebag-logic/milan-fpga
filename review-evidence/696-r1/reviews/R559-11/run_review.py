#!/usr/bin/env python3
"""Focused, read-only source review campaigns; all builds live in packet scratch."""
import argparse, concurrent.futures, importlib.util, json, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--root",type=Path,required=True)
p.add_argument("--verilator",required=True)
p.add_argument("--jobs",type=int,default=2)
a=p.parse_args()
root=a.root.resolve(); packet=Path(__file__).resolve().parent
scratch=packet/"scratch"; scratch.mkdir(exist_ok=True)
receipts=packet/"receipts"; receipts.mkdir(exist_ok=True)
env=dict(os.environ,VERILATOR=a.verilator,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1")
assert 1<=a.jobs<=2
spec=importlib.util.spec_from_file_location("maap_cases",root/"tb/verilator/maap/mutants.py")
cases=importlib.util.module_from_spec(spec); spec.loader.exec_module(cases)
source=(root/"hdl/ieee1722/maap/KL_maap.sv").read_text()
def run(name,argv,cwd):
    start=time.monotonic()
    with (receipts/(name+".log")).open("w") as log:
        log.write("command: "+json.dumps(argv)+"\n"); log.flush()
        rc=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (receipts/(name+".rc")).write_text(str(rc)+"\n")
    print(name,"rc",rc,"seconds",round(time.monotonic()-start,1),flush=True)
    return rc

def case(case, integration=False):
    name,anchor,replacement,failure=case
    if anchor is not None:
        assert source.count(anchor)==1,(name,"anchor")
        text=source.replace(anchor,replacement)
    else: text=source
    work=scratch/name; work.mkdir(exist_ok=True)
    rtl=work/"KL_maap.sv"; rtl.write_text(text)
    obj=work/"obj"
    target="integration-build" if integration else "build"
    directory="DP_MDIR" if integration else "MDIR"
    argv=["make","-j16","-s","-C",str(root/"tb/verilator/maap"),target,
          "VERILATOR="+a.verilator,"VERILATOR_JOBS="+("4" if integration else "2"),
          "MAAP_RTL="+str(rtl),directory+"="+str(obj)]
    built=run(name+"-build",argv,root)
    if built: return False
    exe=obj/("maap_integration" if integration else "VKL_maap_sim")
    rc=run(name+"-run",[str(exe)],obj)
    log=(receipts/(name+"-run.log")).read_text()
    good=(rc==0 and "0 failures" in log) if failure is None else (rc==1 and "[FAIL] "+failure in log)
    print("ACCEPT" if good else "REJECT",name,flush=True)
    return good

def units():
    if not case(("unit-control",None,None,None)): return False
    rows=[(n,old,new,f) for n,item,old,new,f in cases.MUTANTS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results=list(pool.map(case,rows))
    print("unit mutation detections",sum(results),"/",len(results),flush=True)
    return all(results)

def integration():
    rows=[("integration-control",None,None,None),*cases.DATAPATH_MUTANTS]
    results=[case(row,True) for row in rows]
    print("integration accepted rows",sum(results),"/",len(results),flush=True)
    return all(results)

def differential():
    return run("differential",["python3",str(root/"sw/firmware/ctrl/test/maap_differential.py"),
        "--self-test","--keep",str(scratch/"differential")],root)==0

print(subprocess.check_output([a.verilator,"--version"],text=True).strip(),flush=True)
print("Maximum concurrent compile workers: 4 unit + 4 integration + 8 differential = 16",flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(lambda fn:fn(),[units,integration,differential]))
(packet/"campaign-summary.json").write_text(json.dumps(dict(zip(["units","integration","differential"],results)),indent=2)+"\n")
raise SystemExit(0 if all(results) else 1)
