#!/usr/bin/env python3
"""Verify the public author receipt index from git objects, without executing it."""
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
commit = "60ce747fdc9f10e928c87525f3dbc5c5bdaa9780"
prefix = "review-evidence/665f4-r1/author-r8/"
def blob(path):
    return subprocess.check_output(["git", "show", f"{commit}:{prefix}{path}"])

gates = json.loads(blob("ROUND8-GATES.json"))
assert gates["head"] == "a6e6916826448f81de2b779ca61a87a9f8c47278"
assert len(gates["receipts"]) == 102
verified = []
unretained = []
for receipt in gates["receipts"]:
    assert receipt["rc"] == 0, receipt["label"]
    record = receipt.get("retained_log")
    if record is None:
        unretained.append(receipt["label"])
        continue
    data = blob(record["path"])
    assert len(data) == record["size"], receipt["label"]
    assert hashlib.sha256(data).hexdigest() == record["sha256"], receipt["label"]
    verified.append(receipt["label"])
print(json.dumps({"evidence_commit": commit, "head": gates["head"],
                  "zero_exit_records": len(gates["receipts"]),
                  "independently_hashed_retained_logs": verified,
                  "indexed_but_raw_log_unretained": unretained}, indent=2))
