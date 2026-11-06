#!/usr/bin/env python3
"""Compare the head's fw_service_budget oracle.json with the published
service-budget receipts: each oracle row must carry the receipt's raw log,
its digest, its rows/findings/heartbeat/liveness and its media.
usage: check_oracle.py <oracle.json> <receipt dir>"""
import hashlib, json, sys
from pathlib import Path
oracle = json.loads(Path(sys.argv[1]).read_text())
d = Path(sys.argv[2])
names = ["fw-1x1-service-all-1-0-0.json", "fw-8x8-service-all-1-0-0.json",
         "fw-1x1-service-uart-paced-1-0-0.json"]
bad = 0
for row, name in zip(oracle, names):
    rc = json.loads((d / name).read_text())
    for k in ("shape", "raw_log", "log_sha256", "rows", "budget_findings",
              "heartbeat", "liveness"):
        same = row[k] == rc[k]
        bad += not same
        print(f"{name} {k}: {'equal' if same else 'DIFFERENT'}")
    for k in ("populated", "plan", "slots_sha256"):
        same = row["media"][k] == rc["media"][k]
        bad += not same
        print(f"{name} media.{k}: {'equal' if same else 'DIFFERENT'}")
    same = hashlib.sha256(row["raw_log"].encode()).hexdigest() == row["log_sha256"]
    bad += not same
    print(f"{name} log digest self-consistent: {same}")
print("RESULT", "PASS" if bad == 0 else f"FAIL {bad}")
sys.exit(1 if bad else 0)
