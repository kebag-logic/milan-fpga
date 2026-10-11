#!/usr/bin/env python3
"""Scratch (M8a-1 evidence): the recipe's shipping export without Vivado, into WORK/<label>.

Usage: export.py <ax7101|ax8x8> <label> [extra milan_soc.py arguments...]
"""
import json
import shlex
import subprocess
import sys
from pathlib import Path

root = Path("$LANES/640-m8a")
work = Path("$VALIDATION_STORAGE/640m8a-a594/m81/work")
python = "$WORKSPACE_HOME/litex-milan/venv/bin/python3"
shape, label, *extra = sys.argv[1:]
preview = (work / f"{shape}-dry-run.log").read_text()
lines = [line for line in preview.splitlines() if "exec python3 milan_soc.py " in line]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / label)
argv += extra
(work / f"{label}-argv.json").write_text(json.dumps(argv, indent=2) + "\n")
with (work / f"{label}-elaboration.log").open("w") as log:
    rc = subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log,
                        stderr=subprocess.STDOUT).returncode
(work / f"{label}.rc").write_text(f"{rc}\n")
print(label, "rc", rc)
sys.exit(rc)
