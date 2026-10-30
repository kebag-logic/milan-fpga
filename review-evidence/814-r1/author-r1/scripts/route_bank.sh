#!/usr/bin/env bash
# #814 Vivado bank (the #787 and #806 lanes' bank, recipe unchanged: docs/testing/PP_SHADOW_BASELINE_RECIPE.md),
# in one clean clone at <rev>, one Vivado run at a time, each under the exclusive lock and only above 20 GB
# MemAvailable. Steps, in the order given:
#   r1   route-1x1: the shipping AX7101 1x1 export through routing (ExtraPostPlacementOpt), then the gate
#   dir  the recipe's two other placement directives from route-1x1's own synthesis checkpoint (default seed)
#   o1   ooc-1x1: the wrapper alone, parameters from route-1x1's synthesis log, then the gate
#   r8   route-8x8: the 8x8 export through routing at its own directive (AltSpreadLogic_high); no gate endpoint
#   o8   rtl-8x8 (the wrapper's parameter block) then ooc-8x8, then the gate
#   paths  top sys setup paths (paths.tcl) on every routed checkpoint present
# usage: route_bank.sh <label> <rev> <step>...
set -uo pipefail
label=$1; rev=$2; shift 2
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/814-a703
W=$S/viv-$label
export REPO=$S/clone-viv-$label
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
mkdir -p "$W"
exec >> "$W/bank.out" 2>&1
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp "START $label $rev steps: $*"
[ -d "$REPO" ] || bash "$here/make_clone.sh" "$REPO" "$rev" || exit 2
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
trap cleanup EXIT
link_shape() {     # <work>: the checkout's three artifact links name this shape's work directory
  local work=$1
  mkdir -p "$work/builder" "$work/roms"
  cleanup
  test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || return 1
  ln -s "$work/builder" sw/builder/out
  ln -s "$work/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
  ln -s "$work/roms/ucode.hex" configs/generated/ucode.hex
}
export_shape() {   # <shape> <work>: one export per shape, in its own work directory with its own ROM links
  local shape=$1 work=$2
  link_shape "$work" || return 1
  [ -d "$work/$shape/gateware" ] && { echo "export $shape exists"; return 0; }
  bash sw/litex/build.sh "$shape" --dry-run > "$work/$shape-dry-run.log" || return 1
  SHAPE=$shape WORKDIR=$work python3 - <<'PY' || return 1
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
}
unit_anon() {      # this unit's anonymous memory: Vivado starts only with the unit's other work under 3 GB
  local cg; cg=$(systemctl --user show milan-814-a703.service -p ControlGroup --value 2>/dev/null)
  awk '/^anon /{print $2}' "/sys/fs/cgroup$cg/memory.stat" 2>/dev/null || echo 0
}
vivado_run() {     # <dir> <script> <name>
  local mem; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  while [ "$mem" -lt 20971520 ]; do echo "waiting: MemAvailable $mem kB"; sleep 60; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo); done
  local um; um=$(unit_anon)
  while [ "${um:-0}" -gt 3221225472 ]; do echo "waiting: unit anon $um"; sleep 60; um=$(unit_anon); done
  stamp "VIVADO-START $3"
  local vrc=0
  ( cd "$1" && flock -x $VIVADO_LOCK vivado -mode batch -source "$2" -nojournal -log "${4:-baseline.log}" > "${5:-vivado.out}" 2>&1 ) || vrc=$?
  stamp "VIVADO-END $3 rc=$vrc"
  return $vrc
}
gate() {           # <dir> <endpoint>
  local grc=0
  python3 syn/ooc/pp_resource_gate.py check "$1" --endpoint "$2" > "$W/$2-check.log" 2>&1 || grc=$?
  echo "GATE $2 rc=$grc"; cat "$W/$2-check.log"
}
W1=$W/w1; W8=$W/w8; G1=$W1/ax7101/gateware; G8=$W8/ax8x8/gateware; R8=$W8/ax8x8-rtl
prep1() {
  export_shape ax7101 "$W1" || { echo EXPORT-1x1-FAILED; exit 3; }
  [ -e "$G1/baseline_integrated.tcl" ] || python3 syn/ooc/pp_baseline.py "$G1" --single-thread-synthesis || exit 3
}
prep8() {
  export_shape ax8x8 "$W8" || { echo EXPORT-8x8-FAILED; exit 5; }
  if [ ! -e "$R8/rtl.tcl" ]; then
    python3 syn/ooc/pp_baseline.py "$G8" --synthesis-only --single-thread-synthesis || exit 5
    mkdir -p "$R8"; cp "$G8"/*.xdc "$R8"/; cp "$G8"/*.init "$R8"/ 2>/dev/null
    python3 - "$G8/baseline_integrated.tcl" "$R8/rtl.tcl" <<'PY' || exit 5
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
    # route-8x8 runs the full integrated script in the gateware directory itself
    python3 syn/ooc/pp_baseline.py "$G8" --single-thread-synthesis || exit 5
  fi
}
for step in "$@"; do
  case $step in
    r1)
      prep1; stamp EXPORT-1x1-DONE
      vivado_run "$G1" baseline_integrated.tcl route-1x1
      gate "$G1" route-1x1 ;;
    dir)
      prep1
      bash "$here/directive_sweep.sh" "$REPO" "$W1" || echo "DIRECTIVES rc=$?" ;;
    o1)
      prep1
      python3 syn/ooc/pp_baseline.py "$G1" --single-thread-synthesis --output "$W1/ax7101-ooc" \
        --integrated-log "$G1/baseline.log" --integrated-clock || exit 4
      vivado_run "$W1/ax7101-ooc" baseline_ooc.tcl ooc-1x1
      gate "$W1/ax7101-ooc" ooc-1x1 ;;
    r8)
      prep8; stamp EXPORT-8x8-DONE
      vivado_run "$G8" baseline_integrated.tcl route-8x8 ;;
    o8)
      prep8
      vivado_run "$R8" rtl.tcl rtl-8x8
      python3 syn/ooc/pp_baseline.py "$G8" --single-thread-synthesis --output "$W8/ax8x8-ooc" \
        --integrated-log "$R8/baseline.log" --integrated-clock || exit 6
      vivado_run "$W8/ax8x8-ooc" baseline_ooc.tcl ooc-8x8
      gate "$W8/ax8x8-ooc" ooc-8x8 ;;
    paths)
      for dcp in "$G1/alinx_ax7101_route.dcp" "$W1"/ax7101-*/alinx_ax7101_route.dcp "$G8/alinx_ax7101_route.dcp"; do
        [ -e "$dcp" ] || continue
        d=$(dirname "$dcp")
        [ -e "$d/sys_paths.tsv" ] && continue
        vivado_run "$d" "$here/paths.tcl" "paths $(basename "$(dirname "$d")")/$(basename "$d")" paths.log paths.out \
          || echo "PATHS rc=$?"
      done ;;
    *) echo "unknown step $step"; exit 9 ;;
  esac
done
stamp BANK-DONE
echo BANK-DONE
