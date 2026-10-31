"""deciding_paths.py <label=run-dir>...: each routed run's deciding path, named from its own signoff reports.

For every run, reads the four signoff corners' timing reports (`*_signoff_<corner>_timing.rpt`), takes the setup path
with the lowest slack over all of them, and prints its slack, corner(s), path group, source, destination, logic
levels and logic/route split, then the instance hierarchy every cell on the path sits in (the path's cell column,
cut to its parent instance, consecutive repeats folded), so a reader can see which modules the path crosses. Then the
worst setup slack of any listed path whose source or destination names LiteDRAM's ZQCS timer, and the setup
paths of the `sys` clock (`milansoc_crg_clkout0`) the Slow_0C report lists. Host
paths are not printed: a run is named by its label."""
import re
import sys
from pathlib import Path

CORNERS = ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")


def paths(text):
    """Yield (slack, block) for each setup path block of a timing report."""
    blocks = re.split(r"\n(?=Slack \((?:MET|VIOLATED)\) :)", text)
    for block in blocks[1:]:
        if "Path Type:" not in block or "Setup" not in block.split("Path Type:", 1)[1].splitlines()[0]:
            continue
        slack = float(re.match(r"Slack \((?:MET|VIOLATED)\) :\s+(-?[\d.]+)ns", block).group(1))
        yield slack, block


def field(block, name):
    m = re.search(r"^\s*" + re.escape(name) + r":\s+(.*)$", block, re.M)
    return m.group(1).strip() if m else "?"


def hierarchy(block):
    """The parent instance of every cell on the data path, consecutive repeats folded."""
    out = []
    body = block.split("Data Path", 1)[-1] if "Data Path" in block else block
    for line in body.splitlines():
        m = re.search(r"\s(\S+/\S+)\s*$", line)
        if not m or "net (fo=" in line:
            continue
        cell = m.group(1).rsplit("/", 1)[0]
        cell = re.sub(r"/[^/]*(_LUT\d+_\d+|_i_\d+|_CARRY4_\d+|_replica)$", "", cell)
        if not out or out[-1] != cell:
            out.append(cell)
    seen = []
    for c in out:
        if c not in seen:
            seen.append(c)
    return seen


for arg in sys.argv[1:]:
    label, run = arg.split("=", 1)
    run = Path(run)
    best = None
    for corner in CORNERS:
        reports = sorted(run.glob(f"*_signoff_{corner}_timing.rpt"))
        if not reports:
            continue
        for slack, block in paths(reports[0].read_text(errors="replace")):
            if best is None or slack < best[0]:
                best = (slack, [corner], block)
            elif slack == best[0] and corner not in best[1] and field(block, "Source") == field(best[2], "Source") \
                    and field(block, "Destination") == field(best[2], "Destination"):
                best[1].append(corner)
    zq = None
    for corner in CORNERS:
        for report in sorted(run.glob(f"*_signoff_{corner}_timing.rpt")):
            for slack, block in paths(report.read_text(errors="replace")):
                if "zqcs" in field(block, "Source") or "zqcs" in field(block, "Destination"):
                    zq = slack if zq is None else min(zq, slack)
    slack, corners, block = best
    print(f"== {label}")
    print(f"slack {slack:+.3f} ns at {', '.join(corners)}; group {field(block, 'Path Group')}")
    print(f"source      {field(block, 'Source').split()[0]}")
    print(f"destination {field(block, 'Destination').split()[0]}")
    print(f"requirement {field(block, 'Requirement')}")
    print(f"data path   {field(block, 'Data Path Delay')}")
    print(f"levels      {field(block, 'Logic Levels')}")
    print("cells on the path (the source clock path first), by parent instance, in path order:")
    for cell in hierarchy(block):
        print(f"  {cell}")
    print("worst listed path naming the ZQCS timer: " + ("none listed in the signoff reports" if zq is None
                                                         else f"{zq:+.3f} ns"))
    report = sorted(run.glob("*_signoff_Slow_0C_timing.rpt"))[0].read_text(errors="replace")
    sys_paths = sorted((s, b) for s, b in paths(report) if field(b, "Path Group") == "milansoc_crg_clkout0")
    print(f"the {len(sys_paths)} setup paths of milansoc_crg_clkout0 (sys) the Slow_0C report lists (-max_paths 5):")
    for s, b in sys_paths:
        print(f"  {s:+.3f}  {field(b, 'Source').split()[0]} -> {field(b, 'Destination').split()[0]}")
    print()
