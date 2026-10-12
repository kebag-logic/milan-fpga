#!/usr/bin/env python3
"""Lane B10 identity facts over ATDECC (new): decode the live ENTITY descriptor that the identity
gate read (identity-aecp.jsonl, READ_DESCRIPTOR ENTITY 0) and compare the four facts the B10
assignment names: entity_id, entity_name, firmware_version and serial_number.

usage: identity_entity_b10.py <identity_dir>
The READ_DESCRIPTOR response payload is configuration_index (2) and reserved (2), then the
descriptor (IEEE 1722.1-2021 7.2.1): entity_id at 4, entity_name at 48 (64 bytes),
firmware_version at 116 (64), serial_number at 244 (64), all relative to the descriptor.
"""
import json
import sys
from pathlib import Path

EXPECT = dict(entity_id="020000fffe000001", entity_name="Milan FPGA 1x1 TDM8", firmware_version="2.96.0",
              serial_number="AX7101-0001")
d = Path(sys.argv[1])
ent = None
for line in (d / "identity-aecp.jsonl").read_text().splitlines():
    if not line.startswith("{"):
        continue
    r = json.loads(line)
    if r.get("cmd") == "READ_DESCRIPTOR" and r.get("req") == "0000000000000000" and r.get("status") == "SUCCESS":
        ent = bytes.fromhex(r["payload"])[4:]
        break


def s(b):
    return b.split(b"\0", 1)[0].decode("utf-8", "replace")


out = []
if ent is None:
    out.append(dict(check="entity-descriptor", result="FAIL", detail="no ENTITY 0 read"))
else:
    got = dict(entity_id=ent[4:12].hex(), entity_name=s(ent[48:112]), firmware_version=s(ent[116:180]),
               serial_number=s(ent[244:308]))
    for k, v in EXPECT.items():
        out.append(dict(check=f"atdecc-{k}", result="PASS" if got[k] == v else "FAIL", detail=dict(read=got[k], expected=v)))
ok = all(o["result"] == "PASS" for o in out)
txt = "\n".join(json.dumps(o) for o in out) + f"\nENTITY FACTS: {'PASS' if ok else 'FAIL'}\n"
(d / "identity-entity-verdict.txt").write_text(txt)
print(txt, end="")
sys.exit(0 if ok else 1)
