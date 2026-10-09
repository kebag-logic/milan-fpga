#!/usr/bin/env python3
"""Check decimal half-open bins using an independent decimal-time oracle."""
import argparse,csv,decimal,json,pathlib,subprocess,sys
D=decimal.Decimal
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
root=a.packet/"receipts/decimal-boundaries";root.mkdir(parents=True,exist_ok=True)
cases=[("internal-edge","1","0",".4",".1","1.2"),("start-edge",".1",".2",".4",".1",".3"),("end-edge",".1","0",".2",".1",".3")]
results=[]
for name,origin,start,end,step,event in cases:
 for kind in ("dup","skip","recentre"):
  work=root/(name+"-"+kind);work.mkdir(exist_ok=True)
  (work/"run.log").write_text("RING-EVENT: "+kind+" "+event+"\nRING-EVENTS: complete through 2.000000000 s\n")
  (work/"pdu.csv").write_text("arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n")
  (work/"servo.csv").write_text("t_s,state,pi_run,ew_ns,trim_ppm,meter_valid\n")
  cmd=[sys.executable,"-B",str(a.source/"tb/verilator/follow_ring/trace_table.py"),str(work/"run.log"),str(work/"pdu.csv"),str(work/"servo.csv"),"--origin-s",origin,"--from-s",start,"--to-s",end,"--step-s",step,"--csv",str(work/"table.csv")]
  r=subprocess.run(cmd,capture_output=True,text=True);(work/"table.txt").write_text(r.stdout+r.stderr)
  assert r.returncode==0
  with (work/"table.csv").open() as f:rows=list(csv.DictReader(f))
  key="recentres" if kind=="recentre" else "slips"
  actual=[int(row[key]) for row in rows]
  lo=D(origin)+D(start);hi=D(origin)+D(end);width=D(step)
  n=int(((hi-lo)/width).to_integral_value(rounding=decimal.ROUND_CEILING));expected=[0]*n
  if lo<=D(event)<hi:expected[int((D(event)-lo)/width)]+=1
  row={"case":name,"kind":kind,"origin":origin,"from":start,"to":end,"step":step,"event":event,"expected":expected,"actual":actual,"pass":actual==expected,"cli_rc":r.returncode}
  results.append(row);print(json.dumps(row))
(root/"results.json").write_text(json.dumps(results,indent=2)+"\n")
passed=sum(r["pass"] for r in results);print(f"decimal boundary contract: {passed}/{len(results)} passed")
raise SystemExit(0 if passed==len(results) else 1)
