#!/usr/bin/env python3
"""Read selected author-published receipts from the pinned public evidence commit."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(sys.argv[1]).resolve()
commit="dc64b04aef437e6b15071781f08c62a077827262"
prefix="review-evidence/gptpsw-r1/author-r2/receipts/round2b/"
files=["gates/SUMMARY.txt","gates/register_reference.log","yosys/README.md","harness/egress-ledger-8x8-1if.txt","harness/8x8-1if/table.md","harness/8x8/table.md","harness/selftest/README.md","closedloop/make-gptp_sw.log","closedloop/gptp_sw_mutants-f15b3a7d.log","milan_dp/split-sw.log","milan_dp/split-cdc.log","memory/test_ctrl_memory.log","memory/plat_ledger-self-test.log","route/route-8x8-1if-sw-AltSpreadLogic_high.txt","route/route-8x8-1if-sw-ExtraPostPlacementOpt.txt"]
files += [f"sweep/shard-{i}-results.json" for i in range(4)]
files += [f"fwgate/shard-{i}-62fcd154.log"+(".verdicts" if i else "") for i in range(4)]
files += [f"yosys/shard-{i}.log" for i in range(4)]
print("Public author evidence commit",commit)
for name in files:
 path=prefix+name
 data=subprocess.check_output(["git","-C",str(root),"show",commit+":"+path]);s=data.decode()
 print("\nARTIFACT",path,"sha256",hashlib.sha256(data).hexdigest(),"bytes",len(data))
 if name.endswith("-results.json"):
  j=json.loads(s);print("head",j["head"],"return codes",[r["exit_code"] for r in j["results"]])
 elif len(s)<9000: print(s)
 else: print("Last 30 lines:\n"+"\n".join(s.splitlines()[-30:]))
print("\nLater source history:")
print(subprocess.check_output(["git","-C",str(root),"log","--format=%H %s","62fcd154..HEAD"],text=True))
print("Changed artifacts after 62fcd154:")
print(subprocess.check_output(["git","-C",str(root),"diff","--name-only","62fcd154..HEAD"],text=True))
