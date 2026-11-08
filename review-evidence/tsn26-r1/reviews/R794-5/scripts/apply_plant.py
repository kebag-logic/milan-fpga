#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# usage: apply_plant.py TREE NAME [PLANTS_JSON]
# Applies one plant to a disposable TREE: a reviewer plant object from PLANTS_JSON if its name matches,
# else the registered plant of that name in TREE/tests/mutations.json. The old text must occur once.
import json, sys
from pathlib import Path
tree, name = Path(sys.argv[1]), sys.argv[2]
mine = [p for p in json.loads(Path(sys.argv[3]).read_text()) if isinstance(p, dict)] if len(sys.argv) > 3 else []
reg = json.loads((tree / 'tests/mutations.json').read_text())
p = {x['name']: x for x in reg + mine}[name]
f = tree / p['path']
t = f.read_text()
assert t.count(p['old']) == 1, (name, t.count(p['old']))
f.write_text(t.replace(p['old'], p['new']))
print('applied', name)
