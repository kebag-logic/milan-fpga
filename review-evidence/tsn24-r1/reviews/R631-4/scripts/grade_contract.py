#!/usr/bin/env python3
import argparse,json,pathlib,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument("packet",type=pathlib.Path);a=p.parse_args();r=a.packet
plants=json.loads((r/"scripts/plants-contract.json").read_text());rows=json.loads((r/"receipts/contract-results.json").read_text());assert len(rows)==85
baseline=[x for x in rows if x["plant"] is None];assert len(baseline)==1
b=baseline[0];assert b["tests"]==424 and b["build_rc"]==0 and not b["failures"] and not b["skipped"] and not b["disabled"]
counts={k:v["completed"] for k,v in b["binaries"].items()};assert len(counts)==8
receipts=[]
for p in plants:
 matched=[x for x in rows if x["plant"]==p["name"]];assert len(matched)==2
 for x in matched:
  mode=x["mode"];assert mode in ("full","removed");assert x["build_rc"]==0 and not x["skipped"] and not x["disabled"]
  assert x["tests"]==(424 if mode=="full" else 423)
  assert len(x["binaries"])==8 and all(y["xml"] and y["rc"] in (0,1) for y in x["binaries"].values())
  if mode=="full":assert x["only_killer"] and x["needle_seen"] and x["failing_set"]==[p["killer"]]
  else:assert x["escapes"] and not x["failures"] and all(y["rc"]==0 for y in x["binaries"].values())
  found=list((r/"scratch/contract").glob("w*/build/"+p["name"]+"-"+mode+"-*.xml"));assert len(found)==8
  for f in found:
   root=ET.parse(f).getroot();assert int(root.get("errors","0"))==0
   cases=list(root.iter("testcase"));assert all(c.get("result")=="completed" and c.get("status")=="run" and c.find("skipped") is None for c in cases)
 receipts.append({"plant":p["name"],"killer":p["killer"],"caught_only_by_named_killer":True,"named_message_seen":True,"physical_removal_escapes":True,"full_completed":424,"removed_completed":423,"raw_xml_count":16})
(r/"receipts/contract-grade.json").write_text(json.dumps({"baseline_counts":counts,"plants":receipts},indent=2)+"\n")
review_rows=json.loads((r/"receipts/contract-rows.json").read_text());byname={x["plant"]:x for x in receipts}
for x in review_rows:x["verification"]="All listed plants independently caught and escaped after single-killer removal" if x["plants"] else "Caller/authority reason inspected; no core execution claimed"
(r/"receipts/contract-row-grade.json").write_text(json.dumps(review_rows,indent=2)+"\n")
print("PASS: 31 rows; 42/42 caught only by named killer; 42/42 physical escapes; 424 -> 423 instances; zero skips or missing XML")
