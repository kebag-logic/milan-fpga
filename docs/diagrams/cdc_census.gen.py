#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the clock-domain-crossing census — every CDC in the design, which
primitive implements it and which two clocks it joins — as an editable .drawio
master plus a rendered .svg.  Style follows DOC_MAP.gen.py /
SYSTEM_DOMAIN_MAP.gen.py (pastel fill + darker stroke, rounded boxes).

**NOTHING HERE IS TRANSCRIBED.**  Both halves are parsed:

    hdl/**/*.sv          every instantiation of cdc_pulse / cdc_handshake /
                         cdc_pair_fifo / ptp_csr_sync, with the clock nets its
                         port map actually connects
    sw/litex/milan_soc.py  every `_axis_dp_cdc(...)` call site, the AXI-Lite
                         clock-domain crossing and every `MultiReg(...)`

"Only these primitives cross a domain" is the design's core CDC claim, and a
hand-drawn picture of it is exactly the kind of thing that quietly stops being
true.  Re-running this script is how you check it: a new crossing appears in
the drawing by itself, and a crossing built out of something *other* than these
primitives is, by construction, the one thing this census cannot show — which
is why the drawing says so on its face.

Usage:
    python3 docs/diagrams/cdc_census.gen.py docs/diagrams/cdc_census
    rsvg-convert -w 1900 docs/diagrams/cdc_census.svg \
        -o docs/diagrams/cdc_census.png
"""
import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HDL = REPO / "hdl"
SOC = REPO / "sw" / "litex" / "milan_soc.py"

#: primitive -> (the two clock ports, one-line contract)
PRIMS = {
    "cdc_pulse":     (("src_clk", "dest_clk"), "single-cycle pulse, toggle + 2-FF sync"),
    "cdc_handshake": (("src_clk", "dest_clk"), "wide payload, req/ack handshake"),
    "cdc_pair_fifo": (("wclk_i", "rclk_i"),    "async FIFO, gray-coded pointers"),
    "ptp_csr_sync":  (("aclk", "ts_clk"),      "CSR to PHC: value + toggled apply strobe"),
}


def esc(s):
    return html.escape(str(s), quote=True)


def die(what):
    raise SystemExit(f"cdc_census.gen.py: cannot parse {what} — the source shape "
                     f"changed; fix this generator, do not hand-draw the census.")


def strip_comments(txt):
    return re.sub(r"//.*", "", txt)


# --------------------------------------------------------------------------
# RTL side
# --------------------------------------------------------------------------
def rtl_crossings():
    """[(module, instance, primitive, clk_a, clk_b, relpath)] over hdl/."""
    rows = []
    for sv in sorted(HDL.rglob("*.sv")):
        raw = sv.read_text(errors="ignore")
        if sv.stem in PRIMS:          # the primitive's own definition
            continue
        body = strip_comments(raw)
        m = re.search(r"^\s*module\s+(\w+)", body, re.M)
        owner = m.group(1) if m else sv.stem
        for prim, (ports, _doc) in PRIMS.items():
            # `prim [#(...)] inst_name ( ... );`
            for im in re.finditer(
                    rf"\b{prim}\b\s*(?:#\s*\((?:[^()]|\([^()]*\))*\)\s*)?"
                    rf"(\w+)\s*\((?P<map>(?:[^()]|\([^()]*\))*)\)\s*;", body):
                inst, pmap = im.group(1), im.group("map")
                clks = []
                for p in ports:
                    cm = re.search(rf"\.{p}\s*\(\s*([^)]*?)\s*\)", pmap)
                    clks.append(cm.group(1).strip() if cm else "?")
                if "?" in clks:
                    die(f"the clock ports {ports} of {prim} {inst} in "
                        f"{sv.relative_to(REPO)} - the primitive's port names moved")
                rows.append((owner, inst, prim, clks[0], clks[1],
                             str(sv.relative_to(REPO))))
    if not rows:
        die("any CDC primitive instantiation under hdl/")
    return sorted(rows)


# --------------------------------------------------------------------------
# LiteX side
# --------------------------------------------------------------------------
def soc_crossings():
    """[(kind, name, note)] for the SoC-generated crossings."""
    txt = SOC.read_text(encoding="utf-8")
    body = re.sub(r"^\s*#.*", "", txt, flags=re.M)
    rows = []
    for m in re.finditer(r"_axis_dp_cdc\(\s*\w+\s*,\s*\"([^\"]+)\"[^)]*?"
                         r"to_datapath\s*=\s*(True|False)", body, re.S):
        rows.append(("AXIS stream CDC", m.group(1),
                     "into the datapath" if m.group(2) == "True"
                     else "out of the datapath"))
    if re.search(r"milan_axil_cdc\s*=\s*axi\.AXILiteClockDomainCrossing", body):
        rows.append(("AXI-Lite CDC", "milan_axil_cdc",
                     "the whole CSR register ABI, sys to cd_milan"))
    n_multireg = len(re.findall(r"MultiReg\(", body))
    if n_multireg:
        rows.append(("MultiReg 2-FF", f"x{n_multireg} call sites",
                     "single-bit status/IRQ levels (incl. the CSR IRQ to sys)"))
    if not rows:
        die("any _axis_dp_cdc / AXILiteClockDomainCrossing / MultiReg in milan_soc.py")
    return rows


RTL = rtl_crossings()
SOCX = soc_crossings()

# group the RTL rows by owning module for a readable drawing
BY_OWNER = {}
for owner, inst, prim, ca, cb, rel in RTL:
    BY_OWNER.setdefault(owner, []).append((inst, prim, ca, cb))
OWNERS = sorted(BY_OWNER, key=lambda o: (-len(BY_OWNER[o]), o))

# palette (fill, stroke)
BLUE = ("#E3F2FD", "#1565C0")
GREEN = ("#E8F5E9", "#2E7D32")
ORANGE = ("#FFF3E0", "#EF6C00")
PURPLE = ("#F3E5F5", "#6A1B9A")
GREY = ("#ECEFF1", "#455A64")
GOLD = ("#FFF8E1", "#F9A825")
RED = ("#FFEBEE", "#C62828")

PRIM_COLOUR = {"cdc_pulse": GREEN, "cdc_handshake": PURPLE,
               "cdc_pair_fifo": BLUE, "ptp_csr_sync": ORANGE}

COL_W, COL_GAP, MARGIN = 430, 26, 60
COLS = 3
ROW_H, HDR_H, LINE_H = 0, 30, 16


def owner_h(o):
    return HDR_H + len(BY_OWNER[o]) * LINE_H + 14


# lay the owner cards out in COLS balanced columns
def layout():
    heights = [0] * COLS
    place = {}
    for o in OWNERS:
        c = heights.index(min(heights))
        place[o] = (MARGIN + c * (COL_W + COL_GAP), 250 + heights[c])
        heights[c] += owner_h(o) + 14
    return place, max(heights)


PLACE, STACK_H = layout()
W = MARGIN * 2 + COLS * COL_W + (COLS - 1) * COL_GAP
H = 250 + STACK_H + 330


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>']
    o.append('<text x="40" y="52" font-size="30" font-weight="bold" fill="#263238">'
             f'Clock-domain crossings - the whole census ({len(RTL)} in fabric, '
             f'{len(SOCX)} generated by the SoC)</text>')
    o.append('<text x="40" y="82" font-size="15" fill="#546E7A">GENERATED: every '
             'cdc_pulse / cdc_handshake / cdc_pair_fifo / ptp_csr_sync '
             'instantiation parsed out of hdl/**/*.sv with the clock nets its own '
             'port map connects, plus every</text>')
    o.append('<text x="40" y="104" font-size="15" fill="#546E7A">'
             '_axis_dp_cdc / AXILiteClockDomainCrossing / MultiReg call site in '
             'sw/litex/milan_soc.py. Re-run it to re-check the claim below.</text>')

    # the primitive legend
    lx = MARGIN
    o.append(f'<text x="{lx}" y="{150}" font-size="17" font-weight="bold" '
             f'fill="#78909C">THE ONLY FOUR THINGS ALLOWED TO CROSS</text>')
    for i, (prim, (ports, doc)) in enumerate(PRIMS.items()):
        fill, stroke = PRIM_COLOUR[prim]
        n = sum(1 for r in RTL if r[2] == prim)
        x = lx + i * (COL_W * 3 + COL_GAP * 2) / 4
        o.append(f'<rect x="{x:.0f}" y="166" width="{(COL_W*3+COL_GAP*2)/4-14:.0f}" '
                 f'height="58" rx="8" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="2"/>')
        o.append(f'<text x="{x+12:.0f}" y="188" font-size="14" font-weight="bold" '
                 f'fill="#212121">{esc(prim)}  x{n}</text>')
        o.append(f'<text x="{x+12:.0f}" y="208" font-size="11.5" fill="#37474F">'
                 f'{esc(doc)}</text>')

    # one card per owning module
    for owner in OWNERS:
        x, y = PLACE[owner]
        h = owner_h(owner)
        o.append(f'<rect x="{x}" y="{y}" width="{COL_W}" height="{h}" rx="9" '
                 f'fill="#FFFFFF" stroke="#B0BEC5" stroke-width="1.8"/>')
        o.append(f'<text x="{x+12}" y="{y+21}" font-size="14" font-weight="bold" '
                 f'fill="#263238">{esc(owner)}</text>')
        for i, (inst, prim, ca, cb) in enumerate(BY_OWNER[owner]):
            fill, stroke = PRIM_COLOUR[prim]
            ty = y + HDR_H + i * LINE_H + 12
            o.append(f'<rect x="{x+12}" y="{ty-10}" width="9" height="9" rx="2" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
            o.append(f'<text x="{x+28}" y="{ty}" font-size="11" '
                     f'font-family="monospace" fill="#37474F">'
                     f'{esc(inst)}: {esc(ca)} -&gt; {esc(cb)}</text>')

    # the SoC-generated half
    sy = 250 + STACK_H + 20
    o.append(f'<text x="{MARGIN}" y="{sy}" font-size="17" font-weight="bold" '
             f'fill="#78909C">GENERATED BY add_milan_datapath() - the sys / '
             f'cd_milan boundary</text>')
    bw = (W - 2 * MARGIN)
    o.append(f'<rect x="{MARGIN}" y="{sy+16}" width="{bw}" height="{28+len(SOCX)*17}" '
             f'rx="9" fill="{GREY[0]}" stroke="{GREY[1]}" stroke-width="2"/>')
    for i, (kind, name, note) in enumerate(SOCX):
        o.append(f'<text x="{MARGIN+16}" y="{sy+38+i*17}" font-size="11.5" '
                 f'font-family="monospace" fill="#263238">{esc(kind)}</text>')
        o.append(f'<text x="{MARGIN+196}" y="{sy+38+i*17}" font-size="11.5" '
                 f'font-family="monospace" fill="#37474F">{esc(name)}</text>')
        o.append(f'<text x="{MARGIN+440}" y="{sy+38+i*17}" font-size="11.5" '
                 f'fill="#546E7A">{esc(note)}</text>')

    # the claim
    cy = sy + 16 + 28 + len(SOCX) * 17 + 22
    o.append(f'<rect x="{MARGIN}" y="{cy}" width="{bw}" height="92" rx="9" '
             f'fill="{RED[0]}" stroke="{RED[1]}" stroke-width="2"/>')
    o.append(f'<text x="{MARGIN+16}" y="{cy+26}" font-size="14.5" font-weight="bold" '
             f'fill="#B71C1C">What this census can and cannot prove</text>')
    for i, s in enumerate([
        "It proves every crossing built from one of the four primitives is drawn here, with the clock "
        "nets the RTL itself connects.",
        "It CANNOT prove a signal is not crossing a domain some other way - a bare assignment between "
        "two clocked processes is",
        "invisible to this parse and to simulation alike. That is what the constraint files and the "
        "synthesis CDC report are for."]):
        o.append(f'<text x="{MARGIN+16}" y="{cy+50+i*18}" font-size="12" '
                 f'fill="#B71C1C">{esc(s)}</text>')

    o.append('</svg>')
    return "\n".join(o)


def drawio():
    """The editable master: one draw.io vertex per module card and per crossing."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(nid, x, y, w, h, label, fill, stroke, fs=12, bold=False,
               parent="1", align="left"):
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 f"fontSize={fs};align={align};verticalAlign=top;spacingLeft=8;spacingTop=4;"
                 + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{nid}" value="{esc(label)}" style="{style}" vertex="1" '
                     f'parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" '
                     f'height="{h}" as="geometry"/></mxCell>')

    vertex("title", 40, 20, 1500, 44,
           f"Clock-domain crossings - the whole census ({len(RTL)} in fabric, "
           f"{len(SOCX)} generated by the SoC). GENERATED from hdl/**/*.sv + "
           f"sw/litex/milan_soc.py.", "none", "none", 20, True)
    for i, (prim, (_ports, doc)) in enumerate(PRIMS.items()):
        fill, stroke = PRIM_COLOUR[prim]
        n = sum(1 for r in RTL if r[2] == prim)
        vertex(f"p{i}", MARGIN + i * 340, 160, 320, 60,
               f"{prim}  x{n}\n{doc}", fill, stroke)
    # module cards, each carrying its crossings as child vertices
    for oi, owner in enumerate(OWNERS):
        x, y = PLACE[owner]
        h = owner_h(owner)
        vertex(f"m{oi}", x, y, COL_W, h, owner, "#FFFFFF", "#B0BEC5", 13, True)
        for i, (inst, prim, ca, cb) in enumerate(BY_OWNER[owner]):
            fill, stroke = PRIM_COLOUR[prim]
            vertex(f"m{oi}_{i}", 10, HDR_H + i * LINE_H - 2, COL_W - 20, LINE_H,
                   f"{inst}: {ca} -> {cb}", fill, stroke, 10,
                   parent=f"m{oi}")
    sy = 250 + STACK_H + 36
    vertex("soc", MARGIN, sy, W - 2 * MARGIN, 28 + len(SOCX) * 18,
           "GENERATED BY add_milan_datapath() - the sys / cd_milan boundary\n"
           + "\n".join(f"{k}  {n}  -  {note}" for k, n, note in SOCX),
           GREY[0], GREY[1])
    vertex("claim", MARGIN, sy + 40 + len(SOCX) * 18, W - 2 * MARGIN, 92,
           "What this census can and cannot prove: it proves every crossing built "
           "from one of the four primitives is drawn here. It CANNOT prove a signal "
           "is not crossing some other way - a bare assignment between two clocked "
           "processes is invisible to this parse and to simulation alike. That is "
           "what the constraints and the synthesis CDC report are for.",
           RED[0], RED[1])
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="cdc-census">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>{body}</root>'
            f'</mxGraphModel></diagram></mxfile>')


base = sys.argv[1] if len(sys.argv) > 1 else "cdc_census"
Path(base + ".svg").write_text(svg(), encoding="utf-8")
Path(base + ".drawio").write_text(drawio(), encoding="utf-8")
print(f"wrote {base}.svg and {base}.drawio ({len(RTL)} fabric crossings across "
      f"{len(OWNERS)} modules, {len(SOCX)} SoC-generated)")
