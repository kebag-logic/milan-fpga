#!/usr/bin/env bash
# #814 round 2: the recipe's export and measurement scripts for one shape at <rev>, in its own clean clone
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, recipe unchanged, --single-thread-synthesis). Runs no Vivado; each
# Vivado run is launched separately through the slot wrapper (launch.sh).
#   ax7101: the export, baseline_integrated.tcl (route-1x1)
#   ax8x8:  the export, the synthesis-only script, and rtl/rtl.tcl (the recipe's RTL elaboration for ooc-8x8)
# CONTROL=wire-phy elaborates through control_wire_phy.py (the head with the flash stage wired; measurement only).
# usage: r2_export.sh <label> <rev> <shape>
set -uo pipefail
label=$1; rev=$2; shape=$3
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/814-a703b
W=$S/w-$label
export REPO=$S/clone-$label
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export CONTROL_DRIVER="$here/control_wire_phy.py"
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
# the checkout's three artifact links name this shape's work directory; one shape per clone, so they stay put
# while Vivado reads the export
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
control = os.environ.get("CONTROL", "")
preview = (work / f"{shape}-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / shape)
(work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
if control == "wire-phy":
    argv = [os.environ["CONTROL_DRIVER"], *argv]
elif control:
    raise SystemExit("unknown CONTROL " + control)
(work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
with (work / f"{shape}-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
fi
stamp "EXPORT-DONE $shape"
G=$W/$shape/gateware
case $shape in
  ax7101)
    [ -e "$G/baseline_integrated.tcl" ] || python3 syn/ooc/pp_baseline.py "$G" --single-thread-synthesis || exit 4 ;;
  ax8x8)
    R=$W/rtl
    if [ ! -e "$R/rtl.tcl" ]; then
      python3 syn/ooc/pp_baseline.py "$G" --synthesis-only --single-thread-synthesis || exit 5
      mkdir -p "$R"; cp "$G"/*.xdc "$R"/; cp "$G"/*.init "$R"/ 2>/dev/null
      python3 - "$G/baseline_integrated.tcl" "$R/rtl.tcl" <<'PY' || exit 5
import sys
out = []
for line in open(sys.argv[1]).read().splitlines():
    if line.lstrip().startswith("synth_design"):
        out.append(line.rstrip() + " -rtl -rtl_skip_mlo")
        break
    out.append(line)
else:
    sys.exit("no synth_design line")
out.append("quit")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
PY
    fi ;;
esac
stamp "PREPARED $shape"
