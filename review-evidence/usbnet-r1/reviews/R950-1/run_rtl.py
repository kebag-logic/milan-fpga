#!/usr/bin/env python3
"""Focused baseline and all planted RTL controls; bounded foreground workers."""
import sys
sys.dont_write_bytecode=True
import argparse, concurrent.futures, importlib.util, json, os, pathlib, shutil, subprocess
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); ap.add_argument("--jobs",type=int,default=8); ap.add_argument("--simulator",required=True); a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parent; scratch=p/"scratch"; logs=p/"rtl"; logs.mkdir(exist_ok=True)
repo=a.repo.resolve(); spec=importlib.util.spec_from_file_location("controls",repo/"tb/verilator/usbnet/mutants.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
flags='--cc --exe --build -j 1 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-PROCASSINIT -Werror-UNDRIVEN -Werror-MULTIDRIVEN -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
def run(c):
 name,harness,fname,old,new,want=c; work=scratch/name; rtl=work/"rtl"; rtl.mkdir(parents=True,exist_ok=True)
 for f in (repo/"hdl/usbnet").glob("*.sv"): shutil.copy2(f,rtl/f.name)
 if fname:
  f=rtl/fname; s=f.read_text(); assert s.count(old)==1; f.write_text(s.replace(old,new))
 cmd=["make","-j16","-C",str(repo/"tb/verilator/usbnet"),harness,"RTL="+str(rtl),"OBJ="+str(work/"obj"),"VERILATOR="+a.simulator,"VFLAGS="+flags]
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (logs/(name+".log")).write_text(r.stdout.replace(str(repo),"$REPO").replace(str(p),"$PACKET")); (logs/(name+".rc")).write_text(str(r.returncode)+"\n")
 good=r.returncode==0 if not fname else r.returncode!=0 and any(x.startswith("FAIL ") and ".cpp:" in x and want in x for x in r.stdout.splitlines())
 print(name, "PASS" if good else "FAIL",flush=True); return {"name":name,"rc":r.returncode,"expected_check":want,"pass":good}
cs=[("baseline-tap","tap",None,None,None,None),("baseline-leds","leds",None,None,None,None)]+mod.CONTROLS
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,16)) as pool: results=list(pool.map(run,cs))
(logs/"summary.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(not all(x["pass"] for x in results))
