"""Run the entire builder bank while all RV32 compiler candidates are absent."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

root = Path('$LANES/395-timing-grade')
selector = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
candidates = {selector, 'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
hidden = set()
real_run = subprocess.run

def run(argv, *args, **kwargs):
    if not isinstance(argv, str) and str(argv[0]) in candidates:
        hidden.add(str(argv[0]))
        raise FileNotFoundError('deliberately absent RV32 candidate')
    return real_run(argv, *args, **kwargs)

sys.path.insert(0, str(root / 'sw/builder'))
sys.argv = [str(root / 'sw/builder/test_builder.py'), '--require-elaboration']
with patch.object(subprocess, 'run', side_effect=run):
    try:
        runpy.run_path(sys.argv[0], run_name='__main__')
    except SystemExit as exc:
        if exc.code not in (0, None):
            raise
assert hidden == candidates, hidden
print('Full builder bank completed with all three RV32 candidates hidden; host compilers unchanged.')
