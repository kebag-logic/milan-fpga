import json, sys
from pathlib import Path
root=Path.cwd()
sys.path[:0]=[str(root/"sw/firmware/ctrl/test")]
import test_ctrl_firmware as gate
import ctrl_mutants, srp_mutants, srp_pub_mutants
kind, index = sys.argv[1], int(sys.argv[2])
work=Path(sys.argv[3]);work.mkdir(parents=True,exist_ok=True)
print("toolchain:",gate.fw_gtest.toolchain(),flush=True)
print("tsn-c-stack at",gate.stack_pin(),flush=True)
if kind == "control":
 gate.cut_reuse(work/"reuse")
 table=ctrl_mutants.sliced((index+1,4))
 bad=ctrl_mutants.campaign(work/"mutants",work/"reuse",4,(index+1,4))
else:
 interfaces=int(kind[-1])
 table=srp_mutants.DEFECTS
 if interfaces==1:
  table=tuple(d for d in table if d.name.startswith(("four-way-", "binding-", "feedback-", "r10-", "p11-", "srp-bound-", "srp-term-", "srp-poll-extra", "srp-send-extra", *srp_pub_mutants.ROUND5)))
 table=table[index::2]
 srp_mutants.DEFECTS=table
 bad=srp_mutants.campaign(work/"mutants",root/"third_party/lwSRP",4,interfaces)
(work/"population.json").write_text(json.dumps([m.name for m in table],indent=2)+"\n")
print("RESULT:","FAIL" if bad else "PASS",len(table),flush=True)
raise SystemExit(int(bad))
