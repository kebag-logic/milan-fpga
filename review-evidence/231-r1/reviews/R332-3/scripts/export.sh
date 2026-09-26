#!/usr/bin/env bash
# Follows docs/testing/PP_SHADOW_BASELINE_RECIPE.md "Prerequisites" and
# "Export the shipping builds" verbatim, in a disposable copy of the head.
# usage: export.sh <repo-copy> <work> <sdk>
set -euo pipefail
export REPO="$1" WORK="$2" SDK="$3"
export LITEX_PYTHON=$HOME/litex-milan/venv/bin/python3
export PATH="${VIVADO_BIN:-$HOME/Xilinx/2026.1/Vivado/bin}:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
cd "$REPO"
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
mkdir -p "$WORK/builder" "$WORK/roms"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 syn/ooc/pp_baseline.py --selftest
test ! -e sw/builder/out
ln -s "$WORK/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh ax7101 --dry-run > "$WORK/ax7101-dry-run.log"
bash sw/litex/build.sh ax8x8 --dry-run > "$WORK/ax8x8-dry-run.log"
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
echo EXPORT-OK
