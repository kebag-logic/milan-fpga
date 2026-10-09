#!/usr/bin/env python3
"""Check fixture custody on a completed scratch build; restore every mutation."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / 'tb/verilator/fw_service_budget'))
import gen_oracle

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--small-build', type=Path, required=True)
args = parser.parse_args()
root = args.small_build
stem = 'service-all-1-0-0'
controls = (
    (root / (stem + '.log'), 'log', 'fixture log digest mismatch'),
    (root / (stem + '.json'), 'media', 'fixture media differs from current built image'),
    (root / 'service_spec.json', 'build', 'stale or unbound fixture build'),
)
for path, kind, expected in controls:
    original = path.read_bytes()
    try:
        if kind == 'log':
            path.write_bytes(original + b'\n')
        else:
            changed = json.loads(original)
            if kind == 'media':
                changed['media']['image_bytes'] += 1
            else:
                key = next(iter(changed['build_hashes']))
                changed['build_hashes'][key] = '0' * 64
            path.write_text(json.dumps(changed) + '\n')
        try:
            gen_oracle.convert(root, 'all')
        except RuntimeError as error:
            if str(error) != expected:
                raise RuntimeError('wrong refusal for ' + kind + ': ' + str(error)) from error
            print(kind + ': refused as ' + expected, flush=True)
        else:
            raise RuntimeError('planted ' + kind + ' mutation survived')
    finally:
        path.write_bytes(original)
print('generator custody controls: 3 passed')
