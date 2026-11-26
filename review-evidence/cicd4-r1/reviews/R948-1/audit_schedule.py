#!/usr/bin/env python3
"""Inspect event safety, public contexts and the measured regular-worker deal."""
import copy,json,pathlib,subprocess,sys,yaml
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/"scripts"))
import suite_shards as s
base="c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350"
for name in ("docs","elaborate","rtl","rtl-fast"):
 file=f".github/workflows/{name}.yml"
 old=yaml.safe_load(subprocess.check_output(["git","show",base+":"+file],cwd=root))
 new=yaml.safe_load((root/file).read_text())
 for key in (True,"on","concurrency","permissions","env","defaults"):
  assert old.get(key)==new.get(key),(name,key)
 for job in ("changes","full-ci-gate"):
  if job in old["jobs"]:assert old["jobs"][job]==new["jobs"][job],(name,job)
 for job,value in old["jobs"].items():
  assert new["jobs"][job].get("timeout-minutes",360)<=value.get("timeout-minutes",360),(name,job)
 for job,value in new["jobs"].items():
  if "permissions" in value:
   assert job in old["jobs"] and value["permissions"]==old["jobs"][job]["permissions"],(name,job)
 for job in ("ci-fail-fast","ci-terminal-guard"):
  if job in old["jobs"]:
   assert old["jobs"][job].get("if")==new["jobs"][job].get("if"),(name,job)
 print(name,"event/concurrency/permissions/selectors unchanged; no existing timeout increased; no new permission grant")
contexts={}
for name in ("docs","elaborate","rtl","rtl-fast"):
 w=yaml.safe_load((root/f".github/workflows/{name}.yml").read_text())
 for key,job in w["jobs"].items():
  title=job.get("name",key)
  if title in {"rtl-fast","docs-check","wire-accountability","docs-check-no-git","elaborate","verilator-suites","yosys-portability"}:
   contexts[title]=name
assert len(contexts)==7,contexts
print("All seven required context carriers:",json.dumps(contexts,sort_keys=True))
suites=s.expand_suites(s.sweep_suites(root/"tb/verilator"))
issues,loads,bounds=s.headroom_problems(suites,(root/".github/workflows/rtl.yml").read_text())
assert not issues,issues
print("Worker projected seconds:",loads)
print("Maximum regular worker:",max(loads[:-len(s.DEDICATED_SUITES)]),"seconds; bound",s.CI_BUDGET_SECONDS)
print("Dedicated continuous-history worker:",loads[-1],"seconds; separate exception retained")
print("Policy inconsistency: table docs-gates-1=1302, docs-gates-0=738; following prose says slowest docs-gates-0=1395")
print("Keeping the prose's 270-second allowance gives 1572 seconds, 26.2 minutes, 228 seconds margin")
