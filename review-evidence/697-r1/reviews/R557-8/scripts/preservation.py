#!/usr/bin/env python3
import hashlib,io,json,os,pathlib,shlex,shutil,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(sys.argv[2]).resolve();env=dict(os.environ);env.update(json.loads((packet/"scratch/environment.json").read_text()));os.environ.update(env)
sys.path.insert(0,str(root/"scripts"));from compiler_tokens import raw_tokens
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip();base="ae982af85ec97286bd35b39403926d8f0eaec81d";prior="68070cb5723682586c07a6de80a49886732b5dc2"
def blob(rev,path):return subprocess.check_output(["git","show",rev+":"+path],cwd=root)
paths=subprocess.check_output(["git","ls-files","src","include","tests","examples"],cwd=root,text=True).splitlines()
unchanged=[{"path":p,"equal":blob(prior,p)==blob(head,p),"sha256":hashlib.sha256(blob(head,p)).hexdigest()} for p in paths]
assert all(x["equal"] for x in unchanged)
def tokens(data):return [(t[0],t[1]) for t in raw_tokens(data.decode(),"c") if t[0]!="comment" and not t[1].isspace()]
production=[{"path":p,"non_comment_tokens_equal":tokens(blob(base,p))==tokens(blob(head,p))} for p in paths if p.startswith(("src/","include/"))]
assert all(x["non_comment_tokens_equal"] for x in production)
work=packet/"scratch/preservation";work.mkdir(parents=True,exist_ok=True);tree=work/"tree";tree.mkdir(exist_ok=True)
entries=[]
for cfg in ["gcc","clang","rv32/debug","rv32/release"]:
 for e in json.loads((packet/"scratch/local"/cfg/"compile_commands.json").read_text()):
  if pathlib.Path(e["file"]).parent==root/"src": entries.append((cfg,e))
rows=[]
for rev in ["086e5d37c19fbb6f4a628c376ce8f9f20e51df14",head]:
 with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","archive",rev],cwd=root))) as t:t.extractall(tree,filter="data")
 for i,(cfg,e) in enumerate(entries):
  args=shlex.split(e["command"]);out=work/"core.o";args[args.index("-o")+1]=str(out)
  args=[s.replace(str(root),str(tree)) for s in args]+["-g0","-frandom-seed=0"]
  result=subprocess.run(args,cwd=tree,env=env,capture_output=True,text=True)
  if result.returncode:raise RuntimeError(result.stderr)
  digest=hashlib.sha256(out.read_bytes()).hexdigest()
  if rev==head:rows[i].update(after=digest,equal=rows[i]["before"]==digest)
  else:rows.append({"configuration":cfg,"source":pathlib.Path(e["file"]).name,"before":digest})
assert len(rows)==22 and all(x["equal"] for x in rows)
result={"head":head,"round9_unchanged_files":unchanged,"production_base_tokens":production,"comment_reduction_before":"086e5d37c19fbb6f4a628c376ce8f9f20e51df14","core_objects":rows}
(packet/"receipts/preservation.json").write_text(json.dumps(result,indent=2)+"\n");print(len(unchanged),"files unchanged in round 9;",len(production),"production token streams equal base; 22/22 object pairs equal")
