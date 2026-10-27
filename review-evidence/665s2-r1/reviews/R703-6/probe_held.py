#!/usr/bin/env python3
"""Probe ctrl_configs.held's found-by-text cross-check on a stub capture.

Usage: python3 -I probe_held.py <checkout root>
Runs held() with every known builder marked as run and nothing compiled,
scope --without verilator, (a) with the dicts as committed, (b) with each of
the six CPU budget harness entries removed alone, (c) with all six removed
(the dict state at the previous head). Prints each refusal's harness names.
Mutates only in-process copies of the dicts; writes nothing.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import ctrl_configs as cc  # noqa: E402

H = 'tb/verilator/ctrl_service_budget/'
SIX = [H + n for n in ('build.py', 'runtime_ssp.py', 'scenario.py', 'selftest.py', 'split_soc.py',
                       'fixture_variant.py')]
# every file found by text outside the harness counts as compiled in the stub capture, as the real capture's
# builds compile the modules and PART_OF programs among them (they are not under test here)
compiled = {cc.rel(p) for p in cc.builder_texts() if cc.rel(p) not in SIX}
stub = SimpleNamespace(ran={b.path for b in cc.BUILDERS}, builders=compiled, bypassed=[], leaves=[])
scope = cc.Scope(without=frozenset({'verilator'}))
O0, S0 = dict(cc.OUTSIDE), dict(cc.SUITES)


def attempt(drop):
    cc.OUTSIDE.clear(); cc.OUTSIDE.update({k: v for k, v in O0.items() if k not in drop})
    cc.SUITES.clear(); cc.SUITES.update({k: v for k, v in S0.items() if k not in drop})
    try:
        cc.held(stub, scope)
        return 'ACCEPTED', []
    except cc.Refusal as exc:
        text = str(exc)
        return 'REFUSED', [n for n in SIX if n in text], text


fails = 0
r = attempt(set())
print('committed:', r[0], r[1])
fails += r[0] != 'ACCEPTED'
for name in SIX:
    where = 'OUTSIDE' if name in O0 else 'SUITES' if name in S0 else 'NONE'
    r = attempt({name})
    ok = r[0] == 'REFUSED' and r[1] == [name]
    fails += not ok
    print(f'drop {name} ({where}):', r[0], r[1], 'OK' if ok else 'UNEXPECTED')
r = attempt(set(SIX))
print('drop all six:', r[0], r[1])
fails += not (r[0] == 'REFUSED' and r[1] == SIX)
if r[0] == 'REFUSED':
    print('REFUSAL TEXT:', r[2])
print('probe_held:', 'PASS' if not fails else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
