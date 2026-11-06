#!/usr/bin/env python3
"""Compare tb/verilator/fw_service_budget/oracle.json with the published
per-run receipts it was generated from, field by field, and summarise what
moved against the base oracle.

usage: oracle_vs_receipts.py <head-oracle.json> <base-oracle.json>
                             <1x1-all.json> <8x8-all.json> <1x1-paced.json>
"""
import hashlib
import json
import sys

FIELDS = ("rows", "budget_findings", "heartbeat", "liveness")


def main() -> int:
    head = json.load(open(sys.argv[1]))
    base = json.load(open(sys.argv[2]))
    receipts = [json.load(open(p)) for p in sys.argv[3:6]]
    bad = 0
    for i, (row, rec) in enumerate(zip(head, receipts)):
        label = f"row {i} ({row['shape']})"
        checks = {
            "shape": row["shape"] == rec["shape"],
            "raw_log": row["raw_log"] == rec["raw_log"],
            "log_sha256": row["log_sha256"] == rec["log_sha256"]
            == hashlib.sha256(row["raw_log"].encode()).hexdigest(),
            "media": all(row["media"][k] == rec["media"][k]
                         for k in ("populated", "plan", "slots_sha256")),
        }
        for f in FIELDS:
            checks[f] = row[f] == rec[f]
        for k, ok in checks.items():
            print(f"{label}: {k}: {'EQUAL' if ok else 'DIFFERENT'}")
            bad += not ok
    print(f"rows: head {len(head)}, base {len(base)}, receipts {len(receipts)}")
    for i, (h, b) in enumerate(zip(head, base)):
        moved = [k for k in h if h.get(k) != b.get(k)]
        print(f"row {i} ({h['shape']}): fields moved vs base: {moved}")
        hm, bm = h["media"], b["media"]
        print(f"  slots_sha256 base {bm['slots_sha256']} head {hm['slots_sha256']}")
        hv = [(r.get("name") or r.get("duty") or str(j), r.get("verdict"))
              for j, r in enumerate(h["rows"])] if isinstance(h["rows"], list) else None
        bv = [(r.get("name") or r.get("duty") or str(j), r.get("verdict"))
              for j, r in enumerate(b["rows"])] if isinstance(b["rows"], list) else None
        print(f"  row verdicts equal to base: {hv == bv}")
        print(f"  budget_findings equal to base: {h['budget_findings'] == b['budget_findings']}")
    print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
