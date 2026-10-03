#!/usr/bin/env python3
"""Recipe step 'Export the shipping builds' (docs/testing/PP_SHADOW_BASELINE_RECIPE.md),
parameterised by scratch combination. Scratch only; never committed."""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

combo, shape = sys.argv[1], sys.argv[2]
root = Path(f"$VALIDATION_STORAGE/234-a516/{combo}/repo")
work = Path(f"$VALIDATION_STORAGE/234-a516/{combo}/work")
python = os.environ["LITEX_PYTHON"]
preview = (work / f"{shape}-dry-run.log").read_text()
lines = [line for line in preview.splitlines() if "exec python3 milan_soc.py " in line]
assert len(lines) == 1, lines
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / shape)
(work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
with (work / f"{shape}-elaboration.log").open("w") as log:
    rc = subprocess.run([python, *argv], cwd=root / "sw/litex",
                        stdout=log, stderr=subprocess.STDOUT).returncode
print(f"{combo} {shape} elaboration rc={rc}")
sys.exit(rc)
