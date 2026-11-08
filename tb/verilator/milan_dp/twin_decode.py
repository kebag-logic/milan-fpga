#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_decode.py - what the two-placement simulation's comparison reads out of a capture (#665).

The capture each half writes (twin.hpp Capture: every control frame its MAC sent, with the modeled
millisecond it left at, and the stimulus as applied), its frames classified by protocol, and the
fields the comparison (twin_compare.py) names:

  * the AECPDU's (IEEE 1722.1-2021 Figure 9-1, 9.2.1.2), its role (a solicited response, an
    unsolicited notice, or a command the entity originates) and its recipient;
  * GET_STREAM_INFO's (IEEE 1722.1-2021 7.4.16.2), the probing_status that tells a settled sink;
  * MSRP's attributes through sw/firmware/ctrl/test/srp_wire_compare.py (IEEE 802.1Q-2018 10.8,
    Tables 35-1 to 35-3);
  * MVRP's (IEEE 802.1Q-2018 10.8.1.2, 11.2.3.1), whose Message carries no AttributeListLength.

Every frame is read as the wire carries it: shorter than 60 bytes it is padded with zeros to 60,
as the SoC's MAC pads it (LiteEthMACCore with_padding, sw/litex/milan_soc.py; IEEE 802.3-2018 3.2.7).
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "sw/firmware/ctrl/test"))
import srp_wire_compare  # noqa: E402

MIN_FRAME = 60
AVTP = 0x22F0
SUBTYPES = {0xFA: "ADP", 0xFB: "AECP", 0xFC: "ACMP", 0xFE: "MAAP"}
ETHERTYPES = {0x22EA: "MSRP", 0x88F5: "MVRP"}

#: the two controllers of the stimulus (twin.hpp kController, kController2)
CONTROLLERS = {0x1111222233334444: "the first controller", 0x2222333344445555: "the second controller"}


@dataclass(frozen=True)
class Sent:
    """One control frame: the millisecond it left at, its padded bytes and where its protocol PDU starts."""

    ms: int
    data: bytes
    at: int


@dataclass(frozen=True)
class Applied:
    """One stimulus frame as a half applied it: its millisecond, its name and its bytes."""

    ms: int
    what: str
    data: bytes


@dataclass
class Capture:
    """One half's capture, its frames grouped by protocol in the order its MAC sent them."""

    placement: str
    run_ms: int
    notes: dict
    applied: list[Applied]
    frames: dict[str, list[Sent]]
    first_stream_ms: int


def classify(data: bytes) -> tuple[str, int] | None:
    """The protocol of a control frame and its PDU's offset, past an optional C-tag."""
    at = 12
    kind = int.from_bytes(data[at:at + 2], "big")
    if kind == 0x8100:
        at += 4
        kind = int.from_bytes(data[at:at + 2], "big")
    at += 2
    if kind in ETHERTYPES:
        return ETHERTYPES[kind], at
    if kind == AVTP and at < len(data) and data[at] in SUBTYPES:
        return SUBTYPES[data[at]], at
    return None


def load(path: Path) -> Capture:
    """Read a capture; every frame padded as the MAC pads it."""
    doc = json.loads(path.read_text())
    frames: dict[str, list[Sent]] = {}
    for entry in doc["frames"]:
        data = bytes.fromhex(entry["hex"])
        found = classify(data)
        if found is None:
            raise SystemExit(f"{path}: a frame of no compared protocol at ms {entry['ms']}")
        frames.setdefault(found[0], []).append(Sent(entry["ms"], data.ljust(MIN_FRAME, b"\0"), found[1]))
    applied = [Applied(a["ms"], a["what"], bytes.fromhex(a["hex"])) for a in doc["applied"]]
    return Capture(doc["placement"], doc["run_ms"], doc["notes"], applied, frames,
                   int(doc.get("first_stream_ms", -1)))


# ---- AECP (IEEE 1722.1-2021 Figure 9-1, 9.2.1.2) --------------------------

AEM_COMMANDS = {0x0001: "LOCK_ENTITY", 0x0003: "CONTROLLER_AVAILABLE", 0x0004: "READ_DESCRIPTOR",
                0x0008: "SET_STREAM_FORMAT", 0x0009: "GET_STREAM_FORMAT", 0x000E: "SET_STREAM_INFO",
                0x000F: "GET_STREAM_INFO", 0x0022: "START_STREAMING", 0x0023: "STOP_STREAMING",
                0x0024: "REGISTER_UNSOLICITED_NOTIFICATION", 0x0025: "DEREGISTER_UNSOLICITED_NOTIFICATION",
                0x0029: "GET_COUNTERS"}
#: Milan v1.2 Table 5.18
MVU_COMMANDS = {0: "GET_MILAN_INFO", 1: "SET_SYSTEM_UNIQUE_ID", 2: "GET_SYSTEM_UNIQUE_ID",
                3: "SET_MEDIA_CLOCK_REFERENCE_INFO", 4: "GET_MEDIA_CLOCK_REFERENCE_INFO"}
#: IEEE 1722.1-2021 Table 9-1, the command types; a response is one higher
MESSAGES = {0: "AEM", 2: "ADDRESS_ACCESS", 4: "AVC", 6: "VENDOR_UNIQUE", 8: "HDCP_APM", 10: "reserved 10"}
MVU_PROTOCOL = bytes.fromhex("001bc50ac100")
#: where an AEM command's descriptor_type and descriptor_index sit after its command_type (IEEE
#: 1722.1-2021 7.4): ACQUIRE_ENTITY's and LOCK_ENTITY's after their flags and owner (7.4.1.1, 7.4.2.1),
#: READ_DESCRIPTOR's after the configuration (7.4.5.1); None for a command that names none
DESCRIPTOR_AT = {0x0000: 12, 0x0001: 12, 0x0002: None, 0x0003: None, 0x0004: 4, 0x0024: None, 0x0025: None}


@dataclass(frozen=True)
class Aecp:
    """The fields of one AECPDU the comparison names."""

    message_type: int
    status: int
    target: int
    controller: int
    seq: int
    unsolicited: bool
    command: int
    descriptor: tuple[int, int]


def aecp(s: Sent) -> Aecp:
    """Decode the AECPDU at s.at: for an AEM PDU its command_type and descriptor pair, for a Milan
    vendor-unique one its MVU command_type (Milan v1.2 5.4.3.2), otherwise command 0."""
    d, at = s.data, s.at
    kind = d[at + 1] & 0x0F
    word = int.from_bytes(d[at + 22:at + 24], "big")
    command, unsolicited, pair = 0, False, (0, 0)
    if kind in (0, 1):
        command, unsolicited = word & 0x7FFF, bool(word & 0x8000)
        where = DESCRIPTOR_AT.get(command, 0)
        if where is not None:
            o = at + 24 + where
            pair = (int.from_bytes(d[o:o + 2], "big"), int.from_bytes(d[o + 2:o + 4], "big"))
    elif kind in (6, 7) and d[at + 22:at + 28] == MVU_PROTOCOL:
        command = int.from_bytes(d[at + 28:at + 30], "big") & 0x7FFF
    return Aecp(kind, d[at + 2] >> 3, int.from_bytes(d[at + 4:at + 12], "big"),
                int.from_bytes(d[at + 12:at + 20], "big"), int.from_bytes(d[at + 20:at + 22], "big"),
                unsolicited, command, pair)


def control_length(s: Sent) -> int:
    """The AECPDU's control_data_length (IEEE 1722.1-2021 9.2.1.1.7)."""
    return (s.data[s.at + 2] & 0x07) << 8 | s.data[s.at + 3]


def role(s: Sent) -> str:
    """'command' for a command the entity originates (an even message_type, CONTROLLER_AVAILABLE),
    'notice' for an unsolicited response (IEEE 1722.1-2021 7.5.2), 'response' otherwise."""
    f = aecp(s)
    if f.message_type % 2 == 0:
        return "command"
    return "notice" if f.unsolicited else "response"


def recipient(s: Sent) -> int:
    """The controller a frame is for: a response's or notice's controller_entity_id, the target of a
    command the entity sends."""
    f = aecp(s)
    return f.target if role(s) == "command" else f.controller


def who(entity: int) -> str:
    """A controller as a finding names it."""
    return CONTROLLERS.get(entity, f"controller {entity:#018x}")


def command_name(f: Aecp) -> str:
    """The command a PDU carries, by its message type's table."""
    if f.message_type in (0, 1):
        return AEM_COMMANDS.get(f.command, f"command {f.command:#06x}")
    if f.message_type in (6, 7):
        return "MVU " + MVU_COMMANDS.get(f.command, f"command {f.command:#06x}")
    return MESSAGES.get(f.message_type & ~1, f"message_type {f.message_type}")


def notice_key(s: Sent) -> tuple[int, tuple[int, int]]:
    """A notice's sub-sequence: (command_type, (descriptor_type, descriptor_index)) (#665
    issuecomment-6717765106, item 2)."""
    f = aecp(s)
    return f.command, f.descriptor


def without_seq(s: Sent) -> bytes:
    """The frame with its sequence_id zeroed, as notices are compared."""
    return s.data[:s.at + 20] + b"\0\0" + s.data[s.at + 22:]


def describe(proto: str, s: Sent) -> str:
    """A frame as a finding names it."""
    if proto != "AECP":
        return f"{proto} message_type {s.data[s.at + 1] & 0x0F} at ms {s.ms}"
    f = aecp(s)
    named = f.message_type in (0, 1) and DESCRIPTOR_AT.get(f.command, 0) is not None
    pair = f" {f.descriptor[0]:#06x}/{f.descriptor[1]}" if named else ""
    return (f"AECP {role(s)} {command_name(f)}{pair} to {who(recipient(s))} status {f.status} "
            f"sequence_id {f.seq} at ms {s.ms}")


#: GET_STREAM_INFO's fields after its descriptor pair (IEEE 1722.1-2021 7.4.16.2; Milan v1.2 5.4.2.9)
STREAM_INFO_FIELDS = slice(28, 28 + 80)
#: probing_status, the top three bits of the octet 48 into those fields; 3 is COMPLETED, a settled sink
PROBING_OCTET = 48
PROBING_COMPLETED = 3


def stream_info(s: Sent) -> bytes:
    """A GET_STREAM_INFO or SET_STREAM_INFO PDU's fields after its descriptor pair, to its length."""
    end = s.at + 12 + control_length(s)
    return s.data[s.at + STREAM_INFO_FIELDS.start:min(end, s.at + STREAM_INFO_FIELDS.stop)]


def settled(s: Sent) -> bool:
    """A STREAM_INPUT's GET_STREAM_INFO reporting its sink settled (probing_status COMPLETED)."""
    fields = stream_info(s)
    return len(fields) > PROBING_OCTET and fields[PROBING_OCTET] >> 5 == PROBING_COMPLETED


# ---- MRP: MSRP and MVRP (IEEE 802.1Q-2018 10.8) ------------------------------

#: IEEE 802.1Q-2018 10.8.2.6, the ThreePackedEvents values
EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")
DECLARING = frozenset({"New", "JoinIn", "JoinMt"})
#: IEEE 802.1Q-2018 Table 35-1
MSRP_TYPES = {1: "Talker Advertise", 2: "Talker Failed", 3: "Listener", 4: "Domain"}


@dataclass(frozen=True)
class Event:
    """One attribute event of one MRPDU: the attribute (type and value), the event, its
    FourPackedEvent where the type has one, and whether its vector carried a LeaveAll."""

    ms: int
    kind: int
    value: str
    event: str
    four: int | None
    leave_all: bool


def unpad_mrp(data: bytes, at: int) -> bytes:
    """An MSRP frame up to its PDU EndMark (IEEE 802.1Q-2018 10.8.1.2), the MAC's pad dropped: each message
    is AttributeType, AttributeLength and AttributeListLength, then that many bytes. A frame that never
    reaches its EndMark is returned whole, for srp_wire_compare.py's decoder to refuse by name."""
    offset = at + 1
    while offset + 4 <= len(data) and data[offset:offset + 2] != b"\0\0":
        offset += 4 + int.from_bytes(data[offset + 2:offset + 4], "big")
    return data[:offset + 2] if offset + 2 <= len(data) else data


def msrp_frame(s: Sent) -> tuple[list[Event], frozenset[int]]:
    """Every attribute event of one MSRP frame, in encounter order, and the attribute types its LeaveAll
    covers (IEEE 802.1Q-2018 10.8.2.6: a LeaveAll in a Message applies to the Message's type)."""
    d = srp_wire_compare.decode_frame(unpad_mrp(s.data, s.at))
    return ([Event(s.ms, e[0], e[1], EVENTS[e[2]], e[3], e[4]) for e in d["events"]],
            frozenset(d["leave_all_types"]))


def msrp_events(s: Sent) -> tuple[list[Event], bool]:
    """Every attribute event of one MSRP frame, in encounter order, and whether it carried a LeaveAll."""
    events, leave_all = msrp_frame(s)
    return events, bool(leave_all)


def received(cap: Capture, proto: str) -> list[Sent]:
    """The stimulus frames of one protocol a half received, as the comparison reads its own."""
    found = []
    for a in cap.applied:
        data = a.data.ljust(MIN_FRAME, b"\0")
        kind = classify(data)
        if kind is not None and kind[0] == proto:
            found.append(Sent(a.ms, data, kind[1]))
    return found


def mvrp_events(s: Sent) -> tuple[list[Event], bool]:
    """Every attribute event of one MVRP frame (IEEE 802.1Q-2018 10.8.1.2, 11.2.3.1: Message ::=
    AttributeType AttributeLength AttributeList, each VectorAttribute's header, FirstValue and
    ThreePackedEvents, each list and the PDU closed by an EndMark), and whether it carried a LeaveAll.
    A malformed MRPDU raises srp_wire_compare.Malformed, naming what is wrong."""
    pdu, offset = s.data, s.at + 1
    need = srp_wire_compare.require
    need(pdu[s.at] == 0, "MVRP ProtocolVersion")
    events: list[Event] = []
    leave_all = False
    while pdu[offset:offset + 2] != b"\0\0":
        need(offset + 2 <= len(pdu), "missing MVRP PDU EndMark")
        kind, length = pdu[offset], pdu[offset + 1]
        need(kind == 1 and length == 2, "MVRP AttributeType 1, AttributeLength 2")
        offset += 2
        while pdu[offset:offset + 2] != b"\0\0":
            need(offset + 2 <= len(pdu), "missing MVRP AttributeList EndMark")
            flag, count = divmod(int.from_bytes(pdu[offset:offset + 2], "big"), 8192)
            need(flag in (0, 1) and (flag or count), "MVRP vector header")
            leave_all = leave_all or bool(flag)
            first = int.from_bytes(pdu[offset + 2:offset + 2 + length], "big")
            packed = pdu[offset + 2 + length:offset + 2 + length + (count + 2) // 3]
            need(all(v < 216 for v in packed), "reserved MVRP ThreePackedEvents")
            unpacked = [x for p in packed for x in (p // 36, (p // 6) % 6, p % 6)]
            events += [Event(s.ms, kind, f"{first + k:04x}", EVENTS[unpacked[k]], None, bool(flag))
                       for k in range(count)]
            offset += 2 + length + len(packed)
        offset += 2
    return events, leave_all


def attribute_label(kind: int, value: str) -> str:
    """An MSRP attribute as a finding names it: its type, and its stream_id or its value."""
    name = MSRP_TYPES.get(kind, f"type {kind}")
    return f"{name} stream_id {value[:16]}" if kind in (1, 2, 3) else f"{name} value {value}"


def run_length(events: list[str]) -> str:
    """An event sequence as runs, the way a finding prints it: "New x2, JoinMt x14"."""
    runs: list[list] = []
    for e in events:
        if runs and runs[-1][0] == e:
            runs[-1][1] += 1
        else:
            runs.append([e, 1])
    return ", ".join(f"{e} x{n}" for e, n in runs)
