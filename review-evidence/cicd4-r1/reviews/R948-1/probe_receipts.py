#!/usr/bin/env python3
"""Focused fault probes; synthetic records test validation, not execution evidence."""
import contextlib, copy, io, pathlib, sys
from types import SimpleNamespace
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve()
sys.path[:0]=[str(root/"sw/mailbox"),str(root/"scripts"),str(root/"sw/firmware/ctrl/test")]
import census_legs as c
import test_ctrl_firmware as f
from ci_gate_workflows import load_template, generate, rendered
import yaml
identity=("a"*40,"b"*40)
every=c.inventory()
records=[]
for leg in range(c.LEGS):
 groups=c.selection(every,leg)
 records.append(dict(schema=1,head=identity[0],tree=identity[1],leg=leg,legs=c.LEGS,
 inventory=c.names(every),selected=c.names(groups),exit=0,
 rows=[dict(arm=a.what,ok=True,line="synthetic success",through=None if a.rule is None else True)
       for h,_,riders in groups for a in (h,*riders)]))
def verdict(rs):
 try:
  with contextlib.redirect_stdout(io.StringIO()): return c.union(rs,every,identity)
 except (ValueError,TypeError,KeyError): return 1
assert verdict(records)==0
n=0
for leg,rec in enumerate(records):
 for field,value in (("exit",1),("exit",False),("head","c"*40),("tree","c"*40),("leg",True),("legs",True),("schema",True)):
  bad=copy.deepcopy(records); bad[leg][field]=value
  assert verdict(bad)!=0,(leg,field); n+=1
 assert verdict(records[:leg]+records[leg+1:])!=0; n+=1
 assert verdict(records+[rec])!=0; n+=1
 for rowno,row in enumerate(rec["rows"]):
  for field,value in (("ok",False),("ok",1),("through",None if row["through"] is not None else True)):
   bad=copy.deepcopy(records); bad[leg]["rows"][rowno][field]=value
   assert verdict(bad)!=0,(leg,rowno,field); n+=1
  bad=copy.deepcopy(records); bad[leg]["rows"].pop(rowno)
  assert verdict(bad)!=0; n+=1
  if row["through"] is not None:
   bad=copy.deepcopy(records); bad[leg]["rows"][rowno]["through"]=False
   assert verdict(bad)!=0; n+=1
print("Census synthetic negative probes refused:",n,"over",sum(len(r["rows"]) for r in records),"arms")
original=f.srp_mutants.DEFECTS
for leg in range(2):
 args=SimpleNamespace(lwsrp=root/"third_party/lwSRP",jobs=1,campaign_shard=(leg,2))
 for failing in range(3):
  results=[False]*3; results[failing]=True
  with patch.object(f.srp_mutants,"campaign",side_effect=results) as run, patch.object(f.ctrl_mutants,"lwsrp_pin_arms",return_value=0):
   assert f.run_srp_mutants(args,pathlib.Path("unused"))
   assert run.call_count==3
   assert f.srp_mutants.DEFECTS is original
 with patch.object(f.srp_mutants,"campaign",side_effect=RuntimeError("planted exception")):
  try: f.run_srp_mutants(args,pathlib.Path("unused"))
  except RuntimeError: pass
  else: raise AssertionError("exception lost")
 assert f.srp_mutants.DEFECTS is original
print("Each SRP table failure propagates, later tables still execute, and table restored after exception: PASS")
for name in ("docs","elaborate","rtl","rtl-fast"):
 assert (root/f".github/workflows/{name}.yml").read_text()==rendered(name,load_template(root,name)),name
print("All four generated workflows equal rendered bytes: PASS")
new=generate("rtl-fast",load_template(root,"rtl-fast"))
jobs=new["jobs"]
restores=[next(s for s in jobs[j]["steps"] if s.get("name")=="Restore the pinned Yosys build") for j in ("yosys-elaboration","publication-census-legs")]
assert restores[0]["with"]==restores[1]["with"]
assert restores[0]["with"]["fail-on-cache-miss"] is True
assert "restore-keys" not in restores[0]["with"]
assert "yosys-tool" in jobs["publication-census-legs"]["needs"]
print("Shared Yosys restore key/path/miss refusal and dependency: PASS")
