#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the end-to-end audio stream path diagram (talker chain + listener
chain with CSR touchpoints and the AAF_LATENCY_TAPS.md tap points) as both an
editable .drawio and a rendered .svg. Style follows DOC_MAP.gen.py /
SYSTEM_DOMAIN_MAP.gen.py (pastel fill + darker stroke, rounded boxes).

Render PNG with:
    python3 docs/diagrams/audio_stream_path.gen.py docs/diagrams/audio_stream_path
    rsvg-convert -w 2000 docs/diagrams/audio_stream_path.svg \
        -o docs/diagrams/audio_stream_path.png
"""
import html
import sys

def esc(s):
    return html.escape(str(s), quote=True)

# palette (fill, stroke) — DOC_MAP.gen.py family
BLUE   = ("#E3F2FD", "#1565C0")   # capture / frontend sources
PURPLE = ("#F3E5F5", "#6A1B9A")   # channel-map fabric (mux / crossbar)
GREEN  = ("#E8F5E9", "#2E7D32")   # AAF engines (packetizer / depacketizer / monitor)
ORANGE = ("#FFF3E0", "#EF6C00")   # egress-ingress boundary (shaper / MAC / PTP)
GREY   = ("#ECEFF1", "#455A64")   # other fabric egress sources
GOLD   = ("#FFF8E1", "#F9A825")   # latency tap chips

# ---- nodes: id -> (x, y, w, h, title, sublines, (fill, stroke)) -------------
# Talker lane (top), listener lane (bottom). Coordinates hand-placed.
N = {}
def node(nid, x, y, w, h, title, sub, col):
    N[nid] = (x, y, w, h, title, sub, col)

# --- talker sources (pair-stream frontends) ---
node("i2s",  60, 170, 268, 78, "KL_aaf_capture_i2s",
     ["Pmod I2S2 ADC (CS5343), I2S master", "24.576 MHz MMCM /512 = 48 kHz, slot 0"], BLUE)
node("tdm",  60, 262, 268, 78, "KL_tdm_capture",
     ["TDM slave, 8/16/32 slots", "pair k = TDM slots {2k, 2k+1}"], BLUE)
node("loop", 60, 354, 268, 78, "received AAF loopback",
     ["accepted depacketizer channel pairs", "elastic replay queues, per RX stream"], BLUE)
node("tone", 60, 446, 268, 78, "KL_tone_gen",
     ["1 kHz 0 dBFS, 48-entry table", "TONE_CTRL 0x6DC"], BLUE)

node("cmux", 440, 288, 268, 116, "KL_chan_map_capture",
     ["32-slot map RAM {en, src, idx}", "src: I2S / TDM / TONE / LOOP / zero",
      "CSR 0x900 window (bypass = legacy)"], PURPLE)

node("pkt", 812, 288, 292, 116, "KL_aaf_packetizer",
     ["TCTX xN talkers, 6 samples/ch per PDU", "payload 24*C B, frame 42+24*C B",
      "avtp_timestamp = PHC ns + transit offset", "AAF_CTRL 0x654 + 0x800 TCTX window"], GREEN)

# Other live fabric sources join the AAF talker at the arbiter.
node("fabricctl", 850, 130, 300, 64, "fabric protocol / time sources",
     ["protocol processor · MAAP · gPTP · CRF"], GREY)

node("inject", 1208, 288, 268, 116, "fabric egress arbiter",
     ["adp_tx_arbiter (crf_dp_mux)", "AAF heads the fabric TX trunk;",
      "bandwidth held by processor SRP", "reservation face grants admission"], ORANGE)

node("mactx", 1580, 300, 190, 92, "MAC TX",
     ["GMII, VLAN SR class", "egress timestamp at MAC boundary"], ORANGE)

# --- wire ---
node("wire", 1880, 296, 300, 100, "the wire",
     ["AAF-PCM class A, 8000 PDU/s @48 k", "DMAC = MAAP claim, VLAN SR VID",
      "presentation time rides every PDU"], GOLD)

# --- listener lane ---
node("macrx", 60, 760, 200, 92, "MAC RX",
     ["rx_axis_from_mac tap", "TCAM DMAC filter"], ORANGE)
node("parser", 320, 760, 268, 92, "avtp_stream_parser",
     ["+ KL_stream_table: wire-truth", "stream_id match (entry 0 =", "ACMP-bound record)"], GREEN)
node("rxmon", 648, 748, 296, 116, "KL_avtp_rx_monitor_ctx",
     ["lock on 1st valid PDU, 8-PDU settle,", "100 ms silence unlock, format compare",
      "0x6B8/0x6BC/0x6C0 - ts_delta 0x6EC"], GREEN)
node("depkt", 1004, 748, 280, 116, "KL_aaf_rx_depacketizer",
     ["S32BE payload, 1 AXIS frame/PDU,", "tuser = stream; commits only on the",
      "monitor accept pulse - PCMRX_CNT 0x6C4"], GREEN)
node("route", 1344, 760, 240, 92, "KL_pcm_route",
     ["route word {RENDER, reserved}", "reset: stream 0 = RENDER"], PURPLE)

# RENDER branch (right)
node("lpf", 1640, 690, 220, 78, "KL_pcm_lpf",
     ["20 kHz Butterworth biquad", "serial-MAC, ~12 clk/pair",
      "LPF_P=0 PRUNES it (ax7101 does)"], PURPLE)
node("feed", 1900, 690, 220, 78, "KL_i2s_feed_mux",
     ["direct listener tap or", "mapped physical pair {0,1}"], PURPLE)
node("i2spb", 2160, 690, 268, 78, "KL_i2s_playback",
     ["CS4344 DAC, clean-clock free-run", "I2SPB_STAT 0x6D8, wire-truth chans"], BLUE)
node("cxbar", 1640, 820, 220, 92, "KL_chan_map_render",
     ["64 stream-ch -> 10 phys", "wire-truth channels_per_frame", "CSR 0x900 window"], PURPLE)
node("tdmout", 2160, 820, 268, 92, "KL_tdm_render",
     ["TDM8 out, lane 0 slots 0..7", "double-buffered frames"], BLUE)

W, H = 2500, 1060

# ---- latency tap chips (AAF_LATENCY_TAPS.md stage names, CSR 0x870) ---------
# (cx, cy, label)
TAPS = [
    (400, 346, "CAP"),        # pair enters the packetizer feed
    (1130, 320, "PKT_SOF"),   # packetizer first beat
    (1130, 372, "PKT_EOF"),   # packetizer last beat
    (1800, 346, "MAC_TX"),    # frame egress
    (290, 806, "MAC_RX"),     # frame ingress
    (970, 806, "ACCEPT"),     # monitor parse-complete/accept
    (1310, 806, "DEPKT"),     # payload last beat
    (1600, 806, "FABRIC_RENDER"),  # selected render payload
]

# ---- edges (svg hand-routed; drawio uses source/target ids) -----------------
# (from, to, kind) kind: "h" straight horizontal, "elbow" via mid, "v" vertical
EDGES = [
    ("i2s", "cmux", "pair"), ("tdm", "cmux", "pair"),
    ("loop", "cmux", "pair"), ("tone", "cmux", "pair"),
    ("cmux", "pkt", "h"),
    ("pkt", "inject", "h"),
    ("fabricctl", "inject", "v"),
    ("inject", "mactx", "h"),
    ("mactx", "wire", "h"),
    ("wire", "macrx", "wrap"),
    ("macrx", "parser", "h"), ("parser", "rxmon", "h"),
    ("rxmon", "depkt", "h"), ("depkt", "route", "h"),
    ("route", "lpf", "h"), ("lpf", "feed", "h"),
    ("feed", "i2spb", "h"), ("route", "cxbar", "h2"),
    ("cxbar", "feed", "h"), ("cxbar", "tdmout", "h"),
]

def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">']
    o.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')
    o.append('<defs><marker id="arr" markerWidth="12" markerHeight="12" refX="7" refY="4" '
             'orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#546E7A"/></marker></defs>')
    o.append(f'<text x="40" y="52" font-size="30" font-weight="bold" fill="#263238">'
             f'milan-fpga audio stream path - capture to render</text>')
    o.append(f'<text x="40" y="82" font-size="15" fill="#546E7A">talker chain (top) and '
             f'listener chain (bottom) with CSR touchpoints; gold chips = the '
             f'AAF_LATENCY_TAPS.md tap points (CSR 0x870 block)</text>')

    # lane bands
    o.append(f'<rect x="30" y="104" width="{W-60}" height="440" rx="12" fill="none" '
             f'stroke="#B0BEC5" stroke-width="1.6" stroke-dasharray="7,5"/>')
    o.append(f'<text x="48" y="132" font-size="17" font-weight="bold" fill="#78909C">'
             f'TALKER - capture to wire</text>')
    o.append(f'<rect x="30" y="660" width="{W-60}" height="370" rx="12" fill="none" '
             f'stroke="#B0BEC5" stroke-width="1.6" stroke-dasharray="7,5"/>')
    o.append(f'<text x="48" y="688" font-size="17" font-weight="bold" fill="#78909C">'
             f'LISTENER - wire to fabric render</text>')

    def edge_pts(a, b, kind):
        ax, ay, aw, ah = N[a][:4]
        bx, by, bw, bh = N[b][:4]
        if kind in ("h", "pair"):
            return [(ax+aw, ay+ah/2), (bx, by+bh/2)]
        if kind == "h2":   # elbow: right of a, down, into left of b
            return [(ax+aw, ay+ah/2), (bx-26, ay+ah/2), (bx-26, by+bh/2), (bx, by+bh/2)]
        if kind == "v":    # bottom of a to top of b (x of b centre)
            return [(ax+aw/2, ay+ah), (ax+aw/2, (ay+ah+by)/2), (bx+bw/2, (ay+ah+by)/2),
                    (bx+bw/2, by)]
        if kind == "wrap": # wire (talker right) down + left to MAC RX (listener left)
            return [(ax+aw/2, ay+ah), (ax+aw/2, 610), (N[b][0]+N[b][2]/2, 610),
                    (N[b][0]+N[b][2]/2, by)]
        return []

    for a, b, kind in EDGES:
        pts = edge_pts(a, b, kind)
        if not pts:
            continue
        d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
        dash = ' stroke-dasharray="6,4"' if kind == "pair" else ""
        o.append(f'<path d="{d}" fill="none" stroke="#546E7A" stroke-width="2.2" '
                 f'marker-end="url(#arr)"{dash}/>')

    # pair-stream contract label
    o.append(f'<text x="352" y="252" font-size="12.5" fill="#37474F" font-style="italic">'
             f'{esc("{pair_valid, pair_slot, L, R}")}</text>')
    o.append('<text x="352" y="268" font-size="12.5" fill="#37474F" font-style="italic">'
             'one shared contract</text>')
    # loopback note under the received-AAF source
    o.append('<text x="440" y="430" font-size="12" fill="#6A1B9A">the LOOP source replays '
             'accepted receive pairs;</text>')
    o.append('<text x="440" y="446" font-size="12" fill="#6A1B9A">reserved source encodings '
             'resolve to digital silence</text>')
    # wire annotation on the wrap edge
    o.append('<text x="620" y="600" font-size="13.5" font-weight="bold" fill="#8D6E63">'
             'AAF-PCM PDUs with presentation time (avtp_timestamp) - the reference AVB '
             'switch forwards per the SRP reservation</text>')

    # nodes
    for nid, (x, y, w, h, title, sub, (fill, stroke)) in N.items():
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"/>')
        o.append(f'<text x="{x+12}" y="{y+22}" font-size="14.5" font-weight="bold" '
                 f'fill="#212121">{esc(title)}</text>')
        for i, s in enumerate(sub):
            o.append(f'<text x="{x+12}" y="{y+40+i*15}" font-size="11.8" fill="#37474F">'
                     f'{esc(s)}</text>')

    # tap chips
    for cx, cy, lab in TAPS:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{GOLD[1]}" stroke="#795548" '
                 f'stroke-width="1.4"/>')
        o.append(f'<text x="{cx}" y="{cy-13}" font-size="11.5" font-weight="bold" '
                 f'fill="#795548" text-anchor="middle">{esc(lab)}</text>')

    # legend
    lx, ly = 60, 930
    o.append(f'<rect x="{lx}" y="{ly}" width="1080" height="118" rx="10" fill="#FFFFFF" '
             f'stroke="#B0BEC5" stroke-width="1.4"/>')
    o.append(f'<text x="{lx+16}" y="{ly+26}" font-size="14" font-weight="bold" '
             f'fill="#212121">Legend</text>')
    items = [
        (BLUE,   "physical audio I/O (ADC/DAC/TDM) + receive loopback"),
        (PURPLE, "channel-map fabric: capture mux / render crossbar / route"),
        (GREEN,  "AAF engines: packetizer - parser - monitor - depacketizer"),
        (ORANGE, "egress/ingress boundary: CBS shaper, PTP timestamps, MAC"),
        (GREY,   "fabric protocol and time egress sources"),
    ]
    for i, ((f_, s_), txt) in enumerate(items):
        col = i % 2
        row = i // 2
        bx = lx + 16 + col * 540
        by = ly + 40 + row * 30
        o.append(f'<rect x="{bx}" y="{by}" width="26" height="18" rx="4" fill="{f_}" '
                 f'stroke="{s_}" stroke-width="1.6"/>')
        o.append(f'<text x="{bx+36}" y="{by+14}" font-size="12.5" fill="#37474F">'
                 f'{esc(txt)}</text>')
    o.append(f'<circle cx="{lx+569}" cy="{ly+94}" r="8" fill="{GOLD[1]}" stroke="#795548"/>')
    o.append(f'<text x="{lx+592}" y="{ly+98}" font-size="12.5" fill="#37474F">latency tap '
             f'(docs/AAF_LATENCY_TAPS.md; CSR 0x870)</text>')

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
    vertex("title", 40, 20, 1400, 36,
           "milan-fpga audio stream path - capture to render", "none", "none", 22, True)
    for nid, (x, y, w, h, title, sub, (fill, stroke)) in N.items():
        vertex(f"n_{nid}", x, y, w, h, title + "\n" + "\n".join(sub), fill, stroke)
    for i, (cx, cy, lab) in enumerate(TAPS):
        style = (f"ellipse;whiteSpace=wrap;html=1;fillColor={GOLD[1]};strokeColor=#795548;"
                 f"fontSize=9;verticalLabelPosition=top;verticalAlign=bottom;fontStyle=1;")
        cells.append(f'<mxCell id="tap{i}" value="{esc(lab)}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{cx-9}" y="{cy-9}" width="18" height="18" '
                     f'as="geometry"/></mxCell>')
    for i, (a, b, kind) in enumerate(EDGES):
        style = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#546E7A;"
                 "strokeWidth=2;" + ("dashed=1;" if kind == "pair" else ""))
        cells.append(f'<mxCell id="e{i}" style="{style}" edge="1" parent="1" '
                     f'source="n_{a}" target="n_{b}"><mxGeometry relative="1" '
                     f'as="geometry"/></mxCell>')
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="audio-stream-path">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>{body}</root>'
            f'</mxGraphModel></diagram></mxfile>')

base = sys.argv[1] if len(sys.argv) > 1 else "audio_stream_path"
open(base + ".svg", "w").write(svg())
open(base + ".drawio", "w").write(drawio())
print("wrote", base + ".svg", "and", base + ".drawio")
