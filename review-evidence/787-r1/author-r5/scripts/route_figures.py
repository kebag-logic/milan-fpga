"""route_figures.py <label=run-dir>...: per routed run, the figures the round 3 and 4 assignments ask for, as Markdown.

For each run directory (the shipping gateware directory or a comparison directory): every signoff corner's Design
Timing Summary (WNS, TNS, WHS, THS), the post-route utilization the gate reads (`baseline_utilization.rpt`: Slice
LUTs, Slice Registers, Slice used and available, Block RAM Tile), and the worst setup path over every slow-corner
signoff report (the lowest `Slack` of a `Setup` path; the report lists each path group's worst paths), with its
source, destination, path group, requirement, data path delay and its logic and route parts, and logic levels.
Host paths are not printed: a run is named by its label."""
import re
import sys
from pathlib import Path

CORNERS = ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")


def design(text):
    """WNS, TNS, WHS, THS of the Design Timing Summary."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("WNS(ns)") and "THS(ns)" in line:
            v = lines[i + 2].split()
            return float(v[0]), float(v[1]), float(v[4]), float(v[5])
    raise SystemExit("no Design Timing Summary")


def util(text):
    """LUT, FF, slices used, slices available, BRAM tile."""
    def row(label):
        m = re.search(r"^\|\s*" + re.escape(label) + r"\s*\|\s*([\d.]+)\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*\|", text, re.M)
        if not m:
            raise SystemExit(f"no row {label}")
        return float(m.group(1)), int(m.group(2))
    lut, _ = row("Slice LUTs")
    ff, _ = row("Slice Registers")
    sl, avail = row("Slice")
    bram, bram_avail = row("Block RAM Tile")
    return int(lut), int(ff), int(sl), avail, bram, bram_avail


def paths(text):
    """Each reported path block: slack and its header fields."""
    out = []
    for block in re.split(r"\n(?=Slack(?: \((?:MET|VIOLATED)\))? :)", text)[1:]:
        m = re.match(r"Slack(?: \((MET|VIOLATED)\))? :\s+(-?[\d.]+)ns", block)
        if not m:
            continue
        def field(name):
            f = re.search(r"^\s*" + name + r":\s+(.*)$", block, re.M)
            return f.group(1).strip() if f else ""
        out.append({"slack": float(m.group(2)), "type": field("Path Type"), "source": field("Source"),
                    "destination": field("Destination"), "group": field("Path Group"),
                    "requirement": field("Requirement"), "delay": field("Data Path Delay"),
                    "levels": field("Logic Levels")})
    return out


def run(label, d):
    reports = {c: next(d.glob(f"*_signoff_{c}_timing.rpt")) for c in CORNERS}
    corners = {c: design(p.read_text(errors="replace")) for c, p in reports.items()}
    lut, ff, sl, avail, bram, bram_avail = util((d / "baseline_utilization.rpt").read_text(errors="replace"))
    worst = []
    for c in ("Slow_0C", "Slow_85C"):
        for p in paths(reports[c].read_text(errors="replace")):
            if p["type"].startswith("Setup"):
                worst.append((p["slack"], c, p))
    worst.sort(key=lambda t: t[0])
    lines = [f"### {label}", "", "| Corner | WNS ns | TNS ns | WHS ns | THS ns |", "|---|---:|---:|---:|---:|"]
    for c in CORNERS:
        w, t, h, th = corners[c]
        lines.append(f"| {c} | {w:+.3f} | {t:.3f} | {h:+.3f} | {th:.3f} |")
    lines += ["", f"LUT {lut:,}; FF {ff:,}; slices {sl:,} of {avail:,} ({avail - sl:,} free); "
              f"Block RAM tiles {bram:g} of {bram_avail}", ""]
    s, c, p = worst[0]
    tied = sorted({cc for ss, cc, pp in worst if ss == s and pp["source"] == p["source"]
                   and pp["destination"] == p["destination"]})
    lines += [f"Worst setup path: slack {s:+.3f} ns at {', '.join(tied)}; group `{p['group']}`; "
              f"`{p['source']}` -> `{p['destination']}`; requirement {p['requirement']}; "
              f"data path {p['delay']}; logic levels {p['levels']}", ""]
    return "\n".join(lines)


for arg in sys.argv[1:]:
    label, path = arg.split("=", 1)
    print(run(label, Path(path)))
