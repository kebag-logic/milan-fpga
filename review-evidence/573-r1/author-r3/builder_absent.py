"""Run the full builder with only its three RV32 candidates unavailable."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

original_run = subprocess.run
candidates = {
    str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
    'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc',
}
blocked = []


def without_rv32(command, *args, **kwargs):
    if isinstance(command, (list, tuple)) and str(command[0]) in candidates:
        blocked.append(str(command[0]))
        raise FileNotFoundError('RV32 compiler deliberately unavailable for absent-mode gate')
    return original_run(command, *args, **kwargs)


entry = Path.cwd() / 'sw/builder/test_builder.py'
sys.path.insert(0, str(entry.parent))
sys.argv = [str(entry)]
try:
    with patch('subprocess.run', without_rv32):
        runpy.run_path(str(entry), run_name='__main__')
finally:
    print('Absent-mode compiler probes blocked:', len(blocked), flush=True)
    assert blocked, 'absent-mode control did not intercept compiler selection'
