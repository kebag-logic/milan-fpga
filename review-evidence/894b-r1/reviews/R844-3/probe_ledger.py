#!/usr/bin/env python3
"""Exercise real archived logs and the acceptance gate's original fault shapes."""
import copy, decimal, json, os, pathlib, subprocess, sys
repo,out,archive=map(pathlib.Path,sys.argv[1:4])
sys.path.insert(0,str(repo/"tb/verilator/ctrl_service_budget"))
import egress_ledger as e
scratch=out/"scratch"/"independent-probes"
scratch.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(out/"scratch"/"tmp"))
count=0
def invoke(label,args,want,named=None):
 global count
 r=subprocess.run([sys.executable,"-B",str(repo/"tb/verilator/ctrl_service_budget/egress_ledger.py"),"--point","8x8-1if",*map(str,args)],capture_output=True,text=True,env=env)
 text=r.stdout+r.stderr
 assert r.returncode==want and (named is None or named in text),(label,r.returncode,text)
 print(f"{label}: rc {r.returncode}, expected {want}")
 print(text)
 count+=1
# The numerical rule is derived independently using decimal milliseconds.
D=decimal.Decimal
for row,measured in e.MEASURED["8x8-1if"].items():
 want=D(60)+((D(str(measured))-D(60))*D("1.05")).quantize(D(".01"),rounding=decimal.ROUND_CEILING)
 assert D(str(e.LEDGER["8x8-1if"][row]))==want
 print(f"Independent decimal rule: {row}: {want} ms")
base=[dict(probe=n,status="measured",ms=ms,budget_ms=20,within_budget=False) for n,ms in e.LEDGER["8x8-1if"].items()]
def fixture(name,rows,refusals=None,summary=True):
 d=scratch/name;d.mkdir(exist_ok=True)
 (d/"backlog-owed.json").write_text(json.dumps(dict(group="backlog-owed",probes=rows)))
 if summary:(d/"results.json").write_text(json.dumps(dict(refusals=refusals or [])))
 return d
invoke("all seven at limit",[fixture("equal",base)],0)
for k,row in enumerate(base):
 altered=copy.deepcopy(base);altered[k]["ms"]+=0.00001
 invoke(f"one cycle over {row['probe']}",[fixture(f"cycle-{k}",altered)],1,row["probe"])
altered=copy.deepcopy(base);altered[0]["ms"]=100.0
invoke("original large miss",[fixture("large",altered)],1,"backlog.owed.if0")
new=dict(probe="independent.new.cpu.row",status="measured",ms=21,budget_ms=20,within_budget=False)
invoke("new miss",[fixture("new",base+[new])],1,"independent.new.cpu.row")
invoke("run refusal",[fixture("refused",base,["independent group: absent end"])],1,"the run refused 1")
invoke("missing run summary",[fixture("missing",base,summary=False)],1,"no results.json")
logs=sorted((archive/"author-r5/receipts/harness").glob("leg-*-a15345f7.txt"))
# Includes one additional platform SRP leg; all logs have one complete run summary.
invoke("published measured logs",logs,0)
print(f"Independent probes: {count} expected outcomes; decimal formula 7/7.")

