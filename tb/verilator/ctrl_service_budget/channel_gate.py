# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""channel_gate.py - the channels a row's defined load covers: the ones the image opened (#884's ruling, A and B).

A: the opened channels are the bits of the last FILTER_EN write the image made. ctrl_loop_open writes the gate of
every channel it bound, and sim_main.cpp prints each write as OPEN <cycle> <gate>. Each bit is named by the
contract's generated channel table (mailbox.yaml ids), never a hand list. A log with no FILTER_EN write is refused,
never read as every channel: its image's channels are not known.
B: an opened channel with no load frame (grade.LOAD_FRAME_BYTES) is refused, so the rule cannot hide load.
With the gptp channel unopened, every existing row's defined load is unchanged.
"""
from __future__ import annotations

import re
from pathlib import Path

import scenario
from refusal import Refusal

HERE = Path(__file__).resolve().parent
#: sim_main.cpp's line for one FILTER_EN write: its bus cycle and the gate, in hex.
OPEN_RE = re.compile(r'^OPEN (\d+) ([0-9a-f]+)$', re.M)


def writes(text: str) -> list[tuple[int, int]]:
    """Each FILTER_EN write a log records, in order: (cycle, gate)."""
    return [(int(cycle), int(gate, 16)) for cycle, gate in OPEN_RE.findall(text)]


def opened(gates: list[tuple[int, int]]) -> frozenset[str]:
    """The channels the image's last nonzero gate opened (A); refused when the log records none."""
    nonzero = [gate for _, gate in gates if gate]
    if not nonzero:
        raise Refusal('the log records no FILTER_EN write: the channels its image opened are not known')
    return frozenset(ch.name for ch in scenario.CONTRACT.channels if (nonzero[-1] >> ch.ident) & 1)


def fixture() -> frozenset[str]:
    """The channels the committed trace's image opened (selftest.py's fixture.log): the opened set of a caller that
    grades no log of its own."""
    return opened(writes((HERE / 'fixture.log').read_text()))


def loaded(name: str, channels: frozenset[str] | None, frames: dict[str, int]) -> list:
    """The contract's channels a row's defined load covers: the ones opened, the committed trace's when channels is
    None, each with a load frame in frames; an opened channel without one is refused (B)."""
    channels = fixture() if channels is None else channels
    unframed = sorted(ch for ch in channels if ch not in frames)
    if unframed:
        raise Refusal(f'{name}: the image opens {unframed}, which no load frame defines (LOAD_FRAME_BYTES)')
    return [ch for ch in scenario.CONTRACT.channels if ch.name in channels]
