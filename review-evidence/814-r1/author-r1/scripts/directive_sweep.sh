#!/usr/bin/env bash
# #814: the recipe's other two placement directives (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, "Integrated
# measurements"), from route-1x1's own synthesis checkpoint, the default seed, one Vivado run at a time under the
# exclusive lock and only above 20 GB MemAvailable. The #787 lane's driver, its paths passed in.
# usage: directive_sweep.sh <repo> <work>
set -uo pipefail
export REPO=$1 WORK=$2
stamp() { echo "== $1 $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"; }
stamp DIRECTIVES-START
python3 - <<'PY' || exit 2
import importlib.util
import os
from pathlib import Path
import shutil

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
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
    if output.exists():
        continue
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
for directive in AltSpreadLogic_high ExtraTimingOpt; do
  [ -e "$WORK/ax7101-$directive/alinx_ax7101_route.dcp" ] && continue
  mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  while [ "$mem" -lt 20971520 ]; do echo "waiting: MemAvailable $mem kB"; sleep 60; mem=$(awk '/MemAvailable/{print $2}' /proc/meminfo); done
  stamp "VIVADO-START $directive"
  vrc=0
  ( cd "$WORK/ax7101-$directive" && flock -x $VIVADO_LOCK vivado -mode batch -source baseline_implementation.tcl \
      -nojournal -log baseline.log > vivado.out 2>&1 ) || vrc=$?
  stamp "VIVADO-END $directive rc=$vrc"
done
stamp DIRECTIVES-DONE
