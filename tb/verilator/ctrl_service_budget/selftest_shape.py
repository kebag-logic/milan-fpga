# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of the 32x32 two-interface point (#859): its owed save groups, its publication
addresses in the shape's mailbox layout, and its scaled bounded waits. selftest.py runs `checks` with its own.
"""
from __future__ import annotations

import sys
from pathlib import Path

import build
import run
import scenario
import shape_point

HERE = Path(__file__).resolve().parent
Check = tuple[str, bool, str]


def save_checks() -> list[Check]:
    """Built without saved state, the 32x32 point owes every save group to #823 by name and grades none of
    them; a point with saved state owes none."""
    sys.path.insert(0, str(HERE.parents[2] / 'tb/verilator/nvm_split_target'))
    import target_cases
    shape, _ = run.POINTS['32x32']
    owed = run.owed_save_groups({'saved_state': False})
    return [('the 32x32 point is built without saved state and owes every save group to #823 by name',
             not build.keeps_saved_state(shape) and owed == [c.name for c in target_cases.CASES] and bool(owed)
             and run.SAVE_OWNER == '#823', f'{owed}'),
            ('a point with saved state owes no save group', run.owed_save_groups({}) == [] and all(
                build.keeps_saved_state(run.POINTS[p][0]) for p in ('1x1', '8x8')), '1x1 and 8x8'),
            ('the owed save groups are named in the results and are not grades',
             set(run.summary('32x32', 'x', [], [], [], owed)['owed']) == {'to', 'save_groups'}
             and 'owed' not in run.summary('8x8', 'x', [], [], []), 'results.json')]


def layout_checks() -> list[Check]:
    """The 32x32 point's publication addresses are its shape layout's, each interface's sinks by their
    ordinal on it, while the contract's points keep entry k for sink k; its waits scale, the others' do not."""
    shape, n_if = run.POINTS['32x32']
    layout = shape_point.mailbox_layout({'mailbox_layout': 'shape', 'shape': shape, 'interfaces': n_if})
    c = scenario.CONTRACT
    binding = scenario.SINK_REG['BINDING']
    ordinal = all(scenario.binding_word(k % 2, k, layout) == scenario.word(
        layout.pub_base + (k % 2) * layout.pub_stride + layout.pub_sink_base + (k // 2) * layout.pub_sink_stride
        + binding) for k in range(33))
    tracked = all(scenario.binding_word(i, k) == scenario.word(
        c.pub_base + i * c.pub_stride + c.pub_sink_base + k * c.pub_sink_stride + binding)
        for i in range(2) for k in range(16))
    out = [('a shape layout\'s BINDING word is its sink\'s ordinal entry on its interface, the contract\'s '
            'entry k for sink k', ordinal and tracked and layout.entry_ordinal and not c.entry_ordinal
            and shape_point.mailbox_layout({}) is shape_point.CONTRACT, f'ordinal {ordinal}, contract {tracked}')]
    scales = {name: shape_point.wait_scale(n, n) for name, n in (('1x1', 2), ('8x8', 9), ('32x32', 33))}
    steps = ['frame 0 00', 'wait tx 1 2 within 2000000', 'wait cycles 100000']
    point = scenario.Point('32x32', shape, n_if, 0, 0, 33, 33)
    (g,) = shape_point.scaled([scenario.Group('scaled', steps=list(steps))], point)
    (kept,) = shape_point.scaled([scenario.Group('kept', steps=list(steps))], scenario.Point('8x8', '', 2, 0, 0, 9, 9))
    stretched = g.script() == 'frame 0 00\nwait tx 1 2 within 8000000\nwait cycles 100000\nend\n'
    out.append(('a point\'s bounded waits stretch with its streams over the 8x8 shape\'s: 1 at 1x1 and 8x8, 4 at '
                '32x32, and only a wait\'s within bound moves', scales == {'1x1': 1, '8x8': 1, '32x32': 4}
                and stretched and kept.steps == steps, f'{scales}, script scaled {stretched}'))
    settles = {name: next(s for g in scenario.backlog_groups(pt) if g.name == 'backlog-owed'
                          for s, after in zip(g.steps, g.steps[1:]) if after == 'gap 1')
               for name, pt in (('8x8', scenario.Point('8x8', '', 2, 0, 0, 9, 9)), ('32x32', point))}
    out.append(('the owed row\'s settle before its composed window stretches likewise: 50 ms at 8x8, 200 ms at 32x32',
                settles == {'8x8': 'wait cycles 5000000', '32x32': 'wait cycles 20000000'}, f'{settles}'))
    return out


def checks() -> list[Check]:
    """Every check of the 32x32 point and whether it holds."""
    return [*save_checks(), *layout_checks()]
