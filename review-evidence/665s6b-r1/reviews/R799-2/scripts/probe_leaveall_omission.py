#!/usr/bin/env python3
"""Plant, in a copy of the split's capture, one MSRP LeaveAll frame whose Domain Message keeps its LeaveAll
vector but drops the Domain's value vector, so the declared Domain is omitted from that LeaveAll, and print what the head's grade says of it.

usage: probe_leaveall_omission.py LEG_DIR SPLIT.json OUT.json
"""
import json
import sys
from pathlib import Path

leg = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(leg))
import twin_decode as td  # noqa: E402
import twin_mrp  # noqa: E402
import twin_plants as tp  # noqa: E402

doc = json.loads(Path(sys.argv[2]).read_text())
done = None
for entry in doc["frames"]:
    found = tp.frame_fields(entry)
    if found is None or found[0] != "MSRP" or entry["ms"] < 20000:
        continue
    data = bytearray(bytes.fromhex(entry["hex"]))
    s = found[1]
    if 4 not in td.msrp_frame(s)[1]:
        continue
    offset = s.at + 1
    while offset + 4 <= len(data) and data[offset:offset + 2] != b"\0\0":
        kind, length = data[offset], data[offset + 1]
        listlen = int.from_bytes(data[offset + 2:offset + 4], "big")
        vector = offset + 4
        while kind == 4 and vector + 2 <= offset + 4 + listlen and data[vector:vector + 2] != b"\0\0":
            count = int.from_bytes(data[vector:vector + 2], "big") & 0x1FFF
            size = 2 + length + (count + 2) // 3
            if count == 1 and data[vector + 2:vector + 2 + length] == tp.DOMAIN:
                del data[vector:vector + size]
                data[offset + 2:offset + 4] = (listlen - size).to_bytes(2, "big")
                done = entry["ms"]
                break
            vector += size
        if done is not None:
            break
        offset += 4 + listlen
    if done is not None:
        entry["hex"] = bytes(data).hex()
        break
if done is None:
    raise SystemExit("no split MSRP LeaveAll frame carrying the Domain value after 20000 ms")
Path(sys.argv[3]).write_text(json.dumps(doc) + "\n")
cap = td.load(Path(sys.argv[3]))
print(f"planted: the split's MSRP LeaveAll frame at ms {done} carries the Domain type's LeaveAll, no Domain value")
grade = twin_mrp.grade(cap, "MSRP")
print(f"head grade: {len(grade.findings)} finding(s)")
for f in grade.findings:
    print("  ", f)
