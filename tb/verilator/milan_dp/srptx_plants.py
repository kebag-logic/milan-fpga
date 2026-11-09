#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""srptx_plants.py - planted copies of an srptx capture, each refused by srptx_grade.py's words (#867, #665).

Each plant changes a copy of one scenario's capture as the defect it names would have changed it, and
srptx_grade.py --plant must find WORDS[name] in a finding of the planted copy. The unplanted captures have
no finding (make srptx). srptx_mutants.py plants the defects in the code itself.

  srptx_grade.py CAPTURE --make-plant NAME --out PLANTED
  srptx_grade.py PLANTED --plant NAME
  srptx_plants.py DIR      every plant against DIR/{wire,hold,licence}.json (make srptx-plants)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import srptx_grade as g

#: name -> (the scenario it plants, what it changes, the words it must be refused by)
PLANTS = {
    # [WIRE], #867 item 1
    "malformed-endmark": ("wire", "the first MSRP frame's first AttributeList EndMark 0x0001",
                          "MSRP AttributeList EndMark missing where its AttributeListLength ends"),
    "doubled-declaration": ("wire", "the first MSRP frame's Domain vector twice in its Message",
                            "MSRP Domain value 06030002 declared 2 times in one MRPDU"),
    "doubled-message": ("wire", "the first MSRP frame's Domain Message twice",
                        "2 Messages of AttributeType 4, not one per AttributeType"),
    "leave-all-wrong-type": ("wire", "the first MSRP LeaveAll frame's LeaveAll on the Domain alone",
                             "a LeaveAll on AttributeTypes [4], not on every MSRP AttributeType [1, 2, 3, 4]"),
    "oversized": ("wire", "the first MSRP frame's Domain Message grown past 1,500 octets with distinct values",
                  "past 1500 octets and the 1500-byte frame"),
    # [SA], item 2
    "zero-source": ("wire", "the first MRPDU after reset from 00-00-00-00-00-00 (#839)",
                    "[SA] MSRP frame at ms 1 from 000000000000, not the port's MAC"),
    # [TIME], item 3
    "join-late": ("wire", "the second MSRP frame 30 ms later, the Domain's second New",
                  "followed at ms 230, past JoinTime + T_svc (220 ms"),
    "rate": ("wire", "the first MSRP frame sent again 1 and 2 ms after itself",
             "four transmit opportunities in"),
    "leave-all-missing": ("wire", "the first MSRP LeaveAll frame sent without its LeaveAll",
                          "after the last LeaveAll (reset), outside 9780 to 15220 ms"),
    # [TX], item 4
    "dropped-under-backpressure": ("hold", "the first MRPDU the hold kept, dropped at the MAC",
                                   "never left the MAC"),
    "reordered": ("hold", "the first two MRPDUs the hold kept, swapped", "out of the order accepted"),
    "backpressure-unseen": ("hold", "the adapter's refusals gone", "never saw the SRP TX ring full"),
    "refused-with-room": ("hold", "the refusal with 100 words in use", "the ring had room"),
    "retention-lost": ("hold", "the refused MSRP MRPDU one byte off what was sent next",
                       "was not the next MSRP MRPDU the adapter sent"),
    # [608], item 5
    "late-stop": ("licence", "the stop at the withdrawal's LeaveTime, as if it restarted the timer",
                  "[608] the talker stopped at ms 23000.012, not at the LeaveTime deadline"),
    "never-stopped": ("licence", "the licence never cleared", "[608] the talker never stopped"),
    "stream-after-stop": ("licence", "a stream frame 10 ms after the gate closed",
                          "stream frame(s) after the stream gate closed"),
    # [LIC], item 6
    "gate-not-licence": ("licence", "the stream gate closed for a millisecond while the licence holds",
                         "the policer reads active 0x1, admitted 0x1, gate 0x0, and the firmware's LICENCE is 0x1"),
    "aaf-without-licence": ("licence", "the AAF gate open at the first sample", "AAF talker's gate is open without"),
    "stream-without-licence": ("licence", "a stream frame at ms 100", "while no source holds its licence"),
}
WORDS = {name: words for name, (_, _, words) in PLANTS.items()}


def frames(doc: dict, proto: str) -> list[dict]:
    """The MAC frames of one application, in the order sent."""
    kind = f"{g.APPLICATIONS[proto]['ethertype']:04x}"
    return [m for m in doc["mac"] if m["hex"][24:28] == kind]


def parse(entry: dict) -> tuple[bytes, list[g.Message]]:
    """A MAC frame's Ethernet header and Messages."""
    frame = bytes.fromhex(entry["hex"])
    proto = "MSRP" if frame[12:14] == b"\x22\xea" else "MVRP"
    messages, length = g.walk(proto, frame[14:])
    return frame[:14], messages


def encode(header: bytes, messages: list[tuple[int, list[bytes]]], proto: str = "MSRP") -> str:
    """An MRPDU from raw vectors (10.8.1.2), the MSRP AttributeListLength computed (35.2.2.x)."""
    pdu = bytearray(b"\0")
    for kind, vectors in messages:
        body = b"".join(vectors) + b"\0\0"
        pdu += bytes((kind, g.APPLICATIONS[proto]["types"][kind]))
        if g.APPLICATIONS[proto]["list_length"]:
            pdu += len(body).to_bytes(2, "big")
        pdu += body
    return (header + bytes(pdu) + b"\0\0").hex()


def raw(messages: list[g.Message]) -> list[tuple[int, list[bytes]]]:
    """Each Message as its AttributeType and its vectors' bytes."""
    return [(m.kind, [v.raw for v in m.vectors]) for m in messages]


def first_queued(doc: dict) -> int:
    """The index in doc["mac"] of the first MRPDU that left at or after the hold's end."""
    end = doc["holds"][0][1]
    return next(k for k, m in enumerate(doc["mac"]) if m["ms"] >= end and m["hex"][24:28] in ("22ea", "88f5"))


def plant(name: str, doc: dict) -> None:
    """Change the capture as the defect named would have, in place."""
    scenario = PLANTS[name][0]
    if doc["scenario"] != scenario:
        raise SystemExit(f"srptx_plants: {name} plants the {scenario} capture, not the {doc['scenario']} one")
    msrp = frames(doc, "MSRP")
    first = msrp[0]
    header, messages = parse(first)
    if name == "malformed-endmark":
        data = bytearray(bytes.fromhex(first["hex"]))
        end = 14 + 5 + int.from_bytes(data[17:19], "big")
        data[end - 1] = 1
        first["hex"] = data.hex()
    elif name in ("doubled-declaration", "doubled-message", "oversized"):
        msgs = raw(messages)
        domain = next(m for m in msgs if m[0] == 4)
        if name == "doubled-declaration":
            domain[1].append(domain[1][0])
        elif name == "doubled-message":
            msgs.append((4, list(domain[1])))
        else:
            value = 0x06030010
            while len(encode(header, msgs)) // 2 - 14 <= g.MRPDU_MAX:
                domain[1].append(b"\x00\x01" + value.to_bytes(4, "big") + bytes((3 * 36,)))
                value += 2
        first["hex"] = encode(header, msgs)
    elif name in ("leave-all-wrong-type", "leave-all-missing"):
        target = next(m for m in msrp if parse(m)[1] and any(v.leave_all for x in parse(m)[1] for v in x.vectors))
        header, messages = parse(target)
        keep = (4,) if name == "leave-all-wrong-type" else ()
        msgs = [(m.kind, [v.raw for v in m.vectors if not v.leave_all or m.kind in keep]) for m in messages]
        target["hex"] = encode(header, [m for m in msgs if m[1]])
    elif name == "zero-source":
        first["hex"] = first["hex"][:12] + "0" * 12 + first["hex"][24:]
    elif name == "join-late":
        msrp[1]["ms"] += 30
        msrp[1]["us"] += 30000.0
    elif name == "rate":
        at = doc["mac"].index(first)
        doc["mac"][at + 1:at + 1] = [dict(first, ms=first["ms"] + k, us=first["us"] + 1000.0 * k) for k in (1, 2)]
    elif name == "dropped-under-backpressure":
        del doc["mac"][first_queued(doc)]
    elif name == "reordered":
        k = first_queued(doc)
        later = next(j for j in range(k + 1, len(doc["mac"])) if doc["mac"][j]["hex"][24:28] in ("22ea", "88f5"))
        doc["mac"][k]["hex"], doc["mac"][later]["hex"] = doc["mac"][later]["hex"], doc["mac"][k]["hex"]
    elif name == "backpressure-unseen":
        doc["lib"] = [entry for entry in doc["lib"] if entry["rc"] == 0]
    elif name == "refused-with-room":
        next(entry for entry in doc["lib"] if entry["rc"] != 0)["ring_used"] = 100
    elif name == "retention-lost":
        refused = next(entry for entry in doc["lib"] if entry["rc"] != 0)
        refused["hex"] = refused["hex"][:-6] + f"{int(refused['hex'][-6:-4], 16) ^ 1:02x}" + refused["hex"][-4:]
    elif name in ("late-stop", "never-stopped"):
        withdraw = g.applied_ms(g.Capture(None, doc, []), "MSRP Listener Ready Lv")
        cleared = next(w for w in doc["licence_writes"] if not w[1] & 1 and w[0] > withdraw * 1000)
        closed = next(p for p in doc["policer"] if p["ms"] > withdraw and not p["gate"] & 1)
        if name == "never-stopped":
            doc["licence_writes"].remove(cleared)
            doc["policer"] = [p for p in doc["policer"] if p["ms"] < closed["ms"]]
        else:
            shift = (withdraw + g.LEAVE_MS) - closed["ms"]
            cleared[0] += shift * 1000.0
            for p in doc["policer"]:
                if p["ms"] >= closed["ms"]:
                    p["ms"] += shift
    elif name == "stream-after-stop":
        closed = max(p["ms"] for p in doc["policer"] if not p["gate"] & 1)
        doc["stream"].append([closed + 10, doc["stream"][0][1], 1])
    elif name == "gate-not-licence":
        on = next(k for k, p in enumerate(doc["policer"]) if p["gate"] & 1 and p["aaf"])
        doc["policer"].insert(on + 1, dict(doc["policer"][on], ms=doc["policer"][on]["ms"] + 1, gate=0, aaf=0))
        doc["policer"].insert(on + 2, dict(doc["policer"][on], ms=doc["policer"][on]["ms"] + 2))
    elif name == "aaf-without-licence":
        doc["policer"][0]["aaf"] = 1
    elif name == "stream-without-licence":
        doc["stream"].insert(0, [100, doc["stream"][0][1], 1])
    else:
        raise SystemExit(f"srptx_plants: no plant named {name}")


def main() -> int:
    """Every plant against the unplanted captures in one directory: each must be refused by its words, which no
    finding of its unplanted capture holds."""
    if len(sys.argv) != 2:
        print("usage: srptx_plants.py DIR", file=sys.stderr)
        return 2
    out = Path(sys.argv[1])
    docs = {name: json.loads((out / f"{name}.json").read_text()) for name in ("wire", "hold", "licence")}
    clean = {name: g.grade(g.load(out / f"{name}.json"))[0] for name in docs}
    escaped = 0
    for name, (scenario, what, words) in PLANTS.items():
        doc = copy.deepcopy(docs[scenario])
        plant(name, doc)
        planted = out / f"{scenario}-{name}.json"
        planted.write_text(json.dumps(doc) + "\n")
        found = g.grade(g.load(planted))[0]
        caught = [f for f in found if words in f]
        if caught and not any(words in f for f in clean[scenario]):
            print(f"ok   {name} ({what}): {caught[0]}")
        else:
            print(f"FAIL {name} ({what}): escaped; wanted {words!r}")
            escaped += 1
    print(f"srptx plants: {len(PLANTS) - escaped} of {len(PLANTS)} refused")
    return 1 if escaped else 0


if __name__ == "__main__":
    sys.exit(main())
