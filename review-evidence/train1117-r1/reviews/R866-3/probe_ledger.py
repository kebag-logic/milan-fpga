#!/usr/bin/env python3
"""Focused memory refusal and ledger mutation checks; no full builder bank."""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path.cwd() / 'sw/litex'))
import test_ctrl_memory as test

problems = []
with tempfile.TemporaryDirectory(prefix='ledger-probe-') as name:
    out = pathlib.Path(name)
    test.check_arms(problems, out)
    test.ledger_plant_arms(problems, out, {'checks'} if not problems else set())
    # Explicitly check the moved fixture still reaches the next half-tile,
    # and the smaller control remains an actual budget failure.
    for tiles in (62.5, 63.0, 63.5):
        case = test.ledgers.OWN[test.ledgers.PLATFORM]._replace(tiles=tiles)
        path = test.ledger_elf(out, case)
        image = test.ctrl_memory.read_elf(path)
        unbounded = test.ctrl_memory.plan(image, budget=float('inf'))
        assert unbounded.tiles == tiles
        try:
            test.ctrl_memory.plan(image, ledgered=test.ledgers.PLATFORM)
            result = 'accepted'
        except test.ctrl_memory.Refusal as exc:
            result = exc.check
        print('BOUNDARY', tiles, result)
        assert result == ('accepted' if tiles <= 63 else 'allocation over budget')
print('focused ledger probe:', len(problems), 'failures')
for p in problems:
    print('FAIL', p)
raise SystemExit(bool(problems))
