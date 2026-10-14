#!/usr/bin/env python3
"""Focused controls; changes only an archived copy beneath packet/scratch."""
import ast,copy,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tarfile,time
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); packet=Path(sys.argv[2]).resolve()
work=packet/"scratch"/"controls";work.mkdir(parents=True,exist_ok=True)
tree=work/"tree";tree.mkdir(exist_ok=True)
raw=subprocess.check_output(["git","-C",str(repo),"archive","HEAD"])
with tarfile.open(fileobj=io.BytesIO(raw)) as t:t.extractall(tree,filter="data")
env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","TMPDIR":str(work)}
def command(args,cwd=tree):
 r=subprocess.run([sys.executable,*args],cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 return {"rc":r.returncode,"output":r.stdout.replace(str(work),"<scratch>").strip()}
results={}
inventory=tree/"ci/image/tool-inventory.json"; original=inventory.read_bytes()
for kind in ["missing","orphan"]:
 d=json.loads(original)
 if kind=="missing":d["tools"].pop()
 else:d["tools"].append({"tool":"orphan-review-fixture","kind":"pip","pin":"1.0","installed_by":[]})
 inventory.write_text(json.dumps(d));r=command(["scripts/ci_tool_inventory.py","--check"]);assert r["rc"]==2
 results[kind+"_inventory_entry"]=r
 inventory.write_bytes(original)
lock=tree/"ci/image/image.lock.json";old=lock.read_bytes()
for kind in ["empty_layers","wrong_layer_version","arbitrary_image_digest","wrong_platform","wrong_base"]:
 d=json.loads(old)
 if kind=="empty_layers":d["layers"]=[]
 elif kind=="wrong_layer_version":d["layers"][0]["tools"][0]["version"]="review-invalid-version"
 elif kind=="arbitrary_image_digest":d["image_digest"]="sha256:"+"0"*64
 elif kind=="wrong_platform":d["platform"]="linux/arm64"
 else:d["base"]="ubuntu:latest"
 lock.write_text(json.dumps(d));r=command(["ci/image/build.py","--work",str(work/"build"),"--check-lock"])
 results[kind]=r;assert r["rc"]==0
 lock.write_bytes(old)
fixture=work/"inventory-fixture";(fixture/".github/workflows").mkdir(parents=True,exist_ok=True);(fixture/"scripts").mkdir(exist_ok=True)
prefix="name: fixture\njobs:\n  gate:\n    steps:\n"
workflow=fixture/".github/workflows/test.yml"
for kind,body in {
 "literal_list":'import subprocess\nsubprocess.run(["pip", "install", "review-fixture==1.0"])\n',
 "variable_list":'import subprocess\ncmd=["pip", "install", "review-fixture==1.0"]\nsubprocess.run(cmd, check=True)\n',
 "shell_string":'import subprocess\nsubprocess.run("python3 -m pip install review-fixture==1.0", shell=True, check=True)\n',
 }.items():
 (fixture/"scripts/bootstrap.py").write_text(body)
 workflow.write_text(prefix+"      - run: python3 scripts/bootstrap.py\n")
 r=command([str(repo/"scripts/ci_tool_inventory.py"),"--root",str(fixture),"--write"])
 if kind=="literal_list":assert r["rc"]==2
 else:
  assert r["rc"]==0
  r["derived_tools"]=json.loads((fixture/"ci/image/tool-inventory.json").read_text())["tools"]
  r["check"]=command([str(repo/"scripts/ci_tool_inventory.py"),"--root",str(fixture),"--check"])
  assert not r["derived_tools"] and r["check"]["rc"]==0
 results["called_script_"+kind]=r
# Execute the exact installer function with only absolute destinations relocated.
# Two executions have identical bytes/inputs; wall-clock file metadata is measured.
source=ast.parse((repo/"ci/image/install.py").read_text())
function=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=="sbt")
code=compile(ast.Module(body=[function],type_ignores=[]),"ci/image/install.py","exec")
art=work/"artifact.jar";art.write_bytes(b"public deterministic test fixture\n")
pins={"sources":[{"tool":"fixture","kind":"maven","sha256":hashlib.sha256(art.read_bytes()).hexdigest(),"cache_path":"coursier/fixture.jar"}],"sbt_boot":[]}
outputs=[]
for i in range(2):
 dest=work/f"sbt-{i}";dest.mkdir(exist_ok=True);(dest/"recipe").mkdir(exist_ok=True);(dest/"recipe/sbt-repositories").write_text("[repositories]\nlocal\n")
 def path(value):return dest/str(value).lstrip("/")
 def unpack(name,destination):destination.mkdir(parents=True,exist_ok=True)
 class Copier:
  @staticmethod
  def copyfile(src,dst):
   if str(src).startswith("/recipe/"):src=path(src)
   if str(dst).startswith("/opt/"):dst=path(dst)
   return shutil.copyfile(src,dst)
 scope={"Path":path,"PINS":pins,"artifact":lambda name:art,"unpack":unpack,"shutil":Copier,"hashlib":hashlib}
 exec(code,scope);scope["sbt"]()
 data=io.BytesIO()
 with tarfile.open(fileobj=data,mode="w",format=tarfile.USTAR_FORMAT) as archive:
  for f in sorted((dest/"opt").rglob("*")):
   if not f.is_file():continue
   info=archive.gettarinfo(str(f),arcname=f.relative_to(dest).as_posix())
   info.uid=info.gid=0;info.uname=info.gname=""
   with f.open("rb") as stream:archive.addfile(info,stream)
 checks={f.relative_to(dest).as_posix():{"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"mtime":int(f.stat().st_mtime)} for f in sorted((dest/"opt").rglob("*")) if f.is_file()}
 outputs.append({"tar_sha256":hashlib.sha256(data.getvalue()).hexdigest(),"files":checks})
 if i==0:time.sleep(1.2)
assert outputs[0]["tar_sha256"]!=outputs[1]["tar_sha256"]
assert {k:v["sha256"] for k,v in outputs[0]["files"].items()}=={k:v["sha256"] for k,v in outputs[1]["files"].items()}
results["exact_sbt_installer_repeat"]={"method":"Exact sbt() AST function, relocated output only; fixed fixture artifact; normal USTAR file metadata; no Docker execution", "same_file_payloads":True,"different_tar_bytes":True,"runs":outputs}
print(json.dumps(results,indent=2,sort_keys=True))
