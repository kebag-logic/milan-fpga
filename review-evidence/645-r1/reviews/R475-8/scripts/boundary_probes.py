#!/usr/bin/env python3
"""Independent integer-clock oracle for event and PDU bin ownership."""
import argparse,csv,json,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
root=a.packet/"receipts/own-boundaries";root.mkdir(parents=True,exist_ok=True)
scale=10**30
def decimal(t):
 sign="-" if t<0 else "";t=abs(t);return f"{sign}{t//scale}.{t%scale:030d}"
cases=[("offset-nondivisor",137*scale//100,-11*scale//100,23*scale//100,7*scale//100),
       ("subnanosecond",10*scale,0,17,3),
       ("negative-origin",-scale//10,2*scale//10,71*scale//100,13*scale//100),
       ("large-absolute",10**12*scale,0,41*scale//100,scale//10)]
results=[]
for name,origin,start,end,step in cases:
 lo=origin+start;hi=origin+end;n=(end-start+step-1)//step
 stamps=sorted(set([lo-1,hi,hi+1]+[edge+d for edge in [lo+i*step for i in range(n)]+[hi] for d in [-1,0,1]]))
 assert min(stamps)>=0
 for kind in ("dup","skip","recentre"):
  work=root/(name+"-"+kind);work.mkdir(exist_ok=True)
  events="".join(f"RING-EVENT: {kind} {decimal(t)}\n" for t in reversed(stamps))
  (work/"run.log").write_text(events+f"RING-EVENTS: complete through {decimal(hi+1)} s\n")
  (work/"pdu.csv").write_text("arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n"+"".join(f"{decimal(t)},{i},14,8.5\n" for i,t in enumerate(stamps)))
  (work/"servo.csv").write_text("t_s,state,pi_run,ew_ns,trim_ppm,meter_valid\n")
  argv=[sys.executable,"-B",str(a.source/"tb/verilator/follow_ring/trace_table.py"),str(work/"run.log"),str(work/"pdu.csv"),str(work/"servo.csv"),"--origin-s",decimal(origin),"--from-s",decimal(start),"--to-s",decimal(end),"--step-s",decimal(step),"--csv",str(work/"table.csv")]
  r=subprocess.run(argv,capture_output=True,text=True);(work/"command.json").write_text(json.dumps(argv)+"\n");(work/"output.log").write_text(r.stdout+r.stderr);(work/"rc").write_text(str(r.returncode)+"\n")
  assert r.returncode==0,r.stderr
  rows=list(csv.DictReader((work/"table.csv").open()));expected=[[] for _ in range(n)]
  for i,t in enumerate(stamps):
   if lo<=t<hi:expected[(t-lo)//step].append(i)
  good=len(rows)==n
  for row,ids in zip(rows,expected):
   good &= row["slips"]==str(0 if kind=="recentre" else len(ids))
   good &= row["skips"]==str(len(ids) if kind=="skip" else 0)
   good &= row["recentres"]==str(len(ids) if kind=="recentre" else 0)
   good &= row["ring_margin_ticks"]==(f"{min(ids):+.3f}..{max(ids):+.3f}" if ids else "-")
   good &= row["event_trace"]=="complete"
  results.append({"name":name,"kind":kind,"pass":good,"bins":n,"samples":len(stamps),"expected_counts":list(map(len,expected))})
  print(json.dumps(results[-1]))
(root/"summary.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"Independent integer-boundary probes: {sum(x['pass'] for x in results)}/{len(results)} passed")
raise SystemExit(int(not all(x["pass"] for x in results)))
