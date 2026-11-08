#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_mrp.py - the two-placement simulation's MRP Applicant grade, MSRP and MVRP (#665).

Each MSRP and MVRP attribute a half sends is graded on its own, as a trace an Applicant can make (#665
issuecomment-6722002738, item 3; issuecomment-6724570965, item 2 for MVRP): IEEE 802.1Q-2018 Table 10-3
with its notes, the application's Registrar (REGISTRAR: Table 10-4, and for the MSRP application the cell
Milan v1.2 4.2.7.2.2 changes, IN / rLv! -> MT at once in place of LV), and the operPointToPointMAC the
half configures (OPER_P2P). The halves' event counts are not compared: they follow the transmit
opportunities and the LeaveAll timer's random draw (10.7.4.3). For MSRP the comparison compares only the
declaration state (declared or not, and the value) at each half's LeaveAll boundaries, which this grade
derives; MVRP is graded in each half and not compared.

What the grade reads, per attribute (its type and FirstValue):
  * each frame the half sent of the application. A frame carrying a LeaveAll is a txLA! for every
    attribute of the participant, and its sLA gives rise to rLA! against every one of them (10.7.6.6,
    10.7.9), before or after the txLA! (10.7.6.6 does not order them). An attribute such a frame does not
    carry sent nothing there, which only a state whose txLA! action is none or bracketed allows. Any other
    frame is a tx! for each attribute it carries, sending the message the frame shows.
  * each frame of the stimulus of the application, as received: its events (rNew! to rLv!), and rLA! for
    a LeaveAll of the attribute's type (10.7.5.13 to 10.7.5.20).
  * between them, periodic! and leavetimer!, which are not on the wire, as often as a trace needs.
  * the MAD Service User's requests (10.7.5.4 to 10.7.5.6), also not on the wire, only where the
    attribute's next message shows one: a New! before a New, a Join! before a declaration's first Join
    (the attribute's first message, or one after a Lv, In or Mt), a Lv! before a Lv. A declaration
    withdrawn and made again with no Lv between them would be its application changing its mind unseen,
    which nothing in the stimulus causes (Milan v1.2 4.2.7.2.1: a Domain is declared after startup or a
    Link Up, and changed for a received Domain).

No frame here is near an MRPDU's capacity, so txLAF! and note 7 (a full MRPDU) do not arise. Re-declare!
and Flush! are a Bridge's port-role events (10.7.5.2, 10.7.5.3) and do not arise at an end station. The
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


def opportunity(leave_all: bool, config: Config, part: Participant) -> list[tuple[str | None, Config]]:
    """A transmit opportunity's outcomes: tx!, or txLA! with its sLA's rLA! after it or before it."""
    if not leave_all:
        return transmit(False, config, part)
    return [(sent, step("rLA!", moved, part)) for sent, moved in transmit(True, config, part)] + \
        transmit(True, step("rLA!", config, part), part)


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
    attribute or None; `leave_all`, a LeaveAll frame), or an event the half received (`got`)."""

    ms: int
    sent: str | None = None
    leave_all: bool = False
    got: str = ""


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
    could = " or ".join(sorted({s or "nothing" for c in pre for s, _ in opportunity(seen.leave_all, c, part)}))
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
    after = {moved for c in pre for sent, moved in opportunity(seen.leave_all, c, part) if sent == seen.sent}
    if not after:
        trace.findings.append(illegal(label, seen, pre, trace, part))
        anywhere = {(a, r) for a in STATES for r in REGISTRARS}
        after = {moved for c in anywhere for sent, moved in opportunity(seen.leave_all, c, part)
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


def observations(cap: Capture, application: str = "MSRP") -> dict[Key, list[Seen]]:
    """What the grade reads of each attribute of one application in one half, in time order: a stimulus frame
    before the half's own frames of the same millisecond."""
    own = [(s.ms, *frame_events(application, s)) for s in cap.frames.get(application, [])]
    got = [(s.ms, *frame_events(application, s)) for s in td.received(cap, application)]
    keys = sorted({(e.kind, e.value) for _, events, _ in own + got for e in events})
    found: dict[Key, list[Seen]] = {}
    for key in keys:
        timeline: list[tuple[int, int, Seen]] = []
        for ms, events, types in got:
            if key[0] in types:
                timeline.append((ms, 0, Seen(ms, got="rLA!")))
            timeline += [(ms, 0, Seen(ms, got=f"r{e.event}!")) for e in events if (e.kind, e.value) == key]
        for ms, events, types in own:
            mine = [e.event for e in events if (e.kind, e.value) == key]
            if types:
                timeline.append((ms, 1, Seen(ms, mine[0] if mine else None, True)))
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
