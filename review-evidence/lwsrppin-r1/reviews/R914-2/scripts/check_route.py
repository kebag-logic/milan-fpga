"""Cross-check published route figures against raw report sections and PR text.

Usage: python3 -I -B scripts/check_route.py <evidence-directory> <PR-body-snapshot>
"""
from pathlib import Path
import re
import sys

evidence, bodyfile = map(Path, sys.argv[1:])
body = bodyfile.read_text().strip()
draft = (evidence / "author-r2/PR-BODY.md").read_text().strip()
before = "binding check is the routed image."
after = "## Not changed here"
assert body.split(before)[0] == draft.split(before)[0]
assert body.split(after)[1] == draft.split(after)[1]
print("Live PR body matches author-r2/PR-BODY.md except the completed route section")
for side, expected in (("base", (43145, 51005, 78, 33, 11)), ("head", (43068, 51015, 78, 33, 11))):
    folder = evidence / "author-route/receipts" / side
    raw = (folder / "baseline_utilization.rpt").read_text()
    fields = (r"Slice LUTs", r"Slice Registers", r"RAMB36/FIFO\*", r"RAMB18", r"DSPs")
    counts = tuple(int(re.search(r"\|\s*" + field + r"\s*\|\s*(\d+)", raw)[1]) for field in fields)
    assert counts == expected
    print(side, "raw post-route LUT/FF/RAMB36/RAMB18/DSP:", counts)
    wns, whs = [], []
    for corner in ("Slow_85C", "Slow_0C", "Fast_85C", "Fast_0C"):
        lines = (folder / f"alinx_ax7101_signoff_{corner}_timing.rpt.stub.txt").read_text().splitlines()
        index = next(i for i, line in enumerate(lines) if "WNS(ns)" in line)
        fields = lines[index + 2].split()
        assert float(fields[0]) >= .030 and float(fields[4]) >= 0
        assert float(fields[1]) == 0 and fields[2] == "0" and float(fields[5]) == 0 and fields[6] == "0"
        wns.append(float(fields[0])); whs.append(float(fields[4]))
        print(side, corner, "WNS/WHS:", fields[0], fields[4], "zero failing setup/hold endpoints")
    print(side, "worst WNS/WHS:", min(wns), min(whs))
    assert (min(wns), min(whs)) == ((.193, .036) if side == "base" else (.194, .032))
print("Route table: agrees; -77 LUT, +10 FF; memory and DSP unchanged")
print("Recipe: 8x8/1if, ExtraPostPlacementOpt, aa30d77f versus dbba60e6")
print("No new route execution or bitstream claim")
