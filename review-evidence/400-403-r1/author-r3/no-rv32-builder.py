from pathlib import Path
import runpy, shutil, subprocess, sys
from unittest.mock import patch
native = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
blocked = {native, 'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
real_which, real_exists, real_run = shutil.which, Path.exists, subprocess.run
def without_rv32(cmd, *args, **kwargs):
    return None if str(cmd) in blocked else real_which(cmd, *args, **kwargs)
def exists(path):
    return False if str(path) == native else real_exists(path)
hidden = set()
audit = out = Path(__file__).resolve().parent / 'no-rv32-argv.jsonl'
def run(cmd, *args, **kwargs):
    if isinstance(cmd, (list, tuple)) and cmd and str(cmd[0]) in blocked:
        hidden.add(str(cmd[0]))
        with audit.open('a') as log:
            log.write(repr(cmd) + '\n')
        raise FileNotFoundError(str(cmd[0]))
    return real_run(cmd, *args, **kwargs)
sys.argv = ['sw/builder/test_builder.py']
print('No RV32 compiler mode: cross compiler candidates hidden; host compiler retained.', flush=True)
with patch('shutil.which', without_rv32), patch.object(Path, 'exists', exists), patch('subprocess.run', run):
    runpy.run_path('sw/builder/test_builder.py', run_name='__main__')

assert hidden == blocked, hidden
