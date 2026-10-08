import concurrent.futures as cf,json,os,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
root=w/"functional"
def wait(name):
 p=w/"logs"/(name+".rc")
 while not p.exists():time.sleep(2)
 rc=int(p.read_text());print(time.strftime("%FT%T"),"DONE",name,rc,flush=True);return rc
def run(name,argv,cwd):
 if (w/"logs"/(name+".rc")).exists():return wait(name)
 pidfile=w/"jobs"/(name+".pid")
 if pidfile.exists() and Path("/proc",pidfile.read_text().strip()).exists():return wait(name)
 (w/"jobs"/(name+".json")).write_text(json.dumps(dict(argv=argv,cwd=str(cwd))))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  pidfile.write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);p.wait()
 return wait(name)
def campaigns():
 wait("arrival")
 d=root/"campaign/tb/verilator/follow_ring"
 run("quiet-reader",["python3","-B","quiet_distributions.py",str(w/"arrival"),"--band","2","--out",str(w/"quiet.json")],d)
 run("follow-pullin",["python3","-B","sweep.py","pullin","--exe",str(w/"follow-model/Vfollow_ring"),"--out",str(w/"follow-pullin"),"--jobs","16","--hold-us","52","56"],d)
def other():
 wait("physical")
 run("portability",["bash","syn/yosys/run.sh"],root/"builder")
def pullin():run("render-pullin",["make","-j16","tdm8render-pullin","PULLIN_JOBS=16"],root/"render-pullin/tb/verilator/milan_dp_render")
def boundary():run("render-boundary",["make","-j16","tdm8render-law-boundary","LAW_BOUNDARY_JOBS=16"],root/"render-boundary/tb/verilator/milan_dp_render")
with cf.ThreadPoolExecutor(max_workers=6) as pool:
 fs=[pool.submit(f) for f in (campaigns,other,pullin,boundary)]
 fs += [pool.submit(wait,n) for n in ("render-mutants","dev-render-mutants")]
 for f in cf.as_completed(fs):f.result()
(w/"functional-complete").write_text("complete\n")
