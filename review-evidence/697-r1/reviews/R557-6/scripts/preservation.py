#!/usr/bin/env python3
import concurrent.futures,hashlib,io,json,pathlib,shlex,shutil,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve(); w=p/"scratch/preservation"; base=w/"base"; base.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","-C",str(root),"archive","ae982af85ec97286bd35b39403926d8f0eaec81d"]))) as t:t.extractall(base,filter="data")
sys.path.insert(0,str(root/"scripts")); from compiler_tokens import raw_tokens
rows=[]
for directory in ("src","include","examples"):
 for f in sorted((root/directory).rglob("*")):
  if not f.is_file():continue
  rel=f.relative_to(root).as_posix(); current=f.read_bytes(); previous=subprocess.check_output(["git","-C",str(root),"show","60c911b9:"+rel]); row={"file":rel,"round7_bytes_equal":current==previous,"sha256":hashlib.sha256(current).hexdigest()}
  if directory in ("src","include"):
   code=lambda data:[(kind,value) for kind,value,*_ in raw_tokens(data.decode(),"c") if kind!="comment" and not value.isspace()]
   row["base_code_tokens_equal"]=code((base/rel).read_bytes())==code(current)
  rows.append(row)
assert all(r["round7_bytes_equal"] and r.get("base_code_tokens_equal",True) for r in rows)
mut=root/"tests/mutations.json"; old=subprocess.check_output(["git","-C",str(root),"show","60c911b9:tests/mutations.json"])
assert old==mut.read_bytes()
proof={"files":rows,"mutation_table_bytes_equal":True,"round7_commit_count":int(subprocess.check_output(["git","-C",str(root),"rev-list","--count","60c911b9..HEAD"]))}
(p/"receipts/preservation.json").write_text(json.dumps(proof,indent=2)+"\n")
variants=[]
for label,d in (("gcc",p/"scratch/suites/linux/gcc"),("clang-sanitizers",p/"scratch/suites/linux/clang-sanitizers"),("rv32-debug",p/"scratch/suites/rv32/debug"),("rv32-release",p/"scratch/suites/rv32/release")):
 for entry in json.loads((d/"compile_commands.json").read_text()):
  if pathlib.Path(entry["file"]).parent==root/"src": variants.append((label,entry))
def compare(item):
 i,(label,e)=item; active=w/("variant-"+str(i)); active.mkdir(exist_ok=True)
 shutil.copytree(root/"examples",active/"examples",dirs_exist_ok=True)
 argv=shlex.split(e["command"]); row={"configuration":label,"target":argv[argv.index("-o")+1],"source":pathlib.Path(e["file"]).name}
 argv=[a.replace(str(root),str(active)) for a in argv]; obj=active/"comparison.o"; argv[argv.index("-o")+1]=str(obj); argv.extend(["-g0","-frandom-seed=0"])
 for name,source in (("base",base),("head",root)):
  for directory in ("src","include"):shutil.copytree(source/directory,active/directory,dirs_exist_ok=True)
  result=subprocess.run(argv,cwd=active,capture_output=True,text=True); row[name+"_rc"]=result.returncode; (active/(name+".log")).write_text(result.stdout+result.stderr)
  if result.returncode==0:row[name+"_sha256"]=hashlib.sha256(obj.read_bytes()).hexdigest()
 row["equal"]=row["base_rc"]==row["head_rc"]==0 and row["base_sha256"]==row["head_sha256"]
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(compare,enumerate(variants)))
(p/"receipts/object-comparison.json").write_text(json.dumps(results,indent=2)+"\n")
print("round7 unchanged files:",len(rows),"production code token comparisons:",sum("base_code_tokens_equal" in r for r in rows),"mutation table unchanged: True")
print("core object variants:",len(results),"byte identical:",sum(r["equal"] for r in results))
assert len(results)==22 and all(r["equal"] for r in results)
