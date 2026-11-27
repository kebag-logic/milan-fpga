# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The load gate's planted controls of the deliveries term (load_grade.py's term list; #977, the manager's decision of
2026-11-27 on the deferred deliveries): the binding changes and loss completions a registering record defers, one a
delivery, into the polls' base of the passes after it. Each control is refused by load_grade.py --check itself
(delivery_findings), the head's by none.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock


def controls(root: Path) -> list[str]:
    """The deliveries term left out, counted at half its rate, or stated at none or under its dearest-before figure:
    the planted names that escaped."""
    import load_grade
    escaped = ['the head refused'] if load_grade.delivery_findings(root) else []
    real = load_grade.load

    def without(root_: Path, point: str, table: dict | None = None) -> dict[str, float]:
        """The load with no deliveries term."""
        return {k: v for k, v in real(root_, point, table).items() if k != 'deliveries'}

    def halved(root_: Path, point: str, table: dict | None = None) -> dict[str, float]:
        """The load with the deliveries term at half its rate."""
        return {k: v / 2 if k == 'deliveries' else v for k, v in real(root_, point, table).items()}
    for name, patch in (('the deliveries term left out', mock.patch.object(load_grade, 'load', without)),
                        ('the deliveries term counted at half its rate', mock.patch.object(load_grade, 'load', halved)),
                        ('the deliveries cost stated at none', mock.patch.dict(load_grade.DELIVERY_US, clear=True))):
        with patch:
            if not any('but not the deliveries' in f for f in load_grade.findings(root)):
                escaped.append(name)
    low = load_grade.DELIVERY_US_DEAREST['8x8/1if'] - 5
    with mock.patch.dict(load_grade.DELIVERY_US, {'8x8/1if': low}):
        if not any('under its dearest-before figure' in f for f in load_grade.findings(root)):
            escaped.append('the deliveries cost stated under its dearest-before figure')
    return escaped


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import load_grade as _lg
    missed = controls(_lg.ROOT)
    print('\n'.join(f'ESCAPED {n}' for n in missed) or 'every deliveries control refused')
    sys.exit(1 if missed else 0)
