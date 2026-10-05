#!/usr/bin/env python3
"""Foreground, bounded focused checks at the supplied source checkout (no source edits)."""
import argparse, concurrent.futures, importlib.util, json, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("packet",type=Path);p.add_argument("--verilator",required=True);p.add_argument("--jobs",type=int,default=3);p.add_argument("--phase",choices=["clean","mutants"],required=True);a=p.parse_args()
assert 1<=a.jobs<=3
src=a.source.resolve(); packet=a.packet.resolve();scratch=packet/"scratch"; receipts=packet/"receipts"
env=os.environ.copy();env["TMPDIR"]=str(scratch);env["VERILATOR"]=a.verilator;env["VERILATOR_JOBS"]="4";env["MAKEFLAGS"]="--no-print-directory -j16"
version=subprocess.check_output([a.verilator,"--version"],env=env,text=True).strip();assert "Verilator 5.050" in version,version
(receipts/"compiler-identity.txt").write_text(version+"\n")
spec=importlib.util.spec_from_file_location("campaign",src/"tb/verilator/milan_dp/dynmap_mutants.py");mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def command(tag,cmd,cwd):
 start=time.monotonic();path=receipts/(tag+".log")
 with path.open("w") as log:
  log.write("COMMAND "+json.dumps(cmd)+"\n");log.flush()
  try: rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=580).returncode
  except subprocess.TimeoutExpired: rc=124
 elapsed=time.monotonic()-start;(receipts/(tag+".rc")).write_text(str(rc)+"\n")
 print(json.dumps({"task":tag,"rc":rc,"seconds":round(elapsed,2)}),flush=True)
 return rc,path.read_text()
def lane(leg,mut=None):
 suite,target,mvar,clean,exe,args,keep=mod.LEGS[leg]
 tag="clean-"+leg if mut is None else "mutant-"+str(mut+1)
 work=scratch/tag;work.mkdir(exist_ok=True)
 dp=src/"hdl/milan/milan_datapath.sv"
 if mut is not None:
  _,name,edits,check=mod.MUTATIONS[mut];dp=mod.plant(name,edits,work,tag);assert dp
 mdir=work/"obj"
 cmd=["make","--no-print-directory","-j16",target,f"VERILATOR={a.verilator}","VERILATOR_JOBS=4",f"DP_SRC={dp}",f"{mvar}={mdir}"]
 rc,_=command(tag+"-build",cmd,suite)
 if rc: return {"task":tag,"result":"BUILD_FAILED","rc":rc}
 rc,out=command(tag+"-run",[str(mdir/exe),*args],suite)
 want=None if mut is None else mod.MUTATIONS[mut][3]
 verdict=mod.verdict(rc,out,want)
 return {"task":tag,"result":verdict,"expected":"pass" if mut is None else "caught","named_check":want}
jobs=[(k,None) for k in mod.LEGS] if a.phase=="clean" else [(m[0],i) for i,m in enumerate(mod.MUTATIONS)]
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
 results=list(pool.map(lambda x:lane(*x),jobs))
(receipts/(a.phase+"-summary.json")).write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2),flush=True)
raise SystemExit(0 if all(x["result"]==x.get("expected") for x in results) else 1)
