import concurrent.futures as cf,json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
def run(name,argv):
 (w/"jobs"/(name+".json")).write_text(json.dumps(dict(argv=argv,cwd=str(w/"functional/physical"))))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
def mutants():run("fw-mutants",["python3","-B","sw/firmware/ctrl/test/test_ctrl_firmware.py","--require-rv32","--self-test","--jobs","4"])
def image():
 run("fw-image",["python3","-B","sw/firmware/ctrl/test/ctrl_image.py","--out",str(w/"fw-image")])
 run("fw-image-controls",["python3","-B","sw/firmware/ctrl/test/ctrl_image_selftest.py","--require-rv32","--out",str(w/"fw-image-controls")])
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(f) for f in (mutants,image)]
 for f in cf.as_completed(fs):f.result()
(w/"firmware-campaigns-complete").write_text("complete\n")
