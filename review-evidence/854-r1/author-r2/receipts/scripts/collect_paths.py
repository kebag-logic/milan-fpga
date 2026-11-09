"""collect_paths.py <paths-dir> <routed-dir> <out-dir>: publish one routed checkpoint's worst-path receipts.

<paths-dir> is paths.sh's output (report_timing of the routed checkpoint, one worst setup and one worst hold path per
signoff corner); <routed-dir> holds the checkpoint and the route's own signoff timing summaries
(*_signoff_<corner>_<T>C_timing.rpt). Copies each excerpt with host paths masked, and writes summary.md: per corner
the excerpt's slack, its start and end points, logic levels and data path delay, beside the WNS and WHS of that
corner's Design Timing Summary, plus the sha256 and size of the checkpoint and of each summary (not copied).
Exits 1 unless every excerpt's slack equals its corner's WNS (setup) or WHS (hold): a receipt named for the worst
path must be the worst path."""
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mask import mask  # noqa: E402

paths, routed, out = (Path(a) for a in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
CORNERS = ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def summary_wns_whs(rpt: Path) -> tuple[float, float]:
    lines = rpt.read_text(errors="replace").splitlines()
    i = next(n for n, l in enumerate(lines) if "Design Timing Summary" in l)
    hdr = next(n for n in range(i, i + 12) if lines[n].strip().startswith("WNS(ns)"))
    vals = lines[hdr + 2].split()
    return float(vals[0]), float(vals[4])


def path_fields(rpt: Path) -> dict[str, str]:
    t = rpt.read_text(errors="replace")
    get = lambda pat: (re.search(pat, t, re.M).group(1).strip() if re.search(pat, t, re.M) else "?")
    return {
        "slack": get(r"^Slack \(\w+\)\s*:\s*(-?[0-9.]+)ns"),
        "source": get(r"^\s*Source:\s*(\S+)"),
        "destination": get(r"^\s*Destination:\s*(\S+)"),
        "group": get(r"^\s*Path Group:\s*(\S+)"),
        "requirement": get(r"^\s*Requirement:\s*(.*?)\s*$"),
        "delay": get(r"^\s*Data Path Delay:\s*(.*?)\s*$"),
        "levels": get(r"^\s*Logic Levels:\s*(.*?)\s*$"),
    }


dcp = routed / "alinx_ax7101_route.dcp"
rows, bad = [], 0
for c in CORNERS:
    summ = next(routed.glob(f"*_signoff_{c}_timing.rpt"))
    wns, whs = summary_wns_whs(summ)
    for kind, want in (("setup", wns), ("hold", whs)):
        src = paths / f"{c}_worst_{kind}.rpt"
        (out / src.name).write_text(mask(src.read_text(errors="replace")))
        f = path_fields(src)
        ok = abs(float(f["slack"]) - want) < 0.0005
        bad += not ok
        rows.append((c, kind, f, want, ok, summ))
lines = ["# Worst paths, report_timing of the routed checkpoint", "",
         f"Checkpoint: `{dcp.name}`, sha256 `{sha(dcp)}`, {dcp.stat().st_size} bytes (not copied).", "",
         "| Corner | Kind | Slack ns | Summary ns | Equal | Logic levels | Data path delay | Source | Destination | Group |",
         "|---|---|---:|---:|---|---|---|---|---|---|"]
for c, kind, f, want, ok, _ in rows:
    lines.append(f"| {c} | {kind} | {f['slack']} | {want:.3f} | {'yes' if ok else 'NO'} | {f['levels']} | {f['delay']} | "
                 f"`{f['source']}` | `{f['destination']}` | {f['group']} |")
lines += ["", "Signoff summaries (the route's own, not copied):", ""]
for c in CORNERS:
    summ = next(routed.glob(f"*_signoff_{c}_timing.rpt"))
    lines.append(f"- `{summ.name}`: sha256 `{sha(summ)}`, {summ.stat().st_size} bytes")
lines += ["", f"Result: {'PASS' if not bad else 'FAIL'}: every excerpt's slack {'equals' if not bad else 'does NOT equal'} "
          "its corner's WNS (setup) or WHS (hold)."]
(out / "summary.md").write_text(mask("\n".join(lines) + "\n"))
for name in ("slacks.tsv", "dcp.sha256"):
    if (paths / name).exists():
        (out / name).write_text(mask((paths / name).read_text()))
print((out / "summary.md").read_text())
sys.exit(1 if bad else 0)
