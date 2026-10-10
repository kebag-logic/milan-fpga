#!/usr/bin/env python3
# Reviewer probe (R590-1, #640 lane M2): apply the resource gate's own
# per-figure verdict to the M2 route figures the author published, against
# the committed route-1x1 record. This judges the arithmetic only; the route
# reports themselves are not published, so the figures are the author's.
#   gate_arith.py <repo>
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402

entry = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]
base = entry["record"]["figures"]
m2 = {"LUT": 50139, "FF": 54354, "SLICE": 15771, "RAMB36": 74, "RAMB18": 27,
      "DSP": 14, "WNS_ns": 0.306, "WHS_ns": 0.019}
bad = 0
for fig in gate.GATED["route"]:
    text, ok = gate.verdict_for(entry, fig, base[fig], m2[fig])
    bad += not ok
    print(f"{fig}: record {base[fig]} -> M2 {m2[fig]}: {text}")
tiles = m2["RAMB36"] + m2["RAMB18"] / 2
print(f"BRAM_TILE {tiles} vs ceiling {entry['ceiling']['BRAM_TILE']}: {'ok' if tiles <= entry['ceiling']['BRAM_TILE'] else 'OVER'}")
bad += tiles > entry["ceiling"]["BRAM_TILE"]
print("ARITH", "PASS" if not bad else "FAIL")
sys.exit(1 if bad else 0)
