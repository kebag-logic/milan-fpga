"""#806 round 2: one route-1x1 directive run's figures, read with the resource gate's own parsers
(syn/ooc/pp_resource_gate.py utilization() and timing()), each signoff corner's Design Timing Summary, and
the worst setup and hold path at every corner (the smallest slack in that corner's report_timing_summary).
The gate itself cannot check a directive run: the recipe's implementation script is not one of its recipe scripts.
usage: python3 -I directive_figures.py <repo> <label>=<run-dir>..."""
import importlib.util
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", repo / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
CORNERS = ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")
FIELDS = ("Slack", "Source", "Destination", "Path Group", "Path Type", "Data Path Delay", "Logic Levels")


def summary(text):
    lines = text.splitlines()
    i = next(n for n, l in enumerate(lines) if l.startswith("| Design Timing Summary"))
    head = next(n for n in range(i, len(lines)) if lines[n].strip().startswith("WNS(ns)"))
    v = lines[head + 2].split()
    return {"WNS": float(v[0]), "TNS": float(v[1]), "WHS": float(v[4]), "THS": float(v[5])}


def paths(text):
    out = []
    for block in re.split(r"\n(?=Slack \()", text)[1:]:
        row = {}
        for line in block.splitlines()[:16]:
            m = re.match(r"\s*([A-Za-z ]+?)\s*(?:\([A-Z]+\))?\s*:\s+(.*\S)", line)
            if m and m.group(1) in FIELDS and m.group(1) not in row:
                row[m.group(1)] = m.group(2)
        row["slack"] = float(re.match(r"Slack \(\w+\)\s*:\s*(-?[\d.]+)", block).group(1))
        out.append(row)
    return out


for arg in sys.argv[2:]:
    label, run = arg.split("=", 1)
    run = Path(run)
    fig = gate.utilization((run / "baseline_utilization.rpt").read_text(), "route")
    fig.update(gate.timing((run / "baseline_timing.rpt").read_text()))
    status = (run / "alinx_ax7101_route_status.rpt").read_text()
    nets = re.search(r"routable nets\.+ :\s+(\d+)", status).group(1)
    errs = re.search(r"nets with routing errors\.+ :\s+(\d+)", status).group(1)
    print(f"## {label}")
    print("figures (gate parsers): " + ", ".join(f"{k} {v}" for k, v in fig.items()))
    print(f"route status: {nets} routable nets, {errs} with routing errors")
    worst = {}
    for c in CORNERS:
        t = (run / f"alinx_ax7101_signoff_{c}_timing.rpt").read_text()
        s = summary(t)
        print(f"{c}: WNS {s['WNS']:+.3f} TNS {s['TNS']:.3f} WHS {s['WHS']:+.3f} THS {s['THS']:.3f}")
        ps = paths(t)
        for kind in ("Setup", "Hold"):
            sel = [p for p in ps if p.get("Path Type", "").startswith(kind)]
            p = min(sel, key=lambda p: p["slack"])
            worst[(c, kind)] = p
    for (c, kind), p in worst.items():
        print(f"worst {kind.lower()} {c}: slack {p['slack']:+.3f} ns | {p.get('Source')} -> {p.get('Destination')} | "
              f"group {p.get('Path Group')} | data path {p.get('Data Path Delay')} | levels {p.get('Logic Levels')}")
    print()
