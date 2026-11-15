#!/usr/bin/env python3
"""Each new control can fail for the defect it claims to detect: with rows_tiers.tx_statements made blind to 8x8/2if
(it checks 1x1/1if alone), the two TX statement controls (rows_tiers.channel_controls, flip_grade.channel_controls)
must escape by name; at the head both must hold. Run from the tree's top."""
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path('tb/verilator/ctrl_service_budget').resolve()))
import flip_grade  # noqa: E402
import rows_tiers  # noqa: E402

NAME = "THE TRANSMIT's stated figure under its row"


def escaped():
    root = Path('.').resolve()
    return ([e for e in rows_tiers.channel_controls(root) if e == NAME],
            [e for e in flip_grade.channel_controls(root) if e == NAME])


def main():
    real = rows_tiers.tx_statements
    head = escaped()
    print(f'at the head: rows_tiers escaped {head[0]}, flip_grade escaped {head[1]}')
    blind = lambda r, points=rows_tiers.POINTS, texts=None: real(r, tuple(p for p in points if p == '1x1/1if'), texts)
    with mock.patch.object(rows_tiers, 'tx_statements', blind):
        planted = escaped()
    print(f'tx_statements blind to 8x8/2if: rows_tiers escaped {planted[0]}, flip_grade escaped {planted[1]}')
    ok = head == ([], []) and planted == ([NAME], [NAME])
    print(f'RESULT: {"PASS" if ok else "FAIL"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
