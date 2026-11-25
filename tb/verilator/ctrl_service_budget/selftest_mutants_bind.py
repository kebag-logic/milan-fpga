# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#1009's mutants of the self-test (selftest_mutants.py): the binding grade's rules (bind_save.py), each replaced with a
plausible defect."""
from __future__ import annotations

from collections.abc import Callable
from unittest.mock import patch

import bind_save


MUTANTS: dict[str, Callable[[], list]] = {
    "bind: a command's status is not read": lambda: [patch.object(
        bind_save, 'responses', lambda log, _r=bind_save.responses: {k: (c, 0) for k, (c, _) in _r(log).items()})],
    'bind: the target is not held': lambda: [patch.object(
        bind_save, 'misses', lambda g, group, _m=bind_save.misses: [w for w in _m(g, group)
                                                                    if 'over its target' not in w])],
    'bind: a save that began before the response counts': lambda: [patch.object(
        bind_save, 'first_durable', lambda done, cycle, sink, want, image, base, _f=bind_save.first_durable:
        _f(done, -1, sink, want, image, base))],
    "bind: a save's contents are not read": lambda: [patch.object(
        bind_save, 'held', lambda blob, image, base: {s: bind_save.bound_payload() for s in range(64)})],
    "bind: the cut's container is not read": lambda: [patch.object(
        bind_save, 'bind_of', lambda path, image, base: {s: bind_save.bound_payload() for s in range(64)})],
    'bind: a missing journal passes': lambda: [patch.object(
        bind_save, 'misses', lambda g, group, _m=bind_save.misses: [w for w in _m(g, group)
                                                                    if 'left no journal' not in w])],
    'bind: an unanswered command is not refused': lambda: [patch.object(
        bind_save, 'responses', lambda log, _r=bind_save.responses: {**{0x9500: (1000, 0)}, **_r(log)})],
}
