#!/usr/bin/env python3
"""Show that a later route selecting another recipe directive stays comparable with the thirteenth record.

usage: directive_probe.py <clone>
"""
import copy, json, sys
from pathlib import Path
clone = Path(sys.argv[1])
sys.dont_write_bytecode = True
sys.path.insert(0, str(clone / "syn/ooc"))
import pp_resource_gate as g
entry = json.loads((clone / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]
slacks = {"Slow_0C": {"WNS_ns": 0.2, "WHS_ns": 0.02}}
def case(name, flow_from, flow_to, delta, inputs="0" * 64):
    cand = copy.deepcopy(entry["record"])
    cand["inputs_sha256"] = inputs
    cand["identity"]["flow"] = [line.replace(flow_from, flow_to) for line in cand["identity"]["flow"]]
    cand["figures"]["LUT"] += delta
    status, lines = g.judge(entry, cand, [], [], slacks)
    print(f"{name}: exit {status}; {lines[0][:90]}")
    return status
results = [case("selected ExtraPostPlacementOpt, within tolerance", "ExtraTimingOpt", "ExtraPostPlacementOpt", 100) == 0,
           case("selected AltSpreadLogic_high, +501 LUT", "ExtraTimingOpt", "AltSpreadLogic_high", 501) == 1,
           case("a directive outside the recipe", "ExtraTimingOpt", "Default", 0) == 2]
print("all as expected:", all(results))
