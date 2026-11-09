"""collect_area.py <scratch> <out>: the area receipts of the head's six Vivado runs, host paths masked.

For each run directory: its gate-relevant reports (route status, utilization, hierarchy, IOB packing, the signoff
corner summaries' design tables, the image manifest, the bound parameters, rc and seconds), each copied if at most
200 KB, else recorded by SHA-256 and size in <out>/LARGE-FILES.sha256. Writes <out>/runs.md: per run its rc and
seconds, the Vivado memory peak its log reports, the count of `Synth 8-4445` and `Synth 8-6901` diagnostics, and the
log's SHA-256 and size; and <out>/images.md: every baseline_images.json entry rehashed now against its recorded
SHA-256. Exits 1 if a run's rc is not 0, a log carries `Synth 8-4445`, or an image no longer matches."""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mask import mask  # noqa: E402

S, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
RUNS = (("eppo", S / "w/ax7101/gateware", "route-1x1, ExtraPostPlacementOpt, with synthesis"),
        ("aslh", S / "w/ax7101-AltSpreadLogic_high", "route-1x1, AltSpreadLogic_high"),
        ("eto", S / "w/ax7101-ExtraTimingOpt", "route-1x1, ExtraTimingOpt"),
        ("ooc-1x1", S / "w/ax7101-ooc", "ooc-1x1"),
        ("rtl-8x8", S / "w8/ax8x8-rtl", "rtl-8x8 (RTL elaboration for the 8x8 parameters)"),
        ("ooc-8x8", S / "w8/ax8x8-ooc", "ooc-8x8"))
PATTERNS = ("*_route_status.rpt", "*_utilization_place.rpt", "*_iob_pack.rpt", "baseline_utilization.rpt",
            "baseline_hierarchy.rpt", "baseline_images.json", "baseline_parameters.json", "baseline_chparam.txt",
            "baseline_scope_timing.tsv", "baseline_pp_utilization.rpt", "*_signoff_grade.txt", "baseline.log.rc")
large = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def put(dest: Path, name: str, text: str) -> None:
    data = mask(text).encode()
    if len(data) > 200 * 1024:
        large.append(f"{sha(data)}  {len(data)}  {dest.name}/{name} (masked copy not kept)")
        return
    dest.mkdir(parents=True, exist_ok=True)
    (dest / name).write_bytes(data)


def design_table(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "WNS(ns)" in line and "TNS(ns)" in line:
            return "\n".join(lines[i:i + 3]) + "\n"
    return "no design timing summary found\n"


bad = 0
rows = ["# Vivado runs at the head (recipe form, under the slot wrapper)", "",
        "| Run | rc and seconds | Vivado peak memory (MB) | `Synth 8-4445` | `Synth 8-6901` | Log SHA-256 | Log bytes |",
        "|---|---|---:|---:|---:|---|---:|"]
img_rows = ["# Image manifest entries rehashed after measurement", "",
            "| Run | Entry | Recorded SHA-256 | Now | Match |", "|---|---|---|---|---|"]
for name, d, label in RUNS:
    dest = OUT / name
    for pattern in PATTERNS:
        for found in sorted(d.glob(pattern)):
            put(dest, found.name.replace("alinx_ax7101_", ""), found.read_text(errors="replace"))
    summary = [f"== {p.name}\n{design_table(p.read_text(errors='replace'))}" for p in sorted(d.glob("*_timing*.rpt"))]
    if summary:
        put(dest, "timing-design-tables.txt", "\n".join(summary))
    log = d / "baseline.log"
    data = log.read_bytes() if log.exists() else b""
    text = data.decode(errors="replace")
    peaks = [float(x) for x in re.findall(r"peak = ([0-9.]+)", text)]
    n4445 = len(re.findall(r"\[Synth 8-4445\]", text))
    n6901 = len(re.findall(r"\[Synth 8-6901\]", text))
    rcfile = d / "baseline.log.rc"
    rc = rcfile.read_text().strip() if rcfile.exists() else "missing"
    bad += (not rc.startswith("0 ")) + (n4445 > 0)
    rows.append(f"| {label} | {rc} | {max(peaks):,.0f} | {n4445} | {n6901} | `{sha(data)}` | {len(data):,} |"
                if peaks else f"| {label} | {rc} | ? | {n4445} | {n6901} | `{sha(data)}` | {len(data):,} |")
    if text:
        put(dest, "baseline.log.tail", "".join(text.splitlines(True)[-40:]))
    manifest = d / "baseline_images.json"
    if manifest.exists():
        for entry in json.loads(manifest.read_text()):
            p = Path(entry["path"])
            now = sha(p.read_bytes()) if p.exists() else "missing"
            ok = now == entry["sha256"]
            bad += not ok
            img_rows.append(f"| {name} | `{mask(str(p))}` | `{entry['sha256'][:16]}` | `{now[:16]}` | "
                            f"{'yes' if ok else 'NO'} |")
(OUT / "runs.md").write_text(mask("\n".join(rows) + "\n"))
(OUT / "images.md").write_text(mask("\n".join(img_rows) + "\n"))
if large:
    (OUT / "LARGE-FILES.sha256").write_text("\n".join(large) + "\n")
print((OUT / "runs.md").read_text())
print(f"images: {sum(1 for r in img_rows[4:] if r.endswith('yes |'))} of {len(img_rows) - 4} match")
sys.exit(1 if bad else 0)
