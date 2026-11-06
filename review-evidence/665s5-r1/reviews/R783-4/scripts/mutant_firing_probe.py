#!/usr/bin/env python3
"""For each mutant: the assertion it fires first in its named check, whether by assertion or by exception; the
expect sites no mutant fires first; the README rows against the mutant list; every group's supersede-relevant paths.

usage: mutant_firing_probe.py <tree extracted at the exact head>
"""
import ast
import inspect
import re
import sys
from contextlib import ExitStack
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
HERE = TREE / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(HERE))
import hooks_selftest as t  # noqa: E402
hooks, run = t.hooks, t.run

text = (HERE / 'hooks_selftest.py').read_text()
sites = {n.lineno for n in ast.walk(ast.parse(text))
         if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'expect'}
original = t.expect
last = {}


def spying(ok, what):
    """expect, noting the line that fails."""
    if not ok:
        last['line'] = inspect.currentframe().f_back.f_lineno
    original(ok, what)


t.expect = spying
fired = {}
rows = []
for name, make, named in t.MUTANTS:
    with ExitStack() as stack:
        stack.enter_context(make())
        last.clear()
        try:
            t.CHECKS[named]()
            kind, msg = 'NOT FIRED', ''
        except t.Failed as error:
            kind, msg = 'assertion', str(error)
        except Exception as error:  # noqa: BLE001
            kind, msg = 'EXCEPTION', f'{type(error).__name__}: {error}'
    line = last.get('line')
    fired.setdefault(line, []).append(name)
    rows.append((name, named, kind, line, msg[:110].replace('\n', ' ')))
for r in rows:
    print(f'{r[2]:9} L{r[3]} | {r[0]} | {r[1]} | {r[4]}')
print(f'mutants {len(rows)}, by assertion {sum(r[2] == "assertion" for r in rows)}, '
      f'exception {sum(r[2] == "EXCEPTION" for r in rows)}, not fired {sum(r[2] == "NOT FIRED" for r in rows)}')
print(f'expect sites {len(sites)}, fired first by a mutant in its named check {len(sites & set(fired))}, '
      f'by none {len(sites - set(fired))}')

readme = (HERE / 'README.md').read_text()
table = re.findall(r'^\| (.+?) \| (.+?) \|$', readme, re.M)
pairs = {(a, b) for a, b in table}
want = {(n, c) for n, _, c in t.MUTANTS}
print('README rows matching the mutant list', len(pairs & want), 'of', len(want), 'missing', sorted(want - pairs)[:3])
print('names unique', len({n for n, _, _ in t.MUTANTS}) == len(t.MUTANTS))
for stale in ('any later group', 'margin is not recorded', 'its finding is dropped'):
    print(f'stale in the tree: {stale!r}:', stale in readme or stale in text)
