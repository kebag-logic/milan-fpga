"""Assemble one elaborate gate-results tree: production-recorded step receipts for every worker,
stand-in builder leg receipts (the builder legs were not run locally), and the real LiteX leg receipts."""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, "scripts")
from ci_gate_workflows import ROOT, case_inventory, load_template, worker_legs
from ci_gate_workflows_selftest import builder_receipts
from ci_case_receipts import canonical, source_identity
out, legs_dir, dropped = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None
source = load_template(ROOT, "elaborate")
cases = case_inventory("elaborate", source)
steps = {case["id"]: {"outcome": "success", "conclusion": "success"} for case in cases}
identity = source_identity(ROOT)
env = dict(os.environ, GITHUB_SHA=identity[0], CI_GATE_STEPS=json.dumps(steps), CI_GATE_SCOPE="true")
for leg in worker_legs("elaborate", source):
    subprocess.run(["python3", "scripts/ci_gate_receipts.py", "record", "--workflow", "elaborate", "--leg", str(leg),
                    "--output", str(out / f"gate-elaborate-{leg}" / "receipt.json")], env=env, check=True)
for receipt in builder_receipts(identity):
    (out / f"gate-elaborate-{receipt['leg']}" / f"builder-leg-{receipt['leg']}.json").write_bytes(canonical(receipt) + b"\n")
for leg in range(3):
    receipt = json.loads((legs_dir / f"litex-leg-{leg}.json").read_text())
    if dropped and leg == 1:
        receipt["results"] = [row for row in receipt["results"] if row["simulation"] != dropped]
    (out / f"gate-elaborate-{leg + 2}" / f"litex-leg-{leg}.json").write_bytes(canonical(receipt) + b"\n")
print("assembled", out, "dropped:", dropped)
