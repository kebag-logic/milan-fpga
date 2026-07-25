#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the time-sync clock-chain diagram (docs/design/TIME_SYNC.md) as
both an editable .drawio and a rendered .svg from ONE node/edge table.

Content: the three clocks and how they chain -
  wire -> PHY/MAC -> ptp_ts_top taps -> PHC <-> ptp4l/phc2sys <-> system clock
  PHC -> CRF -> MMCM-DRP servo -> audio MMCM -> media clock -> I2S/TDM
with the CSR touchpoints labeled (offsets per docs/reference/REGISTER_MAP.md).
Arrows are TIME/TIMESTAMP flow, not audio sample flow.

Regenerate:
    python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain
    rsvg-convert -w 2000 docs/diagrams/timesync_chain.svg \
        -o docs/diagrams/timesync_chain.png
"""
import html, sys

W, H = 1760, 832

# palette (fill, stroke) - house colors (DOC_MAP.gen.py)
BLUE   = ("#E3F2FD", "#1565C0")   # fabric, network-time lane
GREEN  = ("#E8F5E9", "#2E7D32")   # fabric, media-clock lane
PURPLE = ("#F3E5F5", "#6A1B9A")   # software (softcore daemons/driver)
GOLD   = ("#FFF8E1", "#F9A825")   # the PHC hub
ORANGE = ("#FFF3E0", "#EF6C00")   # AVTP timestamp consumers
GREY   = ("#ECEFF1", "#455A64")   # wire / notes

# ---- nodes: id -> (x, y, w, h, title, sublines, (fill,stroke), dashed) ----
N = {
 # lane A - network time
 "wire":    (40,116,130,84,"1 GbE wire","802.1AS peer\n(AVB switch / board)",GREY,0),
 "phymac":  (205,116,150,84,"PHY + MAC","RGMII/GMII\nLiteEth or MilanMAC",BLUE,0),
 "tstap":   (390,116,250,84,"ptp_ts_top TX+RX taps","latch PHC @SOP, qualify @TLAST\n0x88F7 EVENT msgs only",BLUE,0),
 "tsring":  (675,116,200,84,"dma-ts record ring","16 B {ns, seq/type/dir}\nLiteX CSR (build/csr.csv)",BLUE,0),
 "kleth":   (910,116,190,84,"kl-eth driver","/dev/ptp0 + SO_TIMESTAMPING\nmatches {msgType, seq}",PURPLE,0),
 "ptp4l":   (1135,116,180,84,"ptp4l","BMCA + servo (softcore)\ningressLatency 3511/1490 ns",PURPLE,0),
 "hwnote":  (1350,116,370,84,"silicon record (2026-07-13)","peer delay 600 us (SW) -> 1.3 us (HW)\nslave lock rms 2-4 ns through the AVB switch",GREY,1),
 # row 2 - the PHC hub + system-clock side
 "phc":     (40,290,330,96,"PHC - timestamp_counter","Q8.24 ns accumulator, datapath clock\nCSR 0x500 CTRL - 0x504 INCR - 0x508 ADJ - 0x520 CMD",GOLD,0),
 "phc2sys": (410,290,170,96,"phc2sys","PHC -> CLOCK_REALTIME\n(softcore daemon)",PURPLE,0),
 "sysclk":  (615,290,185,96,"system clock","Linux CLOCK_REALTIME\n(timers, userland)",PURPLE,0),
 "g2c":     (1190,290,330,96,"gptp2csr.sh","publishes GM 0x624/0x628 - pdelay 0x6E4\nAS_PATH parent 0x730/0x734 (ADP/AEM truth)",PURPLE,0),
 # AAF timestamp-consumer strip
 "aafpkt":  (40,445,300,76,"AAF packetizer","avtp_timestamp = ptp_now + PTO\n(PTO: SET_STREAM_INFO acc-lat, reset 2 ms)",ORANGE,0),
 "rxmon":   (380,445,300,76,"AVTP RX monitor","ts_delta 0x6EC = avtp_ts - ptp_now\nLATE / EARLY counters",ORANGE,0),
 "locknote":(1430,445,290,76,"media-lock rule","internal source: lock on first valid PDU\nexternal (CRF): lock only when servo converged",GREY,1),
 # lane B - media clock
 "mmcm":    (40,596,230,96,"audio MMCM 24.576 MHz","integer x34/43 off 31.081 MHz\n-10.6 ppm base - fine-PS 16.9 ps + DRP",GREEN,0),
 "div":     (305,596,150,96,"/512","48 kHz media clock\n(MCLK/SCLK/LRCK dividers)",GREEN,0),
 "frontend":(490,596,200,96,"I2S / TDM front-ends","DAC render + ADC capture\npair FIFO, converged flag",GREEN,0),
 "crftx":   (725,596,240,96,"KL_crf_tx (talker)","every 96th sample event:\nts = PHC ns + PTO - 500 PDU/s",GREEN,0),
 "crfwire": (1000,596,120,96,"wire","CRF stream\nsubtype 4",GREY,0),
 "crfrx":   (1155,596,240,96,"KL_crf_rx (listener)","validate Milan 7.3.2 - delta 0x744\nrate 0x748 - lock 0x738[31]",GREEN,0),
 "servo":   (1430,596,290,96,"KL_mmcm_drp_servo","in: rate error (ns/512 ms) - PI FLL +-200 ppm\nMCSRV 0x8F8/0x8FC - engages at clock_source == 2",GREEN,0),
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
 ("kleth","ptp4l","",                [(1100,158),(1135,158)],"d"),
 ("ptp4l","phc","adjfine / adjtime / settime - CSR 0x500 group (via kl-eth)",
                                     [(1225,200),(1225,246),(205,246),(205,290)],"c"),
 ("phc","tstap","ptp_now (64-bit ns)",[(100,290),(100,224),(515,224),(515,200)],"c"),
 ("phc","phc2sys","",                [(370,338),(410,338)],"c"),
 ("phc2sys","sysclk","",             [(580,338),(615,338)],"c"),
 ("ptp4l","g2c","PMC PARENT_DATA_SET",[(1280,200),(1280,290)],"c"),
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
 (40,278,"THE HUB - PTP hardware clock (PHC) and its software consumers","#B26A00"),
 (40,433,"AVTP TIMESTAMP CONSUMERS (presentation time against the PHC)","#EF6C00"),
 (40,566,"MEDIA CLOCK - CRF + MMCM-DRP servo (Milan v1.2 clause 7.3)","#2E7D32"),
 (40,584,"coherent chain: capture, CRF grid and (via the servo) the listener playback clock follow one audio-MMCM lineage - loop -83.9 dB (2026-07-23, converter floor)","#555555"),
]

TITLE = "milan-fpga time sync - the three clocks and how they chain"
SUB   = ("network PHC (gPTP)  ->  system clock (phc2sys)   -   PHC + CRF  ->  media clock (MMCM-DRP servo)"
         "   -   CSR offsets per docs/reference/REGISTER_MAP.md   -   arrows = time/timestamp flow, not audio samples")
FOOT  = ("sources: hdl/ieee8021as/ptp_timestamp - hdl/ieee1722/crf - hdl/milan/milan_datapath.sv - sw/litex/milan_soc.py"
         "   -   regenerate: python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain")


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- SVG ----
def svg():
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
            o.append(f'<text x="{tx}" y="{ty}" font-size="10.5" fill="#5D4037" text-anchor="{anch}">{esc(label)}</text>')
    o.append(f'<text x="40" y="{H-18}" font-size="11" fill="#78909C">{esc(FOOT)}</text>')
    o.append('</svg>')
    return "\n".join(o)


# ------------------------------------------------------------- drawio ----
def dio_esc(s):
    return html.escape(str(s), quote=True).replace("\n", "&#10;")


def drawio():
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(cid, x, y, w, h, label, fill, stroke, dash, fs=12, bold=1):
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 f"fontSize={fs};align=center;verticalAlign=middle;"
                 + ("dashed=1;" if dash else "")
                 + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{cid}" value="{dio_esc(label)}" style="{style}" '
                     f'vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def text(cid, x, y, w, label, col, fs=13, bold=1):
        style = (f"text;html=1;align=left;verticalAlign=middle;fontSize={fs};"
                 f"fontColor={col};" + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{cid}" value="{dio_esc(label)}" style="{style}" '
                     f'vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y-16}" width="{w}" height="22" as="geometry"/></mxCell>')

    for nid, (x, y, w, h, title, sub, (fill, stroke), dash) in N.items():
        lbl = title + ("\n" + sub if sub else "")
        vertex("n_" + nid, x, y, w, h, lbl, fill, stroke, dash)
    for k, (x, y, t, col) in enumerate(LANE_LABELS):
        text(f"t_{k}", x, y, 1680, t, col, fs=12 if y == 584 else 13, bold=0 if y == 584 else 1)
    text("t_title", 40, 44, 1400, TITLE, "#263238", fs=22)
    text("t_sub", 40, 70, 1680, SUB, "#546E7A", fs=11, bold=0)
    text("t_foot", 40, H-18, 1680, FOOT, "#78909C", fs=10, bold=0)

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
open(base + ".svg", "w").write(svg())
open(base + ".drawio", "w").write(drawio())
print("wrote", base + ".svg", "and", base + ".drawio")
