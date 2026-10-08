import json,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
cg=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
def cpu():return int(dict(line.split() for line in (cg/"cpu.stat").read_text().splitlines())["usage_usec"])
cpu_start=cpu();time_start=time.monotonic()
if len(sys.argv)>1:time.sleep(min(50,int(sys.argv[1])))
print(time.strftime("%FT%T"))
p=w/"vendor.log";lines=p.read_text(errors="replace").splitlines() if p.exists() else []
print("\n".join(lines[-3:]))
starts=[l.split()[2] for l in lines if " START " in l]
if starts:
 name=starts[-1];p=w/"logs"/(name+".log")
 if p.exists():
  with p.open("rb") as f:f.seek(max(0,p.stat().st_size-5000));tail=f.read().decode(errors="replace")
  print("last job:",name,"bytes",p.stat().st_size)
  print("\n".join(l for l in tail.splitlines()[-3:] if l.strip()))
p=w/"vendor.rc"
if p.exists():print("vendor rc",p.read_text().strip())
cg=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
print("memory GB",round(int((cg/"memory.current").read_text())/1e9,3),"peak GB",round(int((cg/"memory.peak").read_text())/1e9,3))
print("CPU seconds during wait",round((cpu()-cpu_start)/1e6,2),"elapsed seconds",round(time.monotonic()-time_start,2))
