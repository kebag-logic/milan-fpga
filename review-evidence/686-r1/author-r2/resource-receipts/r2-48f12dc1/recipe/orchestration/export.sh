#!/usr/bin/env bash
# Recipe steps "Prerequisites" and "Export the shipping builds" of
# docs/testing/PP_SHADOW_BASELINE_RECIPE.md, for the shapes given as arguments.
set -euo pipefail
export REPO=<repo>
export WORK=<work>
export LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
export SDK=<scratch>/rv32-sdk
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export TMPDIR=<scratch>/tmp
cd "$REPO"
LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
export LITEX_ENV_CC_TRIPLE
mkdir -p "$WORK/builder" "$WORK/roms"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 syn/ooc/pp_baseline.py --selftest
if [ ! -L sw/builder/out ]; then
  test ! -e sw/builder/out
  ln -s "$WORK/builder" sw/builder/out
fi
for f in ltn_rom.hex ucode.hex; do
  if [ ! -L "configs/generated/$f" ]; then
    test ! -e "configs/generated/$f"
    ln -s "$WORK/roms/$f" "configs/generated/$f"
  fi
done
for shape in "$@"; do
  bash sw/litex/build.sh "$shape" --dry-run > "$WORK/$shape-dry-run.log"
done
SHAPES="$*" python3 - <<'PY'
import json
import os
from pathlib import Path
import shlex
import subprocess

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
python = os.environ["LITEX_PYTHON"]
for shape in os.environ["SHAPES"].split():
    preview = (work / f"{shape}-dry-run.log").read_text()
    lines = [line for line in preview.splitlines()
             if "exec python3 milan_soc.py " in line]
    assert len(lines) == 1
    argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
    argv.remove("--build")
    argv[argv.index("--output-dir") + 1] = str(work / shape)
    (work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
    with (work / f"{shape}-elaboration.log").open("w") as log:
        subprocess.run([python, *argv], cwd=root / "sw/litex",
                       stdout=log, stderr=subprocess.STDOUT, check=True)
PY
git status --short
