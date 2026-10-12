#!/usr/bin/env python3
"""Copy only hash-verified public runtime inputs into disposable storage."""
import argparse, hashlib, json, pathlib
p = argparse.ArgumentParser()
p.add_argument("packet", type=pathlib.Path)
p.add_argument("dependency_root", type=pathlib.Path)
a = p.parse_args()
source = a.packet / "receipts/public/author-r5/evidence-r5/runtime/provenance.json"
prefix = "$WORKSPACE_HOME/litex-milan/"
count = 0
for record in json.loads(source.read_text())["files"]:
    if not record["path"].startswith(prefix):
        continue
    relative = record["path"][len(prefix):]
    data = (a.dependency_root / relative).read_bytes()
    assert len(data) == record["size"]
    assert hashlib.sha256(data).hexdigest() == record["sha256"], relative
    target = a.packet / "scratch/dependencies" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    count += 1
print("PASS copied", count, "runtime sources and headers at the published hashes")
