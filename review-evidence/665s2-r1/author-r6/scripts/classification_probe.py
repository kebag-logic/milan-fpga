#!/usr/bin/env python3
"""Run ctrl_configs.held's found-by-text classification on the checkout, then once per harness entry with
that entry removed. The capture is a stub: every known builder ran, nothing was bypassed and no compile is
recorded, and every module found by text that is no program, and every PART_OF program, is taken as having
compiled, except the CPU budget harness's. So the only refusals left are the classification's own.

Usage: classification_probe.py CHECKOUT
Prints one line per case; exit 0 only if the checkout's run passes and every removal refuses its own file by name.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import ctrl_configs as cc  # noqa: E402

HARNESS = 'tb/verilator/ctrl_service_budget/'
texts = cc.builder_texts()
compiled = {cc.rel(p) for p, t in texts.items() if not cc.program(p, t) and not cc.rel(p).startswith(HARNESS)}
compiled |= set(cc.PART_OF)  # each compiles under the builder it runs under, in a real capture
capture = SimpleNamespace(ran=frozenset(b.path for b in cc.BUILDERS), builders=frozenset(compiled), bypassed=[],
                          leaves=[])
scope = cc.Scope(without=frozenset({'verilator'}))


def held() -> str:
    """The refusal held gives, or PASS."""
    try:
        cc.held(capture, scope)
    except cc.Refusal as refusal:
        return f'REFUSED: {refusal}'
    return 'PASS'


found = sorted(cc.rel(p) for p in texts if cc.rel(p).startswith(HARNESS))
print('found by text under the harness:', ', '.join(found))
base = held()
print('checkout as is:', base)
ok = base == 'PASS'
for table in (cc.OUTSIDE, cc.SUITES):
    for name in [n for n in table if n.startswith(HARNESS)]:
        reason = table.pop(name)
        got = held()
        table[name] = reason
        caught = got.startswith('REFUSED: ') and f'{name} names the firmware' in got
        others = [r for r in got.removeprefix('REFUSED: ').split('; ') if not r.startswith(name)]
        ok &= caught and not others
        print(f"{'CAUGHT' if caught and not others else 'NOT CAUGHT'}: without {name}: {got}")
sys.exit(0 if ok else 1)
