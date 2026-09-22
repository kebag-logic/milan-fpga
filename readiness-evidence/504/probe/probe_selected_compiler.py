"""Compatibility probe: map one selected compiler argv to the verified SDK.

No product source, environment home, gate outcome, or compiler argument changes.
"""
from pathlib import Path
import json
import runpy
import subprocess
from unittest.mock import patch

native = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
bootlin = '$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc'
real_run = subprocess.run
records = Path('$VALIDATION_STORAGE/504-readiness/bootlin-bound-invocations.jsonl')
records.parent.mkdir(parents=True, exist_ok=True)
assert not records.exists()

def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) == native:
        actual = [bootlin, *args[1:]]
        with records.open("a") as stream:
            stream.write(json.dumps({"requested": list(args), "executed": actual}) + "\n")
        return real_run(actual, *positional, **keyword)
    return real_run(args, *positional, **keyword)

print("Compiler compatibility mapping:", native, "->", bootlin, flush=True)
with patch("subprocess.run", selected_run):
    runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
