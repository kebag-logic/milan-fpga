#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_mrp.py - the two-placement simulation's MRP Applicant grade, MSRP and MVRP (#665).

Each MSRP and MVRP attribute a half sends is graded on its own, as a trace an Applicant can make
(#665): IEEE 802.1Q-2018 Table 10-3
with its notes, the application's Registrar (REGISTRAR: Table 10-4, and for the MSRP application the cell
Milan v1.2 4.2.7.2.2 changes, IN / rLv! -> MT at once in place of LV), and the operPointToPointMAC the
half configures (OPER_P2P). The halves' event counts are not compared: they follow the transmit
opportunities and the LeaveAll timer's random draw (10.7.4.3). For MSRP the comparison compares only the
declaration state (declared or not, and the value) at each half's LeaveAll boundaries, which this grade
derives; MVRP is graded in each half and not compared.

What the grade reads, per attribute (its type and FirstValue):
  * each frame the half sent of the application. A frame carrying a LeaveAll is a txLA! (IEEE 802.1Q-2022
    10.7.5.8) for every attribute it carries and no rLA! for its Applicant: the Applicant takes its own
    LeaveAll as one event of Table 10-3, and the sLA's rLA! reaches only the Registrar (10.7.6.6, Table 10-4),
    where it changes nothing txLA! has not. An attribute such a frame does not carry took either txLA!,
    which sends nothing only from a state whose txLA! action is none or bracketed, or txLAF! (10.7.5.9), which
    sends nothing from any state, but only where the frame is full: where the smallest vector the value could
    add (MRPDU_ROOM, full()) would not fit. Any other frame is a tx! for each attribute it carries, sending
    the message the frame shows.
  * each frame of the stimulus of the application, as received: its events (rNew! to rLv!), and rLA! for
    a LeaveAll of the attribute's type (10.7.5.13 to 10.7.5.20).
  * between them, periodic! and leavetimer!, which are not on the wire, as often as a trace needs.
  * the MAD Service User's requests (10.7.5.4 to 10.7.5.6), also not on the wire, only where the
    attribute's next message shows one: a New! before a New, a Join! before a declaration's first Join
    (the attribute's first message, or one after a Lv, In or Mt), a Lv! before a Lv. A declaration
    withdrawn and made again with no Lv between them would be its application changing its mind unseen,
    which nothing in the stimulus causes (Milan v1.2 4.2.7.2.1: a Domain is declared after startup or a
    Link Up, and changed for a received Domain).

A frame without a LeaveAll is a tx! only for the attributes it carries, so a value one leaves out, full or
not, is graded at its next message. Re-declare! and Flush! are a Bridge's port-role events (10.7.5.2, 10.7.5.3) and do not arise at an end station. The
Registrar reaches a message only through IN against MT or LV (10.7.6.3, 10.7.6.5; note 8), so Milan's cell
changes no message an Applicant may send; it is applied as written all the same, to MSRP's Registrar only.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import twin_decode as td
from twin_decode import Capture, Sent

#: Table 10-3's columns, in the order the standard prints them
STATES = ("VO", "VP", "VN", "AN", "AA", "QA", "LA", "AO", "QO", "AP", "QP", "LO")
#: the states in which the Participant declares the attribute: every state but the Observers, LA and LO
DECLARING = frozenset({"VP", "VN", "AN", "AA", "QA", "AP", "QP"})
REGISTRARS = ("IN", "LV", "MT")


def _row(cells: str) -> dict[str, str]:
    """One row of Table 10-3 as the standard prints it, one cell per state in STATES order; "-" is the
    table's no transition."""
    return {state: cell for state, cell in zip(STATES, cells.split(), strict=True) if cell != "-"}


#: IEEE 802.1Q-2018 Table 10-3: every event that sends nothing, and where it takes each state (notes 4 and
#: 5 are in step())
TRANSITIONS = {
    "Begin!": _row("VO VO VO VO VO VO VO VO VO VO VO VO"),
    "New!": _row("VN VN -  -  VN VN VN VN VN VN VN VN"),
    "Join!": _row("VP -  -  -  -  -  AA AP QP -  -  VP"),
    "Lv!": _row("-  VO LA LA LA LA -  -  -  AO QO -"),
    "rNew!": _row("-  -  -  -  -  -  -  -  -  -  -  -"),
    "rJoinIn!": _row("AO AP -  -  QA -  -  QO -  QP -  -"),
    "rIn!": _row("-  -  -  -  QA -  -  -  -  -  -  -"),
    "rJoinMt!": _row("-  -  -  -  -  AA -  -  AO -  AP VO"),
    "rMt!": _row("-  -  -  -  -  AA -  -  AO -  AP VO"),
    "rLv!": _row("LO -  -  VN VP VP -  LO LO VP VP -"),
    "rLA!": _row("LO -  -  VN VP VP -  LO LO VP VP -"),
    "periodic!": _row("-  -  -  -  -  AA -  -  -  -  AP -"),
}
#: Table 10-3's tx! and txLA! rows: each state's action, bracketed when it is sent only if it improves the
#: encoding (10.7.6.3, 10.7.6.5), and its next state (note 8 is in transmit())
TX = (_row("[s] sJ sN sN sJ [sJ] sL [s] [s] sJ [s] s"),
      _row("-   AA AN QA QA -    VO -   -   QA -   VO"))
TXLA = (_row("[s] s  sN sN sJ sJ   [s] [s] [s] sJ sJ [s]"),
        _row("LO  AA AN QA QA -    LO  LO  LO  QA QA -"))
#: Table 10-3's txLAF! row (IEEE 802.1Q-2022 10.7.5.9: a LeaveAll transmit opportunity whose MRPDU is full): no
#: state sends, and each goes to its next state; Table 10-4 has no txLAF! row, so the Registrar takes only the
#: sLA's rLA!
TXLAF = _row("LO VP VN VN VP VP LO LO LO VP VP -")
#: the octets an MRPDU may fill, ProtocolVersion to its last EndMark: the MAC client data of one frame, the
#: split's lwSRP buffer (MBX_FRAME_BYTES_MAX less its 14-octet header) and no fabric MRPDU larger. The largest
#: room makes the fewest frames full, so a full() frame is full in either half
MRPDU_ROOM = 1500
#: IEEE 802.1Q-2018 Table 10-4 as printed: rLv!, rLA! and txLA! take IN to LV and start the leavetimer
TABLE_10_4 = {
    "Begin!": {"IN": "MT", "LV": "MT"},
    "rNew!": {"LV": "IN", "MT": "IN"},
    "rJoinIn!": {"LV": "IN", "MT": "IN"},
    "rJoinMt!": {"LV": "IN", "MT": "IN"},
    "rLv!": {"IN": "LV"},
    "rLA!": {"IN": "LV"},
    "txLA!": {"IN": "LV"},
    "leavetimer!": {"LV": "MT"},
}
#: each application's Registrar: MSRP's with the cell Milan v1.2 4.2.7.2.2 changes "for the MSRP application"
#: (rLv! takes IN to MT at once), MVRP's Table 10-4 as printed
REGISTRAR = {"MSRP": {**TABLE_10_4, "rLv!": {"IN": "MT"}}, "MVRP": TABLE_10_4}
#: the applications graded, and the frame decoder of each: an MSRP frame's events and the attribute types its
#: LeaveAll covers (10.8.2.6), an MVRP frame's, whose one attribute type (1, the VID) a LeaveAll covers
APPLICATIONS = ("MSRP", "MVRP")
MVRP_VID = 1
#: each attribute type's FirstValue octets: MSRP's (Table 35-1 to 35-3, srp_wire_compare.MSRP), MVRP's VID
WIDTH = {"MSRP": {kind: a.length for kind, a in td.srp_wire_compare.MSRP.items()}, "MVRP": {MVRP_VID: 2}}
#: the events no frame shows, which may happen between any two (10.7.5.10, 10.7.5.21)
UNSEEN = ("periodic!", "leavetimer!")
#: operPointToPointMAC as each half configures it (notes 4 and 5), the port's for both its participants: the
#: fabric's KL_pp_shadow.sv ties the processor's p2p_i to 1, and the split's srp_mbx.c gives both participants
#: point_to_point true
OPER_P2P = {"all-fabric": True, "split": True}

Config = tuple[str, str]


@dataclass(frozen=True)
class Participant:
    """What the grade needs of one half's participant: its application, its Registrar's table and its port's
    operPointToPointMAC."""

    application: str
    registrar: dict[str, dict[str, str]]
    p2p: bool


def participant(cap: Capture, application: str) -> Participant:
    """One half's participant of an application."""
    return Participant(application, REGISTRAR[application], OPER_P2P[cap.placement])


def frame_events(application: str, s: Sent) -> tuple[list[td.Event], frozenset[int]]:
    """One frame's attribute events, in encounter order, and the attribute types its LeaveAll covers."""
    if application == "MSRP":
        return td.msrp_frame(s)
    events, leave_all = td.mvrp_events(s)
    return events, frozenset({MVRP_VID}) if leave_all else frozenset()


def label_of(application: str, key: tuple[int, str]) -> str:
    """An attribute as a finding names it: an MSRP attribute's type and stream_id or value, an MVRP VID."""
    return td.attribute_label(*key) if application == "MSRP" else f"VID {key[1]}"


def message(action: str, registrar: str) -> str:
    """What an action sends (IEEE 802.1Q-2018 10.7.6.2 to 10.7.6.5): sJ and s by whether the Registrar is IN."""
    bare = action.strip("[]")
    if bare in ("sN", "sL"):
        return "New" if bare == "sN" else "Lv"
    if bare == "sJ":
        return "JoinIn" if registrar == "IN" else "JoinMt"
    return "In" if registrar == "IN" else "Mt"


def step(event: str, config: Config, part: Participant) -> Config:
    """One event that sends nothing, on the Applicant (Table 10-3, notes 4 and 5) and the Registrar."""
    applicant, registrar = config
    ignored = (event == "rJoinIn!" and part.p2p and applicant in ("VO", "VP")) or (event == "rIn!" and not part.p2p)
    if not ignored:
        applicant = TRANSITIONS.get(event, {}).get(applicant, applicant)
    return applicant, part.registrar.get(event, {}).get(registrar, registrar)


def transmit(leave_all: bool, config: Config, part: Participant) -> list[tuple[str | None, Config]]:
    """What one tx! (or txLA!) can send from `config`, and where it takes it: a bracketed action sent or
    not (None), none for a state whose cell has no action."""
    applicant, registrar = config
    actions, nexts = TXLA if leave_all else TX
    after = nexts.get(applicant, applicant)
    if not leave_all and applicant == "AN":
        after = "QA" if registrar == "IN" else "AA"
    moved = (after, part.registrar["txLA!"].get(registrar, registrar) if leave_all else registrar)
    sent = message(actions[applicant], registrar)
    return [(sent, moved), (None, moved)] if actions[applicant].startswith("[") else [(sent, moved)]


def opportunity(leave_all: bool, config: Config, part: Participant,
                full: bool = False) -> list[tuple[str | None, Config]]:
    """A transmit opportunity's outcomes: tx!, or txLA! alone, and where the MRPDU is full, txLAF! too.

    The Applicant takes its own LeaveAll as one event of Table 10-3 and no rLA! (IEEE 802.1Q-2022 10.7.5.8,
    10.7.5.9). The sLA's rLA! (10.7.6.6) reaches the Registrar alone: after txLA! it changes nothing (Table
    10-4 takes IN to LV on both), after txLAF!, which Table 10-4 has no row for, it takes IN to LV."""
    outcomes = transmit(leave_all, config, part) if not leave_all else \
        [(x, step("rLA!", y, part)) for x, y in transmit(True, config, part)] + \
        transmit(True, step("rLA!", config, part), part)
    if leave_all and full:
        applicant, registrar = config
        outcomes.append((None, (TXLAF.get(applicant, applicant), part.registrar["rLA!"].get(registrar, registrar))))
    return outcomes


def settle(configs: set[Config], part: Participant) -> set[Config]:
    """Every configuration the unseen events reach from `configs`."""
    found, todo = set(configs), list(configs)
    while todo:
        config = todo.pop()
        for event in UNSEEN:
            moved = step(event, config, part)
            if moved not in found:
                found.add(moved)
                todo.append(moved)
    return found


def requests(sent: str | None, before: str | None) -> tuple[str, ...]:
    """The MAD Service User's requests an attribute's next message shows, after its message `before`."""
    if sent in ("New", "Lv"):
        return ("New!",) if sent == "New" else ("Lv!",)
    if sent in ("JoinIn", "JoinMt") and before in (None, "Lv", "In", "Mt"):
        return ("Join!",)
    return ()


@dataclass(frozen=True)
class Seen:
    """One thing the grade reads of an attribute: a frame the half sent (`sent`, its message for the
    attribute or None; `leave_all`, a LeaveAll frame; `full`, one that leaves the attribute out and has no
    room for it, full()), or an event the half received (`got`)."""

    ms: int
    sent: str | None = None
    leave_all: bool = False
    got: str = ""
    full: bool = False


@dataclass
class Trace:
    """One attribute's grade as it runs: the configurations it can be in, its last message, and its findings
    and LeaveAll boundaries so far."""

    configs: set[Config]
    last: tuple[int, str] | None = None
    findings: list[str] = field(default_factory=list)
    boundaries: list[tuple[int, bool | None]] = field(default_factory=list)


def declared(configs: set[Config]) -> bool | None:
    """Whether every configuration declares the attribute (True), none does (False), or they disagree."""
    found = {applicant in DECLARING for applicant, _ in configs}
    return found.pop() if len(found) == 1 else None


def illegal(label: str, seen: Seen, pre: set[Config], trace: Trace, part: Participant) -> str:
    """A message no configuration could send, as a finding names it."""
    what = seen.sent or "nothing"
    states = ", ".join(sorted({a + (" with the Registrar IN" if r == "IN" else "") for a, r in pre}))
    could = " or ".join(sorted({s or "nothing" for c in pre
                                for s, _ in opportunity(seen.leave_all, c, part, seen.full)}))
    row = "txLA!" if seen.leave_all else "tx!"
    after = f", after {trace.last[1]} at ms {trace.last[0]}" if trace.last else ""
    return (f"{part.application} {label}: {what} at ms {seen.ms}{' (a LeaveAll)' if seen.leave_all else ''} is "
            f"not an Applicant's message: from {states}, Table 10-3's {row} sends {could} (IEEE 802.1Q-2018 "
            f"10.7.7){after}")


def advance(label: str, seen: Seen, trace: Trace, part: Participant) -> None:
    """Take one sent frame into the trace; a message no configuration could send is a finding, and the trace
    goes on from every configuration that sends it."""
    pre = settle(trace.configs, part)
    for request in requests(seen.sent, trace.last[1] if trace.last else None):
        pre |= settle({step(request, c, part) for c in pre}, part)
    after = {moved for c in pre for sent, moved in opportunity(seen.leave_all, c, part, seen.full)
             if sent == seen.sent}
    if not after:
        trace.findings.append(illegal(label, seen, pre, trace, part))
        anywhere = {(a, r) for a in STATES for r in REGISTRARS}
        after = {moved for c in anywhere for sent, moved in opportunity(seen.leave_all, c, part, seen.full)
                 if sent == seen.sent}
    trace.configs = after
    if seen.leave_all:
        trace.boundaries.append((seen.ms, declared(after)))
    if seen.sent is not None:
        trace.last = (seen.ms, seen.sent)


def grade_attribute(label: str, seen: list[Seen], part: Participant) -> Trace:
    """One attribute's trace against Table 10-3, from Begin! at the half's start."""
    trace = Trace({("VO", "MT")})
    for item in seen:
        if item.got:
            trace.configs = {step(item.got, c, part) for c in settle(trace.configs, part)}
        else:
            advance(label, item, trace, part)
    return trace


Key = tuple[int, str]


def mrpdu_octets(application: str, s: Sent) -> int:
    """One frame's MRPDU, ProtocolVersion to the PDU's EndMark, the MAC's pad left out (IEEE 802.1Q-2022
    10.8.1.2): an MSRP Message's AttributeListLength gives its end (35.2.2.6); an MVRP Message has none, so
    its vectors are walked to the list's EndMark (11.2.3.1)."""
    if application == "MSRP":
        return len(td.unpad_mrp(s.data, s.at)) - s.at
    offset = s.at + 1
    while offset + 2 <= len(s.data) and s.data[offset:offset + 2] != b"\0\0":
        length = s.data[offset + 1]
        offset += 2
        while offset + 2 <= len(s.data) and s.data[offset:offset + 2] != b"\0\0":
            count = int.from_bytes(s.data[offset:offset + 2], "big") & 0x1FFF
            offset += 2 + length + (count + 2) // 3
        offset += 2
    return offset + 2 - s.at


def vector_octets(application: str, kind: int) -> int:
    """The smallest VectorAttribute a value of `kind` adds to an MRPDU that already carries its type's Message,
    as a LeaveAll MRPDU carries every type's: its VectorHeader, FirstValue and one ThreePackedEvents octet,
    and for an MSRP Listener one FourPackedEvents octet (IEEE 802.1Q-2022 10.8.1.2, 35.2.2.7). Each value
    has a vector of its own, as both halves encode it (README [ONEVEC]) and lwSRP counts room."""
    return 2 + WIDTH[application][kind] + 1 + (1 if application == "MSRP" and kind == 3 else 0)


def observations(cap: Capture, application: str = "MSRP") -> dict[Key, list[Seen]]:
    """What the grade reads of each attribute of one application in one half, in time order: a stimulus frame
    before the half's own frames of the same millisecond."""
    own = [(s.ms, *frame_events(application, s), MRPDU_ROOM - mrpdu_octets(application, s))
           for s in cap.frames.get(application, [])]
    got = [(s.ms, *frame_events(application, s)) for s in td.received(cap, application)]
    keys = sorted({(e.kind, e.value) for _, events, *_ in own + got for e in events})
    found: dict[Key, list[Seen]] = {}
    for key in keys:
        timeline: list[tuple[int, int, Seen]] = []
        for ms, events, types in got:
            if key[0] in types:
                timeline.append((ms, 0, Seen(ms, got="rLA!")))
            timeline += [(ms, 0, Seen(ms, got=f"r{e.event}!")) for e in events if (e.kind, e.value) == key]
        for ms, events, types, spare in own:
            mine = [e.event for e in events if (e.kind, e.value) == key]
            if types:
                full = not mine and vector_octets(application, key[0]) > spare
                timeline.append((ms, 1, Seen(ms, mine[0] if mine else None, True, full=full)))
                mine = mine[1:]
            timeline += [(ms, 1, Seen(ms, sent)) for sent in mine]
        found[key] = [item for _, _, item in sorted(timeline, key=lambda t: (t[0], t[1]))]
    return found


@dataclass(frozen=True)
class Grade:
    """One half's grade of one application: its findings, and the declaration state of each attribute at each
    of its LeaveAll boundaries (the millisecond, then each attribute's declared, None where undetermined)."""

    findings: list[str]
    boundaries: list[tuple[int, dict[Key, bool | None]]]
    application: str = "MSRP"


def grade(cap: Capture, application: str = "MSRP") -> Grade:
    """Every attribute of one application in one half against Table 10-3, and the half's declarations at its
    LeaveAlls."""
    part = participant(cap, application)
    findings: list[str] = []
    at: dict[int, dict[Key, bool | None]] = {}
    for key, seen in observations(cap, application).items():
        trace = grade_attribute(label_of(application, key), seen, part)
        findings += [f"[MRP] {cap.placement} {f}" for f in trace.findings]
        for ms, state in trace.boundaries:
            at.setdefault(ms, {})[key] = state
    return Grade(findings, sorted(at.items()), application)


def declarations(found: Grade, left_out: set[Key]) -> list[str]:
    """The declaration state at each LeaveAll boundary as the comparison reads it, `left_out` aside: the
    attributes declared, and any undetermined."""
    shown = []
    for _, states in found.boundaries:
        names = [label_of(found.application, k) for k, v in sorted(states.items()) if v and k not in left_out]
        names += [f"undetermined {label_of(found.application, k)}" for k, v in sorted(states.items())
                  if v is None and k not in left_out]
        shown.append("{" + "; ".join(names) + "}" if names else "{none}")
    return shown


def trace_shown(cap: Capture, application: str, key: Key) -> str:
    """One attribute's messages in one half as an owed grade row asserts them: each run of one message, its
    count and its first millisecond, then the frames of its application the half received (none leaves its
    Registrar MT throughout)."""
    runs: list[list] = []
    for seen in observations(cap, application).get(key, []):
        if seen.sent is None:
            continue
        if runs and runs[-1][0] == seen.sent:
            runs[-1][1] += 1
        else:
            runs.append([seen.sent, 1, seen.ms])
    messages = ", ".join(f"{sent} x{n} from ms {ms}" for sent, n, ms in runs) or "nothing"
    got = len(td.received(cap, application))
    heard = (f"received {got} {application}DU(s)" if got
             else f"received no {application}DU, its Registrar MT throughout")
    return f"{application} {label_of(application, key)}: {messages}; {heard}"


def selftest() -> list[str]:
    """The own-LeaveAll grade on hand-made traces and frames; each failed check, by name.

    A Domain value declared and sent JoinMt until QA (Table 10-3, the Registrar MT):
      * at a LeaveAll MRPDU that carries it, its txLA! sends JoinMt and keeps QA, so a Lv! after it sends Lv
        (LA, tx! sL): legal, as for MVRP's VID;
      * Mt there is illegal: no rLA! takes the Applicant to VP before its txLA!;
      * left out of a LeaveAll MRPDU with room for it, nothing is a finding naming JoinMt alone;
      * left out of a full one, nothing is txLAF! (QA to VP), and its next tx! sends JoinMt.
    Then each half's MRPDU octets and the smallest vector of each type."""
    failed: list[str] = []
    msrp = Participant("MSRP", REGISTRAR["MSRP"], True)
    mvrp = Participant("MVRP", REGISTRAR["MVRP"], True)
    joined = [Seen(0, "JoinMt"), Seen(100, "JoinMt")]

    def check(name: str, ok: bool) -> None:
        if not ok:
            failed.append(name)

    lv = grade_attribute("Domain", [*joined, Seen(1000, "JoinMt", True), Seen(1050, "Lv")], msrp)
    check("msrp-lv-after-own-leaveall", not lv.findings and lv.boundaries == [(1000, True)])
    vid = grade_attribute("VID 2", [*joined, Seen(1000, "JoinMt", True), Seen(1050, "Lv")], mvrp)
    check("mvrp-lv-after-own-leaveall", not vid.findings)
    mt = grade_attribute("Domain", [*joined, Seen(1000, "Mt", True)], msrp)
    check("mt-at-own-leaveall", len(mt.findings) == 1)
    fits = grade_attribute("Domain", [*joined, Seen(1000, None, True)], msrp)
    check("omission-with-room", len(fits.findings) == 1 and "Table 10-3's txLA! sends JoinMt (" in fits.findings[0])
    full = grade_attribute("Domain", [*joined, Seen(1000, None, True, full=True), Seen(1010, "JoinMt")], msrp)
    check("omission-from-full", not full.findings and full.configs == {("AA", "MT")}
          and full.boundaries == [(1000, True)])

    header = bytes(14)
    domains = 212   # 1 + 4 + 212 x 7 + 2 + 2 = 1493 octets: room for no Listener, room for one more Domain
    msrp_pdu = bytes([0, 4, 4]) + (domains * 7 + 2).to_bytes(2, "big") + \
        b"".join(bytes([0x00, 0x01, 6, 3, 0, k % 256, 0]) for k in range(domains)) + bytes(4)
    spare = MRPDU_ROOM - mrpdu_octets("MSRP", Sent(0, header + msrp_pdu + bytes(9), 14))
    check("msrp-octets", spare == 7)
    check("msrp-full-for-a-listener", vector_octets("MSRP", 3) == 12 and vector_octets("MSRP", 3) > spare)
    check("msrp-room-for-a-domain", vector_octets("MSRP", 4) == 7 and not vector_octets("MSRP", 4) > spare)
    mvrp_pdu = bytes([0, 1, 2, 0x20, 0x01, 0, 2, 3 * 36, 0, 0, 0, 0])
    check("mvrp-octets", mrpdu_octets("MVRP", Sent(0, header + mvrp_pdu + bytes(30), 14)) == len(mvrp_pdu)
          and vector_octets("MVRP", MVRP_VID) == 5)
    return failed


if __name__ == "__main__":
    import sys
    if sys.argv[1:] != ["--selftest"]:
        raise SystemExit("usage: twin_mrp.py --selftest")
    missed = selftest()
    print("twin_mrp selftest: " + (f"FAILED {', '.join(missed)}" if missed else "OK (10 checks)"))
    raise SystemExit(1 if missed else 0)
