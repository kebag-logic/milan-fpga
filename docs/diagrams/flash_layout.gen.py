#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the QSPI flash map (to scale) as an editable .drawio and a rendered
.svg.  Style follows DOC_MAP.gen.py / SYSTEM_DOMAIN_MAP.gen.py.

**NOTHING HERE IS TRANSCRIBED.**  The slot list, offsets, sizes, DRAM load
addresses, manifests, device size and erase-block size all come from the ONE
source of truth, ``FLASHBOOT_LAYOUT`` + ``FLASHBOOT_RESERVED`` in
``sw/litex/milan_soc.py``, parsed here (never transcribed) by ``load_map()``
below.  A flash map change therefore moves the picture and the BIOS together,
or it does not move at all.  The reader lived in the retired partition emitter
until #259 removed it; it is 25 lines and now lives where its one consumer is.

The bands are drawn **to scale** on purpose: "this slot shrank to make room for
the writable ones" is a statement about proportions, and a table of hex offsets
does not carry it.

Usage:
    python3 docs/diagrams/flash_layout.gen.py docs/diagrams/flash_layout
    rsvg-convert -w 1800 docs/diagrams/flash_layout.svg \
        -o docs/diagrams/flash_layout.png
"""
import ast
import html
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOC = REPO / "sw" / "litex" / "milan_soc.py"

#: Slots no running image may write.  A stray write onto the configuration
#: slot bricks the board's self-config; `journal` and `user` are deliberately
#: writable - they are the whole point of reserving them.
READ_ONLY = {"bitstream", "kernel", "opensbi", "dtb", "rootfs"}


def esc(s):
    return html.escape(str(s), quote=True)


def load_map():
    """[(name, offset, size, kind)] ordered by offset, plus (flash_size, eb)."""
    layout, reserved = _literal("FLASHBOOT_LAYOUT"), _literal("FLASHBOOT_RESERVED")
    rows = [(n, e["offset"], e["size"], "image") for n, e in layout.items()]
    rows += [(n, e["offset"], e["size"], "reserved") for n, e in reserved.items()]
    return (sorted(rows, key=lambda r: r[1]),
            _literal("FLASH_SIZE"), _literal("FLASH_ERASE_BLOCK"))


def check_map(rows, flash_size, erase):
    """Overlap / alignment / past-the-device, printed onto the drawing."""
    problems, prev_end, prev_name = [], 0, None
    for name, off, size, _k in rows:
        if size <= 0:
            problems.append(f"{name}: non-positive size {size}")
        if off % erase:
            problems.append(f"{name}: offset 0x{off:X} not erase-block aligned")
        if size % erase:
            problems.append(f"{name}: size 0x{size:X} not an erase-block multiple")
        if off < prev_end:
            problems.append(f"{name} @0x{off:X} overlaps {prev_name} "
                            f"(ends 0x{prev_end:X})")
        if off + size > flash_size:
            problems.append(f"{name}: ends 0x{off + size:X} past the device "
                            f"(0x{flash_size:X})")
        prev_end, prev_name = off + size, name
    return problems

_tree = ast.parse(SOC.read_text(encoding="utf-8"))


def _literal(name):
    for node in _tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise SystemExit(f"flash_layout.gen.py: {name} not found in {SOC} — "
                     f"fix this generator, do not hand-draw the map.")


LAYOUT = _literal("FLASHBOOT_LAYOUT")
MANIFESTS = _literal("FLASHBOOT_MANIFESTS")
ROWS, FLASH_SIZE, ERASE = load_map()
PROBLEMS = check_map(ROWS, FLASH_SIZE, ERASE)

# palette (fill, stroke)
BLUE = ("#E3F2FD", "#1565C0")     # gateware
GREEN = ("#E8F5E9", "#2E7D32")    # kernel / rootfs payloads
ORANGE = ("#FFF3E0", "#EF6C00")   # firmware / dtb
PURPLE = ("#F3E5F5", "#6A1B9A")   # writable slots
GREY = ("#ECEFF1", "#90A4AE")     # free space
RED = ("#FFEBEE", "#C62828")


def colour(name, kind):
    if kind == "reserved":
        return PURPLE
    if name == "bitstream":
        return BLUE
    if name in ("opensbi", "dtb"):
        return ORANGE
    return GREEN


def human(n):
    if n >= 1 << 20 and n % (1 << 20) == 0:
        return f"{n >> 20} MiB"
    if n >= 1 << 20:
        return f"{n / (1 << 20):.2f} MiB"
    return f"{n >> 10} KiB"


# --- build the band list including the gaps, so free space is visible -------
BANDS = []          # (name, offset, size, kind)
cursor = 0
for name, off, size, kind in ROWS:
    if off > cursor:
        BANDS.append(("(free)", cursor, off - cursor, "free"))
    BANDS.append((name, off, size, kind))
    cursor = off + size
if cursor < FLASH_SIZE:
    BANDS.append(("(free)", cursor, FLASH_SIZE - cursor, "free"))

# geometry: one vertical bar, to scale
BAR_X, BAR_Y, BAR_W, BAR_H = 120, 210, 300, 900
TXT_X = BAR_X + BAR_W + 40
W, H = 1620, BAR_Y + BAR_H + 230


def band_y(off):
    return BAR_Y + BAR_H * off / FLASH_SIZE


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>']
    o.append('<text x="40" y="52" font-size="30" font-weight="bold" fill="#263238">'
             f'QSPI flash map - {human(FLASH_SIZE)} device, drawn to scale</text>')
    o.append('<text x="40" y="82" font-size="15" fill="#546E7A">GENERATED from '
             'FLASHBOOT_LAYOUT + FLASHBOOT_RESERVED in sw/litex/milan_soc.py, read '
             'through sw/dts/gen_mtd_partitions.py - the same reader the kernel\'s '
             'fixed-partitions node comes from.</text>')
    o.append(f'<text x="40" y="106" font-size="15" fill="#546E7A">'
             f'Erase block {human(ERASE)}: every slot starts and ends on one, so '
             f'"write the journal" can never erase a neighbour.</text>')
    o.append(f'<text x="40" y="130" font-size="15" font-weight="bold" '
             f'fill="{"#2E7D32" if not PROBLEMS else "#C62828"}">'
             f'{"map consistent: no overlap, no misalignment, nothing past the device"
                if not PROBLEMS else "MAP PROBLEMS: " + "; ".join(PROBLEMS)}</text>')

    o.append(f'<text x="{BAR_X}" y="{BAR_Y-22}" font-size="17" font-weight="bold" '
             f'fill="#78909C">offset 0 at the top</text>')

    # label anchors: push apart so thin bands (dtb, journal) do not collide
    LBL_H = 52
    anchors = []
    for name, off, size, kind in BANDS:
        anchors.append(band_y(off) + max(band_y(off + size) - band_y(off), 3) / 2)
    for i in range(1, len(anchors)):
        if anchors[i] - anchors[i - 1] < LBL_H:
            anchors[i] = anchors[i - 1] + LBL_H

    for bi, (name, off, size, kind) in enumerate(BANDS):
        y0, y1 = band_y(off), band_y(off + size)
        h = max(y1 - y0, 3)
        if kind == "free":
            fill, stroke = GREY
            o.append(f'<rect x="{BAR_X}" y="{y0:.1f}" width="{BAR_W}" height="{h:.1f}" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.4" '
                     f'stroke-dasharray="6,4"/>')
        else:
            fill, stroke = colour(name, kind)
            o.append(f'<rect x="{BAR_X}" y="{y0:.1f}" width="{BAR_W}" height="{h:.1f}" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        # in-bar label when the band is tall enough
        if h > 26:
            o.append(f'<text x="{BAR_X+BAR_W/2}" y="{y0+h/2+5:.1f}" font-size="15" '
                     f'font-weight="bold" fill="#212121" text-anchor="middle">'
                     f'{esc(name)}</text>')
        # leader (elbow when the label had to be pushed) + detail to the right
        band_mid = y0 + h / 2
        ly = anchors[bi]
        o.append(f'<path d="M{BAR_X+BAR_W},{band_mid:.1f} L{BAR_X+BAR_W+22},{band_mid:.1f} '
                 f'L{BAR_X+BAR_W+22},{ly:.1f} L{TXT_X-14},{ly:.1f}" fill="none" '
                 f'stroke="#B0BEC5" stroke-width="1.2"/>')
        detail = f"0x{off:07X} .. 0x{off + size - 1:07X}   {human(size)}"
        o.append(f'<text x="{TXT_X}" y="{ly-3:.1f}" font-size="13.5" font-weight="bold" '
                 f'fill="#263238">{esc(name)}</text>')
        o.append(f'<text x="{TXT_X}" y="{ly+14:.1f}" font-size="12" font-family="monospace" '
                 f'fill="#546E7A">{esc(detail)}</text>')
        notes = []
        if name in LAYOUT:
            notes.append(f"-> DRAM 0x{LAYOUT[name]['addr']:08X}")
            inm = [k for k, v in MANIFESTS.items() if name in v]
            notes.append("manifest: " + (", ".join(inm) if inm
                                         else "none (config-read by the FPGA itself)"))
        if kind == "reserved":
            notes.append("WRITABLE - a reflash must NEVER erase this")
        if name in READ_ONLY:
            notes.append("read-only at runtime")
        if notes:
            o.append(f'<text x="{TXT_X+430}" y="{ly-3:.1f}" font-size="12" fill="#37474F">'
                     f'{esc(notes[0])}</text>')
            for i, n in enumerate(notes[1:]):
                col = "#6A1B9A" if "NEVER" in n else "#37474F"
                o.append(f'<text x="{TXT_X+430}" y="{ly+14+i*15:.1f}" font-size="11.5" '
                         f'fill="{col}">{esc(n)}</text>')

    # scale ticks every MiB
    for mib in range(0, (FLASH_SIZE >> 20) + 1):
        y = band_y(mib << 20)
        o.append(f'<path d="M{BAR_X-12},{y:.1f} L{BAR_X},{y:.1f}" stroke="#90A4AE" '
                 f'stroke-width="1.2"/>')
        o.append(f'<text x="{BAR_X-18}" y="{y+4:.1f}" font-size="11" fill="#90A4AE" '
                 f'text-anchor="end">{mib} MiB</text>')

    # manifests
    my = BAR_Y + BAR_H + 44
    o.append(f'<rect x="{BAR_X}" y="{my}" width="900" height="{34+len(MANIFESTS)*22}" '
             f'rx="9" fill="#FFFFFF" stroke="#B0BEC5" stroke-width="1.6"/>')
    o.append(f'<text x="{BAR_X+16}" y="{my+24}" font-size="14" font-weight="bold" '
             f'fill="#212121">FLASHBOOT_MANIFESTS - what the BIOS actually copies to '
             f'DRAM at boot</text>')
    for i, (mname, imgs) in enumerate(MANIFESTS.items()):
        o.append(f'<text x="{BAR_X+26}" y="{my+46+i*22}" font-size="12.5" '
                 f'font-family="monospace" font-weight="bold" fill="#263238">'
                 f'--flashboot {esc(mname)}</text>')
        o.append(f'<text x="{BAR_X+250}" y="{my+46+i*22}" font-size="12.5" '
                 f'font-family="monospace" fill="#37474F">'
                 f'{esc(", ".join(imgs) if imgs else "(nothing - serial upload of every image)")}'
                 f'</text>')

    # legend
    ly2 = my
    o.append(f'<rect x="{BAR_X+940}" y="{ly2}" width="480" height="{34+len(MANIFESTS)*22}" '
             f'rx="9" fill="{RED[0]}" stroke="{RED[1]}" stroke-width="1.6"/>')
    o.append(f'<text x="{BAR_X+956}" y="{ly2+24}" font-size="14" font-weight="bold" '
             f'fill="#B71C1C">The rule the purple slots exist to protect</text>')
    for i, s in enumerate([
            "A gateware update that silently wipes saved bindings",
            "and fault logs is worse than not having them: the",
            "entity then comes back unbound only SOMETIMES."]):
        o.append(f'<text x="{BAR_X+956}" y="{ly2+46+i*20}" font-size="12" fill="#B71C1C">'
                 f'{esc(s)}</text>')

    o.append('</svg>')
    return "\n".join(o)


def drawio():
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(nid, x, y, w, h, label, fill, stroke, fs=12, bold=False):
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 f"fontSize={fs};align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
                 + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{nid}" value="{esc(label)}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')

    vertex("title", 40, 20, 1200, 40,
           f"QSPI flash map - {human(FLASH_SIZE)} device, to scale "
           f"(GENERATED from FLASHBOOT_LAYOUT + FLASHBOOT_RESERVED)", "none", "none", 20, True)
    for i, (name, off, size, kind) in enumerate(BANDS):
        y0, y1 = band_y(off), band_y(off + size)
        fill, stroke = (GREY if kind == "free" else colour(name, kind))
        extra = ""
        if name in LAYOUT:
            extra = f"\n-> DRAM 0x{LAYOUT[name]['addr']:08X}"
        if kind == "reserved":
            extra += "\nWRITABLE - a reflash must NEVER erase this"
        vertex(f"b{i}", BAR_X, y0, BAR_W + 520, max(y1 - y0, 18),
               f"{name}   0x{off:07X}..0x{off+size-1:07X}   {human(size)}{extra}",
               fill, stroke)
    vertex("man", BAR_X, BAR_Y + BAR_H + 44, 900, 34 + len(MANIFESTS) * 22,
           "FLASHBOOT_MANIFESTS - what the BIOS copies to DRAM at boot\n"
           + "\n".join(f"{k}: {', '.join(v) if v else '(nothing - serial upload)'}"
                       for k, v in MANIFESTS.items()), "#FFFFFF", "#B0BEC5")
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="flash-layout">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>{body}</root>'
            f'</mxGraphModel></diagram></mxfile>')


base = sys.argv[1] if len(sys.argv) > 1 else "flash_layout"
Path(base + ".svg").write_text(svg(), encoding="utf-8")
Path(base + ".drawio").write_text(drawio(), encoding="utf-8")
print(f"wrote {base}.svg and {base}.drawio ({len(ROWS)} slots, "
      f"{len(PROBLEMS)} map problem(s))")
