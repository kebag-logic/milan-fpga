"""Run the full builder with an audited compiler selection."""

import argparse
import json
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=("sdk", "absent"))
parser.add_argument("--audit", type=Path, required=True)
args = parser.parse_args()
selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
destination = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
cross = {selector, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
real_run = subprocess.run
if args.mode == "sdk":
    real_run([sys.executable, "scripts/ci_rv32_sdk.py", "--destination",
              str(destination), "--verify-only"], check=True, timeout=300)

with args.audit.open("w") as receipt:
    def selected_run(argv, *positional, **keyword):
        if not isinstance(argv, (list, tuple)) or not argv or str(argv[0]) not in cross:
            return real_run(argv, *positional, **keyword)
        requested = [str(arg) for arg in argv]
        if args.mode == "absent":
            receipt.write(json.dumps(dict(requested=requested, executed=None,
                                           result="deliberately absent")) + "\n")
            receipt.flush()
            raise FileNotFoundError("deliberately absent RV32 compiler")
        actual = [str(destination / "bin/riscv32-linux-gcc"), *argv[1:]] \
            if str(argv[0]) == selector else list(argv)
        result = real_run(actual, *positional, **keyword)
        receipt.write(json.dumps(dict(requested=requested, executed=actual,
                                       exit_code=result.returncode)) + "\n")
        receipt.flush()
        return result

    sys.argv = ["sw/builder/test_builder.py"] + (["--require-rv32"] if args.mode == "sdk" else [])
    print("Full builder mode:", args.mode, flush=True)
    with patch("subprocess.run", selected_run):
        runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
assert args.audit.stat().st_size > 0
