"""prep_directives.py <src> <route>: #818's two comparison directives on the split route's synthesis checkpoint, as
docs/testing/PP_SHADOW_BASELINE_RECIPE.md writes them (only the placement directive changes; same checkpoint)."""
import importlib.util
import shutil
import sys
from pathlib import Path

root, work = Path(sys.argv[1]), Path(sys.argv[2])
gateware = work / "split/gateware"
spec = importlib.util.spec_from_file_location("baseline", root / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
source = (gateware / "alinx_ax7101.tcl").read_text()
_, tail = baseline.split_once(source, "# Add pre-optimize commands")
tail, _ = baseline.split_once(tail, "# Bitstream generation")
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    output = work / f"split-{directive}"
    output.mkdir()
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    script += baseline.REPORTS + baseline.PP_REPORTS
    script += baseline.SCOPE_TIMING + "\nquit\n"
    (output / "baseline_implementation.tcl").write_text(script)
    print(output / "baseline_implementation.tcl")
