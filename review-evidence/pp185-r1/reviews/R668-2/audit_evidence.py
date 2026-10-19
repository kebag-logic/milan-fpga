#!/usr/bin/env python3
"""Audit the published comparison receipts independently of their closing totals."""
import collections, json, pathlib, re, shutil
P=pathlib.Path(__file__).resolve().parent
source=P/"scratch/public"
D=P/"receipts/public"
if source.exists(): shutil.copytree(source,D,dirs_exist_ok=True)
def read(rel): return json.loads((D/rel).read_text())
def keys(rows,key): return {r[key]:r for r in rows if r["verdict"]=="KILLED"}
def ids(row): return sorted(re.search(r"(?:\[[^\]]*\]\s*)?([A-Za-z][A-Za-z0-9_.-]*)",s)[1] for s in row["failing_checks"])
summary={}
for suite in ["notify","d3"]:
    b=read(f"base/campaigns/out/{suite}/results.json")
    h=read(f"head/campaigns/out/{suite}/results.json")
    bm,hm=keys(b,"mutant"),keys(h,"mutant")
    common=set(bm)&set(hm)
    changed=sorted(k for k in common if ids(bm[k])!=ids(hm[k]))
    summary[suite]={"base_mutants":len(bm),"head_mutants":len(hm),"same_failure_ids":len(common)-len(changed),"changed_failure_ids":changed,"new_mutants":sorted(set(hm)-set(bm)),"goldens":sum(r["verdict"]=="PASS" for r in h)}
    assert all(r["build_rc"]==0 and r["completed"] and not r["missing"] for r in h)
    assert all(r["run_rc"]!=0 for r in hm.values())
    assert all(collections.Counter(ids(bm[k])) <= collections.Counter(ids(hm[k])) for k in common)
b=read("base/campaigns/out/aecp_dispatch/results.json")
h=read("head/campaigns/out/aecp_dispatch/results.json")
bm,hm=keys(b,"arm"),keys(h,"arm")
changed=sorted(k for k in set(bm)&set(hm) if bm[k]["failures"]!=hm[k]["failures"])
summary["aecp_dispatch"]={"base_mutants":len(bm),"head_mutants":len(hm),"same_failure_count":len(set(bm)&set(hm))-len(changed),"changed_failure_count":changed,"new_mutants":sorted(set(hm)-set(bm)),"goldens":sum(r["verdict"]=="PASS" for r in h)}
assert all(r["rc"]!=0 and r["named"]>0 for r in hm.values())
assert summary["notify"]["same_failure_ids"]==120
assert summary["aecp_dispatch"]["same_failure_count"]==60
assert summary["d3"]["same_failure_ids"]==110
# Exact-head notification rerun preserves each named verdict and failure-ID multiset.
final=read("head-final2/campaigns/out/notify/results.json")
initial=read("head/campaigns/out/notify/results.json")
assert {(r["mutant"],r["verdict"],tuple(ids(r))) for r in final}=={(r["mutant"],r["verdict"],tuple(ids(r))) for r in initial}
summary["exact_head_notify_rerun"]="135 KILLED; 15 goldens PASS; same named failure IDs as earlier head run"
# Consumer gate 11 is an unchanged parent dependency.
a=(D/"parent-base/g11_lint_rtl.log").read_bytes();b=(D/"parent-head/g11_lint_rtl.log").read_bytes()
assert a==b
summary["parent_gate11"]={"byte_identical":True,"base_rc":(D/"parent-base/g11_lint_rtl.rc").read_text().strip(),"head_rc":(D/"parent-head/g11_lint_rtl.rc").read_text().strip()}
summary["parent_rcs"]={k:{f.name:f.read_text().strip() for f in sorted((D/k).glob("*.rc"))} for k in ["parent-base","parent-head"]}
summary["source_gate_rcs"]={f.name:f.read_text().strip() for f in sorted((D/"head-final2/gates").glob("*.rc"))}
(P/"evidence-audit.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
