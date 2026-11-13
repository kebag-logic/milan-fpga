"""Plant named defects of the control campaign or the AECP campaign: plants.py CHECKOUT OUT ctrl|aecp NAME[,NAME...]"""
import sys
from pathlib import Path
co, out, which, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4].split(',')
sys.path[:0] = [str(co / 'sw/firmware/ctrl/test'), str(co / 'sw/firmware/gtest')]
if which == 'ctrl':
    import ctrl_mutants as m
    table = tuple(x for x in m.MUTANTS if x.name in names)
    assert len(table) == len(names), [n for n in names if n not in {x.name for x in table}]
    m.MUTANTS = table
    m.unnamed_tests = lambda: []
    sys.exit(int(m.campaign(out, out / 'reuse', 8)))
else:
    import aecp_mutants as m
    table = tuple(d for d in m.DEFECTS if d.name in names)
    assert len(table) == len(names), [n for n in names if n not in {d.name for d in table}]
    m.DEFECTS = table
    m.controls = lambda: None
    sys.exit(int(m.campaign(out, jobs=8)))
