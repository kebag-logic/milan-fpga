#!/usr/bin/env python3
"""Require completed golden/negative-control executions and check documented counts."""
import importlib.util,json,pathlib,re,sys
sys.dont_write_bytecode=True
src=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
spec=importlib.util.spec_from_file_location("campaign_records",src/"tb/pp_top/notify_mutants.py")
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
records=json.loads((out/"receipts/notify/results.json").read_text())
byname={r["mutant"]:r for r in records}
assert len(records)==len(byname)==96
for r in records:
 assert r["build_rc"]==0 and r["completed"] and not r["missing"],r
 if r["mutant"].startswith("golden-"):
  assert r["verdict"]=="PASS" and r["run_rc"]==0 and not r["failing_checks"],r
 else:
  assert r["verdict"]=="KILLED" and r["run_rc"]!=0 and r["failing_checks"],r
assert set(byname)-{k for k in byname if k.startswith("golden-")}=={x.name for x in m.MUTANTS}
readme=(src/"tb/pp_top/README.md").read_text()
groups={"DN":m.DOMAIN_NOTIFY,"interface_rows":m.INTERFACE_ROWS,"depth_and_probes":m.INTERFACE_DEPTH_PROBES}
checked={}
for label,group in groups.items():
 rows=[]
 for arm in group:
  line=next(x for x in readme.splitlines() if x.startswith("| `"+arm.name+"` |"))
  text=line.split("|")[3].strip();documented=int(re.match(r"[0-9]+",text).group())
  r=byname[arm.name];actual=len(r["failing_checks"]);assert actual==documented,(arm.name,actual,documented)
  rows.append({"name":arm.name,"failing_checks":actual,"documented_checks":documented,"named_checks":r["named_checks"]})
 checked[label]=rows
summary={"goldens_passed":10,"controls_killed":86,"controls_total":86,"build_failures":0,"incomplete_runs":0,"missing_named_failures":0,"merge_groups":checked}
(out/"receipts/campaign-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
