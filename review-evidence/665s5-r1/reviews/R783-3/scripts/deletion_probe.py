#!/usr/bin/env python3
"""Own deletion probes: drop named assertions from the self-test's source, in memory, and list the mutants that escape.

usage: deletion_probe.py TREE   (nothing in TREE is written)
"""
import ast, sys, types
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
tree = Path(sys.argv[1]).resolve()
path = tree / 'tb/verilator/ctrl_service_hooks/hooks_selftest.py'
sys.path.insert(0, str(path.parent)); sys.dont_write_bytecode = True
SOURCE = path.read_text(); N = 0
def load(src):
    global N; N += 1
    m = types.ModuleType(f'st{N}'); m.__file__ = str(path); sys.modules[m.__name__] = m
    exec(compile(src, str(path), 'exec'), m.__dict__); return m
def drop(src, needle):
    """Replace the one `expect(...)` statement holding needle by pass."""
    hits = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
            and getattr(n.value.func, 'id', '') == 'expect' and needle in ast.get_source_segment(src, n)]
    assert len(hits) == 1, (needle, len(hits))
    n = hits[0]; lines = src.split('\n'); first = lines[n.lineno - 1]
    lines[n.lineno - 1:n.end_lineno] = [first[:len(first) - len(first.lstrip())] + 'pass'] + [''] * (n.end_lineno - n.lineno)
    return '\n'.join(lines)
def outcome(m, extra=()):
    fail = {k: v for k, v in m.run_checks().items() if v}
    esc = []
    for name, make, named in [*m.MUTANTS, *extra]:
        with ExitStack() as s:
            s.enter_context(make())
            try:
                m.CHECKS[named](); esc.append(name)
            except Exception:
                pass
    return fail, esc
def probe(label, needles=(), sub=(), extra_fn=None):
    src = SOURCE
    for x in needles: src = drop(src, x)
    for a, b in sub:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    m = load(src)
    fail, esc = outcome(m, extra_fn(m) if extra_fn else ())
    print(f'{label}: checks failing {list(fail)}; {len(esc)} escaped {esc}')
ARM = 'the window opens before the arm'
GRADED = 'the amended bounds graded a path'; LATE = "f'findings {late}'"; NO = "the path table\\'s amended figure"
IFACE = "f'other interface: {got}'"; OTHER = "f'another path: {got}'"; POS = "f'superseded: {got}'"
NARROW = "narrow fits, not 1"; HMS = 'the held row reports'; HMG = 'the held margin is {past'
MREC = 'a push never sent records a service'; MID = "f'missing row {identity}'"; HID = "f'held row {identity}'"
probe('head, nothing deleted')
probe('arm rule deleted', [ARM])
probe('grades-nothing verdict assertion deleted', [GRADED])
probe('LATE assertion deleted', [LATE])
probe('both grades-nothing assertions deleted', [GRADED, LATE])
probe('positive supersede assertion deleted', [POS])
probe('other-interface assertion deleted', [IFACE])
probe('another-path assertion deleted', [OTHER])
probe('other-interface and another-path deleted', [IFACE, OTHER])
probe('narrow-count assertion deleted', [NARROW])
probe('held service assertion deleted', [HMS])
probe('held fine margin assertion deleted', [HMG])
probe('held identity assertion deleted', [HID])
probe('missing record assertion deleted', [MREC])
probe('missing identity assertion deleted', [MID])
AT = "('at-swing', 'maap', 20.0 - swing, 0.0, False, 'maap'),"
UN = "('under-swing', 'maap', 20.0 - swing + 1e-5, 0.0, False, 'maap'),"
SL = "expect((slack['at-swing'], slack['under-swing']) == (6490, 6489), f'the rows are not at the swing: {slack}')"
probe('summary row at the swing moved 1 cycle off (slack 6491), slack pin off', sub=[(SL, 'pass'), (AT, "('at-swing', 'maap', 20.0 - swing - 1e-5, 0.0, False, 'maap'),")])
probe('summary row under the swing moved 1 cycle off (slack 6488), slack pin off', sub=[(SL, 'pass'), (UN, "('under-swing', 'maap', 20.0 - swing + 2e-5, 0.0, False, 'maap'),")])
# The D2 shape: the verdict and the column at the point's two interfaces, added as an extra mutant.
def d2(m):
    def shape(r, group):
        out = m.HOOK_ROW(r, group)
        return dict(out, within=not out['unbounded'] and out['ms'] <= m.hooks.amended_ms(out, 2))
    return [('EXTRA verdict reads the column at two interfaces', m.mutant(m.run, 'hook_row', shape), 'the amended column grades nothing')]
probe('head plus the two-interface shape', extra_fn=d2)
probe('two-interface shape, both grades-nothing assertions deleted', [GRADED, LATE], extra_fn=d2)
probe('two-interface shape, those two and the NO pin deleted', [GRADED, LATE, NO], extra_fn=d2)
