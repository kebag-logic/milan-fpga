#!/bin/bash
# Recipe "Export the shipping builds", ax8x8 only; reviewer-private paths.
set -u
S=$REVIEWS/587-r351-1-packet/scratch
export REPO=$REVIEWS/r351-1-587 WORK=$S/work LITEX_PYTHON=$S/pybin/python3 SDK=$S/sdk
export PATH="$HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$S/pybin:/usr/bin:/bin"
export PYTHONHASHSEED=0
export LITEX_ENV_CC_TRIPLE="$(cd $REPO && PYTHONPATH=scripts /usr/bin/python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
cd $REPO
/usr/bin/python3 - <<'PY'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
for shape in ("ax8x8",):
    preview = (work / f"{shape}-dry-run.log").read_text()
    lines = [line for line in preview.splitlines() if "exec python3 milan_soc.py " in line]
    assert len(lines) == 1
    argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
    argv.remove("--build")
    argv[argv.index("--output-dir") + 1] = str(work / shape)
    (work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
    with (work / f"{shape}-elaboration.log").open("w") as log:
        subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
echo "export rc=$?" > $WORK/ax8x8-export.rc
