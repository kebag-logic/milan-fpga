#!/usr/bin/env bash
# #774 round 2: route-1x1 only (the round-2 assignment asks for route-1x1 when RTL changes), the
# round-1 bank's route leg unchanged (scripts/vivado_bank.sh): the shipping AX7101 1x1 export per
# docs/testing/PP_SHADOW_BASELINE_RECIPE.md in one clean clone at <rev>, --single-thread-synthesis,
# one Vivado run under the exclusive lock, then checked against the committed record.
# usage: vivado_route.sh <label> <rev>
set -uo pipefail
label=$1; rev=$2
here=$(cd "$(dirname "$0")/.." && pwd)
S=$VALIDATION_STORAGE/scratch/774-a665
W=$S/viv-$label
export REPO=$S/clone-viv-$label
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/679-a557/sdk
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
mkdir -p "$W"
exec > "$W/bank.out" 2>&1
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp START
[ -d "$REPO" ] || bash "$here/make_clone.sh" "$REPO" "$rev" || exit 2
cd "$REPO" || exit 2
git rev-parse HEAD; git -C protocol-processor rev-parse HEAD; git -C gptp-processor rev-parse HEAD; git status --short
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
# one export per shape, each in its own work directory with its own ROM links
export_shape() {   # <shape> <work>
  local shape=$1 work=$2
  mkdir -p "$work/builder" "$work/roms"
  cleanup
  test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || return 1
  ln -s "$work/builder" sw/builder/out
  ln -s "$work/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
  ln -s "$work/roms/ucode.hex" configs/generated/ucode.hex
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
# this session's unit is capped at 12 GB and a route peaks near 8.4 GB: Vivado starts only with the unit's other
# work under 3 GB of anonymous memory (its page cache is reclaimed under pressure, so MemoryCurrent overstates it)
unit_anon() {
  local cg; cg=$(systemctl --user show milan-774-a665b.service -p ControlGroup --value 2>/dev/null)
  awk '/^anon /{print $2}' "/sys/fs/cgroup$cg/memory.stat" 2>/dev/null || echo 0
}
vivado_run() {     # <dir> <script> <name>
  local mem; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  while [ "$mem" -lt 20971520 ]; do echo "waiting: MemAvailable $mem kB"; sleep 60; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo); done
  local um; um=$(unit_anon)
  while [ "${um:-0}" -gt 3221225472 ]; do echo "waiting: unit anon $um"; sleep 60; um=$(unit_anon); done
  stamp "VIVADO-START $3"
  local vrc=0
  ( cd "$1" && flock -x $VIVADO_LOCK vivado -mode batch -source "$2" -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
  stamp "VIVADO-END $3 rc=$vrc"
  return $vrc
}
gate() {           # <dir> <endpoint>
  local grc=0
  python3 syn/ooc/pp_resource_gate.py check "$1" --endpoint "$2" > "$W/$2-check.log" 2>&1 || grc=$?
  echo "GATE $2 rc=$grc"; cat "$W/$2-check.log"
}
# route-1x1
W1=$W/w1
export_shape ax7101 "$W1" || { echo EXPORT-1x1-FAILED; exit 3; }
python3 syn/ooc/pp_baseline.py "$W1/ax7101/gateware" --single-thread-synthesis || exit 3
stamp EXPORT-1x1-DONE
vivado_run "$W1/ax7101/gateware" baseline_integrated.tcl route-1x1
gate "$W1/ax7101/gateware" route-1x1
stamp BANK-DONE
echo BANK-DONE
