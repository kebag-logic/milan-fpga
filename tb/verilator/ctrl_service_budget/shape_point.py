# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""What a point's scenario takes from its shape (#859): the mailbox layout its build carries, the publication
addresses in that layout, and how much longer its bounded waits are.

A shape whose streams outgrow the contract's tables carries the layout sized from them
(gen_mailbox.shape_variant, split_soc.mailbox_contract), which holds each interface's sinks by their ordinal on
it; every other point carries the contract's own, entry k for sink k. scenario.py takes pub_word, binding_word,
mailbox_layout and scaled from here; selftest_shape.py grades them.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'sw/mailbox'))
from mailbox_model import load  # noqa: E402

CONTRACT = load()
PUB_REG = {r.name: r.offset for r in CONTRACT.pub_registers}
SINK_REG = {r.name: r.offset for r in CONTRACT.pub_sink_registers}

#: The streams (sources and sinks) of the largest shape the scripts' bounded waits were sized at, the
#: 8x8 shape's 9 and 9: a wait bounds how long a step waits for its event, never a grade, and at a
#: larger shape a response can come later than the wait (a GET_TX_STATE answered 54.5 ms after its
#: command at 32x32/2if, past its 20 ms wait and 20 ms settle, so the next probe's frame went in first).
WAIT_SIZED_STREAMS = 18


def mailbox_layout(build: dict) -> object:
    """The mailbox layout a point's build carries (split_soc records it as soc.json's mailbox_layout)."""
    if build.get('mailbox_layout') != 'shape':
        return CONTRACT
    import gen_mailbox
    config = ROOT / 'configs' / (build['shape'] + '.yaml')
    return gen_mailbox.shape_variant(CONTRACT, config, build['interfaces'])[0]


def pub_word(interface: int, name: str, layout: object = CONTRACT) -> int:
    """The host port's word address of an interface's publication register (contract 2.2), in a layout."""
    return (layout.pub_base + interface * layout.pub_stride + PUB_REG[name]) // 4


def binding_word(interface: int, sink: int, layout: object = CONTRACT) -> int:
    """The host port's word address of a sink's BINDING publication register, in a layout: a shape's
    holds sink k at its ordinal on its interface, the contract's at entry k."""
    entry = sink // layout.interfaces if layout.entry_ordinal else sink
    return (layout.pub_base + interface * layout.pub_stride + layout.pub_sink_base
            + entry * layout.pub_sink_stride + SINK_REG['BINDING']) // 4


def wait_scale(sources: int, sinks: int) -> int:
    """How many times longer a point's bounded waits are: its streams over WAIT_SIZED_STREAMS, rounded
    up, and never less than 1, so the 1x1 and 8x8 scripts are unchanged."""
    return max(1, -(-(sources + sinks) // WAIT_SIZED_STREAMS))


def scaled(groups: list, point: object) -> list:
    """The groups, every bounded wait's `within` wait_scale times longer at the point's streams; at a
    scale of 1 they are returned untouched."""
    scale = wait_scale(point.sources, point.sinks)
    if scale == 1:
        return groups
    for g in groups:
        g.steps = [re.sub(r'\bwithin (\d+)\b', lambda m: f'within {int(m[1]) * scale}', step)
                   if step.startswith('wait ') else step for step in g.steps]
    return groups
