#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""srptx_plants.py - planted copies of an srptx capture, each refused by srptx_grade.py's words (#867, #665).

Each plant changes a copy of one scenario's capture as the defect it names would have changed it, and
srptx_grade.py --plant must find WORDS[name] in a finding of the planted copy. The unplanted captures have
no finding (make srptx). Each WITHIN control moves a transmit opportunity to 1 ms inside a bound #867 item 3
allows, beside the plant 1 ms past it, and its copy must grade with no finding. srptx_mutants.py plants the
defects in the code itself.

  srptx_grade.py CAPTURE --make-plant NAME --out PLANTED
  srptx_grade.py PLANTED --plant NAME
  srptx_plants.py DIR      every plant and control against DIR/{wire,hold,licence}.json (make srptx-plants)
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import srptx_grade as g

#: #867 item 3's approved service allowance, T_svc 20 ms, held here apart from the grade's SVC_MS: each plant on
#: a bound sits 1 ms past what item 3 allows and its control 1 ms inside, so a grade bound off item 3's is refused
ITEM3_SVC_MS = 20
FOLLOW_MS = g.JOIN_MS + ITEM3_SVC_MS
JOIN_BOUNDS_MS = (g.JOIN_RANGE_MS[0] - ITEM3_SVC_MS, g.JOIN_RANGE_MS[1] + ITEM3_SVC_MS)
LEAVE_ALL_BOUNDS_MS = (g.LEAVE_ALL_MS - g.JOIN_MS - ITEM3_SVC_MS,
                       3 * g.LEAVE_ALL_MS // 2 + g.JOIN_MS + ITEM3_SVC_MS)
JOIN_WORDS = f"ms after the one before, outside JoinTime's range widened by T_svc ({JOIN_BOUNDS_MS[0]} to " \
             f"{JOIN_BOUNDS_MS[1]} ms"

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
                  f"followed at ms 230, past JoinTime + T_svc ({FOLLOW_MS} ms"),
    "join-late-past-t-svc": ("wire", f"the second MSRP frame and the adapter's record of it {FOLLOW_MS + 1} ms after "
                             "the first: 1 ms past JoinTime + T_svc",
                             f"followed at ms 222, past JoinTime + T_svc ({FOLLOW_MS} ms"),
    "join-early-past-t-svc": ("wire", "a short Join timer: the second and third MSRP frames, their records and the "
                              f"Join timer that sent each, earlier, the second {JOIN_BOUNDS_MS[0] - 1} ms after the "
                              "first: 1 ms short of JoinTime's range less T_svc",
                              f"a Join timer's transmit opportunity at ms 160, {JOIN_BOUNDS_MS[0] - 1:.3f} "
                              + JOIN_WORDS),
    "join-interval-late": ("wire", "a long Join timer: the second and third Join timer frames after the first MSRP "
                           f"LeaveAll, their records and timers, later, the second {JOIN_BOUNDS_MS[1] + 1} ms after "
                           "the one before: 1 ms past JoinTime's range plus T_svc, where no New is followed",
                           f"a Join timer's transmit opportunity at ms 15021, {JOIN_BOUNDS_MS[1] + 1:.3f} "
                           + JOIN_WORDS),
    "rate": ("wire", "the first MSRP frame sent again 1 and 2 ms after itself",
             "four transmit opportunities in"),
    "leave-all-missing": ("wire", "the first MSRP LeaveAll frame sent without its LeaveAll",
                          f"after the last LeaveAll (reset), outside {LEAVE_ALL_BOUNDS_MS[0]} to "
                          f"{LEAVE_ALL_BOUNDS_MS[1]} ms"),
    "bench-overrun": ("wire", "a modeled millisecond of 1,200 us of RTL time",
                      "[BENCH] a modeled millisecond took 1200.000 us of RTL time"),
    "timer-layout": ("wire", "the bench's report of a Join timer arm outside its participant's state",
                     "[BENCH] a Join timer arm outside its participant's state"),
    # [TX], item 4
    "dropped-under-backpressure": ("hold", "the first MRPDU the hold kept, dropped at the MAC",
                                   "never left the MAC"),
    "reordered": ("hold", "the first two MRPDUs the hold kept, swapped", "out of the order accepted"),
    "backpressure-unseen": ("hold", "the adapter's refusals gone", "never saw the SRP transmit ring full"),
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
#: name -> (the scenario it plants, what it changes): 1 ms inside the bound its plant passes, graded clean
WITHIN = {
    "join-late-within-t-svc": ("wire", f"the second MSRP frame and its record {FOLLOW_MS - 1} ms after the first"),
    "join-early-within-t-svc": ("wire", f"join-early-past-t-svc's move, the second frame {JOIN_BOUNDS_MS[0] + 1} ms "
                                "after the first"),
    "join-interval-late-within": ("wire", f"join-interval-late's move, the second frame {JOIN_BOUNDS_MS[1] - 1} ms "
                                  "after the one before"),
}
#: each timing plant and control: (the MSRP frame its move is measured from: the first, or the first after the
#: first LeaveAll frame; how many frames after it move; the ms the first of them then leaves after it; whether
#: the Join timer that sent each moves with it, as a timer of another length, or its egress alone, as a late one)
TIMING = {
    "join-late-past-t-svc": ("first", 1, FOLLOW_MS + 1, False),
    "join-late-within-t-svc": ("first", 1, FOLLOW_MS - 1, False),
    "join-early-past-t-svc": ("first", 2, JOIN_BOUNDS_MS[0] - 1, True),
    "join-early-within-t-svc": ("first", 2, JOIN_BOUNDS_MS[0] + 1, True),
    "join-interval-late": ("leave-all", 2, JOIN_BOUNDS_MS[1] + 1, True),
    "join-interval-late-within": ("leave-all", 2, JOIN_BOUNDS_MS[1] - 1, True),
}


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


def leave_all(entry: dict) -> bool:
    """Whether a MAC frame's MRPDU carries a LeaveAll."""
    return any(v.leave_all for m in parse(entry)[1] for v in m.vectors)


def move(doc: dict, entries: list[dict], shift: float, timer: bool) -> None:
    """Move MAC frames by shift us with the adapter's record of each (the grade pairs them by position), and with
    timer the Join timer's expiry and re-arm that sent each, as transmit opportunities that came then."""
    mrpdus = [m for m in doc["mac"] if m["hex"][24:28] in ("22ea", "88f5")]
    records = [r for r in doc["lib"] if r["rc"] == 0]
    moved = list(entries)
    for entry in entries:
        moved.append(records[next(k for k, m in enumerate(mrpdus) if m is entry)])
        if timer:
            joins = [t for t in doc["timers"] if t["proto"] == "MSRP" and t["kind"] == "join"]
            expiry = max((t for t in joins if t["event"] == "expire" and t["us"] <= entry["us"]), key=lambda t: t["us"])
            moved += [t for t in joins if expiry["us"] <= t["us"] <= entry["us"]]
    for item in moved:
        was = item["ms"]
        item["us"] += shift
        item["ms"] = int(item["us"] // 1000)
        if "last_ms" in item:
            item["last_ms"] += item["ms"] - was


def plant_timing(name: str, msrp: list[dict], doc: dict) -> None:
    """A TIMING plant or control: frames after an MSRP frame moved so the first leaves the ms named after it."""
    start, count, ms, timer = TIMING[name]
    k = 0 if start == "first" else next(j for j, m in enumerate(msrp) if leave_all(m)) + 1
    move(doc, msrp[k + 1:k + 1 + count], msrp[k]["us"] + ms * 1000.0 - msrp[k + 1]["us"], timer)


def first_queued(doc: dict) -> int:
    """The index in doc["mac"] of the first MRPDU that left at or after the hold's end."""
    end = doc["holds"][0][1]
    return next(k for k, m in enumerate(doc["mac"]) if m["ms"] >= end and m["hex"][24:28] in ("22ea", "88f5"))


def plant(name: str, doc: dict) -> None:
    """Change the capture as the defect named would have, in place."""
    scenario = (PLANTS.get(name) or WITHIN.get(name) or ("",))[0]
    if doc["scenario"] != scenario:
        raise SystemExit(f"srptx_plants: {name} plants the {scenario} capture, not the {doc['scenario']} one")
    msrp = frames(doc, "MSRP")
    first = msrp[0]
    header, messages = parse(first)
    if name in TIMING:
        plant_timing(name, msrp, doc)
    elif name == "malformed-endmark":
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
        msrp[1]["us"] += 30 * 1000.0
    elif name == "bench-overrun":
        doc["intra_ms_max_us"] = 1200.0
    elif name == "timer-layout":
        doc["layout_error"] = "a Join timer arm outside its participant's state: lwSRP's port layout changed"
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


def planted_findings(out: Path, docs: dict, name: str, scenario: str) -> list[str]:
    """The grade's findings on a copy of scenario's capture with name planted, written beside it."""
    doc = copy.deepcopy(docs[scenario])
    plant(name, doc)
    planted = out / f"{scenario}-{name}.json"
    planted.write_text(json.dumps(doc) + "\n")
    return g.grade(g.load(planted))[0]


def main() -> int:
    """Every plant against the unplanted captures in one directory: each must be refused by its words, which no
    finding of its unplanted capture holds; and every control must grade clean."""
    if len(sys.argv) != 2:
        print("usage: srptx_plants.py DIR", file=sys.stderr)
        return 2
    out = Path(sys.argv[1])
    docs = {name: json.loads((out / f"{name}.json").read_text()) for name in ("wire", "hold", "licence")}
    clean = {name: g.grade(g.load(out / f"{name}.json"))[0] for name in docs}
    escaped = 0
    for name, (scenario, what, words) in PLANTS.items():
        caught = [f for f in planted_findings(out, docs, name, scenario) if words in f]
        if caught and not any(words in f for f in clean[scenario]):
            print(f"ok   {name} ({what}): {caught[0]}")
        else:
            print(f"FAIL {name} ({what}): escaped; wanted {words!r}")
            escaped += 1
    refused = 0
    for name, (scenario, what) in WITHIN.items():
        found = planted_findings(out, docs, name, scenario)
        if found:
            print(f"FAIL {name} ({what}): inside the bound and refused: {found[0]}")
            refused += 1
        else:
            print(f"ok   {name} ({what}): no finding")
    print(f"srptx plants: {len(PLANTS) - escaped} of {len(PLANTS)} refused; {len(WITHIN) - refused} of {len(WITHIN)} "
          "controls inside their bound clean")
    return 1 if escaped or refused else 0


if __name__ == "__main__":
    sys.exit(main())
