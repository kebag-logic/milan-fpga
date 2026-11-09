#!/usr/bin/env python3
"""Print the routed LUT/FF totals of the top, milan_datapath, the KL_pp_shadow
wrapper and the DMA write bridge aligner in each published route hierarchy report.
Usage: datapath_ff.py <author-r2/receipts/area/runs directory>"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hier_rows import rows
runs = pathlib.Path(sys.argv[1])
for run in ("eppo", "aslh", "eto"):
    h = rows(runs / run / "baseline_hierarchy.rpt")
    top = min(h, key=len)
    want = {"top": top}
    for k in h:
        leaf = k.split("/")[-1]
        if "milan_datapath" in leaf and "dp" not in want: want["dp"] = k
        if leaf in ("pp_shadow", "KL_pp_shadow") and "wrap" not in want: want["wrap"] = k
        if k.endswith("dma_bridge_write_bridge/aligner"): want["aligner"] = k
    print(run, {n: (k, h[k]) for n, k in want.items()})
