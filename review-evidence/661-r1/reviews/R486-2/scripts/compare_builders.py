#!/usr/bin/env python3
"""Compare all generated outputs and packed images at three review revisions."""
import argparse, concurrent.futures, hashlib, io, json, subprocess, sys, tarfile
from pathlib import Path
REVS=("42f654478c11bd8f2b070969d83140587190f276","ba57a3bc5","3880c1eb6e2f927a07f98150d5b05a228f8f4efd")
SUBS=("protocol-processor","gptp-processor","third_party/verilog-axis")
DRIVER=r"""
import sys
from pathlib import Path
sys.path.insert(0,"sw/builder")
import test_builder as t
out=Path(sys.argv[1])
for name,config in t.CONFIGS.items():
 r=t.eb.build(str(config),str(out),write_fragment=False)
 artifacts=t.eb._entity_model_image(r["cfg"],r["overlay"])
 dst=out/r["cfg"]["name"]
 for name, data in artifacts.items():
  (dst/name).write_bytes(data if isinstance(data,bytes) else data.encode())
"""
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("scratch",type=Path);a=p.parse_args();root=a.source.resolve();scratch=a.scratch.resolve();scratch.mkdir(parents=True,exist_ok=True)
def export(repo,rev,dst):
 dst.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(["git","-C",str(repo),"archive",rev])
 with tarfile.open(fileobj=io.BytesIO(data)) as tar:tar.extractall(dst,filter="data")
def one(rev):
 sha=subprocess.check_output(["git","-C",str(root),"rev-parse",rev]).decode().strip();tree=scratch/sha[:8];export(root,sha,tree)
 for name in SUBS:
  pin=subprocess.check_output(["git","-C",str(root),"rev-parse",sha+":"+name]).decode().strip();export(root/name,pin,tree/name)
 out=tree/"review-build"
 r=subprocess.run([sys.executable,"-B","-c",DRIVER,str(out)],cwd=tree,capture_output=True,text=True)
 (scratch/(sha[:8]+".log")).write_text(r.stdout+r.stderr)
 assert r.returncode==0,(sha,r.stderr)
 return sha,{str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob("*")) if f.is_file()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,REVS))
for sha,files in results[1:]:
 assert files==results[0][1],(sha,[(p,results[0][1].get(p),files.get(p)) for p in set(files)|set(results[0][1]) if files.get(p)!=results[0][1].get(p)])
print(json.dumps({"result":"PASS","revisions":[s for s,f in results],"files_per_revision":len(results[0][1]),"configurations":5,"outputs_sha256":results[0][1]},indent=2))
