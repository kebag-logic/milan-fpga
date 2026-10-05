"""Replace private protocol identities in selected public wire receipts.
Usage: python3 -B sanitize_receipts.py RAW_DIRECTORY PACKET_DIRECTORY
Timing, message/status fields, counters and descriptor indices are preserved.
"""
import hashlib
import json
import sys
from pathlib import Path

raw, packet = map(Path, sys.argv[1:])
rows = [json.loads(x) for x in (raw / "peer-descs-start.jsonl").read_text().splitlines()]
a = bytes.fromhex(next(x["payload"] for x in rows if x.get("what") == "desc-peer-0-0x0000-0"))
peer = a[8:16]
dut = bytes.fromhex("020000fffe000001")
peer_mac = bytes.fromhex(next(x["payload"] for x in rows if x.get("what") == "desc-peer-1-0x0009-0"))[74:80]
neutral_peer = bytes.fromhex("0000000000000003")
neutral_mac = bytes.fromhex("000000000003")
# Primary and auxiliary controllers receive deterministic role tokens.
controllers = {}
for f in sorted(packet.glob("wire-receipts-*.json")):
    for r in json.loads(f.read_text()):
        for key in ("command", "response", "unlock"):
            if r[key]:
                b = bytes.fromhex(r[key]["raw"])
                controllers.setdefault(b[12:20], bytes.fromhex("0000000000000001"))
changed = []
for f in sorted(packet.glob("wire-receipts-*.json")):
    old = f.read_bytes()
    doc = json.loads(old)
    count = 0
    for r in doc:
        for key in ("command", "response", "unlock"):
            if not r[key]:
                continue
            b = bytearray.fromhex(r[key]["raw"])
            assert b[0] in (0xfc, 0xfb)
            b[12:20] = controllers[bytes(b[12:20])]
            if b[0] == 0xfc:
                for off in (20, 28):
                    if b[off:off+8] == peer:
                        b[off:off+8] = neutral_peer
                if b[4:10] == peer_mac:
                    b[4:10] = neutral_mac
                if b[40:46] == peer_mac:
                    b[40:46] = neutral_mac
            elif b[4:12] == peer:
                b[4:12] = neutral_peer
            if r[key]["raw"] != b.hex():
                count += 1
            r[key]["raw"] = b.hex()
    data = (json.dumps(doc, indent=1) + "\n").encode()
    f.write_bytes(data)
    changed.append(dict(file=f.name, before_sha256=hashlib.sha256(old).hexdigest(), after_sha256=hashlib.sha256(data).hexdigest(), rewritten_headers=count))
receipt = dict(reason="Round-2 ruling requires no reference-peer identity in the packet. DUT configured public identity is permitted. Only structured transport/stream/entity identity bytes were replaced.", tokens=dict(controller="0000000000000001", reference_peer="0000000000000003", reference_peer_stream_prefix="000000000003"), original_sources="Retained captures and per-cycle results remain outside the packet; artifact indexes record their hashes.", files=changed)
(packet / "redaction-r2.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(sum(x["rewritten_headers"] for x in changed), "headers sanitized across", len(changed), "files")
