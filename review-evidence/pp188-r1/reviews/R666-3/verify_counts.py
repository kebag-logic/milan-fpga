#!/usr/bin/env python3
"""Recount published campaign lines and check the live-body snapshot."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=ROOT/"public/author-r2/receipts/round2"
body=(ROOT/"pr-body.md").read_text()
required="150 -> 161 mutation entries, all KILLED; 17 golden runs PASS at each revision, plus one passing assertion-coverage check (94/94 -> 101/101), giving 168 -> 179 total campaign checks"
assert required in body
print("PASS live PR Records contains required corrected wording")
suites={}
for rev,mut,cov,total,acmp,checks,pp,srp in [("base",150,94,168,60,1030051,10533,1352),("head",161,101,179,65,1030070,10543,1361)]:
 log=(R/f"campaigns/{rev}/srp_top.log").read_text()
 killed=re.findall(r"^.* KILLED tags=.*$",log,re.M)
 gold=re.findall(r"^control .*rc=0 PASS$",log,re.M)
 assert (len(killed),len(gold))==(mut,17)
 assert f"assertion coverage: {cov}/{cov}; missing=[]" in log
 assert f"{total} checks: {total} PASS, 0 FAIL" in log
 assert len(killed)+len(gold)+1==total
 print(f"PASS {rev}: {mut} KILLED entries + {len(gold)} golden PASS + coverage {cov}/{cov} = {total} checks")
 a=(R/f"campaigns/{rev}/acmp.log").read_text()
 entries=[json.loads(x) for x in a.splitlines() if x.startswith("{")]
 assert sum(x["verdict"]=="KILLED" for x in entries)==acmp
 assert f"ACMP mutations: {acmp} of {acmp} KILLED" in a
 print(f"PASS {rev}: ACMP {acmp} killed mutation entries")
 log=(R/f"gates/{rev}/run_suites.log").read_text()
 rows=re.findall(r"^PASS (\w+) \((\d+) checks: (\d+) PASS, (\d+) FAIL\)$",log,re.M)
 assert all(n==passed and fail=="0" for _,n,passed,fail in rows)
 suites[rev]={name:int(n) for name,n,_,_ in rows}
 assert sum(suites[rev].values())==checks
 assert suites[rev]["pp_top"]==pp and suites[rev]["srp_stream_fsms"]==srp
 print(f"PASS {rev}: {len(rows)} suites, summed checks={checks}, pp_top={pp}, srp_stream_fsms={srp}")
 for group in ["campaigns","gates"]:
  rcs=list((R/group/rev).glob("*.rc"))
  assert all(p.read_text().strip()=="0" for p in rcs)
  print(f"PASS {rev}: {group} {len(rcs)} final return codes all 0")
failed={}
for rev in ["base","head"]:
 failed[rev]={p.stem:p.read_text().strip() for p in (R/"consumers"/rev).glob("*.rc") if p.read_text().strip()!="0"}
assert failed["base"]==failed["head"] and len(failed["base"])==2
print("PASS identical consumer failure map:",json.dumps(failed["base"],sort_keys=True))
changed={k:(v,suites["head"][k]) for k,v in suites["base"].items() if suites["head"][k]!=v}
assert set(changed)=={"pp_top","srp_stream_fsms"}
print("PASS only two suite counts changed:",json.dumps(changed,sort_keys=True))
for rev,lut in [("base",56701),("head",56105)]:
 log=(R/f"consumers/ooc-{rev}/ooc_pp_shadow.log").read_text()
 row=re.search(r"^KL_pp_shadow\s+(.*)$",log,re.M).group(1).split()
 assert list(map(int,row))==[lut,4236,lut+4236,26299,15,4,10,2392]
 print(f"PASS {rev}: LUT={lut}; other resource categories unchanged; LUT_TOT is LUT+LUTRAM")
print("PASS all numeric Records claims checked")

for b in sorted((R/"campaigns/base").glob("*.log")):
 if b.stem in ["srp_top","acmp"]: continue
 h=R/"campaigns/head"/b.name
 def normalized(path):
  t=path.read_text().replace("<submodule>","<source>").replace("<lane>","<source>").replace("base-camps","revision-camps").replace("head-camps","revision-camps")
  return sorted(t.splitlines())
 assert normalized(b)==normalized(h),b.stem
 print(f"PASS {b.stem}: other campaign results identical after path normalization and ordering")
for name in ["lint_hdl","gen_matrix","yosys_run","elab_guards_yosys"]:
 assert (R/f"gates/base/{name}.log").read_bytes()==(R/f"gates/head/{name}.log").read_bytes()
 print(f"PASS {name}: raw gate log byte-identical")
