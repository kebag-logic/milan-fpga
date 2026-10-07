#!/usr/bin/env python3
"""Recheck every compared artifact's bytes and publish the digest population."""
import json
from pathlib import Path
import sys

packet = Path(sys.argv[1])
rows = []
for config in ('ax7101_8x8', 'ax7101_1x1_tdm8'):
    root = packet / 'scratch/ax'
    base = json.loads((root / f'baseline-fixed-{config}.json').read_text())
    head = json.loads((root / f'candidate-fixed-{config}.json').read_text())
    assert base == head
    for key in base['files']:
        assert (root / 'snapshots/baseline-fixed' / config / key).read_bytes() == (root / 'snapshots/candidate-fixed' / config / key).read_bytes()
    rows.append({'config': config, 'base': 'e21c1ca024d37ea188ad15b5c8f9c2dae18628df',
                 'head': 'd6b6ca899ae4c248a1342867bb89060e24febcd5', 'raw_byte_equal': True,
                 'count': len(base['files']), 'total_bytes': sum(f['bytes'] for f in base['files'].values()),
                 'files': base['files']})
print(json.dumps(rows, indent=2))
