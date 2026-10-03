#!/usr/bin/env python3
"""Scratch (never committed): run receipts for every measurement, as JSON and a Markdown table."""
import datetime
import hashlib
import json
import sys
from pathlib import Path

S = Path("$VALIDATION_STORAGE/234-a516")
RUNS = [
    ("A", "Integrated route, 1x1", "A/work/ax7101/gateware", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_integrated.tcl", "baseline_images.json", "baseline_scope_timing.tsv",
      "alinx_ax7101_route_status.rpt", "alinx_ax7101_signoff_all_timing.rpt", "alinx_ax7101_route.dcp"]),
    ("B", "Integrated route, 1x1", "B/work/ax7101/gateware", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_integrated.tcl", "baseline_images.json", "baseline_scope_timing.tsv",
      "alinx_ax7101_route_status.rpt", "alinx_ax7101_signoff_all_timing.rpt", "alinx_ax7101_route.dcp"]),
    ("A", "Standalone synthesis, 1x1", "A/work/ax7101-ooc", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_ooc.tcl", "baseline_parameters.json", "clock.xdc", "baseline_synth.dcp"]),
    ("B", "Standalone synthesis, 1x1", "B/work/ax7101-ooc", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_ooc.tcl", "baseline_parameters.json", "clock.xdc", "baseline_synth.dcp"]),
    ("A", "RTL elaboration, 8x8 parameters", "A/work/ax8x8-elab", "elaborate.log", ["elaborate.tcl"]),
    ("B", "RTL elaboration, 8x8 parameters", "B/work/ax8x8-elab", "elaborate.log", ["elaborate.tcl"]),
    ("A", "RTL elaboration, 1x1 control", "A/work/ax7101-elab", "elaborate.log", ["elaborate.tcl"]),
    ("A", "Standalone synthesis, 8x8", "A/work/ax8x8-ooc", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_ooc.tcl", "baseline_parameters.json", "clock.xdc", "baseline_synth.dcp"]),
    ("B", "Standalone synthesis, 8x8", "B/work/ax8x8-ooc", "baseline.log",
     ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_timing.rpt", "baseline_cells.tsv",
      "baseline_ooc.tcl", "baseline_parameters.json", "clock.xdc", "baseline_synth.dcp"]),
    ("A", "Storage cone probe, 1x1", "A/work/cone-probe", "probe.log", ["cones.tsv", "run.tcl"]),
    ("A", "Yosys flattened, 1x1", "A/work/ax7101-yosys", "ooc.sh.log", ["KL_pp_shadow.ooc.log", "KL_pp_shadow.ooc.json"]),
    ("B", "Yosys flattened, 1x1", "B/work/ax7101-yosys", "ooc.sh.log", ["KL_pp_shadow.ooc.log", "KL_pp_shadow.ooc.json"]),
    ("A", "Yosys flattened, 8x8", "A/work/ax8x8-yosys", "ooc.sh.log", ["KL_pp_shadow.ooc.log", "KL_pp_shadow.ooc.json"]),
    ("B", "Yosys flattened, 8x8", "B/work/ax8x8-yosys", "ooc.sh.log", ["KL_pp_shadow.ooc.log", "KL_pp_shadow.ooc.json"]),
    ("A", "Yosys hierarchical, 1x1", "A/work/ax7101-yosys", "hierarchical.log", ["hierarchical.json", "hierarchical.ys"]),
    ("A", "Yosys hierarchical, 8x8", "A/work/ax8x8-yosys", "hierarchical.log", ["hierarchical.json", "hierarchical.ys"]),
]
EXTRA = [("A", "Standalone synthesis, 1x1 at 10 ns (#231 clock control)", "A/work/ax7101-ooc10", "baseline.log",
          ["baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_cells.tsv", "clock.xdc"])]


def digest(path: Path) -> dict:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return {"sha256": h.hexdigest(), "bytes": path.stat().st_size}


def minutes(start: str, end: str) -> float:
    a = datetime.datetime.fromisoformat(start.strip())
    b = datetime.datetime.fromisoformat(end.strip())
    return round((b - a).total_seconds() / 60, 1)


rows = []
for combo, label, folder, log, files in RUNS + EXTRA:
    d = S / folder
    if not (d / log).exists():
        continue
    rec = {"combination": combo, "run": label, "directory": str(d), "log": log}
    rc_file = d / f"{log}.rc"
    rec["rc"] = int(rc_file.read_text().strip()) if rc_file.exists() else None
    if (d / f"{log}.start").exists() and (d / f"{log}.end").exists():
        rec["start"] = (d / f"{log}.start").read_text().strip()
        rec["end"] = (d / f"{log}.end").read_text().strip()
        rec["minutes"] = minutes(rec["start"], rec["end"])
    rec["log_digest"] = digest(d / log)
    rec["files"] = {f: digest(d / f) for f in files if (d / f).exists()}
    rows.append(rec)
out = Path(sys.argv[1])
out.write_text(json.dumps(rows, indent=1) + "\n")
print("| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |")
print("|---|---|---:|---:|---|---|---:|")
for r in rows:
    print(f"| {r['combination']} | {r['run']} | {r['rc']} | {r.get('minutes', '-')} | `{r['log']}` | "
          f"`{r['log_digest']['sha256'][:16]}` | {r['log_digest']['bytes']:,} |")
