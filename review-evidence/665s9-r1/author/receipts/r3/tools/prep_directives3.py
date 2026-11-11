"""prep_directives3.py <route>: #818's three directives on the split route's one synthesis checkpoint (round 3: the
host reset at 08:23 cut the recipe route after its synthesis checkpoint was written, during placement). Each is the
integrated script's tail from "# Add pre-optimize commands" (its full-split census and reports included) with only
the placement directive set, opening that checkpoint; ExtraPostPlacementOpt, the recipe's, keeps the tail as is."""
import shutil
import sys
from pathlib import Path

work = Path(sys.argv[1])
gateware = work / "split/gateware"
integ = (gateware / "baseline_integrated.tcl").read_text()
tail = integ[integ.index("# Add pre-optimize commands"):]
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("ExtraPostPlacementOpt", "ExtraTimingOpt", "AltSpreadLogic_high"):
    output = work / f"split-{directive}"
    output.mkdir()
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    (output / "baseline_implementation.tcl").write_text(script)
    print(output / "baseline_implementation.tcl")
