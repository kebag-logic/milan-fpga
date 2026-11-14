"""Audit recorded handler costs against the stated load table. Arguments: checkout result-directory."""
import json,sys
from collections import defaultdict
from pathlib import Path
root,results=map(lambda s:Path(s).resolve(),sys.argv[1:3])
sys.path.insert(0,str(root/"tb/verilator/ctrl_service_budget"))
import load_grade,poll_grade,shape_costs
point="8x8/1if"; shape=shape_costs.of_point(point,root)
costs=load_grade.stated(root,point,load_grade.STATED_US)
functions={"aecp_mbx:frame":"record.aecp","srp_mbx:receive":"record.srp","acmp_mbx:on_frame":"record.acmp","acmp_mbx:on_adp_frame":"record.adp","maap_mbx:receive":"record.maap"}
maxima={}; traces=[]
for path in sorted(results.glob("*.log")):
 for lineno,line in enumerate(path.open(),1):
  values=line.split()
  if len(values)!=6 or values[0]!="SPAN":continue
  name=values[5];cycles=int(values[3])
  if cycles>maxima.get(name,(0,))[0]:maxima[name]=(cycles,path.name,lineno,line.rstrip())
print("Point",point,"shape",tuple(shape),"100 MHz CPU; required us = ceil(measured us * 1.05 / 5) * 5")
bad=[]
for function,key in functions.items():
 if function not in maxima:print(key,"NOT MEASURED");continue
 cycles,file,line,raw=maxima[function];required=((cycles*21+9999)//10000)*5
 print(key,"measured cycles",cycles,"us",cycles/100,"required us",required,"stated us",costs[key],"at",f"{file}:{line}")
 print(raw)
 if required>costs[key]:bad.append(key)
print("Understated record costs:",bad)
print("ADP uses its outer ACMP adapter wrapper; adp_mbx:on_frame is tail-called and its raw SPAN return PC is not a linking call, so it is excluded.")
for path in sorted(results.glob("notice-*.json")):
 g=json.loads(path.read_text());p=g["passes"]
 print("GROUP",g["group"],"probes",len(g["probes"]),"unmeasured",sum(x["status"]!="measured" for x in g["probes"]),"budget misses",sum(not x.get("within_budget",False) for x in g["probes"]))
 for family in ("polls","stated"):
  q=p[family];print(family,"heaviest",q["heaviest"],"limits",q["limits"],"over",q["over"])
 print("rounds",p["rounds"])
 print("slices",p["slices"])
print("This audit covers only the supplied groups and observed handlers; missing paths are not passes.")
