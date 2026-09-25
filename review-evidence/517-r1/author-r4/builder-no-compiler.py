from pathlib import Path
import json
import runpy
import subprocess
import sys
from unittest.mock import patch

native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
blocked = {native, 'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
records = Path(__file__).resolve().parent / 'builder-no-compiler-argv.jsonl'
real_run = subprocess.run

def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) in blocked:
        with records.open('a') as receipt:
            receipt.write(json.dumps(dict(requested=list(args), unavailable=True)) + '\n')
        raise FileNotFoundError(2, 'Cross compiler unavailable for the no-compiler validation mode', str(args[0]))
    return real_run(args, *positional, **keyword)

print('No-compiler mode: all RV32 candidate executable launches are unavailable; host compilers remain real.', flush=True)
sys.argv = ['sw/builder/test_builder.py']
with patch('subprocess.run', selected_run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
assert records.exists() and records.stat().st_size > 0
