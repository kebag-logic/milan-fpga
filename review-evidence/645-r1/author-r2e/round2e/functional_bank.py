import concurrent.futures as cf,json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
root=w/"functional"

def run(name,argv,cwd):
 (w/"jobs"/(name+".json")).write_text(json.dumps(dict(argv=argv,cwd=str(cwd))))
 with (w/"logs"/(name+".launcher.log")).open("w") as log:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=log,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True)
  rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
 return rc

def sweep():
 for shard in (0,1):
  run("sweep-"+str(shard),["bash","scripts/run_all_suites.sh",str(w/"sweep"/str(shard)),"--shard",str(shard)+"/2"],root/"sweep")

def render():
 d=root/"render/tb/verilator/milan_dp_render"
 for name,args in [("render-default",["make","-j16"]),("render-mutants",["make","-j16","tdm8render-mutants"]),("render-pullin",["make","-j16","tdm8render-pullin","PULLIN_JOBS=8"]),("render-boundary",["make","-j16","tdm8render-law-boundary","LAW_BOUNDARY_JOBS=8"])]:
  run(name,args,d)

def dev_render():
 d=root/"dev-render/tb/verilator/milan_dp_render"
 run("dev-render-default",["make","-j16"],d)
 run("dev-render-mutants",["make","-j16","tdm8render-mutants"],d)

def campaigns():
 d=root/"campaign/tb/verilator/follow_ring"
 exe=w/"follow-model/Vfollow_ring"
 if run("follow-build",["make","-j16","build","MDIR="+str(exe.parent)],d):return
 run("arrival",["python3","-B",str(w/"campaign.py"),"--repo",str(root/"campaign"),"--exe",str(exe),"--out",str(w/"arrival"),"--jobs","16"],d)
 run("quiet-reader",["python3","-B","quiet_distributions.py",str(w/"arrival"),"--band","2","--out",str(w/"quiet.json")],d)
 run("follow-pullin",["python3","-B","sweep.py","pullin","--exe",str(exe),"--out",str(w/"follow-pullin"),"--jobs","16","--hold-us","52","56"],d)

def other():
 d=root/"builder"
 for name,args in [("builder",["python3","-B","sw/builder/test_builder.py","--require-rv32","--require-elaboration"]),("physical",["bash","scripts/run_all_suites.sh",str(w/"physical"),"--physical-gptp"]),("portability",["bash","syn/yosys/run.sh"])]:
  run(name,args,d)

with cf.ThreadPoolExecutor(max_workers=5) as pool:
 futures=[pool.submit(f) for f in (sweep,render,dev_render,campaigns,other)]
 for f in cf.as_completed(futures): f.result()
(w/"functional-complete").write_text("complete\n")
