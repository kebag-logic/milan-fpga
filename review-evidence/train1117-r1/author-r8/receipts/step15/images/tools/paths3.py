"""paths3.py <route dir>: the worst setup path of the design and of each system clock at the slow 85 C corner, and
the worst hold path at the fast 85 C corner, from the signoff timing reports (each path's header lines)."""
import re, sys
from pathlib import Path
d = Path(sys.argv[1])
def paths(rpt, kind):
    t = (d / rpt).read_text(errors="replace")
    out = []
    for b in re.split(r"\n(?=Slack \()", t)[1:]:
        first = b.split("\n")[0]
        if kind in first:
            m = re.search(r"([-\d.]+)ns", first)
            grp = re.search(r"Path Group:\s+(\S+)", b)
            out.append((float(m[1]), grp[1] if grp else "?", b))
    return sorted(out, key=lambda x: x[0])
def show(label, p):
    keep = [l.strip() for l in p[2].split("\n") if re.match(r"^  (Source|Destination|Data Path Delay|Logic Levels):", l)]
    print(f"{label}: slack {p[0]:+.3f} ns, group {p[1]}\n    " + "\n    ".join(k[:160] for k in keep))
setup = paths("alinx_ax7101_signoff_Slow_85C_timing.rpt", "(required time - arrival time)")
show("design worst setup, Slow_85C", setup[0])
for clk in ("milansoc_crg_clkout0", "milansoc_crg_clkout1", "eth_clocks0_rx"):
    p = [x for x in setup if x[1] == clk]
    if p:
        show(f"worst setup at {clk}, Slow_85C", p[0])
hold = paths("alinx_ax7101_signoff_Fast_85C_timing.rpt", "(arrival time - required time)")
show("design worst hold, Fast_85C", hold[0])
