#!/usr/bin/env python3
"""Independent physical counter stimuli and declared-action diagnostic probes."""
import argparse, concurrent.futures, csv, hashlib, json, math, pathlib, re, subprocess, sys, time
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("exe",type=pathlib.Path);p.add_argument("--jobs",type=int,default=3);p.add_argument("--cpus",default="104,105,106",help="three available CPUs, one per probe");a=p.parse_args();cpus=[int(c) for c in a.cpus.split(",")];assert len(cpus)==3
reader=a.source/"tb/verilator/follow_ring/trace_table.py"
root=a.packet/"receipts/traces";root.mkdir(parents=True,exist_ok=True)
cases=[("declared",["--case","pullin","--latency-us","210.42","--after-s","1.5"],"recentre",cpus[0]),("duplicate",["--case","b8","--peer-ppm","-100","--dwell-s","3","--hold-s","0.1"],"dup",cpus[1]),("skip",["--case","b8","--peer-ppm","100","--dwell-s","3","--hold-s","0.1"],"skip",cpus[2])]
def run(case):
 name,args,kind,cpu=case;work=a.packet/"scratch"/name;work.mkdir(exist_ok=True)
 cmd=["taskset","-c",str(cpu),str(a.exe)]+args+["--trace",str(work/"pdu.csv"),"--servo-trace",str(work/"servo.csv")]
 start=time.monotonic()
 with (root/(name+".log")).open("w") as f: rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT).returncode
 log=(root/(name+".log")).read_text();events=[float(t) for t in re.findall(r"^RING-EVENT: "+kind+r" ([0-9.]+)$",log,re.M)]
 assert events,(name,"missing actual counter/pulse event")
 event=events[-1] if name=="declared" else events[0]
 lo=math.floor(event*100)/100; hi=lo+0.01
 for src in ("pdu","servo"):
  with (work/(src+".csv")).open() as f:rd=csv.DictReader(f);fields=rd.fieldnames;rows=list(rd)
  if src=="pdu":rows=[r for r in rows if lo<=float(r["arrive_s"])<hi]
  else:rows=[r for r in rows if float(r["t_s"])<=hi][-1:]
  with (root/(name+"."+src+".csv")).open("w") as f:wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)
 cmd2=[sys.executable,"-B",str(reader),str(root/(name+".log")),str(root/(name+".pdu.csv")),str(root/(name+".servo.csv")),"--origin-s","0","--from-s",str(lo),"--to-s",str(hi),"--step-s","0.01","--csv",str(root/(name+".table.csv"))]
 result=subprocess.run(cmd2,capture_output=True,text=True)
 (root/(name+".table.txt")).write_text(result.stdout+result.stderr)
 assert result.returncode==0
 with (root/(name+".table.csv")).open() as f:rows=list(csv.DictReader(f))
 expected=(0,0,1) if name=="declared" else (1,int(kind=="skip"),0)
 actual=tuple(sum(int(r[k]) for r in rows) for k in ("slips","skips","recentres"))
 assert actual==expected,(name,actual,expected)
 assert all(r["event_trace"]=="complete" for r in rows)
 if name=="declared": assert rc==0
 else: assert rc!=0 # deliberately truncated acquisition; not a suite-acceptance run
 meta={"stimulus":args,"raw_rc":rc,"wall_seconds":time.monotonic()-start,"event":event,"expected_counts":expected,"actual_counts":actual,"table_rc":result.returncode,"full_pdu_sha256":hashlib.sha256((work/"pdu.csv").read_bytes()).hexdigest(),"table_command":cmd2}
 (root/(name+".json")).write_text(json.dumps(meta,indent=2)+"\n")
 print(name,meta,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(run,cases))
print("PASS: independent duplicate and skip stimuli counted; declared pulse separated")
