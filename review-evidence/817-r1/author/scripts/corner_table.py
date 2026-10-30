"""#817: the Design Timing Summary of each signoff corner report and of the routed summary, as Markdown rows.
usage: python3 corner_table.py <gateware-dir> <label>
"""
import re
import sys
from pathlib import Path

gateware, label = Path(sys.argv[1]), sys.argv[2]
reports = [("routed (alinx_ax7101_timing.rpt)", gateware / "alinx_ax7101_timing.rpt")]
reports += [(f"{speed} {temp}", gateware / f"alinx_ax7101_signoff_{speed}_{temp}_timing.rpt")
            for speed in ("Slow", "Fast") for temp in ("0C", "85C")]
print(f"| {label} | WNS ns | TNS ns | setup failing | WHS ns | THS ns | hold failing | WPWS ns |")
print("|---|---:|---:|---:|---:|---:|---:|---:|")
for name, path in reports:
    text = path.read_text()
    block = text[text.index("| Design Timing Summary"):]
    row = next(line for line in block.splitlines()[5:] if re.match(r"\s+-?\d", line))
    f = row.split()
    print(f"| {name} | {float(f[0]):+.3f} | {f[1]} | {f[2]} | {float(f[4]):+.3f} | {f[5]} | {f[6]} | {float(f[8]):+.3f} |")
