"""Run the complete builder bank with cross-compiler candidates absent."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

root = Path.cwd()
sys.path.insert(0, str(root / "sw/builder"))
original_run = subprocess.run
hidden = set()
candidates = {str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
              "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}

def absent(argv, **kwargs):
    if str(argv[0]) in candidates:
        hidden.add(str(argv[0]))
        raise FileNotFoundError("deliberately absent cross-compiler candidate")
    return original_run(argv, **kwargs)

sys.argv = [str(root / "sw/builder/test_builder.py"), "--require-elaboration"]
with patch.object(subprocess, "run", side_effect=absent):
    try:
        runpy.run_path(sys.argv[0], run_name="__main__")
    except SystemExit as error:
        if error.code not in (None, 0):
            raise
assert hidden == candidates, hidden
print("FULL BUILDER ABSENT PASS: all three cross-compiler candidates hidden")
