#!/usr/bin/env bash
# relroute.sh: the release (all-fabric) image's route set and resource gate at p11 (RULING-1118c item 2), by
# docs/testing/PP_SHADOW_BASELINE_RECIPE.md: the shipping export (build.sh ax7101's launch argv without --build),
# pp_baseline.py --single-thread-synthesis, the integrated route (ExtraPostPlacementOpt) through vivado-slot.sh, the
# other two placement directives from its synthesis checkpoint, then pp_resource_gate.py check --endpoint route-1x1
# with both comparisons. Measurement only; no bitstream, no hardware.
set -u
R=<scratch>/r5rel; REPO=$R/repo; WORK=$R/work; V=<management>/2026-09-23/vivado-slot.sh
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
export PATH=/usr/local/bin:/usr/bin:/bin:<home>/Xilinx/2026.1/Vivado/bin:<home>/br-milan-rv32/host/bin
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux REPO WORK LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
say() { echo "[rel $(date +%T)] $*"; }
cd $REPO
say "head $(git rev-parse HEAD)"
if [ ! -f $WORK/ax7101/gateware/alinx_ax7101.tcl ]; then
  python3 - <<'PY'
import json, os, shlex, subprocess
from pathlib import Path
root, work, python = Path(os.environ["REPO"]), Path(os.environ["WORK"]), os.environ["LITEX_PYTHON"]
preview = (work / "ax7101-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1, lines
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
env = dict(os.environ, PATH="<home>/litex-milan/venv/bin:" + os.environ["PATH"])
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True, env=env)
PY
  say "export rc=$?"
fi
python3 syn/ooc/pp_baseline.py $WORK/ax7101/gateware --single-thread-synthesis > $WORK/pp_baseline.log 2>&1; say "pp_baseline rc=$?"
source <home>/Xilinx/2026.1/Vivado/settings64.sh
$V bash -c "cd $WORK/ax7101/gateware && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1; echo \$? > route.rc"
say "integrated rc=$(cat $WORK/ax7101/gateware/route.rc 2>/dev/null)"
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
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    output = work / f"ax7101-{directive}"
    output.mkdir(exist_ok=True)
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    script += baseline.REPORTS + baseline.PP_REPORTS
    script += baseline.SCOPE_TIMING + "\nquit\n"
    (output / "baseline_implementation.tcl").write_text(script)
    print(output)
PY
for d in AltSpreadLogic_high ExtraTimingOpt; do
  ( $V bash -c "cd $WORK/ax7101-$d && vivado -mode batch -source baseline_implementation.tcl -nojournal -log baseline.log > vivado.out 2>&1; echo \$? > route.rc"; say "$d rc=$(cat $WORK/ax7101-$d/route.rc 2>/dev/null)" ) &
  sleep 90
done
wait
python3 syn/ooc/pp_resource_gate.py check $WORK/ax7101/gateware --endpoint route-1x1 \
  --comparison $WORK/ax7101-AltSpreadLogic_high --comparison $WORK/ax7101-ExtraTimingOpt > $WORK/resource_gate.log 2>&1
say "resource gate rc=$?"; tail -40 $WORK/resource_gate.log
echo done > $WORK/REL_DONE
