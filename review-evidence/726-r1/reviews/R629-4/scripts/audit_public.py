#!/usr/bin/env python3
"""Independently grade public author measurements and control receipts."""
import collections,json,pathlib,sys
packet=pathlib.Path(sys.argv[1]); source=packet/"receipts/public/author-r4/review-round4"
summary={}
for condition in ("clean","frames-only"):
 for shape in (1,8):
  text=(source/f"measure-{condition}-{shape}.log").read_text(); notes=collections.defaultdict(list); gaps={}
  for line in text.splitlines():
   fields=line.split(",")
   if fields[0]=="NOTE":notes[tuple(map(int,fields[1:4]))].append(int(fields[4]))
   if fields[0]=="GAPS":gaps[tuple(map(int,fields[2:5]))]=list(map(float,fields[6:]))
  assert len(notes)==4*(shape+1)==len(gaps)
  deltas=[]
  for key,times in notes.items():
   delta=[(b-a)/1000 for a,b in zip(times,times[1:])];count,low,high,tail,service=gaps[key]
   assert len(times)==count and min(delta)==low and max(delta)==high
   assert low>=1000 and high<=1000+service and tail<=1000+service
   for shift in (0,200,300,800,900,1000000):
    shifted=[t for t in times if t>=shift];differences=[b-a for a,b in zip(shifted,shifted[1:])]
    assert len(shifted)>=2 and min(differences)>=1000000 and max(differences)<=1000000+service*1000
   deltas.extend(delta)
  summary[f"{condition}-{shape}"]={"rows":len(notes),"gaps":len(deltas),"min_ms":min(deltas),"max_ms":max(deltas),"max_service_ms":max(g[4] for g in gaps.values())}
  if condition=="frames-only":
   rows=[line.split(",") for line in text.splitlines() if line.startswith("OUTPUT_CONDITION,")]
   assert len(rows)==shape+1 and all(r[2:]==["frames-only","0","0","1","0","0","0"] for r in rows)
  assert "RESULT: PASS" in text and "[FAIL]" not in text
plants={}
for name,group in {"tx-interval":"TX","rx-interval":"RX","tx-reset":"TX_RESET","aaf-reset":"RX_RESET","crf-reset":"RX_RESET","rx-saturation":"RX","late":"CADENCE","rate":"RATE","tx-nodirty":"OUTPUT_CADENCE","grid":"PHASE"}.items():
 prefix="plant-grid" if name=="grid" else "earlier-scratch__plant-"+name
 run=(source/(prefix+"__run.log")).read_text();escape=(source/(prefix+"__escape.log")).read_text();failures=[s for s in run.splitlines() if "[FAIL]" in s]
 assert failures and all("[726 "+group+"]" in s for s in failures)
 assert "RESULT: PASS" in escape and "[FAIL]" not in escape
 plants[name]={"failure_group":group,"failures":len(failures),"escape":"PASS"}
summary["public_plants"]=plants
for i in range(78):
 item=json.loads((source/f"docs-{i:02}.json").read_text())
 if i==35:
  assert item["rc"]==124
  recovered=json.loads((source/"builder-complete.json").read_text())
  assert recovered["observer_rc"]==recovered["container_rc"]==recovered["logs_rc"]==0
  summary["builder_recovery"]={"initial_observer_rc":124,**recovered}
 else:assert item["rc"]==0,(i,item)
summary["public_docs_receipts"]=78
(packet/"receipts/independent-receipt-audit.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
