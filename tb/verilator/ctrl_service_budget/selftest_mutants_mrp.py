# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The MRP timers' mutants of the self-test (selftest_mutants.py): the join intervals' grade (join_grade.py) and
THE TRANSMIT's run-outs and LeaveAlls, each judged on its owner from its transmit opportunity (mrpdu_grade.py),
each replacing one of their rules with a plausible defect; selftest_mutants.MUTANTS takes them where they stood,
in this order."""
from __future__ import annotations

from collections.abc import Callable
from unittest.mock import patch

import join_grade
import mrpdu_grade
import scenario


MUTANTS: dict[str, Callable[[], list]] = {
    'joins: no join interval held to its range': lambda: [patch.object(
        join_grade, 'held', lambda log, f=join_grade.held: dict(f(log), over=[]))],
    'joins: the range from the armed 190 ms': lambda: [patch.object(join_grade, 'LEAST_MS', 190.0)],
    "joins: an MRPDU a join timer did not release taken for a join's": lambda: [patch.object(
        join_grade, 'released', lambda log: {c: max((e for e, n in log.entries if n == join_grade.JOIN and e < c),
                                                    default=c) for c, _, _, _ in log.tx})],
    "joins: a periodic or LeaveAll timer's MRPDU taken for a join's": lambda: [patch.object(join_grade, 'OTHERS', ())],
    "joins: the participants' applications not told apart": lambda: [patch.dict(
        join_grade.APPLICATIONS, {0x22EA: 'MRP', 0x88F5: 'MRP'})],
    'joins: any two MRPDUs, with no join timer between': lambda: [patch.object(
        join_grade, 'intervals', lambda log: [(ms, who, end) for ms, who, end in (
            ((b - a) * 1000 / log.sys_hz, 'if0 MRP', b) for a, b in zip(
                *(lambda c: (c, c[1:]))(sorted(c for c, ch, _, fr in log.tx if ch == scenario.CH['srp']))))])],
    "joins: a run-out's builds sought within 100 ms of it (earlier rule)": lambda: [patch.object(
        mrpdu_grade, 'resolve', lambda log, entry, f=mrpdu_grade.resolve: f(log, entry) if any(
            entry < c < entry + log.sys_hz // 10 for c, n in log.entries if n == mrpdu_grade.BUILD) else
        ('empty', []))],
    "joins: the wire's 180.0 to 240.0 ms held at the commit, T_egress uncounted": lambda: [
        patch.object(join_grade, 'LEAST_MS', 180.0), patch.object(join_grade, 'MOST_MS', 240.0)],
    'joins: a late build taken for an on-time one': lambda: [patch.object(mrpdu_grade, 'LATE_MS', 10 ** 6)],
    "joins: a late build's run-out not failing the run": lambda: [patch.object(mrpdu_grade, 'FAILING', ('absent',))],
    'joins: an absent build taken for an unresolved one': lambda: [patch.object(
        mrpdu_grade, 'resolve', lambda log, entry, f=mrpdu_grade.resolve: (
            lambda r: ('unresolved', r[1]) if r[0] == 'absent' else r)(f(log, entry)))],
    'joins: an unresolved build taken for one that owes nothing': lambda: [patch.object(
        mrpdu_grade, 'resolve', lambda log, entry, f=mrpdu_grade.resolve: (
            lambda r: ('empty', r[1]) if r[0] == 'unresolved' else r)(f(log, entry)))],
    "joins: a frame its build left owed not the build's": lambda: [patch.object(
        mrpdu_grade, 'index', lambda log, f=mrpdu_grade.index: (lambda builds, passes, sent, last: (
            builds, passes, [s for s in sent if any(q.start_sys <= s[0] < mrpdu_grade.end_of(log, q) and any(
                q.start_sys <= c < mrpdu_grade.end_of(log, q) for c in builds) for q in passes)], last))(*f(log)))],
    "transmit: an MRPDU a timer owes timed from its run-out, not its participant's transmit opportunity (earlier "
    "rule)": lambda: [patch.object(mrpdu_grade, 'opportunity', lambda log, who, entry: entry)],
    "transmit: a build that sends nothing late only past the last join callback before it, any participant's (earlier "
    "rule)": lambda: [patch.object(mrpdu_grade, 'anchor', lambda log, entry: max([entry] + [
        c for c, name in log.entries if name == 'on_join_timer' and entry < c <= next(
            (b for b in mrpdu_grade.index(log)[0] if b > entry), entry)]))],
    "transmit: an expiry with no owner recorded given the participant whose opportunity is latest (the fallback "
    "restored)": lambda: [patch.object(mrpdu_grade, 'recorded_owner', lambda log, entry, f=mrpdu_grade.recorded_owner: (
        f(log, entry) or max(mrpdu_grade.sends(log)[0], key=lambda who: mrpdu_grade.opportunity(log, who, entry),
                             default=None)))],
    "transmit: an unowned run-out not failing the run": lambda: [patch.object(
        mrpdu_grade, 'FAILING', ('late', 'absent'))],
    "transmit: a run-out with no build after it held to the latest of every participant's opportunity (earlier rule)":
        lambda: [patch.object(mrpdu_grade, 'horizon', lambda log, entry, who: max([entry] + [
            mrpdu_grade.opportunity(log, other, entry) for other in mrpdu_grade.sends(log)[0]]))],
    "transmit: a build's first frame answering a run-out whichever participant's, timed from that participant's "
    "opportunity (earlier rule)": lambda: [patch.object(mrpdu_grade, 'served', lambda log, entry, who, frames: (
        frames, min([mrpdu_grade.opportunity(log, other, entry) for other in mrpdu_grade.sends(log)[1].get(
            frames[0], ())] or [entry]) if frames else entry))],
    "transmit: another participant's MRPDU credited to a run-out, timed from its owner": lambda: [patch.object(
        mrpdu_grade, 'served', lambda log, entry, who, frames: (frames, mrpdu_grade.opportunity(log, who, entry)))],
    "transmit: a build's recorded participant ignored, every build from the owner's opportunity taken for the owner's":
        lambda: [patch.object(mrpdu_grade, 'candidate', lambda log, b, who, start: 'own' if b >= start else None)],
    "transmit: a run-out settled by the first build after it, whichever participant's (earlier rule)": lambda: [
        patch.object(mrpdu_grade, 'candidate', lambda log, b, who, start: 'own')],
    "transmit: a build with no participant recorded that sends nothing taken for the owner's": lambda: [patch.object(
        mrpdu_grade, 'candidate', lambda log, b, who, start, f=mrpdu_grade.candidate: (
            lambda kind: 'own' if kind == 'unattributed' else kind)(f(log, b, who, start)))],
    "transmit: the owner's own build before its transmit opportunity settling its run-out": lambda: [patch.object(
        mrpdu_grade, 'candidate', lambda log, b, who, start, f=mrpdu_grade.candidate: f(log, b, who, -1))],
    "transmit: a timer's row started at the earliest opportunity of its commit's participants (earlier rule)":
        lambda: [patch.object(mrpdu_grade, 'start_of', lambda log, entry, whose: min([
            mrpdu_grade.opportunity(log, other, entry) for other in whose] or [entry]))],
    "transmit: the participant's join timer run out a centisecond early": lambda: [patch.object(
        mrpdu_grade, 'JOIN_CS', mrpdu_grade.JOIN_CS - 1)],
    "held: a run-out the held egress made late never judged from the egress's return": lambda: [patch.object(
        mrpdu_grade, 'hold_end', lambda log, cycle: None)],
    "held: a held run-out's MRPDU past JoinTime of the return taken for held": lambda: [patch.object(
        mrpdu_grade, 'HELD_JOIN_MS', 10 ** 6)],
    'held: a held run-out failing the run': lambda: [patch.object(mrpdu_grade, 'FAILING', ('late', 'absent', 'unowned',
                                                                                         'held'))],
    "held: any later return taken for the hold's, though the hold ended before the opportunity": lambda: [patch.object(
        mrpdu_grade, 'hold_end', lambda log, cycle: next((c for c, v in sorted(log.txready) if c > cycle and v == 1),
                                                         None))],
    "held: a repeated hold read as the egress's return": lambda: [patch.object(
        mrpdu_grade, 'hold_end', lambda log, cycle: next((c for c, v in sorted(log.txready) if c > cycle), None) if any(
            c <= cycle for c, v in log.txready) and [v for c, v in sorted(log.txready) if c <= cycle][-1] == 0
        else None)],
    'held: a join interval across the hold failing the run': lambda: [patch.object(
        join_grade, 'hold_spans', lambda log, out, judged: (out, []))],
    'held: any join interval outside the range named apart, the run-out late or not': lambda: [patch.object(
        join_grade, 'hold_spans', lambda log, out, judged: ([], out))],
    'leaveall: a LeaveAll past its first transmit opportunity not failing the run': lambda: [patch.object(
        mrpdu_grade, 'LEAVE_ALL_FAILING', ('late', 'absent'))],
    "leaveall: a late LeaveAll not failing the run": lambda: [patch.object(
        mrpdu_grade, 'LEAVE_ALL_FAILING', ('skipped', 'absent'))],
    'leaveall: any MRPDU taken for the LeaveAll': lambda: [patch.object(mrpdu_grade, 'leave_all', lambda frame: True)],
    "leaveall: the participants' applications not told apart": lambda: [patch.dict(
        mrpdu_grade.APPLICATIONS, {0x22EA: 'MRP', 0x88F5: 'MRP'})],
    "leaveall: a Listener vector's FourPackedEvents not skipped": lambda: [patch.object(mrpdu_grade, 'LISTENER', 0)],
    "leaveall: an expiry bound to the participant whose LeaveAll comes first after it, not its recorded owner "
    "(earlier rule)": lambda: [patch.object(mrpdu_grade, 'owner', lambda log, entry: next((who for _, who in sorted(
        (c, who) for who, mine in mrpdu_grade.sends(log)[0].items() for c, la in mine if c > entry and la)), None))],
    "leaveall: an expiry with no owner, or its owner unresolved, taken for interface 0's MSRP": lambda: [patch.object(
        mrpdu_grade, 'owner', lambda log, entry, f=mrpdu_grade.owner: f(log, entry) or 'if0 MSRP')],
    "leaveall: the participants' interfaces not told apart": lambda: [patch.object(
        mrpdu_grade, 'participant', lambda frame, interface, f=mrpdu_grade.participant: f(frame, 0))],
    'leaveall: an unowned LeaveAll not failing the run': lambda: [patch.object(
        mrpdu_grade, 'LEAVE_ALL_FAILING', ('skipped', 'late', 'absent'))],
    'leaveall: an absent LeaveAll taken for an unresolved one': lambda: [patch.object(
        mrpdu_grade, 'leave_alls', lambda log, f=mrpdu_grade.leave_alls: [
            dict(r, outcome='unresolved') if r['outcome'] == 'absent' else r for r in f(log)])],
}
