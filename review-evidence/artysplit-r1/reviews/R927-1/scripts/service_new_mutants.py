#!/usr/bin/env python3
"""Run the service-budget self-test's checks under the mutants this change adds
(the two Arty clock mutants), each of which must turn a check red, and under no
mutant, which must pass.

usage: python3 service_new_mutants.py <repo>
"""
from __future__ import annotations

import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    here = Path(argv[0]).resolve() / 'tb/verilator/ctrl_service_budget'
    sys.path.insert(0, str(here))
    import grade  # noqa: E402
    import selftest  # noqa: E402
    import selftest_mutants  # noqa: E402
    names = [n for n in selftest_mutants.MUTANTS if n.startswith('clock: ')]
    print('new mutants:', names)
    bad = 0
    failed = [n for n, ok, _ in selftest.checks() if not ok]
    print(f'unmutated: {len(failed)} failing checks' + (f': {failed[:3]}' if failed else ''))
    bad += bool(failed)
    for name in names:
        with selftest.mutated(name):
            try:
                failed = [n for n, ok, _ in selftest.checks() if not ok]
            except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
                failed = [f'refused: {error}']
        print(f'MUTANT {"caught" if failed else "ESCAPED"}: {name}' + (f': {failed[0]}' if failed else ''))
        bad += not failed
    print(f'RESULT: {"PASS" if not bad else "FAIL"}')
    return int(bool(bad))


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
