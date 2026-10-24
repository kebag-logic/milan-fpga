#!/usr/bin/env bash
# route_export.sh <repo> <work>: the shipping AX7101 1x1 export per
# docs/testing/PP_SHADOW_BASELINE_RECIPE.md, recipe unchanged (the eleventh
# record's method: pp_baseline.py --single-thread-synthesis). No Vivado here:
# the route itself is started afterwards, alone, under the exclusive lock.
set -euo pipefail
export REPO=$1
export WORK=$2
export LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
export SDK=<sdk>
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
mkdir -p "$WORK"
date -u +%FT%TZ
cd "$REPO"
git rev-parse HEAD; git -C protocol-processor rev-parse HEAD; git -C gptp-processor rev-parse HEAD; git status --short
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
cleanup() {
  cd "$REPO"
  [ -L sw/builder/out ] && unlink sw/builder/out
  [ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
  [ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
  true
}
trap cleanup EXIT
bash sw/litex/build.sh ax7101 --dry-run > "$WORK/ax7101-dry-run.log"
python3 - <<'PY'
import json
import os
from pathlib import Path
import shlex
import subprocess

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
python = os.environ["LITEX_PYTHON"]
preview = (work / "ax7101-dry-run.log").read_text()
lines = [line for line in preview.splitlines() if "exec python3 milan_soc.py " in line]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --single-thread-synthesis
git status --short
echo EXPORT-DONE; date -u +%FT%TZ
