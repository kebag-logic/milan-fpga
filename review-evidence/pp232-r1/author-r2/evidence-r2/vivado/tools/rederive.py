#!/usr/bin/env python3
"""Re-derive the #232 lane's Vivado figures from this packet's files alone.

Usage: python3 tools/rederive.py [PACKET_DIR]   (default: this script's parent's parent)

Reads, per run directory: #638's utilization report (baseline_utilization.rpt)
and hierarchical utilization (baseline_hierarchy.rpt), the timing extract (its
first block is #638's baseline_timing.rpt), the route status, the log
extract's diagnostic counts and the cell census. Prints each run's figures,
then the head-minus-base deltas the PR body quotes.
"""
import re
import sys
from pathlib import Path

SCOPES = ("u_notify", "u_resp", "u_d3")


def util_row(text: str, label: str) -> float:
    m = re.search(r"^\|\s*" + re.escape(label) + r"\*?\s*\|\s*([0-9.]+)\s*\|", text, re.M)
    return float(m.group(1)) if m else float("nan")


def prim_row(text: str, prim: str) -> float:
    m = re.search(r"^\|\s*" + prim + r"\s*\|\s*([0-9]+)\s*\|", text, re.M)
    return float(m.group(1)) if m else float("nan")


def hier(text: str, scope: str) -> tuple[int, int, int]:
    """Total LUTs, LUTRAMs, FFs of the first row naming the scope."""
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 8 and cells[1] == scope:
            return int(cells[3]), int(cells[5]), int(cells[7])
    return (-1, -1, -1)


def summaries(text: str) -> list[tuple[str, float, float]]:
    """(source report, WNS, WHS) of every Design Timing Summary block in the extract."""
    out, name, want = [], "", False
    for line in text.splitlines():
        m = re.match(r"^##\s+(\S+):\d+-\d+$", line)
        if m:
            name, want = m.group(1), False
        elif re.match(r"^\s+-------\s+-------", line):
            want = True
        elif want and line.strip():
            cols = line.split()
            out.append((name, float(cols[0]), float(cols[4])))
            want = False
    return out


def census(text: str) -> dict[tuple[str, str], int]:
    out = {}
    for line in text.splitlines()[1:]:
        scope, prim, n = line.split("\t")
        out[(scope, prim)] = int(n)
    return out


def figures(run: Path) -> dict[str, object]:
    route = (run / "alinx_ax7101_route_status.rpt").exists()
    util = (run / "baseline_utilization.rpt").read_text()
    hierarchy = (run / "baseline_hierarchy.rpt").read_text()
    timing = (run / "timing-extract.txt").read_text()
    log = (run / "log-extract.txt").read_text()
    cells = census((run / "census.tsv").read_text())
    f: dict[str, object] = {
        "LUT": util_row(util, "Slice LUTs"), "LUT logic": util_row(util, "LUT as Logic"),
        "LUT memory": util_row(util, "LUT as Memory"), "FF": util_row(util, "Slice Registers"),
        "CARRY4": prim_row(util, "CARRY4"), "RAMB36": prim_row(util, "RAMB36E1"),
        "RAMB18": prim_row(util, "RAMB18E1"),
    }
    if route:
        f["Slice"] = util_row(util, "Slice")
        status = (run / "alinx_ax7101_route_status.rpt").read_text()
        nets = re.search(r"# of routable nets\.*\s*:\s*(\d+)", status).group(1)
        full = re.search(r"# of fully routed nets\.*\s*:\s*(\d+)", status).group(1)
        errs = re.search(r"# of nets with routing errors\.*\s*:\s*(\d+)", status).group(1)
        f["route"] = f"{full} of {nets} routable nets fully routed, {errs} with errors"
    sums = summaries(timing)
    f["WNS / WHS (design summary)"] = f"{sums[0][1]:+.3f} / {sums[0][2]:+.3f}" if sums else "n/a"
    if route and sums:
        f["WNS"], f["WHS"] = sums[0][1], sums[0][2]
    if route:
        f["corners WNS / WHS"] = "; ".join(f"{n.split('signoff_')[1].split('_timing')[0]} {w:+.3f} / {h:+.3f}"
                                          for n, w, h in sums if "signoff_" in n)
    for scope in SCOPES:
        lut, lutram, ff = hier(hierarchy, scope)
        f[f"{scope} LUT / LUTRAM / FF"] = (lut, lutram, ff)
    f["Synth 8-7186"] = int(re.search(r"^## Synth 8-7186: (\d+)", log, re.M).group(1))
    f["Synth 8-4445"] = int(re.search(r"^## Synth 8-4445: (\d+)", log, re.M).group(1))
    f["u_notify RAM32M / RAM64X1D / RAM32X1D"] = tuple(cells.get(("u_notify", p), 0)
                                                      for p in ("RAM32M", "RAM64X1D", "RAM32X1D"))
    fd = ("FDRE", "FDSE", "FDCE", "FDPE")
    f["u_notify rows_r_reg FD"] = sum(cells.get(("u_notify rows_r_reg", p), 0) for p in fd)
    f["u_notify ctr_last_r_reg FD"] = sum(cells.get(("u_notify ctr_last_r_reg", p), 0) for p in fd)
    return f


def delta(head: dict, base: dict, title: str) -> None:
    print(f"\n### {title}")
    for key in ("LUT", "LUT logic", "LUT memory", "FF", "Slice", "CARRY4"):
        if key in head:
            print(f"  {key:12s} {head[key]:>9,.0f} - {base[key]:>9,.0f} = {head[key] - base[key]:+,.0f}")
    if "WNS" in head:
        print(f"  WNS / WHS    {head['WNS']:+.3f} / {head['WHS']:+.3f} vs {base['WNS']:+.3f} / {base['WHS']:+.3f}:"
              f" {head['WNS'] - base['WNS']:+.3f} / {head['WHS'] - base['WHS']:+.3f}")
    for scope in SCOPES:
        h, b = head[f"{scope} LUT / LUTRAM / FF"], base[f"{scope} LUT / LUTRAM / FF"]
        print(f"  {scope:9s} LUT {h[0] - b[0]:+,d}, LUTRAM {h[1] - b[1]:+,d}, FF {h[2] - b[2]:+,d}")


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    runs = {p.name: figures(p) for p in sorted(packet.iterdir()) if (p / "census.tsv").exists()}
    for name, f in runs.items():
        print(f"## {name}")
        for key, value in f.items():
            print(f"  {key}: {value}")
    pairs = (("r1b-head-6e950fea-route-1x1", "r1b-main-5c71928a-route-1x1", "route at the round-1b merge: head - main"),
             ("r1-head-3ab2e4da-route-1x1", "r1-base-f4167536-route-1x1", "round 1 route: head - base"),
             ("r1-head-3ab2e4da-ooc-1x1", "r1-base-f4167536-ooc-1x1", "standalone 1x1: head - base"),
             ("r1-head-3ab2e4da-ooc-8x8", "r1-base-f4167536-ooc-8x8", "standalone 8x8: head - base"))
    for head, base, title in pairs:
        delta(runs[head], runs[base], title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
