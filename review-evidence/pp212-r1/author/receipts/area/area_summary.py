#!/usr/bin/env python3
"""area_summary.py <dir>: one row per yosys stat file of area.sh."""
import re, sys
from pathlib import Path
out = Path(sys.argv[1])
rows = []
for name in ["listener_n2", "listener_n8", "srp_top_2x2", "srp_top_8x8"]:
    text = (out / f"{name}.stat").read_text()
    cells = {m.group(2): int(m.group(1)) for m in re.finditer(r"^\s+(\d+)\s+(\S+)$", text, re.M)}
    lut = sum(v for k, v in cells.items() if re.fullmatch(r"LUT[1-6]", k))
    ff = sum(v for k, v in cells.items() if re.fullmatch(r"FD[RSCPE]{2}", k))
    ram = sum(v for k, v in cells.items() if k.startswith("RAM"))
    rows.append(f"| {name} | {lut} | {cells.get('INV', 0)} | {ff} | {ram} | {cells.get('CARRY4', 0)} | "
                f"{cells.get('MUXF7', 0) + cells.get('MUXF8', 0)} |")
(out / "SUMMARY.md").write_text("| shape | LUT1-6 | INV | FF | RAM cells | CARRY4 | MUXF7/8 |\n"
                                 "|---|---:|---:|---:|---:|---:|---:|\n" + "\n".join(rows) + "\n")
print((out / "SUMMARY.md").read_text())
