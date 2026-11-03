#!/usr/bin/env python3
"""Build an elaborate aggregate download root from real LiteX leg receipts.

usage: mk_gate_root.py <clone> <litex-receipt-dir> <root-out>
Writes passing worker receipts (production record()) and passing builder leg receipts
(the gate selftest's builder_receipts helper) bound to the clone's real head, tree and
template digest, copies litex-leg-*.json in, and prints the CI_GATE_NEEDS JSON."""
import hashlib, json, shutil, sys
from pathlib import Path
clone, litex_dir, root = map(Path, sys.argv[1:4])
sys.path.insert(0, str(clone / "scripts"))
from ci_case_receipts import canonical, source_identity
from ci_gate_receipts import StepContext, record
from ci_gate_workflows import TEMPLATES, case_inventory, load_template, worker_id, worker_legs
from ci_gate_workflows import builder_command
from ci_builder_legs import requirements
import ci_gate_workflows_selftest as st
name = "elaborate"
identity = source_identity(clone)
source = load_template(clone, name)
digest = hashlib.sha256((clone / TEMPLATES[name]).read_bytes()).hexdigest()
cases = case_inventory(name, source)
actual = {case["id"]: {"outcome": "success", "conclusion": "success"} for case in cases}
for leg in worker_legs(name, source):
    d = root / f"gate-elaborate-{leg}"; d.mkdir(parents=True)
    (d / "receipt.json").write_bytes(canonical(record(name, leg, source, identity, digest,
                                                      StepContext(actual, "true"))) + b"\n")
flags = requirements(builder_command(name, source))
for i, b in enumerate(st.builder_receipts(identity, flags=tuple(flags))):
    (root / f"gate-elaborate-{i}" / f"builder-leg-{i}.json").write_bytes(canonical(b) + b"\n")
for f in sorted(litex_dir.glob("litex-leg-*.json")):
    shutil.copy(f, root / f"gate-elaborate-{2 + int(f.stem.rsplit('-', 1)[1])}" / f.name)
print(json.dumps({worker_id(name, leg): {"result": "success"} for leg in worker_legs(name, source)}))
