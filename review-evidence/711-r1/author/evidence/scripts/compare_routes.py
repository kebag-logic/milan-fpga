"""Compare two route-1x1 measurement directories report by report (scratch).

Usage: python3 -I compare_routes.py BASE_GATEWARE CAND_GATEWARE
Prints, per report, whether the files are byte-identical, and otherwise whether
they are identical once lines naming tool run metadata (dates, host, paths,
command lines) are dropped; then the timing summary and route status rows.
Exit 0 when every compared report matches after normalisation, 1 otherwise.
"""
import hashlib
import re
import sys
from pathlib import Path

base, cand = Path(sys.argv[1]), Path(sys.argv[2])
REPORTS = ("baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_cells.tsv", "baseline_timing.rpt",
           "baseline_pp_utilization.rpt", "baseline_pp_boundary_timing.rpt", "baseline_scope_timing.tsv",
           "alinx_ax7101_route_status.rpt", "alinx_ax7101_utilization_place.rpt",
           "alinx_ax7101_utilization_synth.rpt", "alinx_ax7101_iob_pack.rpt", "alinx_ax7101_signoff_grade.txt")
META = re.compile(r"^\| (Date|Host|Command|Design|Device|Speed File|Design State|Tool Version)\b|"
                  r"^(Date|Host|Command)\s*:|^# (Date|Host)|$SCRATCH/(exp|res)-?\w*")


def normal(path):
    out = []
    for line in path.read_text(errors="replace").splitlines():
        line = re.sub(r"$SCRATCH/(exp-(base|cand)|res/(base|cand))", "<ROOT>", line)
        if META.search(line):
            continue
        out.append(line)
    return out


bad = 0
for name in REPORTS:
    b, c = base / name, cand / name
    if not b.is_file() or not c.is_file():
        print(f"{name}: MISSING base={b.is_file()} cand={c.is_file()}")
        bad += 1
        continue
    if hashlib.sha256(b.read_bytes()).digest() == hashlib.sha256(c.read_bytes()).digest():
        print(f"{name}: byte-identical")
        continue
    nb, nc = normal(b), normal(c)
    if nb == nc:
        print(f"{name}: identical after dropping run metadata lines")
        continue
    diff = [i for i, (x, y) in enumerate(zip(nb, nc)) if x != y]
    print(f"{name}: DIFFERENT ({len(diff)} differing lines, lengths {len(nb)}/{len(nc)}); first: "
          f"{nb[diff[0]] if diff else ''!r} / {nc[diff[0]] if diff else ''!r}")
    bad += 1
for side, root in (("base", base), ("cand", cand)):
    rpt = (root / "baseline_timing.rpt").read_text().splitlines()
    i = next(n for n, line in enumerate(rpt) if "Design Timing Summary" in line)
    print(side, "timing:", " ".join(rpt[i + 6].split()))
sys.exit(1 if bad else 0)
