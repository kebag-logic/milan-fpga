#!/usr/bin/env python3
"""Run focused review checks in an exact-head disposable clone. No source fixes."""
import argparse, concurrent.futures, importlib.util, os, pathlib, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument("repo",type=pathlib.Path); p.add_argument("packet",type=pathlib.Path); p.add_argument("--case",choices=["dma","meter","split","render"]); a=p.parse_args()
a.repo=a.repo.resolve(); a.packet=a.packet.resolve()
work=a.packet/"scratch"/"focused"; work.mkdir(parents=True,exist_ok=True)
os.environ["TMPDIR"]=str(work); os.environ["PYTHONUNBUFFERED"]="1"
os.environ.setdefault("VERILATOR_JOBS","3")
os.environ["MAKEFLAGS"]="-j16 --no-print-directory"
def run(cmd,cwd):
 print("COMMAND",*cmd,flush=True)
 r=subprocess.run(cmd,cwd=cwd,stderr=subprocess.STDOUT)
 if r.returncode: raise RuntimeError(f"command rc={r.returncode}")
def module(path):
 spec=importlib.util.spec_from_file_location("probe_module",path); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m); return m
def check(case):
 here=a.repo/"tb"/"verilator"
 if case=="dma":
  run(["make","-j16","run-dma"],here/"mbx")
  os.environ["VERILATOR_JOBS"]="1"
  run([sys.executable,"dma_mutants.py","--jobs","4","--keep",str(work/"dma")],here/"mbx")
 elif case=="meter":
  run(["make","-j16","cases"],here/"aaf_clock_meter")
  m=module(here/"aaf_clock_meter"/"mutants.py")
  arms=[x for x in m.MUTANTS if x[0].startswith("group_reference_")]; assert len(arms)==2
  w=work/"meter"; w.mkdir(exist_ok=True)
  for name,rtl,edits,target,failure in arms:
   source=m.mutate(m.RTL[rtl].read_text(),edits); assert source is not None
   exe=m.build(w,name,rtl,source,target); assert exe is not None
   r=subprocess.run([str(exe),"shapes"],capture_output=True,text=True)
   print(r.stdout); print(r.stderr)
   assert r.returncode==1 and f"[FAIL] {failure}" in r.stdout+r.stderr
   print("NAMED MUTATION CAUGHT",name,flush=True)
 elif case=="split":
  run(["make","-j16","split"],here/"milan_dp")
 elif case=="render":
  m=module(here/"milan_dp_render"/"tdm8_render_mutants.py")
  clean=m.build("ship",{},work/"render_clean"); assert clean is not None
  rc,out=m.run_leg(clean,"--serial-only"); print(out); assert m.verdict(rc,out,None)=="pass"
  arm=[x for x in m.MUTATIONS if x[1]=="fifo"]; assert len(arm)==1
  name,source,edits,leg,mode,breaks=arm[0]
  value,why=m.plant(source,edits,work,"render_fifo"); assert value is not None,why
  exe=m.build(leg,{m.SOURCES[source][1]:value},work/"render_mutant"); assert exe is not None
  rc,out=m.run_leg(exe,mode); print(out); assert m.verdict(rc,out,breaks)=="caught"
  print("NAMED MUTATION CAUGHT",name,flush=True)
 print("FOCUSED PASS",case,flush=True)
if a.case:
 check(a.case)
else:
 def one(case):
  with (work/f"{case}.raw.log").open("w") as f:
   r=subprocess.run([sys.executable,__file__,str(a.repo),str(a.packet),"--case",case],stdout=f,stderr=subprocess.STDOUT)
  (work/f"{case}.rc").write_text(str(r.returncode)+"\n")
  print(case,"rc",r.returncode,flush=True); return r.returncode
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  results=list(pool.map(one,["dma","meter","split","render"]))
 sys.exit(any(results))
