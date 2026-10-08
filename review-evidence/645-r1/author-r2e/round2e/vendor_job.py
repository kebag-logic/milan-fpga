import json,os,signal,subprocess,sys,time
from pathlib import Path
signal.signal(signal.SIGHUP,signal.SIG_DFL)
w=Path(__file__).resolve().parent
name=sys.argv[1]
spec=json.loads((w/"jobs"/(name+".json")).read_text())
e=os.environ.copy();e.update(PYTHONDONTWRITEBYTECODE="1",PYTHONHASHSEED="0",TMPDIR=str(w/"tmp"));e.update(spec.get("env",{}))
e["PATH"]=str(Path.home()/"litex-milan/venv/bin")+":"+str(Path.home()/"Xilinx/2026.1/Vivado/bin")+":"+e["PATH"]
cg=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
peak=0;stopped=False;t=time.time()
with (w/"logs"/(name+".log")).open("w") as f:
 p=subprocess.Popen(spec["argv"],cwd=spec["cwd"],env=e,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 while p.poll() is None:
  memory=int((cg/"memory.current").read_text());peak=max(peak,memory)
  if memory>16800000000:
   stopped=True;os.killpg(p.pid,signal.SIGTERM);time.sleep(3)
   if p.poll() is None:os.killpg(p.pid,signal.SIGKILL)
   break
  time.sleep(1)
 rc=p.wait()
(w/"logs"/(name+".rc")).write_text(str(rc)+"\n")
(w/"logs"/(name+".receipt.json")).write_text(json.dumps(dict(**spec,rc=rc,seconds=round(time.time()-t,1),peak_memory_bytes=peak,resource_interruption=stopped),indent=2)+"\n")
raise SystemExit(rc)
