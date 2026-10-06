#!/usr/bin/env python3
"""Read stamp dimensions from the completed one- and two-interface models."""
import argparse
import json
from pathlib import Path
import re

ap = argparse.ArgumentParser()
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
p = a.packet.resolve()
rows = []
for count, name in [(1, 'obj_dir'), (2, 'obj_if2')]:
    declarations = []
    for f in (p / 'scratch/guards-tree/tb/aecp_notify' / name).glob('*.h'):
        for line in f.read_text().splitlines():
            if 'ctr_last_r' in line:
                declarations.append((f.name, line.strip()))
    assert len(declarations) == 1, declarations
    filename, declaration = declarations[0]
    match = re.search(r'VlUnpacked<IData/\*31:0\*/, (\d+)>', declaration)
    assert match, declaration
    stamps = int(match[1])
    assert stamps == 1 + 1 + 1 + count, (name, stamps)
    rows.append({'interfaces': count, 'streams_in': 1, 'streams_out': 1,
                 'stamps': stamps, 'bits': stamps * 32, 'source_file': filename,
                 'declaration': declaration, 'pass': True})
(p / 'receipts/compiled-stamp-shapes.json').write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps(rows))
