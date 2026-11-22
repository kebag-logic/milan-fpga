#!/usr/bin/env python3
"""Compare the in-memory generation receipts without rebuilding anything."""
import json
from pathlib import Path
p = Path(__file__).resolve().parent
a = json.loads((p / 'configs-base.json').read_text())
b = json.loads((p / 'configs-head.json').read_text())
with (p / 'config-comparison.txt').open('w') as f:
    for k in a:
        changed = [x for x in a[k]['hashes'] if a[k]['hashes'][x] != b[k]['hashes'][x]]
        if 'ax7101_8x8' not in k:
            assert not changed, (k, changed)
        f.write(f"{k}: {len(a[k]['hashes'])} compared; changed={changed}; model {a[k]['id']} -> {b[k]['id']}\n")
print((p / 'config-comparison.txt').read_text())
