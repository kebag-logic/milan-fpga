#!/usr/bin/env python3
import argparse,hashlib,json,pathlib
p=argparse.ArgumentParser();p.add_argument("packet",type=pathlib.Path);a=p.parse_args();r=a.packet;s=r/"scratch"
physical=[]
for f in sorted(s.glob("physical-*/physical-removal.json")):physical.extend(json.loads(f.read_text()))
assert len(physical)==31 and len({x["plant"] for x in physical})==31
assert all(x["build_rc"]==x["suite_rc"]==0 and x["escapes"] and not x["removed_present_after"] and not x["still_failing_tests"] for x in physical)
esc=json.loads((s/"escape/escape-probe.json").read_text());reg=[x for x in esc if x["plant"].startswith("dafresh-")];assert len(reg)==29
assert all(x["escapes_without_killer"] and x["suite_without_killer_rc"]==0 and x["killer_fails_with_needle"] and x["killer_alone_rc"]==8 and not x["other_failures"] for x in reg)
zero=next(x for x in esc if x["plant"]=="x-zero-never-expires");assert zero["result"]=="CAUGHT"
yaml=next(x for x in esc if x["plant"]=="y-yaml-wide-range");assert yaml["caught"] and yaml["escapes_without_owner"]
gap=json.loads((s/"gap-mutants/gap-mutants.json").read_text());assert len(gap)==6 and all(x["result"]=="CAUGHT" for x in gap)
fs=json.loads((r/"receipts/r630-3-full-suite.json").read_text());assert len(fs)==17
required={"r630-3-listener-range-only":"AcmpFresh.ListenerInterfaceMismatch","r630-3-withdrawal-clears-probe":"AcmpFresh.FreshProbeAfterListenerWithdrawal","r630-3-init-keeps-listener":"AcmpFresh.InitClearsListener"}
for name,killer in required.items():
 x=next(x for x in fs if x["plant"]==name);assert x["build_rc"]==0 and x["tests"]==424 and x["failing_set"]==[killer] and x["caught"] and x["skipped"]==x["disabled"]==0
 assert len(x["binaries"])==8 and all(b["xml"] and b["rc"] in (0,1) for b in x["binaries"].values())
ids=[]
for f in (r/"scripts/prior").glob("*.py"):
 raw=f.read_bytes();ids.append({"file":str(f.relative_to(r)),"sha256":hashlib.sha256(raw).hexdigest(),"git_blob":hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()})
public=json.loads((r/"receipts/public-fetch.json").read_text())
for x in ids:
 origin=next(z for z in public if z["local"]==x["file"]);assert x["git_blob"]==origin["blob"] and x["sha256"]==origin["sha256"];x["source"]=origin["source"];x["unchanged"]=True
result={"physical_removals":len(physical),"all_physical_escapes":True,"filtered_dafresh_catches_and_escapes":len(reg),"zero_mutant_caught":True,"yaml_owner_catch_and_escape":True,"gap_mutants":gap,"r630_3_required_all_caught":required,"r630_3_exploratory_survivors":[x["plant"] for x in fs if not x["caught"]],"escape_exploratory_survivors":[x["plant"] for x in esc if x.get("result")=="SURVIVED"],"unchanged_script_identities":ids}
(r/"receipts/prior-probe-grade.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps({k:v for k,v in result.items() if k not in ("gap_mutants","unchanged_script_identities")},indent=2))
