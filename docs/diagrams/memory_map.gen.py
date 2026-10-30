#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the SoC memory-map block diagram as an editable .drawio and a
rendered .svg (#797). Style follows flash_layout.gen.py.

NOTHING HERE IS TRANSCRIBED. The regions, the windows inside them and the LiteX
CSR banks come from `scripts/register_map_soc.json`, which
`scripts/gen_register_reference.py --soc-from` writes from a builder export's
`csr.csv` and `aem_desc.json`. The Milan CSR modules are the offset ranges the
register reference uses. Region heights are NOT to scale: the map spans 4 GiB
and the smallest window is 4 KiB, so each block is one row, ordered by address.

Usage:
    python3 docs/diagrams/memory_map.gen.py           # write .svg and .drawio
    python3 docs/diagrams/memory_map.gen.py --check   # fail when either is stale
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from register_page import soc_windows  # noqa: E402

SOC = REPO / "scripts" / "register_map_soc.json"
DESCRIPTIONS = REPO / "scripts" / "register_descriptions.json"
BASE = REPO / "docs" / "diagrams" / "memory_map"

ROW_H, GAP = 30, 6
LEFT_X, LEFT_W = 40, 640
RIGHT_X, RIGHT_W = 720, 640
TOP = 120
REGION = ("#E3F2FD", "#1565C0")
WINDOW = ("#E8F5E9", "#2E7D32")
MILAN = ("#FFF3E0", "#EF6C00")
BANK = ("#F3E5F5", "#6A1B9A")


def esc(text: object) -> str:
    """XML-safe text, quotes included, because every use is an attribute value."""
    return html.escape(str(text), quote=True)


def rows(soc: dict, desc: dict) -> tuple[list[tuple], list[tuple]]:
    """(left, right): the address-ordered regions and windows, and the Milan
    modules plus the LiteX banks, each as (label, start, end, palette, indent)."""
    left = []
    for name, start, size, _ in soc_windows(soc, desc):
        window = " " in name.strip("`")
        label = name.replace("`", "")
        left.append((label, start, start + size - 1, WINDOW if window else
                     (MILAN if label == "milan_csr" else REGION), 24 if window else 0))
    base = next(r["origin"] for r in soc["memory_regions"] if r["name"] == "milan_csr")
    right = [(m["heading"].split("  `", 1)[0].split("  -  ", 1)[-1], base + int(m["start"], 16),
              base + int(m["end"], 16), MILAN, 0) for m in desc["modules"]]
    banks = sorted(soc["csr_banks"], key=lambda b: b["origin"])
    step = min(b["origin"] - a["origin"] for a, b in zip(banks, banks[1:]))
    right += [(f"LiteX CSR bank {b['name']}", b["origin"], b["origin"] + step - 1, BANK, 0) for b in banks]
    return left, right


def block_svg(x: int, y: int, w: int, row: tuple) -> str:
    """One block: name on the left, the address range on the right."""
    label, start, end, (fill, stroke), indent = row
    return (f'<rect x="{x + indent}" y="{y}" width="{w - indent}" height="{ROW_H}" rx="4" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
            f'<text x="{x + indent + 10}" y="{y + 20}" font-size="13" fill="#212121">{esc(label)}</text>'
            f'<text x="{x + w - 10}" y="{y + 20}" font-size="12" font-family="monospace" fill="#37474F" '
            f'text-anchor="end">0x{start:08X} - 0x{end:08X}</text>')


def svg(left: list[tuple], right: list[tuple], soc: dict) -> str:
    """The rendered diagram."""
    height = TOP + max(len(left), len(right)) * (ROW_H + GAP) + 40
    width = RIGHT_X + RIGHT_W + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
           f'<text x="40" y="44" font-size="26" font-weight="bold" fill="#263238">'
           f'SoC memory map - {esc(soc["shape"])}</text>',
           '<text x="40" y="70" font-size="14" fill="#546E7A">GENERATED from scripts/register_map_soc.json '
           '(the builder export) by docs/diagrams/memory_map.gen.py. Not to scale.</text>',
           f'<text x="{LEFT_X}" y="{TOP - 14}" font-size="15" font-weight="bold" fill="#263238">'
           'Regions and windows</text>',
           f'<text x="{RIGHT_X}" y="{TOP - 14}" font-size="15" font-weight="bold" fill="#263238">'
           'Milan CSR modules and LiteX CSR banks</text>']
    for k, row in enumerate(left):
        out.append(block_svg(LEFT_X, TOP + k * (ROW_H + GAP), LEFT_W, row))
    for k, row in enumerate(right):
        out.append(block_svg(RIGHT_X, TOP + k * (ROW_H + GAP), RIGHT_W, row))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def drawio(left: list[tuple], right: list[tuple], soc: dict) -> str:
    """The same blocks as an editable .drawio."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for side, (x, w, blocks) in enumerate(((LEFT_X, LEFT_W, left), (RIGHT_X, RIGHT_W, right))):
        for k, (label, start, end, (fill, stroke), indent) in enumerate(blocks):
            style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                     "fontSize=12;align=left;spacingLeft=8;")
            text = f"{label}   0x{start:08X} - 0x{end:08X}"
            cells.append(f'<mxCell id="b{side}_{k}" value="{esc(text)}" style="{style}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x + indent}" y="{TOP + k * (ROW_H + GAP)}" width="{w - indent}" '
                         f'height="{ROW_H}" as="geometry"/></mxCell>')
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="memory-map {esc(soc["shape"])}">'
            '<mxGraphModel dx="1400" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
            'arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="0"><root>'
            f"{body}</root></mxGraphModel></diagram></mxfile>\n")


def main(argv: list[str]) -> int:
    """Write both renders, or with --check fail when either differs."""
    soc = json.loads(SOC.read_text(encoding="utf-8"))
    desc = json.loads(DESCRIPTIONS.read_text(encoding="utf-8"))
    left, right = rows(soc, desc)
    want = {BASE.with_suffix(".svg"): svg(left, right, soc), BASE.with_suffix(".drawio"): drawio(left, right, soc)}
    if argv[1:] == ["--check"]:
        stale = [p for p, text in want.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
        for path in stale:
            print(f"STALE {path.relative_to(REPO)}")
        print(f"memory map diagram: {'STALE' if stale else 'fresh'}")
        return 1 if stale else 0
    if argv[1:]:
        print(__doc__)
        return 2
    for path, text in want.items():
        path.write_text(text, encoding="utf-8")
    print(f"wrote {BASE.relative_to(REPO)}.svg and .drawio ({len(left)} regions and windows, {len(right)} blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
