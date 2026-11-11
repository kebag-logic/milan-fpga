"""buspaths.py <report>...: every setup (max delay) path of path group milansoc_crg_clkout0 in each Vivado timing
summary report, with its section (from and to clock), slack, source, destination, delay and levels."""
import re, sys
from pathlib import Path
for rpt in map(Path, sys.argv[1:]):
    t = rpt.read_text(errors="replace")
    cmd = re.search(r"\| Command\s+: (.*)", t)[1].strip()
    print(f"### {rpt.parent.name}/{rpt.name}\n# {cmd}")
    rows = []
    for b in re.split(r"\n(?=Slack \()", t)[1:]:
        head = b.split("\n")[0]
        if "(required time - arrival time)" not in head:
            continue
        g = re.search(r"Path Group:\s+(\S+)", b)
        if not g or g[1] != "milansoc_crg_clkout0":
            continue
        slack = float(re.search(r"([-\d.]+)ns", head)[1])
        f = {k: re.search(rf"^  {k}:\s+(.*)$", b, re.M) for k in
             ("Source", "Destination", "Path Type", "Data Path Delay", "Logic Levels")}
        clocks = re.findall(r"clocked by (\S+)", b)
        rows.append((slack, clocks[0] if clocks else "?", *(f[k][1].strip() if f[k] else "?" for k in
                     ("Source", "Destination", "Data Path Delay", "Logic Levels", "Path Type"))))
    rows.sort(key=lambda r: r[0])
    print(f"# {len(rows)} setup paths of group milansoc_crg_clkout0")
    for i, (s, clk, src, dst, dly, lv, pt) in enumerate(rows, 1):
        print(f"{i:2d} slack {s:+.3f} ns  from clock {clk}\n     Source: {src}\n     Destination: {dst}\n"
              f"     Data Path Delay: {dly}\n     Logic Levels: {lv}")
