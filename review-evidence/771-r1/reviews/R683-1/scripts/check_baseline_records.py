#!/usr/bin/env python3
"""Usage: check_baseline_records.py BASE_JSON HEAD_JSON RECEIPT_DIR
Checks: policy fields (tolerance/floor/ceiling) unchanged base->head; each head
record equals the author's record-head-<ep>.json.log receipt; recomputes the
deltas head-vs-dev-receipt and head-vs-base-record and their verdict vs tolerance."""
import json, sys, os
def load(path):
    # receipts may end with a trailing "rc=N" line after the JSON object
    return json.JSONDecoder().raw_decode(open(path).read())[0]
base = json.load(open(sys.argv[1]))["endpoints"]; head = json.load(open(sys.argv[2]))["endpoints"]; rd = sys.argv[3]
rc = 0
for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    b, h = base[ep], head[ep]
    pol = {k: (b.get(k), h.get(k)) for k in ("tolerance", "floor", "ceiling")}
    same = all(x == y for x, y in pol.values())
    rec_h = load(os.path.join(rd, f"record-head-{ep}.json.log"))
    rec_d = load(os.path.join(rd, f"record-dev-{ep}.json.log"))
    eq = (rec_h == h["record"])
    idsame = (b["record"]["identity"] == h["record"]["identity"] == rec_d["identity"])
    print(f"{ep}: policy_unchanged={same} head_record_equals_receipt={eq} identity_same_base_head_dev={idsame}")
    if not (same and eq): rc = 1
    tol = h["tolerance"]
    for f in ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "WNS_ns", "WHS_ns"):
        if f not in h["record"]["figures"]: continue
        hv, dv, bv = h["record"]["figures"][f], rec_d["figures"][f], b["record"]["figures"][f]
        t = tol.get(f)
        print(f"   {f:7} record708={bv} dev={dv} head={hv}  head-dev={round(hv-dv,3):+} head-708={round(hv-bv,3):+} dev-708={round(dv-bv,3):+} tol={t}"
              + ("  OVER" if t is not None and f not in ('WNS_ns','WHS_ns') and hv - dv > t else ""))
    print("   floor", h.get("floor"), "ceiling", h.get("ceiling"))
sys.exit(rc)
