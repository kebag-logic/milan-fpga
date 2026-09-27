#!/usr/bin/env python3
"""Compare a #397 receipt's tracked input hashes with a checkout and generated dir.

Usage: receipt_drift.py <receipt.json> <checkout> <generated-shape-dir>
Prints each recorded source/generated file whose bytes differ at the checkout.
"""
import hashlib
import json
import sys
from pathlib import Path

receipt, root, gen = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2]), Path(sys.argv[3])
same = differ = skipped = 0
for key in ('input_hashes', 'build_hashes'):
    for rel, digest in sorted(receipt[key].items()):
        if rel.startswith('build/generated/'):
            path = gen / Path(rel).name
        elif rel.startswith('build/') or rel.startswith('external/'):
            skipped += 1
            continue
        else:
            path = root / rel
        now = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else 'ABSENT'
        if now == digest:
            same += 1
        else:
            differ += 1
            print(f'DIFFERS {key} {rel} recorded={digest[:16]} now={now[:16]}')
print(f'same={same} differ={differ} skipped_build_outputs={skipped}')
