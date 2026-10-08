import concurrent.futures as cf,json,re,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
started=time.time()
def run(i):
 name="fw-mutants-shard-"+str(i)
 spec=dict(argv=["python3","-B","sw/firmware/ctrl/test/test_ctrl_firmware.py","--require-rv32","--self-test","--slice",str(i+1)+"/4","--jobs","4"],cwd=str(w/"functional/physical"))
 (w/"jobs"/(name+".json")).write_text(json.dumps(spec))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
 return dict(name=name,rc=rc)
with cf.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,range(4)))
rc=0 if all(r["rc"]==0 for r in rows) else 1
(w/"firmware-shards.json").write_text(json.dumps(dict(head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",expected_controls=469,partition="MUTANTS[index*118:(index+1)*118]",runs=rows,rc=rc),indent=2)+"\n")
(w/"logs/fw-mutants.log").write_text("Four complete disjoint partitions of 469 controls; each partition includes the clean firmware and RV32 arms. See fw-mutants-shard-0 through fw-mutants-shard-3 logs.\n"+json.dumps(rows,indent=2)+"\n")
(w/"logs/fw-mutants.rc").write_text(str(rc)+"\n")
(w/"logs/fw-mutants.receipt.json").write_text(json.dumps(dict(argv=["python3","-B","firmware_shards.py"],cwd=str(w),rc=rc,seconds=round(time.time()-started,1)),indent=2)+"\n")
(w/"firmware-campaigns-complete").write_text("complete\n")
raise SystemExit(rc)
