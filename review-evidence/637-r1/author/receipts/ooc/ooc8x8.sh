#!/usr/bin/env bash
# ooc-8x8 per docs/testing/PP_SHADOW_BASELINE_RECIPE.md: the 8x8 export, an RTL-only elaboration for the wrapper's
# parameter block (the recipe's 8x8 route, as #234 used it), then the standalone synthesis, --integrated-clock.
# usage: ooc8x8.sh <label> <repo>
set -uo pipefail
label=$1; export REPO=$2
W=<scratch>/route-$label/work8
export WORK=$W
export LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
export SDK=<scratch>/sdk
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export TMPDIR=<scratch>/tmp
mkdir -p "$W/builder" "$W/roms"
cd "$REPO" || exit 2
date -u +%FT%TZ; git rev-parse HEAD; git -C protocol-processor rev-parse HEAD; git status --short
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only || exit 1
test ! -e sw/builder/out || exit 1
ln -s "$W/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex || exit 1
test ! -e configs/generated/ucode.hex || exit 1
ln -s "$W/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$W/roms/ucode.hex" configs/generated/ucode.hex
cleanup() {
  cd "$REPO"
  [ -L sw/builder/out ] && unlink sw/builder/out
  [ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
  [ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
  true
}
trap cleanup EXIT
bash sw/litex/build.sh ax8x8 --dry-run > "$W/ax8x8-dry-run.log" || exit 1
python3 - <<'PY' || exit 1
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
preview = (work / "ax8x8-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax8x8")
(work / "ax8x8-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax8x8-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
python3 syn/ooc/pp_baseline.py "$W/ax8x8/gateware" --synthesis-only --single-thread-synthesis || exit 1
G=$W/ax8x8/gateware; R=$W/ax8x8-rtl
mkdir -p "$R"; cp "$G"/*.xdc "$G"/*.init "$R"/ 2>/dev/null
python3 - "$G/baseline_integrated.tcl" "$R/rtl.tcl" <<'PY' || exit 1
import sys
src = open(sys.argv[1]).read().splitlines()
out = []
for line in src:
    if line.lstrip().startswith("synth_design"):
        out.append(line.rstrip() + " -rtl -rtl_skip_mlo")
        break
    out.append(line)
else:
    sys.exit("no synth_design line")
out.append("quit")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
PY
echo RTL-SCRIPT-DONE; date -u +%FT%TZ
vrc=0; ( cd "$R" && flock -x $VIVADO_LOCK vivado -mode batch -source rtl.tcl -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
echo "RTL-ELAB VIVADO rc=$vrc"; date -u +%FT%TZ
python3 syn/ooc/pp_baseline.py "$G" --single-thread-synthesis --output "$W/ax8x8-ooc" \
  --integrated-log "$R/baseline.log" --integrated-clock || exit 1
vrc=0; ( cd "$W/ax8x8-ooc" && flock -x $VIVADO_LOCK vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
echo "OOC VIVADO rc=$vrc"; date -u +%FT%TZ
grc=0; python3 syn/ooc/pp_resource_gate.py check "$W/ax8x8-ooc" --endpoint ooc-8x8 || grc=$?
echo "GATE rc=$grc"; date -u +%FT%TZ
