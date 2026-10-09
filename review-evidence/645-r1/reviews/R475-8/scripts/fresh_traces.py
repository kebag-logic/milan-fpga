#!/usr/bin/env python3
"""Acquire and replay real counter/pulse traces concurrently with bounded output."""
import argparse,concurrent.futures,csv,hashlib,json,pathlib,subprocess,sys,time
from decimal import Decimal as D
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("exe",type=pathlib.Path);a=p.parse_args()
root=a.packet/"receipts/fresh-traces";root.mkdir(parents=True,exist_ok=True)
scratch=a.packet/"scratch/fresh-traces";scratch.mkdir(exist_ok=True)
cases=[("declared",["--case","pullin","--latency-us","210.42","--after-s","1.5"],"4.6","0","1.5",".1",(0,0,1)),
("duplicate",["--case","b8","--dwell-s","1.0","--set-phase","0.0","--hold-s","16"],"0","1.25","1.75",".25",(1,0,0)),
("skip",["--case","b8","--dwell-s","45","--set-phase","0.0","--hold-s","16","--peer-ppm","0.82"],"0","38.5","38.75",".25",(1,1,0))]
def run(case):
 name,args,origin,start,end,step,expected=case
 pdu=scratch/(name+".full.csv");servo=root/(name+".servo.csv");log=root/(name+".log")
 argv=[str(a.exe),*args,"--trace",str(pdu),"--servo-trace",str(servo)]
 t=time.monotonic()
 with log.open("w") as f:r=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
 elapsed=time.monotonic()-t
 (root/(name+".rc")).write_text(str(r.returncode)+"\n")
 assert r.returncode==0 and "checks: 18   failures: 0" in log.read_text()
 lo=D(origin)+D(start);hi=D(origin)+D(end)
 window=root/(name+".pdu.csv")
 with pdu.open() as f,window.open("w") as g:
  reader=csv.DictReader(f);writer=csv.DictWriter(g,reader.fieldnames);writer.writeheader()
  for row in reader:
   if lo<=D(row["arrive_s"])<hi:writer.writerow(row)
 table=root/(name+".table.csv")
 cmd=[sys.executable,"-B",str(a.source/"tb/verilator/follow_ring/trace_table.py"),str(log),str(window),str(servo),"--origin-s",origin,"--from-s",start,"--to-s",end,"--step-s",step,"--csv",str(table)]
 rr=subprocess.run(cmd,capture_output=True,text=True);(root/(name+".table.log")).write_text(rr.stdout+rr.stderr)
 rows=list(csv.DictReader(table.open()));actual=tuple(sum(int(row[k]) for row in rows) for k in ("slips","skips","recentres"))
 good=rr.returncode==0 and actual==expected and all(r["event_trace"]=="complete" for r in rows)
 result={"name":name,"argv":argv,"reader_argv":cmd,"elapsed_s":elapsed,"run_rc":r.returncode,"reader_rc":rr.returncode,"expected":expected,"actual":actual,"pass":good,"full_trace_sha256":hashlib.sha256(pdu.read_bytes()).hexdigest(),"full_trace_bytes":pdu.stat().st_size}
 (root/(name+".json")).write_text(json.dumps(result,indent=2)+"\n")
 print(name,"run rc",r.returncode,"elapsed",round(elapsed,3),"counts",actual,"pass",good,flush=True)
 return good
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,cases))
raise SystemExit(int(not all(results)))
