#!/usr/bin/env python3
"""Scratch (M8a-1 round 5): tabulate fit_r5.sh output for one tree, independently of the planner.

usage: fit_table.py <fit-dir>
"""
import json
import re
import sys
from pathlib import Path

GRANULE, BUDGET_GRANULES, REGION = 2048, 112, 229376
POINTS = [("endstation_ax7101_1x1_tdm8", 1), ("endstation_ax7101_1x1_tdm8", 2),
          ("endstation_ax7101_8x8", 1), ("endstation_ax7101_8x8", 2)]


def symbol(path: Path, name: str) -> int:
    """Size of one symbol from the fixture's symbols.txt (nm -S style)."""
    for line in path.read_text().splitlines():
        f = line.split()
        if f and f[-1] == name and len(f) >= 4:
            return int(f[1], 16)
    return -1


fit = Path(sys.argv[1])
rows = []
for shape, ifs in POINTS:
    split = fit / f"split-{shape}-if{ifs}"
    flat = fit / f"flat-{shape}-if{ifs}"
    s = json.loads((split / "size.json").read_text())
    fl = json.loads((flat / "size.json").read_text())
    plan = json.loads((fit / f"plan-{shape}-if{ifs}.json").read_text())
    sec = s["sections"]
    rom, ram = plan["rom"]["bytes"], plan["sram"]["bytes"]
    assert (rom, ram) == (s["split"]["rom"]["bytes"], s["split"]["sram"]["bytes"])
    granules = -(-rom // GRANULE) + -(-ram // GRANULE)
    assert granules / 2 == plan["tiles"], (granules, plan["tiles"])
    # Banks: the granule count's binary digits, largest first.
    for region, need in (("rom", rom), ("sram", ram)):
        g, banks, bit = -(-need // GRANULE), [], 1 << 20
        while bit:
            if g & bit:
                banks.append(bit * GRANULE)
            bit >>= 1
        assert banks == plan[region]["banks"], (region, banks, plan[region]["banks"])
    alloc = sum(plan["rom"]["banks"]) + sum(plan["sram"]["banks"])
    span = fl["ram_sections"]
    m = re.search(r'"ram_span": (\d+)', (fit / f"flat-{shape}-if{ifs}.log").read_text())
    log_span = int(m.group(1)) if m else None
    row = {
        "point": f"{shape}-if{ifs}", "text": sec[".text"], "rodata": sec[".rodata"], "data": sec[".data"],
        "bss": sec[".bss"], "stack": sec[".stack"], "rom": rom, "sram": ram, "sum": rom + ram,
        "flat_span": log_span if log_span is not None else span, "flat_ram_sections": span,
        "floor": -(-(log_span or span) // 4096), "rom_banks": plan["rom"]["banks"], "sram_banks": plan["sram"]["banks"],
        "alloc": alloc, "used_pct": round(100 * (rom + ram) / alloc, 1),
        "rom_fill_pct": round(100 * rom / sum(plan["rom"]["banks"]), 1),
        "sram_fill_pct": round(100 * ram / sum(plan["sram"]["banks"]), 1),
        "planned": plan["tiles"], "headroom_tiles": 56 - plan["tiles"],
        "headroom_granule_bytes": (BUDGET_GRANULES - granules) * GRANULE,
        "headroom_bytes_with_slack": (BUDGET_GRANULES - granules) * GRANULE + alloc - rom - ram,
        "rom_le_224k": rom <= REGION, "sram_le_224k": ram <= REGION,
        "flat_le_224k": (log_span or span) <= REGION,
        "nvm_stage": symbol(split / "symbols.txt", "nvm_stage"),
        "aecp_entity_image": symbol(split / "symbols.txt", "aecp_entity_image"),
        "image_arena": s["static_storage"].get("image_arena"),
        "elf_sha256": next(a["sha256"] for a in s["artifacts"] if a["name"] == "ctrl_app.elf"),
    }
    rows.append(row)
    print(json.dumps(row))
for r in rows:
    print(f"| {r['point']} | {r['text']:,} | {r['rodata']:,} | {r['data']:,} | {r['bss']:,} | {r['stack']:,} | "
          f"{r['rom']:,} | {r['sram']:,} | {r['sum']:,} | {r['flat_span']:,} |")
for r in rows:
    print(f"{r['point']}: rom {r['rom_banks']} sram {r['sram_banks']} planned {r['planned']} alloc {r['alloc']:,} "
          f"used {r['used_pct']}% fill rom {r['rom_fill_pct']}% sram {r['sram_fill_pct']}% floor {r['floor']} "
          f"headroom {r['headroom_tiles']} tiles, {r['headroom_granule_bytes']} B granules, "
          f"{r['headroom_bytes_with_slack']} B with slack; 224K rom {r['rom_le_224k']} sram {r['sram_le_224k']} "
          f"flat {r['flat_le_224k']}; nvm_stage {r['nvm_stage']} aecp_entity_image {r['aecp_entity_image']} "
          f"arena {r['image_arena']}")
