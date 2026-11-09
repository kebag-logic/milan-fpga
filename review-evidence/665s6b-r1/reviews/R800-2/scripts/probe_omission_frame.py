#!/usr/bin/env python3
"""probe_omission_frame.py LEG_DIR UNPLANTED_SPLIT_JSON PLANTED_SPLIT_JSON

The leave-all-omission plant's one changed frame, decoded before and after: exactly one frame differs; the
difference is one 7-octet Domain VectorAttribute (VectorHeader with NumberOfValues 1 and no LeaveAll, the 4-octet
value, one ThreePackedEvents octet) and the enclosing Message's AttributeListLength reduced by 7; both frames
decode as well-formed MSRPDUs; the planted one keeps its Domain-type LeaveAll and carries no Domain event; and no
other split MSRP frame of that millisecond carries the Domain (so the omission is not a split MRPDU)."""
import json
import sys
from pathlib import Path

LEG = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(LEG))
import twin_decode as td  # noqa: E402
import twin_plants as tp  # noqa: E402

a, b = (json.loads(Path(p).read_text()) for p in sys.argv[2:4])
fails = 0


def check(ok, what):
    global fails
    fails += not ok
    print(f"[{'ok' if ok else 'FAIL'}] {what}")


diff = [i for i, (x, y) in enumerate(zip(a["frames"], b["frames"])) if x != y]
check(len(a["frames"]) == len(b["frames"]) and len(diff) == 1, f"one frame differs (index {diff})")
i = diff[0]
old, new = a["frames"][i], b["frames"][i]
check(old["ms"] == new["ms"] == 27910, f"the changed frame is at ms {new['ms']}")
fo, fn = tp.frame_fields(old), tp.frame_fields(new)
eo, lo = td.msrp_frame(fo[1])
en, ln = td.msrp_frame(fn[1])
print(f"  before: {len(bytes.fromhex(old['hex']))} octets, LeaveAll types {sorted(lo)}, events "
      f"{[(e.kind, e.value, e.event) for e in eo]}")
print(f"  after:  {len(bytes.fromhex(new['hex']))} octets, LeaveAll types {sorted(ln)}, events "
      f"{[(e.kind, e.value, e.event) for e in en]}")
dom = [(e.kind, e.value) for e in eo if e.kind == 4]
check(len(dom) == 1, f"the unplanted frame carries one Domain event {dom}")
check(not [e for e in en if e.kind == 4], "the planted frame carries no Domain event")
check(4 in lo and 4 in ln, "both frames carry the Domain type's LeaveAll")
check([(e.kind, e.value, e.event) for e in eo if e.kind != 4] == [(e.kind, e.value, e.event) for e in en],
      "every other attribute event is unchanged")
ob, nb = bytes.fromhex(old["hex"]), bytes.fromhex(new["hex"])
check(len(ob) - len(nb) == 7, f"the planted frame is {len(ob) - len(nb)} octets shorter")
# the expected planted frame, built independently: the Domain Message (AttributeType 4, AttributeLength 4) found
# by walking the MSRPDU's Messages, its NumberOfValues-1 VectorAttribute without LeaveAll removed, and its
# AttributeListLength reduced by the 7 octets removed
at = fo[1].at + 1
expect = None
while at + 4 <= len(ob) and ob[at:at + 2] != b"\0\0":
    length = int.from_bytes(ob[at + 2:at + 4], "big")
    if ob[at] == 4:
        vec = ob[at + 4:at + 4 + length]
        run = bytes.fromhex("0001") + tp.DOMAIN
        v = vec.find(run)
        check(v >= 0 and vec[v + 6] < 0xd8, f"the Domain Message at octet {at} holds the vector {vec[v:v + 7].hex()}")
        body = vec[:v] + vec[v + 7:]
        expect = ob[:at + 2] + (length - 7).to_bytes(2, "big") + body + ob[at + 4 + length:]
        print(f"  Domain Message at octet {at}: list {vec.hex()} -> {body.hex()} (AttributeListLength {length} -> {length - 7})")
    at += 4 + length
check(expect == nb, "the planted frame equals the unplanted one with exactly that vector removed and the length fixed")
others = [f for f in b["frames"] if f["ms"] == 27910 and f is not new and (ff := tp.frame_fields(f)) and ff[0] == "MSRP"
          and [e for e in td.msrp_frame(ff[1])[0] if e.kind == 4]]
check(not others, "no other split MSRP frame of ms 27910 carries the Domain")
print("PASS" if not fails else "FAIL")
sys.exit(1 if fails else 0)
