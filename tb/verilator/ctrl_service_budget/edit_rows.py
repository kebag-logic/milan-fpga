# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE PACE's records among AECP's ordinary records (#894's class-split amendment, and its SET_CONFIGURATION ruling,
item 3): every checked ADD or REMOVE_AUDIO_MAPPINGS and every accepted SET_CONFIGURATION is paced (aecp_maps.c and
aecp_commands.c stamp it, aecp_mbx.c, ready, holds the next record; paced_rows.py), so a row's window of w ms holds at
most edits(w, P) of them, ceil((w + 1) / P). A tier-model row that is not one of rows_tiers.LONG_ROWS charges each
AECP record it counts at record.aecp, the ordinary commands' record, and here those paced records the difference to
their class's, EDIT_RECORD_US: of the k records it counts, min(k, edits(w, P)) are paced, the dearest mix the pace
allows. Unpaced (a pace of 0), the window holds as many paced records as records, so every one is charged the class's
record. LONG_ROWS charge every paced record the largest legal command's record (paced_rows.record) and take none of
these.

EDIT_RECORD_US is the paced class's record, the dearest of its members' (PACED), each as the CPU budget harness
measures it, the AECP record handler (aecp_mbx.c, frame), plus 5 %, rounded up to 5 us, the most over every arm that
reaches it: a one-row edit's, an ADD or REMOVE_AUDIO_MAPPINGS of one mapping, in the aecp-fanout group of arm A, whose
input map holds a row, and of the answering-ports arm, whose port observation answers, so its output map is edited
too (at 8x8/2if, whose input maps have capacity 0, only the output map); and an accepted SET_CONFIGURATION's, which
only the answering-ports arm reaches (arm A's observation ports never answer, so its running check refuses).
record_classes.py holds each measured paced record to it, and every other AECP record to record.aecp. A module of the
model alone: tier1_rows charges the term, rows_tiers solves the rows."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import paced_rows

if TYPE_CHECKING:
    from rows_tiers import Inputs

#: Each paced member's record in us at each point (above). A one-row edit's under #894's one-row edit cut, bc971054: at
#: 1x1/1if 24,360 CPU cycles, a REMOVE of one output row in the answering-ports arm, 260 by the rule (arm A's REMOVE of
#: one input row 22,728, 240; 27,851 at 7398ec0a), 24,418 under the SET_CONFIGURATION cut; with its commit to the
#: datapath's map store through the EDIT window (#923), each beat answered at the contract's bound, 27,866, 295 by the
#: rule (arm A's REMOVE of one input row 26,177, 275; 23,877 and 21,543 at #923's base 16ba667d); at 8x8/2if 30,563, a
#: REMOVE of one output row, 325 (30,124 under that cut), and with its commit 33,481, 355 (28,627 at that base). An
#: accepted SET_CONFIGURATION's under #894's cut of it (f275b619, paced at fe0cef5b), in the answering-ports arm's
#: aecp-fanout: at 1x1/1if 28,376 CPU cycles, 300 by the rule (33,724 at 9606b3a9, 355; 28,076 at #923's head, 295, the
#: larger kept), and 28,752, 305, once that arm's path port reads the window (#897, arm_path.py), the same work, its
#: fetches moved by the port's code (28,357 with the port answering at once), and with AECP's REBOOT merged on the tiers
#: (#871), whose image moves the hot code, 28,750, 305; at 8x8/2if 56,474, 595 (78,332, 825; 55,928 at #923's head,
#: 590), and 55,631 with that port.
#: At 8x8/1if, one interface's 8x8 streams, on the image that merges #902's 234bc149 (#894's shape ruling, item (b);
#: THE SHAPES): a one-row edit's 30,277 CPU cycles, a REMOVE of one output row in the answering-ports arm, 320 by the
#: rule, and an accepted SET_CONFIGURATION's 60,027 there, 635, each the most over every arm that reaches it; on the
#: image that merges dev-soft-core 70f4056f (#901), 31,449 and 65,169 cycles there, 335 and 685 by the rule.
#: On the composed flip train's final head with attempt 2's cuts (#665's ruling of 2026-11-18, item 2): 1x1/1if a
#: one-row edit 29,331 CPU cycles (the answering-ports arm, aecp-fanout, a one-row REMOVE_AUDIO_MAPPINGS), 310 us,
#: each by the rule; on the SRP cut's head (#665's ruling of 2026-11-20, item 3), whose code moves AECP's, 29,993 CPU
#: cycles there, 315 us, raised as the owner decided on 2026-11-20 (#665, ruling item 4).
PACED = {
    'arty-1x1': {'a one-row edit': 335, 'an accepted SET_CONFIGURATION': 315},'1x1/1if': {'a one-row edit': 315, 'an accepted SET_CONFIGURATION': 305},
         '8x8/2if': {'a one-row edit': 355, 'an accepted SET_CONFIGURATION': 595},
         '8x8/1if': {'a one-row edit': 335, 'an accepted SET_CONFIGURATION': 685}}
#: The paced class's record at each point: the dearest of its members'.
EDIT_RECORD_US = {point: max(members.values()) for point, members in PACED.items()}
#: The planted defects controls() plants (rows_tiers.CONTROLS names them).
CONTROLS = ("an unpaced edit charged at the non-edit record", "an unpaced SET_CONFIGURATION charged as ordinary")


def point_of(i: Inputs) -> str:
    """The point whose stated costs the inputs are, by its shape, its interfaces and its sinks (load_grade.POINTS),
    never by its interface count alone (THE SHAPES): 1x1/1if, 8x8/1if or 8x8/2if; a point the class is not measured at
    takes the measured one of its interface count."""
    import load_grade
    own = [p for p in PACED if (load_grade.POINTS[p]['n_if'], load_grade.POINTS[p]['sinks_per_if'],
                              load_grade.POINTS[p].get('sources')) ==
           (i.s['n_if'], i.s['sinks_per_if'], i.s.get('sources'))]
    return own[0] if own else '1x1/1if' if i.s['n_if'] == 1 else '8x8/2if'


def edits_in(i: Inputs, w_ms: float, records: int) -> int:
    """Of the records a row counts in a window of w_ms, the most that are edits: under the pace edits(w, P) at most,
    unpaced every one."""
    return records if not i.pace_ms else min(records, paced_rows.edits(w_ms, i.pace_ms))


def terms(i: Inputs, w_ms: float, records: int) -> dict[str, float]:
    """The term the edits among a row's AECP records add, in us: each the edit's record less the ordinary one."""
    more = max(0.0, EDIT_RECORD_US[point_of(i)] - i.c['record.aecp'])
    return {'edits': edits_in(i, w_ms, records) * more} if records else {}


def findings(i: Inputs) -> list[str]:
    """A paced member charged below its record (the class's record is the dearest of its members'), and each count the
    term charges other than the rule's, at windows of 1 to 120 ms and counts of 1 to 40 records, paced and unpaced: an
    unpaced window's records each the class's, a paced window's no more than edits(w, P)."""
    point = point_of(i)
    below = [f'{member} charged below its record: {us} us, the paced class {EDIT_RECORD_US[point]} us'
             for member, us in PACED[point].items() if us > EDIT_RECORD_US[point]]
    if below:
        return below
    more = max(0.0, EDIT_RECORD_US[point] - i.c['record.aecp'])
    for pace in (0, i.pace_ms or 8):
        at = i._replace(pace_ms=pace)
        for w in range(1, 121):
            for k in range(1, 41):
                want = (k if not pace else min(k, paced_rows.edits(w, pace))) * more
                got = terms(at, w, k).get('edits', 0.0)
                if got != want:
                    kind = 'an unpaced edit' if not pace else 'a paced edit'
                    return [f'{kind} charged other than its record: {k} records in {w} ms charged {got:.0f} us of '
                            f'edits, not {want:.0f}']
    return []


def controls(root: Path) -> list[str]:
    """The planted defects not refused, each refused by name and shortening ACMP's row: an unpaced edit charged at the
    non-edit record (the term taken as the pace's count where no pace holds), unpaced, at 1x1/1if; and an unpaced
    SET_CONFIGURATION charged as ordinary (the class's record its edits' alone, the command left out of the pace), at
    the first point whose SET_CONFIGURATION is the class's dearer member."""
    from unittest import mock

    import rows_tiers as rt
    i = rt.point_inputs(root, '1x1/1if')
    bare = i._replace(pace_ms=0)
    escaped = [] if not findings(i) else [CONTROLS[0]]
    plain = rt.solve('ACMP', bare, rt.BUILT)[0]
    module = sys.modules[__name__]
    with mock.patch.object(module, 'edits_in',
                           lambda at, w, k: 0 if not at.pace_ms else min(k, paced_rows.edits(w, at.pace_ms))):
        named = any(f.startswith('an unpaced edit charged') for f in findings(i))
        planted = rt.solve('ACMP', bare, rt.BUILT)[0]
    if not named or plain is None or planted is None or not planted < plain:
        escaped.append(CONTROLS[0])
    # The second is planted where an accepted SET_CONFIGURATION is the class's dearer member, so that leaving it out
    # moves the class's record: 1x1/1if while it is there, else the first point where it is (at 1x1/1if a one-row
    # edit measured past it on #665's final head, where the defect would change no figure)
    point = next(p for p in ('1x1/1if', '8x8/2if', '8x8/1if')
                 if PACED[p]['an accepted SET_CONFIGURATION'] > PACED[p]['a one-row edit'])
    at = i if point == '1x1/1if' else rt.point_inputs(root, point)
    plain = rt.solve('ACMP', at, rt.BUILT)[0]
    edits_only = {**EDIT_RECORD_US, point: PACED[point]['a one-row edit']}
    with mock.patch.object(module, 'EDIT_RECORD_US', edits_only):
        named = any(f.startswith('an accepted SET_CONFIGURATION charged below its record') for f in findings(at))
        planted = rt.solve('ACMP', at, rt.BUILT)[0]
    if not named or plain is None or planted is None or not planted < plain:
        escaped.append(CONTROLS[1])
    return escaped
