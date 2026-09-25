from pathlib import Path
import json, runpy, subprocess, sys
from unittest.mock import patch
mode = sys.argv[1]
output = Path(__file__).resolve().parent
native = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
compiler = "$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc"
records = output / ("full-builder-" + mode + "-argv.jsonl")
real_run = subprocess.run
cross = {native, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
def selected_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args:
        if mode == "absent" and str(args[0]) in cross:
            with records.open("a") as stream:
                stream.write(json.dumps(dict(requested=list(args), executed=None, result="deliberately absent")) + "\n")
            raise FileNotFoundError("deliberately absent RV32 candidate")
        if mode == "sdk" and str(args[0]) == native:
            actual = [compiler, *args[1:]]
            result = real_run(actual, *positional, **keyword)
            with records.open("a") as stream:
                stream.write(json.dumps(dict(requested=list(args), executed=actual, exit_code=result.returncode)) + "\n")
            return result
    return real_run(args, *positional, **keyword)
records.write_text("")
if mode == "sdk":
    subprocess.run(["python3", "scripts/ci_rv32_sdk.py", "--destination", str(Path(compiler).parents[1]), "--verify-only"], check=True)
sys.argv = ["sw/builder/test_builder.py"] + (["--require-rv32"] if mode == "sdk" else [])
with patch("subprocess.run", selected_run):
    runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
assert records.stat().st_size > 0
