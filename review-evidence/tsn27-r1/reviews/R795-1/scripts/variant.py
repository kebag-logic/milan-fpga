#!/usr/bin/env python3
"""Edit one exported tree: apply a wire.h substitution or registered plant, optionally drop W1."""
import argparse, json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('tree', type=Path)
p.add_argument('--plant', help='registered plant name from tests/mutations.json')
p.add_argument('--old'); p.add_argument('--new')
p.add_argument('--wire-from', type=Path, help='replace include/wire.h with this file')
p.add_argument('--drop-w1', action='store_true')
a = p.parse_args()
if a.old is not None and not a.plant:
    a.old, a.new = (x.encode().decode('unicode_escape') for x in (a.old, a.new))
wire = a.tree / 'include/wire.h'
if a.wire_from:
    wire.write_text(a.wire_from.read_text())
if a.plant:
    m = next(m for m in json.loads((a.tree / 'tests/mutations.json').read_text()) if m['name'] == a.plant)
    a.old, a.new = m['old'], m['new']
    target = a.tree / m['path']
else:
    target = wire
if a.old is not None:
    t = target.read_text(); assert t.count(a.old) == 1, a.old
    target.write_text(t.replace(a.old, a.new))
if a.drop_w1:
    f = a.tree / 'tests/test_acmp.cpp'; s = f.read_text()
    start = s.index('// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)')
    end = s.index('\n}\n', start) + 3
    s = s[:start] + s[end:]; assert 'W1PutBe' not in s
    f.write_text(s)
print('edited', a.tree)
