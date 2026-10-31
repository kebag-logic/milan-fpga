#!/usr/bin/env bash
# #787 round 4: prepare route-1x1 at one revision in a clean clone, recipe unchanged
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, "Integrated measurements"): the shipping AX7101 1x1 export,
# pp_baseline.py --single-thread-synthesis, and the recipe snippet's two comparison scripts (written, not run).
# The #814 round 1 bank's export, the Vivado runs left to launch.sh. The three artifact links stay
# in place for the life of the runs.
# usage: prep_route.sh <repo> <work> <rev>
set -uo pipefail
export REPO=$1 WORK=$2; rev=$3
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export TMPDIR=$VALIDATION_STORAGE/787-a700e/tmp
mkdir -p "$WORK" "$TMPDIR"
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp "PREP $rev"
cd "$REPO" || exit 2
git rev-parse HEAD; git -C protocol-processor rev-parse HEAD; git -C gptp-processor rev-parse HEAD; git status --short
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$rev^{commit}")" ] || { echo "CLONE-NOT-AT-REV"; exit 2; }
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only || exit 2
python3 syn/ooc/pp_baseline.py --selftest || exit 2
cleanup() {
  cd "$REPO"
  [ -L sw/builder/out ] && unlink sw/builder/out
  [ -L configs/generated/ltn_rom.hex ] && unlink configs/generated/ltn_rom.hex
  [ -L configs/generated/ucode.hex ] && unlink configs/generated/ucode.hex
  true
}
# Round 3's lesson: the links must outlive the prep, so no exit trap removes them. unlink_links.sh
# removes them once every Vivado run has ended.
shape=ax7101; W1=$WORK/w1; G1=$W1/ax7101/gateware
mkdir -p "$W1/builder" "$W1/roms"
cleanup
test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || exit 3
ln -s "$W1/builder" sw/builder/out
ln -s "$W1/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$W1/roms/ucode.hex" configs/generated/ucode.hex
if [ ! -d "$G1" ]; then
  bash sw/litex/build.sh "$shape" --dry-run > "$W1/$shape-dry-run.log" || exit 3
  SHAPE=$shape WORKDIR=$W1 python3 - <<'PY' || exit 3
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
stamp EXPORT-DONE
[ -e "$G1/baseline_integrated.tcl" ] || python3 syn/ooc/pp_baseline.py "$G1" --single-thread-synthesis || exit 4
# the recipe snippet's comparison scripts, from the shipping script, the synthesis checkpoint reused
python3 - <<'PY' || exit 5
import importlib.util
import os
from pathlib import Path
import shutil

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"]) / "w1"
gateware = work / "ax7101/gateware"
spec = importlib.util.spec_from_file_location("baseline", root / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
source = (gateware / "alinx_ax7101.tcl").read_text()
_, tail = baseline.split_once(source, "# Add pre-optimize commands")
tail, _ = baseline.split_once(tail, "# Bitstream generation")
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    output = work / f"ax7101-{directive}"
    output.mkdir()
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    script += baseline.REPORTS + baseline.PP_REPORTS
    script += baseline.SCOPE_TIMING + "\nquit\n"
    (output / "baseline_implementation.tcl").write_text(script)
    print(output / "baseline_implementation.tcl")
PY
stamp PREP-DONE
echo PREP-DONE
