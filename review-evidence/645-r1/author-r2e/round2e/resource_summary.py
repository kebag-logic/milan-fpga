"""Summarize completed repository resource checks without changing a baseline."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

w = Path(__file__).resolve().parent
root = w / "functional/route"
sys.path.insert(0, str(root / "syn/ooc"))
spec = importlib.util.spec_from_file_location("resource_gate", root / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
baseline_path = root / "syn/ooc/pp_resource_baseline.json"
baseline = json.loads(baseline_path.read_text())
rows = []
for endpoint, relative in (
    ("route-1x1", "timing/ax7101/gateware"),
    ("ooc-1x1", "timing/ooc-1x1"),
    ("ooc-8x8", "timing/ooc-8x8"),
):
    rc_path = w / "logs" / ("resource-" + endpoint + ".rc")
    if not rc_path.exists():
        rows.append(dict(endpoint=endpoint, status="NOT RUN"))
        continue
    rc = int(rc_path.read_text())
    row = dict(endpoint=endpoint, rc=rc)
    if rc == 0:
        candidate = gate.record(w / relative, gate.kind_of(w / relative))
        entry = baseline["endpoints"][endpoint]
        original = entry["record"]
        row.update(
            baseline=original["figures"], candidate=candidate["figures"],
            delta={k: round(v-original["figures"][k], 6) for k, v in candidate["figures"].items()},
            identity_matches=candidate["identity"] == original["identity"],
            baseline_inputs_sha256=original["inputs_sha256"],
            candidate_inputs_sha256=candidate["inputs_sha256"],
        )
        assert row["identity_matches"], endpoint
    rows.append(row)
result = dict(
    head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",
    baseline_sha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
    rows=rows,
)
(w / "resource-summary.json").write_text(json.dumps(result, indent=2) + "\n")
for row in rows:
    print(row["endpoint"], row.get("rc", row.get("status")), row.get("candidate", {}))
