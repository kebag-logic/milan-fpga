"""Run the complete builder bank with RV32 compiler candidates unavailable."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

ROOT = Path.cwd()
CROSS = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
         'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
original_run = subprocess.run
hidden = set()

def absent(argv, **kwargs):
    if str(argv[0]) in CROSS:
        hidden.add(str(argv[0]))
        print('HIDDEN RV32 CANDIDATE', argv[0], flush=True)
        raise FileNotFoundError('deliberately absent RV32 candidate')
    return original_run(argv, **kwargs)

sys.path.insert(0, str(ROOT/'sw/builder'))
sys.argv = [str(ROOT/'sw/builder/test_builder.py')]
with patch.object(subprocess, 'run', side_effect=absent):
    result = runpy.run_path(sys.argv[0], run_name='__main__')
assert hidden == CROSS, hidden
assert any('THREE INSTRUMENTS' in why for _, why, _ in result['SKIPPED'])
print('PASS: full builder bank completed with all RV32 candidates absent')
