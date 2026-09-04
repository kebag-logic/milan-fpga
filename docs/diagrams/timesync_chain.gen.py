#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the time-sync clock-chain diagram (docs/design/TIME_SYNC.md) as
both an editable .drawio and a rendered .svg from ONE node/edge table.

Content: the three clocks and how they chain -
  wire -> PHY/MAC -> fabric gPTP engine <-> PHC -> atomic publication bank
  PHC -> CRF -> MMCM-DRP servo -> audio MMCM -> media clock -> I2S/TDM
with the CSR touchpoints labeled (offsets per docs/reference/REGISTER_MAP.md).
Arrows are TIME/TIMESTAMP flow, not audio sample flow.

Regenerate:
    python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain
    rsvg-convert -w 2000 docs/diagrams/timesync_chain.svg \
        -o docs/diagrams/timesync_chain.png
"""
import html, sys
from dataclasses import dataclass

W, H = 1760, 832

# palette (fill, stroke) - house colors (DOC_MAP.gen.py)
BLUE   = ("#E3F2FD", "#1565C0")   # fabric, network-time lane
GREEN  = ("#E8F5E9", "#2E7D32")   # fabric, media-clock lane
PURPLE = ("#F3E5F5", "#6A1B9A")   # bare-metal firmware/control
GOLD   = ("#FFF8E1", "#F9A825")   # the PHC hub
ORANGE = ("#FFF3E0", "#EF6C00")   # AVTP timestamp consumers
GREY   = ("#ECEFF1", "#455A64")   # wire / notes

# ---- nodes: id -> (x, y, w, h, title, sublines, (fill,stroke), dashed) ----
N = {
 # lane A - network time
 "wire":    (40,116,130,84,"1 GbE wire","802.1AS peer\n(AVB switch / board)",GREY,0),
 "phymac":  (205,116,150,84,"PHY + MAC","RGMII/GMII\nLiteEth or MilanMAC",BLUE,0),
 "tstap":   (390,116,250,84,"KL_gptp_shadow RX/TX","delivered-frame RX stamp\nMAC-boundary TX stamp",BLUE,0),
 "tsring":  (675,116,200,84,"timestamp transport","RX side FIFO + TX seq/type\nfabric tuple pairing",BLUE,0),
 "kleth":   (910,116,190,84,"KL_gptp_engine","BTCA + Pdelay + Sync\nPHC servo in fabric",BLUE,0),
 "pub":     (1135,116,180,84,"atomic publish bank","GM + parent + flags\npdelay + offset + annq",BLUE,0),
 "hwnote":  (1350,116,370,84,"product ownership (0x0002_0056)",
             "fabric is the ONE PHC/protocol/publication owner (#259)\n"
             "option OFF is ownerless verification hardware",GREY,1),
 # row 2 - the PHC hub + its fabric-owned public consumers
 "phc":     (40,290,330,96,"PHC - timestamp_counter",
             "Q8.24 ns accumulator, datapath clock\n"
             "CSR 0x500 CTRL - 0x504 INCR - 0x508 ADJ - 0x520 CMD",GOLD,0),
 "g2c":     (1190,290,330,96,"public gPTP consumers",
             "CSR GM/parent/pdelay - GET_AVB_INFO/PATH\n"
             "CLKV asCapable/sync - every AVTP tu",BLUE,0),
 # AAF timestamp-consumer strip
 "aafpkt":  (40,445,300,76,"AAF packetizer",
             "avtp_timestamp = ptp_now + PTO\n"
             "(PTO: SET_STREAM_INFO acc-lat, reset 2 ms)",ORANGE,0),
 "rxmon":   (380,445,300,76,"AVTP RX monitor","ts_delta 0x6EC = avtp_ts - ptp_now\nLATE / EARLY counters",ORANGE,0),
 "locknote":(1430,445,290,76,"media-lock rule",
             "internal source: lock on first valid PDU\n"
             "external (CRF): lock only when servo converged",GREY,1),
 # lane B - media clock
 "mmcm":    (40,596,230,96,"audio MMCM 24.576 MHz",
             "integer x34/43 off 31.081 MHz\n"
             "-10.6 ppm base - fine-PS 16.9 ps + DRP",GREEN,0),
 "div":     (305,596,150,96,"/512","48 kHz media clock\n(MCLK/SCLK/LRCK dividers)",GREEN,0),
 "frontend":(490,596,200,96,"I2S / TDM front-ends","DAC render + ADC capture\npair FIFO, converged flag",GREEN,0),
 "crftx":   (725,596,240,96,"KL_crf_tx (talker)","every 96th sample event:\nts = PHC ns + PTO - 500 PDU/s",GREEN,0),
 "crfwire": (1000,596,120,96,"wire","CRF stream\nsubtype 4",GREY,0),
 "crfrx":   (1155,596,240,96,"KL_crf_rx (listener)",
             "validate Milan 7.3.2 - delta 0x744\n"
             "rate 0x748 - lock 0x738[31]",GREEN,0),
 "servo":   (1430,596,290,96,"KL_mmcm_drp_servo",
             "in: rate error (ns/512 ms) - PI FLL +-200 ppm\n"
             "MCSRV 0x8F8/0x8FC - engages at the shape.s CRF clock_source",GREEN,0),
}

# ---- edges: (src, dst, label, [waypoints], style) ----
# waypoints = full polyline INCLUDING endpoints (svg draws it verbatim; the
# drawio export derives exit/entry pins + intermediate mxPoints from it).
# style: "d"=data (solid), "c"=control (dashed)
E = [
 ("wire","phymac","RX",              [(170,145),(205,145)],"d"),
 ("phymac","wire","TX",              [(205,175),(170,175)],"d"),
 ("phymac","tstap","",               [(355,145),(390,145)],"d"),
 ("tstap","phymac","",               [(390,175),(355,175)],"d"),
 ("tstap","tsring","",               [(640,158),(675,158)],"d"),
 ("tsring","kleth","",               [(875,158),(910,158)],"d"),
 ("kleth","pub","commit",            [(1100,158),(1135,158)],"d"),
 ("kleth","phc","adjfine / adjtime (fabric owner); settime stays on CSR face",
                                     [(1225,200),(1225,246),(205,246),(205,290)],"c"),
 ("phc","tstap","ptp_now (64-bit ns)",[(100,290),(100,224),(515,224),(515,200)],"c"),
 ("pub","g2c","one coherent generation",[(1280,200),(1280,290)],"c"),
 ("phc","aafpkt","ptp_now + PTO",    [(190,386),(190,445)],"c"),
 ("phc","rxmon","ptp_now",           [(330,386),(330,415),(530,415),(530,445)],"c"),
 ("phc","crftx","ptp_now",           [(350,386),(350,412),(845,412),(845,596)],"c"),
 ("phc","crfrx","ptp_now",           [(310,386),(310,400),(1275,400),(1275,596)],"c"),
 ("mmcm","div","",                   [(270,644),(305,644)],"d"),
 ("div","frontend","",               [(455,644),(490,644)],"d"),
 ("crftx","crfwire","",              [(965,644),(1000,644)],"d"),
 ("crfwire","crfrx","",              [(1120,644),(1155,644)],"d"),
 ("crfrx","servo","",                [(1395,644),(1430,644)],"d"),
 ("mmcm","crftx","clk_audio 24.576 MHz - own /512 + /96 event grid",
                                     [(100,692),(100,718),(830,718),(830,692)],"c"),
 ("servo","mmcm","fine-PS step rate = ppm trim - DRP verify/repair (auto_repair 0x8FC[1])",
                                     [(1575,692),(1575,744),(60,744),(60,692)],"c"),
]

LANE_LABELS = [
 (40,104,"NETWORK TIME - gPTP (802.1AS, domain 0)","#1565C0"),
 (40,278,"THE HUB - PTP hardware clock (PHC) and its public consumers (one owner, #259)","#B26A00"),
 (40,433,"AVTP TIMESTAMP CONSUMERS (presentation time against the PHC)","#EF6C00"),
 (40,566,"MEDIA CLOCK - CRF + MMCM-DRP servo (Milan v1.2 clause 7.3)","#2E7D32"),
 (40,584,
  "coherent chain: capture, CRF grid and (via the servo) the listener playback "
  "clock follow one audio-MMCM lineage - loop -83.9 dB (2026-07-23, converter "
  "floor)","#555555"),
]

TITLE = "milan-fpga time sync - the three clocks and how they chain"
SUB   = ("fabric gPTP  ->  network PHC + atomic public state   -   PHC + CRF  ->  media clock (MMCM-DRP servo)"
         "   -   CSR offsets per docs/reference/REGISTER_MAP.md   -   arrows = time/timestamp flow, not audio samples")
FOOT  = ("sources: hdl/ieee8021as/ptp_timestamp - hdl/ieee1722/crf - "
         "hdl/milan/milan_datapath.sv - sw/litex/milan_soc.py"
         "   -   regenerate: python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain")


def esc(s: object) -> str:
    """XML-safe text, quotes included, because every use is an attribute value."""
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- SVG ----
def svg() -> str:
    """the published .svg: the node boxes, the flow arrows with their labels,
    the lane notes and the source footer."""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">']
    o.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')
    o.append('<defs>'
             '<marker id="arr" markerWidth="12" markerHeight="12" refX="7" refY="4" orient="auto">'
             '<path d="M0,0 L8,4 L0,8 Z" fill="#455A64"/></marker>'
             '<marker id="arrc" markerWidth="12" markerHeight="12" refX="7" refY="4" orient="auto">'
             '<path d="M0,0 L8,4 L0,8 Z" fill="#8D6E63"/></marker>'
             '</defs>')
    o.append(f'<text x="40" y="44" font-size="26" font-weight="bold" fill="#263238">{esc(TITLE)}</text>')
    o.append(f'<text x="40" y="70" font-size="12.5" fill="#546E7A">{esc(SUB)}</text>')
    for x, y, t, col in LANE_LABELS:
        fs = 11 if y in (584,) else 13
        fw = "400" if y in (584,) else "700"
        o.append(f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="{fw}" fill="{col}">{esc(t)}</text>')
    # boxes first, then edges + labels on top (edge labels must never be
    # painted under a box fill)
    for nid, (x, y, w, h, title, sub, (fill, stroke), dash) in N.items():
        dd = ' stroke-dasharray="7 5"' if dash else ''
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"{dd}/>')
        subl = sub.split("\n") if sub else []
        ty = y + 24 if subl else y + h/2 + 5
        o.append(f'<text x="{x+w/2}" y="{ty}" font-size="14" font-weight="bold" '
                 f'fill="#212121" text-anchor="middle">{esc(title)}</text>')
        for j, sl in enumerate(subl):
            o.append(f'<text x="{x+w/2}" y="{y+42+j*15}" font-size="11" fill="#37474F" '
                     f'text-anchor="middle">{esc(sl)}</text>')
    for src, dst, label, pts, sty in E:
        col = "#455A64" if sty == "d" else "#8D6E63"
        mk = "arr" if sty == "d" else "arrc"
        dash = "" if sty == "d" else ' stroke-dasharray="6 4"'
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" marker-end="url(#{mk})"{dash}/>')
        if label:
            # label near the midpoint of the longest segment
            best, bl = None, -1
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                l = abs(x2-x1) + abs(y2-y1)
                if l > bl:
                    bl, best = l, ((x1+x2)/2, (y1+y2)/2, x2 == x1)
            mx, my, vert = best
            tx, ty, anch = (mx+6, my-4, "start") if vert else (mx, my-6, "middle")
            o.append(f'<text x="{tx}" y="{ty}" font-size="10.5" fill="#5D4037" '
                     f'text-anchor="{anch}">{esc(label)}</text>')
    o.append(f'<text x="40" y="{H-18}" font-size="11" fill="#78909C">{esc(FOOT)}</text>')
    o.append('</svg>')
    return "\n".join(o)


# ------------------------------------------------------------- drawio ----
def dio_esc(s: object) -> str:
    """`esc` plus the newline entity: a drawio label lives inside an attribute,
    where a literal line break would end the value."""
    return html.escape(str(s), quote=True).replace("\n", "&#10;")


@dataclass(frozen=True)
class CellStyle:
    """How one drawio vertex is painted: the (fill, stroke) pair off the node
    table, its dashed flag, and the font the label is set in."""
    fill: str
    stroke: str
    dash: int = 0
    fs: int = 12
    bold: int = 1


@dataclass(frozen=True)
class LabelStyle:
    """How one free-standing drawio text cell is painted."""
    col: str
    fs: int = 13
    bold: int = 1


def drawio() -> str:
    """the same chain as an editable .drawio: a vertex per node, a text cell per
    lane note and one routed edge per arrow."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(cid: str, rect: tuple[int, int, int, int], label: str,
               style: CellStyle) -> None:
        """one drawio node box, painted from a `CellStyle` rather than five loose flags."""
        x, y, w, h = rect
        st = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={style.fill};"
              f"strokeColor={style.stroke};"
              f"fontSize={style.fs};align=center;verticalAlign=middle;"
              + ("dashed=1;" if style.dash else "")
              + ("fontStyle=1;" if style.bold else ""))
        cells.append(f'<mxCell id="{cid}" value="{dio_esc(label)}" style="{st}" '
                     f'vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def text(cid: str, x: int, y: int, w: int, label: str,
             style: LabelStyle) -> None:
        """one free-standing drawio label. `y` is the SVG text baseline, and the
        cell is hung 16 above it so both renders put the note in the same place."""
        st = (f"text;html=1;align=left;verticalAlign=middle;fontSize={style.fs};"
              f"fontColor={style.col};" + ("fontStyle=1;" if style.bold else ""))
        cells.append(f'<mxCell id="{cid}" value="{dio_esc(label)}" style="{st}" '
                     f'vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y-16}" width="{w}" height="22" as="geometry"/></mxCell>')

    for nid, (x, y, w, h, title, sub, (fill, stroke), dash) in N.items():
        lbl = title + ("\n" + sub if sub else "")
        vertex("n_" + nid, (x, y, w, h), lbl, CellStyle(fill, stroke, dash))
    for k, (x, y, t, col) in enumerate(LANE_LABELS):
        text(f"t_{k}", x, y, 1680, t,
             LabelStyle(col, fs=12 if y == 584 else 13, bold=0 if y == 584 else 1))
    text("t_title", 40, 44, 1400, TITLE, LabelStyle("#263238", fs=22))
    text("t_sub", 40, 70, 1680, SUB, LabelStyle("#546E7A", fs=11, bold=0))
    text("t_foot", 40, H-18, 1680, FOOT, LabelStyle("#78909C", fs=10, bold=0))

    for k, (src, dst, label, pts, sty) in enumerate(E):
        sx, sy, sw, sh = N[src][:4]
        dx, dy, dw, dh = N[dst][:4]
        (x0, y0), (xn, yn) = pts[0], pts[-1]
        ex, ey = round((x0-sx)/sw, 3), round((y0-sy)/sh, 3)
        nx, ny = round((xn-dx)/dw, 3), round((yn-dy)/dh, 3)
        dash = "dashed=1;" if sty == "c" else ""
        color = "#455A64" if sty == "d" else "#8D6E63"
        st = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
              f"strokeColor={color};strokeWidth=1.8;fontSize=10;labelBackgroundColor=#FAFAFA;"
              f"{dash}exitX={ex};exitY={ey};entryX={nx};entryY={ny};")
        geo = '<mxGeometry relative="1" as="geometry">'
        mid = pts[1:-1]
        if mid:
            geo += ('<Array as="points">'
                    + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in mid)
                    + '</Array>')
        geo += '</mxGeometry>'
        cells.append(f'<mxCell id="e_{k}" value="{dio_esc(label)}" style="{st}" edge="1" '
                     f'parent="1" source="n_{src}" target="n_{dst}">{geo}</mxCell>')

    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="timesync-chain">'
            f'<mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" '
            f'pageHeight="{H}" math="0" shadow="0"><root>{body}</root></mxGraphModel>'
            f'</diagram></mxfile>')


base = sys.argv[1] if len(sys.argv) > 1 else "timesync_chain"
with open(base + ".svg", "w") as fh:
    fh.write(svg())
with open(base + ".drawio", "w") as fh:
    fh.write(drawio())
print("wrote", base + ".svg", "and", base + ".drawio")
