#!/usr/bin/env python3
"""Recipe "Hierarchical mapping comparison" block, restricted to the 1x1 shape.
usage: WORK=<work> yosys_hier_1x1.py"""
import os
from pathlib import Path
import subprocess

work = Path(os.environ["WORK"])
for shape in ("ax7101",):
    output = work / f"{shape}-yosys"
    values = (work / f"{shape}-ooc/baseline_chparam.txt").read_text().split()
    script = f"read_verilog {output}/KL_pp_shadow.ooc.v; "
    for item in values:
        key, value = item.split("=", 1)
        script += f"chparam -set {key} {value} KL_pp_shadow; "
    script += "synth_xilinx -family xc7 -top KL_pp_shadow; "
    script += "stat; write_json hierarchical.json\n"
    (output / "hierarchical.ys").write_text(script)
    with (output / "hierarchical.log").open("w") as log:
        subprocess.run(["yosys", "-s", "hierarchical.ys"], cwd=output,
                       stdout=log, stderr=subprocess.STDOUT, check=True)
