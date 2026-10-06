#!/usr/bin/env python3
"""Read-only planting audit; no HDL is compiled and no source checkout is edited."""
import argparse,concurrent.futures,importlib.util,json,pathlib,subprocess,sys,tarfile
ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=pathlib.Path,required=True); ap.add_argument("--jobs",type=int,default=8); a=ap.parse_args(); assert 1<=a.jobs<=8
p=pathlib.Path(__file__).resolve().parents[1]; root=a.repo.resolve(); sys.dont_write_bytecode=True
records=[]
for label,rev in [("base","86a7b0c57831c15e9cd8b42d64cc4a9843f4e726"),("head","cd9825c947cf67b735d26cc1c42541ccd9d7f637")]:
 tree=p/"scratch"/("plant-"+label); tree.mkdir(exist_ok=True); archive=p/"scratch"/("plant-"+label+".tar")
 with archive.open("wb") as f: subprocess.run(["git","archive",rev],cwd=root,stdout=f,check=True)
 with tarfile.open(archive) as tf: tf.extractall(tree,filter="data")
 def check(f):
  r=subprocess.run(["git","apply","--check",str(f)],cwd=tree,capture_output=True,text=True)
  return dict(revision=rev,patch=str(f.relative_to(tree)),rc=r.returncode,error=r.stderr.strip())
 with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex: rows=list(ex.map(check,sorted(tree.glob("tb/**/*.patch"))))
 records+=rows; print(label,len(rows),"patches",sum(x["rc"]!=0 for x in rows),"refused")
(p/"receipts/patch-plants.json").write_text(json.dumps(records,indent=1)+"\n")
def module(rel):
 spec=importlib.util.spec_from_file_location("review_"+pathlib.Path(rel).stem,root/rel); m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
arms=[]
def plant(driver,name,edits):
 cache={};details=[]
 for rel,old,new,sites in edits:
  s=cache.get(rel,(root/rel).read_text()); n=s.count(old); details.append(dict(path=rel,sites=n,expected=sites));cache[rel]=s.replace(old,new)
 arms.append(dict(driver=driver,name=name,planted=all(x["sites"]==x["expected"] for x in details),edits=details))
for f in ["notify_mutants","acmp_mutants","d3_mutants","gsi_mutants"]:
 m=module("tb/pp_top/"+f+".py")
 for v in m.MUTANTS if hasattr(m,"MUTANTS") else m.mutations():
  name=v.name if hasattr(v,"name") else v[0]; edits=v.edits if hasattr(v,"edits") else [v[1:5]]
  plant(f,name,[(*edit,1) if len(edit)==3 else edit for edit in edits])
plant("name_wr_mutant","decode",[("hdl/aecp/KL_aecp_engine.sv","  assign name_wr_o = d3_nchg_w;","  assign name_wr_o = txn_valid_i && txn_ready_o && sname_w;",1)])
m=module("tb/srp_admission/mutants.py")
for name,edits,_ in m.MUTANTS:plant("srp_admission",name,[(m.ADMISSION,*e) for e in edits])
m=module("tb/acmp_talker/retry_mutants.py")
for name,edits in m.MUTATIONS.items():
 edits=(edits,) if isinstance(edits[0],str) else edits
 plant("retry_mutants",name,[(m.RTL,*e,1) for e in edits])
(p/"receipts/exact-text-plants.json").write_text(json.dumps(arms,indent=1)+"\n");print(len(arms),"exact-text arms",sum(not x["planted"] for x in arms),"refused")
raise SystemExit(int(any(x["rc"] for x in records) or any(not x["planted"] for x in arms)))
