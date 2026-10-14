#!/usr/bin/env python3
"""Verify public receipt contents without rerunning banks or claiming fresh execution."""
import ast,copy,hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/"scripts"))
from ci_case_receipts import verify
from ci_suite_pieces import inventory
commit="ef2f49e58bf81e5e149e7698221161f5ce0fbef2"
prefix="review-evidence/737-r1/author-r2/"
inputs=[]
publication=json.loads(subprocess.check_output(["git","show",commit+":review-evidence/737-r1/MANIFEST.json"],cwd=root))
publication={row["file"]:row for row in publication}
def raw(name):
 data=subprocess.check_output(["git","show",commit+":"+prefix+name],cwd=root)
 inputs.append({"path":prefix+name,"sha256":hashlib.sha256(data).hexdigest()});return data
def read(name):return json.loads(raw(name))
summary=read("round2-case-evidence/comparison-summary.json");comparisons=[]
for row in summary:
 suite=row["suite"];directory="round2-case-evidence/"+suite+"/"
 names=inventory(suite);assert names==row["inventory"]
 full=read(directory+"full.json");legs=[read(directory+f"leg{n}.json") for n in range(row["legs"])]
 reference=verify(names,[full],suite,row["head"],row["tree"])
 actual=verify(names,legs,suite,row["head"],row["tree"]);assert actual==reference
 changed=copy.deepcopy(legs)
 for leg in changed:
  leg["inventory"].remove(names[-1]);leg["results"]=[v for v in leg["results"] if v["case"]!=names[-1]]
 try: verify(names,changed,suite,row["head"],row["tree"])
 except ValueError: dropped="refused"
 else:raise AssertionError("dropped case accepted")
 changed=copy.deepcopy(legs);changed[0]["results"][0]["output_sha256"]="f"*64
 assert verify(names,changed,suite,row["head"],row["tree"])!=reference
 comparisons.append({"suite":suite,"head":row["head"],"tree":row["tree"],"cases":len(names),"legs":len(legs),"equal_recorded_observations":True,"fresh_inventory_matches":True,"dropped_from_all_claims":dropped,"changed_observation":"different"})
resources=read("round2-resumed-resource-summary.json");memory=[]
for row in resources["receipts"]:
 data=raw(row["receipt"]);published=publication["author-r2/"+row["receipt"]]
 assert hashlib.sha256(data).hexdigest()==published["published_sha256"]
 assert row["sha256"]==published["original_sha256"]
 receipt=json.loads(data);assert receipt["returncode"]==0 and not any(receipt["memory_events"].values())
 assert receipt["memory_peak_bytes"]==row["peak_bytes"]<receipt["container_limit_bytes"]==8*2**30
 memory.append({"class":row["class"],"cpus":row["cpus"],"peak_bytes":row["peak_bytes"],"returncode":0,"all_memory_events_zero":True,"publication_path_redacted":published["path_redacted"]})
build=read("round2-dispatcher-build.json")
files={"patch_sha256":"ci/act/fail-fast.patch","controls_sha256":"ci/act/parallel_executor_test.go","admission_sha256":"ci/act/job_admission.go","cpu_ranges_sha256":"ci/act/cpu_ranges.go","cpu_controls_sha256":"ci/act/cpu_ranges_test.go","dependencies_sha256":"ci/act/dependency_executor.go","dependency_controls_sha256":"ci/act/dependency_executor_test.go","recipe_sha256":"scripts/build_ci_act.py"}
for key,path in files.items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==build[key],path
measurement="21bd10cec1a999791c9cd2c6d37c52372fb1504e"
old=subprocess.check_output(["git","show",measurement+":scripts/act_ci.py"],cwd=root,text=True)
assert ast.dump(ast.parse(old))==ast.dump(ast.parse((root/"scripts/act_ci.py").read_text()))
changes=subprocess.check_output(["git","diff","--name-only",measurement+"..HEAD"],cwd=root,text=True).splitlines()
assert set(changes)=={"scripts/act_ci.py","docs/testing/CI_WORKFLOWS.md"}
rows=read("round2-dispatch-start-times.json");dispatch=[]
for replay in sorted({row["replay"] for row in rows}):
 groups={}
 for row in rows:
  if row["replay"]!=replay:continue
  key=row["job"]+"/"+row["event"]
  groups.setdefault(key,[]).append(row["time"])
 dispatch.append({"replay":replay,"observed_intervals":{key:{"first":min(times),"last":max(times)} for key,times in groups.items()}})
headroom=read("round2-worker-headroom.json")
assert len(headroom)==16
for row in headroom: assert row["projection_seconds"]<=row["bound_seconds"]==row["limit_minutes"]*60*.6
out={"public_evidence_commit":commit,"comparisons":comparisons,"comparison_limit":"Recorded verdicts, return codes and output digests verified; original per-case stdout was not available in this packet and was not rehashed. No full suite rerun.","memory":memory,"max_peak_bytes":max(row["peak_bytes"] for row in memory),"slot_arithmetic_gib":"4 * 8 + 4 = 36; not a simultaneous peak measurement","dispatcher_input_digests_match_head":True,"dispatcher_version":build["version"],"dispatcher_binary_not_executed":True,"measurement_source_to_head_files":changes,"runner_ast_unchanged":True,"dispatch_start_receipts":dispatch,"worker_projection_own_limit_checks":16,"inputs":inputs}
print(json.dumps(out,indent=2))
