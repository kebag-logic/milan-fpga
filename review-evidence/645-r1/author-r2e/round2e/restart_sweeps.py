import json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
for shard in (0,1):
 name="sweep-"+str(shard)+"-rerun"
 spec=json.loads((w/"jobs"/("sweep-"+str(shard)+".json")).read_text())
 spec["argv"][2]=str(w/"sweep-rerun"/str(shard))
 (w/"jobs"/(name+".json")).write_text(json.dumps(spec))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True)
  rc=p.wait()
  print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
(w/"sweeps-complete").write_text("complete\n")
