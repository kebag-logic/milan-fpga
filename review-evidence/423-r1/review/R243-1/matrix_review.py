import importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent;source=Path("$VALIDATION_STORAGE/reviews/r243-423-r1")
sys.path.insert(0,str(source/"scripts"));import check_merge_containment as mc;import merge_containment_replay as proof
from merge_containment_selftest_mutations import MUTATIONS
fixture=root/"public-fixtures/fixtures.py"
sys.argv=[str(fixture),"unused","unused","unused","unused"]
spec=importlib.util.spec_from_file_location("published_fixture",fixture);fx=importlib.util.module_from_spec(spec);spec.loader.exec_module(fx)
public=json.loads((root/"public-fixtures/fixture-matrix.json").read_text())["rows"]
os.environ.update(GIT_CONFIG_NOSYSTEM="1",GIT_CONFIG_GLOBAL=os.devnull,PYTHONDONTWRITEBYTECODE="1")
repo_root=root/"matrix-repos";repo_root.mkdir(exist_ok=True)
original=(source/"scripts/merge_containment_replay.py").read_text();checker=(source/"scripts/check_merge_containment.py").read_text()
mutants=[]
for name,edits,cases in MUTATIONS:
 target=root/"mutants"/name;target.mkdir(parents=True,exist_ok=True);code=original
 for old,new in edits:assert code.count(old)==1;code=code.replace(old,new)
 (target/"merge_containment_replay.py").write_text(code);(target/"check_merge_containment.py").write_text(checker);mutants.append((name,target/"check_merge_containment.py",cases))
def run(path):
 r=subprocess.run(["rtk","proxy",sys.executable,"-B","-I",str(path),"--no-fetch","--base","main","pr"],capture_output=True)
 words=r.stdout.split();result=[r.returncode,words[0].decode() if words else r.stderr.decode()]
 return dict(result=result,stdout=r.stdout.decode(),stderr=r.stderr.decode())
rows=[];changes={name:[] for name,_,_ in mutants}
for index,(name,build,_old,want,_class) in enumerate(fx.SCENARIOS,1):
 repo=repo_root/name;repo.mkdir();os.chdir(repo);fx.TICK[0]=1790000000;build()
 head=fx.git("rev-parse","pr");tip=fx.git("rev-parse","main");expected=public[index-1]
 assert (name,head,tip)==(expected["scenario"],expected["branch_head"],expected["base_tip"])
 actual=run(source/"scripts/check_merge_containment.py");assert actual["result"]==list(want)
 # Each normal arm is actually called in order; tracing delegates unchanged.
 trace=[]
 for helper in ("_path_scoped_verdict","_patch_id_verdict","replay_verdict"):
  fn=getattr(mc,helper)
  def wrap(*args,_fn=fn,_name=helper,**kwargs):
   answer=_fn(*args,**kwargs);trace.append([_name,answer]);return answer
  setattr(mc,helper,wrap)
 try: value=mc.contained(head,tip)
 finally:
  for helper in ("_path_scoped_verdict","_patch_id_verdict","replay_verdict"):
   wrapper=getattr(mc,helper);setattr(mc,helper,wrapper.__kwdefaults__["_fn"])
 row=dict(index=index,scenario=name,head=head,tip=tip,actual=actual,trace=trace,mutants={})
 for mutant,path,cases in mutants:
  answer=run(path);row["mutants"][mutant]=answer
  expected_result=list(cases.get(index,want));assert answer["result"]==expected_result,(index,mutant,answer,expected_result)
  if answer["result"]!=actual["result"]:changes[mutant].append(index)
 rows.append(row);print(index,name,actual["result"],"mutants checked",flush=True)
for name,_,cases in mutants:assert changes[name]==sorted(cases)
(root/"matrix-review-data.json").write_text(json.dumps(dict(rows=rows,changed_cases=changes,cli_runs=len(rows)*11),indent=2)+"\n")
print("PASS: 31 original public OID pairs, 341 real CLI results, ten exact guard change sets")
