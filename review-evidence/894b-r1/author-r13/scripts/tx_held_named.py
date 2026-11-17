#!/usr/bin/env python3
"""flip_grade.py's three new controls at a tree, each by name with the finding that refuses it: 8x8/1if's
CTRL_LOOP_TX_MS planted at each of TX_UNDER_MS (60, 69 and 74 ms) in memory, as tx_held_controls plants it, and the head
unplanted; then the controls as the self-test reads them (tx_held_controls, the names that escape). Read only.
usage: python3 -I tx_held_named.py TREE"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import flip_grade  # noqa: E402
import shape_costs  # noqa: E402

loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
text = (root / loop).read_text()
at = shape_costs.of_point('8x8/1if', root)
print(f'the head unplanted: tx_held findings {flip_grade.tx_held(root, ("8x8/1if",)) or "none"}')
for ms, name in zip(flip_grade.TX_UNDER_MS, flip_grade.TX_HELD_CONTROLS):
    found = flip_grade.tx_held(root, ('8x8/1if',), {loop: shape_costs.planted_at(text, at, shape_costs.TX, ms)})
    named = [f for f in found if f.startswith(f'8x8/1if: CTRL_LOOP_TX_MS states {ms} ms')]
    print(f'{name}: {"REFUSED" if named else "ESCAPED"}: {"; ".join(found) or "no finding"}')
escaped = flip_grade.tx_held_controls(root)
print(f'tx_held_controls: {len(flip_grade.TX_HELD_CONTROLS) - len(escaped)} of {len(flip_grade.TX_HELD_CONTROLS)} '
      f'refused{"; escaped: " + ", ".join(escaped) if escaped else ""}')
sys.exit(1 if escaped else 0)
