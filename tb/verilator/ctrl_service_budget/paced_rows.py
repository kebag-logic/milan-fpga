# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE PACE in the tier model (#894, #904; #894's pace ruling of 2026-11-13, lever 3): an ADD or
REMOVE_AUDIO_MAPPINGS holds AECP's next record in its ring, never dropped, until AECP_PACE_MS after it was taken
(aecp_mbx.c, ready). Every edit is paced, so the rows that count every AECP command as the largest legal one,
rows_tiers.LONG_ROWS, take at most one a pace:

  txL   THE TRANSMIT's MRPDU: in a window of w ms at most ceil((w + 1) / P) of AECP's arrivals are edits (edits, the
        firmware's whole-millisecond gate) at the largest legal command's record (rows_tiers.LONG_RECORD_US), and every
        other arrival an ordinary record, the dearest mix the pace allows (record);
  R4L   AECP's burst, every command the largest legal one: its last is taken 15 paces after its first at the latest,
        each take late by at most TAKE_PASSES passes (the gate reads the core's clock, which each pass's poll moves
        on, and the take is the next pass's tier 1), and is then the row of one such command by every source (r4l).

The pace is the smallest that holds txL within the MRP timer budget at 1x1/1if and R4L within the response time of
IEEE 1722.1-2021 9.3.2.6 less the fabric's allowances (choice, PACED_BOUNDS), at most PACE_MOST_MS; aecp_mbx.h must
state it (controls refuses a tree that does not). A module of the model alone: rows_tiers reads the tree and solves the
rows."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from tier1_rows import allowance

if TYPE_CHECKING:
    from rows_tiers import Inputs

#: The pace's ceiling in ms, the ruling's: 15 paces and a row of 20 ms within 240.
PACE_MOST_MS = 13
#: The passes a paced record's take may wait past its pace: the pass in which the pace opens, whose poll moves the
#: core's clock on, and the next, whose tier 1 takes it (ctrl_loop.c), each within THE SHARE.
TAKE_PASSES = 2
#: The response time a paced edit is answered within, in ms (IEEE 1722.1-2021 9.3.2.6; Milan v1.2 5.4.3.4).
RESPONSE_MS = 240
#: ctrl_loop.h, which states the fabric's allowances (CTRL_LOOP_T_INGRESS_MS, CTRL_LOOP_T_EGRESS_MS).
LOOP = Path(__file__).resolve().parents[3] / 'sw/firmware/ctrl/loop/ctrl_loop.h'
#: R4L's bound under the pace, in ms (#894's pace ruling of 2026-11-13, item 1): its commands are paced edits, each
#: answered on the wire within the response time, so by every source at its commit within that less T_ingress and
#: T_egress, 238 ms, derived (#894's egress ruling of 2026-11-13, item 1); AECP's ordinary rows keep tier 1's 20 ms.
PACED_BOUNDS = {'R4L': RESPONSE_MS - sum(allowance(LOOP.read_text(), name)
                                         for name in ('CTRL_LOOP_T_INGRESS_MS', 'CTRL_LOOP_T_EGRESS_MS'))}
#: The longest window count_findings holds edits to the gate over, in ms: past every txL window up to PACE_MOST_MS.
COUNT_MS = 120
#: AECP_PACE_MS's statement in aecp_mbx.h, which controls plants.
HEADER = 'sw/firmware/ctrl/aecp/aecp_mbx.h'
#: The planted defects controls() plants, in its order (rows_tiers.CONTROLS names them).
CONTROLS = ("THE PACE not the model's", "txL's AECP records not paced", "R4L's burst without its paces",
            "THE PACE's edits not the gate's count", "THE PACE's edits counted 1 + floor(w / P)")


def edits(w_ms: float, pace_ms: int) -> int:
    """The most paced edits AECP takes in a window of w_ms (a multiple of 0.01 ms): ceil((w + 1) / P). The gate
    compares whole milliseconds (aecp_mbx.c, ready): an edit is stamped with the clock aecp_rx reads as it takes the
    record (aecp.c, now; aecp_maps.c), and the next is taken once the core's clock, never ahead of that read, is P
    past the stamp. So floor(t[k+1]) >= floor(t[k]) + P, N edits span more than P (N - 1) - 1 ms, and the window holds
    N - 1 < (w + 1) / P paces (#894's egress ruling of 2026-11-13, item 2)."""
    return -(-(round(w_ms * 100) + 100) // (100 * pace_ms))


def gate_most(w_us: int, pace_ms: int) -> int:
    """The most edits the gate takes in a window of w_us, by its own arithmetic and not edits' formula: the first
    taken in its millisecond's last microsecond, each next at the first microsecond whose whole millisecond is the
    pace past the last one's stamp (aecp_mbx.c, ready: now - edited_ms >= AECP_PACE_MS), the window opening at the
    first."""
    first, stamp, taken = 999, 0, 1
    while (stamp + pace_ms) * 1000 - first <= w_us:
        stamp, taken = stamp + pace_ms, taken + 1
    return taken


def count_findings() -> list[str]:
    """Each window, of 0.01 to COUNT_MS ms in steps of 0.01, and pace up to PACE_MOST_MS, at which edits counts other
    than the gate takes (gate_most)."""
    for pace in range(1, PACE_MOST_MS + 1):
        for hundredths in range(1, 100 * COUNT_MS + 1):
            counted, most = edits(hundredths / 100, pace), gate_most(10 * hundredths, pace)
            if counted != most:
                return [f"THE PACE's edits in a window of {hundredths / 100:.2f} ms at {pace} ms counted {counted}, "
                        f"not the {most} the gate takes (aecp_mbx.c, ready)"]
    return []


def record(row: str, i: Inputs, w_ms: float) -> float:
    """A LONG_ROWS row's AECP record in us, charged to each of its arrivals: under no pace, or in R4L (every command
    of its burst the largest legal one), the largest legal command's; in txL with a pace, the window's dearest mix,
    edits(w, P) of them at that record and the rest ordinary, spread over the arrivals."""
    long, short = max(i.c['record.aecp'], i.c['record.aecp.long']), i.c['record.aecp']
    if row != 'txL' or not i.pace_ms:
        return long
    arrivals = i.rate['aecp'][0] + math.floor(w_ms / i.rate['aecp'][1])
    paced = min(arrivals, edits(w_ms, i.pace_ms))
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
    its paced bound (PACED_BOUNDS) at 1x1/1if under the built design; None where none does."""
    import rows_tiers as rt
    i = rt.point_inputs(root, '1x1/1if')
    for pace in range(1, PACE_MOST_MS + 1):
        at = i._replace(pace_ms=pace)
        tx, r4 = rt.solve('txL', at, rt.BUILT)[0], rt.solve('R4L', at, rt.BUILT)[0]
        if tx is not None and tx <= i.tx_bound and r4 is not None and r4 <= PACED_BOUNDS['R4L']:
            return pace
    return None


def statements(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each way the tree's pace is not the model's: AECP_PACE_MS not choice's, or over PACE_MOST_MS."""
    import rows_tiers as rt
    stated, taken = rt.point_inputs(root, '1x1/1if', texts).pace_ms, choice(root)
    if taken is None:
        return [f"no pace up to {PACE_MOST_MS} ms holds txL within its bound and R4L within {PACED_BOUNDS['R4L']} ms"]
    return [] if stated == taken else [f'aecp_mbx.h states AECP_PACE_MS {stated} ms, not the model\'s {taken} ms']


def controls(root: Path) -> list[str]:
    """Each planted defect of the pace not refused: a pace the tree states other than the model's, the pace left out
    of txL's records, and R4L's burst without its paces."""
    from unittest import mock

    import rows_tiers as rt
    escaped = []
    text = (root / HEADER).read_text()
    taken = choice(root)
    if taken is None:
        # no pace holds txL: the tree is refused whatever it states, by name
        if not any('no pace up to' in s for s in statements(root)):
            escaped.append("THE PACE not the model's")
    elif statements(root) or f'#define AECP_PACE_MS {taken}u\n' not in text or not all(
            statements(root, {HEADER: text.replace(f'#define AECP_PACE_MS {taken}u\n', f'#define AECP_PACE_MS {p}u\n')})
            for p in (taken - 1, taken + 1)):
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
    return escaped + count_controls(i)


def count_controls(i: Inputs) -> list[str]:
    """The count's planted defects not refused: edits not the gate's, and the earlier rule, 1 + floor(w / P), which
    undercounts where w mod P is over P - 1: it must be refused by name and must shorten txL at a pace whose window
    falls there."""
    from unittest import mock

    import rows_tiers as rt
    escaped = [] if not count_findings() else [CONTROLS[3]]
    gate = [rt.solve('txL', i._replace(pace_ms=p), rt.BUILT)[0] or 2000.0 for p in range(1, PACE_MOST_MS + 1)]
    with mock.patch.object(sys.modules[__name__], 'edits', lambda w_ms, pace_ms: 1 + math.floor(w_ms / pace_ms)):
        named = any('counted' in f and 'not the' in f for f in count_findings())
        earlier = [rt.solve('txL', i._replace(pace_ms=p), rt.BUILT)[0] or 2000.0 for p in range(1, PACE_MOST_MS + 1)]
    if not named or not any(e < g for e, g in zip(earlier, gate)) or any(e > g for e, g in zip(earlier, gate)):
        escaped.append(CONTROLS[4])
    return escaped
