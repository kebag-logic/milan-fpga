"""Audit role-safe publication against retained private protocol receipts.
Usage: python3 -B audit_packet_r2.py RAW_DIRECTORY PACKET_DIRECTORY FINDINGS_PAGE
Only local retained files are accessed. Private values are never printed.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from wire import records

raw, packet, page = map(Path, sys.argv[1:])
rows = [json.loads(x) for x in (raw / "peer-descs-start.jsonl").read_text().splitlines()]
a = bytes.fromhex(next(r["payload"] for r in rows if r.get("what") == "desc-peer-0-0x0000-0"))
private = {"entity_id": a[8:16], "entity_name": a[52:116].split(bytes(1))[0], "group_name": a[184:248].split(bytes(1))[0], "serial": a[248:312].split(bytes(1))[0]}
for r in rows:
    if "-0x0009-" in r.get("what", ""):
        b = bytes.fromhex(r["payload"])
        suffix = r["what"].rsplit("-", 1)[1]
        private["interface_mac_" + suffix] = b[74:80]
        private["clock_identity_" + suffix] = b[82:90]
violations = []
files = sorted(x for x in packet.rglob("*") if x.is_file())
for name, value in private.items():
    assert value and value != bytes(len(value))
    variants = {value.lower(), value.hex().encode(), b":".join(f"{x:02x}".encode() for x in value), value.hex().encode().hex().encode()}
    if name == "entity_name":
        variants |= {x.lower() for x in value.split() if len(x) >= 4}
    for f in files + [page]:
        data = f.read_bytes().lower()
        if any(x in data for x in variants):
            violations.append(dict(file=f.name, field=name))
checked = 0
for f in sorted(packet.glob("wire-receipts-*.json")):
    for case in json.loads(f.read_text()):
        source = {r["i"]: r for r in records(raw / case["capture"], not case["capture"].endswith("observer.pcap"))}
        for key in ("command", "response", "unlock"):
            r = case[key]
            old = source[r["i"]]
            assert (old["tns"], old["status"], old["port"]) == (r["tns"], r["status"], r["port"])
            b, c = bytearray.fromhex(old["raw"]), bytearray.fromhex(r["raw"])
            assert len(b) == len(c)
            spans = ((4, 36), (40, 46)) if b[0] == 0xfc else ((4, 20),)
            for start, end in spans:
                b[start:end] = bytes(end-start)
                c[start:end] = bytes(end-start)
            assert b == c, "non-identity bytes changed"
            checked += 1
oversized = [f.name for f in files if f.stat().st_size > 200000]
result = dict(passed=not violations and not oversized, scanned_packet_files=len(files), private_field_categories=len(private), private_identity_matches=violations, page_included=True, compared_wire_headers=checked, nonidentity_wire_bytes_unchanged=True, oversized_files=oversized, largest_packet_file_bytes=max(f.stat().st_size for f in files), note="Peer identities checked as bytes, text, hexadecimal and colon-delimited forms, including encoded protocol fields. DUT configured public identity is permitted by the ruling.")
print(json.dumps(result, indent=2))
sys.exit(0 if result["passed"] else 1)
