# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Clock the budget stimulus at its own point without changing the 100 MHz scripts."""


from collections.abc import Callable
from functools import wraps


def at_clock(factory: Callable[[object, dict], list]) -> Callable[[object, dict], list]:
    """Give every variant and reference group the bus clock recorded by its build."""
    @wraps(factory)
    def groups(point: object, spec: dict) -> list:
        """Construct the groups and attach the clock used when their scripts are rendered."""
        made = factory(point, spec)
        for group in made:
            group.sys_hz = spec.get('sys_hz', 100_000_000)
        return made
    return groups


def clocked_step(step: str, sys_hz: int) -> str:
    """Convert legacy 100 MHz temporal cycle counts to the point's clock, rounding up.

    Frame bytes, counts, protocol milliseconds and the one-cycle pulse/gap stay
    untouched. At 100 MHz the script stays byte-identical.
    """
    if sys_hz == 100_000_000:
        return step
    words = step.split()
    indices = []
    if words[:2] == ['wait', 'cycles']:
        indices.append(2)
    if words[:3] == ['wait', 'flash', 'idle']:
        indices.append(3)
    if words and words[0] == 'wait' and words[-2:-1] == ['within']:
        indices.append(len(words) - 1)
    if words[:1] == ['gap'] and int(words[1]) > 1:
        indices.append(1)
    for index in indices:
        words[index] = str((int(words[index]) * sys_hz + 99_999_999) // 100_000_000)
    return ' '.join(words)
