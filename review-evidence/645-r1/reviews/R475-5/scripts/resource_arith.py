"""Judge published route-1x1 figures against the candidate's recorded baseline.

Usage: python3 -I resource_arith.py <tree> <resource-summary.json>
Uses the tree's own syn/ooc/pp_resource_gate.py judge() and baseline. Two
synthetic candidate records share the baseline identity:
  A. the #645 source head's published route-1x1 figures as measured (F base);
  B. a linear composition estimate: #686 record + (#645 figures - F figures).
Neither is a measurement of the composed tree; both are arithmetic only.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", tree / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
baseline = json.loads((tree / "syn/ooc/pp_resource_baseline.json").read_text())
entry = baseline["endpoints"]["route-1x1"]
row = next(r for r in json.loads(Path(sys.argv[2]).read_text())["rows"] if r["endpoint"] == "route-1x1")
base_f, author = row["baseline"], row["candidate"]
rec = entry["record"]
print("recorded baseline (#686):", rec["figures"])
print("F baseline used by #645:", base_f)
print("#645 published candidate:", author)
estimate = {k: (round(rec["figures"][k] + author[k] - base_f[k], 3)) for k in rec["figures"]}
worst = 0
for label, figures in (("A. #645 published figures vs #686 record", author),
                       ("B. linear estimate #686 + (#645 - F)", estimate)):
    cand = copy.deepcopy(rec)
    cand["figures"] = dict(figures)
    cand["inputs_sha256"] = "0" * 64  # differs from the record: judged, not refused
    status, lines = gate.judge(entry, cand, unrouted=[])
    print("==", label, "-> exit", status)
    for line in lines:
        if not line.startswith("  "):
            print("  " + line)
    worst = max(worst, status)
print("floor margin of the #645 measured WNS:", round(author["WNS_ns"] - entry["floor"]["WNS_ns"], 3), "ns")
sys.exit(worst)
