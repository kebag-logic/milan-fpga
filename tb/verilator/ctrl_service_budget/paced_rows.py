# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE PACE in the tier model (#894, #904; the ruling of 2026-11-13 on round 5, lever 3): an ADD or
REMOVE_AUDIO_MAPPINGS holds AECP's next record in its ring, never dropped, until AECP_PACE_MS after it was taken
(aecp_mbx.c, ready). Every edit is paced, so the rows that count every AECP command as the largest legal one,
rows_tiers.LONG_ROWS, take at most one a pace:

  txL   THE TRANSMIT's MRPDU: in a window of w ms at most 1 + floor(w / P) of AECP's arrivals are edits at the largest
        legal command's record (rows_tiers.LONG_RECORD_US), each pace apart, and every other arrival an ordinary
        record, the dearest mix the pace allows (record);
  R4L   AECP's burst, every command the largest legal one: its last is taken 15 paces after its first at the latest,
        each take late by at most TAKE_PASSES passes (the gate reads the core's clock, which each pass's poll moves
        on, and the take is the next pass's tier 1), and is then the row of one such command by every source (r4l).

The pace is the smallest that holds txL within the MRP timer budget at 1x1/1if and R4L within the response time of
IEEE 1722.1-2021 9.3.2.6 (choice), at most PACE_MOST_MS; aecp_mbx.h must state it (controls refuses a tree that
does not). A module of the model alone: rows_tiers reads the tree and solves the rows."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from rows_tiers import Inputs

#: The pace's ceiling in ms, the ruling's: 15 paces and a row of 20 ms within 240.
PACE_MOST_MS = 13
#: The passes a paced record's take may wait past its pace: the pass in which the pace opens, whose poll moves the
#: core's clock on, and the next, whose tier 1 takes it (ctrl_loop.c), each within THE SHARE.
TAKE_PASSES = 2
#: The response time a paced edit is answered within, in ms (IEEE 1722.1-2021 9.3.2.6; Milan v1.2 5.4.3.4).
RESPONSE_MS = 240
#: R4L's bound under the pace, in ms (the ruling of 2026-11-13 on round 5, item 1): its commands are paced edits, each
#: answered within the response time; AECP's ordinary rows keep tier 1's 20 ms.
PACED_BOUNDS = {'R4L': RESPONSE_MS}
#: AECP_PACE_MS's statement in aecp_mbx.h, which controls plants.
HEADER = 'sw/firmware/ctrl/aecp/aecp_mbx.h'


def record(row: str, i: Inputs, w_ms: float) -> float:
    """A LONG_ROWS row's AECP record in us, charged to each of its arrivals: under no pace, or in R4L (every command
    of its burst the largest legal one), the largest legal command's; in txL with a pace, the window's dearest mix,
    1 + floor(w / P) of them at that record and the rest ordinary, spread over the arrivals."""
    long, short = max(i.c['record.aecp'], i.c['record.aecp.long']), i.c['record.aecp']
    if row != 'txL' or not i.pace_ms:
        return long
    arrivals = i.rate['aecp'][0] + math.floor(w_ms / i.rate['aecp'][1])
    paced = min(arrivals, 1 + math.floor(w_ms / i.pace_ms))
    return (paced * long + (arrivals - paced) * short) / arrivals


def bounds(i: Inputs) -> dict[str, int]:
    """The bounds the pace restates: PACED_BOUNDS under a pace, none without one."""
    return dict(PACED_BOUNDS) if i.pace_ms else {}


def one(i: Inputs) -> Inputs:
    """The inputs of R4L's last command alone: AECP's burst of one, no pace ahead of it."""
    return i._replace(rate={**i.rate, 'aecp': (1, i.rate['aecp'][1])}, pace_ms=0)


def waits_ms(i: Inputs) -> float:
    """What R4L's last command waits for its take behind the burst's paces, in ms: each of the burst's others a pace
    and TAKE_PASSES passes of THE SHARE."""
    return (i.rate['aecp'][0] - 1) * (i.pace_ms + TAKE_PASSES * i.h['CTRL_LOOP_SHARE_US'] / 1000)


def r4l(i: Inputs, solve: Callable, dropped: str | None = None) -> tuple[float | None, dict[str, float]]:
    """R4L under the pace, in ms, with its terms in us: its burst's paces (the term `pace`, unless `dropped`), then its
    last command's row by every source."""
    w, terms = solve('R4L', one(i))
    pace = waits_ms(i) if dropped != 'pace' else 0.0
    return (None if w is None else round(w + pace, 2)), {**terms, **({'pace': pace * 1000} if pace else {})}


def choice(root: Path) -> int | None:
    """The pace the model takes: the smallest whole ms, from 1 to PACE_MOST_MS, at which txL holds its bound and R4L
    the response time at 1x1/1if under the built design; None where none does."""
    import rows_tiers as rt
    i = rt.point_inputs(root, '1x1/1if')
    for pace in range(1, PACE_MOST_MS + 1):
        at = i._replace(pace_ms=pace)
        tx, r4 = rt.solve('txL', at, rt.BUILT)[0], rt.solve('R4L', at, rt.BUILT)[0]
        if tx is not None and tx <= i.tx_bound and r4 is not None and r4 <= RESPONSE_MS:
            return pace
    return None


def statements(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each way the tree's pace is not the model's: AECP_PACE_MS not choice's, or over PACE_MOST_MS."""
    import rows_tiers as rt
    stated, taken = rt.point_inputs(root, '1x1/1if', texts).pace_ms, choice(root)
    if taken is None:
        return [f'no pace up to {PACE_MOST_MS} ms holds txL within its bound and R4L within {RESPONSE_MS} ms']
    return [] if stated == taken else [f'aecp_mbx.h states AECP_PACE_MS {stated} ms, not the model\'s {taken} ms']


def controls(root: Path) -> list[str]:
    """Each planted defect of the pace not refused: a pace the tree states other than the model's, the pace left out
    of txL's records, and R4L's burst without its paces."""
    from unittest import mock

    import rows_tiers as rt
    escaped = []
    text = (root / HEADER).read_text()
    taken = choice(root)
    stated = f'#define AECP_PACE_MS {taken}u\n'
    if statements(root) or stated not in text or not all(
            statements(root, {HEADER: text.replace(stated, f'#define AECP_PACE_MS {p}u\n')}) for p in (taken - 1,
                                                                                                         taken + 1)):
        escaped.append("THE PACE not the model's")
    i = rt.point_inputs(root, '1x1/1if')
    unpaced = i._replace(pace_ms=0)
    tx, bare = rt.solve('txL', i, rt.BUILT)[0], rt.solve('txL', unpaced, rt.BUILT)[0]
    if tx is None or (bare is not None and not tx < bare):
        escaped.append("txL's AECP records not paced")
    w, terms = rt.solve('R4L', i, rt.BUILT)
    alone = rt.solve('R4L', one(i), rt.BUILT)[0]
    if w is None or alone is None or w < alone + waits_ms(i) - 0.01 or not terms.get('pace'):
        escaped.append("R4L's burst without its paces")
    with mock.patch.object(sys.modules[__name__], 'waits_ms', lambda inputs: 0.0):
        if not rt.broken(root, rt.BUILT, ('1x1/1if',)):
            escaped.append("R4L's burst without its paces")
    return escaped
