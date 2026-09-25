"""Run the complete builder suite with only compiler selection intercepted."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

mode = sys.argv[1]
assert mode in ("sdk", "absent")
native = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
sdk = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
cross = {native, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
calls = []
real_run = subprocess.run

def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args:
        requested = str(args[0])
        if mode == "absent" and requested in cross:
            calls.append(dict(requested=list(args), result="deliberately absent"))
            raise FileNotFoundError("deliberately absent RV32 candidate")
        if mode == "sdk" and requested == native:
            actual = [str(sdk / "bin/riscv32-linux-gcc"), *args[1:]]
            result = real_run(actual, *positional, **keyword)
            calls.append(dict(requested=list(args), executed=actual,
                              returncode=result.returncode))
            return result
    return real_run(args, *positional, **keyword)

if mode == "sdk":
    real_run([sys.executable, "scripts/ci_rv32_sdk.py", "--destination",
              str(sdk), "--verify-only"], check=True, timeout=600)
sys.argv = ["sw/builder/test_builder.py", "--require-elaboration"]
if mode == "sdk":
    sys.argv.append("--require-rv32")
print("Complete builder mode:", mode, flush=True)
try:
    with patch("subprocess.run", selected_run):
        runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
finally:
    record = json.dumps(calls, indent=2).replace(str(Path.home()), "<home>")
    packet = (Path.home() / "milan-fpga-management/2026-09-23/400-403-a322")
    (packet / ("compiler-" + mode + "-argv.json")).write_text(record + "\n")
    print("Compiler selection audit calls:", len(calls), flush=True)
