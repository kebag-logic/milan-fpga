from pathlib import Path
import os,time,json,shutil
r=Path(__file__).resolve().parent
cg=Path("/sys/fs/cgroup"+Path("/proc/self/cgroup").read_text().strip().split(":")[-1])
while not (r/"resources.stop").exists():
 memory=int((cg/"memory.current").read_text())
 row=dict(time=time.time(),memory=memory,free=shutil.disk_usage(r).free)
 with (r/"resources.jsonl").open("a") as f: f.write(json.dumps(row)+"\n")
 if memory>7000000000:
  released=0
  for p in r.rglob("*"):
   if p.is_file() and p.suffix in {".o",".gcno",".gcda",".gch",".a",".so",".elf",".log"}:
    try:
     fd=os.open(p,os.O_RDONLY)
     try: os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
     finally: os.close(fd)
     released+=1
    except FileNotFoundError: pass
  with (r/"cache-release.jsonl").open("a") as f: f.write(json.dumps(dict(time=time.time(),files=released))+"\n")
 if row["free"]<30*2**30 or memory>=9000000000:
  print("RESOURCE THRESHOLD",row,flush=True)
 time.sleep(5)
print("Resource monitor stopped after final job completion")
