#!/usr/bin/env python3
"""R607-1: one shipping export without Vivado, from a launcher dry-run line.

    export.py <tree> <dry-run.log> <out-dir> <litex-python> [extra milan_soc.py args...]

Takes the single `exec python3 milan_soc.py ...` line of the dry run, drops
`--build`, points `--output-dir` at <out-dir>/gw, appends the extra arguments
and runs it from <tree>/sw/litex. Writes argv.json, elaboration.log and rc.
"""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

tree, dry, out, python, *extra = sys.argv[1:]
tree, out = Path(tree).resolve(), Path(out).resolve()
out.mkdir(parents=True, exist_ok=False)
lines = [ln for ln in Path(dry).read_text().splitlines() if "exec python3 milan_soc.py " in ln]
assert len(lines) == 1, lines
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(out / "gw")
argv += extra
(out / "argv.json").write_text(json.dumps(argv, indent=2) + "\n")
env = dict(os.environ, PYTHONHASHSEED="0")
with (out / "elaboration.log").open("w") as log:
    rc = subprocess.run([python, *argv], cwd=tree / "sw/litex", stdout=log,
                        stderr=subprocess.STDOUT, env=env, timeout=3000).returncode
(out / "rc").write_text(f"{rc}\n")
print(out.name, "rc", rc)
sys.exit(rc)
