"""Compare descriptors and library verdicts from three independent enumerations."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import re
p = Path(__file__).resolve().parent.parent
def canonical(o):
 return json.dumps(o, sort_keys=True, separators=(",", ":")).encode()
def stable_model(o):
 if isinstance(o, dict):
  return {k:stable_model(v) for k,v in o.items() if k != "dynamic"}
 if isinstance(o, list):
  return [stable_model(v) for v in o]
 return o
def descriptors(o, found):
 if isinstance(o, dict):
  for k,v in o.items():
   if k.endswith("_descriptors") and isinstance(v, list):
    for d in v:
     found[k.removesuffix("_descriptors").upper()].append(d["_index (informative)"])
   descriptors(v, found)
 elif isinstance(o, list):
  for v in o:
   descriptors(v, found)
models = []
verdicts = []
for n in (1,2,3):
 j = json.loads((p / f"run-{n}.entity.json").read_text())
 log = (p / f"run-{n}.log").read_text()
 assert "rc=0" in log and "complaints=0" in log and "query-errors 0" in log
 assert j["adp_information"]["common"]["entity_id"] == "0x020000FFFE000001"
 assert j["entity_model_id"] == "0x001BC5C40236BA0E"
 found = defaultdict(list, ENTITY=[0])
 descriptors(j["entity_model"], found)
 inv = {k:sorted(v) for k,v in sorted(found.items())}
 (p / f"run-{n}.inventory.json").write_text(json.dumps(inv, indent=2)+"\n")
 model = stable_model(j["entity_model"])
 models.append(model)
 verdict = {k:j[k] for k in ["compatibility_flags", "compatibility_events", "milan_compatibility_version", "milan_information", "diagnostics"]}
 verdicts.append(verdict)
 print(json.dumps({"run":n,"window":[l for l in log.splitlines() if l.startswith(("START ","END "))], "verdict":verdict,"statistics":j["statistics"], "descriptor_counts":{k:len(v) for k,v in inv.items()},"total_descriptors":sum(map(len,inv.values())),"static_tree_sha256":hashlib.sha256(canonical(model)).hexdigest()}))
assert models[0] == models[1] == models[2]
assert verdicts[0] == verdicts[1] == verdicts[2]
assert all(v["compatibility_flags"] == ["IEEE17221", "MILAN"] and not v["compatibility_events"] for v in verdicts)
print("STABLE: all static descriptor trees, descriptor inventories and compatibility verdicts are identical across three fresh controller instances.")
