from pathlib import Path
import json
import runpy
import subprocess
import sys
from unittest.mock import patch

native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
sdk = '$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc'
records = Path(__file__).resolve().parent / 'builder-sdk-argv.jsonl'
real_run = subprocess.run

def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) == native:
        actual = [sdk, *args[1:]]
        result = real_run(actual, *positional, **keyword)
        with records.open('a') as receipt:
            receipt.write(json.dumps(dict(requested=list(args), executed=actual,
                                          exit_code=result.returncode)) + '\n')
        return result
    return real_run(args, *positional, **keyword)

subprocess.run(['python3', 'scripts/ci_rv32_sdk.py', '--destination',
                str(Path(sdk).parents[1]), '--verify-only'], check=True)
print('Pinned SDK compiler selected; installation remains read-only.', flush=True)
sys.argv = ['sw/builder/test_builder.py', '--require-rv32']
with patch('subprocess.run', selected_run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
assert records.exists() and records.stat().st_size > 0
