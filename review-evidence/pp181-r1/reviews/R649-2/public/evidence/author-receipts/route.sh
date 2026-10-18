#!/usr/bin/env bash
# route-1x1 on the scratch parent, per docs/testing/PP_SHADOW_BASELINE_RECIPE.md,
# recipe unchanged; Vivado under the exclusive lock.  usage: route.sh <label>
set -euo pipefail
label=$1
W=<data>/tmp/pp181-a635/route-$label
export REPO=<data>/tmp/pp181-a635/parent
export WORK=$W/work
export LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
export SDK=<data>/tmp/708-a585/sdk
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
mkdir -p "$W"
exec > "$W/route.out" 2>&1
date -u +%FT%TZ
cd "$REPO"
git rev-parse HEAD; git -C protocol-processor rev-parse HEAD; git status --short
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
for shape in ("ax7101",):
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
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --single-thread-synthesis
echo EXPORT-DONE; date -u +%FT%TZ
(
  cd "$WORK/ax7101/gateware"
  flock -x $VIVADO_LOCK vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1
)
echo "VIVADO rc=$?"; date -u +%FT%TZ
rc=0
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 > "$W/route-1x1-check.log" 2>&1 || rc=$?
echo "GATE rc=$rc"
cat "$W/route-1x1-check.log"
date -u +%FT%TZ
echo ROUTE-DONE
