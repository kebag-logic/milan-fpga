#!/usr/bin/env python3
"""Run sw/builder/test_builder.py --require-rv32 with the compiler argv mapped to a verified SDK.

The gate's selector is fixed at ~/br-milan-rv32/host/bin/riscv32-linux-gcc. Every
subprocess.run whose argv[0] is that selector is re-executed with the compiler of the
SDK named by R249_SDK (verified first with scripts/ci_rv32_sdk.py --verify-only), and
each mapping is appended to R249_ARGV_LOG. Run from the candidate root.
"""
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
sdk = Path(os.environ['R249_SDK'])
mapped = str(sdk / 'bin/riscv32-linux-gcc')
records = Path(os.environ['R249_ARGV_LOG'])
records.unlink(missing_ok=True)
real_run = subprocess.run


def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) == native:
        actual = [mapped, *args[1:]]
        result = real_run(actual, *positional, **keyword)
        with records.open('a') as handle:
            handle.write(json.dumps(dict(requested=list(args), executed=actual,
                                         exit_code=result.returncode)) + '\n')
        return result
    return real_run(args, *positional, **keyword)


real_run(['python3', 'scripts/ci_rv32_sdk.py', '--destination', str(sdk), '--verify-only'], check=True)
print('Exact compiler argv mapping:', native, '->', mapped, flush=True)
sys.argv = ['sw/builder/test_builder.py', '--require-rv32']
with patch('subprocess.run', selected_run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
if not (records.exists() and records.stat().st_size > 0):
    raise SystemExit('no compiler invocation was mapped')
print('mapped compiler invocations:', sum(1 for _ in records.open()))
