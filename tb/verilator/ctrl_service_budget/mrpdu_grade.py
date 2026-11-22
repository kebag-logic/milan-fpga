# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE TRANSMIT's row (#665; ctrl_loop.h; FR_NFR.md 3.4.1): under every channel at its refill rate, each MRPDU a join,
periodic or LeaveAll timer made owed, timed from its owner's transmit opportunity to the TX commit of the owner's frame
that answers it. The opportunity is the deadline, the centisecond whose TICK ran the timer out, where the participant's
join timer has run out by then; and where it still runs, the centisecond whose TICK runs it out, since an MRPDU a timer
requests goes out at the participant's next transmit opportunity, the join timer's expiry (IEEE 802.1Q-2018 10.7.4.1;
#665's ruling of 2026-11-16, Q1). A participant is an interface and an MRP application, told by its MRPDU's EtherType;
lwSRP arms its join timer at a commit alone, CTRL_LOOP_JOIN_CS centiseconds (mrp_mad.c, mrp_transmit).
Its budget is THE TRANSMIT's bound, CTRL_LOOP_TX_BOUND_MS as ctrl_loop.h derives it (BUDGET_MS; #894's held-egress
ruling, item (b)(i)), where the family's T_svc held it before THE TIERS.

A timer that runs out with nothing to send owes nothing, and lwSRP reports no such thing: a build after it that sends
no frame shows it. So a timer's run-out is resolved by the builds that follow it, wherever they come, with no horizon
(#894's egress ruling of 2026-11-13, item 4; resolve): the first after it and, where the other participant or
interface owes one too, the next, at most one ordinary or idle pass standing between two (ctrl_loop.c, whole_runs), each
build's frames those it commits and those it leaves owed, which only the poll sends, before the next build (A3). Each
run-out is judged on its owner alone, the participant the testbench recorded at the expiry (recorded_owner; PR #934),
and on the owner's first transmit opportunity. Only a build that can be the owner's settles it (settle, candidate):
the testbench records each build's participant at the build itself (builder; srp_mbx.c's build_mrpdu builds one
participant's MRPDU), and a build recorded as another participant's, or any build before the owner's opportunity,
never settles it. The run-out is `released` where the settling build's run sends the owner's frames (served); `empty`
where the owner's own build sends none of them; `late` where the owner's first frame, or the owner's build that sends
nothing, comes past THE TRANSMIT's bound (LATE_MS) after the owner's opportunity (anchor), or where no build settles it
by then and a build comes past the bound; `absent` where no build follows it in a log that runs on past the bound after
the owner's opportunity (horizon), and `unresolved` where the log ends first; and whatever its builds sent, `unowned`
where the testbench recorded no owner at the expiry, or recorded it unresolved. A build with no participant recorded
settles a run-out only on the owner's frames: it is never taken for the owner's build that sends nothing. Another
participant's callback, running join timer, build or frame never defers a run-out's deadline nor settles it. A late,
absent or unowned run-out fails the run (join_grade.held); an unresolved one is counted and named, never taken for one
that owes nothing.

A run-out late by THE TRANSMIT's bound whose owner's opportunity falls while the testbench holds the egress (TXREADY
0; sim_main.cpp, txready) is judged again from the egress's return (hold_end): `held` where the owner's first frame, or
the owner's build that sends nothing, comes within JoinTime (HELD_JOIN_MS) of the return, and `late` past it. A held
run-out passes and is named (join_grade.held): #872's rulings of 2026-11-21, rule 2, on #894's held-egress precedent;
IEEE 802.1Q-2018 10.7.11, Milan v1.2 Table 4.3. A run-out whose egress is still held at the log's end is judged as any
other.

A LeaveAll timer's run-out owes its owner's LeaveAll (leave_alls). The owner is the participant the testbench recorded
at the expiry itself, read off the callback's own argument and bound to an interface and an application at the
participant's creation (grade.Log.owners; sim_main.cpp, owner_of and note_owner), never inferred from an output after
it (PR #934). The owner's LeaveAll is the first of the owner's own MRPDUs after the run-out that declares a LeaveAll,
which must be the first MRPDU the owner sends after the run-out, at its first transmit opportunity, and within THE
TRANSMIT's bound of that opportunity (IEEE 802.1Q-2018 10.7.4.1: the LeaveAll goes out at the next transmit
opportunity after the timer expires). An owner that sends an MRPDU without it first has `skipped` a transmit
opportunity; one whose LeaveAll comes past the bound is `late`; no MRPDU of the owner's after the run-out is `absent`
in a log that runs on past the bound after the owner's opportunity, and `unresolved` where the log ends first; and a
run-out with no owner recorded, or its owner recorded unresolved, is `unowned`. A skipped, late, absent or unowned
LeaveAll fails the run (join_grade.held). The LeaveAll's row is timed on the owner's LeaveAll, from the owner's first
transmit opportunity (rows).
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from pathlib import Path

import grade
import scenario
from tier1_rows import join_cs, tx_budget_ms

#: The lwSRP callbacks that end a timer (mrp_mad.c), and the row's name for each.
TIMERS = {'on_join_timer': 'join', 'on_pt_timer': 'periodic', 'on_la_timer': 'leaveall'}
#: The function each MRPDU's build enters (srp_mbx.c).
BUILD = 'build_mrpdu'
#: MBX_EV_TYPE_TICK (mbx_contract.h): a TICK event's type, the low byte of its first word.
TICK = 4
PATH = 'mrpdu'
#: THE TRANSMIT's bound in ms as ctrl_loop.h derives it (CTRL_LOOP_TX_BOUND_MS, tier1_rows.tx_budget_ms), never typed:
#: a run-out's build past it is late, and a log that runs on past it with no build after a run-out has none.
_HEADER = (Path(__file__).resolve().parents[3] / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
LATE_MS = tx_budget_ms(_HEADER)
#: The row's harness budget in ms: that bound, read once (LATE_MS), where the family's T_svc held it before THE TIERS
#: (#894's held-egress ruling, item (b)(i): the MRP timer budget's lateness).
BUDGET_MS = LATE_MS
#: CTRL_LOOP_JOIN_CS (ctrl_loop.h): the centiseconds of the join timer a participant's commit arms; the TICK that runs
#: it out is the participant's next transmit opportunity (IEEE 802.1Q-2018 10.7.4.1).
JOIN_CS = join_cs(_HEADER)
#: JoinTime in ms (IEEE 802.1Q-2018 Table 10-7; Milan v1.2 Table 4.3): the most a run-out whose owner's transmit
#: opportunity falls while the egress is held may wait past the egress's return (held; #872's rulings of 2026-11-21,
#: rule 2, on #894's held-egress precedent).
HELD_JOIN_MS = 200.0
#: The MRP applications by their MRPDUs' EtherType (IEEE 802.1Q-2018 Table 10-2, 35.2.2.1).
APPLICATIONS = {0x22EA: 'MSRP', 0x88F5: 'MVRP'}
#: MSRP's Listener attribute, whose vectors carry FourPackedEvents after their ThreePackedEvents (lwSRP's mrp_pdu.c,
#: attr_has_subtype).
LISTENER = 3
#: The LeaveAll timer's callback (mrp_mad.c).
LEAVE_ALL = 'on_la_timer'
#: The outcomes of a LeaveAll timer's run-out by its LeaveAll (leave_alls), and those that fail a run.
LEAVE_ALL_OUTCOMES = ('sent', 'skipped', 'late', 'absent', 'unresolved', 'unowned')
LEAVE_ALL_FAILING = ('skipped', 'late', 'absent', 'unowned')
#: The outcomes of a timer's run-out (resolve), and those that fail a run.
OUTCOMES = ('released', 'empty', 'held', 'late', 'absent', 'unresolved', 'unowned')
FAILING = ('late', 'absent', 'unowned')


def ticks(log: grade.Log) -> list[int]:
    """Each centisecond's TICK, by the cycle its record was posted."""
    return [cycle for cycle, words in log.records if words[0] & 0xFF == TICK]


def participant(frame: bytes, interface: int) -> str | None:
    """A frame's participant, its interface and MRP application (`if0 MSRP`), or None for a frame of neither."""
    kind = APPLICATIONS.get(frame[12] << 8 | frame[13]) if len(frame) > 14 else None
    return f'if{interface} {kind}' if kind else None


def leave_all(frame: bytes) -> bool:
    """Whether an MRPDU declares a LeaveAll: a VectorAttribute whose header's LeaveAllEvent is LeaveAll, in any of its
    Messages, read as lwSRP's mrp_pdu.c (parse_pass) reads them: past the EtherType the ProtocolVersion, then each
    Message's AttributeType and AttributeLength, MSRP's AttributeListLength, and its VectorAttributes to an EndMark,
    each a VectorHeader (LeaveAllEvent in its top three bits, NumberOfValues below), the FirstValue and its packed
    events."""
    msrp = frame[12] << 8 | frame[13] == 0x22EA
    pdu, at = frame[14:], 1
    while at + 2 <= len(pdu):
        kind, size = pdu[at], pdu[at + 1]
        at += 2
        if kind == 0 and size == 0:
            break
        end = len(pdu)
        if msrp:
            end = min(len(pdu), at + 2 + (pdu[at] << 8 | pdu[at + 1]) if at + 2 <= len(pdu) else len(pdu))
            at += 2
        while at + 2 <= end:
            header = pdu[at] << 8 | pdu[at + 1]
            at += 2
            if header == 0:
                break
            if header >> 13 == 1:
                return True
            count = header & 0x1FFF
            at += size + (count + 2) // 3 + ((count + 3) // 4 if msrp and kind == LISTENER else 0)
        if msrp:
            at = end
    return False


#: sends' last log and what it found there.
_SENT: list = [None, None]


def sends(log: grade.Log) -> tuple[dict[str, list[tuple[int, bool]]], dict[tuple[int, int], list[str]], list[int]]:
    """Each participant's MRPDUs, by their commit's bus cycle and whether each declares a LeaveAll, in time order; the
    participants each commit (a bus cycle and an interface) carries, since one TX_HEAD write may commit two; and the
    log's TICKs."""
    if _SENT[0] is not log:
        srp = scenario.CH['srp']
        by: dict[str, list[tuple[int, bool]]] = {}
        at: dict[tuple[int, int], list[str]] = {}
        for cycle, ch, interface, frame in sorted(log.tx, key=lambda r: r[0]):
            who = participant(frame, interface) if ch == srp else None
            if who:
                by.setdefault(who, []).append((cycle, leave_all(frame)))
                at.setdefault((cycle, interface), []).append(who)
        _SENT[:] = [log, (by, at, ticks(log))]
    return _SENT[1]


def opportunity(log: grade.Log, who: str, entry: int) -> int:
    """The participant's first transmit opportunity at or after a timer's run-out at entry (IEEE 802.1Q-2018
    10.7.4.1): where the join timer its last commit before entry armed, at that commit's build, still runs at entry,
    the TICK that runs it out, the JOIN_CS-th after the build (or, past the log's last TICK, the build plus JOIN_CS
    centiseconds); and entry itself where that timer has run out, or the participant has sent nothing."""
    by, _, posted = sends(log)
    builds = index(log)[0]
    mine = [c for c, _ in by.get(who, ()) if c < entry]
    if not mine:
        return entry
    k = bisect_right(builds, mine[-1]) - 1
    armed = builds[k] if k >= 0 else mine[-1]
    j = bisect_right(posted, armed) + JOIN_CS - 1
    expiry = posted[j] if j < len(posted) else armed + JOIN_CS * log.sys_hz // 100
    return max(entry, expiry)


def begin(log: grade.Log, entry: int, cycle: int, interface: int) -> int:
    """Where THE TRANSMIT's row of the frame committed at that cycle on that interface, answering the timer that ran
    out at entry, starts: the deadline of its owner's transmit opportunity (start_of), the centisecond whose TICK ran
    the timer out or runs the owner's join timer out."""
    _, at, posted = sends(log)
    start = start_of(log, entry, at.get((cycle, interface), ()))
    k = bisect_right(posted, start)
    return posted[k - 1] if k else start


def start_of(log: grade.Log, entry: int, whose: tuple | list) -> int:
    """Where a timer's row starts, the commit it ends at carrying the MRPDUs of the participants in whose: its owner's
    first transmit opportunity, the owner the testbench recorded at the expiry, though the commit carries another
    participant's MRPDU too (PR #934); with none recorded, an unowned run-out that fails the run (resolve), the earliest
    of the commit's participants' (the run-out itself for a frame of neither application)."""
    who = recorded_owner(log, entry)
    if who:
        return opportunity(log, who, entry)
    return min([opportunity(log, other, entry) for other in whose] or [entry])


def commits(grader: grade.Grader, entry: int) -> list[tuple[int, int]]:
    """The (cycle, interface) of the frames of the builds after a timer's entry, as the module docstring says."""
    return released(grader.log, entry)


def released(log: grade.Log, entry: int) -> list[tuple[int, int]]:
    """commits' frames, from the log alone: what the timer that ran out at entry released, late or not (join_grade.py
    too); an unowned run-out's too, which fails the run whatever its builds sent."""
    outcome, frames = resolve(log, entry)
    return frames if outcome in ('released', 'held', 'late', 'unowned') else []


def end_of(log: grade.Log, p: grade.Pass) -> int:
    """A pass's end, in bus cycles."""
    return p.start_sys + p.cycles * log.sys_hz // log.cpu_hz


#: index's last log and what it found there.
_INDEXED: list = [None, None]


def index(log: grade.Log) -> tuple[list[int], list[grade.Pass], list[tuple[int, int]], int]:
    """A log's builds, its passes and its SRP frames, each in time order, and its last cycle: the last millisecond it
    records, or its last pass's end."""
    if _INDEXED[0] is not log:
        srp = scenario.CH['srp']
        passes = sorted(log.passes, key=lambda p: p.start_sys)
        last = max([*log.ms.values(), *(end_of(log, p) for p in passes), 0])
        _INDEXED[:] = [log, (sorted(c for c, name in log.entries if name == BUILD), passes,
                             sorted((c, i) for c, ch, i, _ in log.tx if ch == srp), last)]
    return _INDEXED[1]


def resolve(log: grade.Log, entry: int) -> tuple[str, list[tuple[int, int]]]:
    """The outcome (OUTCOMES) of the timer that ran out at entry, and the (cycle, interface) of the frames its builds
    sent, as the module docstring says: `unowned` where the testbench recorded no owner at the expiry, whatever its
    builds sent, since no transmit opportunity is the run-out's without its owner (PR #934). An unowned run-out's frames
    are every participant's its builds committed, so that the failing log still shows them."""
    who = recorded_owner(log, entry)
    if who is None:
        return 'unowned', window(log, entry)[1]
    return built(log, entry, who)


def built(log: grade.Log, entry: int, who: str) -> tuple[str, list[tuple[int, int]]]:
    """What the builds after the timer's run-out at entry did for its owner who (resolve): each judged on the owner
    alone, its frames the owner's and its lateness from the owner's first transmit opportunity. Another participant's
    callback, running join timer, build or frame neither defers the run-out's deadline nor answers it (PR #934)."""
    outcome, frames, _, _ = settle(log, entry, who)
    return outcome, frames


def settle(log: grade.Log, entry: int, who: str) -> tuple[str, list[tuple[int, int]], int | None, str]:
    """The owned run-out's outcome, the owner's frames that answer it, the cycle a late one rests on, and on what:
    `owner` its owner's frame or build, `bound` the first build past THE TRANSMIT's bound with none of the owner's.

    The builds after the run-out are taken in turn (candidate): the first that can be the owner's settles it. A build
    the testbench recorded as the owner's settles it on the owner's frames of its builds (served), or as the owner's
    own build that sends nothing (anchor). One it recorded no participant for settles it only on the owner's frames:
    it is never taken for the owner's empty build. A build before the owner's opportunity, or another participant's,
    never settles it. With none settling by the bound, the first build past it makes the run-out late; with no build
    after it at all, the log's end decides absent or unresolved (horizon)."""
    outcome = judge(log, entry, who, None)
    if outcome[0] == 'late':
        # an opportunity the held egress made it miss: judged again from the egress's return, within JoinTime
        back = hold_end(log, opportunity(log, who, entry))
        if back is not None:
            return judge(log, entry, who, back)
    return outcome


def judge(log: grade.Log, entry: int, who: str, back: int | None) -> tuple[str, list[tuple[int, int]], int | None, str]:
    """settle's judgement of the owned run-out at entry: with back None, from the owner's opportunity within THE
    TRANSMIT's bound; with back the egress's return (hold_end), from back within JoinTime, `held` in place of
    `released` and `empty`."""
    builds, _, _, last = index(log)
    start = opportunity(log, who, entry)
    bound = int((LATE_MS if back is None else HELD_JOIN_MS) * log.sys_hz / 1000)
    past = None
    for k in range(bisect_right(builds, entry), len(builds)):
        b = builds[k]
        kind = candidate(log, b, who, start)
        if kind is not None:
            mine, since = served(log, entry, who, run_from(log, k)[1])
            if mine:
                late = mine[0][0] > (since if back is None else back) + bound
                return ('late' if late else 'released' if back is None else 'held'), mine, \
                    mine[0][0] if late else None, 'owner'
            if kind == 'own':
                late = b > (anchor(log, entry) if back is None else back) + bound
                return ('late' if late else 'empty' if back is None else 'held'), [], b if late else None, 'owner'
        if past is None and b > (start if back is None else back) + bound:
            past = b
    if past is not None:
        return 'late', [], past, 'bound'
    return ('absent' if last > horizon(log, entry, who) + bound else 'unresolved'), [], None, 'owner'


def hold_end(log: grade.Log, cycle: int) -> int | None:
    """Where the egress returns, the next TXREADY 1, when it is held at bus cycle `cycle` (the last TXREADY at or
    before it a 0; sim_main.cpp, txready), else None. A late run-out whose owner's opportunity falls in a hold is
    `held` where its owner's frame or build comes within JoinTime of that return (settle), and late past it: #872's rulings of
    2026-11-21, rule 2, on #894's held-egress precedent (IEEE 802.1Q-2018 10.7.11; Milan v1.2 Table 4.3)."""
    held = False
    for c, value in sorted(log.txready):
        if c > cycle:
            if held and value == 1:
                return c
            if not held:
                return None
        else:
            held = value == 0
    return None


def candidate(log: grade.Log, b: int, who: str, start: int) -> str | None:
    """Whether the build at bus cycle b can settle the run-out its owner who answers from its opportunity start
    (settle): `own` where the testbench recorded it as the owner's build (builder), `unattributed` where it recorded
    none, and None where it recorded another participant's, or the build comes before the owner's opportunity."""
    if b < start:
        return None
    whose = builder(log, b)
    return 'own' if whose == who else 'unattributed' if whose is None else None


def builder(log: grade.Log, b: int) -> str | None:
    """The participant whose MRPDU the build at bus cycle b made, as the testbench recorded it at the build's entry
    (srp_mbx.c's build_mrpdu, one participant's MRPDU a build; sim_main.cpp, builder_of), or None where it recorded none
    or recorded it unresolved."""
    return log.owners.get((b, BUILD))


def late_at(log: grade.Log, entry: int) -> tuple[int | None, str]:
    """The cycle a late run-out's judgement rests on, and on what (settle), for its finding (join_grade.held)."""
    who = recorded_owner(log, entry)
    return settle(log, entry, who)[2:] if who else (None, 'owner')


def horizon(log: grade.Log, entry: int, who: str) -> int:
    """Where a run-out with no build after it counts from: its owner's first transmit opportunity. It is absent where
    the log runs on past THE TRANSMIT's bound after that, unresolved where the log ends first; another participant's
    running join timer never defers it (PR #934)."""
    return opportunity(log, who, entry)


def served(log: grade.Log, entry: int, who: str, frames: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], int]:
    """The frames of the builds after a run-out that answer it, its owner's alone (a commit that carries the owner's
    MRPDU), and where their lateness counts from, the owner's first transmit opportunity: another participant's frame
    neither answers the run-out nor times it (PR #934). With none of the owner's, the first build is judged as one that
    sends nothing (anchor)."""
    at = sends(log)[1]
    return [f for f in frames if who in at.get(f, ())], opportunity(log, who, entry)


def window(log: grade.Log, entry: int) -> tuple[int | None, list[tuple[int, int]]]:
    """The first build after the timer's run-out at entry, or None for none, and the (cycle, interface) of every
    participant's frames its builds committed, as the module docstring says."""
    k = bisect_right(index(log)[0], entry)
    return run_from(log, k) if k < len(index(log)[0]) else (None, [])


def run_from(log: grade.Log, k: int) -> tuple[int, list[tuple[int, int]]]:
    """The build at index k of the log's builds and the (cycle, interface) of every participant's frames its run of
    builds committed: it and the builds after it with at most one ordinary or idle pass between two, each build's frames
    those it commits and those it leaves owed (the module docstring)."""
    builds, passes, sent, _ = index(log)
    starts = [p.start_sys for p in passes]

    def pass_at(cycle: int) -> int:
        """The index of the pass a build at that cycle ran in."""
        return max(0, bisect_right(starts, cycle) - 1)
    run, at = [builds[k]], pass_at(builds[k])
    for b in builds[k + 1:]:
        # every pass between the two, idle ones too (a pass's index counts them), but those that send what a build
        # left owed
        between = passes[at + 1:pass_at(b)]
        owed = sum(1 for p in between if bisect_left(sent, (p.start_sys, -1)) < bisect_left(sent, (end_of(log, p), -1)))
        if passes[pass_at(b)].index - passes[at].index - 1 - owed > 1:
            break
        run.append(b)
        at = pass_at(b)
    first = passes[pass_at(run[0])].start_sys if passes else run[0]
    stop = builds[k + len(run)] if k + len(run) < len(builds) else 1 << 62
    frames, interfaces, own = [], set(), sent[bisect_left(sent, (first, -1)):bisect_left(sent, (stop, -1))]
    for cycle, interface in own:
        if len(interfaces) == 2 and interface not in interfaces:
            break
        frames.append((cycle, interface))
        interfaces.add(interface)
    return run[0], frames


def recorded_owner(log: grade.Log, entry: int) -> str | None:
    """The participant the testbench recorded at the MRP timer's expiry at entry (grade.Log.owners), whichever of the
    timers it was, or None where it recorded none or recorded the owner unresolved."""
    return next((log.owners[(entry, name)] for name in TIMERS if log.owners.get((entry, name))), None)


def anchor(log: grade.Log, entry: int) -> int:
    """Where the lateness of the timer's first build after its run-out at entry counts from, where that build sends no
    frame (resolve): the first transmit opportunity of the timer's owner, the participant the testbench recorded at
    the expiry, as opportunity derives it from the posted TICKs. Never a join timer's callback, which may be another
    participant's, and never another participant's opportunity (PR #934). A run-out with no owner recorded has none:
    it is unowned (resolve), and the run-out itself stands in here."""
    who = recorded_owner(log, entry)
    return opportunity(log, who, entry) if who else entry


def outcomes(log: grade.Log) -> list[tuple[int, str, str]]:
    """Each timer's run-out of the log: its cycle, its timer's row name (TIMERS) and its outcome."""
    return [(entry, TIMERS[name], resolve(log, entry)[0]) for entry, name in log.entries if name in TIMERS]


def wait_ms() -> float:
    """The row's normative wait W (FR_NFR.md 3.4.1): what brings its family's budget, min(T_svc, the srp ceiling), to
    BUDGET_MS (grade.budget_ms)."""
    return BUDGET_MS - min(scenario.T_SVC_MS, scenario.CEILING_MS['srp'])


def owner(log: grade.Log, entry: int) -> str | None:
    """The participant that owns a LeaveAll timer's run-out at entry, as the testbench recorded it at the expiry
    (grade.Log.owners), or None where it recorded none or recorded the owner unresolved."""
    return log.owners.get((entry, LEAVE_ALL))


def leave_alls(log: grade.Log) -> list[dict]:
    """Each LeaveAll timer's run-out and the LeaveAll its owner owes, as the module docstring says: its time, its
    outcome (LEAVE_ALL_OUTCOMES), its owner, the owner's first transmit opportunity after it, the commit of the
    owner's first MRPDU after it and of its LeaveAll; with no owner, whether the testbench recorded one unresolved."""
    by, _, _ = sends(log)
    last, bound = index(log)[3], int(LATE_MS * log.sys_hz / 1000)
    out = []
    for entry in sorted(c for c, name in log.entries if name == LEAVE_ALL):
        who = owner(log, entry)
        if who is None:
            out.append(dict(at=entry, outcome='unowned', recorded=(entry, LEAVE_ALL) in log.owners))
            continue
        mine = by.get(who, [])
        start = opportunity(log, who, entry)
        first = next((c for c, _ in mine if c > entry), None)
        sent = next((c for c, la in mine if c > entry and la), None)
        if first is None:
            out.append(dict(at=entry, outcome='absent' if last > start + bound else 'unresolved', who=who,
                            opportunity=start))
            continue
        outcome = 'skipped' if sent is None or first < sent else 'late' if sent > start + bound else 'sent'
        out.append(dict(at=entry, outcome=outcome, who=who, opportunity=start, first=first, sent=sent))
    return out


def tick_at(log: grade.Log, at: int) -> int:
    """The centisecond whose TICK is the last at or before a bus cycle, or that cycle with none before it."""
    posted = sends(log)[2]
    k = bisect_right(posted, at)
    return posted[k - 1] if k else at


def rows(grader: grade.Grader, group: scenario.Group) -> list[dict]:
    """A held group's timer rows: for each timer and interface the longest, each a row of its own, held to BUDGET_MS, on
    its owner's frames from its owner's transmit opportunity (served, begin); a LeaveAll's on its owner's LeaveAll
    (leave_alls)."""
    if not group.save or not group.save.get('loaded'):
        return []
    log = grader.log
    origin = next(cycle for cycle, name in log.marks if name == group.save.get('origin', 'save.change'))
    posted = ticks(log)
    alls = leave_alls(log)
    worst: dict[tuple[str, int], tuple[int, int]] = {}
    for entry, name in log.entries:
        if name not in TIMERS or entry < origin:
            continue
        deadline = max((c for c in posted if c <= entry), default=None)
        if deadline is None or deadline < origin:
            continue
        if name == LEAVE_ALL:
            # the owner's LeaveAll, from the owner's first transmit opportunity (leave_alls)
            r = next((r for r in alls if r['at'] == entry), {})
            timed = [(r['sent'], int(r['who'].split()[0][2:]), tick_at(log, r["opportunity"]))] if r.get('sent') else []
        else:
            timed = [(end, interface, begin(log, entry, end, interface)) for end, interface in commits(grader, entry)]
        for end, interface, start in timed:
            key = (TIMERS[name], interface)
            if key not in worst or end - start > worst[key][1] - worst[key][0]:
                worst[key] = (start, end)
    out = []
    for (kind, interface), (deadline, end) in sorted(worst.items()):
        probe = scenario.Probe(f'{group.name}.mrpdu.{kind}.if{interface}',
                               f'an MRPDU its {kind} timer owes, the longest', 'srp', 'tick', [], path=PATH,
                               wait_ms=wait_ms())
        ms = grader.ms(end - deadline)
        out.append(dict(probe=probe.name, row=probe.row, family=probe.family, interface=interface,
                        path=list(probe.path_key()), start_sys=deadline, end_sys=end, wait_ms=probe.wait_ms, ring='srp',
                        ahead=0,
                        sys_cycles=end - deadline, cpu_cycles=grader.cpu_cycles(end - deadline), ms=round(ms, 5),
                        passes=len(grader.window_passes(deadline, end)), status='measured',
                        **grade.verdicts(ms, probe)))
    return out
