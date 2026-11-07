#!/usr/bin/env python3
"""Check every oracle.json row against the published fixture receipts (raw_log, digest, media, grading).
Usage: python3 -I oracle_vs_receipts.py <oracle.json> <service-budget receipts dir>"""
import hashlib, json, sys, pathlib
rows = json.load(open(sys.argv[1])); d = pathlib.Path(sys.argv[2])
files = ["fw-1x1-service-all-1-0-0.json", "fw-8x8-service-all-1-0-0.json", "fw-1x1-service-uart-paced-1-0-0.json"]
bad = 0
for row, f in zip(rows, files):
    r = json.load(open(d / f))
    checks = {
        "shape": row["shape"] == r["shape"],
        "raw_log": row["raw_log"] == r["raw_log"],
        "log_sha256": row["log_sha256"] == r["log_sha256"] == hashlib.sha256(row["raw_log"].encode()).hexdigest(),
        "media": all(row["media"][k] == r["media"][k] for k in ("populated", "plan", "slots_sha256")),
        **{k: row[k] == r[k] for k in ("rows", "budget_findings", "heartbeat", "liveness")},
    }
    bad += sum(not v for v in checks.values())
    print(f, row["shape"], " ".join(f"{k}={'ok' if v else 'DIFF'}" for k, v in checks.items()))
print("RESULT", "PASS" if not bad else f"FAIL({bad})"); sys.exit(1 if bad else 0)
