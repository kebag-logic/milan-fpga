#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the NxN `0x800` window row map — which lwSRP attribute-context row
a given window selection actually reaches, per shipping shape — as an editable
.drawio and a rendered .svg.  Style follows DOC_MAP.gen.py /
SYSTEM_DOMAIN_MAP.gen.py.

**NOTHING HERE IS TRANSCRIBED.**  The geometry comes from the three places that
define it, and the generator asserts each one still has the shape it reads:

    hdl/milan/milan_datapath.sv        SRP_CTX_ROWS_C = 2*N_STREAMS - 1
                                       (how many rows the fabric elaborates)
    sw/builder/endstation_builder.py   ctx_rows_required = L + T - 1  and
                                       SRP_CTX_IDX_BITS  (the hard row ceiling)
    configs/*.yaml                     L and T of every shipping shape

This is the diagram of a bug that already shipped: with the table sized
``max(L, T)`` instead of ``L + T - 1`` every ``t > 0`` talker row sat above
``N_CTX_P``, was refused *silently*, and the readback aliased row 0 — so the
window reported the legacy pair's live status for a row that had never been
provisioned, and every ``t > 0`` admission gate was pinned shut.  The mapping is
pure arithmetic, which is exactly why it should be drawn from the arithmetic
rather than copied by hand.

Usage:
    python3 docs/diagrams/nxn_window_map.gen.py docs/diagrams/nxn_window_map
    rsvg-convert -w 1800 docs/diagrams/nxn_window_map.svg \
        -o docs/diagrams/nxn_window_map.png
"""
import html
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
DATAPATH = REPO / "hdl" / "milan" / "milan_datapath.sv"
BUILDER = REPO / "sw" / "builder" / "endstation_builder.py"
CONFIGS = sorted((REPO / "configs").glob("endstation_*.yaml"))


def esc(s):
    return html.escape(str(s), quote=True)


def die(what):
    raise SystemExit(f"nxn_window_map.gen.py: cannot confirm {what} — the source "
                     f"shape changed; fix this generator, do not hand-draw it.")


# --- confirm the formulas, do not assume them -------------------------------
dp = DATAPATH.read_text(encoding="utf-8")
if not re.search(r"localparam\s+int\s+SRP_CTX_ROWS_C\s*=\s*2\s*\*\s*N_STREAMS\s*-\s*1\s*;", dp):
    die("SRP_CTX_ROWS_C = 2*N_STREAMS - 1 in milan_datapath.sv")

bl = BUILDER.read_text(encoding="utf-8")
if not re.search(r"ctx_rows_required\s*=\s*len\(listeners\)\s*\+\s*len\(talkers\)\s*-\s*1", bl):
    die("ctx_rows_required = L + T - 1 in endstation_builder.py")
m = re.search(r"^SRP_CTX_IDX_BITS\s*=\s*(\d+)", bl, re.M)
if not m:
    die("SRP_CTX_IDX_BITS in endstation_builder.py")
IDX_BITS = int(m.group(1))
ROW_CEILING = 1 << IDX_BITS

# --- the shipping shapes ----------------------------------------------------
SHAPES = []            # (label, board, L, T)
for cfg in CONFIGS:
    d = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    st = d.get("streams", {})
    L = len(st.get("listeners", []))
    T = len(st.get("talkers", []))
    board = (d.get("board", {}).get("target") or "?")
    SHAPES.append((cfg.stem.replace("endstation_", ""), board, L, T))
if not SHAPES:
    die("any configs/endstation_*.yaml")


def ctx_row(kind, i, L):
    """The lwSRP ctx row a `0x800` selection reaches (milan_datapath comment).

    row 0            = the legacy talker+listener pair (LWSRP_* 0x680 group)
    listener k>0     -> k
    talker t>0       -> (L-1)+t
    """
    if i == 0:
        return 0
    return i if kind == "listener" else (L - 1) + i


# palette
BLUE = ("#E3F2FD", "#1565C0")      # listener selections
GREEN = ("#E8F5E9", "#2E7D32")     # talker selections
GOLD = ("#FFF8E1", "#F9A825")      # the shared legacy row 0
GREY = ("#ECEFF1", "#B0BEC5")      # rows the shape does not use
RED = ("#FFEBEE", "#C62828")

CELL_W, CELL_H, CELL_GAP = 96, 58, 8
MARGIN_X = 60
SHAPE_H = 300
SHAPE_H_MIN = 210
W = max(1500, MARGIN_X * 2 + (2 * max(s[2] for s in SHAPES) - 1) * (CELL_W + CELL_GAP))
H = 250 + SHAPE_H * len(SHAPES) + 150


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>',
         '<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="6" refY="3.5" '
         'orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#546E7A"/></marker></defs>']
    o.append('<text x="40" y="52" font-size="30" font-weight="bold" fill="#263238">'
             'The 0x800 window row map - which lwSRP attribute row a selection '
             'really reaches</text>')
    o.append('<text x="40" y="82" font-size="15" fill="#546E7A">GENERATED from '
             'milan_datapath.sv (SRP_CTX_ROWS_C = 2*N_STREAMS - 1), '
             'endstation_builder.py (ctx_rows_required = L+T-1, SRP_CTX_IDX_BITS) '
             'and every configs/endstation_*.yaml.</text>')
    o.append('<text x="40" y="106" font-size="15" fill="#546E7A">'
             'An attribute row is NOT a stream. Row 0 is the legacy talker+listener '
             'PAIR (the LWSRP_* 0x680 group); listener k maps to row k; talker t maps '
             'to row (L-1)+t.</text>')
    o.append(f'<text x="40" y="130" font-size="15" fill="#B71C1C">'
             f'So the top row an LxT shape can name is (L-1)+(T-1) and the table must '
             f'be L+T-1 rows - NOT max(L,T). ctx_idx is {IDX_BITS} bits, so '
             f'L+T-1 &lt;= {ROW_CEILING} caps the fabric.</text>')

    y = 190
    for label, board, L, T in SHAPES:
        rows = L + T - 1
        o.append(f'<text x="{MARGIN_X}" y="{y}" font-size="19" font-weight="bold" '
                 f'fill="#263238">{esc(label)} - board {esc(board)}, L={L} listeners, '
                 f'T={T} talkers  =&gt;  {rows} attribute row{"s" if rows != 1 else ""}</text>')
        fits = rows <= ROW_CEILING
        o.append(f'<text x="{MARGIN_X}" y="{y+22}" font-size="13" '
                 f'fill="{"#2E7D32" if fits else "#C62828"}">'
                 f'{esc(f"L+T-1 = {rows} <= {ROW_CEILING}: fits the ctx_idx width" if fits else f"L+T-1 = {rows} > {ROW_CEILING}: the builder REFUSES this shape")}'
                 f'</text>')

        # --- listener selections (above the strip) ---
        ly = y + 46
        for k in range(L):
            x = MARGIN_X + ctx_row("listener", k, L) * (CELL_W + CELL_GAP)
            fill, stroke = (GOLD if k == 0 else BLUE)
            o.append(f'<rect x="{x}" y="{ly}" width="{CELL_W}" height="40" rx="7" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
            o.append(f'<text x="{x+CELL_W/2}" y="{ly+17}" font-size="11.5" '
                     f'fill="#37474F" text-anchor="middle">dir=0 (listener)</text>')
            o.append(f'<text x="{x+CELL_W/2}" y="{ly+32}" font-size="13.5" '
                     f'font-weight="bold" fill="#212121" text-anchor="middle">'
                     f'idx {k}</text>')

        # --- the ctx row strip ---
        sy = ly + 62
        for r in range(rows):
            x = MARGIN_X + r * (CELL_W + CELL_GAP)
            fill, stroke = (GOLD if r == 0 else GREY)
            o.append(f'<rect x="{x}" y="{sy}" width="{CELL_W}" height="{CELL_H}" rx="7" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            o.append(f'<text x="{x+CELL_W/2}" y="{sy+24}" font-size="15" '
                     f'font-weight="bold" fill="#212121" text-anchor="middle">'
                     f'row {r}</text>')
            note = "legacy pair" if r == 0 else ("listener" if r < L else "talker")
            o.append(f'<text x="{x+CELL_W/2}" y="{sy+43}" font-size="11" fill="#546E7A" '
                     f'text-anchor="middle">{esc(note)}</text>')

        # the row the OLD max(L,T) sizing stopped at — the shipped bug, to scale
        old = max(L, T)
        if old < rows:
            bx = MARGIN_X + old * (CELL_W + CELL_GAP) - CELL_GAP / 2
            o.append(f'<path d="M{bx},{sy-8} L{bx},{sy+CELL_H+8}" stroke="#C62828" '
                     f'stroke-width="2.6" stroke-dasharray="7,5"/>')
            o.append(f'<text x="{bx+8}" y="{sy-14}" font-size="12" font-weight="bold" '
                     f'fill="#C62828">the old max(L,T)={old} table ended here - rows '
                     f'{old}..{rows-1} were refused SILENTLY and aliased row 0</text>')

        # --- talker selections (below the strip) ---
        ty = sy + CELL_H + 22
        for t in range(T):
            x = MARGIN_X + ctx_row("talker", t, L) * (CELL_W + CELL_GAP)
            fill, stroke = (GOLD if t == 0 else GREEN)
            o.append(f'<rect x="{x}" y="{ty}" width="{CELL_W}" height="40" rx="7" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
            o.append(f'<text x="{x+CELL_W/2}" y="{ty+17}" font-size="11.5" '
                     f'fill="#37474F" text-anchor="middle">dir=1 (talker)</text>')
            o.append(f'<text x="{x+CELL_W/2}" y="{ty+32}" font-size="13.5" '
                     f'font-weight="bold" fill="#212121" text-anchor="middle">'
                     f'idx {t}</text>')

        # connector ticks
        for k in range(L):
            x = MARGIN_X + ctx_row("listener", k, L) * (CELL_W + CELL_GAP) + CELL_W / 2
            o.append(f'<path d="M{x},{ly+40} L{x},{sy}" stroke="#546E7A" '
                     f'stroke-width="1.6" marker-end="url(#arr)"/>')
        for t in range(T):
            x = MARGIN_X + ctx_row("talker", t, L) * (CELL_W + CELL_GAP) + CELL_W / 2
            o.append(f'<path d="M{x},{ty} L{x},{sy+CELL_H}" stroke="#546E7A" '
                     f'stroke-width="1.6" marker-end="url(#arr)"/>')

        y += SHAPE_H

    # the loud-refusal note
    ny = y - SHAPE_H + 250
    o.append(f'<rect x="{MARGIN_X}" y="{ny}" width="{W-2*MARGIN_X}" height="112" rx="9" '
             f'fill="{RED[0]}" stroke="{RED[1]}" stroke-width="2"/>')
    o.append(f'<text x="{MARGIN_X+18}" y="{ny+26}" font-size="15" font-weight="bold" '
             f'fill="#B71C1C">The refusal is now LOUD - which is the whole point of '
             f'sizing the table from this arithmetic</text>')
    for i, s in enumerate([
            "An out-of-range row is still granted (the port must never hang), but ctx_rd_stat returns "
            "0xDEAD - the window's",
            "\"not backed\" idiom - instead of row 0's live status, and ctx_oor_o latches into "
            "LWSRP_STATUS[11]. On a correctly-sized",
            "build that bit reads 0; a 1 means the shape needs more attribute rows than N_CTX_P "
            "provides, which is otherwise",
            "invisible from every counter in the design."]):
        o.append(f'<text x="{MARGIN_X+18}" y="{ny+50+i*18}" font-size="12" fill="#B71C1C">'
                 f'{esc(s)}</text>')

    o.append('</svg>')
    return "\n".join(o)


def drawio():
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(nid, x, y, w, h, label, fill, stroke, fs=12, bold=False):
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 f"fontSize={fs};align=center;verticalAlign=middle;"
                 + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{nid}" value="{esc(label)}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')

    vertex("title", 40, 20, 1400, 40,
           "The 0x800 window row map - listener k -> row k, talker t -> row (L-1)+t "
           "(GENERATED)", "none", "none", 20, True)
    y = 190
    for si, (label, board, L, T) in enumerate(SHAPES):
        rows = L + T - 1
        vertex(f"h{si}", MARGIN_X, y - 34, 900, 28,
               f"{label} - board {board}, L={L}, T={T} => {rows} attribute rows "
               f"(ceiling {ROW_CEILING})", "none", "none", 15, True)
        for k in range(L):
            x = MARGIN_X + ctx_row("listener", k, L) * (CELL_W + CELL_GAP)
            f_, s_ = (GOLD if k == 0 else BLUE)
            vertex(f"l{si}_{k}", x, y + 46, CELL_W, 40, f"dir=0 idx {k}", f_, s_)
        for r in range(rows):
            x = MARGIN_X + r * (CELL_W + CELL_GAP)
            f_, s_ = (GOLD if r == 0 else GREY)
            note = "legacy pair" if r == 0 else ("listener" if r < L else "talker")
            vertex(f"r{si}_{r}", x, y + 108, CELL_W, CELL_H, f"row {r}\n{note}", f_, s_)
        for t in range(T):
            x = MARGIN_X + ctx_row("talker", t, L) * (CELL_W + CELL_GAP)
            f_, s_ = (GOLD if t == 0 else GREEN)
            vertex(f"t{si}_{t}", x, y + 188, CELL_W, 40, f"dir=1 idx {t}", f_, s_)
        for k in range(L):
            cells.append(f'<mxCell id="el{si}_{k}" style="edgeStyle=orthogonalEdgeStyle;'
                         f'html=1;strokeColor=#546E7A;" edge="1" parent="1" '
                         f'source="l{si}_{k}" target="r{si}_{ctx_row("listener", k, L)}">'
                         f'<mxGeometry relative="1" as="geometry"/></mxCell>')
        for t in range(T):
            cells.append(f'<mxCell id="et{si}_{t}" style="edgeStyle=orthogonalEdgeStyle;'
                         f'html=1;strokeColor=#546E7A;" edge="1" parent="1" '
                         f'source="t{si}_{t}" target="r{si}_{ctx_row("talker", t, L)}">'
                         f'<mxGeometry relative="1" as="geometry"/></mxCell>')
        y += SHAPE_H
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="nxn-window-map">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>{body}</root>'
            f'</mxGraphModel></diagram></mxfile>')


base = sys.argv[1] if len(sys.argv) > 1 else "nxn_window_map"
Path(base + ".svg").write_text(svg(), encoding="utf-8")
Path(base + ".drawio").write_text(drawio(), encoding="utf-8")
print(f"wrote {base}.svg and {base}.drawio ("
      + ", ".join(f"{n} L={L} T={T} rows={L+T-1}" for n, _b, L, T in SHAPES)
      + f"; ceiling {ROW_CEILING})")
