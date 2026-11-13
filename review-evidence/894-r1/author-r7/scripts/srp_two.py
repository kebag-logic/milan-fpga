"""Run named SRP defects of srp_mutants.DEFECTS alone, by the campaign's own driver, against a tree.
usage: srp_two.py TREE OUT NAME..."""
import sys
from pathlib import Path
tree, out, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import srp_mutants as m
m.DEFECTS = [d for d in m.DEFECTS if d.name in names]
assert len(m.DEFECTS) == len(names), [d.name for d in m.DEFECTS]
sys.exit(1 if m.campaign(out, tree / 'third_party/lwSRP', jobs=4) else 0)
