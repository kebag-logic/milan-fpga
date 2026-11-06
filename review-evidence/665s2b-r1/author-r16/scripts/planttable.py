#!/usr/bin/env python3
"""HANDOFF section 3's plant table (#665, round 16): every plant this round adds, its test and the failing words its
campaign's needle matches, read off the committed plant lists.

usage: planttable.py CHECKOUT OUT.md
"""
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import loop_step_mutants  # noqa: E402
import srp_transmit_mutants  # noqa: E402


def loop_kind(name, path, old, new, arm, test, needle, **kw):
    return ('loop', name, path, arm, test, needle)


def srp_kind(name, test, old, new, needle, **kw):
    return ('srp', name, kw.get('path', 'srp/srp_mbx.c'), 'srp', test, needle)


rows = [*loop_step_mutants.transmit_mutants(loop_kind), *loop_step_mutants.tick_mutants(loop_kind),
        *srp_transmit_mutants.defects(srp_kind)]
lines = ['| # | Campaign | Plant | File | Test | Failing words |', '|---:|---|---|---|---|---|']
for n, (camp, name, path, arm, test, needle) in enumerate(rows, 1):
    lines.append(f'| {n} | {camp} | `{name}` | `{path}` | `{test}` | {needle} |')
out.write_text('\n'.join(lines) + '\n')
print(len(rows), 'plants;', sum(r[0] == 'loop' for r in rows), 'loop,', sum(r[0] == 'srp' for r in rows), 'srp')
