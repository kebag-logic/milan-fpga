#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the ATDECC control-plane overview diagram (docs/design/AEM_AND_AECP.md)
as both an editable .drawio and a rendered .svg (house pattern: DOC_MAP.gen.py).

Shows the fabric control plane: ADP advertiser/parser, the AECP subsystem
(ingress -> validator -> parser -> L0 lock state -> response builder ->
AEM ROM/overlays -> 4-slot unsolicited push engine), the ACMP listener/talker
contexts with the saved-state bind-restore port, MAAP, the monitor-tap RX
recipe, the pairwise low-rate TX arbiter chain, and the CSR/driver touchpoints.

Usage:  python3 atdecc_control_plane.gen.py [basename]
        (writes <basename>.svg + <basename>.drawio; default atdecc_control_plane)
PNG:    rsvg-convert -w 2000 atdecc_control_plane.svg -o atdecc_control_plane.png
"""
import html
import sys

W, H = 1940, 1500

# palette (fill, stroke) — DOC_MAP house pastels
BLUE   = ("#E3F2FD", "#1565C0")   # AECP
GREEN  = ("#E8F5E9", "#2E7D32")   # ADP
ORANGE = ("#FFF3E0", "#EF6C00")   # ACMP
PURPLE = ("#F3E5F5", "#6A1B9A")   # MAAP
GREY   = ("#ECEFF1", "#455A64")   # RX tap / TX chain
GOLD   = ("#FFF8E1", "#F9A825")   # CSR strip
WHITE  = ("#FFFFFF", "#90A4AE")   # note chips

def esc(s):
    return html.escape(s, quote=True)

# ---- boxes: id -> (x, y, w, h, title, sublines, (fill,stroke), kind) ------
# kind: "container" (tinted region, title top-left), "box" (title + sub
# centered-ish), "note" (dashed border)
B = {}
def box(bid, x, y, w, h, title, sub, col, kind="box"):
    B[bid] = (x, y, w, h, title, sub, col, kind)

# RX monitor tap column
box("RX", 40, 190, 250, 840, "MAC RX stream",
    ["post rx_mac_filter (TCAM)",
     "",
     "MONITOR taps only:",
     "every control engine",
     "reads this stream,",
     "none may backpressure",
     "it (house recipe)"], GREY)

# AECP container + children
box("AECP", 340, 130, 1160, 540,
    "KL_aecp_top — AECP / AEM listener   (IEEE 1722.1-2021 §9 · Milan v1.2 §5.4)",
    [], BLUE, "container")
box("ING", 370, 190, 200, 95, "KL_aecp_ingress",
    ["AECP-for-us / discover filter", "store-and-forward, src MAC"], BLUE)
box("VAL", 595, 190, 200, 95, "KL_aecp_packet_validator",
    ["drop bad message_type /", "control_data_length < 12"], BLUE)
box("PAR", 820, 190, 200, 95, "KL_aecp_common_parser",
    ["header struct, entity_id", "match on the first beat"], BLUE)
box("L0", 1045, 190, 200, 95, "KL_aecp_l0_state",
    ["LOCK 60 s owner/expiry", "ACQUIRE -> NOT_SUPPORTED"], BLUE)
box("TMR", 1270, 190, 205, 95, "KL_aecp_timers",
    ["1 kHz tick · lock expiry", "counter-push 1/s throttle"], BLUE)
box("RB", 370, 340, 470, 180, "KL_aecp_response_builder",
    ["capture · classify · SET_* write-back · segment serialiser",
     "4-slot unsolicited push engine (u=1, no-change gate)",
     "GET_DYNAMIC_INFO 0x4B two-pass batch engine",
     "`AEM_DYNMAP dynamic audio-map engine (5.4.2.26-28)",
     "identify_o -> board LED"], BLUE)
box("ACC", 870, 340, 310, 55, "KL_aecp_accessor",
    ["directory (type,index) -> {base,len}"], BLUE)
box("STO", 870, 415, 310, 55, "KL_aecp_aem_store",
    ["generated ROM + write-back RAM"], BLUE)
box("DYN", 870, 490, 310, 55, "KL_aecp_aem_dyn_mux",
    ["live-field read overlay"], BLUE)
box("GEN", 1210, 340, 270, 185, "entity model (generated)",
    ["avdecc/milan-v12-entity*.json",
     "-> avdecc/gen_aem_store.py",
     "   (--overlay: sw/builder",
     "    endstation shapes, NxN)",
     "-> gen/aecp_aem_rom.svh",
     "   + aem_golden.h + aem_rom.json"], WHITE, "note")

# ADP container + children
box("ADP", 340, 720, 390, 310,
    "ADP   (IEEE 1722.1-2021 §6 · discovery)", [], GREEN, "container")
box("ADPP", 365, 785, 165, 150, "KL_adp_parser",
    ["RX: ENTITY_AVAILABLE /", "DEPARTING / DISCOVER", "decode (82-B rule)"], GREEN)
box("ADPA", 550, 785, 165, 220, "adp_advertiser",
    ["ENTITY_AVAILABLE every", "valid_time; discover resp", "(random delay); departing;",
     "available_index++ on", "EVERY ADPDU; discover", "pulse from AECP ingress"], GREEN)

# ACMP container + children
box("ACMP", 770, 720, 450, 310,
    "ACMP   (IEEE 1722.1-2021 §8 · Milan v1.2 §5.5)", [], ORANGE, "container")
box("LST", 785, 785, 205, 220, "KL_acmp_lstn_ctx",
    ["N sink bind contexts,", "one SM + one ctx RAM:",
     "ctx0 probe ladder (5.5.3),", "ctx1 CRF record;",
     "CONNECT/DISCONNECT/", "GET_RX_STATE responder;",
     "ADP talker watch feeds it"], ORANGE)
box("TLK", 1005, 785, 200, 130, "KL_acmp_tlkr_ctx",
    ["N source contexts:", "PROBE_TX SM, 15 s", "window, live params"], ORANGE)
box("RST", 1005, 925, 200, 80, "bind-restore port",
    ["0x7A0 commit -> ENTRY", "record (saved-state)"], ORANGE)

# MAAP
box("MAAP", 1250, 720, 270, 310, "KL_maap",
    ["IEEE 1722 Annex B", "PROBE x3 -> ANNOUNCE,", "DEFEND on conflict;",
     "pool 91:E0:F0 + offset;", "claimed DMAC drives the", "AAF framer (eff_aaf_dmac",
     "mux); softcore may seed", "the offset (re-claim)"], PURPLE)

# TX chain column
box("ARB", 1620, 190, 280, 400, "low-rate TX arbiter chain",
    ["pairwise adp_tx_arbiter tree:", "", "1  AECP + ACMP talker",
     "2  + ADP advertise", "3  + lwSRP MRPDUs (0x680)", "4  + ACMP listener",
     "5  + MAAP", "", "one whole frame per grant"], GREY)
box("DPM", 1620, 660, 280, 90, "TX merge with datapath",
    ["control stream + shaped/PTP", "stream -> one MAC TX"], GREY)
box("MTX", 1620, 790, 280, 80, "MAC TX", ["MilanMAC -> PHY"], GREY)

# CSR strip
box("CSR", 40, 1090, 1860, 330,
    "CSR / driver touchpoints   (milan_csr window; ABI: docs/reference/REGISTER_MAP.md)",
    ["softcore/driver: provisions identity at boot, runs the gptp->CSR daemon, seeds MAAP re-claim, saves/restores ACMP binds (acmp-persist), reads status + forensics"],
    GOLD, "container")
box("C1", 70, 1165, 580, 110, "0x600-0x644  ADP identity + control",
    ["entity_id/model_id/caps · gPTP GM 0x624/8 + domain (daemon-fed)",
     "valid_time · ADP_CMD advertise-now · ADP_STATUS available_index"], GOLD)
box("C2", 670, 1165, 580, 110, "0x648 / 0x64C  AECP status (RO)",
    ["A_AECP_STAT0/1: locked + command count ·",
     "response count + current_configuration"], GOLD)
box("C3", 1270, 1165, 580, 110, "0x6A4 ACMPL_STATE (RO) · 0x6E8 forensics",
    ["listener SM state / bound / SRP flags / last ACMP status ·",
     "walker classify counters"], GOLD)
box("C4", 70, 1290, 580, 110, "0x6CC-0x6D4  MAAP",
    ["enable / seed re-claim · claimed offset, conflicts, DEFENDs ·",
     "addr_valid + SM state"], GOLD)
box("C5", 670, 1290, 580, 110, "0x7A0-0x7B4  ACMP bind-restore",
    ["saved talker/controller ids + flags + commit/status;",
     "software-gated: VERSION >= 0x000A + 0x7A0 write/readback probe"], GOLD)
box("C6", 1270, 1290, 580, 110, "0x680  lwSRP engine (neighbor)",
    ["MSRP Domain/TalkerAdvertise; couples listener_observed into the",
     "talker contexts and gates AAF admission on the reservation"], GOLD)

# ---- edges: (points, label, color, dashed, has_arrow) ---------------------
E = []
def edge(pts, label="", col="#546E7A", dashed=False, arrow=True, lab_at=None):
    E.append((pts, label, col, dashed, arrow, lab_at))

# RX fan-out
edge([(290, 237), (370, 237)], "tap", GREY[1])
edge([(290, 500), (318, 500), (318, 692), (1385, 692)], "monitor-tap rail",
     GREY[1], dashed=True, arrow=False, lab_at=(1150, 684))
edge([(535, 692), (535, 720)], "", GREY[1])
edge([(995, 692), (995, 720)], "", GREY[1])
edge([(1385, 692), (1385, 720)], "", GREY[1])

# AECP pipeline
edge([(570, 237), (595, 237)], "", BLUE[1])
edge([(795, 237), (820, 237)], "", BLUE[1])
edge([(1020, 237), (1045, 237)], "", BLUE[1])
edge([(1270, 237), (1245, 237)], "", BLUE[1])                       # timers -> l0
edge([(920, 285), (920, 305), (560, 305), (560, 340)], "", BLUE[1])  # parser -> builder
edge([(1145, 285), (1145, 318), (660, 318), (660, 340)], "status/reject",
     BLUE[1], lab_at=(900, 314))
edge([(1372, 285), (1372, 330), (760, 330), (760, 340)], "ticks",
     BLUE[1], lab_at=(1080, 326))
edge([(840, 367), (870, 367)], "", BLUE[1])
edge([(1025, 395), (1025, 415)], "", BLUE[1])
edge([(1025, 470), (1025, 490)], "", BLUE[1])
edge([(840, 442), (870, 442)], "SET_* wb", BLUE[1], lab_at=(843, 410))
edge([(870, 517), (840, 517)], "overlaid byte", BLUE[1], lab_at=(700, 535))
edge([(1210, 442), (1180, 442)], "generates", WHITE[1], dashed=True,
     lab_at=(1198, 462))

# couplings (unlabeled dashes; the target boxes name the relationship)
edge([(370, 262), (332, 262), (332, 714), (632, 714), (632, 720)],
     "", GREEN[1], dashed=True)
edge([(460, 720), (460, 706), (860, 706), (860, 720)],
     "", ORANGE[1], dashed=True)

# TX merges
edge([(1500, 430), (1620, 430)], "AECP responses", GREY[1], lab_at=(1504, 424))
edge([(535, 1030), (535, 1055), (1548, 1055), (1548, 470), (1620, 470)],
     "ADPDUs", GREY[1], lab_at=(600, 1049))
edge([(995, 1030), (995, 1065), (1560, 1065), (1560, 510), (1620, 510)],
     "ACMP responses / probes", GREY[1], lab_at=(1060, 1082))
edge([(1520, 875), (1572, 875), (1572, 550), (1620, 550)], "", GREY[1])
edge([(1760, 590), (1760, 660)], "", GREY[1])
edge([(1760, 750), (1760, 790)], "", GREY[1])

TITLE = "ATDECC control plane in fabric — ADP · AECP/AEM · ACMP · MAAP"
SUB = ("Every engine follows the monitor-tap + low-rate-TX recipe; identity is "
       "shared through the 0x600 CSR group so ADP and AEM can never disagree. "
       "Design record: docs/design/AEM_AND_AECP.md")

# ------------------------------------------------------------------ SVG ----
def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>',
         '<defs><marker id="arr" markerWidth="12" markerHeight="12" refX="7" '
         'refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#607D8B"/>'
         '</marker></defs>',
         f'<text x="40" y="56" font-size="30" font-weight="bold" '
         f'fill="#263238">{esc(TITLE)}</text>',
         f'<text x="40" y="88" font-size="14.5" fill="#546E7A">{esc(SUB)}</text>']

    # containers first (background), then boxes
    for kind_pass in ("container", "box", "note"):
        for bid, (x, y, w, h, title, sub, (fill, stroke), kind) in B.items():
            if kind != kind_pass:
                continue
            dash = ' stroke-dasharray="6,4"' if kind == "note" else ""
            op = ' fill-opacity="0.45"' if kind == "container" else ""
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}{op}/>')
            if kind == "container":
                o.append(f'<text x="{x+18}" y="{y+30}" font-size="16.5" '
                         f'font-weight="bold" fill="{stroke}">{esc(title)}</text>')
                for j, sl in enumerate(sub):
                    o.append(f'<text x="{x+18}" y="{y+52+j*17}" font-size="12.5" '
                             f'fill="#5D4037">{esc(sl)}</text>')
            else:
                o.append(f'<text x="{x+12}" y="{y+22}" font-size="13.5" '
                         f'font-weight="bold" fill="#212121">{esc(title)}</text>')
                for j, sl in enumerate(sub):
                    o.append(f'<text x="{x+12}" y="{y+40+j*15}" font-size="11.5" '
                             f'fill="#37474F">{esc(sl)}</text>')

    # edges
    for pts, label, col, dashed, arrow, lab_at in E:
        d = "M" + " L".join(f"{px} {py}" for px, py in pts)
        dash = ' stroke-dasharray="7,5"' if dashed else ""
        mk = ' marker-end="url(#arr)"' if arrow else ""
        o.append(f'<path d="{d}" fill="none" stroke="{col}" '
                 f'stroke-width="2"{dash}{mk}/>')
        if label:
            lx, ly = lab_at if lab_at else (pts[0][0] + 6, pts[0][1] - 6)
            o.append(f'<text x="{lx}" y="{ly}" font-size="11.5" '
                     f'fill="{col}">{esc(label)}</text>')

    o.append(f'<text x="40" y="{H-32}" font-size="12.5" fill="#546E7A">'
             + esc("Generated by docs/diagrams/atdecc_control_plane.gen.py — "
                   "edit the generator (or the .drawio), never the render. "
                   "Beat-level drill-down: hdl/ieee17221/aecp/doc/"
                   "atdecc_architecture.drawio") + '</text>')
    o.append("</svg>")
    return "\n".join(o)

# --------------------------------------------------------------- drawio ----
def drawio():
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    ids = {}
    n = [1]

    def vtx(label, x, y, w, h, style):
        n[0] += 1
        i = f"n{n[0]}"
        cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" '
                     f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
                     f'width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    vtx(TITLE, 40, 20, 1400, 34,
        "text;html=1;fontSize=22;fontStyle=1;align=left;")
    vtx(SUB, 40, 58, 1700, 24, "text;html=1;fontSize=12;align=left;")

    for kind_pass in ("container", "box", "note"):
        for bid, (x, y, w, h, title, sub, (fill, stroke), kind) in B.items():
            if kind != kind_pass:
                continue
            label = title if not sub else title + "\n" + "\n".join(sub)
            style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};"
                     f"strokeColor={stroke};align=left;verticalAlign=top;"
                     f"spacingLeft=10;spacingTop=6;fontSize=12;")
            if kind == "container":
                style += "fontStyle=1;fontSize=14;opacity=60;"
            if kind == "note":
                style += "dashed=1;"
            ids[bid] = vtx(label, x, y, w, h, style)

    def ept(pts, label, col, dashed):
        n[0] += 1
        i = f"e{n[0]}"
        style = (f"edgeStyle=none;rounded=1;html=1;strokeColor={col};"
                 f"strokeWidth=2;fontSize=11;fontColor={col};"
                 + ("dashed=1;" if dashed else ""))
        (x0, y0), (x1, y1) = pts[0], pts[-1]
        mids = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts[1:-1])
        arr = f'<Array as="points">{mids}</Array>' if mids else ""
        cells.append(
            f'<mxCell id="{i}" value="{esc(label)}" style="{style}" edge="1" '
            f'parent="1"><mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x0}" y="{y0}" as="sourcePoint"/>'
            f'<mxPoint x="{x1}" y="{y1}" as="targetPoint"/>{arr}'
            f'</mxGeometry></mxCell>')

    for pts, label, col, dashed, arrow, _ in E:
        ept(pts, label, col, dashed)

    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="atdecc-control-plane">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0">'
            f'<root>{body}</root></mxGraphModel></diagram></mxfile>')

base = sys.argv[1] if len(sys.argv) > 1 else "atdecc_control_plane"
open(base + ".svg", "w").write(svg())
open(base + ".drawio", "w").write(drawio())
print("wrote", base + ".svg", "and", base + ".drawio")
