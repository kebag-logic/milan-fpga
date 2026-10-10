#!/bin/bash
# PP_SHADOW_BASELINE_RECIPE.md prerequisites, shipping export and integrated preparation; no Vivado run.
# Usage: export_shipping.sh SIDE COMMIT
set -e
side=$1; commit=$2
root=$SCRATCH
export REPO=$root/exp-$side
export WORK=$root/res/$side
export LITEX_PYTHON=$LITEX_ENV/venv/bin/python3
export SDK=$SDK
export PATH=$XILINX/2026.1/Vivado/bin:$SDK/bin:$LITEX_ENV/venv/bin:$PATH
export TMPDIR=$root/tmp PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 MAKEFLAGS=-j4
cd "$REPO"
test "$(git rev-parse --show-toplevel)" = "$REPO"
test "$(git rev-parse HEAD)" = "$commit"
test -z "$(git status --porcelain)"
test ! -e "$WORK"
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
mkdir -p "$WORK/builder" "$WORK/roms"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only > "$WORK/sdk.log" 2>&1
python3 syn/ooc/pp_baseline.py --selftest > "$WORK/baseline-selftest.log" 2>&1
test ! -e sw/builder/out
ln -s "$WORK/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh ax7101 --dry-run > "$WORK/ax7101-dry-run.log" 2>&1
bash sw/litex/build.sh ax8x8 --dry-run > "$WORK/ax8x8-dry-run.log" 2>&1
python3 - <<'PY'
import json
import os
from pathlib import Path
import shlex
import subprocess
root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
python = os.environ["LITEX_PYTHON"]
for shape in ("ax7101", "ax8x8"):
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
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --single-thread-synthesis > "$WORK/prepare-1x1.log" 2>&1
python3 syn/ooc/pp_baseline.py "$WORK/ax8x8/gateware" --synthesis-only --single-thread-synthesis > "$WORK/prepare-8x8.log" 2>&1
echo "export $side done"
