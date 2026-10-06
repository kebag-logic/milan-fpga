#!/usr/bin/env python3
"""Recheck published area arithmetic and shared-function equivalence."""
import json, subprocess, sys, re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E=P/"scratch/review-evidence/645-r1/author/stage2e/merged"
A=E/"area-route"
O=P/"scratch/area-proof"; O.mkdir(exist_ok=True)
with (P/"receipts/shared-proof.log").open("w") as log:
 rc=subprocess.run([sys.executable,"-B",str(A/"prove_shared.py"),str(A),str(O)],stdout=log,stderr=subprocess.STDOUT).returncode
assert rc==0
proof=json.loads((O/"shared_logic_equivalence.json").read_text())
assert len(proof["cells"])==10
assert all(x["identical"] and x["assignments"]==65536 and x["base_sha256"]==x["head_sha256"] for x in proof["cells"])
assert proof["negative_control"]["caught"]
x=json.loads((A/"candidate_area_comparison.json").read_text())
count=lambda f:len((A/f).read_text().splitlines())
counts={name:count(name) for name in ["candidate_settle_cone.tsv","candidate_unchanged_LUT_cone.tsv","candidate_shared_band_LUT.tsv","candidate_owned_LUT_upper_bound.tsv","candidate_settle_cells.tsv","capture_added_FF.txt"]}
assert counts["candidate_settle_cone.tsv"]==80
assert counts["candidate_unchanged_LUT_cone.tsv"]==6
assert counts["candidate_shared_band_LUT.tsv"]==10
assert counts["candidate_owned_LUT_upper_bound.tsv"]==63
assert counts["candidate_settle_cells.tsv"]==41
assert counts["capture_added_FF.txt"]==32
lut_delta=1125-1076
own_lut=80-1-6-10+lut_delta
own_ff=41+32
assert own_lut==112 and own_ff==73
rows={}
for name in ["settle_base","settle_head","cmc_base","cmc_head"]:
 text=(E/"area-ooc"/("util_"+name+".rpt")).read_text()
 rows[name]={key:int(float(re.search(r"\|\s*"+re.escape(key)+r"\*?\s*\|\s*([0-9.]+)",text).group(1))) for key in ["Slice LUTs","Slice Registers"]}
delta={key:sum(rows[n+"_head"][key]-rows[n+"_base"][key] for n in ["settle","cmc"]) for key in ["Slice LUTs","Slice Registers"]}
assert delta=={"Slice LUTs":80,"Slice Registers":73}
result={"ooc_rows":rows,"ooc_delta":delta,"routed_files_counts":counts,"routed_own_lut":own_lut,"routed_own_ff":own_ff,"shared_identical_functions":10,"all_assignments":65536,"planted_control_caught":True,"limit":120,"result":"PASS"}
(P/"receipts/area-verification.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
