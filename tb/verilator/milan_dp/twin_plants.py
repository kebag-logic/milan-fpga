#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_plants.py - the two-placement simulation's capture plants (#665).

Each plant writes a copy of one half's capture (twin.hpp Capture) with one planted difference, which
twin_compare.py must refuse by the plant's words (twin_compare.PLANT_WORDS), against the unplanted capture
and between the placements (make twin-plants). SPLIT_PLANTS plant the split half's capture and FABRIC_PLANTS
the all-fabric half's: an owed defect of the fabric gone is planted where the fix would land.

Each plant names the grade or row it is the plant of:
  * uncovered-field: a difference no row covers; OWED holds no row at this head, so none plants one gone;
  * output-dest-mac-zero: #943's defect back, the split's declared STREAM_OUTPUT 0 notices with stream_dest_mac 0,
    which the notice comparison refuses since its owed row went;
  * output-notice-dropped: the split's STREAM_OUTPUT 0 notices dropped (#936), which the notice comparison refuses;
  * command-byte: the entity's own commands are still byte-compared, sequence_id aside;
  * command-sequence, response-sequence: the commands' sequence_id per controller (grade_commands);
  * table-10-3, received-join: an MSRP attribute's trace against Table 10-3, and through a received MRPDU,
    against its Registrar (twin_mrp.py);
  * mvrp-join-in, mvrp-received-join: the same grade of an MVRP attribute, the split's VID 2 (#665);
  * leave-all-declaration: the declaration state at the LeaveAll boundaries (compare_declarations);
  * talker-failed-back: the same comparison of the Talker declarations, which no owed row holds since #895
    (#929): the split's Talker Advertise declared as Talker Failed again;
  * leave-all-omission: a LeaveAll frame that leaves out a declared attribute, against Table 10-3's txLA!
    (twin_mrp.py);
  * FABRIC_PLANTS is empty: the owed fabric defects whose fixes its plants landed (#857, #858, #860) are
    fixed at processor 801ef228 (#893), and their rows are gone.
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
#: a Talker Advertise FirstValue's octets (IEEE 802.1Q-2018 35.2.2.8.1: StreamID, DataFrameParameters, TSpec,
#: PriorityAndRank, AccumulatedLatency)
TALKER_ADVERTISE_BYTES = 25


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


def output_notices(doc: dict) -> list[dict]:
    """A capture's GET_STREAM_INFO notices of STREAM_OUTPUT 0, in send order."""
    return [e for e in doc["frames"] if (f := aecp_doc_frame(e)) and f.unsolicited
            and (f.command, f.descriptor) == (0x000F, (6, 0))]


#: a GET_STREAM_INFO notice's frame octets: the first of its flags (STREAM_DEST_MAC_VALID, 0x10, in it) and its
#: stream_dest_mac (Milan v1.2 Figure 5.1, after the AECPDU's 38 octets through command_type)
FLAGS_AT, DEST_MAC_AT = 42, 66


def plant_output_dest_mac_zero(fabric: dict, split: dict) -> dict:
    """#943's defect back: the split capture's declared GET_STREAM_INFO notices of STREAM_OUTPUT 0 with
    stream_dest_mac 0 and STREAM_DEST_MAC_VALID kept, as the split sent them before its firmware answered the
    Talker's MAAP address."""
    del fabric
    declared = [e for e in output_notices(split) if bytes.fromhex(e["hex"])[FLAGS_AT] & 0x10]
    if not declared:
        raise SystemExit("plant output-dest-mac-zero: the split capture has no declared STREAM_OUTPUT 0 notice")
    for entry in declared:
        for at in range(DEST_MAC_AT, DEST_MAC_AT + 6):
            set_byte(entry, at, 0)
    return planted(split, "output-dest-mac-zero")


def plant_output_notice_dropped(fabric: dict, split: dict) -> dict:
    """#936's defect back: the split capture with no GET_STREAM_INFO notice of STREAM_OUTPUT 0, as the split sent
    none when its Talker declared and withdrew."""
    del fabric
    dropped = output_notices(split)
    if not dropped:
        raise SystemExit("plant output-notice-dropped: the split capture has no STREAM_OUTPUT 0 notice to drop")
    split["frames"] = [e for e in split["frames"] if not any(e is x for x in dropped)]
    return planted(split, "output-notice-dropped")


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


def plant_leave_all_omission(fabric: dict, split: dict) -> dict:
    """The split's first MSRP LeaveAll frame at or after 20000 ms that carries the declared Domain, its Domain
    value's vector taken out and the Message's AttributeListLength shortened, its LeaveAll kept: a txLA! that
    sends nothing for a declared attribute, which Table 10-3 allows only from a state whose txLA! action is
    none or bracketed (IEEE 802.1Q-2022 10.7.5.8), the frame having room for the value (10.7.5.9; twin_mrp.py)."""
    del fabric
    for entry in split["frames"]:
        found = frame_fields(entry)
        if found is None or found[0] != "MSRP" or entry["ms"] < 20000 or 4 not in td.msrp_frame(found[1])[1]:
            continue
        data = bytearray(bytes.fromhex(entry["hex"]))
        message = found[1].at + 1
        for kind, vector, packed in msrp_vectors(found[1].data, found[1].at):
            while message + 4 + int.from_bytes(data[message + 2:message + 4], "big") <= vector:
                message += 4 + int.from_bytes(data[message + 2:message + 4], "big")
            if kind == 4 and data[vector + 2:vector + 6] == DOMAIN and data[vector + 1] == 1 and data[vector] < 0x20:
                size = packed + 1 - vector  # its VectorHeader, the value and one ThreePackedEvents octet
                listed = int.from_bytes(data[message + 2:message + 4], "big")
                data[message + 2:message + 4] = (listed - size).to_bytes(2, "big")
                del data[vector:vector + size]
                entry["hex"] = bytes(data).hex()
                return planted(split, "leave-all-omission")
    raise SystemExit("plant leave-all-omission: no split MSRP LeaveAll frame carrying the Domain after 20000 ms")


def plant_talker_failed_back(fabric: dict, split: dict) -> dict:
    """The split's Talker declared as Talker Failed again, as before #895: every Message of Talker Advertise
    vectors re-encoded in place as Talker Failed of the same StreamIDs and events, each FirstValue followed by
    FailureInformation, the split's MAC as system identifier and code 2 (IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6),
    and its AttributeLength and AttributeListLength grown by it (10.8.1.2)."""
    del fabric
    planted_any = False
    for entry in split["frames"]:
        found = frame_fields(entry)
        if found is None or found[0] != "MSRP":
            continue
        raw = bytes.fromhex(entry["hex"])
        data, offset = bytearray(raw), found[1].at + 1
        while offset + 4 <= len(data) and data[offset:offset + 2] != b"\0\0":
            listed = int.from_bytes(data[offset + 2:offset + 4], "big")
            if data[offset] == 1 and data[offset + 1] == TALKER_ADVERTISE_BYTES:
                failure = bytes(2) + raw[6:12] + bytes([2])
                vector, end, grown = offset + 4, offset + 4 + listed, 0
                while vector + 2 <= end + grown and data[vector:vector + 2] != b"\0\0":
                    count = int.from_bytes(data[vector:vector + 2], "big") & 0x1FFF
                    at = vector + 2 + TALKER_ADVERTISE_BYTES
                    data[at:at] = failure
                    grown += len(failure)
                    vector = at + len(failure) + (count + 2) // 3
                data[offset], data[offset + 1] = 2, TALKER_ADVERTISE_BYTES + len(failure)
                data[offset + 2:offset + 4] = (listed + grown).to_bytes(2, "big")
                listed += grown
                planted_any = True
            offset += 4 + listed
        entry["hex"] = bytes(data).hex()
    if not planted_any:
        raise SystemExit("plant talker-failed-back: the split declared no Talker Advertise")
    return planted(split, "talker-failed-back")


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


Plant = Callable[[dict, dict], dict]
#: the plants of the split half's capture (--make-plant writes the planted split capture)
SPLIT_PLANTS: dict[str, Plant] = {
    "uncovered-field": plant_uncovered_field, "output-dest-mac-zero": plant_output_dest_mac_zero,
    "output-notice-dropped": plant_output_notice_dropped,
    "command-byte": plant_command_byte, "command-sequence": plant_command_sequence,
    "response-sequence": plant_response_sequence, "table-10-3": plant_table_10_3,
    "received-join": plant_received_join, "leave-all-declaration": plant_leave_all_declaration,
    "leave-all-omission": plant_leave_all_omission, "talker-failed-back": plant_talker_failed_back,
    "mvrp-join-in": plant_mvrp_join_in, "mvrp-received-join": plant_mvrp_received_join,
}
#: the plants of the all-fabric half's capture (--make-plant writes the planted fabric capture): none at this
#: head, since no owed fabric defect is left to plant the fix of (processor 801ef228, #893, fixed #857, #858, #860)
FABRIC_PLANTS: dict[str, Plant] = {}
CAPTURE_PLANTS: dict[str, Plant] = {**SPLIT_PLANTS, **FABRIC_PLANTS}
