"""prep_directives.py <route>: #818's two comparison directives on the split route's synthesis checkpoint, as round 1
wrote them for full-split: the integrated script's tail from "# Add pre-optimize commands" (its full-split census and
reports included) with only the placement directive replaced, opening the same synthesis checkpoint."""
import shutil
import sys
from pathlib import Path

work = Path(sys.argv[1])
gateware = work / "split/gateware"
integ = (gateware / "baseline_integrated.tcl").read_text()
tail = integ[integ.index("# Add pre-optimize commands"):]
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    output = work / f"split-{directive}"
    output.mkdir()
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    (output / "baseline_implementation.tcl").write_text(script)
    print(output / "baseline_implementation.tcl")
