#!/usr/bin/env python3
"""Scratch (never committed): gather every run's receipt into the packet, and render the
findings page's receipt tables. Digests and sizes only for anything large."""
import hashlib
import json
import sys
from pathlib import Path

S = Path("$VALIDATION_STORAGE/649-a527")
PACKET = Path("$MANAGEMENT/2026-09-23/649-a527/receipts")
SMALL = 200_000


def digest(path: Path) -> dict:
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def text(path: Path) -> str:
    return path.read_text().strip() if path.is_file() else ""


def minutes(start: str, end: str) -> float | None:
    from datetime import datetime
    if not start or not end:
        return None
    return round((datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60, 1)


def vivado_run(directory: Path, log: str, files: list[str]) -> dict:
    return {"directory": str(directory), "rc": text(directory / f"{log}.rc"),
            "queued": text(directory / f"{log}.queued"), "start": text(directory / f"{log}.start"),
            "end": text(directory / f"{log}.end"),
            "minutes_under_lock": minutes(text(directory / f"{log}.start"), text(directory / f"{log}.end")),
            "log": digest(directory / log) if (directory / log).is_file() else None,
            "tcl": text(directory / "tcl.sha256").split()[0] if (directory / "tcl.sha256").is_file() else "",
            "files": {name: digest(directory / name) for name in files if (directory / name).is_file()}}


def main() -> int:
    PACKET.mkdir(parents=True, exist_ok=True)
    out = {"route_map": vivado_run(S / "route-map-2", "route_map.log",
                                   ["map_hierarchy.rpt", "map_utilization.rpt", "map_cells.tsv"]),
           "route_map_killed_first_attempt": vivado_run(S / "route-map", "route_map.log",
                                                        ["map_hierarchy.rpt", "map_utilization.rpt"]),
           "route_checkpoint": digest(Path("$VALIDATION_STORAGE/234-a516/C/work/ax7101/gateware/alinx_ax7101_route.dcp")),
           "map_outputs": {p.name: digest(p) for p in sorted((S / "map-out").glob("*"))},
           "anchors": {}, "points": {}, "soc": {}}
    for name in ("ship", "streams-2", "streams-4", "streams-8", "ship-8x8"):
        d = S / "sweep" / "vivado" / name
        if d.is_dir():
            out["anchors"][name] = vivado_run(d, "ooc.log", ["point.txt", "synth_hierarchy.rpt", "synth_utilization.rpt",
                                                            "opt_hierarchy.rpt", "opt_utilization.rpt", "opt_cells.tsv",
                                                            "timing_opt.rpt"])
    for receipt in sorted((S / "sweep" / "points").glob("*/receipt.json")):
        out["points"][receipt.parent.name] = json.loads(receipt.read_text())
    for name in ("exports.json", "prices.json"):
        p = S / "sweep" / "soc" / name
        if p.is_file():
            out["soc"][name] = json.loads(p.read_text())
    (PACKET / "run-receipts.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for p in [S / "sweep" / "summary.json", S / "models-out" / "models.json", S / "tables.md",
              S / "map-out" / "map.json", S / "map-out" / "blocks_ranked.tsv", S / "map-out" / "rows_all.tsv",
              S / "map-out" / "partition.md", S / "map-out" / "blocks_ranked.md"]:
        if p.is_file() and p.stat().st_size <= SMALL:
            (PACKET / p.name).write_bytes(p.read_bytes())
    print(f"receipts: {len(out['points'])} points, {len(out['anchors'])} anchors")
    return 0


if __name__ == "__main__" and len(sys.argv) == 1:
    sys.exit(main())


def render_markdown() -> str:
    """The findings page's receipt tables, from run-receipts.json and the point receipts."""
    r = json.loads((PACKET / "run-receipts.json").read_text())
    lines = ["| Run | rc | Minutes under the lock | Log | Log SHA-256, first 16 | Log bytes |",
             "|---|---:|---:|---|---|---:|"]
    killed = r["route_map_killed_first_attempt"]
    lines.append(f"| Route reopen, first attempt, stopped by this lane | 143 | {killed['minutes_under_lock'] or '-'} | "
                 f"`route_map.log` | `{killed['log']['sha256'][:16]}` | {killed['log']['bytes']:,} |")
    rm = r["route_map"]
    lines.append(f"| Route reopen | {rm['rc']} | {rm['minutes_under_lock']} | `route_map.log` | "
                 f"`{rm['log']['sha256'][:16]}` | {rm['log']['bytes']:,} |")
    for name, a in r["anchors"].items():
        label = {"ship": "Anchor 1x1, shipping shape", "streams-2": "Anchor 2x2", "streams-4": "Anchor 4x4",
                 "streams-8": "Anchor 8x8 TDM8, refused in synthesis", "ship-8x8": "Anchor 8x8, tracked configuration"}[name]
        if not a.get("log"):
            continue
        lines.append(f"| {label} | {a['rc']} | {a['minutes_under_lock']} | `ooc.log` | `{a['log']['sha256'][:16]}` | "
                     f"{a['log']['bytes']:,} |")
    vivado = "\n".join(lines) + "\n"
    rows = ["| Point | Top | rc | Seconds | `stat.json` SHA-256, first 16 | Guard |", "|---|---|---:|---:|---|---|"]
    for name, p in r["points"].items():
        rc = max(p["rc"].values())
        stat = p["outputs"].get("stat.json", {}).get("sha256", "")[:16]
        guard_file = S / "sweep" / "points" / name / "guards.json"
        guard = json.loads(guard_file.read_text()) if guard_file.is_file() else None
        guard_text = "-" if guard is None else ("refused" if guard["refusals"] else "clean")
        rows.append(f"| {name} | `{p['point']['top']}` | {rc} | {p['seconds']['total']} | `{stat}` | {guard_text} |")
    return vivado + "\n" + "\n".join(rows) + "\n"


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--markdown":
    (S / "receipts.md").write_text(render_markdown())
    print(S / "receipts.md")
