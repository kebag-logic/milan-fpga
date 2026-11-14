#!/usr/bin/env python3
"""plants_equal.py TESTDIR A B: srp_talker_mutants.defects() of two copies, built with a recording kind, compared tuple
by tuple; TESTDIR is the tree's sw/firmware/ctrl/test (for srp_mutants and the module's imports)."""
import importlib.util, sys
testdir, a, b = sys.argv[1:4]
sys.path.insert(0, testdir)
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
rec = lambda *args, **kw: (args, tuple(sorted(kw.items())))
da, db = load(a, 'ma').defects(rec), load(b, 'mb').defects(rec)
print(f'A {len(da)} plants, B {len(db)} plants, identical in order: {da == db}')
for i, (x, y) in enumerate(zip(da, db)):
    if x != y: print('DIFF', i, x[0][0], y[0][0])
sys.exit(0 if da == db else 1)
