# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The planted defects of the tier model's rows that count the largest legal notice (rows_tiers.LONG_ROWS: R4L and
txL, #894) and of the slice rule's row among them (rows_tiers.SLICE_HELD, #894's slice ruling of 2026-11-13), each a
control rows_tiers.tree_controls runs and rows_tiers.CONTROLS names. A module of the model's controls alone."""
from __future__ import annotations

from pathlib import Path
from unittest import mock

import rows_tiers as rt


def slice_held(root: Path) -> list[str]:
    """The slice rule's planted defect not refused: a largest legal notice dear enough to put txL over its bound at the
    tree's slice must move the rule to a slice at which txL holds."""
    i = rt.point_inputs(root, '1x1/1if')

    def dear(us: int) -> rt.Inputs:
        """The point's inputs with the largest legal notice costing us and its command an ordinary record's."""
        return i._replace(c={**i.c, 'item.aecp.long': us, 'record.aecp.long': i.c['record.aecp']})
    cost = next((us for us in range(int(i.c['item.aecp.long']), 10_000, 5)
                 if (rt.solve('txL', dear(us), rt.BUILT)[0] or 2000) > i.tx_bound), None)
    if cost is None:
        return ['a slice chosen at which txL is over its bound']   # txL is blind to the notice's cost
    first = rt.point_inputs
    with mock.patch.object(rt, 'point_inputs', lambda r, p, texts=None: dear(cost) if p == '1x1/1if' else
                           first(r, p, texts)):
        us = rt.slice_choice(root)[0]
    w = rt.solve('txL', dear(cost), rt.BUILT._replace(slice_us=us))[0]
    held = us != i.slice_us and w is not None and w <= i.tx_bound
    return [] if held else ['a slice chosen at which txL is over its bound']


def records_counted(root: Path) -> list[str]:
    """Each LONG_ROWS row whose AECP records are not the largest legal command's, measured (rows_tiers.LONG_RECORD_US):
    charged as an ordinary record each row must be shorter, or solved where it was not."""
    i = rt.point_inputs(root, '1x1/1if')
    plain = i._replace(c={**i.c, 'record.aecp.long': i.c['record.aecp']})
    out = []
    for row in rt.LONG_ROWS:
        w, short = rt.solve(row, i, rt.BUILT)[0], rt.solve(row, plain, rt.BUILT)[0]
        if short is None or (w is not None and not short < w):
            out.append(f"{row}'s AECP records not the largest legal command's")
    return out


def controls(root: Path) -> list[str]:
    """Every control of this module not refused."""
    return slice_held(root) + records_counted(root)
