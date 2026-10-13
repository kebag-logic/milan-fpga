import hashlib, json, os, subprocess, sys, time
from pathlib import Path
root,out=map(lambda s:Path(s).resolve(),sys.argv[1:])
out.mkdir(parents=True,exist_ok=True)
runtime=out.parents[1]/"runtime"
base=Path(os.environ["RUNTIME_ROOT"])
shapes=sorted((root/"configs").glob("endstation_*.yaml"))
rows=[]
def run(label,argv):
 start=time.monotonic()
 with (out/(label+".log")).open("w") as f:
  r=subprocess.run(argv,cwd=root,stdout=f,stderr=subprocess.STDOUT)
 print(label,"rc",r.returncode,"seconds",round(time.monotonic()-start,1),flush=True)
 if r.returncode: raise SystemExit(r.returncode)
def record(path):
 data=path.read_bytes()
 rows.append(dict(path=str(path.relative_to(out)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
args=[sys.executable,"sw/firmware/ctrl/test/ctrl_image.py","--out",str(out/"ctrl_image")]
for shape in shapes: args += ["--shape",shape.stem]
run("ctrl_image",args)
for path in sorted((out/"ctrl_image").rglob("ctrl_app.elf")): record(path)
for layout in ("flat","split"):
 for shape in shapes:
  for interfaces in (1,2):
   for composition in ("srp","nosrp","aecp"):
    label=f"{layout}-{shape.stem}-if{interfaces}-{composition}"
    extra={"srp":[],"nosrp":["--without-srp"],"aecp":["--with-aecp"]}[composition]
    runtime=base/("runtime-freestanding" if composition=="aecp" else "runtime")
    run(label,[sys.executable,"sw/firmware/ctrl/test/ctrl_srp_image.py","--config",str(shape),"--interfaces",str(interfaces),"--layout",layout,"--output",str(out/label),"--libc",str(runtime/"libc.a"),"--compiler-runtime",str(runtime/"libcompiler_rt.a"),*extra])
    record(out/label/"ctrl_app.elf")
(out/"manifest.json").write_text(json.dumps(rows,indent=2)+"\n")
print("images",len(rows),flush=True)
