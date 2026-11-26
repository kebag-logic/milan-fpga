#!/usr/bin/env python3
import argparse, concurrent.futures, json, pathlib, shutil, subprocess
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); ap.add_argument("--jobs",type=int,default=3); ap.add_argument("--simulator",required=True); a=ap.parse_args()
r=a.repo.resolve(); p=pathlib.Path(__file__).resolve().parent; out=p/"shapers"; out.mkdir(exist_ok=True)
shutil.copytree(r/"tb/common",p/"scratch/common",dirs_exist_ok=True)
def run(name):
 w=p/"scratch/shapers"/name; shutil.copytree(r/"tb/verilator"/name,w,dirs_exist_ok=True,ignore=shutil.ignore_patterns("obj_dir"))
 f=w/"Makefile"; f.write_text(f.read_text().replace("--build -j 0","--build -j 2"))
 cmd=["make","-j16","-C",str(w),"VERILATOR="+a.simulator,"RTL_DIR="+str(r/"hdl"),"AXIS_DIR="+str(r/"third_party/verilog-axis/rtl")]
 v=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (out/(name+".log")).write_text(v.stdout.replace(str(r),"$REPO").replace(str(p),"$PACKET")); (out/(name+".rc")).write_text(str(v.returncode)+"\n")
 print(name,v.returncode,flush=True); return {"suite":name,"rc":v.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool: result=list(pool.map(run,["cbs","shaper_core","queues"]))
(out/"summary.json").write_text(json.dumps(result,indent=2)+"\n"); raise SystemExit(any(v["rc"] for v in result))
