#!/usr/bin/env python3
"""Compare the graded rows of three 1x1 `all` service traces: the dev
oracle (base), the dev re-measure receipt and the head oracle.
usage: compare_service_rows.py <dev oracle.json> <dev receipt.json> <head oracle.json>"""
import json, sys
from pathlib import Path
dev_o = json.loads(Path(sys.argv[1]).read_text())[0]
dev_r = json.loads(Path(sys.argv[2]).read_text())
head_o = json.loads(Path(sys.argv[3]).read_text())[0]
for k in ("rows", "budget_findings", "heartbeat", "liveness"):
    print(f"{k}: dev-oracle==dev-remeasure {dev_o[k] == dev_r[k]}; "
          f"dev-remeasure==head {dev_r[k] == head_o[k]}; dev-oracle==head {dev_o[k] == head_o[k]}")
print("media slots: dev", dev_r["media"]["slots_sha256"] == head_o["media"]["slots_sha256"])
