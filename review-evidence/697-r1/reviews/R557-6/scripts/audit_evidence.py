#!/usr/bin/env python3
import collections,hashlib,json,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve(); table=json.loads((root/"tests/mutations.json").read_text()); output={}
for label,work in (("local",p/"scratch/suites/linux"),("hosted",p/"scratch/hosted/quality-evidence")):
 campaign=work/"mutations"; results=json.loads((campaign/"results.json").read_text()); markers=json.loads((campaign/"message-markers.json").read_text()); pattern=re.compile(re.escape("\n"+markers[0]+"\n")+"(.*?)"+re.escape("\n"+markers[1]+"\n"),re.S)
 assert len(results)==len(table)==311 and {r["name"] for r in results}=={r["name"] for r in table}
 assert all(r["status"]=="CAUGHT" for r in results)
 rows=[]; xmls=set()
 for plant in table:
  module=pathlib.Path(plant["path"]).stem
  default="maap_debug" if any(k["test"].startswith("MaapDebug.") for k in plant["kills"]) else module
  for kill in plant["kills"]:
   arm=kill.get("arm",default); path=campaign/plant["name"]/(arm+".xml"); doc=ET.parse(path).getroot(); cases=list(doc.iter("testcase")); names=[c.get("classname")+"."+c.get("name") for c in cases]; xmls.add(str(path.relative_to(campaign)))
   assert len(names)==len(set(names))==int(doc.get("tests")) and int(doc.get("errors"))==int(doc.get("disabled"))==0
   assert all(c.get("status")=="run" and c.get("result")=="completed" and not c.findall("skipped") and not c.findall("error") for c in cases)
   selected=[c for c,name in zip(cases,names) if name.startswith(kill["test"]) if kill["test"].endswith("/")] if kill["test"].endswith("/") else [c for c,name in zip(cases,names) if name==kill["test"]]
   assert selected
   matches=[]
   for c in selected:
    for f in c.findall("failure"):
     message=f.get("message",""); streams=pattern.findall(message)
     if any(kill["needle"] in stream for stream in streams): matches.append(c.get("classname")+"."+c.get("name"))
   assert matches,(label,plant["name"],kill)
   rows.append({"plant":plant["name"],"arm":arm,"test":kill["test"],"needle":kill["needle"],"matching_failures":matches,"status":"CAUGHT_BY_STREAMED_MESSAGE"})
 assert len(rows)==329
 (p/"receipts"/(label+"-killer-audit.json")).write_text(json.dumps(rows,indent=2)+"\n")
 gates=json.loads((work/"gates.json").read_text()); assert all(x["rc"]==0 for x in gates)
 output[label]={"gate_count":len(gates),"gate_failures":0,"plants":len(results),"named_catches":311,"killers":len(rows),"per_arm_xml":len(xmls),"comment_controls":len(re.findall(r"^comment control ",(work/"comments.log").read_text(),re.M)),"templates":(work/"assertion-templates.log").read_text().strip(),"graphs":len(list((work/"graphs").glob("*.svg")))}
 if label=="local":
  counts={}
  for config in ("gcc","clang-sanitizers"):
   text=(work/config/"Testing/Temporary/LastTest.log").read_text(); numbers=[int(n) for n in re.findall(r"\[==========\] (\d+) tests? from .* ran\.",text)]
   assert sum(numbers)==369 and len(numbers)==7 and "[  SKIPPED ]" not in text
   counts[config]={"instances":sum(numbers),"binaries":len(numbers),"skipped":0}
  output[label]["instances"]=counts
for label,name in (("pull_request","hosted-jobs.json"),("push","hosted-push-jobs.json")):
 jobs=json.loads((p/"receipts"/name).read_text())["jobs"]
 assert {j["name"] for j in jobs}=={"quality","bare-metal"} and all(j["conclusion"]=="success" for j in jobs)
 output[label]={"jobs":2,"steps":sum(len(j["steps"]) for j in jobs),"skipped_steps":sum(s["conclusion"]=="skipped" for j in jobs for s in j["steps"])}
old=p/"scratch/public-evidence/review-evidence/697-r1"; manifest=json.loads((old/"MANIFEST.json").read_text()); assert all(hashlib.sha256((old/r["file"]).read_bytes()).hexdigest()==r["published_sha256"] for r in manifest)
output["initial_public_packet"]={"commit":"2ae0b85299a979413a5ba4b7fe3e3de175967a19","verified_manifest_entries":len(manifest),"scope":"Original-import evidence, not current-head or manager source execution"}
(p/"receipts/evidence-audit.json").write_text(json.dumps(output,indent=2)+"\n"); print(json.dumps(output,indent=2))
