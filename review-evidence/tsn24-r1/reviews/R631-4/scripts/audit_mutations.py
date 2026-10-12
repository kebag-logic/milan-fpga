#!/usr/bin/env python3
import argparse,fnmatch,json,pathlib,re,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("work",type=pathlib.Path);p.add_argument("out",type=pathlib.Path);a=p.parse_args()
ms=json.loads((a.source/"tests/mutations.json").read_text());rs=json.loads((a.work/"results.json").read_text());assert len(rs)==len(ms)==388
assert len({x["name"] for x in rs})==388 and {x["name"] for x in rs}=={x["name"] for x in ms}
assert all(x["status"]=="CAUGHT" and x["rc"]==1 for x in rs)
begin,end=json.loads((a.work/"message-markers.json").read_text());pattern=re.compile(re.escape("\n"+begin+"\n")+r"(.*?)"+re.escape("\n"+end+"\n"),re.S)
names=lambda root:{x.get("classname")+"."+x.get("name") for x in root.iter("testcase")}
bases={f.stem:names(ET.parse(f).getroot()) for f in (a.work/"baseline").glob("*.xml")}
needles=0;receipts=[]
for m in ms:
 default="maap_debug" if any(x["test"].startswith("MaapDebug.") for x in m["kills"]) else pathlib.Path(m["path"]).stem
 arms={k.get("arm",default) for k in m["kills"]}
 for arm in sorted(arms):
  kills=[k for k in m["kills"] if k.get("arm",default)==arm];root=ET.parse(a.work/m["name"]/(arm+".xml")).getroot();cases=list(root.iter("testcase"))
  expected={n for n in bases[arm] if any(n.startswith(k["test"]) if k["test"].endswith("/") else n==k["test"] for k in kills)}
  assert expected and names(root)==expected and len(cases)==len(expected)==int(root.get("tests"))
  assert root.get("errors")=="0" and root.get("disabled")=="0"
  assert all(c.get("status")=="run" and c.get("result")=="completed" and c.find("skipped") is None and c.find("error") is None for c in cases)
  assert int(root.get("failures"))==sum(bool(c.findall("failure")) for c in cases)
  for k in kills:
   owns=[c for c in cases if (c.get("classname")+"."+c.get("name")).startswith(k["test"]) if k["test"].endswith("/")]
   if not k["test"].endswith("/"):owns=[c for c in cases if c.get("classname")+"."+c.get("name")==k["test"]]
   assert any(k["needle"] in "\0".join(pattern.findall(f.get("message",""))) for c in owns for f in c.findall("failure")),(m["name"],k)
   needles+=1
 receipts.append({"plant":m["name"],"arms":sorted(arms),"required_needles_verified":len(m["kills"])})
a.out.write_text(json.dumps({"plants":len(ms),"required_needles_verified":needles,"all_complete":True,"receipt_rows":receipts},indent=2)+"\n");print("PASS",len(ms),"plants",needles,"streamed assertion needles")
