#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_plants.py - the two-placement simulation's capture plants (#665).

Each plant writes a copy of one half's capture (twin.hpp Capture) with one planted difference, which
twin_compare.py must refuse by the plant's words (twin_compare.PLANT_WORDS), against the unplanted capture
and between the placements (make twin-plants). SPLIT_PLANTS plant the split half's capture and FABRIC_PLANTS
the all-fabric half's: an owed defect of the fabric gone is planted where the fix would land.

Each plant names the grade or row it is the plant of:
  * uncovered-field, vanished-owed: a difference no row covers, and an owed difference gone (OWED);
  * command-byte: the entity's own commands are still byte-compared, sequence_id aside;
  * command-sequence, response-sequence: the commands' sequence_id per controller (grade_commands);
  * table-10-3, received-join: an MSRP attribute's trace against Table 10-3, and through a received MRPDU,
    against its Registrar (twin_mrp.py);
  * mvrp-join-in, mvrp-received-join: the same grade of an MVRP attribute, the split's VID 2 (#665
    issuecomment-6724570965, item 2);
  * leave-all-declaration: the declaration state at the LeaveAll boundaries (compare_declarations);
  * vanished-mvrp-leave-all: the #857 owed row's defect gone (OWED_GRADES);
  * vanished-available-index: the #858 owed row's difference gone (OWED);
  * vanished-domain-new, vanished-vid2-join-in: the #860 owed rows' defects gone, where the fix would land
    (OWED_GRADES; issuecomment-6724570965, items 1 and 2);
  * domain-trace-moved, vid2-registrar-in: each #860 row's exact trace, the defect kept but the trace changed:
    the Domain's first Join sent as JoinIn, and VID 2 registered by a peer's MVRPDU.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator

import twin_decode as td
from twin_decode import Sent, aecp

FIRST, SECOND = 0x1111222233334444, 0x2222333344445555
#: the peer's MAC (twin.hpp kPeerMac), MSRP's destination, the nearest-bridge group address, and MVRP's, the
#: Customer Bridge MVRP address (IEEE 802.1Q-2018 Table 10-1)
PEER_MAC = bytes.fromhex("001b920000aa")
MSRP_DA = bytes.fromhex("0180c200000e")
MSRP_ETHERTYPE = 0x22EA
MVRP_DA = bytes.fromhex("0180c2000021")
MVRP_ETHERTYPE = 0x88F5
#: the Domain the halves declare (Milan v1.2 4.2.7.2.1: SRclassID 6, priority 3, VID 2)
DOMAIN = bytes.fromhex("06030002")
#: IEEE 802.1Q-2018 10.8.2.6: a single value's ThreePackedEvents octet is its event x 36
NEW, JOIN_IN, JOIN_MT, LV = 0, 1, 3, 5


def frame_fields(entry: dict) -> tuple[str, Sent] | None:
    """A capture entry's protocol and frame, padded as the comparison reads it, or None for no compared one."""
    data = bytes.fromhex(entry["hex"]).ljust(td.MIN_FRAME, b"\0")
    found = td.classify(data)
    return (found[0], Sent(entry["ms"], data, found[1])) if found else None


def aecp_doc_frame(entry: dict) -> td.Aecp | None:
    """A capture entry's AECPDU fields, or None for any other frame."""
    found = frame_fields(entry)
    return aecp(found[1]) if found and found[0] == "AECP" else None


def planted(doc: dict, name: str) -> dict:
    """The capture, marked with the plant it carries."""
    doc["notes"]["plant"] = name
    return doc


def set_byte(entry: dict, at: int, value: int) -> None:
    """One byte of a capture entry's frame set to `value`."""
    data = bytearray(bytes.fromhex(entry["hex"]))
    data[at] = value
    entry["hex"] = data.hex()


# ---- AECP --------------------------------------------------------------------------


def plant_uncovered_field(fabric: dict, split: dict) -> dict:
    """A fourth difference, in a field no row covers: the first GET_STREAM_INFO notice of STREAM_INPUT 0 to
    the first controller, msrp_accumulated_latency's last octet inverted (frame byte 65)."""
    del fabric
    for entry in split["frames"]:
        f = aecp_doc_frame(entry)
        if f and f.unsolicited and (f.command, f.descriptor) == (0x000F, (5, 0)) and f.controller == FIRST:
            set_byte(entry, 65, bytes.fromhex(entry["hex"])[65] ^ 0xFF)
            return planted(split, "uncovered-field")
    raise SystemExit("plant uncovered-field: no GET_STREAM_INFO notice of STREAM_INPUT 0 to plant")


def plant_vanished_owed(fabric: dict, split: dict) -> dict:
    """An owed difference gone: the split capture carries the fabric's GET_STREAM_INFO notices of
    STREAM_OUTPUT 0, each at its own millisecond, as the lane that fixes the talker's state would send them."""
    owed = [e for e in fabric["frames"] if (f := aecp_doc_frame(e)) and f.unsolicited
            and (f.command, f.descriptor) == (0x000F, (6, 0))]
    if not owed:
        raise SystemExit("plant vanished-owed: the fabric capture has no STREAM_OUTPUT 0 notice to copy")
    split["frames"] = sorted(split["frames"] + owed, key=lambda e: e["ms"])
    return planted(split, "vanished-owed")


def controller_available(doc: dict, to: int) -> list[dict]:
    """The split's CONTROLLER_AVAILABLE commands to one controller, in send order."""
    return [e for e in doc["frames"] if (f := aecp_doc_frame(e)) and f.message_type == 0 and f.command == 0x0003
            and f.target == to]


def plant_command_byte(fabric: dict, split: dict) -> dict:
    """The entity's first CONTROLLER_AVAILABLE command to the first controller with its controller_entity_id's
    last octet inverted (frame byte 33): the command compare reads every byte but the sequence_id."""
    del fabric
    found = controller_available(split, FIRST)
    if not found:
        raise SystemExit("plant command-byte: no CONTROLLER_AVAILABLE command to the first controller")
    set_byte(found[0], 33, bytes.fromhex(found[0]["hex"])[33] ^ 0xFF)
    return planted(split, "command-byte")


def plant_command_sequence(fabric: dict, split: dict) -> dict:
    """The entity's second CONTROLLER_AVAILABLE command to the second controller given the first's
    sequence_id, so the ids to that controller do not rise."""
    del fabric
    found = controller_available(split, SECOND)
    if len(found) < 2:
        raise SystemExit("plant command-sequence: fewer than two CONTROLLER_AVAILABLE commands to the second "
                         "controller")
    first = bytes.fromhex(found[0]["hex"])
    set_byte(found[1], 34, first[34])
    set_byte(found[1], 35, first[35])
    return planted(split, "command-sequence")


def plant_response_sequence(fabric: dict, split: dict) -> dict:
    """The first controller's answer to the entity's CONTROLLER_AVAILABLE, as the stimulus applied it, with a
    sequence_id one higher than its command's."""
    del fabric
    for entry in split["applied"]:
        if entry["what"] == "AECP CONTROLLER_AVAILABLE response, the first controller":
            seq = (int.from_bytes(bytes.fromhex(entry["hex"])[34:36], "big") + 1) & 0xFFFF
            set_byte(entry, 34, seq >> 8)
            set_byte(entry, 35, seq & 0xFF)
            return planted(split, "response-sequence")
    raise SystemExit("plant response-sequence: the first controller never answered a CONTROLLER_AVAILABLE")


# ---- MSRP --------------------------------------------------------------------------


def msrp_vectors(data: bytes, at: int) -> Iterator[tuple[int, int, int]]:
    """Each VectorAttribute of an MSRP frame (IEEE 802.1Q-2018 10.8.1.2): its AttributeType, the offset of
    its VectorHeader and its ThreePackedEvents' offset."""
    offset = at + 1
    while offset + 4 <= len(data) and data[offset:offset + 2] != b"\0\0":
        kind, length = data[offset], data[offset + 1]
        end = offset + 4 + int.from_bytes(data[offset + 2:offset + 4], "big")
        vector = offset + 4
        while vector + 2 <= end and data[vector:vector + 2] != b"\0\0":
            count = int.from_bytes(data[vector:vector + 2], "big") & 0x1FFF
            yield kind, vector, vector + 2 + length
            vector += 2 + length + (count + 2) // 3 + ((count + 3) // 4 if kind == 3 else 0)
        offset = end


def domain_events(doc: dict) -> Iterator[tuple[dict, int]]:
    """Each MSRP frame of a capture carrying the Domain, and its Domain vector's ThreePackedEvents offset (one
    value, its event the octet's first of three)."""
    for entry in doc["frames"]:
        found = frame_fields(entry)
        if found is None or found[0] != "MSRP":
            continue
        s = found[1]
        for kind, vector, packed in msrp_vectors(s.data, s.at):
            if kind == 4 and s.data[vector + 2:vector + 6] == DOMAIN:
                yield entry, packed


def plant_table_10_3(fabric: dict, split: dict) -> dict:
    """The split's Domain sends New once, as the fabric's does: its second New (from AN) re-encoded JoinMt
    (IEEE 802.1Q-2018 10.8.2.6: JoinMt is 3, so the octet is 3 x 36)."""
    del fabric
    news = [(e, at) for e, at in domain_events(split) if bytes.fromhex(e["hex"])[at] // 36 == 0]
    if len(news) < 2:
        raise SystemExit("plant table-10-3: the split's Domain does not send New twice")
    set_byte(news[1][0], news[1][1], 3 * 36)
    return planted(split, "table-10-3")


def plant_leave_all_declaration(fabric: dict, split: dict) -> dict:
    """The split's Domain withdrawn from its first frame at or after 30000 ms: a Lv there and Mt in every later
    frame, a legal Applicant's trace (Lv! in QA, then LA, VO and LO), so only the declaration state at the
    later LeaveAll boundaries differs."""
    del fabric
    later = [(e, at) for e, at in domain_events(split) if e["ms"] >= 30000]
    if not later:
        raise SystemExit("plant leave-all-declaration: no Domain after 30000 ms")
    set_byte(later[0][0], later[0][1], 5 * 36)
    for entry, at in later[1:]:
        set_byte(entry, at, 4 * 36)
    return planted(split, "leave-all-declaration")


def plant_received_join(fabric: dict, split: dict) -> dict:
    """A peer's MSRP Domain JoinIn the split receives at 30500 ms, as the stimulus would apply it: its Registrar
    goes IN (IEEE 802.1Q-2018 Table 10-4), so its next sJ must be JoinIn (10.7.6.3), and the split, which never
    received it, sends JoinMt."""
    del fabric
    pdu = bytes([0, 4, 4]) + (2 + 4 + 1 + 2).to_bytes(2, "big") + bytes.fromhex("0001") + DOMAIN + bytes([1 * 36])
    pdu += bytes(4)
    frame = (MSRP_DA + PEER_MAC + MSRP_ETHERTYPE.to_bytes(2, "big") + pdu).ljust(td.MIN_FRAME, b"\0")
    split["applied"] = sorted(split["applied"] + [{"ms": 30500, "what": "MSRP Domain JoinIn from a peer (planted)",
                                                   "hex": frame.hex()}], key=lambda a: a["ms"])
    return planted(split, "received-join")


# ---- MVRP --------------------------------------------------------------------------


def vid2_events(doc: dict) -> Iterator[tuple[dict, int]]:
    """Each VID 2 vector of a capture's MVRP frames, as its frame entry and its ThreePackedEvents offset (one
    value, its event the octet's first of three): IEEE 802.1Q-2018 10.8.1.2, 11.2.3.1, a Message with no
    AttributeListLength, each vector a VectorHeader, a FirstValue of AttributeLength octets and its events."""
    for entry in doc["frames"]:
        found = frame_fields(entry)
        if found is None or found[0] != "MVRP":
            continue
        data, offset = found[1].data, found[1].at + 1
        while offset + 2 <= len(data) and data[offset:offset + 2] != b"\0\0":
            length = data[offset + 1]
            offset += 2
            while offset + 2 <= len(data) and data[offset:offset + 2] != b"\0\0":
                count = int.from_bytes(data[offset:offset + 2], "big") & 0x1FFF
                if count == 1 and int.from_bytes(data[offset + 2:offset + 2 + length], "big") == 2:
                    yield entry, offset + 2 + length
                offset += 2 + length + (count + 2) // 3
            offset += 2


def vid2_frame(event: int) -> bytes:
    """A peer's MVRPDU declaring VID 2 with one event, as the stimulus would apply it: ProtocolVersion 0, one
    Message of AttributeType 1 (the VID) and AttributeLength 2, one vector, and the list's and the PDU's
    EndMarks (IEEE 802.1Q-2018 10.8.1.2, 11.2.3.1)."""
    pdu = bytes([0, 1, 2]) + bytes.fromhex("0001") + bytes.fromhex("0002") + bytes([event * 36]) + bytes(4)
    return (MVRP_DA + PEER_MAC + MVRP_ETHERTYPE.to_bytes(2, "big") + pdu).ljust(td.MIN_FRAME, b"\0")


def plant_mvrp_join_in(fabric: dict, split: dict) -> dict:
    """The split's second VID 2 message, a JoinMt with its Registrar MT, re-encoded JoinIn, as the fabric sends
    it: sJ sends JoinIn only with the Registrar IN (IEEE 802.1Q-2018 10.7.6.3)."""
    del fabric
    found = list(vid2_events(split))
    if len(found) < 2 or bytes.fromhex(found[1][0]["hex"])[found[1][1]] != JOIN_MT * 36:
        raise SystemExit("plant mvrp-join-in: the split's second VID 2 message is not a JoinMt")
    set_byte(found[1][0], found[1][1], JOIN_IN * 36)
    return planted(split, "mvrp-join-in")


def plant_mvrp_received_join(fabric: dict, split: dict) -> dict:
    """A peer's VID 2 JoinIn the split receives at 30500 ms, as the stimulus would apply it: MVRP's Registrar
    (Table 10-4) goes IN, so its next sJ must be JoinIn (10.7.6.3), and the split, which never received it,
    sends JoinMt."""
    del fabric
    split["applied"] = sorted(split["applied"] + [{"ms": 30500, "what": "MVRP VID 2 JoinIn from a peer (planted)",
                                                   "hex": vid2_frame(JOIN_IN).hex()}], key=lambda a: a["ms"])
    return planted(split, "mvrp-received-join")


# ---- the fabric's owed defects gone ----------------------------------------------


def plant_vanished_mvrp_leave_all(fabric: dict, split: dict) -> dict:
    """#857 fixed: the fabric's MVRP sends a LeaveAll every 12 s after its one at 10201 ms, each an MRPDU of
    one LeaveAll vector of no value (IEEE 802.1Q-2018 10.8.2.4, 11.2.3.1), from its own header."""
    del split
    own = [e for e in fabric["frames"] if (f := frame_fields(e)) and f[0] == "MVRP"]
    if not own:
        raise SystemExit("plant vanished-mvrp-leave-all: the fabric sent no MVRP")
    header = bytes.fromhex(own[0]["hex"])[:14]
    pdu = bytes([0, 1, 2]) + bytes.fromhex("2000") + bytes.fromhex("0002") + bytes(4)
    added = [{"ms": ms, "hex": (header + pdu).ljust(td.MIN_FRAME, b"\0").hex()} for ms in range(22201, 75000, 12000)]
    fabric["frames"] = sorted(fabric["frames"] + added, key=lambda e: e["ms"])
    return planted(fabric, "vanished-mvrp-leave-all")


def plant_vanished_available_index(fabric: dict, split: dict) -> dict:
    """#858 fixed: the fabric's ENTITY descriptor of the later read carries its last ENTITY_AVAILABLE's
    available_index, 1 (frame byte 81, the index's last octet)."""
    del split
    for entry in fabric["frames"]:
        f = aecp_doc_frame(entry)
        if f and f.message_type == 1 and f.command == 0x0004 and f.controller == FIRST and f.seq == 25:
            set_byte(entry, 14 + 64 + 3, 1)
            return planted(fabric, "vanished-available-index")
    raise SystemExit("plant vanished-available-index: no response to the later ENTITY read")


def fabric_domain(fabric: dict, name: str) -> list[tuple[dict, int]]:
    """The fabric's Domain messages, which must open with one New and then a JoinMt (#860)."""
    found = list(domain_events(fabric))
    octets = [bytes.fromhex(e["hex"])[at] for e, at in found[:2]]
    if octets != [NEW * 36, JOIN_MT * 36]:
        raise SystemExit(f"plant {name}: the fabric's Domain does not open with one New, then JoinMt")
    return found


def plant_vanished_domain_new(fabric: dict, split: dict) -> dict:
    """#860 fixed for the Domain: the fabric's first JoinMt (1000 ms) sent as a second New, so its Domain is New
    twice, then JoinMt (Table 10-3: VN, AN, then AA by note 8 with the Registrar MT)."""
    del split
    entry, at = fabric_domain(fabric, "vanished-domain-new")[1]
    set_byte(entry, at, NEW * 36)
    return planted(fabric, "vanished-domain-new")


def plant_domain_trace_moved(fabric: dict, split: dict) -> dict:
    """The fabric's Domain still not an Applicant's, but its trace another than the #860 row asserts: its first
    JoinMt (1000 ms) sent as JoinIn."""
    del split
    entry, at = fabric_domain(fabric, "domain-trace-moved")[1]
    set_byte(entry, at, JOIN_IN * 36)
    return planted(fabric, "domain-trace-moved")


def plant_vanished_vid2_join_in(fabric: dict, split: dict) -> dict:
    """#860 fixed for VID 2: the fabric's first JoinIn (6200 ms) sent as a second New and every later JoinIn as
    JoinMt, its Registrar being MT (10.7.6.3); the Lv at 20000 ms kept."""
    del split
    found = list(vid2_events(fabric))
    octets = [bytes.fromhex(e["hex"])[at] for e, at in found]
    if octets[:2] != [NEW * 36, JOIN_IN * 36]:
        raise SystemExit("plant vanished-vid2-join-in: the fabric's VID 2 does not open with New, then JoinIn")
    set_byte(found[1][0], found[1][1], NEW * 36)
    for (entry, at), octet in zip(found[2:], octets[2:]):
        if octet == JOIN_IN * 36:
            set_byte(entry, at, JOIN_MT * 36)
    return planted(fabric, "vanished-vid2-join-in")


def plant_vid2_registrar_in(fabric: dict, split: dict) -> dict:
    """The fabric's VID 2 still sent New then JoinIn, but registered by a peer's VID 2 JoinIn at 6000 ms, so its
    Registrar is no longer MT throughout, as the #860 row asserts."""
    del split
    fabric["applied"] = sorted(fabric["applied"] + [{"ms": 6000, "what": "MVRP VID 2 JoinIn from a peer (planted)",
                                                     "hex": vid2_frame(JOIN_IN).hex()}], key=lambda a: a["ms"])
    return planted(fabric, "vid2-registrar-in")


Plant = Callable[[dict, dict], dict]
#: the plants of the split half's capture (--make-plant writes the planted split capture)
SPLIT_PLANTS: dict[str, Plant] = {
    "uncovered-field": plant_uncovered_field, "vanished-owed": plant_vanished_owed,
    "command-byte": plant_command_byte, "command-sequence": plant_command_sequence,
    "response-sequence": plant_response_sequence, "table-10-3": plant_table_10_3,
    "received-join": plant_received_join, "leave-all-declaration": plant_leave_all_declaration,
    "mvrp-join-in": plant_mvrp_join_in, "mvrp-received-join": plant_mvrp_received_join,
}
#: the plants of the all-fabric half's capture (--make-plant writes the planted fabric capture)
FABRIC_PLANTS: dict[str, Plant] = {
    "vanished-mvrp-leave-all": plant_vanished_mvrp_leave_all,
    "vanished-available-index": plant_vanished_available_index,
    "vanished-domain-new": plant_vanished_domain_new, "domain-trace-moved": plant_domain_trace_moved,
    "vanished-vid2-join-in": plant_vanished_vid2_join_in, "vid2-registrar-in": plant_vid2_registrar_in,
}
CAPTURE_PLANTS: dict[str, Plant] = {**SPLIT_PLANTS, **FABRIC_PLANTS}
