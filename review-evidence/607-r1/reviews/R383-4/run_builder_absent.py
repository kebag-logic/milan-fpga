"""Run the complete builder bank with exactly its three RV32 compiler candidates unavailable.

Usage: <litex-python> run_builder_absent.py <clone>
The host compilers (cc, gcc) remain; --require-elaboration is retained, --require-rv32 is not.
"""
from pathlib import Path
import runpy
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
blocked = {str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
           "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
real_run = subprocess.run
refused = []


def compiler_absent(command, *args, **kwargs):
    if isinstance(command, (list, tuple)) and command and str(command[0]) in blocked:
        refused.append(str(command[0]))
        raise FileNotFoundError("compiler-absent control: " + str(command[0]))
    return real_run(command, *args, **kwargs)


subprocess.run = compiler_absent
sys.path.insert(0, str(root / "sw/builder"))
sys.argv = [str(root / "sw/builder/test_builder.py"), "--require-elaboration"]
try:
    runpy.run_path(sys.argv[0], run_name="__main__")
finally:
    print(f"[absent-control] refused compiler launches: {len(refused)} {sorted(set(refused))}")
