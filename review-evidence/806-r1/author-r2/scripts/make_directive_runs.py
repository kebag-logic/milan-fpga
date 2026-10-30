# #806 round 2: the recipe's "other two placement directives" step (docs/testing/PP_SHADOW_BASELINE_RECIPE.md),
# its script text unchanged, except that it only writes each directory's baseline_implementation.tcl;
# each Vivado run is then started through the host's slot wrapper.
# usage: python3 -I make_directive_runs.py <repo> <gateware> <work>
import importlib.util
import shutil
import sys
from pathlib import Path

root, gateware, work = (Path(a) for a in sys.argv[1:4])
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
