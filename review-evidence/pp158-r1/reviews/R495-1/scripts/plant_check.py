#!/usr/bin/env python3
"""Plant-only coverage of every published source mutation arm, with raw records."""
import argparse, ast, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys
p=argparse.ArgumentParser();p.add_argument("--repo",type=pathlib.Path,required=True);p.add_argument("--packet",type=pathlib.Path,required=True);a=p.parse_args()
root=a.repo.resolve();packet=a.packet.resolve();scratch=packet/"scratch";tree=scratch/"plant-tree";tree.mkdir(exist_ok=True)
os.environ["PYTHONDONTWRITEBYTECODE"]="1";sys.dont_write_bytecode=True
records=[]
def module(rel):
 spec=importlib.util.spec_from_file_location(rel.replace("/","_").replace(".","_"),root/rel)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def record(group,name,ok,**details):
 row=dict(group=group,name=name,passed=bool(ok),**details);records.append(row)
 print(json.dumps(row),flush=True)

# All patches check against one unchanged extraction. No patch is cumulatively applied.
subprocess.run(["git","-C",str(root),"archive","HEAD","--output",str(scratch/"plant-head.tar")],check=True)
subprocess.run(["tar","-xf",str(scratch/"plant-head.tar"),"-C",str(tree)],check=True)
for patch in sorted((root/"tb").rglob("*.patch")):
 r=subprocess.run(["git","apply","--check",str(patch)],cwd=tree,capture_output=True,text=True)
 record("patch",str(patch.relative_to(root)),r.returncode==0,rc=r.returncode,diagnostic=r.stderr.strip())
for rel in ("tb/pp_top/notify_mutants.py","tb/pp_top/d3_mutants.py","tb/pp_top/acmp_mutants.py"):
 m=module(rel)
 for arm in m.MUTANTS:
  files={f for f,_,_ in arm.edits}
  for f in files:(tree/f).write_bytes((root/f).read_bytes())
  refusal=m.plant(tree,arm.edits)
  changed={f:hashlib.sha256((tree/f).read_bytes()).hexdigest() for f in files}
  record("plant",rel+":"+arm.name,not refusal,diagnostic=refusal,planted_sha256=changed)
  for f in files:(tree/f).write_bytes((root/f).read_bytes())

m=module("tb/acmp_talker/retry_mutants.py");source=(root/m.RTL).read_text()
for name in m.MUTATIONS:
 try:
  mutated=m.mutated_source(source,name);record("other","retry:"+name,mutated!=source,sha256=hashlib.sha256(mutated.encode()).hexdigest())
 except Exception as e:record("other","retry:"+name,False,diagnostic=str(e))
# The driver's two first-occurrence bench instrumentation replacements.
astree=ast.parse((root/"tb/acmp_talker/retry_mutants.py").read_text())
for n in ast.walk(astree):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="bfm" and n.func.attr=="replace":
  old,new=map(ast.literal_eval,n.args[:2]);s=(root/"tb/acmp_talker/sim_main.cpp").read_text()
  record("other","retry-bench:"+str(n.lineno),s.count(old)==1,anchor_count=s.count(old),sha256=hashlib.sha256(s.replace(old,new,1).encode()).hexdigest())
for name,rel,old,new,count,_ in module("tb/pp_top/gsi_mutants.py").mutations():
 s=(root/rel).read_text();record("other","gsi:"+name,s.count(old)==count,anchor_count=s.count(old),expected=count,sha256=hashlib.sha256(s.replace(old,new).encode()).hexdigest())
# Read the name-write driver's literal anchor and replacement from its source.
mod=ast.parse((root/"tb/pp_top/name_wr_mutant.py").read_text())
old=next(ast.literal_eval(n.value) for n in ast.walk(mod) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="export" for t in n.targets))
new=next(ast.literal_eval(n.args[1]) for n in ast.walk(mod) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="replace" and isinstance(n.args[0],ast.Name) and n.args[0].id=="export")
s=(root/"hdl/aecp/KL_aecp_engine.sv").read_text();record("other","name-write:decode",s.count(old)==1,anchor_count=s.count(old),sha256=hashlib.sha256(s.replace(old,new).encode()).hexdigest())
m=module("tb/srp_admission/mutants.py")
for name,edits,_ in m.MUTANTS:
 s=(root/m.ADMISSION).read_text();counts=[]
 for old,new,count in edits:
  counts.append((s.count(old),count));s=s.replace(old,new)
 record("other","admission:"+name,all(x==y for x,y in counts),counts=counts,sha256=hashlib.sha256(s.encode()).hexdigest())
counts={g:sum(r["group"]==g for r in records) for g in ("patch","plant","other")}
print("COUNTS",json.dumps(counts),"FAILURES",sum(not r["passed"] for r in records))
(packet/"receipts/planting.json").write_text(json.dumps(records,indent=2)+"\n")
assert counts==dict(patch=277,plant=199,other=96),counts
assert all(r["passed"] for r in records)
