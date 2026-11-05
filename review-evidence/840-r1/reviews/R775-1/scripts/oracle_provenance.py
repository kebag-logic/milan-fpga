#!/usr/bin/env python3
"""Reviewer probe: check that the service-budget oracle has the exact shape
gen_oracle.py writes (key order, json.dumps indent 2 plus newline), that each
row's raw_log hashes to its log_sha256, and summarise the PHY and identity
evidence carried in each raw log.

Usage: python3 -I oracle_provenance.py <repo-root>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
path = root / "tb/verilator/fw_service_budget/oracle.json"
text = path.read_text()
rows = json.loads(text)
print("byte-identical to json.dumps(rows, indent=2)+newline:",
      json.dumps(rows, indent=2) + "\n" == text)
want = ["shape", "raw_log", "log_sha256", "media", "rows", "budget_findings",
        "heartbeat", "liveness"]
for i, row in enumerate(rows):
    digest = hashlib.sha256(row["raw_log"].encode()).hexdigest()
    print(f"row {i}: shape={row['shape']} plan={row['media'].get('plan')} "
          f"populated={row['media'].get('populated')} keys_in_gen_order={list(row) == want} "
          f"digest_ok={digest == row['log_sha256']}")
    log = row["raw_log"]
    for pattern in (r"02:4b:4c:00:00:0[12]", r"024b4cfffe00000[12]", r"02:00:00:00:00:0[12]",
                    r"020000fffe00000[12]", r"PHY[^\n]{0,80}", r"MDIO[^\n]{0,80}"):
        found = re.findall(pattern, log, re.IGNORECASE)
        if found:
            print(f"   {pattern!r}: {len(found)} e.g. {found[0][:90]!r}")
