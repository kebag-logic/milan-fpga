#!/usr/bin/env python3
"""Round-4 census of every ACMP command in the lane, by destination.

Usage: acmp_census_r4.py <archived author dir>

Tests the PR #622 body's Round 2 F2 phrase "210 ACMP commands all to the
peer's input" against the controller transcripts. Two record shapes carry ACMP
exchanges:
  - kind 'transaction' with 'mt' (IEEE 1722.1 ACMP message type: 6
    CONNECT_RX_COMMAND, 8 DISCONNECT_RX_COMMAND), destination read from the
    response's listener_uid (the peer's Stream Input 8 in this lane);
  - role/what 'state-<type>-<index>' records whose response is an ACMPDU
    (stream_id, controller, talker, listener, *_uid, conn_count): GET_RX_STATE
    for descriptor type 5 (STREAM_INPUT), GET_TX_STATE for type 6
    (STREAM_OUTPUT).
Byte-duplicate snapshot.jsonl copies of snapshot-after.jsonl are excluded.
Prints no identifier other than record labels.
"""
import json
import sys
from collections import Counter
from pathlib import Path

A = Path(sys.argv[1])
MT = {6: "CONNECT_RX", 8: "DISCONNECT_RX"}
ACMPDU = {"stream_id", "talker", "listener", "talker_uid", "listener_uid", "conn_count"}

files, dups = [], 0
for p in sorted(A.rglob("*.jsonl")):
    if p.name == "snapshot.jsonl" and (p.parent / "snapshot-after.jsonl").read_bytes() == p.read_bytes():
        dups += 1
        continue
    files.append(p)

acmp = Counter()
shape_bad = []
for p in files:
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        if r.get("kind") == "transaction":
            acmp[(MT.get(r["mt"], f"mt{r['mt']}"), f"peer? listener_uid {resp.get('listener_uid')}")] += 1
            continue
        w = r.get("what")
        if isinstance(w, str) and w.startswith("state-"):
            _, t, i = w.split("-")
            if not ACMPDU <= set(resp):
                shape_bad.append((p.relative_to(A).as_posix(), w))
            name = {"5": "GET_RX_STATE", "6": "GET_TX_STATE"}.get(t, f"state type {t}")
            kind = {"5": "Stream Input", "6": "Stream Output"}.get(t, t)
            acmp[(name, f"{r.get('role')} {kind} {i}")] += 1

print("duplicate snapshot.jsonl excluded:", dups)
print("state records without an ACMPDU-shaped response:", shape_bad or "none")
print("distinct ACMP commands (command, destination):")
for k in sorted(acmp):
    print(f"  {k[0]:14s} {k[1]:28s} {acmp[k]}")
tot = sum(acmp.values())
state_changing = sum(v for (c, _), v in acmp.items() if c in ("CONNECT_RX", "DISCONNECT_RX"))
to_dut = sum(v for (c, d), v in acmp.items() if d.startswith("dut "))
to_dut_si = sum(v for (c, d), v in acmp.items() if d.startswith("dut Stream Input"))
print("total distinct ACMP commands:", tot)
print("  state-changing (CONNECT_RX + DISCONNECT_RX):", state_changing)
print("  addressed to the DUT:", to_dut, "of which to a DUT Stream Input:", to_dut_si)
print("  so '210 ACMP commands all to the peer's input' holds only for the state-changing subset:",
      state_changing == 210 and to_dut > 0)
