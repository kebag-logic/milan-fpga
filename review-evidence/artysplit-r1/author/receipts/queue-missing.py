"""Foreground worker queue, two simulation legs after the existing pair becomes free."""
import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
r=Path("$VALIDATION_STORAGE/artysplit-a829/r4");root=Path.cwd()
def running():
    found=[]
    for p in Path("/proc").glob("[0-9]*/cmdline"):
        try: args=p.read_bytes().split(b"\0")
        except (OSError,ProcessLookupError):continue
        if args and args[0].startswith(str(r).encode()) and args[0].endswith(b"/native/Vsim"):
            found.append(int(p.parent.name))
    return found
def every_finished():
    for prefix in ("notice-every-", "notice-burst-"):
        for n in range(8):
            path=r/"arm-every/results"/(prefix+str(n)+".log")
            if not path.exists():return False
            with path.open("rb") as f:
                f.seek(max(0,path.stat().st_size-4000))
                if b"RESULT:" not in f.read():return False
    return True
while not every_finished() or len(running())>2:time.sleep(10)
print("Two simulation slots available",running(),flush=True)
jobs=[("arm-fast",[sys.executable,"-B","tb/verilator/ctrl_service_budget/run.py","--point","arty-1x1","--build-dir",str(r/"arm-fast"),"--reuse-build","--groups","adp-link,datapath-events,maap,backlog-adp@blank-aged2-0,backlog-adp@program-aged2-0,backlog-adp@verify-aged2-0","--jobs","1","--record-budget-findings","--record-share-findings"]),
      ("boot",[sys.executable,"-B",str(r/"run-prepared.py"),"boot"]),
      ("two-mrpdus",[sys.executable,"-B",str(r/"run-prepared.py"),"two"])]
# Keep the scheduler measurement's expensive destination arm in one lane,
# while the other runs the bounded notice and completion paths.
for name,variant in (("arm-valid","valid-destinations"),("arm-declaring","declaring-outputs"),("arm-later","answering-later")):
    jobs.append((name,[sys.executable,"-B","tb/verilator/ctrl_service_budget/run.py","--point","arty-1x1","--build-dir",str(r/name),"--reuse-build","--variant",variant,"--jobs","1","--record-budget-findings","--record-share-findings"]))
# The longest destination arm starts beside the fast cost-source arm.
jobs.sort(key=lambda job: ('arm-fast','arm-valid','boot','two-mrpdus','arm-declaring','arm-later').index(job[0]))
def one(job):
    name,command=job
    print("START",name,flush=True)
    with (r/(name+"-queued.log")).open("w") as log:
        proc=subprocess.run(command,cwd=root,env=dict(os.environ,PYTHONHASHSEED="0",COURSIER_MODE="offline",SBT_OPTS="-Dsbt.offline=true"),stdout=log,stderr=subprocess.STDOUT,timeout=86400)
    result=dict(job=name,returncode=proc.returncode,command=command)
    (r/(name+"-queued.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("DONE",name,proc.returncode,flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,jobs))
(r/"queue-missing-results.json").write_text(json.dumps(results,indent=2)+"\n")
