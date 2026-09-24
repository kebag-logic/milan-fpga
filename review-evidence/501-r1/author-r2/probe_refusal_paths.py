#!/usr/bin/env python3
"""Exercise unrelated exit-1 output and a traceback following a named finding."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
source = root / 'scripts/check_nvm_record_space.py'
original = source.read_text()
old = '    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])\n'
assert original.count(old) == 1
cases = {
    'unrelated_finding': '    print("FINDING: unrelated refusal")\n    raise SystemExit(1)\n',
    'named_without_finding': '    print("is claimed by both FMT_IN[0] and FMT_OUT[0]")\n    raise SystemExit(1)\n',
    'finding_then_crash': '    print("FINDING: is claimed by both FMT_IN[0] and FMT_OUT[0]")\n    raise RuntimeError("crash after named finding")\n',
}
env = os.environ.copy()
env['PYTHONPATH'] = str(root / 'scripts')
env['PYTHONDONTWRITEBYTECODE'] = '1'
with tempfile.TemporaryDirectory(prefix='501-refusal-') as temporary:
    copied = Path(temporary) / source.name
    for name, replacement in cases.items():
        copied.write_text(original.replace(old, replacement))
        result = subprocess.run([sys.executable, str(copied), '--self-test', '--quiet'],
            cwd=root, env=env, text=True, capture_output=True, timeout=600)
        refusal = next((line for line in result.stdout.splitlines()
            if 'SELF-TEST FAILED: negative control --mutate=collide:' in line), None)
        assert result.returncode == 1 and refusal, (name, result)
        print(name, 'rc=1:', refusal)
assert source.read_text() == original
print('source SHA-256 unchanged:', hashlib.sha256(source.read_bytes()).hexdigest())
