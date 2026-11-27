#!/usr/bin/env python3
"""Verify the public evidence packet and its exact-source bindings. Run in the candidate clone."""
import ast,hashlib,json,pathlib,subprocess,sys
import yaml
OUT=pathlib.Path(__file__).resolve().parent
REV="d96d07a8bfe91d12391acf37e888b4f47e527fbd"
HEAD="0f7402ee97d347352b8c3d613033c440ee55986a"
BASE="review-evidence/usbaudfpga-r1/"
def git(*args):return subprocess.check_output(["git",*args])
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(p):return git("show",REV+":"+BASE+p)
manifest=json.loads(blob("MANIFEST.json"))
checks=[]
for row in manifest:
 p=row["file"]
 if not (p.startswith("author-r5/") or p.startswith("author-r3-route/")):continue
 data=blob(p)
 assert sha(data)==row["published_sha256"],p
 target=OUT/"scratch/public"/p
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 checks.append({"path":p,"sha256":sha(data),"redacted":row["path_redacted"]})
root=OUT/"scratch/public/author-r5/receipts-r5"
def read(n):return json.loads((root/n).read_text())
tracked=git("ls-tree","-r","--name-only",HEAD).decode().splitlines()
source_checks=[]
sources=read("source-digests.json")
for row in sources["audio_sources"]:
 matches=[p for p in tracked if pathlib.PurePosixPath(p).name==row["artifact"] and sha(git("show",HEAD+":"+p))==row["sha256"]]
 assert matches,row
 source_checks.append({"artifact":row["artifact"],"matches":matches,"sha256":row["sha256"]})
network=[]
for row in read("network-identity.json")["files"]:
 if row["result"]=="DELETED_IN_BOTH":
  for rev in (HEAD,"b4a1df4a"):
   assert not any(pathlib.PurePosixPath(p).name==row["artifact"] for p in git("ls-tree","-r","--name-only",rev).decode().splitlines())
  network.append({"artifact":row["artifact"],"result":"DELETED_IN_BOTH"});continue
 matches=[p for p in tracked if pathlib.PurePosixPath(p).name==row["artifact"] and sha(git("show",HEAD+":"+p))==row["sha256"]]
 if row.get("group")=="network regression": matches=[p for p in matches if p.startswith("tb/verilator/usbnet/")]
 assert len(matches)==1,(row,matches)
 p=matches[0]
 assert git("ls-tree",HEAD,"--",p).split(None,3)[:3]==git("ls-tree","b4a1df4a","--",p).split(None,3)[:3],p
 network.append({"path":p,"result":"IDENTICAL","sha256":row["sha256"]})
gates=read("repository-gates.json")
wf=git("show",HEAD+":"+gates["workflow"])
assert sha(wf)==gates["workflow_sha256"]
y=yaml.safe_load(wf)
gate_checks=[]
for row in gates["gate_results"]:
 step=next(s for s in y["jobs"][row["job"]]["steps"] if s.get("id")==row["gate"])
 body=step["run"]
 variants={"as_yaml":body,"newline":body.rstrip()+"\n","strip":body.strip(),"strict_shell":"set -euo pipefail\n"+body}
 match=[name for name,b in variants.items() if sha(b.encode())==row["command_sha256"]]
 gate_checks.append({"job":row["job"],"gate":row["gate"],"name":step["name"],"exit":row["exit"],"command_hash_match":match})
 assert row["exit"]==0
 assert match
expected_gates={(j,s["id"]) for j,job in y["jobs"].items() for s in job["steps"] if s.get("id", "").startswith("gate_") and "run" in s}
assert {(r["job"],r["gate"]) for r in gate_checks}==expected_gates
reg=read("regression.json")
assert sha((root/"long-run.txt").read_bytes())==reg["long_run_sha256"]
default_manifest=next(r for r in manifest if r["file"]=="author-r5/receipts-r5/default-run.txt")
default_binding={"published_excerpt_sha256":default_manifest["published_sha256"],"full_log_receipt_sha256":reg["default_log_sha256"],"full_log_available":False}
assert sha((OUT/"audio-contract.md").read_bytes())==read("contract-delta.json")["merged_document_sha256"]
result={"head":HEAD,"evidence_commit":REV,"evidence_signature_status":git("show","-s","--format=%G?",REV).decode().strip(),"packet_files":checks,"audio_source_bindings":source_checks,"network_identity":network,"workflow_gate_bindings":gate_checks,"million_frame_log_hash":"PASS","default_run_excerpt":default_binding,"merged_contract_hash":"PASS"}
(OUT/"packet-audit.json").write_text(json.dumps(result,indent=2)+"\n")
print("Verified",len(checks),"published files;",len(source_checks),"audio sources;",len(network),"network entries;",len(gate_checks),"workflow commands")
print("Command matches",sum(bool(r["command_hash_match"]) for r in gate_checks))
print("Evidence commit signature status",result["evidence_signature_status"])
support={"route_reports":[],"corners":[]}
for row in read("route-report-manifest.json")["files"]:
 data=(root/"physical-reports"/row["file"]).read_bytes()
 assert sha(data)==row["published_sha256"],row["file"]
 support["route_reports"].append({"file":row["file"],"sha256":sha(data)})
for row in read("arty-route.json")["corners"]:
 lines=(root/"physical-reports"/("digilent_arty_audio_"+row["corner"]+"_timing.rpt")).read_text().splitlines()
 i=next(i for i,l in enumerate(lines) if "TNS Total Endpoints" in l)
 vals=[float(v) for v in lines[i+2].split()]
 assert vals[0]==row["setup_ns"] and vals[4]==row["hold_ns"] and vals[8]==row["pulse_width_ns"]
 assert all(vals[k]==0 for k in [1,2,5,6,9,10])
 support["corners"].append({"corner":row["corner"],"summary":vals})
cost=read("arty-cost.json")
assert all(cost["audio"][k]-cost["baseline"][k]==v for k,v in cost["difference"].items())
support["cost_arithmetic"]="PASS"
union=read("builder-union.json")
allcases=[c for leg in union["legs"] for c in leg["cases"]]
assert len(allcases)==115 and len(set(allcases))==115 and set(allcases)==set(union["inventory"])
support["builder_cases"]=115
support["calibration"]="NOT RUN"
old=ast.parse(git("show","9a3bd0f8:tb/verilator/ctrl_service_budget/run.py").decode())
new=ast.parse(pathlib.Path("tb/verilator/ctrl_service_budget/burst_report.py").read_text())
names=read("report-extraction.json")["extracted_functions"]
for name in names:
 a=next(x for x in old.body if isinstance(x,ast.FunctionDef) and x.name==name)
 b=next(x for x in new.body if isinstance(x,ast.FunctionDef) and x.name==name)
 assert ast.dump(a)==ast.dump(b),name
support["identical_extracted_functions"]=names
controls=read("defect-controls.json")["controls"]
assert len(controls)==77 and all(r["result"]=="CAUGHT" for r in controls)
expected_plants={}
for filename in ("mutations.py","transport_mutations.py"):
 tree=ast.parse((pathlib.Path("tb/verilator/usbaudio")/filename).read_text())
 table=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="PLANTS" for t in n.targets))
 expected_plants.update({row[0]:row[-1] for row in ast.literal_eval(table)})
assert {r["plant"]:r["check"] for r in controls}==expected_plants
support["named_defects"]=77
support["all_defects_caught"]=True
(OUT/"supporting-audit.json").write_text(json.dumps(support,indent=2)+"\n")
