#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the AECP unsolicited-notification SLOT anatomy diagram as both an
editable .drawio and a rendered .svg (house pattern: DOC_MAP.gen.py).

WHY THIS DIAGRAM EXISTS. `AECP_UNSOL_SLOTS_C` (aecp_pkg.sv:190) is a bare 4,
and that 4 is the single largest parameterised lever in the AECP subsystem:
Vivado OOC of KL_aecp_response_builder measures 4 -> 2 slots at -749 LUT
(-8.7 %) and -296 FF, about -523 LUT in context = 2.0 % of the whole Milan
fabric. Nothing in the tree showed WHAT that 4 multiplies, so the cost looked
like a mystery instead of a structure. It is not a mystery: one slot is a
129-bit registration record plus TWELVE independent pending-notification
classes plus a monitor rail, and every one of those needs its own slot walk.

Three panels, which is what makes it useful rather than decorative:
  1. HIERARCHY   - where slot-dimensioned state physically lives, and the
                   two-reader hazard the package comment warns about.
  2. DATA FLOW   - registration in, the pend set, the emission walk, the wire.
  3. STATE       - the slot lifecycle and the gh #59 controller-available
                   probe that sheds a dead controller.

Usage:  python3 unsol_slots.gen.py [basename]
        (writes <basename>.svg + <basename>.drawio; default unsol_slots)
PNG:    rsvg-convert -w 2200 unsol_slots.svg -o unsol_slots.png
"""
import html
import sys

W, H = 2200, 1560

TITLE = "AECP_UNSOL_SLOTS_C = 4 — what the 4 actually multiplies"
SUB = ("IEEE 1722.1-2021 §7.5.2 REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION · Milan v1.2 §5.4.5 · "
       "hdl/ieee17221/aecp/  ·  measured: 4→2 slots = −749 LUT OOC (−8.7 %), ~−523 LUT in context")

BLUE   = ("#E3F2FD", "#1565C0")   # response builder / AECP
GREEN  = ("#E8F5E9", "#2E7D32")   # per-slot storage
ORANGE = ("#FFF3E0", "#EF6C00")   # timers / monitor
PURPLE = ("#F3E5F5", "#6A1B9A")   # emission / TX
GREY   = ("#ECEFF1", "#455A64")   # ingress / wire
GOLD   = ("#FFF8E1", "#F9A825")   # states
WHITE  = ("#FFFFFF", "#90A4AE")   # notes
RED    = ("#FFEBEE", "#C62828")   # hazards


def esc(s):
    return html.escape(s, quote=True)


B = {}
def box(bid, x, y, w, h, title, sub, col, kind="box"):
    B[bid] = (x, y, w, h, title, sub, col, kind)


E = []
def edge(pts, label="", col="#546E7A", dashed=False, arrow=True, lab_at=None):
    E.append((pts, label, col, dashed, arrow, lab_at))


# ======================================================================== #
# PANEL 1 — HIERARCHY: where slot-dimensioned state lives                   #
# ======================================================================== #
box("P1", 30, 120, 690, 1330,
    "1 · HIERARCHY — where the ×4 physically lives", [], WHITE, "container")

box("DP", 55, 175, 640, 62, "milan_datapath",
    ["instantiates KL_aecp_top with only .CLK_FREQ_HZ_P —",
     "MON_SLOTS_P / MONITOR_* take SV defaults (:2851)"], GREY)

box("TOP", 55, 265, 640, 118, "KL_aecp_top   (hdl/ieee17221/aecp/KL_aecp_top.sv)",
    ["THE JOIN. :261 declares the four slot rails",
     "   logic [AECP_UNSOL_SLOTS_C-1:0] mon_arm_w, mon_heard_w,",
     "                                  mon_clear_w, mon_exp_w;",
     ":265 passes .MON_SLOTS_P(AECP_UNSOL_SLOTS_C) to the timers"], BLUE)

box("RB", 80, 415, 590, 470,
    "KL_aecp_response_builder   — READER 1", [], GREEN, "container")

box("TBL", 105, 470, 540, 110, "THE REGISTRATION TABLE  (:1682-1685)",
    ["unsol_valid_r [0:SLOTS-1]        1 bit    — slot occupied",
     "unsol_eid_r   [0:SLOTS-1]       64 bits   — controller entity_id",
     "unsol_mac_r   [0:SLOTS-1]       48 bits   — controller MAC",
     "unsol_seq_r   [0:SLOTS-1]       16 bits   — per-slot sequence_id",
     "                              = 129 bits of storage PER SLOT"], GREEN)

box("PEND", 105, 600, 540, 200, "ELEVEN PENDING CLASSES  (:1686-1711 — numbering runs to 12, no pend2)",
    ["bit-per-slot vectors  [SLOTS-1:0]:",
     "  unsol_pend_r    stream-info      unsol_pend8_r   GET_AS_PATH",
     "  unsol_pend3_r   AVB_INTERFACE    unsol_pend9_r   CLOCK_DOMAIN",
     "  unsol_pend4_r   SET-resp replay  unsol_pend11_r  CRF media clock",
     "  unsol_pend7_r   GET_AVB_INFO     unsol_pend12_r  LOCK_ENTITY",
     "WIDER, one word per slot  [0:SLOTS-1]:",
     "  unsol_pend5_r  [TKD_MAX_C-1:0]   per talker descriptor",
     "  unsol_pend6_r  [1:0]",
     "  unsol_pend10_r [RXD_MAX_C-1:0]   per rx descriptor",
     "",
     "THIS is the LUT cost: every class needs its OWN slot walk"], GREEN)

box("CA", 105, 815, 540, 55, "CONTROLLER-AVAILABLE PROBE  (gh #59, :1743-1779)",
    ["ca_owed_r[SLOTS-1:0] · ca_probe_idx_r · w_ca_reply_match[SLOTS-1:0]"], GREEN)

box("TMR", 80, 915, 590, 175,
    "KL_aecp_timers   — READER 2   (:76-101)", [], ORANGE, "container")
box("MON", 105, 970, 540, 105, "ONE MONITOR TIMER PER SLOT",
    ["parameter MON_SLOTS_P = 4          (must equal the builder's, forever)",
     "MONITOR_MIN_MS_P = 30 000  +  LFSR fold of MONITOR_RND_MS_P = 30 000",
     "in : mon_arm_i / mon_heard_i / mon_clear_i   [MON_SLOTS_P-1:0]",
     "out: mon_expired_o                           [MON_SLOTS_P-1:0]"], ORANGE)

box("HAZ", 80, 1120, 590, 145, "THE HAZARD THE PACKAGE COMMENT NAMES",
    ["aecp_pkg.sv:185-190 — \"gh #59 gave the table a SECOND reader:",
     "KL_aecp_timers carries one monitor timer per slot and both",
     "modules' port widths have to be the same number, forever.",
     "A copied 4 is exactly the defect RECURRING_DEFECT_PATTERNS.md",
     "is about — it agrees on day one and diverges in silence.\"",
     "",
     "=> change the localparam, never a literal. Both readers move."], RED, "note")

box("COST", 80, 1295, 590, 130, "WHAT SHRINKING IT BUYS  (Vivado OOC, AreaOptimized_high)",
    ["4 → 2 slots :  8583 → 7834 LUT   = −749 (−8.7 %), −296 FF",
     "               ≈ −523 LUT in context  = 2.0 % of the Milan fabric",
     "4 → 1 slot  :  8583 → 7574 LUT   = −1009,  ≈ −704 in context",
     "               …but a SECOND controller is then refused registration",
     "≈ 336 LUT per slot at the top of the range"], WHITE, "note")

edge([(375, 237), (375, 265)])
edge([(375, 383), (375, 415)])
edge([(375, 885), (375, 915)], "mon_* rails", "#EF6C00")


# ======================================================================== #
# PANEL 2 — DATA FLOW                                                       #
# ======================================================================== #
box("P2", 745, 120, 745, 1330,
    "2 · DATA FLOW — registration in, notification out", [], WHITE, "container")

box("ING", 770, 180, 695, 70, "AECP ingress  →  validator  →  common parser",
    ["controller frame: message_type, target_entity_id, controller_entity_id,",
     "sequence_id, command_type, + source MAC lifted off the wire"], GREY)

box("REG", 770, 285, 335, 130, "REGISTER_UNSOLICITED_NOTIFICATION",
    ["1. scan unsol_valid_r for a FREE slot",
     "2. if none free → status NO_RESOURCES",
     "3. write eid / mac / seq=0, valid←1",
     "   (a DEDUP re-register PRESERVES seq)",
     "4. pulse mon_arm_p_o[slot]",
     "   (slot born: monitor starts)"], BLUE)

box("DEREG", 1130, 285, 335, 130, "DEREGISTER_UNSOLICITED_NOTIFICATION",
    ["1. match unsol_eid_r[i] == controller",
     "2. valid ← 0",
     "3. pulse mon_clear_p_o[slot]",
     "   (slot died: monitor stops)",
     "4. all pend bits for that slot cleared"], BLUE)

box("TRIG", 770, 460, 695, 140, "STATE CHANGE  →  SET THE PEND BIT FOR EVERY REGISTERED SLOT",
    ["a SET_* write-back, a stream bind, a GM change, a clock-domain change,",
     "a media-clock event …  each owns ONE of the eleven pend classes and arms",
     "it per slot, gated on registration (:2661):",
     "      for (s) if (unsol_valid_r[s]) unsol_pendN_r[s] <= 1'b1;",
     "u=1 in the emitted AECPDU marks it unsolicited; a no-change gate stops",
     "an event that did not actually move a field from waking the bus"], BLUE)

box("WALK", 770, 615, 695, 158, "THE EMISSION WALK — the part that costs LUTs",
    ["ONE priority encode per class, lowest slot wins (:1814-1816):",
     "      if (unsol_pendN_r[s]) w_unsol_pushN_idx = 2'(s);",
     "then read back unsol_eid_r / unsol_mac_r / unsol_seq_r at that index,",
     "build the AECPDU, emit, seq++, clear the bit (:2957).",
     "",
     "11 classes × SLOTS priority-encodes + 11 × SLOTS-wide read muxes over a",
     "129-bit record.  Halving SLOTS halves BOTH — hence the −8.7 %.",
     "NOTE the 2'(s) — the index width is a LITERAL, see panel 3 note 1."], PURPLE)

box("BLD", 770, 788, 695, 95, "RESPONSE SCRATCH  →  segment serialiser",
    ["const_q 80-byte scratch (:945) · seg_kind/seg_addr/seg_len engine",
     "same emitter the solicited responses use — unsolicited is a SOURCE of",
     "work for it, not a second datapath"], PURPLE)

box("ARB", 770, 898, 695, 78, "low-rate TX arbiter chain  →  MAC TX  →  PHY",
    ["pairwise adp_tx_arbiter tree; one WHOLE frame per grant",
     "unicast to unsol_mac_r[slot] — not multicast"], GREY)

box("PROBE", 770, 991, 695, 165, "gh #59 — SHEDDING A DEAD CONTROLLER",
    ["mon_expired_o[slot]  →  ca_owed_r[slot]",
     "     ↓",
     "emit CONTROLLER_AVAILABLE to that slot's controller (unicast)",
     "     ↓",
     "reply matched by ENTITY_ID, never by MAC — a controller that moved",
     "MAC still proves itself alive (:1872).  unsol_mac_r is CARRIED, never",
     "compared: it is the unicast destination and nothing else.",
     "   yes → mon_heard_p_o[slot]  (reload, slot survives)",
     "   no  → probe again, then mon_clear_p_o[slot] + valid←0  (slot freed)",
     "",
     "This is WHY the table has two readers, and why the widths must agree."], ORANGE)

box("SWEEP", 770, 1171, 695, 92, "TABLE FULL → THE NO_RESOURCES SWEEP  (Milan 5.4.2.21, :327/:2882)",
    ["mon_force_exp_p_o force-expires the monitors so silent controllers are",
     "probed and shed instead of a live controller being refused forever.",
     "ONE probe outstanding at a time (ca_inflight_r) — two silent controllers",
     "serialise ~500 ms apart, so a sweep never puts four probes on the wire."], ORANGE)

box("N2", 770, 1278, 695, 112, "WHY 4 AND NOT 2",
    ["aecp_pkg.sv:183 declares MAX_UNSOLICITED_CTLR_C = 16 — the reference",
     "bound, which dimensions NOTHING. We implement 4 of a possible 16.",
     "is how many CONTROLLERS touch this entity at once: Hive + la_avdecc + a",
     "test harness is three. Two is a real constraint, four is comfortable —",
     "a PRODUCT decision, not a standards one. Argue it before cutting it."], WHITE, "note")

edge([(1117, 250), (1117, 285)])
edge([(937, 415), (937, 460)], "slot table write", "#1565C0")
edge([(1297, 415), (1297, 440), (1000, 440), (1000, 460)], "", "#1565C0")
edge([(1117, 600), (1117, 615)], "pend bits set", "#6A1B9A")
edge([(1117, 773), (1117, 788)])
edge([(1117, 883), (1117, 898)])
edge([(1117, 976), (1117, 991)], "", "#EF6C00", True)
edge([(1117, 1156), (1117, 1171)], "", "#EF6C00", True)


# ======================================================================== #
# PANEL 3 — STATE MACHINES                                                  #
# ======================================================================== #
box("P3", 1515, 120, 655, 1330,
    "3 · STATE — one slot's lifecycle, ×4 independently", [], WHITE, "container")

box("SM1", 1540, 175, 605, 40, "SLOT LIFECYCLE   (per slot i, in the builder)",
    [], GOLD, "container")

box("S_FREE", 1600, 235, 220, 62, "FREE",
    ["unsol_valid_r[i] = 0", "monitor stopped"], GOLD)
box("S_REG", 1600, 360, 220, 76, "REGISTERED",
    ["valid=1, eid/mac held", "seq counting", "monitor armed"], GOLD)
box("S_PEND", 1600, 500, 220, 76, "NOTIFY OWED",
    ["≥1 of 11 pend bits set", "for this slot"], GOLD)
box("S_PROBE", 1880, 430, 235, 76, "PROBE OWED",
    ["ca_owed_r[i] = 1", "CONTROLLER_AVAILABLE", "in flight"], ORANGE)

edge([(1710, 297), (1710, 360)], "REGISTER (free slot)", "#F9A825",
     lab_at=(1560, 332))
edge([(1710, 436), (1710, 500)], "state change → pend", "#6A1B9A",
     lab_at=(1545, 470))
edge([(1600, 538), (1548, 538), (1548, 398), (1600, 398)],
     "emitted → bit cleared", "#6A1B9A", lab_at=(1545, 600))
edge([(1820, 398), (1880, 430)], "mon_expired", "#EF6C00", lab_at=(1826, 392))
edge([(1997, 506), (1997, 560), (1710, 560), (1710, 576)],
     "reply → mon_heard (reload)", "#2E7D32", lab_at=(1770, 600))
edge([(2115, 468), (2150, 468), (2150, 266), (1820, 266)],
     "no reply → mon_clear, valid←0", "#C62828", lab_at=(1830, 240))
edge([(1600, 266), (1552, 266), (1552, 232)], "DEREGISTER", "#C62828",
     lab_at=(1545, 222))

box("SM2", 1540, 660, 605, 40, "MONITOR TIMER   (per slot i, KL_aecp_timers)",
    [], ORANGE, "container")
box("T_IDLE", 1570, 720, 175, 62, "IDLE", ["not counting"], ORANGE)
box("T_RUN", 1810, 720, 175, 76, "COUNTING",
    ["MIN 30 000 ms", "+ LFSR fold of", "RND 30 000 ms"], ORANGE)

edge([(1745, 751), (1810, 751)], "mon_arm_i[i]", "#EF6C00", lab_at=(1735, 742))
edge([(1897, 796), (1897, 830), (1657, 830), (1657, 782)],
     "mon_heard_i[i] → reload", "#2E7D32", lab_at=(1680, 850))
edge([(1985, 751), (2060, 751), (2060, 700)], "mon_expired_o[i]", "#EF6C00",
     lab_at=(1995, 742))

box("N3", 1540, 890, 605, 200, "READING THIS DIAGRAM",
    ["Everything in panel 1's green and orange blocks is ×4. Everything in",
     "panel 3 is ONE slot's behaviour, running four times independently and",
     "concurrently — there is no arbitration BETWEEN slots except in the",
     "emission walk, which serialises them onto one TX arbiter grant.",
     "",
     "So the 4 costs area in two different ways:",
     "  · STORAGE   129 bits × 4, plus 11 pend classes × 4",
     "  · SELECTION 11 priority encodes and 11 read muxes, each ×4 wide",
     "The second is the larger, and it is why the saving is super-linear in",
     "the pend-class count rather than just in the slot count."], WHITE, "note")

box("N4", 1540, 1120, 605, 305, "IF YOU CHANGE IT",
    ["1. Edit ONLY aecp_pkg.sv:190. Both readers derive from it; a literal",
     "   4 anywhere else is the divergence the package comment warns of.",
     "   (A related live hazard: the 2-bit slot INDEX width is restated as a",
     "    literal 2 in 27 places instead of $clog2(SLOTS) — fix that first,",
     "    or a slot-count change silently truncates the index.)",
     "",
     "2. Suites that would catch a mistake:",
     "   tb/verilator/aecp        registration / dereference / NO_RESOURCES",
     "   tb/verilator/tsn_fuzz    fuzz_aecp field grading",
     "   tests/  @notifications   the unsolicited BDD tier",
     "",
     "3. It is ABI-visible: a controller that registers and is refused sees",
     "   a different status. Milan es-1.1 does not test the slot count, but",
     "   a multi-controller bench does.",
     "",
     "4. Re-measure with scripts/area_baseline.py --compare against a routed",
     "   build. The OOC figure above is the response builder ALONE."], WHITE, "note")


# ======================================================================== #
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
    for kind_pass in ("container", "box", "note"):
        for bid, (x, y, w, h, title, sub, (fill, stroke), kind) in B.items():
            if kind != kind_pass:
                continue
            dash = ' stroke-dasharray="6,4"' if kind == "note" else ""
            op = ' fill-opacity="0.45"' if kind == "container" else ""
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}{op}/>')
            if kind == "container":
                o.append(f'<text x="{x+18}" y="{y+28}" font-size="16.5" '
                         f'font-weight="bold" fill="{stroke}">{esc(title)}</text>')
                for j, sl in enumerate(sub):
                    o.append(f'<text x="{x+18}" y="{y+50+j*17}" font-size="12.5" '
                             f'fill="#5D4037">{esc(sl)}</text>')
            else:
                o.append(f'<text x="{x+12}" y="{y+22}" font-size="13.5" '
                         f'font-weight="bold" fill="#212121">{esc(title)}</text>')
                for j, sl in enumerate(sub):
                    o.append(f'<text x="{x+12}" y="{y+40+j*15}" font-size="11.5" '
                             f'fill="#37474F">{esc(sl)}</text>')
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
    o.append(f'<text x="40" y="{H-30}" font-size="12.5" fill="#546E7A">'
             + esc("Generated by docs/diagrams/unsol_slots.gen.py — edit the "
                   "generator (or the .drawio), never the render. Source of "
                   "truth: hdl/ieee17221/aecp/aecp_pkg.sv:190, "
                   "KL_aecp_response_builder.sv:1682-1779, KL_aecp_timers.sv:76-101")
             + '</text>')
    o.append('</svg>')
    return "\n".join(o)


def drawio():
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    n = [2]

    def vtx(label, x, y, w, h, style):
        i = n[0]; n[0] += 1
        cells.append(f'<mxCell id="n{i}" value="{esc(label)}" style="{style}" '
                     f'vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')

    def ept(pts, label, col, dashed):
        i = n[0]; n[0] += 1
        d = 1 if dashed else 0
        pt = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts[1:-1])
        cells.append(
            f'<mxCell id="e{i}" value="{esc(label)}" '
            f'style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
            f'strokeColor={col};dashed={d};endArrow=block;fontSize=11" '
            f'edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{pts[0][0]}" y="{pts[0][1]}" as="sourcePoint"/>'
            f'<mxPoint x="{pts[-1][0]}" y="{pts[-1][1]}" as="targetPoint"/>'
            f'<Array as="points">{pt}</Array></mxGeometry></mxCell>')

    vtx(TITLE, 40, 20, 1600, 34,
        "text;html=1;fontSize=26;fontStyle=1;fontColor=#263238;align=left;verticalAlign=middle")
    vtx(SUB, 40, 60, 2000, 24,
        "text;html=1;fontSize=13;fontColor=#546E7A;align=left;verticalAlign=middle")

    for kind_pass in ("container", "box", "note"):
        for bid, (x, y, w, h, title, sub, (fill, stroke), kind) in B.items():
            if kind != kind_pass:
                continue
            body = title if not sub else title + "\n" + "\n".join(sub)
            dash = "dashed=1;" if kind == "note" else "dashed=0;"
            op = "opacity=55;" if kind == "container" else ""
            va = "top" if kind == "container" else "top"
            vtx(body, x, y, w, h,
                f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};"
                f"strokeColor={stroke};{dash}{op}align=left;verticalAlign={va};"
                f"spacing=8;fontSize=11;")

    for pts, label, col, dashed, arrow, lab_at in E:
        ept(pts, label, col, dashed)

    return ('<mxfile host="app.diagrams.net">'
            f'<diagram name="AECP_UNSOL_SLOTS_C">'
            f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" '
            f'guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            f'page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
            f'math="0" shadow="0"><root>' + "".join(cells) +
            '</root></mxGraphModel></diagram></mxfile>')


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "unsol_slots"
    with open(base + ".svg", "w") as f:
        f.write(svg())
    with open(base + ".drawio", "w") as f:
        f.write(drawio())
    print(f"wrote {base}.svg and {base}.drawio")
