import json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
for name,argv in [("litex-controls",["bash","scripts/run_litex_sims.sh","--selftest"]),("litex-sims",["bash","scripts/run_litex_sims.sh",str(w/"litex-sims")])]:
 (w/"jobs"/(name+".json")).write_text(json.dumps(dict(argv=argv,cwd=str(w/"functional/campaign"),env={"LITEX_SIM_TIMEOUT":"14400"})))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
(w/"litex-complete").write_text("complete\n")
