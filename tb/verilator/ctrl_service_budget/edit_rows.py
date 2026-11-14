# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE PACE's edits among AECP's ordinary records (#894's round-11 amendment, the class split): every checked ADD or
REMOVE_AUDIO_MAPPINGS is paced (aecp_maps.c stamps it, aecp_mbx.c, ready, holds the next record; paced_rows.py), so
a row's window of w ms holds at most edits(w, P) of them, ceil((w + 1) / P). A tier-model row that is not one of
rows_tiers.LONG_ROWS charges each AECP record it counts at record.aecp, the ordinary commands' record, and here those
edits the difference to their own record, EDIT_RECORD_US: of the k records it counts, min(k, edits(w, P)) are edits,
the dearest mix the pace allows. Unpaced (a pace of 0), the window holds as many edits as records, so every one is
charged the edit's record. LONG_ROWS charge every edit the largest legal command's record (paced_rows.record) and take
none of these.

EDIT_RECORD_US is a one-row edit's record as the CPU budget harness measures it, the AECP record handler (aecp_mbx.c,
frame) of an ADD or REMOVE_AUDIO_MAPPINGS of one mapping, plus 5 %, rounded up to 5 us, the most over every arm that
edits a map with one: the aecp-fanout group of arm A, whose input map holds a row, and of the answering-ports arm,
whose port observation answers, so its output map is edited too (at 8x8/2if, whose input maps have capacity 0, only
the output map). record_classes.py holds each measured edit to it, and every other AECP record to record.aecp. A
module of the model alone: tier1_rows charges the term, rows_tiers solves the rows."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import paced_rows

if TYPE_CHECKING:
    from rows_tiers import Inputs

#: A one-row edit's record in us at each point (above), under the cut of #894's round 11: at 1x1/1if 24,360 CPU cycles,
#: a REMOVE of one output row in the answering-ports arm, 260 by the rule (arm A's REMOVE of one input row 22,728, 240;
#: 27,851 at 7398ec0a); at 8x8/2if 30,563, a REMOVE of one output row, 325.
EDIT_RECORD_US = {'1x1/1if': 260, '8x8/2if': 325}
#: The planted defect controls() plants (rows_tiers.CONTROLS names it).
CONTROLS = ("an unpaced edit charged at the non-edit record",)


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
    """Each count the term charges other than the rule's, at windows of 1 to 120 ms and counts of 1 to 40 records,
    paced and unpaced: an unpaced window's records each the edit's, a paced window's no more than edits(w, P)."""
    more = max(0.0, EDIT_RECORD_US[point_of(i)] - i.c['record.aecp'])
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
    """The planted defect not refused: an unpaced edit charged at the non-edit record (the term taken as the pace's
    count where no pace holds) must be refused by name, and must shorten a held row at 1x1/1if unpaced."""
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
    return escaped
