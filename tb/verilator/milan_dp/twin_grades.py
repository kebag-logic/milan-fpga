#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_grades.py - the two-placement simulation's grades of each half on its own (#665).

What a standard leaves random or bounded is graded against that bound in each half, never against the
other half (#665 issuecomment-6716584453, item 1); what issuecomment-6717765106 rules is graded per half
is graded here too:

  * ADP's start delay, advertise interval and DISCOVER answer (Milan v1.2 5.6.3.5, Table 5.50);
  * MAAP's probe and announce intervals (IEEE 1722-2016 Table B.8);
  * each AEM, vendor-unique and HDCP_APM command answered within 240 ms (IEEE 1722.1-2021 9.3.2.6);
  * the notices' sequence_id: per registered controller, one increment per notice, no gap and no repeat
    (Milan v1.2 5.4.5.1);
  * the sequence_id of the commands the entity sends (CONTROLLER_AVAILABLE): per destination controller,
    rising in send order, gaps allowed, and each controller's response carrying its command's (IEEE
    1722.1-2021 9.2.2.9 says only that it "is incremented on each command sent"; #665
    issuecomment-6722002738, item 2);
  * each MRP participant's transmit opportunities (IEEE 802.1Q-2018 10.7.4; Milan v1.2 Table 4.3): no more
    than three in any 1.5 x JoinTime, LeaveAll within its interval, a declaration repeated within the
    periodic interval;
  * each MSRP and MVRP attribute's events, a trace an Applicant can make (IEEE 802.1Q-2018 Table 10-3;
    twin_mrp.py; issuecomment-6722002738, item 3, and issuecomment-6724570965, item 2, for MVRP);
  * MVRP (Milan v1.2 4.3.2, 4.4.1): VID 2 declared before the first stream frame and while any sink is
    settled, beside the Table 10-3 grade of its events.
"""
from __future__ import annotations

import twin_decode as td
import twin_mrp
from twin_decode import Capture, Sent, aecp, role


def gaps(frames: list[Sent]) -> list[int]:
    """The milliseconds between consecutive frames."""
    return [b.ms - a.ms for a, b in zip(frames, frames[1:])]


def grade_adp(cap: Capture) -> tuple[list[str], dict]:
    """ADP's start delay, advertise interval and DISCOVER answer (Milan v1.2 5.6.3.5, Table 5.50; IEEE
    1722.1-2021 6.2.2.6 valid_time)."""
    adp = [x for x in cap.frames.get("ADP", []) if x.data[x.at + 1] & 0x0F == 0]
    boot = int(cap.notes.get("boot_ms", 0))
    found: list[str] = []
    if not adp:
        return [f"[TIME] {cap.placement} ADP: no ENTITY_AVAILABLE"], {}
    valid_ms = (adp[0].data[adp[0].at + 2] >> 3) * 2000
    if adp[0].ms - boot > 2000:
        found.append(f"[TIME] {cap.placement} ADP: the first ENTITY_AVAILABLE {adp[0].ms - boot} ms after the "
                     "entity started, past Milan v1.2 5.6.3.5.2's 2000 ms")
    found += [f"[TIME] {cap.placement} ADP: {g} ms between ENTITY_AVAILABLEs, past Milan v1.2 Table 5.50's "
              f"9000 ms or valid_time's {valid_ms} ms" for g in gaps(adp) if g > 9000 or g >= valid_ms]
    for t in [a.ms for a in cap.applied if a.what.startswith("ADP ENTITY_DISCOVER")]:
        answer = next((x.ms for x in adp if x.ms >= t), None)
        if answer is None or answer - t > 4000:
            found.append(f"[TIME] {cap.placement} ADP: the ENTITY_DISCOVER at ms {t} answered at {answer}, "
                         "past Milan v1.2 5.6.3.5.3's 4000 ms")
    return found, {"adp_start_ms": adp[0].ms - boot, "adp_gaps_ms": gaps(adp), "adp_valid_time_ms": valid_ms}


def grade_maap(cap: Capture) -> tuple[list[str], dict]:
    """MAAP's probe and announce intervals (IEEE 1722-2016 Table B.8)."""
    maap = cap.frames.get("MAAP", [])
    probes = [x for x in maap if x.data[x.at + 1] & 0x0F == 1]
    announces = [x for x in maap if x.data[x.at + 1] & 0x0F == 3]
    found = [f"[TIME] {cap.placement} MAAP: {g} ms between PROBEs, outside MAAP_PROBE_INTERVAL_BASE 500 + "
             "VARIATION 100" for g in gaps(probes) if not 500 <= g <= 600]
    found += [f"[TIME] {cap.placement} MAAP: {g} ms between ANNOUNCEs, outside MAAP_ANNOUNCE_INTERVAL_BASE "
              "30000 + VARIATION 2000" for g in gaps(announces) if not 30000 <= g <= 32000]
    return found, {"maap_probe_gaps_ms": gaps(probes), "maap_announce_gaps_ms": gaps(announces)}


def commands(cap: Capture) -> list[tuple[int, int, int, int]]:
    """Each controller's AECP command of the stimulus: (ms, controller, sequence_id, message_type)."""
    found = []
    for a in cap.applied:
        d = a.data
        if len(d) > 36 and d[12:14] == b"\x22\xf0" and d[14] == 0xFB and d[15] & 0x0F in (0, 2, 4, 6, 8):
            found.append((a.ms, int.from_bytes(d[26:34], "big"), int.from_bytes(d[34:36], "big"), d[15] & 0x0F))
    return found


def grade_aecp(cap: Capture) -> tuple[list[str], dict]:
    """Each command answered within 240 ms (IEEE 1722.1-2021 9.3.2.6, as aecp.h cites it); a command with
    no answer at all (a reserved message type) is the comparison's, not this bound's."""
    took: dict[str, int] = {}
    for ms, controller, seq, kind in commands(cap):
        answer = next((s.ms for s in cap.frames.get("AECP", []) if role(s) == "response" and s.ms >= ms
                       and (aecp(s).controller, aecp(s).seq, aecp(s).message_type) == (controller, seq, kind + 1)),
                      None)
        if answer is not None:
            took[f"{td.who(controller)} {seq}"] = answer - ms
    found = [f"[TIME] {cap.placement} AECP: {q} answered after {t} ms, past 240 ms" for q, t in took.items() if t > 240]
    return found, {"aecp_response_ms": took}


def grade_sequence(cap: Capture) -> tuple[list[str], dict]:
    """The notices' sequence_id per registered controller: one higher than the last notice's, no gap and
    no repeat (Milan v1.2 5.4.5.1)."""
    seqs: dict[int, list[int]] = {}
    for s in cap.frames.get("AECP", []):
        if role(s) == "notice":
            seqs.setdefault(td.recipient(s), []).append(aecp(s).seq)
    found = [f"[SEQ] {cap.placement} AECP: the notices to {td.who(c)} go from sequence_id {a} to {b}, not one "
             "higher (Milan v1.2 5.4.5.1)"
             for c, run in sorted(seqs.items()) for a, b in zip(run, run[1:]) if (b - a) % 65536 != 1]
    return found, {"notice_sequence_ids": {td.who(c): run for c, run in sorted(seqs.items())}}


#: CONTROLLER_AVAILABLE's command_type (IEEE 1722.1-2021 Table 7-140)
CONTROLLER_AVAILABLE = 0x0003


def answers(cap: Capture) -> dict[int, list[tuple[int, int]]]:
    """Each controller's AEM_RESPONSE to the entity's CONTROLLER_AVAILABLE, as the stimulus applied it: the
    millisecond and the sequence_id, per controller (its target_entity_id)."""
    found: dict[int, list[tuple[int, int]]] = {}
    for s in td.received(cap, "AECP"):
        f = aecp(s)
        if f.message_type == 1 and f.command == CONTROLLER_AVAILABLE:
            found.setdefault(f.target, []).append((s.ms, f.seq))
    return found


def grade_commands(cap: Capture) -> tuple[list[str], dict]:
    """The sequence_id of the commands the entity sends: per destination controller, each higher than the last
    (gaps allowed, modulo 2^16), and each controller's response, in order, carrying its command's."""
    sent: dict[int, list[tuple[int, int]]] = {}
    for s in cap.frames.get("AECP", []):
        if role(s) == "command":
            sent.setdefault(td.recipient(s), []).append((s.ms, aecp(s).seq))
    got = answers(cap)
    found = [f"[SEQ] {cap.placement} AECP: the CONTROLLER_AVAILABLE commands to {td.who(c)} go from sequence_id "
             f"{a} to {b}, not higher (IEEE 1722.1-2021 9.2.2.9)"
             for c, run in sorted(sent.items()) for (_, a), (_, b) in zip(run, run[1:])
             if not 0 < (b - a) % 65536 < 32768]
    for c in sorted(set(sent) | set(got)):
        commands_to, responses_from = sent.get(c, []), got.get(c, [])
        if len(commands_to) != len(responses_from):
            found.append(f"[SEQ] {cap.placement} AECP: {len(commands_to)} CONTROLLER_AVAILABLE command(s) to "
                         f"{td.who(c)}, {len(responses_from)} response(s) from it")
        found += [f"[SEQ] {cap.placement} AECP: {td.who(c)}'s CONTROLLER_AVAILABLE response at ms {t} carries "
                  f"sequence_id {r}, its command's {q}"
                  for (_, q), (t, r) in zip(commands_to, responses_from) if q != r]
    return found, {"controller_available_ids": {td.who(c): [q for _, q in run] for c, run in sorted(sent.items())}}


#: IEEE 802.1Q-2018 Table 10-7 as Milan v1.2 Table 4.3 sets it (docs/reference/FR_NFR.md): JoinTime 200 ms
#: (to 240), LeaveAllTime 10 s drawn up to 1.5 x (10.7.4.3), +/- 0.5 s, periodic 1 s (900 to 1500)
JOIN_MAX_MS = 240
RATE_WINDOW_MS = 300
LEAVE_ALL_MS = (10000 - 500, 15000 + 500 + JOIN_MAX_MS)
PERIODIC_MAX_MS = 1500 + JOIN_MAX_MS


def grade_mrp(cap: Capture) -> tuple[list[str], dict]:
    """Each participant's transmit opportunities against the MRP timers (IEEE 802.1Q-2018 10.7.4): at most
    three in any 1.5 x JoinTime; each LeaveAll within its drawn interval (10.7.4.3) of the last, or of the
    entity's start, and none missing at the run's end; while it declares, the next transmission within
    the periodic interval (10.7.4.4)."""
    found: list[str] = []
    measured: dict = {}
    boot = int(cap.notes.get("boot_ms", 0))
    low, high = LEAVE_ALL_MS
    for proto, decode in (("MSRP", td.msrp_events), ("MVRP", td.mvrp_events)):
        frames = cap.frames.get(proto, [])
        decoded = [decode(s) for s in frames]
        for k in range(len(frames) - 3):
            span = frames[k + 3].ms - frames[k].ms
            if span < RATE_WINDOW_MS:
                found.append(f"[MRP] {cap.placement} {proto}: four transmit opportunities in {span} ms from ms "
                             f"{frames[k].ms}, more than three in 1.5 x JoinTime")
        leave = [s.ms for s, (_, carried) in zip(frames, decoded) if carried]
        for a, b in zip([boot, *leave], [*leave, cap.run_ms]):
            if b - a > high or (b != cap.run_ms and b - a < low):
                found.append(f"[MRP] {cap.placement} {proto}: {b - a} ms from ms {a} to the next LeaveAll "
                             f"(or the run's end at {cap.run_ms}), outside {low} to {high}")
        for k, (events, _) in enumerate(decoded):
            later = frames[k + 1].ms if k + 1 < len(frames) else cap.run_ms
            if any(e.event in td.DECLARING for e in events) and later - frames[k].ms > PERIODIC_MAX_MS:
                found.append(f"[MRP] {cap.placement} {proto}: declaring at ms {frames[k].ms}, the next "
                             f"transmission at {later}, past {PERIODIC_MAX_MS} ms")
        measured[f"{proto.lower()}_leave_all_ms"] = leave
        measured[f"{proto.lower()}_opportunities"] = len(frames)
    return found, measured


def vid2_events(cap: Capture) -> list[td.Event]:
    """MVRP's events for VID 2, the SR class's VLAN (Milan v1.2 4.3.2), in time order."""
    return [e for s in cap.frames.get("MVRP", []) for e in td.mvrp_events(s)[0] if e.value == "0002"]


def declared_at(events: list[td.Event], ms: int) -> bool:
    """Whether VID 2 is declared at `ms`: the last event before it a New or a Join."""
    last = [e for e in events if e.ms <= ms]
    return bool(last) and last[-1].event in td.DECLARING


def settled_intervals(cap: Capture) -> list[tuple[int, int]]:
    """Each interval a sink is settled in, from its STREAM_INPUT's GET_STREAM_INFO notices (probing_status
    COMPLETED, IEEE 1722.1-2021 7.4.16.2), to the next notice that is not, or the run's end."""
    found: list[tuple[int, int]] = []
    since: dict[int, int] = {}
    for s in cap.frames.get("AECP", []):
        f = aecp(s)
        if role(s) != "notice" or f.command != 0x000F or f.descriptor[0] != 0x0005:
            continue
        if td.settled(s):
            since.setdefault(f.descriptor[1], s.ms)
        elif f.descriptor[1] in since:
            found.append((since.pop(f.descriptor[1]), s.ms))
    return found + [(t, cap.run_ms) for t in since.values()]


def grade_mvrp(cap: Capture) -> tuple[list[str], dict]:
    """VID 2 declared before the first stream frame (Milan v1.2 4.3.2) and while any sink is settled, from
    one JoinTime after it settles (4.4.1). Its events are an Applicant's when Table 10-3 says so
    (grade_applicant), which also refuses a Lv before any declaration."""
    events = vid2_events(cap)
    found: list[str] = []
    if cap.first_stream_ms >= 0 and not declared_at(events, cap.first_stream_ms):
        found.append(f"[MVRP] {cap.placement}: the first stream frame at ms {cap.first_stream_ms} before VID 2 "
                     "is declared (Milan v1.2 4.3.2)")
    intervals = settled_intervals(cap)
    for t0, t1 in intervals:
        if not declared_at(events, t0 + JOIN_MAX_MS) or any(e.event == "Lv" for e in events if t0 < e.ms < t1):
            found.append(f"[MVRP] {cap.placement}: a sink settled from ms {t0} to {t1} without VID 2 declared "
                         "throughout (Milan v1.2 4.4.1)")
    first = next((e.ms for e in events if e.event in td.DECLARING), None)
    return found, {"mvrp_vid2_declared_from_ms": first, "mvrp_vid2_events": td.run_length([e.event for e in events]),
                   "first_stream_ms": cap.first_stream_ms, "settled_sinks_ms": intervals}


def grade_applicant(cap: Capture) -> tuple[list[str], dict]:
    """Each MSRP and MVRP attribute's events against Table 10-3 (twin_mrp.py), and what each application
    declares at each of its LeaveAlls."""
    findings: list[str] = []
    measured: dict = {}
    for application in twin_mrp.APPLICATIONS:
        found = twin_mrp.grade(cap, application)
        findings += found.findings
        measured[f"{application.lower()}_leave_all_declarations"] = [
            [ms, shown] for (ms, _), shown in zip(found.boundaries, twin_mrp.declarations(found, set()))]
    return findings, measured


def grade(cap: Capture) -> tuple[list[str], dict]:
    """Every grade of one half."""
    found: list[str] = []
    measured: dict = {}
    for grader in (grade_adp, grade_maap, grade_aecp, grade_sequence, grade_commands, grade_mrp, grade_applicant,
                   grade_mvrp):
        f, m = grader(cap)
        found += f
        measured.update(m)
    return found, measured
