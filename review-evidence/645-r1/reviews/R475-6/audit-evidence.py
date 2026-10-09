#!/usr/bin/env python3
"""Read-only comparison of published measurements and the reviewed source."""
import csv, hashlib, json, re, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
base="6aa25dec977c6ad78bf4ff6275de47fb81d0c246"
measured="a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb"
head="1e79ebdc06528edff74c0a7f530f20f99e3326a2"
def read(p):return json.loads(p.read_text())
current=read(root/"syn/ooc/pp_resource_baseline.json")
before=json.loads(subprocess.check_output(["git","show",base+":syn/ooc/pp_resource_baseline.json"],cwd=root))
public=read(out/"author-receipts/author-r2f/resource-receipts/measurement-summary.json")
records=[]
for entry in public["endpoints"]:
 name=entry["endpoint"]
 current_endpoint=current["endpoints"][name]
 old_endpoint=before["endpoints"][name]
 policy=lambda d:{k:d[k] for k in ("tolerance","floor","ceiling") if k in d}
 records.append({"endpoint":name,"record_equal":current_endpoint["record"]==entry["record"],"policy_unchanged":policy(current_endpoint)==policy(old_endpoint),"figures":current_endpoint["record"]["figures"]})
assert all(x["record_equal"] and x["policy_unchanged"] for x in records)
binding=read(out/"author-receipts/author-r2g/round2g/measured-source-binding.json")
for row in binding:
 row["reviewed_sha256"]=hashlib.sha256((root/row["path"]).read_bytes()).hexdigest()
 assert row["reviewed_sha256"]==row["final_sha256"]
changed=subprocess.check_output(["git","diff","--name-only",measured,head],cwd=root,text=True).splitlines()
assert not any(x.startswith("hdl/") for x in changed)
wall=[]
for name in ("follow-default","render-default"):
 r=read(out/("author-receipts/author-r2g/round2g/jobs/"+name+".result.json"))
 wall.append({"leg":name,"seconds":r["seconds"],"scaled_1_58":round(r["seconds"]*1.58,3),"under_1440":r["seconds"]*1.58<=1440,"rc":r["rc"]})
assert all(x["rc"]==0 and x["under_1440"] for x in wall)
log=(out/"trace-probe.log").read_text()
slips=re.search(r"slips before it (\d+), after it (\d+)",log)
rows=list(csv.DictReader((out/"trace-table.csv").open()))
trace={"simulation_slips_before":int(slips[1]),"simulation_slips_after":int(slips[2]),"table_slips":sum(int(r["slips"]) for r in rows),"rows_reporting_slips":[r for r in rows if int(r["slips"])],"simulation_checks_pass":"checks: 18   failures: 0" in log}
assert trace["simulation_slips_before"]==trace["simulation_slips_after"]==0
assert trace["simulation_checks_pass"] and trace["table_slips"]==1
old_area_head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed"
old_dp=subprocess.check_output(["git","show",old_area_head+":hdl/milan/milan_datapath.sv"],cwd=root,text=True)
new_dp=(root/"hdl/milan/milan_datapath.sv").read_text()
def extract(s):
 a=s.index("  localparam int unsigned SRC_SETTLE_ERR_C")
 b=s.index("  end : g_settle_recentre",a)+len("  end : g_settle_recentre")
 return s[a:b]
assert extract(old_dp)==extract(new_dp)
cap_sha=hashlib.sha256((root/"hdl/ieee1722/aaf/KL_chan_map_capture.sv").read_bytes()).hexdigest()
area=read(out/"author-receipts/author-r2e/round2e/area-ooc/comparison.json")
assert cap_sha==area["inputs"]["cmc_head.sv"]["sha256"]
assert all(v<=120 for v in area["combined_delta"].values())
(out/"own-area-source-audit.json").write_text(json.dumps({"measurement_head":old_area_head,"reviewed_head":head,"production_settle_extract_identical":True,"production_settle_extract_sha256":hashlib.sha256(extract(new_dp).encode()).hexdigest(),"capture_sha256":cap_sha,"own_area_delta":area["combined_delta"]},indent=2)+"\n")
result={"head":head,"resource_measurement_head":measured,"records":records,"paths_changed_since_resource_measurement":changed,"binding":binding,"author_default_timings":wall,"trace_diagnostic_counterexample":trace}
(out/"evidence-audit.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
