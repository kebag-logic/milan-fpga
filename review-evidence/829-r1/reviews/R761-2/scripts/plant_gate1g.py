#!/usr/bin/env python3
"""Does gate 1g's reader accept a commented-out MII table entry? usage: plant_gate1g.py <tree>"""
import importlib.util, sys
from pathlib import Path
tree = Path(sys.argv[1]); sys.path.insert(0, str(tree / "sw/builder"))
spec = importlib.util.spec_from_file_location("tb", tree / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec); sys.modules["tb"] = tb; spec.loader.exec_module(tb)
soc = (tree / "sw/litex/milan_soc.py").read_text()
o = '"mii": {"GPTP_ETH_TICK_NS_P": 40,'
assert soc.count(o) == 1
print("commented entry:", tb._launch_shape_findings(soc.replace(o, '"mii": {# "GPTP_ETH_TICK_NS_P": 40,\n')))
