"""#814 round 2: the recipe's two comparison directives (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, "Integrated
measurements"), from route-1x1's own synthesis checkpoint, default seed: the recipe's snippet, writing the scripts
only (each run is launched through the slot wrapper). Refuses unless route-1x1's log shows the checkpoint written.
usage: dir_prep.py <repo> <work>
"""
import importlib.util
from pathlib import Path
import shutil
import sys

root, work = Path(sys.argv[1]), Path(sys.argv[2])
gateware = work / "ax7101/gateware"
log = (gateware / "baseline.log").read_text()
assert "write_checkpoint -force alinx_ax7101_synth.dcp" in log and "Command: opt_design" in log, "synthesis checkpoint not written yet"
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
