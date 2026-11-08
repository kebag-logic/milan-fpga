"""route_figures.py <work> <out.md>: each directive's post-route figures from its own reports (baseline_utilization.rpt,
the recipe's post-route report_utilization; alinx_ax7101_route_status.rpt; the four signoff timing summaries), one row
per directive, with the sha256 of every report read."""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mask import mask
work, out = Path(sys.argv[1]), Path(sys.argv[2])
DIRS = (("ExtraPostPlacementOpt", work / "ax7101/gateware"), ("AltSpreadLogic_high", work / "ax7101-AltSpreadLogic_high"),
        ("ExtraTimingOpt", work / "ax7101-ExtraTimingOpt"))
def util(t, name):
    m = re.search(r"^\|\s*" + re.escape(name) + r"\s*\|\s*([0-9.]+)\s*\|", t, re.M)
    return m.group(1) if m else "?"
def summ(p):
    l = p.read_text(errors="replace").splitlines()
    i = next(n for n, x in enumerate(l) if "Design Timing Summary" in x)
    h = next(n for n in range(i, i + 12) if l[n].strip().startswith("WNS(ns)"))
    v = l[h + 2].split(); return v[0], v[4]
rows, shas = [], []
for name, d in DIRS:
    u = d / "baseline_utilization.rpt"; t = u.read_text(errors="replace")
    rs = (d / "alinx_ax7101_route_status.rpt").read_text(errors="replace")
    err = re.search(r"nets with routing errors\.*\s*:\s*(\d+)", rs).group(1)
    c = {k: summ(next(d.glob(f"*_signoff_{k}_timing.rpt"))) for k in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")}
    slc = util(t, "Slice")
    rows.append(f"| {name} | {util(t, 'Slice LUTs')} | {util(t, 'Slice Registers')} | {slc} | {15850 - int(slc) if slc.isdigit() else '?'} | "
                f"{util(t, 'RAMB36/FIFO*') if util(t, 'RAMB36/FIFO*') != '?' else util(t, 'RAMB36/FIFO')} / {util(t, 'RAMB18')} | {util(t, 'DSPs')} | "
                f"{c['Slow_0C'][0]} / {c['Slow_0C'][1]} | {c['Slow_85C'][0]} / {c['Slow_85C'][1]} | {c['Fast_0C'][0]} / {c['Fast_0C'][1]} | "
                f"{c['Fast_85C'][0]} / {c['Fast_85C'][1]} | {err} |")
    for p in [u, d / "alinx_ax7101_route_status.rpt", *sorted(d.glob("*_signoff_*_timing.rpt"))]:
        shas.append(f"- `{name}/{p.name}`: sha256 `{hashlib.sha256(p.read_bytes()).hexdigest()}`, {p.stat().st_size} bytes")
text = ("# Route set at the merge commit, post-route figures per directive\n\n"
        "| Directive | LUT | FF | Slice | Free | RAMB36 / RAMB18 | DSP | Slow_0C WNS / WHS | Slow_85C | Fast_0C | Fast_85C | Routing errors |\n"
        "|---|---:|---:|---:|---:|---|---:|---|---|---|---|---:|\n" + "\n".join(rows) + "\n\nReports read (not copied):\n\n" + "\n".join(shas) + "\n")
out.write_text(mask(text)); print(text)
