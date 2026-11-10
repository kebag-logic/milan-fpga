#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""srptx_grade.py - the split build's SRP transmit path, graded at the wire (#867, #665).

Reads what twin_split.cpp --srptx records (srptx.hpp) and grades it:

  [WIRE]  every MSRP and MVRP frame the MAC sent is a well-formed MRPDU (IEEE 802.1Q-2018 10.8.1, 10.8.2):
          ProtocolVersion, AttributeType and AttributeLength, AttributeListLength (MSRP, 35.2.2.x), each
          vector, each AttributeList EndMark and the PDU EndMark, at most 1,500 octets and the frame at most
          1,500 bytes (#665, the decoded SRP comparison's rule); one Message per AttributeType (lwSRP PR #18;
          10.8.1.2); no attribute value twice in one MRPDU; a LeaveAll on every AttributeType of its
          application (10.7.9: one LeaveAll state machine a participant; 10.8.2.6: a LeaveAllEvent applies
          to its Message's AttributeType); the group address and EtherType of its application (MSRP
          35.2.2.1/.2, MVRP 11.2.3.1.3 and Table 10-1).
  [SA]    every MRPDU's source address is the port's MAC from the first frame after reset (#839; IEEE
          802.1AC-2016 11.1).
  [TIME]  each participant's transmit opportunities at egress (IEEE 802.1Q-2018 10.7.4, Table 10-7, Milan
          v1.2 Table 4.3's values), each bound widened by the approved service allowance T_svc = 20 ms
          (#867 item 3; #665, the owner's ruling of 2026-11-06): no four in 1.5 x JoinTime; after a New, or
          a declaration's first message, the attribute's next message within JoinTime; each LeaveAll within
          LeaveAllTime to 1.5 x LeaveAllTime (10.7.4.3) of the last, or of a received one (rLA!, Table
          10-5), the transmit opportunity's wait (JoinTime) added, and none missing at the run's end.
  [TX]    every MRPDU the adapter accepted from lwSRP left the MAC, byte for byte, in the order accepted,
          and nothing else did; with the MAC held, the adapter saw the SRP transmit ring full, and the MRPDU it
          refused was the next one it sent.
  [608]   the licence scenario: a peer's withdrawal after its LeaveAll stops the talker at the LeaveTime
          deadline that LeaveAll started, not one the withdrawal restarted (#608; Table 10-4: LV/rLv! is no
          transition; Milan v1.2 4.2.7.2.2 changes only IN/rLv!), and the stream frames stop with it.
  [LIC]   the licence scenario: at every millisecond the policer's stream gate holds exactly the LICENCE
          the firmware last wrote, the AAF talker's gate opens only under source 0's, and no stream frame
          leaves while no source holds one (#867 item 6).

The licence scenario runs the srptx.hpp fixture (source 0 allocated at SRP creation), and every finding of
that scenario names it.

Measurements: the egress interval error per MRP timer (JoinTime, periodic, LeaveAll; and LeaveTime in the
licence scenario), in us, min/mean/max over N: each egress interval less the interval its timer was armed
with, and each frame's egress after its timer's expiry; and the frames per transmit opportunity.

  srptx_grade.py CAPTURE [--report OUT.json]          grade; exit 1 on any finding
  srptx_grade.py CAPTURE --make-plant NAME --out OUT   write a planted copy (srptx_plants.py)
  srptx_grade.py CAPTURE --plant NAME                  the planted capture must be refused by NAME's words,
                                                       or for a control (srptx_plants.WITHIN) graded clean
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "sw/firmware/ctrl/test"))
import srp_wire_compare as swc  # noqa: E402

#: the approved service allowance, T_svc = 20 ms, which widens every [TIME] bound and the [608] window (#867
#: item 3; #665: the owner's ruling of 2026-11-06 sets the SRP/MRP bound to T_svc, no longer min(T_svc, 10 % of the
#: shortest JoinTime) = 18 ms)
SVC_MS = 20
#: IEEE 802.1Q-2018 Table 10-7 as Milan v1.2 Table 4.3 sets it, and the adapter configures it (srp_mbx.c)
JOIN_MS = 200
LEAVE_MS = 5000
LEAVE_ALL_MS = 10000
PERIODIC_MS = 1000
#: lwSRP's timer resolution, one centisecond (docs/reference/FR_NFR.md 3.4.1)
RESOLUTION_MS = 10
RATE_WINDOW_MS = 3 * JOIN_MS // 2 - SVC_MS
JOIN_FOLLOW_MS = JOIN_MS + SVC_MS
LEAVE_ALL_BOUNDS_MS = (LEAVE_ALL_MS - JOIN_MS - SVC_MS, 3 * LEAVE_ALL_MS // 2 + JOIN_MS + SVC_MS)
#: a modeled millisecond's RTL time, which the time base assumes is under one millisecond (srptx.hpp)
MS_US = 1000.0
MRPDU_MAX = 1500
FRAME_MAX = 1500
APPLICATIONS = {
    "MSRP": {"ethertype": 0x22EA, "group": "0180c200000e", "types": {1: 25, 2: 34, 3: 8, 4: 4},
             "list_length": True, "four_packed": {3}},
    "MVRP": {"ethertype": 0x88F5, "group": "0180c2000021", "types": {1: 2}, "list_length": False,
             "four_packed": set()},
}
MSRP_NAMES = {1: "Talker Advertise", 2: "Talker Failed", 3: "Listener", 4: "Domain"}
EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")
DECLARING = {"New", "JoinIn", "JoinMt"}
#: how long after a timer's expiry its frame may leave and still be that timer's (the measurement only)
ATTRIBUTE_MS = 100
FIXTURE = " (the licence scenario's fixture: source 0 allocated at SRP creation)"


class Malformed(ValueError):
    """An MRPDU that 10.8 does not allow, named."""


def need(condition: bool, reason: str) -> None:
    """Refuse the MRPDU with the reason named."""
    if not condition:
        raise Malformed(reason)


@dataclass
class Vector:
    leave_all: bool
    first: bytes
    events: list[str]
    raw: bytes


@dataclass
class Message:
    kind: int
    vectors: list[Vector]


@dataclass
class Mrpdu:
    proto: str
    ms: int
    us: float
    frame: bytes
    messages: list[Message] = field(default_factory=list)
    error: str = ""
    accepted_ms: int | None = None   # when the adapter accepted it from lwSRP, matched in order

    def values(self) -> list[tuple[int, str, str]]:
        """Every (AttributeType, value, event) the MRPDU carries, FirstValue + k expanded (10.8.2.8)."""
        found = []
        fields = swc.MSRP if self.proto == "MSRP" else {1: swc.Attribute(2, False, ((0, 2),))}
        for m in self.messages:
            for v in m.vectors:
                for k, e in enumerate(v.events):
                    found.append((m.kind, swc.increment(v.first, k, fields[m.kind].increment_fields).hex(), e))
        return found

    def leave_all_types(self) -> set[int]:
        """The AttributeTypes whose Message carries a LeaveAll vector."""
        return {m.kind for m in self.messages if any(v.leave_all for v in m.vectors)}


def walk(proto: str, pdu: bytes) -> tuple[list[Message], int]:
    """The Messages of one MRPDU and its length to the PDU EndMark (IEEE 802.1Q-2018 10.8.1.2: ProtocolVersion,
    Messages, EndMark; a Message is AttributeType, AttributeLength, the MSRP AttributeListLength, then
    vectors to the AttributeList EndMark; a vector is its header, FirstValue, ThreePackedEvents and, for the
    MSRP Listener, FourPackedEvents). Every rule is checked here, apart from the application's tables."""
    app = APPLICATIONS[proto]
    need(len(pdu) >= 3 and pdu[0] == 0, f"{proto} ProtocolVersion or a truncated MRPDU")
    off, messages = 1, []
    while True:
        need(off + 2 <= len(pdu), f"{proto} missing PDU EndMark")
        if pdu[off:off + 2] == b"\0\0":
            off += 2
            break
        kind, length = pdu[off], pdu[off + 1]
        need(kind in app["types"], f"{proto} unknown AttributeType {kind}")
        need(length == app["types"][kind], f"{proto} AttributeType {kind}'s AttributeLength {length}")
        off += 2
        end = len(pdu)
        if app["list_length"]:
            need(off + 2 <= len(pdu), f"{proto} truncated Message header")
            end = off + 2 + int.from_bytes(pdu[off:off + 2], "big")
            off += 2
            need(end <= len(pdu) - 2, f"{proto} AttributeListLength past the MRPDU")
            need(pdu[end - 2:end] == b"\0\0",
                 f"{proto} AttributeList EndMark missing where its AttributeListLength ends")
        vectors = []
        while True:
            need(off + 2 <= end, f"{proto} missing AttributeList EndMark")
            header = int.from_bytes(pdu[off:off + 2], "big")
            off += 2
            if header == 0:
                need(not app["list_length"] or off == end,
                     f"{proto} AttributeList EndMark before its AttributeListLength")
                break
            flag, count = divmod(header, 8192)
            need(flag in (0, 1), f"{proto} reserved LeaveAllEvent")
            need(flag == 1 or count > 0, f"{proto} empty vector without a LeaveAll")
            three = (count + 2) // 3
            four = (count + 3) // 4 if kind in app["four_packed"] else 0
            stop = off + length + three + four
            need(stop <= end - 2, f"{proto} truncated vector")
            packed = pdu[off + length:off + length + three]
            need(all(p < 216 for p in packed), f"{proto} reserved ThreePackedEvents")
            unpacked = [x for p in packed for x in (p // 36, (p // 6) % 6, p % 6)]
            need(not any(unpacked[count:]), f"{proto} nonzero ThreePacked padding")
            vectors.append(Vector(bool(flag), bytes(pdu[off:off + length]), [EVENTS[e] for e in unpacked[:count]],
                                  bytes(pdu[off - 2:stop])))
            off = stop
        need(vectors, f"{proto} empty AttributeList")
        messages.append(Message(kind, vectors))
    need(messages, f"{proto} empty MRPDU")
    need(not any(pdu[off:]), f"{proto} nonzero bytes after the PDU EndMark")
    return messages, off


@dataclass
class Capture:
    path: Path
    doc: dict
    mrpdus: list[Mrpdu]

    @property
    def scenario(self) -> str:
        """The scenario the capture ran."""
        return self.doc["scenario"]

    def received(self, proto: str) -> list[tuple[int, bool]]:
        """The peer's MRPDUs of one application as applied: (ms, carried a LeaveAll)."""
        found = []
        for a in self.doc["applied"]:
            data = bytes.fromhex(a["hex"])
            if data[12:14].hex() == f"{APPLICATIONS[proto]['ethertype']:04x}":
                try:
                    messages, _ = walk(proto, data[14:])
                except Malformed:
                    continue
                found.append((a["ms"], any(v.leave_all for m in messages for v in m.vectors)))
        return found

    def held(self, a: float, b: float) -> bool:
        """Whether the span from a to b ms touches a window the MAC refused every beat in."""
        return any(a < h[1] and b >= h[0] for h in self.doc["holds"])

    def queued(self, f: Mrpdu) -> bool:
        """Whether the frame waited behind a hold: from its acceptance to its egress the MAC was held."""
        return self.held(f.ms if f.accepted_ms is None else f.accepted_ms, f.ms)


def load(path: Path) -> Capture:
    """Read a capture, each MRPDU walked and matched in order to the MRPDU the adapter accepted."""
    doc = json.loads(path.read_text())
    mrpdus = []
    for m in doc["mac"]:
        frame = bytes.fromhex(m["hex"])
        kind = frame[12:14].hex()
        proto = next((p for p, a in APPLICATIONS.items() if kind == f"{a['ethertype']:04x}"), None)
        if proto is None:
            continue
        mrpdu = Mrpdu(proto, m["ms"], m["us"], frame)
        try:
            mrpdu.messages, _ = walk(proto, frame[14:])
        except Malformed as error:
            mrpdu.error = str(error)
        mrpdus.append(mrpdu)
    accepted = [entry for entry in doc["lib"] if entry["rc"] == 0]
    for f, a in zip(mrpdus, accepted):
        if f.frame[14:14 + len(a["hex"]) // 2].hex() == a["hex"]:
            f.accepted_ms = a["ms"]
    return Capture(path, doc, mrpdus)


def label(proto: str, kind: int, value: str) -> str:
    """An attribute as a finding names it: its application, type and stream_id or value."""
    if proto == "MVRP":
        return f"MVRP VID {value}"
    return f"MSRP {MSRP_NAMES[kind]} {'stream_id ' + value[:16] if kind in (1, 2, 3) else 'value ' + value}"


# ---- [WIRE] and [SA] --------------------------------------------------------------

def grade_wire(cap: Capture) -> list[str]:
    """Each MRPDU's 10.8.1/10.8.2 form, its size, its group address, one Message per AttributeType, no value
    twice and its LeaveAll on every AttributeType of its application."""
    found = []
    for f in cap.mrpdus:
        where = f"[WIRE] {f.proto} frame at ms {f.ms}"
        if f.error:
            found.append(f"{where}: {f.error}")
            continue
        app = APPLICATIONS[f.proto]
        _, length = walk(f.proto, f.frame[14:])
        if length > MRPDU_MAX or 14 + length > FRAME_MAX:
            found.append(f"{where}: an MRPDU of {length} octets in a frame of {14 + length} bytes, past "
                         f"{MRPDU_MAX} octets and the {FRAME_MAX}-byte frame")
        if f.frame[:6].hex() != app["group"]:
            found.append(f"{where}: sent to {f.frame[:6].hex()}, not the {f.proto} group address {app['group']}")
        if f.proto == "MSRP":
            try:
                swc.decode_frame(f.frame[:14 + length])
            except swc.Malformed as error:
                found.append(f"{where}: the clause 10.8 decoder refuses it: {error}")
        kinds = [m.kind for m in f.messages]
        for kind in sorted({k for k in kinds if kinds.count(k) > 1}):
            found.append(f"{where}: {kinds.count(kind)} Messages of AttributeType {kind}, not one per "
                         "AttributeType (lwSRP PR #18; IEEE 802.1Q-2018 10.8.1.2)")
        seen: dict[tuple[int, str], int] = {}
        for kind, value, _ in f.values():
            seen[(kind, value)] = seen.get((kind, value), 0) + 1
        for (kind, value), n in sorted(seen.items()):
            if n > 1:
                found.append(f"{where}: {label(f.proto, kind, value)} declared {n} times in one MRPDU")
        la = f.leave_all_types()
        if la and la != set(app["types"]):
            found.append(f"{where}: a LeaveAll on AttributeTypes {sorted(la)}, not on every {f.proto} "
                         f"AttributeType {sorted(app['types'])} (IEEE 802.1Q-2018 10.7.9, 10.8.2.6)")
    return found


def grade_source(cap: Capture) -> tuple[list[str], dict]:
    """Every MRPDU from the port's MAC, from the first after reset (#839)."""
    mac = cap.doc["port_mac"]
    found = [f"[SA] {f.proto} frame at ms {f.ms} from {f.frame[6:12].hex()}, not the port's MAC {mac} (#839; "
             "IEEE 802.1AC-2016 11.1)" for f in cap.mrpdus if f.frame[6:12].hex() != mac]
    if not cap.mrpdus:
        found.append("[SA] no MRPDU left the MAC")
    first = cap.mrpdus[0].ms if cap.mrpdus else None
    return found, {"first_mrpdu_ms": first, "mrpdus": len(cap.mrpdus)}


# ---- [TIME] ------------------------------------------------------------------------

def grade_time(cap: Capture) -> list[str]:
    """Each participant's transmit opportunities at egress against 10.7.4 and Table 10-7, each bound widened
    by T_svc; a frame queued behind a hold is not graded."""
    found = []
    low, high = LEAVE_ALL_BOUNDS_MS
    for proto in APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        for a, b in zip(frames, frames[3:]):
            if (b.us - a.us) / 1000 < RATE_WINDOW_MS and not cap.held(a.ms, b.ms):
                found.append(f"[TIME] {proto}: four transmit opportunities in {(b.us - a.us) / 1000:.3f} ms from ms "
                             f"{a.ms}, inside 1.5 x JoinTime less T_svc ({RATE_WINDOW_MS} ms; IEEE 802.1Q-2018 "
                             "10.7.4.1)")
        received = cap.received(proto)
        # after a New, or a declaration's first message, the next message of the attribute (Table 10-3:
        # VN, AN, AA and VP each send again at the next transmit opportunity)
        history: dict[tuple[int, str], list[tuple[Mrpdu, str]]] = {}
        for f in frames:
            for kind, value, event in f.values():
                history.setdefault((kind, value), []).append((f, event))
        for (kind, value), msgs in sorted(history.items()):
            for k, (f, event) in enumerate(msgs):
                first = event in DECLARING and (k == 0 or msgs[k - 1][1] in ("Lv", "Mt"))
                if event != "New" and not first:
                    continue
                later = msgs[k + 1][0] if k + 1 < len(msgs) else None
                until = later.us / 1000 if later else cap.doc["run_ms"]
                if any(f.ms <= r <= until for r, _ in received) or cap.held(f.ms, until):
                    continue
                if until - f.us / 1000 > JOIN_FOLLOW_MS:
                    nxt = f"at ms {later.ms}" if later else "never"
                    found.append(f"[TIME] {label(proto, kind, value)}: its {event} at ms {f.ms} followed {nxt}, past "
                                 f"JoinTime + T_svc ({JOIN_FOLLOW_MS} ms; IEEE 802.1Q-2018 10.7.4.1, Table 10-3)")
        # LeaveAll: from the last one sent or received (Table 10-5 restarts the timer at either), or reset
        refs = [(0.0, "reset")] + [(r * 1000.0, "received") for r, la in received if la]
        sent = [f for f in frames if f.leave_all_types()]
        for f in sent + [None]:
            at = f.us if f else cap.doc["run_ms"] * 1000.0
            prior = [r for r in refs if r[0] < at]
            ref, why = max(prior) if prior else (0.0, "reset")
            gap = (at - ref) / 1000
            if cap.held(ref / 1000, at / 1000):
                pass
            elif gap > high or (f is not None and gap < low):
                what = f"its LeaveAll at ms {f.ms}" if f else f"the run's end at ms {cap.doc['run_ms']}"
                found.append(f"[TIME] {proto}: {what} {gap:.3f} ms after the last LeaveAll ({why}), outside "
                             f"{low} to {high} ms (IEEE 802.1Q-2018 10.7.4.3, Table 10-7, plus JoinTime and "
                             "T_svc)")
            if f:
                refs.append((f.us, "sent"))
    return found


def stats(values: list[float]) -> dict:
    """min, mean and max of a list of us, and its size."""
    if not values:
        return {"n": 0}
    return {"n": len(values), "min_us": round(min(values), 3), "mean_us": round(statistics.fmean(values), 3),
            "max_us": round(max(values), 3)}


def measure_time(cap: Capture) -> dict:
    """The egress interval error per MRP timer, and each frame's egress after its timer's expiry."""
    out: dict = {}
    timers = cap.doc["timers"]
    for proto in APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        expiries = [t for t in timers if t["proto"] == proto and t["event"] == "expire"
                    and t["kind"] in ("join", "periodic", "leaveall")]
        armed = {(t["id"], round(t["us"], 3)): t["cs"] for t in timers if t["event"] == "arm"}
        cause: list[tuple[str, dict] | None] = []
        for f in frames:
            kinds = ("leaveall",) if f.leave_all_types() else ("join", "periodic")
            before = [t for t in expiries if t["kind"] in kinds and t["us"] <= f.us
                      and f.us - t["us"] < ATTRIBUTE_MS * 1000]
            cause.append(("leaveall" if f.leave_all_types() else max(before, key=lambda t: t["us"])["kind"],
                          max(before, key=lambda t: t["us"])) if before else None)
        after: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        interval: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        for f, c in zip(frames, cause):
            if c and not cap.held(c[1]["ms"], f.ms):
                after[c[0]].append(f.us - c[1]["ms"] * 1000.0)
        for k in range(1, len(frames)):
            c, p = cause[k], cause[k - 1]
            if c is None or cap.held(frames[k - 1].ms, frames[k].ms):
                continue
            gap = frames[k].us - frames[k - 1].us
            if c[0] == "join":
                interval["join"].append(gap - JOIN_MS * 1000)
            elif c[0] == "periodic" and p and p[0] == "periodic":
                interval["periodic"].append(gap - PERIODIC_MS * 1000)
        la = [(f, c) for f, c in zip(frames, cause) if c and c[0] == "leaveall"]
        for (fa, ca), (fb, cb) in zip(la, la[1:]):
            draw = armed.get((ca[1]["id"], round(ca[1]["us"], 3)))
            # the draw armed at the earlier expiry, unless a received LeaveAll restarted the timer between
            restarted = any(t["proto"] == proto and t["kind"] == "leaveall" and t["event"] == "arm"
                            and ca[1]["us"] < t["us"] < cb[1]["us"] for t in timers)
            if draw and not restarted and not cap.held(fa.ms, fb.ms):
                interval["leaveall"].append((fb.us - fa.us) - draw * 10000)
        out[proto] = {"interval_error": {k: stats(v) for k, v in interval.items()},
                      "egress_after_tick": {k: stats(v) for k, v in after.items()}}
        per = [o[3] for o in cap.doc["opportunities"] if o[1] == proto]
        out[proto]["frames_per_opportunity"] = (
            {"n": len(per), "min": min(per), "mean": round(statistics.fmean(per), 3), "max": max(per)}
            if per else {"n": 0})
    return out


# ---- [TX] --------------------------------------------------------------------------

def grade_tx(cap: Capture) -> tuple[list[str], dict]:
    """The MRPDUs the adapter accepted against the MAC's, aligned by position: equal, a swapped pair, one
    accepted and lost, or one sent and never accepted. Periodic MRPDUs repeat byte for byte, so the
    alignment never searches ahead, and a frame is an accepted MRPDU's only if it left in the millisecond
    of its acceptance or the next, or behind a hold. Identical MRPDUs queued behind one hold cannot be told
    apart; a loss among them is still one, named at the first position no frame can fill."""
    found = []
    accepted = [entry for entry in cap.doc["lib"] if entry["rc"] == 0]
    sent = cap.mrpdus

    def same(a: dict | None, f: Mrpdu | None) -> bool:
        """Whether the MAC frame is the accepted MRPDU: its application, its bytes and a time it could leave at."""
        return a is not None and f is not None and f.proto == a["proto"] and \
            f.frame[14:14 + len(a["hex"]) // 2].hex() == a["hex"] and \
            a["ms"] <= f.ms and (f.ms - a["ms"] <= 1 or cap.held(a["ms"], f.ms))

    def at(seq: list, k: int) -> object:
        """The k-th entry, or None past the end."""
        return seq[k] if k < len(seq) else None

    i = j = 0
    while i < len(accepted) or j < len(sent):
        a, f = at(accepted, i), at(sent, j)
        if same(a, f):
            i, j = i + 1, j + 1
        elif same(at(accepted, i + 1), f) and same(a, at(sent, j + 1)) and (
                same(at(accepted, i + 2), at(sent, j + 2)) or (i + 2 >= len(accepted) and j + 2 >= len(sent))):
            found.append(f"[TX] the {a['proto']} MRPDU the adapter accepted at ms {a['ms']} left after the one it "
                         f"accepted next, at ms {at(sent, j + 1).ms}: out of the order accepted")
            i, j = i + 2, j + 2
        elif a and (f is None or same(at(accepted, i + 1), f)):
            found.append(f"[TX] the {a['proto']} MRPDU the adapter accepted at ms {a['ms']} never left the MAC")
            i += 1
        elif f and (a is None or same(a, at(sent, j + 1))):
            found.append(f"[TX] the {f.proto} frame at ms {f.ms} is no MRPDU the adapter accepted")
            j += 1
        else:
            found.append(f"[TX] the {a['proto']} MRPDU the adapter accepted at ms {a['ms']} never left the MAC, and "
                         f"the {f.proto} frame at ms {f.ms} in its place is no MRPDU the adapter accepted")
            i, j = i + 1, j + 1
    refused = [entry for entry in cap.doc["lib"] if entry["rc"] != 0]
    words = cap.doc["ring_words"]
    for r in refused:
        if r["ring_used"] + r["record"] <= words:
            found.append(f"[TX] the adapter refused the {r['proto']} MRPDU at ms {r['ms']} with {r['ring_used']} of "
                         f"{words} words in use and {r['record']} wanted: the ring had room")
        nxt = next((entry for entry in accepted if entry["proto"] == r["proto"] and entry["ms"] >= r["last_ms"]), None)
        if nxt is None or nxt["hex"] != r["hex"]:
            found.append(f"[TX] the {r['proto']} MRPDU refused from ms {r['ms']} to {r['last_ms']} was not the next "
                         f"{r['proto']} MRPDU the adapter sent")
    for a, b in cap.doc["holds"]:
        if not any(a <= r["ms"] < b for r in refused):
            found.append(f"[TX] the MAC refused every beat from ms {a} to {b}, and the adapter never saw the SRP "
                         "transmit ring full")
    measured = {"accepted": len(accepted), "sent": len(sent),
                "refusals": [{"proto": r["proto"], "from_ms": r["ms"], "to_ms": r["last_ms"], "retries": r["retries"],
                              "ring_used_min": r["ring_used"], "record_words": r["record"]} for r in refused]}
    return found, measured


# ---- [608] and [LIC] ---------------------------------------------------------------

def applied_ms(cap: Capture, prefix: str) -> int | None:
    """The millisecond the first stimulus frame named with this prefix was applied."""
    return next((a["ms"] for a in cap.doc["applied"] if a["what"].startswith(prefix)), None)


def gate_at(policer: list[dict], ms: int) -> int:
    """The stream gate as sampled at the end of millisecond ms."""
    value = 0
    for p in policer:
        if p["ms"] > ms:
            break
        value = p["gate"]
    return value


def grade_licence(cap: Capture) -> tuple[list[str], dict]:
    """The licence scenario: the #608 stop at the LeaveAll's LeaveTime deadline, and the policer holding the
    licence written at every millisecond."""
    if cap.scenario != "licence":
        return [], {}
    found: list[str] = []
    policer, writes = cap.doc["policer"], cap.doc["licence_writes"]
    leave_all = applied_ms(cap, "MSRP LeaveAll, the peer, no re-declaration")
    withdraw = applied_ms(cap, "MSRP Listener Ready Lv")
    on = next((p["ms"] for p in policer if p["gate"] & 1), None)
    if on is None or on > leave_all:
        found.append(f"[608] source 0 never held its licence before the peer's LeaveAll at ms {leave_all}" + FIXTURE)
        return found, {}
    off = next((p for p in policer if p["ms"] > leave_all and not p["gate"] & 1), None)
    cleared = next((w for w in writes if w[0] > leave_all * 1000 and not w[1] & 1), None)
    deadline = leave_all + LEAVE_MS
    if off is None:
        found.append(f"[608] the talker never stopped after the peer's LeaveAll at ms {leave_all} and its withdrawal "
                     f"at ms {withdraw}" + FIXTURE)
    else:
        stop = cleared[0] / 1000 if cleared else off["ms"]
        if stop > deadline + SVC_MS or stop < deadline - RESOLUTION_MS:
            found.append(f"[608] the talker stopped at ms {stop:.3f}, not at the LeaveTime deadline the peer's "
                         f"LeaveAll at ms {leave_all} started ({deadline} ms, T_svc {SVC_MS} ms; "
                         f"the withdrawal at ms {withdraw} in LV restarts nothing, IEEE 802.1Q-2018 Table 10-4, "
                         "Milan v1.2 4.2.7.2.2)" + FIXTURE)
        late = [s for s in cap.doc["stream"] if s[0] > off["ms"]]
        if late:
            found.append(f"[608] {sum(s[2] for s in late)} stream frame(s) after the stream gate closed at ms "
                         f"{off['ms']}, the last at ms {late[-1][0]}" + FIXTURE)
    # [LIC]: the gate is the licence written, at every sample; the AAF gate and the stream follow it
    for p in policer:
        written = [w for w in writes if w[0] <= p["ms"] * 1000 + 999.999]
        licence = written[-1][1] if written else 0
        mask = (1 << max(1, licence.bit_length(), p["gate"].bit_length())) - 1
        if p["gate"] & mask != licence & mask or p["active"] != p["admitted"] or p["active"] != p["gate"]:
            found.append(f"[LIC] at ms {p['ms']} the policer reads active {p['active']:#x}, admitted "
                         f"{p['admitted']:#x}, gate {p['gate']:#x}, and the firmware's LICENCE is {licence:#x}"
                         + FIXTURE)
        if p["aaf"] and not p["gate"] & 1:
            found.append(f"[LIC] at ms {p['ms']} the AAF talker's gate is open without source 0's licence" + FIXTURE)
        if p["crf_active"] != bool(p["gate"] & 2):
            found.append(f"[LIC] at ms {p['ms']} the CRF source's licence term reads {int(p['crf_active'])}, its "
                         f"stream gate bit {int(bool(p['gate'] & 2))}" + FIXTURE)
    for ms, sid, n in cap.doc["stream"]:
        if not gate_at(policer, ms) and not gate_at(policer, ms - 1):
            found.append(f"[LIC] {n} stream frame(s) with stream_id {sid} at ms {ms} while no source holds its licence"
                         + FIXTURE)
    leave = [t for t in cap.doc["timers"] if t["kind"] == "leave" and t["proto"] == "MSRP"]
    stream = cap.doc["stream"]
    return found, {"licence_from_ms": on, "peer_leave_all_ms": leave_all, "withdrawal_ms": withdraw,
                   "deadline_ms": deadline, "gate_closed_ms": off["ms"] if off else None,
                   "licence_cleared_us": cleared[0] if cleared else None,
                   "leave_timer_after_leave_all": [[t["ms"], t["event"], t["cs"]] for t in leave
                                                   if t["ms"] >= leave_all],
                   "stream_frames": sum(s[2] for s in stream), "first_stream_ms": stream[0][0] if stream else None,
                   "last_stream_ms": stream[-1][0] if stream else None,
                   "stream_ids": sorted({s[1] for s in stream})}


# ---- the run -----------------------------------------------------------------------

def grade(cap: Capture) -> tuple[list[str], dict]:
    """Every grade of one capture, and what it measured."""
    found: list[str] = []
    measured: dict = {"scenario": cap.scenario, "run_ms": cap.doc["run_ms"], "fixture": cap.doc["fixture"],
                      "intra_ms_max_us": cap.doc["intra_ms_max_us"]}
    if cap.doc["layout_error"]:
        found.append(f"[BENCH] {cap.doc['layout_error']}")
    if cap.doc["intra_ms_max_us"] >= MS_US:
        found.append(f"[BENCH] a modeled millisecond took {cap.doc['intra_ms_max_us']:.3f} us of RTL time, past the "
                     "1 ms the time base assumes")
    found += grade_wire(cap)
    f, m = grade_source(cap)
    found += f
    measured.update(m)
    f, m = grade_tx(cap)
    found += f
    measured["tx"] = m
    found += grade_time(cap)
    measured["timers"] = measure_time(cap)
    f, m = grade_licence(cap)
    found += f
    if m:
        measured["licence"] = m
    return found, measured


def main() -> int:
    """Grade a capture, plant one, or check a planted one's words; the exit status is the verdict."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--make-plant")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--plant")
    args = parser.parse_args()
    if args.make_plant:
        import srptx_plants
        doc = json.loads(args.capture.read_text())
        srptx_plants.plant(args.make_plant, doc)
        args.out.write_text(json.dumps(doc) + "\n")
        print(f"srptx_grade: planted {args.make_plant} into {args.out.name}")
        return 0
    cap = load(args.capture)
    found, measured = grade(cap)
    if args.report:
        args.report.write_text(json.dumps({"findings": found, "measured": measured}, indent=1) + "\n")
    if args.plant:
        import srptx_plants
        if args.plant in srptx_plants.WITHIN:
            print(f"control {args.plant}: {'REFUSED: ' + found[0] if found else 'clean'}")
            return 1 if found else 0
        words = srptx_plants.WORDS[args.plant]
        caught = [x for x in found if words in x]
        print(f"plant {args.plant}: {'refused' if caught else 'ESCAPED'}: {caught[0] if caught else words}")
        return 0 if caught else 1
    for x in found:
        print(x)
    print(f"srptx {cap.scenario}: {len(found)} finding(s), {len(cap.mrpdus)} MRPDUs, run {cap.doc['run_ms']} ms")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
