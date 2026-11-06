#!/usr/bin/env python3
"""R784-3: the case F-1 asks for, tried on a disposable copy. usage: fix_feasibility.py HARNESS_DIR"""
import sys
from pathlib import Path
h = Path(sys.argv[1]).resolve()
p = h / 'hooks_selftest.py'
t = p.read_text()
old = "    expect(len(got['refusals']) == 1, f'another path: {got}')\n"
new = old + ("    got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [dict(again, path=['acmp.entity_available', 1])]})\n"
             "    expect(len(got['refusals']) == 1 and not got['superseded'], f'a row of another path: {got}')\n")
assert t.count(old) == 1
p.write_text(t.replace(old, new))
