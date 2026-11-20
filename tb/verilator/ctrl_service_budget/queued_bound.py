# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The last queued notice's bound at one interface (#894's contingent ruling of 2026-11-13, item 2, as its
amendment of 2026-11-13 states it): decision D's 125 ms (rows_grade.BOUNDS) while the built design's row
holds that by every source, else the row rounded up to the next STEP_MS, never over MOST_MS. ctrl_loop.h states it in
1x1/1if's block of THE SHAPES, CTRL_LOOP_QUEUED_MS, which aecp_mbx.h's AECP_QUEUED_MS is, each shape its own, and the
tier model (rows_tiers.bounds_at), the firmware's tests (test_aecp.cpp) and the
CPU budget harness (notice_window.py) read that statement. #908 stays open while it is over 125 ms.
"""
from __future__ import annotations

import math
from pathlib import Path

import rows_grade
import shape_costs

#: ctrl_loop.h, whose table states the bound for each shape, and the point the bound is held at.
HEADER, POINT = shape_costs.HEADER, '1x1/1if'
#: The amendment's grid and its ceiling, in ms.
STEP_MS, MOST_MS = 5, 140


def ruled(w: float | None) -> int | None:
    """The bound a final row of w ms takes: decision D's while the row holds it, else w rounded up to the next STEP_MS;
    None past MOST_MS (or no row), which goes back to the owner."""
    least = rows_grade.BOUNDS['last']
    if w is None or w > MOST_MS:
        return None
    return least if w <= least else STEP_MS * math.ceil(w / STEP_MS - 1e-9)


def stated(root: Path, texts: dict[str, str] | None = None) -> int:
    """AECP_QUEUED_MS at the point's shape, as ctrl_loop.h's table (or its text in texts) states it."""
    return shape_costs.at(shape_costs.of_point(POINT, root), root, texts)[shape_costs.QUEUED]


def statements(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each way the table's AECP_QUEUED_MS at the point is not the bound the built design's last row rules."""
    import rows_tiers as rt
    w = rt.solve('last', rt.point_inputs(root, POINT, texts), rt.BUILT)[0]
    bound, said = ruled(w), stated(root, texts)
    shown = 'none' if w is None else f'{w:.2f}'
    if bound is None:
        return [f'{POINT}: the last queued notice {shown} ms, past the amendment\'s {MOST_MS} ms: the owner\'s']
    if said != bound:
        return [f'{POINT}: ctrl_loop.h states AECP_QUEUED_MS {said} ms, not the {bound} ms its row {shown} ms rules']
    return []


def controls(root: Path) -> list[str]:
    """Each planted defect of the bound not refused: the rule off its grid or its ceiling, a statement other than the
    rule's, and a row past the ceiling."""
    from unittest import mock

    import rows_tiers as rt
    escaped = []
    if [ruled(w) for w in (100.0, 125.0, 125.01, 130.0, 138.2, 140.0, 140.01, None)] != \
            [125, 125, 130, 130, 140, 140, None, None]:
        escaped.append("the last queued notice's bound not the amendment's rule")
    text, at = (root / HEADER).read_text(), shape_costs.of_point(POINT, root)
    if statements(root) or not all(
            statements(root, {HEADER: shape_costs.planted_at(text, at, shape_costs.QUEUED, v)})
            for v in (stated(root) - STEP_MS, stated(root) + STEP_MS)):
        escaped.append("AECP_QUEUED_MS not the bound the last queued notice's row rules")
    solve = rt.solve
    past = lambda row, *a, **k: (MOST_MS + 0.01, {}) if row == 'last' else solve(row, *a, **k)  # noqa: E731
    with mock.patch.object(rt, 'solve', past):
        if not any('past the amendment' in s for s in statements(root)):
            escaped.append('a last queued notice past 140 ms not the owner\'s')
    return escaped
