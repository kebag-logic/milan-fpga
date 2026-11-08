#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_compare.py - the two-placement simulation's comparison (#665).

It reads the capture each half wrote (twin_fabric.cpp, twin_split.cpp, decoded by twin_decode.py)
and compares them by #665's two-placement comparison contract:

  * ADP, ACMP and MAAP: each protocol's frames as an ordered sequence, raw bytes equal. Times are
    never compared between the halves.
  * AECP: the solicited responses as one ordered sequence, raw bytes equal; the unsolicited notices
    as ordered sub-sequences per (command_type, descriptor_type, descriptor_index), sequence_id out
    of the byte compare; the commands the entity sends (CONTROLLER_AVAILABLE) per controller, also
    with sequence_id out of the byte compare (IEEE 1722.1-2021 9.2.2.9 leaves its counter's scope
    open). Equal apart from the F5 difference ledger (LEDGER, sw/firmware/ctrl/aecp/README.md), each
    row asserting its exact fabric and split values, a row that does not hold a finding.
  * MSRP: only the declaration state, each attribute declared or not and its value, at each half's
    LeaveAll boundaries (twin_mrp.py), in order, a run of equal states one state. The event counts
    follow the transmit opportunities and the LeaveAll timer's random draw (IEEE 802.1Q-2018 10.7.4.3),
    so they are graded in each half, not compared.
  * Apart from the ledger, the owed-difference list (OWED, and OWED_GRADES for a defect one half's grade
    finds): differences a later step owes the fix of. Each row names the difference, its cause and the
    owing step and asserts its exact values, so any other difference still fails; a row whose
    difference has gone is a finding too, so the lane that fixes it deletes the row.
  * Each half on its own: what a standard leaves random or bounded against that bound (ADP's and
    MAAP's intervals, the 240 ms AEM response), the notices' sequence_id per registered controller
    (Milan v1.2 5.4.5.1), the entity's own commands' sequence_id per controller, the MRP timers (IEEE
    802.1Q-2018 10.7.4), each MSRP and MVRP attribute's events as an Applicant's (Table 10-3), and
    MVRP's VID 2 (Milan v1.2 4.3.2, 4.4.1), which is not compared across the halves.

An ADP or MAAP frame one half sent past the other's last is not a difference when the other half's
next one was not yet due at the run's end (its bound, TAIL_MS).

  twin_compare.py FABRIC.json SPLIT.json [--report OUT.json] [--report-only]
      every finding as "[DIFF] ...", "[SEQ] ...", "[MRP] ...", "[MVRP] ..." or "[TIME] ...", exit 1 on any
      (0 with --report-only, which only writes the plants' baseline)
  twin_compare.py FABRIC.json SPLIT.json --plant NAME --baseline BASE.json
      one half's capture was planted (the split's, or the fabric's for a FABRIC_PLANTS plant): exit 0 only
      when the comparison refuses it with the plant's words (PLANT_WORDS), in a finding the unplanted
      comparison (BASE.json, a --report) does not make
  twin_compare.py SPLIT.json PLANTED.json --plant NAME --self
      the control: a capture against its planted copy, every finding about the planted protocol (the
      comparison's, and each grade finding the plant adds to the planted half or takes from it)
  twin_compare.py FABRIC.json SPLIT.json --make-plant NAME --out PLANTED.json
      write a capture plant (CAPTURE_PLANTS): the planted half's capture with its planted difference
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import twin_decode as td
from twin_decode import Capture, Sent, aecp, describe, recipient, role
import twin_grades
import twin_mrp
from twin_plants import CAPTURE_PLANTS

#: a periodic frame's latest next departure, for the tail rule: ADP's advertise period and largest
#: delay (Milan v1.2 Table 5.50), MAAP's announce interval and its variation (IEEE 1722-2016 Table B.8)
TAIL_MS = {"ADP": 5000 + 4000, "MAAP": 30000 + 2000}

#: each plant's words, which its refusal against the all-fabric capture must carry
PLANT_WORDS = {
    "byte-flip": "ADP frame 1 differs at byte 34",
    "srp-plus-k": "MSRP Talker Failed stream_id 0200000000010001",
    "missing-notification": "the fabric sent and the split did not: AECP notice STOP_STREAMING 0x0005/0 "
                            "to the second controller",
    "uncovered-field": "AECP notice GET_STREAM_INFO 0x0005/0 frame 0 differs at byte 65",
    "vanished-owed": "owed row stream-output-0-notices: the difference has gone",
    "command-byte": "AECP command 0 differs at byte 33",
    "command-sequence": "the CONTROLLER_AVAILABLE commands to the second controller go from sequence_id 0 to 0",
    "response-sequence": "the first controller's CONTROLLER_AVAILABLE response at ms 52806 carries sequence_id 2, its "
                         "command's 1",
    "table-10-3": "[MRP] split MSRP Domain value 06030002: JoinMt at ms 200 is not an Applicant's message: "
                  "from AN, Table 10-3's tx! sends New",
    "received-join": "[MRP] split MSRP Domain value 06030002: JoinMt at ms 31000 is not an Applicant's message: "
                     "from AA with the Registrar IN, QA with the Registrar IN, Table 10-3's tx! sends JoinIn or "
                     "nothing",
    "leave-all-declaration": "MSRP declarations at the LeaveAll boundaries differ: the fabric's [{Domain value "
                             "06030002} x6], the split's [{Domain value 06030002} x2, {none} x3]",
    "vanished-mvrp-leave-all": "owed row fabric-mvrp-leave-all: the defect has gone",
    "vanished-available-index": "owed row entity-available-index: the difference has gone",
    "mvrp-join-in": "[MRP] split MVRP VID 0002: JoinIn at ms 212 is not an Applicant's message: from AA, Table "
                    "10-3's tx! sends JoinMt",
    "mvrp-received-join": "[MRP] split MVRP VID 0002: JoinMt at ms 31012 is not an Applicant's message: from AA with "
                          "the Registrar IN, QA with the Registrar IN, Table 10-3's tx! sends JoinIn or nothing",
    "vanished-domain-new": "owed row fabric-domain-one-new: the defect has gone",
    "domain-trace-moved": "owed row fabric-domain-one-new does not hold: the all-fabric half sent MSRP Domain value "
                          "06030002: New x1 from ms 200, JoinIn x1 from ms 1000",
    "vanished-vid2-join-in": "owed row fabric-vid2-join-in: the defect has gone",
    "vid2-registrar-in": "owed row fabric-vid2-join-in does not hold: the all-fabric half sent MVRP VID 0002: New x1 "
                         "from ms 5200, JoinIn x15 from ms 6200, Lv x1 from ms 20000; received 1 MVRPDU(s)",
}
#: the words of the control against the unplanted capture, where they differ
SELF_WORDS = {
    "vanished-owed": "the split sent and the fabric did not: AECP notice GET_STREAM_INFO 0x0006/0",
    "leave-all-declaration": "MSRP declarations at the LeaveAll boundaries differ",
    "vanished-mvrp-leave-all": "the planted half no longer makes: [MRP] all-fabric MVRP: 64799 ms from ms 10201",
    "vanished-available-index": "AECP response 13 differs at byte 81",
    "vanished-domain-new": "the planted half no longer makes: [MRP] all-fabric MSRP Domain value 06030002: JoinMt at "
                           "ms 1000",
    "domain-trace-moved": "[MRP] all-fabric MSRP Domain value 06030002: JoinIn at ms 1000 is not an Applicant's "
                          "message",
    "vanished-vid2-join-in": "the planted half no longer makes: [MRP] all-fabric MVRP VID 0002: JoinIn at ms 6200",
    "vid2-registrar-in": "[MRP] all-fabric MVRP VID 0002: JoinIn at ms 6200 is not an Applicant's message: from AN "
                         "with the Registrar IN",
}
PLANTED_PROTOCOL = {"byte-flip": "ADP", "srp-plus-k": "MSRP", "missing-notification": "AECP",
                    "uncovered-field": "AECP", "vanished-owed": "AECP", "command-byte": "AECP",
                    "command-sequence": "AECP", "response-sequence": "AECP", "table-10-3": "MSRP",
                    "received-join": "MSRP", "leave-all-declaration": "MSRP", "vanished-mvrp-leave-all": "MVRP",
                    "vanished-available-index": "AECP", "mvrp-join-in": "MVRP", "mvrp-received-join": "MVRP",
                    "vanished-domain-new": "MSRP", "domain-trace-moved": "MSRP", "vanished-vid2-join-in": "MVRP",
                    "vid2-registrar-in": "MVRP"}


# ---- the ordered raw-byte comparison ---------------------------------------

def first_byte(a: bytes, b: bytes) -> int:
    """The first byte two frames differ at (the shorter one's length when one is a prefix)."""
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))


def tail_allowed(proto: str, extra: list[Sent], other: list[Sent], run_ms: int) -> bool:
    """Unpaired trailing frames of a periodic protocol, the other half's next not yet due at the run's end."""
    if proto not in TAIL_MS or not other:
        return False
    return run_ms - other[-1].ms < TAIL_MS[proto] and extra[0].ms > other[-1].ms


@dataclass(frozen=True)
class Ordering:
    """How one sequence is compared: its name in a finding, what pairs two frames, what is compared."""

    label: str
    key: Callable[[Sent], tuple]
    body: Callable[[Sent], bytes]


def raw_ordering(proto: str) -> Ordering:
    """A protocol compared frame by frame on its message_type, raw bytes."""
    return Ordering(f"{proto} frame", lambda s: (s.data[s.at + 1] & 0x0F,), lambda s: s.data)


def compare_ordered(proto: str, fab: list[Sent], spl: list[Sent], run_ms: int,
                    order: Ordering) -> tuple[list[str], list[str]]:
    """Pair the two sequences in order by key, then compare each pair's bytes; findings and notes."""
    findings: list[str] = []
    notes: list[str] = []
    matcher = difflib.SequenceMatcher(None, [order.key(x) for x in fab], [order.key(x) for x in spl],
                                      autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                a, b = order.body(fab[i]), order.body(spl[j])
                if a != b:
                    at = first_byte(a, b)
                    findings.append(f"[DIFF] {order.label} {i} differs at byte {at} (fabric {a[at:at + 8].hex()}, "
                                    f"split {b[at:at + 8].hex()}): {describe(proto, fab[i])}")
            continue
        last = i2 == len(fab) and j2 == len(spl)
        if last and j1 == j2 and tail_allowed(proto, fab[i1:i2], spl, run_ms):
            notes.append(f"[TAIL] {proto}: the fabric's last {i2 - i1} frame(s), the split's next not yet due")
        elif last and i1 == i2 and tail_allowed(proto, spl[j1:j2], fab, run_ms):
            notes.append(f"[TAIL] {proto}: the split's last {j2 - j1} frame(s), the fabric's next not yet due")
        else:
            findings += [f"[DIFF] the fabric sent and the split did not: {describe(proto, x)}" for x in fab[i1:i2]]
            findings += [f"[DIFF] the split sent and the fabric did not: {describe(proto, x)}" for x in spl[j1:j2]]
    return findings, notes


# ---- AECP --------------------------------------------------------------------

def response_key(s: Sent) -> tuple:
    """What pairs two solicited responses: the controller, the message type, the sequence_id, the command."""
    f = aecp(s)
    return (f.controller, f.message_type, f.seq, f.command, f.descriptor)


RESPONSES = Ordering("AECP response", response_key, lambda s: s.data)
#: the commands the entity sends, paired per controller by their command, compared without their sequence_id:
#: IEEE 1722.1-2021 9.2.2.9 says only that it "is incremented on each command sent", not whether per entity or
#: per controller, so each half's is graded on its own (twin_grades.grade_commands)
COMMANDS = Ordering("AECP command", lambda s: (aecp(s).message_type, aecp(s).command), td.without_seq)


def notice_ordering(key: tuple) -> Ordering:
    """One notice sub-sequence: its frames paired by recipient, compared without their sequence_id."""
    command, pair = key
    name = td.AEM_COMMANDS.get(command, f"command {command:#06x}")
    return Ordering(f"AECP notice {name} {pair[0]:#06x}/{pair[1]} frame", lambda s: (recipient(s),), td.without_seq)


def compare_aecp(fab: list[Sent], spl: list[Sent], run_ms: int) -> tuple[list[str], list[str]]:
    """The responses in order; the notices per (command_type, descriptor) in order, sequence_id
    excluded; the entity's own commands per controller."""
    findings, notes = compare_ordered("AECP", [x for x in fab if role(x) == "response"],
                                      [x for x in spl if role(x) == "response"], run_ms, RESPONSES)
    keys = sorted({td.notice_key(x) for x in fab + spl if role(x) == "notice"})
    for key in keys:
        d, n = compare_ordered("AECP", [x for x in fab if role(x) == "notice" and td.notice_key(x) == key],
                               [x for x in spl if role(x) == "notice" and td.notice_key(x) == key], run_ms,
                               notice_ordering(key))
        findings += d
        notes += n
    for entity in sorted({recipient(x) for x in fab + spl if role(x) == "command"}):
        d, n = compare_ordered("AECP", [x for x in fab if role(x) == "command" and recipient(x) == entity],
                               [x for x in spl if role(x) == "command" and recipient(x) == entity], run_ms,
                               COMMANDS)
        findings += d
        notes += n
    return findings, notes


# ---- MSRP: the declarations at the LeaveAll boundaries -------------------------

Attributes = dict[tuple[int, str], list[str]]


def msrp_attributes(frames: list[Sent]) -> Attributes:
    """Each MSRP attribute's ordered events (its ThreePacked event, and its FourPacked one where it has
    one), whatever MRPDU and Message carried them; LeaveAll is not part of the event. The owed rows read
    them."""
    found: Attributes = {}
    for s in frames:
        for e in td.msrp_events(s)[0]:
            found.setdefault((e.kind, e.value), []).append(e.event if e.four is None else f"{e.event}/{e.four}")
    return found


def runs(states: list[str]) -> list[tuple[str, int]]:
    """A sequence of declaration states as runs, a state and how many boundaries in a row show it."""
    found: list[tuple[str, int]] = []
    for state in states:
        if found and found[-1][0] == state:
            found[-1] = (state, found[-1][1] + 1)
        else:
            found.append((state, 1))
    return found


def compare_declarations(fab: twin_mrp.Grade, spl: twin_mrp.Grade, left_out: set) -> list[str]:
    """The declaration state at each half's LeaveAll boundaries (#665), the
    attributes an owed row covers left out: the halves' sequences of states equal, a run of equal states
    one state. The boundaries are paired by the states they show, in order, never by their times or their
    count, which the LeaveAll timer's random draw sets (IEEE 802.1Q-2018 10.7.4.3)."""
    rf = runs(twin_mrp.declarations(fab, left_out))
    rs = runs(twin_mrp.declarations(spl, left_out))
    if [state for state, _ in rf] == [state for state, _ in rs]:
        return []
    return [f"[DIFF] MSRP declarations at the LeaveAll boundaries differ: the fabric's [{shown_runs(rf)}], "
            f"the split's [{shown_runs(rs)}]"]


def shown_runs(found: list[tuple[str, int]]) -> str:
    """Declaration-state runs as a finding prints them: "{Domain value 06030002} x6"."""
    return ", ".join(f"{state} x{n}" for state, n in found)


def msrp_headers(frames: list[Sent]) -> set[str]:
    """The Ethernet headers a half's MSRP frames carry."""
    return {s.data[:14].hex() for s in frames}


# ---- the F5 difference ledger and the owed-difference list -------------------

@dataclass(frozen=True)
class Half:
    """What a row reads in one half: its AECP frames, its MSRP attributes and its stimulus."""

    aecp: list[Sent]
    msrp: Attributes
    capture: Capture


@dataclass(frozen=True)
class Row:
    """One row: what it covers in a half, its clause, the exact value each half must show and how a
    finding prints what a half showed. Owed rows also name their cause and owing step."""

    name: str
    clause: str
    select: Callable[[Half], list]
    fabric: Callable[[Half, list], bool]
    split: Callable[[Half, list], bool]
    fabric_says: str
    split_says: str
    shown: Callable[[list], str]
    cause: str = ""
    owed_to: str = ""


def responses(h: Half, seq: int) -> list[Sent]:
    """The solicited responses to the first controller's command with that sequence_id."""
    return [s for s in h.aecp if role(s) == "response" and aecp(s).seq == seq
            and aecp(s).controller == 0x1111222233334444]


def notices(h: Half, command: int, pair: tuple[int, int]) -> list[Sent]:
    """The notices of one (command_type, descriptor) sub-sequence."""
    return [s for s in h.aecp if role(s) == "notice" and td.notice_key(s) == (command, pair)]


def stimulus(h: Half, seq: int) -> bytes:
    """The first controller's command with that sequence_id, as applied: its bytes after the sequence_id,
    to its control_data_length."""
    d = next(a.data for a in h.capture.applied if a.data[14] == 0xFB and a.data[15] & 1 == 0
             and int.from_bytes(a.data[26:34], "big") == 0x1111222233334444
             and int.from_bytes(a.data[34:36], "big") == seq)
    return d[36:26 + ((d[16] & 0x07) << 8 | d[17])]


def body(s: Sent) -> bytes:
    """A PDU's bytes after its sequence_id, to its control_data_length."""
    return s.data[s.at + 22:s.at + 12 + td.control_length(s)]


def shown_aecp(frames: list) -> str:
    """AECP frames as a finding prints them."""
    return "[" + "; ".join(f"{td.command_name(aecp(s))} to {td.who(recipient(s))} status {aecp(s).status} "
                           f"{body(s).hex()}" for s in frames) + "]"


def shown_msrp(attributes: list) -> str:
    """MSRP attributes as a finding prints them."""
    return "[" + "; ".join(f"MSRP {td.attribute_label(*k)}: {td.run_length(v)}" for k, v in attributes) + "]"


FIRST, SECOND = 0x1111222233334444, 0x2222333344445555
MVU = td.MVU_PROTOCOL
SYSTEM_UNIQUE_ID = bytes.fromhex("0102030405060708")


def configuration(s: Sent) -> int:
    """A READ_DESCRIPTOR PDU's configuration_index (IEEE 1722.1-2021 7.4.5.1)."""
    return int.from_bytes(s.data[s.at + 24:s.at + 26], "big")


def statuses(frames: list[Sent]) -> list[tuple[int, int]]:
    """Each frame's message_type and status."""
    return [(aecp(s).message_type, aecp(s).status) for s in frames]


def current_fields(h: Half, before_ms: int) -> bytes | None:
    """STREAM_INPUT 0's current stream info: its last GET_STREAM_INFO notice's fields before `before_ms`."""
    found = [s for s in notices(h, 0x000F, (5, 0)) if s.ms <= before_ms]
    return td.stream_info(found[-1]) if found else None


def holds_current(h: Half, sel: list[Sent]) -> bool:
    """One NOT_SUPPORTED response whose fields are STREAM_INPUT 0's current stream info (its last notice's,
    over the notice's shorter length), then zero."""
    current = current_fields(h, sel[0].ms) if len(sel) == 1 else None
    fields = td.stream_info(sel[0]) if sel else b""
    return statuses(sel) == [(1, 11)] and current is not None and fields[:len(current)] == current \
        and not any(fields[len(current):])


#: The F5 difference ledger (sw/firmware/ctrl/aecp/README.md, Observed difference rows 1 to 4, the
#: Non-AEM contract's reserved type and HDCP_APM): the stimulus reaches every row (twin.hpp), and each
#: asserts its exact values (#665): a row no stimulus reaches is unproven. Rows 5 (the started state's
#: GET_STREAM_INFO notice) and 6 (the release notice's UNLOCK flag) are not rows: at this processor pin
#: the fabric sends both as the split does, and the ledger records only real differences, so the
#: notice comparison holds them equal.
LEDGER = (
    Row("root-configuration-index", "IEEE 1722.1-2021 7.4.5.1/2; aecp/README.md, Observed difference row 1",
        lambda h: responses(h, 11),
        lambda h, sel: [(aecp(s).status, configuration(s), aecp(s).descriptor) for s in sel] == [(7, 1, (0, 0))],
        lambda h, sel: [(aecp(s).status, configuration(s), aecp(s).descriptor) for s in sel] == [(0, 0, (0, 0))],
        "one response, BAD_ARGUMENTS, the received configuration_index 1",
        "one response, SUCCESS, the ENTITY descriptor at configuration_index 0", shown_aecp),
    Row("set-stream-info-current-fields", "IEEE 1722.1-2021 7.4.15.1; aecp/README.md, Observed difference row 2",
        lambda h: responses(h, 12),
        lambda h, sel: statuses(sel) == [(1, 11)] and td.stream_info(sel[0]) == bytes(80),
        holds_current,
        "one response, NOT_SUPPORTED, the command's fields echoed (all zero)",
        "one response, NOT_SUPPORTED, STREAM_INPUT 0's current fields (its last GET_STREAM_INFO notice's)",
        shown_aecp),
    Row("system-unique-id", "Milan v1.2 5.4.4.2/3; aecp/README.md, Observed difference row 3",
        lambda h: responses(h, 18) + responses(h, 19),
        lambda h, sel: statuses(sel) == [(7, 1), (7, 1)]
        and [body(s) for s in sel] == [stimulus(h, 18), stimulus(h, 19)],
        lambda h, sel: statuses(sel) == [(7, 0), (7, 0)]
        and [body(s) for s in sel] == [MVU + bytes.fromhex(f"000{c}0000") + SYSTEM_UNIQUE_ID for c in (1, 2)],
        "SET and GET_SYSTEM_UNIQUE_ID each refused NOT_IMPLEMENTED, the command echoed",
        "SET_SYSTEM_UNIQUE_ID SUCCESS and GET_SYSTEM_UNIQUE_ID SUCCESS, each with system_unique_id "
        "0102030405060708", shown_aecp),
    Row("default-format-override-notice", "Milan v1.2 5.4.5.2; aecp/README.md, Observed difference row 4",
        lambda h: notices(h, 0x0008, (5, 0)),
        lambda h, sel: sel == [],
        lambda h, sel: [(recipient(s), aecp(s).status, s.data[s.at + 28:s.at + 36]) for s in sel]
        == [(SECOND, 0, bytes.fromhex("0205022002006000"))],
        "no SET_STREAM_FORMAT notice for the default-valued SET",
        "one SET_STREAM_FORMAT notice of STREAM_INPUT 0's format to the second controller", shown_aecp),
    Row("reserved-message-type", "IEEE 1722.1-2021 Table 9-1, 9.2.2.4; aecp/README.md, Non-AEM contract",
        lambda h: responses(h, 14),
        lambda h, sel: statuses(sel) == [(11, 1)],
        lambda h, sel: sel == [],
        "one frame, message_type 11, status 1", "nothing", shown_aecp),
    Row("hdcp-apm-data", "IEEE 1722.1-2021 9.7.4; aecp/README.md, Non-AEM contract",
        lambda h: responses(h, 22),
        lambda h, sel: statuses(sel) == [(9, 1)] and [body(s) for s in sel] == [stimulus(h, 22)],
        lambda h, sel: statuses(sel) == [(9, 1)] and [body(s) for s in sel] == [bytes(6)],
        "HDCP_APM_RESPONSE NOT_IMPLEMENTED echoing the HDCP data and its length",
        "HDCP_APM_RESPONSE NOT_IMPLEMENTED with no HDCP data, its flags and fragment offset kept", shown_aecp),
)

#: the ENTITY descriptor's available_index in a READ_DESCRIPTOR response: the descriptor follows the
#: configuration_index and its reserved octets (IEEE 1722.1-2021 7.4.5.2), the field at its octet 36 (Table
#: 7-2: "the same as the available_index field in ATDECC Discovery Protocol", 6.2.2.15)
AVAILABLE_INDEX_AT = 28 + 36


def available_index(s: Sent) -> int:
    """The available_index of a READ_DESCRIPTOR response's ENTITY descriptor."""
    return int.from_bytes(s.data[s.at + AVAILABLE_INDEX_AT:s.at + AVAILABLE_INDEX_AT + 4], "big")


def but_available_index(s: Sent) -> bytes:
    """A READ_DESCRIPTOR response after its sequence_id, its ENTITY descriptor's available_index left out."""
    d, k = body(s), AVAILABLE_INDEX_AT - 22
    return d[:k] + d[k + 4:]


def advertised(h: Half, before_ms: int) -> list[int]:
    """The available_index of each ENTITY_AVAILABLE the half sent before `before_ms` (IEEE 1722.1-2021 6.2.2.15)."""
    return [int.from_bytes(s.data[s.at + 36:s.at + 40], "big") for s in h.capture.frames.get("ADP", [])
            if s.data[s.at + 1] & 0x0F == 0 and s.ms < before_ms]


def entity_read(h: Half, sel: list[Sent], index: int) -> bool:
    """One SUCCESS response to the later ENTITY read, after exactly two ENTITY_AVAILABLE (available_index 0
    and 1): the ENTITY descriptor the first read returned (the response comparison holds that one equal
    across the halves), with available_index `index`."""
    first = responses(h, 2)
    return (statuses(sel) == [(1, 0)] and len(first) == 1 and available_index(sel[0]) == index
            and but_available_index(sel[0]) == but_available_index(first[0]) and advertised(h, sel[0].ms) == [0, 1])


#: STREAM_OUTPUT 0's GET_STREAM_INFO fields as the fabric notifies them: its talker declared after the
#: PROBE_TX (stream_id, accumulated latency, the MAAP address, VLAN 2), and withdrawn about 15 s later
OUT0_DECLARED = bytes.fromhex("f2000000" "0205022002006000" "0200000000010000" "001e8480" "91e0f0000100" "00" "00"
                              "0000000000000000" "0002" "0000" "00000000" "00" "000000").hex()
OUT0_WITHDRAWN = bytes.fromhex("a0000000" "0205022002006000" "0000000000000000" "001e8480" "000000000000" "00" "00"
                               "0000000000000000" "0000" "0000" "00000000" "00" "000000").hex()
#: the Talker attributes each half declares (IEEE 802.1Q-2018 Table 35-1, 35.2.2.8): the fabric's Talker
#: Advertise for source 0, the split's Talker Failed for both sources
FABRIC_TALKER = (1, "020000000001000091e0f00001000002004900017000000000")
SPLIT_TALKERS = ((2, "0200000000010000000000000000000200d900017000000000000002000000000102"),
                 (2, "02000000000100010000000000000002001d00017000000000000002000000000102"))
SRP_ADAPTER = ("the split's talker declaration state never changes: no SRP adapter entry takes MAAP's "
               "allocation (sw/firmware/ctrl/plat/README.md, Not yet done)")
SRP_ROUND = "the SRP adapter entry that takes MAAP's allocation (#665)"
FABRIC_INDEX = ("the fabric's AECP engine serves the AEM image's ENTITY descriptor, whose available_index is the "
                "image's constant 0, and never reads ADP's")

#: The owed-difference list, apart from the ledger (#665): each row names the
#: difference, its cause and the step that owes the fix, and asserts its exact values in both halves.
OWED = (
    Row("stream-output-0-notices", "Milan v1.2 5.4.5.2, Table 5.22: the talker declaration state changed",
        lambda h: notices(h, 0x000F, (6, 0)),
        lambda h, sel: [(recipient(s), td.stream_info(s).hex()) for s in sel]
        == [(FIRST, OUT0_DECLARED), (SECOND, OUT0_DECLARED), (FIRST, OUT0_WITHDRAWN), (SECOND, OUT0_WITHDRAWN)],
        lambda h, sel: sel == [],
        "GET_STREAM_INFO notices of STREAM_OUTPUT 0 to both controllers as its talker declares after the "
        "PROBE_TX and as it withdraws", "none", shown_aecp, SRP_ADAPTER, SRP_ROUND),
    Row("split-talker-failed", "IEEE 802.1Q-2018 35.2.2.8; Milan v1.2 4.3.3: a talker's declaration",
        lambda h: [(k, v) for k, v in sorted(h.msrp.items()) if k[0] in (1, 2)],
        lambda h, sel: [(k, td.run_length(v)) for k, v in sel]
        == [(FABRIC_TALKER, "New x2, JoinMt x15, Lv x1, Mt x5")],
        lambda h, sel: [(k, td.run_length(v)) for k, v in sel]
        == [(SPLIT_TALKERS[0], "New x2, JoinMt x89"), (SPLIT_TALKERS[1], "New x2, JoinMt x89")],
        "Talker Advertise for STREAM_OUTPUT 0's stream from the PROBE_TX until it withdraws",
        "Talker Failed for both sources' streams from boot, never withdrawn", shown_msrp, SRP_ADAPTER,
        SRP_ROUND),
    Row("entity-available-index",
        "IEEE 1722.1-2021 Table 7-2, 6.2.2.15: ENTITY's available_index, the last ENTITY_AVAILABLE's",
        lambda h: responses(h, 25),
        lambda h, sel: entity_read(h, sel, 0),
        lambda h, sel: entity_read(h, sel, 1),
        "the ENTITY descriptor with available_index 0 after the ENTITY_AVAILABLE that carried 1",
        "the ENTITY descriptor with available_index 1, its last ENTITY_AVAILABLE's", shown_aecp, FABRIC_INDEX,
        "#858 (a release-image defect)"),
)


@dataclass(frozen=True)
class GradeRow:
    """An owed defect one half's grade finds: the half, the grade findings the row covers, the exact behaviour
    it asserts, its cause and the step that owes the fix. A row whose findings have gone is a finding, so the
    lane that fixes the defect deletes the row."""

    name: str
    clause: str
    placement: str
    covers: Callable[[str], bool]
    shown: Callable[[Capture], str]
    says: str
    cause: str
    owed_to: str


def mvrp_shown(cap: Capture) -> str:
    """A half's MVRP as the #857 row reads it: each LeaveAll's millisecond, and its last MRPDU's events."""
    frames = cap.frames.get("MVRP", [])
    if not frames:
        return "no MVRPDU"
    events = ", ".join(f"VID {e.value} {e.event}" for e in td.mvrp_events(frames[-1])[0])
    return (f"MVRP LeaveAll at ms {[s.ms for s in frames if td.mvrp_events(s)[1]]}, its last MVRPDU at ms "
            f"{frames[-1].ms} ({events})")


#: The fabric's MVRP as #857 has it: one LeaveAll, then VID 2's Lv at 20 s and no PDU after it
FABRIC_MVRP = "MVRP LeaveAll at ms [10201], its last MVRPDU at ms 20000 (VID 0002 Lv)"
#: The two attributes #860 has: the Domain the halves declare (Milan v1.2 4.2.7.2.1) and VID 2, its VLAN
DOMAIN_KEY, VID2_KEY = (4, "06030002"), (1, "0002")
#: The fabric's Domain as #860 has it: one New at 200 ms, then JoinMt at every periodic and LeaveAll, with no
#: MSRPDU received; and its VID 2: one New at 5200 ms, then JoinIn from 6200 ms with no MVRPDU received
FABRIC_DOMAIN = ("MSRP Domain value 06030002: New x1 from ms 200, JoinMt x79 from ms 1000; received no MSRPDU, its "
                 "Registrar MT throughout")
FABRIC_VID2 = ("MVRP VID 0002: New x1 from ms 5200, JoinIn x15 from ms 6200, Lv x1 from ms 20000; received no MVRPDU, "
               "its Registrar MT throughout")
ONE_NEW = "#860 (a release-image defect)"


def applicant_findings(application: str, key: tuple[int, str]) -> Callable[[str], bool]:
    """Whether a grade finding is the all-fabric half's Table 10-3 finding of one attribute."""
    head = f"[MRP] all-fabric {application} {twin_mrp.label_of(application, key)}: "
    return lambda f: f.startswith(head)


def traced(application: str, key: tuple[int, str]) -> Callable[[Capture], str]:
    """A half's messages for one attribute, as an owed grade row asserts them (twin_mrp.trace_shown)."""
    return lambda cap: twin_mrp.trace_shown(cap, application, key)


#: The owed defects a half's grade finds (#857, #860), apart from the differences OWED holds: each covers its
#: grade findings while the half shows exactly the behaviour it asserts.
OWED_GRADES = (
    GradeRow("fabric-mvrp-leave-all",
             "IEEE 802.1Q-2018 10.7.9, 10.7.4.3; Milan v1.2 Table 4.3: a full participant's LeaveAll, declaring "
             "or not", "all-fabric",
             lambda f: f.startswith("[MRP] all-fabric MVRP: ") and "to the next LeaveAll" in f, mvrp_shown,
             FABRIC_MVRP, "the fabric's MVRP participant sends nothing, LeaveAll included, once it declares nothing",
             "#857 (a release-image defect)"),
    GradeRow("fabric-domain-one-new",
             "IEEE 802.1Q-2018 Table 10-3: from AN, tx! sends New again; Milan v1.2 4.2.7.2.1: the Domain declared "
             "after startup", "all-fabric", applicant_findings("MSRP", DOMAIN_KEY), traced("MSRP", DOMAIN_KEY),
             FABRIC_DOMAIN, "the fabric's Domain participant queues one New at startup and at LINK_UP, then re-joins "
             "(KL_srp_domain.sv)", ONE_NEW),
    GradeRow("fabric-vid2-join-in",
             "IEEE 802.1Q-2018 Table 10-3, 10.7.6.3: from AN, tx! sends New again, and sJ sends JoinIn only with "
             "the Registrar IN", "all-fabric", applicant_findings("MVRP", VID2_KEY), traced("MVRP", VID2_KEY),
             FABRIC_VID2, "the fabric's MVRP participant declares a VID with one New, then re-joins it on every "
             "periodic and LeaveAll tick with JoinIn, the only Join it sends (KL_srp_vlan.sv)", ONE_NEW),
)


def apply_grade_rows(cap: Capture, findings: list[str]) -> tuple[list[str], list[str]]:
    """Each owed grade row of one half: while it holds, the findings it covers are taken out. The half's
    remaining grade findings, with any the rows make, and the notes."""
    rest, notes = list(findings), []
    for row in (r for r in OWED_GRADES if r.placement == cap.placement):
        covered = [f for f in findings if row.covers(f)]
        if not covered:
            rest.append(f"[DIFF] owed row {row.name}: the defect has gone, the {cap.placement} half's grade finds "
                        f"none of it; the lane that fixed it ({row.owed_to}) deletes the row")
        elif row.shown(cap) == row.says:
            rest = [f for f in rest if f not in covered]
            notes.append(f"[OWED] {row.name}: the {cap.placement} half sends {row.says} ({row.clause}; "
                         f"cause: {row.cause}; owed to {row.owed_to})")
        else:
            rest.append(f"[DIFF] owed row {row.name} does not hold: the {cap.placement} half sent {row.shown(cap)} "
                        f"(the row: {row.says})")
    return rest, notes


def apply_rows(rows: tuple[Row, ...], fab: Half, spl: Half, owed: bool) -> tuple[list, list, list[str], list[str]]:
    """Check each row in both halves and take what it covers out of them; the remaining AECP frames,
    the remaining MSRP attributes, the notes and the findings."""
    notes: list[str] = []
    findings: list[str] = []
    covered_f: list = []
    covered_s: list = []
    kind = "owed row" if owed else "AECP ledger row"
    for row in rows:
        f, s = row.select(fab), row.select(spl)
        covered_f += f
        covered_s += s
        if owed and normalized(f) == normalized(s):
            findings.append(f"[DIFF] {kind} {row.name}: the difference has gone, both halves send "
                            f"{row.shown(f)}; the lane that fixed it ({row.owed_to}) deletes the row")
        elif row.fabric(fab, f) and row.split(spl, s):
            tail = f"; cause: {row.cause}; owed to {row.owed_to}" if owed else ""
            notes.append(f"[{'OWED' if owed else 'LEDGER'}] {row.name}: the fabric sends {row.fabric_says}, "
                         f"the split {row.split_says} ({row.clause}{tail})")
        else:
            findings.append(f"[DIFF] {kind} {row.name} does not hold: the fabric sent {row.shown(f)} (the row: "
                            f"{row.fabric_says}), the split {row.shown(s)} (the row: {row.split_says})")
    rest_f = [x for x in fab.aecp if not any(x is y for y in covered_f)]
    rest_s = [x for x in spl.aecp if not any(x is y for y in covered_s)]
    return rest_f, rest_s, notes, findings


def normalized(items: list) -> list:
    """A row's selection as two halves could share it: notices without their sequence_id."""
    return [td.without_seq(x) if isinstance(x, Sent) else x for x in items]


# ---- the verdict --------------------------------------------------------------

def compare_rows(hf: Half, hs: Half) -> tuple[list[Sent], list[Sent], set, list[str], list[str]]:
    """The ledger and the owed rows between the placements: the AECP frames no row covers, the MSRP attributes
    an owed row covers, the notes and the findings."""
    aecp_f, aecp_s, notes, findings = apply_rows(LEDGER, hf, hs, owed=False)
    aecp_f, aecp_s, n, d = apply_rows(OWED, Half(aecp_f, hf.msrp, hf.capture), Half(aecp_s, hs.msrp, hs.capture),
                                      owed=True)
    owed_msrp = {x[0] for row in OWED for x in row.select(hf) + row.select(hs) if not isinstance(x, Sent)}
    return aecp_f, aecp_s, owed_msrp, notes + n, findings + d


def compare(fab: Capture, spl: Capture, between_placements: bool = True) -> dict:
    """Every finding and note of the two captures. The ledger, the owed lists and each half's grades are the
    two placements' comparison's. The plants' control compares a half with its own planted copy, and adds each
    grade finding the plant gives the planted half or takes from it."""
    findings: list[str] = []
    notes: list[str] = []
    run_ms = min(fab.run_ms, spl.run_ms)
    for proto in ("ADP", "ACMP", "MAAP"):
        d, n = compare_ordered(proto, fab.frames.get(proto, []), spl.frames.get(proto, []), run_ms,
                               raw_ordering(proto))
        findings += d
        notes += n
    hf = Half(fab.frames.get("AECP", []), msrp_attributes(fab.frames.get("MSRP", [])), fab)
    hs = Half(spl.frames.get("AECP", []), msrp_attributes(spl.frames.get("MSRP", [])), spl)
    aecp_f, aecp_s, owed_msrp = hf.aecp, hs.aecp, set()
    if between_placements:
        aecp_f, aecp_s, owed_msrp, n, d = compare_rows(hf, hs)
        notes += n
        findings += d
    d, n = compare_aecp(aecp_f, aecp_s, run_ms)
    findings += d
    notes += n
    findings += compare_declarations(twin_mrp.grade(fab), twin_mrp.grade(spl), owed_msrp)
    if msrp_headers(fab.frames.get("MSRP", [])) != msrp_headers(spl.frames.get("MSRP", [])):
        findings.append("[DIFF] MSRP: the halves' frames carry different Ethernet headers")
    (gf, mf), (gs, ms) = twin_grades.grade(fab), twin_grades.grade(spl)
    measured = {}
    if between_placements:
        for cap, graded, m in ((fab, gf, mf), (spl, gs, ms)):
            rest, n = apply_grade_rows(cap, graded)
            findings += rest
            notes += n
            measured[cap.placement] = m
    else:
        findings += [f for f in gs if f not in gf]
        findings += [f"[GRADE] the planted half no longer makes: {f}" for f in gf if f not in gs]
    return {"findings": findings, "notes": notes, "measured": measured,
            "counts": {c.placement: {p: len(v) for p, v in sorted(c.frames.items())} for c in (fab, spl)}}


def plant_verdict(report: dict, name: str, baseline: list[str] | None) -> int:
    """0 when the plant is refused by its words, in a finding the baseline does not make (or, for --self, with
    every finding about the planted protocol)."""
    words = PLANT_WORDS[name] if baseline is not None else SELF_WORDS.get(name, PLANT_WORDS[name])
    hits = [f for f in report["findings"] if words in f]
    if baseline is None:
        ok = bool(hits) and all(PLANTED_PROTOCOL[name] in f for f in report["findings"])
    else:
        ok = any(h not in baseline for h in hits)
    print(f"plant {name}: {'REFUSED' if ok else 'ESCAPED'} by \"{words}\"")
    return 0 if ok else 1


def main() -> int:
    """Compare two captures, grade a plant, or write a capture plant."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("fabric", type=Path)
    parser.add_argument("split", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--plant", choices=sorted(PLANT_WORDS))
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--self", dest="self_control", action="store_true")
    parser.add_argument("--make-plant", choices=sorted(CAPTURE_PLANTS))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--report-only", action="store_true",
                        help="write the report and exit 0: the plants' baseline, whose verdict is make twin's")
    args = parser.parse_args()
    if args.make_plant:
        planted = CAPTURE_PLANTS[args.make_plant](json.loads(args.fabric.read_text()),
                                                 json.loads(args.split.read_text()))
        args.out.write_text(json.dumps(planted) + "\n")
        print(f"plant {args.make_plant}: written to {args.out.name}")
        return 0
    fab, spl = td.load(args.fabric), td.load(args.split)
    report = compare(fab, spl, between_placements=not args.self_control)
    for line in report["notes"] + report["findings"]:
        print(line)
    if args.report:
        args.report.write_text(json.dumps(report, indent=1) + "\n")
    if args.plant:
        base = None if args.self_control else json.loads(args.baseline.read_text())["findings"]
        return plant_verdict(report, args.plant, base)
    print(f"twin: {len(report['findings'])} finding(s); counts {report['counts']}")
    return 1 if report["findings"] and not args.report_only else 0


if __name__ == "__main__":
    sys.exit(main())
