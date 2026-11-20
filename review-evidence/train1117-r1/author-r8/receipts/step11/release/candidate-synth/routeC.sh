#!/usr/bin/env bash
# routeC.sh: the candidate c8ff391a's release image placed and routed from its synthesis checkpoint with the recipe's
# ExtraPostPlacementOpt tail (the integrated script's tail, as relroute.sh writes the comparison directives), for a
# like-for-like placed figure against p11's release route (attribution of the resource gate's LUT growth).
set -u
R=<scratch>/r5relC; REPO=$R/repo; WORK=$R/work
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic REPO WORK
export PATH=/usr/local/bin:/usr/bin:/bin:<home>/Xilinx/2026.1/Vivado/bin
python3 - <<'PY'
import importlib.util, os, shutil
from pathlib import Path
root, work = Path(os.environ["REPO"]), Path(os.environ["WORK"])
gateware = work / "ax7101/gateware"
spec = importlib.util.spec_from_file_location("baseline", root / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec); spec.loader.exec_module(baseline)
source = (gateware / "alinx_ax7101.tcl").read_text()
_, tail = baseline.split_once(source, "# Add pre-optimize commands")
tail, _ = baseline.split_once(tail, "# Bitstream generation")
assert tail.count("place_design -directive ExtraPostPlacementOpt") == 1
out = work / "ax7101-ExtraPostPlacementOpt"; out.mkdir(exist_ok=True)
shutil.copy2(gateware / "alinx_ax7101.xdc", out)
script = "set_param general.maxThreads 32\n" + f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n" + tail
script += baseline.REPORTS + baseline.PP_REPORTS + baseline.SCOPE_TIMING + "\nquit\n"
(out / "baseline_implementation.tcl").write_text(script)
PY
source <home>/Xilinx/2026.1/Vivado/settings64.sh
cd $WORK/ax7101-ExtraPostPlacementOpt && vivado -mode batch -source baseline_implementation.tcl -nojournal -log baseline.log > vivado.out 2>&1; echo $? > route.rc
echo "routeC rc=$(cat route.rc) $(date +%T)"
