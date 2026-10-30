#!/usr/bin/env bash
# #817: the recipe's export for the ax7101 shape at <rev>, in its own clean clone
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, recipe unchanged, --single-thread-synthesis), then
# pp_baseline.py's route-1x1 script. Runs no Vivado; the route is launched separately through the slot
# wrapper (launch.sh).
# usage: export.sh <label> <rev>
set -uo pipefail
label=$1; rev=$2
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/817-a709
W=$S/w-$label
export REPO=$S/clone-$label
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export TMPDIR=$S/tmp
shape=ax7101
mkdir -p "$W"
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp "EXPORT-START $label $rev $shape"
[ -d "$REPO" ] || bash "$here/make_clone.sh" "$REPO" "$rev" || exit 2
cd "$REPO" || exit 2
git rev-parse HEAD; git submodule status; git status --short
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$rev^{commit}")" ] || { echo "CLONE-NOT-AT-REV"; exit 2; }
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only || exit 2
python3 syn/ooc/pp_baseline.py --selftest || exit 2
mkdir -p "$W/builder" "$W/roms"
for l in sw/builder/out configs/generated/ltn_rom.hex configs/generated/ucode.hex; do [ -L "$l" ] && unlink "$l"; done
test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || exit 2
ln -s "$W/builder" sw/builder/out
ln -s "$W/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$W/roms/ucode.hex" configs/generated/ucode.hex
if [ ! -d "$W/$shape/gateware" ]; then
  bash sw/litex/build.sh "$shape" --dry-run > "$W/$shape-dry-run.log" || exit 3
  SHAPE=$shape WORKDIR=$W python3 - <<'PY' || exit 3
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORKDIR"]); shape = os.environ["SHAPE"]
python = os.environ["LITEX_PYTHON"]
preview = (work / f"{shape}-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / shape)
(work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
with (work / f"{shape}-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
fi
stamp "EXPORT-DONE $shape"
G=$W/$shape/gateware
[ -e "$G/baseline_integrated.tcl" ] || python3 syn/ooc/pp_baseline.py "$G" --single-thread-synthesis || exit 4
stamp "PREPARED $shape"
