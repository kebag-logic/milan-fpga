#!/usr/bin/env python3
"""Per-point input recording, ROM digests against the tracked ledger, anchors and route receipts.

Usage: check_receipts2.py <run-receipts.json> <syn/yosys/rom_digests.tsv> <page.md> <234 findings page>
"""
import json, re, sys
rr = json.load(open(sys.argv[1])); ledger = open(sys.argv[2]).read(); page = open(sys.argv[3]).read(); f234 = open(sys.argv[4]).read()
fails = []
for name, r in rr["points"].items():
    inp = r["inputs"]
    if r["point"]["top"] == "milan_datapath" and not inp.get("shape_header"): fails.append(f"{name}: no shape header digest")
    if not inp.get("design.v"): fails.append(f"{name}: no design digest")
    for rom, dig in r.get("roms", {}).items():
        if dig not in ledger: fails.append(f"{name}: ROM {rom} {dig[:16]} not in ledger")
    if any(v != 0 for v in r["rc"].values()): fails.append(f"{name}: rc {r['rc']}")
    if r["point"].get("anchor") and "flat" not in r["rc"]: fails.append(f"{name}: anchor without flat run")
print("points with ROMs recorded:", sum(1 for r in rr["points"].values() if r.get("roms")), "of", len(rr["points"]))
for name, a in rr["anchors"].items():
    d16 = a["log"]["sha256"][:16]
    row = re.search(rf"\| [^|]+ \| {a['rc']} \| {a['minutes_under_lock']} \| `ooc.log` \| `{d16}` \| {a['log']['bytes']:,} \|", page)
    print("anchor", name, "rc", a["rc"], "min", a["minutes_under_lock"], "log", d16, "page row", bool(row))
    if not row: fails.append(f"anchor {name} row not on page")
ck = rr["route_checkpoint"]["sha256"]
print("route checkpoint", ck[:16], "in #234 page:", ck[:16] in f234 or ck in f234)
if ck[:16] not in f234: fails.append("checkpoint digest not in #234 findings")
print("FAILURES" if fails else "ALL PASS", fails[:20])
