#!/usr/bin/env python3
"""R738-F2's real-build probe, on one point's fresh run: --regrade with the capture build's cpu_hz deleted
must exit 2 and leave refused.json alone (no table.md, no results.json); with build.json restored byte for
byte, --regrade must exit 0 and reproduce the fresh run's table.md and results.json byte for byte, with no
refusal left.

Usage, from the checkout, in the gate environment: real_refusal_probe.py POINT BUILD_DIR
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

point, root = sys.argv[1], Path(sys.argv[2])
out, build_json = root / 'results', root / 'capture-all' / 'build.json'
sha = lambda data: hashlib.sha256(data).hexdigest()
fresh = {name: (out / name).read_bytes() for name in ('results.json', 'table.md')}
original = build_json.read_bytes()
listing = lambda: sorted(p.name for p in out.iterdir() if p.name in ('results.json', 'table.md', 'refused.json'))


def regrade() -> int:
    """run.py --regrade of the recorded run; its rc."""
    argv = [sys.executable, '-B', 'tb/verilator/nvm_split_target/run.py', '--point', point, '--build-dir', str(root),
            '--regrade', '--jobs', '8']
    print('COMMAND', ' '.join(argv[1:3]), *argv[3:5], '--build-dir <build-dir> --regrade --jobs 8', flush=True)
    done = subprocess.run(argv, capture_output=True, text=True, check=False)
    print('\n'.join(line for line in done.stdout.splitlines() if line.startswith('REFUSED')) or '(no REFUSED line)')
    return done.returncode


print(f'fresh run: table.md {sha(fresh["table.md"])}, results.json {sha(fresh["results.json"])}')
spec = json.loads(original)
del spec['cpu_hz']
build_json.write_text(json.dumps(spec, indent=1) + '\n')
try:
    rc = regrade()
    left = listing()
    refused = json.loads((out / 'refused.json').read_text()) if 'refused.json' in left else {}
    print(f'missing cpu_hz: rc {rc}; left {left}; refused.json top keys {sorted(refused)}')
    first = rc == 2 and left == ['refused.json'] and sorted(refused) == ['record', 'refused']
finally:
    build_json.write_bytes(original)
print(f'build.json restored: {sha(build_json.read_bytes()) == sha(original)}')
rc = regrade()
left = listing()
same = all((out / name).read_bytes() == data for name, data in fresh.items() if (out / name).is_file())
print(f'restored: rc {rc}; left {left}; table.md and results.json byte-identical to the fresh run: {same}')
second = rc == 0 and left == ['results.json', 'table.md'] and same
print('PROBE PASS' if first and second else 'PROBE FAIL')
sys.exit(0 if first and second else 1)
