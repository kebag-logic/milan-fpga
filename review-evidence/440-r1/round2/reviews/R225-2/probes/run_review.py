import ast,collections,concurrent.futures,difflib,json,os,shutil,subprocess,sys
from pathlib import Path
out=Path(__file__).resolve().parents[1]; scratch=Path((out/"scratch-path.txt").read_text().strip())
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",MAX_JOBS="4",JOBS="4")
def run(cmd,cwd,log):
 p=subprocess.run(["rtk","proxy",*cmd],cwd=cwd,env=env,capture_output=True,text=True)
 dest=out/log; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(p.stdout+p.stderr)
 return dict(command=["rtk","proxy",*cmd],cwd=str(cwd),rc=p.returncode,log=log)
for v in ("old","head"):
 r=run(["python3","-B",str(out/"probes/population.py"),str(scratch/v/"scripts")],scratch/v,f"populations/{v}.json")
 assert r["rc"]==0,r
old=json.loads((out/"populations/old.json").read_text()); new=json.loads((out/"populations/head.json").read_text())
# Guard fixtures derive their synthetic tally from MIN_ARMS; their source and
# predicate bytecode remain identical while four closure totals rise with it.
def key(r):
 if isinstance(r,dict):
  r=dict(r); r["holds"]=dict(r["holds"]);r["holds"].pop("closure",None)
 return json.dumps(r,sort_keys=True)
closure_changes=[]
new_by_id={(r["family"],r["name"]):r for r in new["arms"]}
for r in old["arms"]:
 t=new_by_id[(r["family"],r["name"])]
 if r["holds"]["closure"]!=t["holds"]["closure"]:
  assert r["family"]=="guard" and r["holds"]["closure"]==["<class 'dict'>",5464] and t["holds"]["closure"]==["<class 'dict'>",5656]
  closure_changes.append(dict(name=r["name"],old=r["holds"]["closure"],head=t["holds"]["closure"]))
assert len(closure_changes)==4
(out/"guard-floor-closures.json").write_text(json.dumps(closure_changes,indent=2)+"\n")
a=collections.Counter(map(key,old["arms"])); b=collections.Counter(map(key,new["arms"]))
x=collections.Counter(map(key,old["labels"])); y=collections.Counter(map(key,new["labels"]))
ret=dict(old_raw=len(old["arms"]),head_raw=len(new["arms"]),old_label_rows=len(old["labels"]),head_label_rows=len(new["labels"]),missing_raw=list((a-b).elements()),missing_labels=list((x-y).elements()),added_raw=[json.loads(r) for r in (b-a).elements()],added_labels=[json.loads(r) for r in (y-x).elements()])
assert not ret["missing_raw"] and not ret["missing_labels"]
assert len(ret["added_raw"])==24 and len(ret["added_labels"])==6
(out/"retention.json").write_text(json.dumps(ret,indent=2)+"\n")
oldsrc=(scratch/"old/scripts/gen_toc.py").read_text(); newsrc=(scratch/"head/scripts/gen_toc.py").read_text()
assert oldsrc.replace("MIN_ARMS = 683","MIN_ARMS = 707")==newsrc
identical=[]
for f in ("gen_toc_cases.py","gen_toc_guards.py","check_em_dash.py"):
 assert (scratch/"old/scripts"/f).read_bytes()==(scratch/"head/scripts"/f).read_bytes();identical.append(f)
(out/"unchanged-production.json").write_text(json.dumps(dict(gen_toc_only_change="MIN_ARMS = 683 -> 707",byte_identical=identical,prior="0d43ff25d38917e77bb5c3d2ddb6473013cea3ba",head="9d6109ccf924c03308cb8aa202ce68a435cd4f8d"),indent=2)+"\n")
variants=[]
for version in ("old","head"):
 for tag in (None,"div","title","xmp"):
  label=version+"-"+(tag or "correct"); root=scratch/label
  shutil.copytree(scratch/version/"scripts",root/"scripts",dirs_exist_ok=True)
  if tag:
   f=root/"scripts/gen_toc.py"; src=f.read_text(); needle='return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD))'; assert src.count(needle)==1
   altered=src.replace(needle,needle.replace('RAW_HTML_TAGS','(*RAW_HTML_TAGS, "'+tag+'")'));f.write_text(altered)
   patch=''.join(difflib.unified_diff(src.splitlines(True),altered.splitlines(True),fromfile="a/scripts/gen_toc.py",tofile="b/scripts/gen_toc.py"))
   dest=out/"mutations"/(label+".patch");dest.parent.mkdir(exist_ok=True);dest.write_text(patch)
  variants.append((label,root,tag,version))
def trial(v):
 label,root,tag,version=v
 results=[run(["python3","-B","scripts/"+f,"--selftest"],root,f"mutations/{label}.{f}.log") for f in ("gen_toc.py","check_em_dash.py")]
 expected=[1,2] if tag and version=="head" else [0,0]
 assert [r["rc"] for r in results]==expected,results
 if tag and version=="head":
  raw=(out/results[0]["log"]).read_text();labels=(out/results[1]["log"]).read_text()
  assert raw.count("FAIL [I440-T-other-name ")==8 and "GUARD" not in raw,raw
  assert labels.count("got 0/1")==2 and "FATAL: 4 of 57" in labels,labels
 return dict(variant=label,results=results)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(trial,variants))
(out/"mutations.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(dict(retention={k:v for k,v in ret.items() if not k.startswith("added")},mutations=[dict(variant=x["variant"],rc=[r["rc"] for r in x["results"]]) for x in results]),indent=2))
