#!/usr/bin/env python3
"""load_split.py TREE COSTS_DIR: the 8x8/2if load with ACMP's owed-frame item taken three ways (recorded, not graded;
#665 issuecomment-6811790762): as the committed rule measures it (the whole poll), the poll less the acmp_rx calls nested
in it (acmp-item-parts-8x8.txt: 6,302 CPU cycles), and the core's poll alone (3,990). Each stated as load_grade states a
cost (the most cycles plus 5 %, rounded up to 5 us), never below the committed donor column, in load_r2.json's column."""
import json, math, sys
from pathlib import Path
tree, costs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
stated = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)
col = json.loads((costs / 'load_r2.json').read_text())['column']['8x8/2if']
for label, cycles in (('the whole poll (the committed rule)', None), ('the poll less its nested acmp_rx', 6302),
                      ("the core's poll alone", 3990)):
    c = dict(col)
    if cycles is not None:
        c['item.acmp'] = max(stated(cycles), load_grade.STATED_US_DONOR['8x8/2if']['item.acmp'])
    terms = load_grade.load(tree, '8x8/2if', {'8x8/2if': c})
    print(f"8x8/2if, item.acmp {c['item.acmp']} us, {label}: load {sum(terms.values()):.3f} (item.acmp term {terms['item.acmp']:.3f})")
