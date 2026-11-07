"""set_measured.py <baseline>: route-1x1's `measured` note, the one field the gate's record --write leaves alone
(set by hand on every earlier re-record; #845's set_measured.py did the same). Touches no record, tolerance, floor or
ceiling, and no other endpoint; writes the gate's own format (indent 1)."""
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
b = json.loads(path.read_text())
G = "1616fc8f062fbf58c35ad31674b5b233207bbdb8"
P = "9210065779b0f698fd7bdb22323a1ed5b8482677"
DEV = "1eb5289db8fc9d139ce90cad2e380b4515793806"
L = "a6d7cdf3e29fd07f98e3fcd0b4d1402302f65a3e"
URL = "https://github.com/kebag-logic/milan-fpga/issues/843#issuecomment-6689115541"
note = (f"2026-11-07, issue #843 (PR #846 for FPGA-gPTP pin {G}, FPGA-gPTP #98 and #100, with clockAccuracy per board): "
        f"RTL inputs at lane commit {L}, the merge of dev {DEV}, with processor {P}; the lane's later commits change no synthesis input. "
        "Explicit synth.maxThreads 1, general.maxThreads 32; the recipe's three placement directives from one synthesis checkpoint, "
        "AltSpreadLogic_high selected by the gate at WNS +0.242 ns over ExtraPostPlacementOpt +0.062 ns and ExtraTimingOpt +0.058 ns. "
        "16 of 15,850 slices remain. Maintainer decision: against the thirteenth record the route moved by +692 LUT (tolerance +500), "
        "+172 FF (+600), -1 slice (80) and +2 DSP (0), with RAMB36 and RAMB18 unchanged, WNS -0.131 ns and WHS 0.000 ns; the gate refused "
        f"the LUT and DSP growth. The maintainer accepted this growth on 2026-11-06, with a re-baselined budget, in {URL} (the same "
        "decision as issue #845's issuecomment-6689114981). The differences include dev's movement since the thirteenth record (b16f0175): "
        "PR #841's transmitter hold and PR #842's prototype identity, without a new record. Every tolerance, floor and ceiling unchanged. "
        "docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the earlier records and this delta.")
b["endpoints"]["route-1x1"]["measured"] = note
path.write_text(json.dumps(b, indent=1) + "\n")
print("note set")
