"""Run the complete builder bank with every RV32 compiler candidate hidden.

Usage: python3 -B run_builder_absent.py <repository root>

The hidden set is the three RV32 cross candidates named in the repository's
compiler search list (sw/builder/test_builder.py and test_firmware_compiler.py);
the host C compilers stay visible. Required elaboration is retained, and the
wrapper fails unless the bank probed every hidden candidate.
"""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
candidates = {selector, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
hidden = set()
real_run = subprocess.run


def run(argv, *args, **kwargs):
    if not isinstance(argv, str) and str(argv[0]) in candidates:
        hidden.add(str(argv[0]))
        raise FileNotFoundError("deliberately absent RV32 candidate")
    return real_run(argv, *args, **kwargs)


sys.path.insert(0, str(root / "sw/builder"))
sys.argv = [str(root / "sw/builder/test_builder.py"), "--require-elaboration"]
code = 0
with patch.object(subprocess, "run", side_effect=run):
    try:
        runpy.run_path(sys.argv[0], run_name="__main__")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
assert hidden == candidates, f"not every candidate was probed: {sorted(hidden)}"
print(f"absent-mode wrapper: all three RV32 candidates hidden; bank exit {code}")
sys.exit(code)
