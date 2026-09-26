from pathlib import Path
import json
import runpy
import subprocess
import sys
from unittest.mock import patch

mode = sys.argv[1]
assert mode in {"sdk", "absent"}
out = Path(__file__).resolve().parent
selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
sdk = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
cross = {selector, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
real_run = subprocess.run
mapped = 0
hidden = set()

def selected_run(args, *positional, **keyword):
    global mapped
    if isinstance(args, (list, tuple)) and args:
        requested = [str(arg) for arg in args]
        if mode == "absent" and requested[0] in cross:
            hidden.add(requested[0])
            with (out / "builder-absent-argv.jsonl").open("a") as record:
                record.write(json.dumps({"requested": requested, "result": "deliberately absent"}) + "\n")
            raise FileNotFoundError("deliberately absent RV32 candidate")
        if mode == "sdk" and requested[0] == selector:
            actual = [str(sdk / "bin/riscv32-linux-gcc"), *args[1:]]
            result = real_run(actual, *positional, **keyword)
            mapped += 1
            with (out / "builder-sdk-argv.jsonl").open("a") as record:
                record.write(json.dumps({"requested": requested, "executed": [str(arg) for arg in actual], "rc": result.returncode}) + "\n")
            return result
    return real_run(args, *positional, **keyword)

if mode == "sdk":
    real_run([sys.executable, "scripts/ci_rv32_sdk.py", "--destination", str(sdk), "--verify-only"], check=True)
print("Full builder mode:", mode, flush=True)
sys.argv = ["sw/builder/test_builder.py"] + (["--require-rv32"] if mode == "sdk" else [])
with patch("subprocess.run", selected_run):
    runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
if mode == "sdk":
    assert mapped > 0
    print("SDK invocations:", mapped)
else:
    assert hidden == cross, hidden
    print("Hidden cross candidates:", len(hidden))
