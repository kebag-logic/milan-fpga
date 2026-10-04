#!/usr/bin/env python3
"""Scratch (never committed): assemble the round-2 packet's re-runnable inputs for issue #649.

Lays the small inputs out so `resmap_map.py map`, `resmap_models.py` and `resmap_tables.py --page`
run from them, compresses the two JSON files above the packet's 200 KB limit with xz, and writes
MANIFEST.json: sha256 and bytes of every file placed, and of every input left out with the reason.
"""
import hashlib
import json
import lzma
import shutil
import sys
from pathlib import Path

PACKET = Path("$MANAGEMENT/2026-09-23/649-a527/r2")
SCRATCH = Path("$VALIDATION_STORAGE/649-a527")
LIMIT = 200 * 1024


def digest(path: Path) -> dict:
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def place(source: Path, target: Path, manifest: dict, compress: bool = False) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if compress:
        target = target.with_name(target.name + ".xz")
        target.write_bytes(lzma.compress(source.read_bytes(), preset=9 | lzma.PRESET_EXTREME))
    else:
        shutil.copyfile(source, target)
    if target.stat().st_size > LIMIT:
        raise SystemExit(f"{target} is {target.stat().st_size} bytes, over the packet limit")
    manifest["placed"][str(target.relative_to(PACKET))] = {**digest(target), "from": str(source),
                                                          "source": digest(source)}


def keep_out(source: Path, reason: str, manifest: dict) -> None:
    manifest["kept_out"][str(source)] = {**digest(source), "reason": reason}


def main() -> int:
    map_dir = Path(sys.argv[1])
    inputs = PACKET / "inputs"
    if inputs.exists():
        shutil.rmtree(inputs)
    manifest = {"placed": {}, "kept_out": {}}
    for name in ("map_hierarchy.rpt", "map_utilization.rpt", "route_map.log", "tcl.sha256"):
        place(map_dir / name, inputs / "map" / name, manifest)
    keep_out(map_dir / "map_cells.tsv", "the census, 12.5 MB (540 KB with xz): over the packet's 200 KB limit; "
             "`map` and `tables` read it", manifest)
    work = SCRATCH / "sweep"
    place(work / "summary.json", inputs / "work" / "summary.json", manifest, compress=True)
    for anchor in ("ship", "streams-2", "streams-4", "ship-8x8"):
        for stage in ("synth", "opt"):
            place(work / "vivado" / anchor / f"{stage}_hierarchy.rpt",
                  inputs / "work" / "vivado" / anchor / f"{stage}_hierarchy.rpt", manifest)
    for name in ("exports.json", "prices.json"):
        place(work / "soc" / name, inputs / "work" / "soc" / name, manifest)
    for point in sorted((work / "points").iterdir()):
        place(point / "guards.json", inputs / "work" / "guards" / f"{point.name}.json", manifest)
    place(SCRATCH / "r2" / "models-out" / "models.json", inputs / "models" / "models.json", manifest, compress=True)
    soc = SCRATCH / "r2" / "soc"
    place(soc / "soc_prices.json", inputs / "soc_prices.json", manifest)
    for name in ("prepare.json", "exports.json", "pricing-copy.diff"):
        place(soc / name, inputs / "soc-variants" / name, manifest)
    for directory in sorted((soc / "vivado").iterdir()):
        for name in ("synth_hierarchy.rpt", "opt_hierarchy.rpt", "meta.json", "soc_ooc.tcl"):
            if (directory / name).is_file():
                place(directory / name, inputs / "soc-variants" / directory.name / name, manifest)
        if (directory / "ooc.log").is_file():
            keep_out(directory / "ooc.log", "Vivado log; digest only", manifest)
    for directory in sorted((soc / "soc").iterdir()):
        if (directory / "export.log").is_file():
            keep_out(directory / "export.log", "export log; digest only", manifest)
    (PACKET / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print(f"placed {len(manifest['placed'])}, kept out {len(manifest['kept_out'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
