#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys,xml.etree.ElementTree as ET
root=pathlib.Path(sys.argv[1]);campaign=pathlib.Path(sys.argv[2]);output=pathlib.Path(sys.argv[3])
table=json.loads((root/"tests/mutations.json").read_text());results=json.loads((campaign/"results.json").read_text());markers=json.loads((campaign/"message-markers.json").read_text());begin,end=["\n"+m+"\n" for m in markers]
assert len(table)==len(results)==311
assert {r["name"] for r in results}=={p["name"] for p in table}
assert all(r["status"]=="CAUGHT" and r["rc"]==1 for r in results)
rows=[]
for plant in table:
 module=pathlib.Path(plant["path"]).stem
 default="maap_debug" if any(k["test"].startswith("MaapDebug.") for k in plant["kills"]) else module
 for kill in plant["kills"]:
  arm=kill.get("arm",default);report=campaign/plant["name"]/(arm+".xml");doc=ET.parse(report).getroot();cases=list(doc.iter("testcase"))
  assert len(cases)==int(doc.get("tests")) and all(c.get("status")=="run" and c.get("result")=="completed" and c.find("skipped") is None for c in cases)
  found=[]
  for case in cases:
   name=case.get("classname")+"."+case.get("name")
   if not (name.startswith(kill["test"]) if kill["test"].endswith("/") else name==kill["test"]):continue
   for f in case.findall("failure"):
    text=f.get("message","");streams=[]
    while begin in text:
     _,_,text=text.partition(begin);stream,sep,text=text.partition(end)
     assert sep;streams.append(stream)
    if any(kill["needle"] in stream for stream in streams):found.append(name)
  assert found,(plant["name"],kill)
  rows.append({"plant":plant["name"],"arm":arm,"test":kill["test"],"needle":kill["needle"],"matched":found,"report_sha256":hashlib.sha256(report.read_bytes()).hexdigest()})
assert len(rows)==329
baseline=[]
for report in sorted((campaign/"baseline").glob("*.xml")):
 doc=ET.parse(report).getroot();assert int(doc.get("failures"))==0 and int(doc.get("disabled"))==0
 baseline.append({"arm":report.stem,"tests":int(doc.get("tests"))})
assert sum(x["tests"] for x in baseline)==369
output.write_text(json.dumps({"plants":311,"named_streamed_killers":329,"baseline_instances":369,"baseline":baseline,"killers":rows},indent=2)+"\n")
print("311/311 names; 329/329 streamed-message killers; 369 baseline instances")
