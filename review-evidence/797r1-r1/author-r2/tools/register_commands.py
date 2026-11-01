#!/usr/bin/env python3
"""Register the freshness-gate commands and pin the two entry scripts in
ci/image/command-table.json, canonical form (rerun after any script edit)."""
import hashlib
import json
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import ci_tool_inventory as inv  # noqa: E402

path = tree / "ci/image/command-table.json"
table = json.loads(path.read_text())
pats = table["commands"]["python3"]["patterns"]
for p in (["scripts/gen_register_reference.py", "--check"], ["scripts/gen_register_reference.py", "--selftest"],
          ["docs/diagrams/memory_map.gen.py", "--check"]):
    if p not in pats:
        pats.append(p)
pats.sort()
reason = "Validation and source inspection: invokes existing tools or local fixtures; installs nothing."
for rel in ("scripts/gen_register_reference.py", "docs/diagrams/memory_map.gen.py"):
    table["scripts"][rel] = {"class": "reviewed non-installing", "reason": reason,
                             "sha256": hashlib.sha256((tree / rel).read_bytes()).hexdigest()}
path.write_text(inv.serialized(table))
print("registered", {k: v["sha256"][:12] for k, v in table["scripts"].items() if "register_reference" in k or "memory_map" in k})
