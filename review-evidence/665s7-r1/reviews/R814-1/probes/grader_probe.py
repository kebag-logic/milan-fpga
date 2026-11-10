#!/usr/bin/env python3
"""grader_probe.py - reviewer probes of srptx_grade.py at the reviewed head.

  python3 -I grader_probe.py TREE CAPDIR OUTDIR

TREE    a checkout of the reviewed head (its tb/verilator/milan_dp is imported)
CAPDIR  the directory holding wire.json, hold.json and licence.json from `make srptx`

1. Ablation: every srptx_plants.py plant is graded section by section. For each plant it prints which
   sections raise a finding the unplanted capture does not, and whether the plant escapes once the
   section that owns its words is removed (no new finding left in any other section).
2. Extra malformations, beyond the plants, applied to real MSRP and MVRP frames of the wire capture; each
   must be refused by grade_wire (any new [WIRE] finding).
"""
import copy
import json
import sys
from pathlib import Path

TREE, CAPDIR, OUT = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(TREE / "tb/verilator/milan_dp"))
import srptx_grade as g  # noqa: E402
import srptx_plants as sp  # noqa: E402

OUT.mkdir(parents=True, exist_ok=True)


def sections(cap):
    """Findings per grader section."""
    out = {"BENCH": [], "WIRE": g.grade_wire(cap), "SA": g.grade_source(cap)[0], "TX": g.grade_tx(cap)[0],
           "TIME": g.grade_time(cap), "608/LIC": g.grade_licence(cap)[0]}
    if cap.doc["layout_error"]:
        out["BENCH"].append(f"[BENCH] {cap.doc['layout_error']}")
    if cap.doc["intra_ms_max_us"] >= g.MS_US:
        out["BENCH"].append(f"[BENCH] a modeled millisecond took {cap.doc['intra_ms_max_us']:.3f} us")
    return out


def load_doc(doc, name):
    path = OUT / f"probe-{name}.json"
    path.write_text(json.dumps(doc) + "\n")
    return g.load(path)


docs = {s: json.loads((CAPDIR / f"{s}.json").read_text()) for s in ("wire", "hold", "licence")}
clean = {s: sections(g.load(CAPDIR / f"{s}.json")) for s in docs}
for s, sec in clean.items():
    total = sum(len(v) for v in sec.values())
    print(f"control {s}: {total} finding(s)")

print("\n== 1. ablation of each plant")
rows = []
for name, (scen, what, words) in sp.PLANTS.items():
    doc = copy.deepcopy(docs[scen])
    sp.plant(name, doc)
    sec = sections(load_doc(doc, f"{scen}-{name}"))
    new = {k: [f for f in v if f not in clean[scen][k]] for k, v in sec.items()}
    owner = [k for k, v in new.items() if any(words in f for f in v)]
    others = {k: len(v) for k, v in new.items() if v and k not in owner}
    escapes = not others
    rows.append((name, owner, others, escapes))
    print(f"{name:28s} owner={','.join(owner) or 'NONE':8s} other-sections-with-new-findings={others or '{}'} "
          f"escapes-without-owner={'yes' if escapes else 'NO'}")

print("\n== 2. extra malformations against [WIRE]")
wire = docs["wire"]
frames = [m for m in wire["mac"] if m["hex"][24:28] in ("22ea", "88f5")]


def mrpdu_len(f):
    proto = "MSRP" if f[12:14] == b"\x22\xea" else "MVRP"
    return g.walk(proto, f[14:])[1]


msrp = next(bytes.fromhex(m["hex"]) for m in frames if m["hex"][24:28] == "22ea")
mvrp = next(bytes.fromhex(m["hex"]) for m in frames if m["hex"][24:28] == "88f5")
msrp_la = next(bytes.fromhex(m["hex"]) for m in frames if m["hex"][24:28] == "22ea"
               and any(v.leave_all for x in g.walk("MSRP", bytes.fromhex(m["hex"])[14:])[0] for v in x.vectors))
print(f"first MSRP frame {len(msrp)} bytes (MRPDU {mrpdu_len(msrp)}), first MVRP frame {len(mvrp)} bytes "
      f"(MRPDU {mrpdu_len(mvrp)})")


def edit(frame, fn):
    b = bytearray(frame)
    fn(b)
    return bytes(b)


L_MS, L_MV = mrpdu_len(msrp), mrpdu_len(mvrp)
cases = {
    "MSRP ProtocolVersion 1": edit(msrp, lambda b: b.__setitem__(14, 1)),
    "MVRP ProtocolVersion 1": edit(mvrp, lambda b: b.__setitem__(14, 1)),
    "MSRP PDU EndMark removed": msrp[:14 + L_MS - 2],
    "MVRP PDU EndMark removed": mvrp[:14 + L_MV - 2],
    "MVRP AttributeList EndMark removed": mvrp[:14 + L_MV - 4] + mvrp[14 + L_MV - 2:14 + L_MV],
    "MSRP first AttributeLength +1": edit(msrp, lambda b: b.__setitem__(16, b[16] + 1)),
    "MVRP AttributeLength 3": edit(mvrp, lambda b: b.__setitem__(16, 3)),
    "MSRP first AttributeListLength +2": edit(msrp, lambda b: b.__setitem__(18, b[18] + 2)),
    "MSRP first AttributeListLength -2": edit(msrp, lambda b: b.__setitem__(18, b[18] - 2)),
    "MSRP unknown AttributeType 5": edit(msrp, lambda b: b.__setitem__(15, 5)),
    "MSRP LeaveAllEvent 2": edit(msrp, lambda b: b.__setitem__(19, (b[19] & 0x1F) | 0x40)),
    "MVRP LeaveAllEvent 2": edit(mvrp, lambda b: b.__setitem__(17, (b[17] & 0x1F) | 0x40)),
    "MVRP ThreePacked 216": edit(mvrp, lambda b: b.__setitem__(14 + 3 + 2 + 2, 216)),
    "MSRP trailing nonzero byte": msrp[:14 + L_MS] + b"\x01",
    "MVRP trailing nonzero byte": mvrp[:14 + L_MV] + b"\x01",
    "MSRP to the MVRP group": bytes.fromhex("0180c2000021") + msrp[6:],
    "MVRP to the MSRP group": bytes.fromhex("0180c200000e") + mvrp[6:],
    "MSRP truncated after the first Message header": msrp[:14 + 1 + 4],
    "MSRP LeaveAll frame, type 2's LeaveAll vector dropped": None,
}
# build the dropped-type case from the first LeaveAll frame
hdr, msgs = msrp_la[:14], g.walk("MSRP", msrp_la[14:])[0]
cases["MSRP LeaveAll frame, type 2's LeaveAll vector dropped"] = bytes.fromhex(sp.encode(
    hdr, [(m.kind, [v.raw for v in m.vectors]) for m in msgs if m.kind != 2]))
cases["MSRP LeaveAll frame, NumberOfValues 0 LeaveAll vector only on 3 of 4 types"] = bytes.fromhex(sp.encode(
    hdr, [(m.kind, [v.raw for v in m.vectors if not (v.leave_all and m.kind == 1)] or
           [b"\x00\x01" + b"\x00" * 25 + b"\x00"]) for m in msgs]))
base_wire = g.grade_wire(g.load(CAPDIR / "wire.json"))
fails = 0
for name, frame in cases.items():
    doc = copy.deepcopy(wire)
    doc["mac"] = [dict(ms=1, us=1000.0, hex=frame.hex())]
    found = [f for f in g.grade_wire(load_doc(doc, "mal")) if f not in base_wire]
    if not found:
        fails += 1
    print(f"{'refused' if found else 'ESCAPED':8s} {name}: {found[0] if found else ''}")
print(f"extra malformations: {len(cases) - fails} of {len(cases)} refused")
