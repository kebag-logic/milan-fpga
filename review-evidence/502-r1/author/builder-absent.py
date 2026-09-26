from pathlib import Path
import json
import runpy
import subprocess
import sys
from unittest.mock import patch

cross = {str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"),
         "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
hidden = set()
records = Path("$MANAGEMENT/2026-09-23/502-a338/builder-absent-argv.jsonl")
real_run = subprocess.run

def absent_run(args, *positional, **keyword):
    if isinstance(args, (list, tuple)) and args and str(args[0]) in cross:
        hidden.add(str(args[0]))
        with records.open("a") as log:
            log.write(json.dumps(dict(requested=list(args), result="deliberately absent")) + "\n")
        raise FileNotFoundError("deliberately absent RV32 candidate")
    return real_run(args, *positional, **keyword)

print("Full builder test with all RV32 candidates hidden; host tools remain available", flush=True)
sys.argv = ["sw/builder/test_builder.py"]
with patch("subprocess.run", absent_run):
    runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
assert hidden == cross, hidden
print("All three RV32 candidates were refused as absent", flush=True)
