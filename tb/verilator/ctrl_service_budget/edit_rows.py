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

#: Each paced member's record in us at each point (above). A one-row edit's under #894's one-row edit cut, bc971054:
#: at 1x1/1if 24,360 CPU cycles, a REMOVE of one output row in the answering-ports arm, 260 by the rule (arm A's REMOVE
#: of one input row 22,728, 240; 27,851 at 7398ec0a), 24,418 under the SET_CONFIGURATION cut; with its commit to the
#: datapath's map store through the EDIT window (#923), each beat answered at the contract's bound, 27,866, 295 by the
#: rule (arm A's REMOVE of one input row 26,177, 275); at 8x8/2if 30,563, a REMOVE of one output row, 325 (30,124 under
#: that cut). An accepted SET_CONFIGURATION's under #894's cut of it (f275b619, paced at fe0cef5b), in the
#: answering-ports arm's aecp-fanout: at 1x1/1if 28,376 CPU cycles, 300 by the rule (33,724 at 9606b3a9, 355; 28,076
#: at #923's head, 295, the larger kept); at 8x8/2if 56,474, 595 (78,332, 825).
PACED = {'1x1/1if': {'a one-row edit': 295, 'an accepted SET_CONFIGURATION': 300},
         '8x8/2if': {'a one-row edit': 325, 'an accepted SET_CONFIGURATION': 595}}
#: The paced class's record at each point: the dearest of its members'.
EDIT_RECORD_US = {point: max(members.values()) for point, members in PACED.items()}
#: The planted defects controls() plants (rows_tiers.CONTROLS names them).
CONTROLS = ("an unpaced edit charged at the non-edit record", "an unpaced SET_CONFIGURATION charged as ordinary")


def point_of(i: Inputs) -> str:
    """The point whose stated costs the inputs are: one interface's 1x1/1if's, two 8x8/2if's."""
    return '1x1/1if' if i.s['n_if'] == 1 else '8x8/2if'


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
    """The planted defects not refused, each refused by name and shortening a held row at 1x1/1if: an unpaced edit
    charged at the non-edit record (the term taken as the pace's count where no pace holds), unpaced; and an unpaced
    SET_CONFIGURATION charged as ordinary (the class's record its edits' alone, the command left out of the pace)."""
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
    plain = rt.solve('ACMP', i, rt.BUILT)[0]
    edits_only = {**EDIT_RECORD_US, '1x1/1if': PACED['1x1/1if']['a one-row edit']}
    with mock.patch.object(module, 'EDIT_RECORD_US', edits_only):
        named = any(f.startswith('an accepted SET_CONFIGURATION charged below its record') for f in findings(i))
        planted = rt.solve('ACMP', i, rt.BUILT)[0]
    if not named or plain is None or planted is None or not planted < plain:
        escaped.append(CONTROLS[1])
    return escaped
