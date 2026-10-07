#!/usr/bin/env python3
"""Rebuild all linked-size fixture rows with provisioned runtime sources."""
import argparse, concurrent.futures, hashlib, json, os, subprocess, sys, tarfile, io
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path)
for n in ("picolibc","compiler-rt","litex-software"): p.add_argument("--"+n,type=Path,required=True)
p.add_argument("--jobs",type=int,default=4)
a=p.parse_args();root=a.source.resolve();packet=Path(__file__).resolve().parent
scratch=packet/"scratch/sizes";scratch.mkdir(parents=True,exist_ok=True)
receipts=packet/"receipts"; out=receipts/"sizes";out.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(scratch))
def cmd(argv,name):
 r=subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True)
 (out/(name+".log")).write_text(r.stdout+r.stderr)
 (out/(name+".rc")).write_text(str(r.returncode)+"\n")
 if r.returncode: raise RuntimeError(name+" failed; see log")
 return r
runtime=scratch/"runtime"
cmd([sys.executable,"-B",str(root/"sw/firmware/ctrl/test/ctrl_image_runtime.py"),
 "--picolibc",str(a.picolibc),"--compiler-rt",str(a.compiler_rt),
 "--litex-software",str(a.litex_software),"--output",str(runtime)],"runtime")
expected=json.loads(subprocess.check_output(["git","show","95f80a0a:review-evidence/665f4-r1/author-r2/ROUND2-SIZE.json"],cwd=root))
for name,commit in [("fc","db9aa8c9b135b34ff3d070a979dee70440b37cc6"),("dev","d51b373ad7e8e8381af2797be3ebb8ee45c62e3c")]:
 dest=scratch/name;dest.mkdir(exist_ok=True)
 archive=subprocess.check_output(["git","archive",commit,"sw/firmware/ctrl"],cwd=root)
 with tarfile.open(fileobj=io.BytesIO(archive)) as tar: tar.extractall(dest,filter="data")
def row(e):
 name=f"{e['base']}-{e['shape']}-if{e['interfaces']}";build=scratch/name
 argv=[sys.executable,"-B",str(root/"sw/firmware/ctrl/test/ctrl_image.py"),
 "--config",str(root/"configs"/(e["shape"]+".yaml")),"--interfaces",str(e["interfaces"]),
 "--output",str(build),"--libc",str(runtime/"libc.a"),"--compiler-runtime",str(runtime/"libcompiler_rt.a")]
 if e["base"]!="head": argv += ["--without-srp","--ctrl-source",str(scratch/e["base"]/"sw/firmware/ctrl")]
 cmd(argv,name)
 actual=json.loads((build/"size.json").read_text())
 for n in ("size.json","size.txt","symbols.txt"): (out/(name+"-"+n)).write_bytes((build/n).read_bytes())
 keys=("sections","static_storage","ram_sections","ram_span")
 match=all(actual[k]==e[k] for k in keys)
 r={"name":name,"match":match,"expected_span":e["ram_span"],"actual_span":actual["ram_span"]}
 print(json.dumps(r),flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,4)) as pool: results=list(pool.map(row,expected))
(out/"results.json").write_text(json.dumps(results,indent=2)+"\n")
sys.exit(0 if all(r["match"] for r in results) else 1)
