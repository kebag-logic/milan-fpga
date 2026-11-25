# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#920's mutants of the self-test (selftest_mutants.py): a burst's and a change in flight's grade
(save_burst.py), each replacing one of its rules with a plausible defect; selftest_mutants.MUTANTS takes them
first, in this order."""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import save_burst
import save_grade


def _burst_cut_any_slot(path: Path, image: int, base: int) -> tuple:
    """save_burst.journal reading slot A whatever the two slots' sequences."""
    data = path.read_bytes()
    seq = save_burst.accepted(data[:image], image)
    return seq, save_burst.held_names(data[:image], image, base) if seq is not None else {}


MUTANTS: dict[str, Callable[[], list]] = {
    'burst: a container is accepted whatever its CRC': lambda: [patch.object(
        save_burst, 'accepted', lambda blob, image: int.from_bytes(blob[8:12], 'little'))],
    'burst: the cut is not read': lambda: [patch.object(
        save_burst, 'journal', lambda path, image, base: (1, dict(enumerate([b'burst 000'.ljust(64, b'\0'),
                                                                             b'burst 001'.ljust(64, b'\0')]))))],
    'burst: the cut reads slot A whatever the sequences': lambda: [patch.object(
        save_burst, 'journal', _burst_cut_any_slot)],
    "burst: a SET_NAME's status is not read": lambda: [patch.object(
        save_burst, 'responses', lambda log, _r=save_burst.responses: {k: (c, 0) for k, (c, _) in _r(log).items()})],
    'burst: a delta frame is not a save': lambda: [patch.object(
        save_burst, 'frame_saves', lambda log, image, blocks: [])],
    "burst: a slot's delta frames are not applied": lambda: [patch.object(
        save_burst, 'slot_state', lambda slot, image: (save_burst.accepted(bytes(slot[:image]), image),
                                                       bytes(slot[:image])))],
    "save: a whole save's pages run to the next erase, a delta frame's with them": lambda: [patch.object(
        save_grade, 'container_end', lambda log, erase, stop, base: None)],
    "flight: the next save's steps are not counted": lambda: [patch.object(
        save_burst, 'next_steps', lambda log, done, spec, image: dict(steps=0, want=0, gap_ms=0))],
}
