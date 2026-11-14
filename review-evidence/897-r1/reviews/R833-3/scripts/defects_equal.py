"""Compare aecp_mutants.DEFECTS between two extracted test trees (name, file, old, new, checks)."""
import importlib, sys, json
def load(d):
    for m in [k for k in sys.modules if k.startswith('aecp')]:
        del sys.modules[m]
    sys.path.insert(0, d)
    try:
        mod = importlib.import_module('aecp_mutants')
        rows = [(x.name, str(x.path).split('sw/firmware/ctrl/')[-1], x.old, x.new, tuple(map(tuple, x.checks)) if not isinstance(x.checks[0], str) else x.checks) for x in mod.DEFECTS]
    finally:
        sys.path.remove(d)
    return rows
a = load(sys.argv[1]); b = load(sys.argv[2])
print('pre', len(a), 'head', len(b))
print('names unique', len({r[0] for r in a}) == len(a), len({r[0] for r in b}) == len(b))
print('same set of rows', sorted(map(repr, a)) == sorted(map(repr, b)))
print('same order', a == b)
moved = [r[0] for r in b if r[0].startswith('face-as-path')]
print('face-as-path rows at head', len(moved), moved)
