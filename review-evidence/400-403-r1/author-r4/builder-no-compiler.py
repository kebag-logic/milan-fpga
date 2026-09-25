from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
absent = {native, 'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
real_run = subprocess.run

def without_cross_compiler(argv, *args, **kwargs):
    if isinstance(argv, (list, tuple)) and argv and str(argv[0]) in absent:
        raise FileNotFoundError(str(argv[0]))
    return real_run(argv, *args, **kwargs)

sys.argv = ['sw/builder/test_builder.py']
with patch('subprocess.run', without_cross_compiler):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
