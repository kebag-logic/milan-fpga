from pathlib import Path
import json, runpy, subprocess, sys
from unittest.mock import patch
out = Path(__file__).parent
candidates = {str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"), "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
real_run = subprocess.run
with (out / "builder-absent-argv.jsonl").open("w") as audit:
    def absent_run(argv, *positional, **kwargs):
        if isinstance(argv, (list, tuple)) and argv and str(argv[0]) in candidates:
            audit.write(json.dumps({"requested": list(argv), "result": "deliberately absent"}) + "\n")
            audit.flush()
            raise FileNotFoundError("deliberately absent RV32 compiler")
        return real_run(argv, *positional, **kwargs)
    sys.argv = ["sw/builder/test_builder.py"]
    with patch("subprocess.run", absent_run):
        runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
