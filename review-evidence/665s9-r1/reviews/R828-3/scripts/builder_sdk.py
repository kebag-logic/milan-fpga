"""Run sw/builder/test_builder.py --require-rv32 from the current checkout with the native
RV32 compiler path mapped to the pinned SDK compiler (same mapping as the manager's candidate run).
argv: <records.jsonl> [extra test_builder args...]"""
from pathlib import Path
import json, runpy, subprocess, sys
from unittest.mock import patch
native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
sdk = '$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
records = Path(sys.argv[1]); extra = sys.argv[2:]
assert not records.exists(), records
real_run = subprocess.run
def selected_run(args, *a, **k):
    if isinstance(args, (list, tuple)) and args and str(args[0]) == native:
        actual = [sdk, *args[1:]]
        r = real_run(actual, *a, **k)
        with records.open('a') as f:
            f.write(json.dumps(dict(requested=list(args), executed=actual, exit_code=r.returncode)) + '\n')
        return r
    return real_run(args, *a, **k)
subprocess.run(['python3', 'scripts/ci_rv32_sdk.py', '--destination', str(Path(sdk).parents[1]), '--verify-only'], check=True)
print('compiler argv mapping:', native, '->', sdk, flush=True)
sys.argv = ['sw/builder/test_builder.py', '--require-rv32', *extra]
with patch('subprocess.run', selected_run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
