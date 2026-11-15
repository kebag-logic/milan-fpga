"""worst10.py <route dir> [n]: the n (default 10) worst setup paths of the whole design, from the route's
report_timing_summary (alinx_ax7101_timing.rpt, 10 paths per path group, so the union's first 10 are the design's
first 10), and the same from the Slow_85C signoff report (5 per group: its first 5 are exact). S9's buspaths.py
parse, over every path group instead of the bus clock's alone. Also the worst hold path at Fast_85C and the
utilisation lines of the placed design."""
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10


def paths(rpt: Path, kind: str) -> list:
    t = rpt.read_text(errors="replace")
    rows, seen = [], set()
    for b in re.split(r"\n(?=Slack \()", t)[1:]:
        head = b.split("\n")[0]
        if kind not in head:
            continue
        slack = float(re.search(r"([-\d.]+)ns", head)[1])
        f = {k: re.search(rf"^  {k}:\s+(.*)$", b, re.M) for k in
             ("Source", "Destination", "Path Group", "Data Path Delay", "Logic Levels", "Requirement")}
        v = {k: (f[k][1].strip() if f[k] else "?") for k in f}
        clocks = re.findall(r"clocked by (\S+?)[ )]", b)
        key = (v["Source"], v["Destination"], v["Path Group"], slack)
        if key in seen:
            continue
        seen.add(key)
        rows.append((slack, clocks[0] if clocks else "?", v))
    rows.sort(key=lambda r: r[0])
    return rows


def show(title: str, rows: list, k: int) -> None:
    print(f"## {title}")
    for i, (s, clk, v) in enumerate(rows[:k], 1):
        dly = re.sub(r"\s+\(.*", "", v["Data Path Delay"])
        print(f"{i:2d} {s:+.3f} ns  group {v['Path Group']}  (launch {clk}, req {v['Requirement'].split()[0]})\n"
              f"     {v['Source']}\n  -> {v['Destination']}\n     delay {dly}, levels {v['Logic Levels']}")


show(f"{n} worst setup, route report (alinx_ax7101_timing.rpt)",
     paths(d / "alinx_ax7101_timing.rpt", "(required time - arrival time)"), n)
show("5 worst setup, Slow_85C signoff", paths(d / "alinx_ax7101_signoff_Slow_85C_timing.rpt",
                                              "(required time - arrival time)"), 5)
show("3 worst hold, Fast_85C signoff", paths(d / "alinx_ax7101_signoff_Fast_85C_timing.rpt",
                                            "(arrival time - required time)"), 3)
print("## utilisation (alinx_ax7101_utilization_place.rpt)")
u = (d / "alinx_ax7101_utilization_place.rpt").read_text(errors="replace")
for name in ("Slice LUTs", "LUT as Memory", "Slice Registers", "Slice", "Block RAM Tile", "RAMB36/FIFO",
             "RAMB18", "DSPs", "CARRY4"):
    m = re.search(rf"^\|\s+{re.escape(name)}\*?\s+\|\s+([\d.]+)\s+\|\s+\d+\s+\|\s+\d+\s+\|\s+(\d+)\s+\|\s+([\d.<]+)\s+\|", u, re.M)
    if m:
        print(f"{name}: {m[1]} / {m[2]} ({m[3]} %)")
    elif name == "CARRY4":
        m = re.search(r"^\|\s+CARRY4\s+\|\s+(\d+)\s+\|", u, re.M)
        if m:
            print(f"CARRY4: {m[1]}")
r = d / "alinx_ax7101_route_status.rpt"
if r.exists():
    for line in r.read_text().splitlines():
        if re.search(r"routable nets|fully routed|routing errors", line):
            print(line.strip())
