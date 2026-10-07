"""Probe: a measurement whose flow drops or changes the synthesis worker cap is
NOT COMPARABLE (exit 2) against every baseline-F endpoint; the unchanged record
is judged 0; and the gate's own flow extraction captures the cap line the
baseline helper prepends.  Usage: python3 -I probe_flow_identity.py <repo>"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", repo / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec)
sys.modules["gate"] = gate
spec.loader.exec_module(gate)
baseline = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
CAP = "set_param synth.maxThreads 1"
failures = 0
for name, entry in baseline["endpoints"].items():
    record = entry["record"]
    flow = record["identity"]["flow"]
    ok_first = flow and flow[0] == CAP
    status, _ = gate.judge(entry, copy.deepcopy(record))
    dropped = copy.deepcopy(record)
    dropped["identity"]["flow"] = [line for line in flow if line != CAP]
    s_drop, lines_drop = gate.judge(entry, dropped)
    changed = copy.deepcopy(record)
    changed["identity"]["flow"] = ["set_param synth.maxThreads 4" if l == CAP else l for l in flow]
    s_chg, _ = gate.judge(entry, changed)
    good = ok_first and status == 0 and s_drop == 2 and s_chg == 2
    failures += not good
    print(f"{name}: cap-first={ok_first} control={status} dropped={s_drop} changed={s_chg} "
          f"{'PASS' if good else 'FAIL'} :: {lines_drop[0][:90]}")
script = CAP + "\ncreate_project -force -name x -part p\nset_param general.maxThreads 32\n"
extracted = [m.group(0).strip() for m in gate.FLOW.finditer(script)]
cap_seen = extracted[:1] == [CAP]
failures += not cap_seen
print(f"FLOW extraction of a capped script: {extracted} {'PASS' if cap_seen else 'FAIL'}")
print("probe_flow_identity:", "PASS" if failures == 0 else f"FAIL ({failures})")
sys.exit(1 if failures else 0)
