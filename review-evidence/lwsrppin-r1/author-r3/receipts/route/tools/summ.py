"""summ.py <gateware dir> <receipt dir> <label>: the routed image's totals and signoff slacks, plus receipts.

Prints the Slice LUT, Slice Register, Block RAM Tile, RAMB36, RAMB18 and DSP totals from the placed
(alinx_ax7101_utilization_place.rpt) and post-route (baseline_utilization.rpt) utilization reports, and each signoff
corner's WNS/TNS/WHS/THS from its Design Timing Summary. Copies the utilization reports, route status, check_timing and
each signoff timing report's head (through its Design Timing Summary and clock summary, under 200 KB) to the receipt
dir, and the sha256 of each checkpoint.
"""
import hashlib
import re
import shutil
import sys
from pathlib import Path

g, out, label = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
ROWS = (("LUT", r"\| Slice LUTs\s+\|\s+([\d.]+)"), ("FF", r"\| Slice Registers\s+\|\s+([\d.]+)"),
        ("BRAM tile", r"\| Block RAM Tile\s+\|\s+([\d.]+)"), ("RAMB36", r"\|\s+RAMB36/FIFO\*\s+\|\s+([\d.]+)"),
        ("RAMB18", r"\|\s+RAMB18\s+\|\s+([\d.]+)"), ("DSP", r"\| DSPs\s+\|\s+([\d.]+)"))
for rpt in ("alinx_ax7101_utilization_place.rpt", "baseline_utilization.rpt"):
    text = (g / rpt).read_text()
    state = re.search(r"Design State : (.*)", text)[1].strip()
    vals = ", ".join(f"{name} {re.search(pat, text)[1]}" for name, pat in ROWS)
    print(f"{label} {rpt} ({state}): {vals}")
    shutil.copy2(g / rpt, out / rpt)
for c in ("Slow_85C", "Slow_0C", "Fast_85C", "Fast_0C"):
    p = g / f"alinx_ax7101_signoff_{c}_timing.rpt"
    text = p.read_text(errors="replace")
    at = text.index("Design Timing Summary")
    m = re.search(r"\n\s+WNS\(ns\).*\n\s+-+.*\n\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)",
                  text[at:at + 4000])
    print(f"{label} {c}: WNS {float(m[1]):+.3f} TNS {float(m[2]):.3f} ({m[3]} failing), "
          f"WHS {float(m[5]):+.3f} THS {float(m[6]):.3f} ({m[7]} failing)")
    cut = text.find("Intra Clock Table")
    head = text[: cut if cut > 0 else 150_000][:190_000]
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    (out / f"{p.name}.stub.txt").write_text(f"{p.name}: {p.stat().st_size} bytes, sha256 {digest}; over 200 KB, "
                                            f"kept in scratch. Its head, through the clock summary:\n{head}")
for name in ("alinx_ax7101_route_status.rpt", "alinx_ax7101_signoff_check_timing.rpt", "alinx_ax7101_iob_pack.rpt"):
    if (g / name).exists():
        shutil.copy2(g / name, out / name)
for dcp in sorted(g.glob("*.dcp")):
    print(f"{label} {dcp.name} sha256 {hashlib.sha256(dcp.read_bytes()).hexdigest()} {dcp.stat().st_size}")
