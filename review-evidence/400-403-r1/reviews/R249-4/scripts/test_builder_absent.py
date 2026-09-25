#!/usr/bin/env python3
"""Run sw/builder/test_builder.py --require-elaboration with every RV32 cross compiler hidden.

Each subprocess.run whose argv[0] is one of the gate's cross-compiler candidates raises
FileNotFoundError (logged to R249_ARGV_LOG); host compilers and everything else run
unchanged. Run from the candidate root.
"""
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

cross = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
         'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
records = Path(os.environ['R249_ARGV_LOG'])
records.unlink(missing_ok=True)
real_run = subprocess.run


def hidden_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) in cross:
        with records.open('a') as handle:
            handle.write(json.dumps(dict(requested=[str(a) for a in args],
                                         result='deliberately absent')) + '\n')
        raise FileNotFoundError('deliberately absent RV32 candidate')
    return real_run(args, *positional, **keyword)


sys.argv = ['sw/builder/test_builder.py', '--require-elaboration']
with patch('subprocess.run', hidden_run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
print('hidden cross-compiler probes:',
      sum(1 for _ in records.open()) if records.exists() else 0)
