"""Run the complete builder with exactly its three RV32 candidates unavailable."""
from pathlib import Path
import runpy
import subprocess
import sys

root = Path('$LANES/607-xdc-clock-names')
blocked = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
           'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
real_run = subprocess.run

def compiler_absent(command, *args, **kwargs):
    if isinstance(command, (list, tuple)) and command and str(command[0]) in blocked:
        raise FileNotFoundError('compiler-absent control: ' + str(command[0]))
    return real_run(command, *args, **kwargs)

subprocess.run = compiler_absent
sys.path.insert(0, str(root / 'sw/builder'))
sys.argv = [str(root / 'sw/builder/test_builder.py'), '--require-elaboration']
runpy.run_path(sys.argv[0], run_name='__main__')
