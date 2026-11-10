#!/usr/bin/env python3
"""Reviewer probes of srptx_grade.py: defects the author's plants do not cover, each planted into a copy of
an unplanted capture. Each probe names the section tag a finding must carry ("expect"), or None when the
probe is a boundary case the grade must accept.

  python3 -I probe_grader.py MILAN_DP_DIR CAPTURE_DIR OUT_DIR
"""
import copy
import json
import sys
from pathlib import Path

DP, CAPS, OUT = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(DP))
import srptx_grade as g  # noqa: E402
import srptx_plants as sp  # noqa: E402

OUT.mkdir(parents=True, exist_ok=True)
docs = {s: json.loads((CAPS / f"{s}.json").read_text()) for s in ("wire", "hold", "licence")}


def by_proto(doc, proto):
    kind = f"{g.APPLICATIONS[proto]['ethertype']:04x}"
    return [m for m in doc["mac"] if m["hex"][24:28] == kind]


def setb(entry, off, val):
    b = bytearray(bytes.fromhex(entry["hex"]))
    b[off] = val
    entry["hex"] = b.hex()


def pdu_end(entry, proto):
    b = bytes.fromhex(entry["hex"])
    _, n = g.walk(proto, b[14:])
    return 14 + n  # offset just past the PDU EndMark


def p_pdu_endmark(doc):
    f = by_proto(doc, "MSRP")[0]
    e = pdu_end(f, "MSRP")
    b = bytearray(bytes.fromhex(f["hex"]))
    b[e - 2:e] = b"\x01\x00"
    f["hex"] = b.hex()


def p_list_length(doc):
    f = by_proto(doc, "MSRP")[0]
    b = bytearray(bytes.fromhex(f["hex"]))
    n = int.from_bytes(b[17:19], "big") + 2
    b[17:19] = n.to_bytes(2, "big")
    f["hex"] = b.hex()


def p_version(doc):
    setb(by_proto(doc, "MSRP")[0], 14, 1)


def p_attr_len(doc):
    f = by_proto(doc, "MSRP")[0]
    setb(f, 16, bytes.fromhex(f["hex"])[16] + 1)


def p_mvrp_endmark(doc):
    f = by_proto(doc, "MVRP")[0]
    e = pdu_end(f, "MVRP")
    setb(f, e - 3, 1)  # the AttributeList EndMark's second octet (just before the PDU EndMark)


def p_mvrp_doubled_message(doc):
    f = by_proto(doc, "MVRP")[0]
    h, msgs = sp.parse(f)
    raw = sp.raw(msgs)
    raw.append(raw[0])
    f["hex"] = sp.encode(h, raw, "MVRP")


def p_mvrp_doubled_vid(doc):
    f = next(m for m in by_proto(doc, "MVRP") if any(v.events for x in sp.parse(m)[1] for v in x.vectors))
    h, msgs = sp.parse(f)
    raw = sp.raw(msgs)
    v = next(v for v in msgs[0].vectors if v.events)
    raw[0][1].append(b"\x00\x01" + v.first + bytes((v.raw[4] // 36 * 36,)))
    f["hex"] = sp.encode(h, raw, "MVRP")


def p_mvrp_oversized(doc):
    f = by_proto(doc, "MVRP")[0]
    h, msgs = sp.parse(f)
    raw = sp.raw(msgs)
    vid = 100
    while len(sp.encode(h, raw, "MVRP")) // 2 - 14 <= 1500:
        raw[0][1].append(b"\x00\x01" + vid.to_bytes(2, "big") + bytes((36 * 3,)))
        vid += 2
    f["hex"] = sp.encode(h, raw, "MVRP")


def p_mvrp_group(doc):
    f = by_proto(doc, "MVRP")[3]
    f["hex"] = g.APPLICATIONS["MSRP"]["group"] + f["hex"][12:]


def p_three_packed(doc):
    f = by_proto(doc, "MSRP")[0]
    b = bytes.fromhex(f["hex"])
    msgs, _ = g.walk("MSRP", b[14:])
    m = msgs[-1]
    v = m.vectors[0]
    at = b.find(v.raw, 14) + 2 + len(v.first)
    setb(f, at, 216)


def p_trailing(doc):
    f = by_proto(doc, "MSRP")[0]
    e = pdu_end(f, "MSRP")
    b = bytearray(bytes.fromhex(f["hex"]))
    if len(b) <= e:
        b += b"\0" * 4
    b[e] = 0x55
    f["hex"] = b.hex()


def p_leave_all_123(doc):
    target = next(m for m in by_proto(doc, "MSRP")
                  if any(v.leave_all for x in sp.parse(m)[1] for v in x.vectors))
    h, msgs = sp.parse(target)
    raw = [(m.kind, [v.raw for v in m.vectors if not (v.leave_all and m.kind == 4)]) for m in msgs]
    target["hex"] = sp.encode(h, [m for m in raw if m[1]])


def p_mvrp_leave_all_missing(doc):
    target = next(m for m in by_proto(doc, "MVRP")
                  if any(v.leave_all for x in sp.parse(m)[1] for v in x.vectors))
    h, msgs = sp.parse(target)
    raw = [(m.kind, [v.raw for v in m.vectors if not v.leave_all]) for m in msgs]
    target["hex"] = sp.encode(h, [m for m in raw if m[1]], "MVRP")


def p_truncated_vector(doc):
    f = by_proto(doc, "MSRP")[0]
    b = bytes.fromhex(f["hex"])
    msgs, _ = g.walk("MSRP", b[14:])
    m = msgs[-1]
    v = m.vectors[0]
    at = b.find(v.raw, 14)
    hdr = int.from_bytes(b[at:at + 2], "big") + 3  # three more values than encoded
    bb = bytearray(b)
    bb[at:at + 2] = hdr.to_bytes(2, "big")
    f["hex"] = bb.hex()


def p_sa_late_mvrp(doc):
    f = by_proto(doc, "MVRP")[-1]
    f["hex"] = f["hex"][:12] + "020000000002" + f["hex"][24:]


def p_tx_duplicate(doc):
    k = next(i for i, m in enumerate(doc["mac"]) if m["hex"][24:28] == "22ea" and m["ms"] > 5000)
    doc["mac"].insert(k + 1, dict(doc["mac"][k]))


def p_tx_drop_wire(doc):
    k = next(i for i, m in enumerate(doc["mac"]) if m["hex"][24:28] == "88f5" and m["ms"] > 100000)
    del doc["mac"][k]


def p_tx_late(doc):
    k = next(i for i, m in enumerate(doc["mac"]) if m["hex"][24:28] == "22ea" and m["ms"] > 5000)
    for m in doc["mac"][k:k + 1]:
        m["ms"] += 2
        m["us"] += 2000.0


def p_tx_corrupt(doc):
    m = next(m for m in doc["mac"] if m["hex"][24:28] == "22ea" and m["ms"] > 5000)
    b = bytearray(bytes.fromhex(m["hex"]))
    b[30] ^= 0x01  # inside a FirstValue, still well formed
    m["hex"] = b.hex()


def p_tx_far_reorder(doc):
    idx = [i for i, m in enumerate(doc["mac"]) if m["hex"][24:28] in ("22ea", "88f5") and m["ms"] > 5000]
    a, b = idx[0], idx[3]
    doc["mac"][a]["hex"], doc["mac"][b]["hex"] = doc["mac"][b]["hex"], doc["mac"][a]["hex"]


def shift_second_msrp(ms):
    def plant(doc):
        f = by_proto(doc, "MSRP")[1]
        f["ms"] += ms
        f["us"] += ms * 1000.0
    return plant


def p_rate_281(doc):
    f = by_proto(doc, "MSRP")
    a = f[10]
    k = doc["mac"].index(a)
    doc["mac"][k + 1:k + 1] = [dict(a, ms=a["ms"] + d, us=a["us"] + 1000.0 * d) for d in (93, 187, 280)]


def p_received_leave_all_before_sent(doc):
    sent = next(m for m in by_proto(doc, "MSRP")[5:]
                if any(v.leave_all for x in sp.parse(m)[1] for v in x.vectors))
    peer = next(a for a in docs["hold"]["applied"] if a["what"].startswith("MSRP LeaveAll, the peer"))
    doc["applied"].append({"ms": sent["ms"] - 1000, "what": "probe: a peer MSRP LeaveAll", "hex": peer["hex"]})
    doc["applied"].sort(key=lambda a: a["ms"])


PROBES = [
    ("wire", "PDU EndMark 0x0100", p_pdu_endmark, "[WIRE]"),
    ("wire", "MSRP AttributeListLength +2", p_list_length, "[WIRE]"),
    ("wire", "ProtocolVersion 1", p_version, "[WIRE]"),
    ("wire", "AttributeLength +1", p_attr_len, "[WIRE]"),
    ("wire", "MVRP AttributeList EndMark nonzero", p_mvrp_endmark, "[WIRE]"),
    ("wire", "MVRP Message twice", p_mvrp_doubled_message, "[WIRE]"),
    ("wire", "MVRP VID declared twice", p_mvrp_doubled_vid, "[WIRE]"),
    ("wire", "MVRP MRPDU past 1,500 octets", p_mvrp_oversized, "[WIRE]"),
    ("wire", "MVRP frame to the MSRP group", p_mvrp_group, "[WIRE]"),
    ("wire", "ThreePackedEvents 216", p_three_packed, "[WIRE]"),
    ("wire", "nonzero byte after the PDU EndMark", p_trailing, "[WIRE]"),
    ("wire", "MSRP LeaveAll on types 1-3 only", p_leave_all_123, "[WIRE]"),
    ("wire", "NumberOfValues past the vector", p_truncated_vector, "[WIRE]"),
    ("wire", "MVRP LeaveAll frame without its LeaveAll", p_mvrp_leave_all_missing, "[TIME]"),
    ("wire", "last MVRP frame from another MAC", p_sa_late_mvrp, "[SA]"),
    ("wire", "an MSRP frame sent twice", p_tx_duplicate, "[TX]"),
    ("wire", "an MVRP frame lost outside a hold", p_tx_drop_wire, "[TX]"),
    ("wire", "an MSRP frame 2 ms after its acceptance", p_tx_late, "[TX]"),
    ("wire", "one FirstValue bit flipped on the wire", p_tx_corrupt, "[TX]"),
    ("wire", "two frames three apart swapped", p_tx_far_reorder, "[TX]"),
    ("wire", "second MSRP frame +19 ms (218.0 ms after the New's egress, at the bound)", shift_second_msrp(19), None),
    ("wire", "second MSRP frame +19.2 ms (218.2 ms after the New's egress)", shift_second_msrp(19.2), "[TIME]"),
    ("wire", "four MSRP opportunities in 280 ms", p_rate_281, "[TIME]"),
    ("wire", "a peer LeaveAll 1 s before a sent one", p_received_leave_all_before_sent, "[TIME]"),
]


def main():
    clean = {s: g.grade(g.load(CAPS / f"{s}.json"))[0] for s in docs}
    for s, f in clean.items():
        print(f"control {s}: {len(f)} finding(s)")
    bad = 0
    rows = []
    for n, (scenario, name, fn, expect) in enumerate(PROBES):
        doc = copy.deepcopy(docs[scenario])
        fn(doc)
        path = OUT / f"probe-{n:02d}.json"
        path.write_text(json.dumps(doc) + "\n")
        found = g.grade(g.load(path))[0]
        new = [x for x in found if x not in clean[scenario]]
        if expect is None:
            # a boundary probe of [TIME]: the shift also leaves its frame outside [TX]'s one-millisecond
            # acceptance window, which is [TX]'s own (correct) finding, so only [TIME] is read
            ok = not any(x.startswith("[TIME]") for x in new)
        else:
            ok = any(x.startswith(expect) for x in new)
        shown = [x for x in new if x.startswith(expect or "[TIME]")] or new
        bad += not ok
        rows.append((ok, name, expect, new[:2]))
        print(f"{'ok  ' if ok else 'FAIL'} {name}: expect {expect or 'accepted'}; {len(new)} new finding(s)"
              + (f": {shown[0][:200]}" if shown else ""))
    print(f"probes: {len(PROBES) - bad} of {len(PROBES)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
