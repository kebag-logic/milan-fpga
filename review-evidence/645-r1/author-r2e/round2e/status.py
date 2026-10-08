from pathlib import Path
import json,re,sys,time
w=Path(__file__).resolve().parent
if len(sys.argv)>1:time.sleep(min(50,int(sys.argv[1])))
print(time.strftime("%FT%T"))
for name in ("vendor",):
 p=w/(name+".log")
 if p.exists():print(name,*p.read_text(errors="replace").splitlines()[-4:],sep="\n  ")
for name in ("sweep-0-rerun","sweep-1-rerun","builder","physical","render-default","render-mutants","dev-render-mutants","render-pullin","render-boundary","follow-pullin","quiet-reader","portability","fw-mutants-shard-0","fw-mutants-shard-1","fw-mutants-shard-2","fw-mutants-shard-3"):
 p=w/"logs"/(name+".rc");q=w/"logs"/(name+".log")
 if q.exists():print(name,"rc="+p.read_text().strip() if p.exists() else "running",q.stat().st_size)
for i in range(4):
 p=w/"logs"/("fw-mutants-shard-"+str(i)+".log")
 if p.exists():print("firmware shard",i,"caught",len(re.findall(r"^\[ok\] mutant ",p.read_text(),re.M)),"escapes",len(re.findall(r"^\[ESCAPED\]",p.read_text(),re.M)))
for name in ("arrival","follow-pullin"):
 p=w/name/"results.json"
 if p.exists():
  try:
   j=json.loads(p.read_text());print(name,"complete",len(j),"nonzero",sum(int(r.get("rc",0))!=0 for r in j))
  except (ValueError,AttributeError,TypeError):pass
cg=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
for name in ("sweep-0-rerun","sweep-1-rerun"):
 p=w/"logs"/(name+".log")
 if p.exists():print(name,"completed suites",len(re.findall(r"^PASS\s",p.read_text(),re.M)))
print("memory GB",round(int((cg/"memory.current").read_text())/1e9,3),"peak GB",round(int((cg/"memory.peak").read_text())/1e9,3))
