#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the egress queue map (strict-priority ladder + CBS shaping + the
classification paths that feed it) as both an editable .drawio and a rendered
.svg.  Style follows DOC_MAP.gen.py / SYSTEM_DOMAIN_MAP.gen.py (pastel fill +
darker stroke, rounded boxes).

**NOTHING HERE IS TRANSCRIBED.** Every queue, its name, its purpose line, its
reset idleSlope, its hi/lo credit, the arbitration direction and the reset
shaping mask are PARSED out of the RTL that defines them:

    hdl/common/ethernet_packet_pkg.sv   NUMBER_OF_QUEUES, network_priority_t,
                                        IDLE_SLOPE_1G / IDLE_SLOPE_100M,
                                        priority_encode (scan direction)
    hdl/common/csr/milan_csr.sv         CBS_HI_RST / CBS_LO_RST / CBS_EN_RST,
                                        cls_tcq reset (TC -> queue map)
    hdl/ieee8021q/ts/traffic_class_map.sv   the reserved control DMAC table

so a change to the queue count or the map re-renders correctly instead of
turning this picture into a lie.  The parse is STRICT: a shape it does not
recognise raises, rather than silently emitting a stale diagram.

The one thing not literally in a constant is *which* queues CBS may shape.
That is REQ-CBS-02 ("CBS shapes reserved SR classes only, never best effort"),
so the rule applied here is: **the SR_* enum members are the CBS-capable set**,
and `CBS_EN_RST` (all zero today) says how many of them are shaped at reset.
Both are stated on the drawing rather than assumed by the reader.

Usage:
    python3 docs/diagrams/egress_queue_map.gen.py docs/diagrams/egress_queue_map
    rsvg-convert -w 2000 docs/diagrams/egress_queue_map.svg \
        -o docs/diagrams/egress_queue_map.png
"""
import html
import re
import sys
from pathlib import Path
from typing import NamedTuple, NoReturn

REPO = Path(__file__).resolve().parents[2]
PKG = REPO / "hdl" / "common" / "ethernet_packet_pkg.sv"
CSR = REPO / "hdl" / "common" / "csr" / "milan_csr.sv"
TCM = REPO / "hdl" / "ieee8021q" / "ts" / "traffic_class_map.sv"


class Box(NamedTuple):
    """One drawio vertex's geometry, in diagram user units."""

    x: float
    y: float
    w: float
    h: float


def esc(s: object) -> str:
    """XML-escape a value for SVG text AND for a drawio `value=` attribute."""
    return html.escape(str(s), quote=True)


def die(what: str) -> NoReturn:
    """Refuse to draw: the RTL moved, and a stale picture is worse than none."""
    raise SystemExit(f"egress_queue_map.gen.py: cannot parse {what} — the RTL "
                     f"shape changed; fix this generator, do not hand-draw.")


# ---------------------------------------------------------------------------
# parse the RTL
# ---------------------------------------------------------------------------

def _int(tok):
    return int(tok.replace("_", ""))


pkg = PKG.read_text(encoding="utf-8")
csr = CSR.read_text(encoding="utf-8")
tcm = TCM.read_text(encoding="utf-8")

m = re.search(r"parameter\s+int\s+NUMBER_OF_QUEUES\s*=\s*(\d+)\s*;", pkg)
if not m:
    die("NUMBER_OF_QUEUES")
NQ = int(m.group(1))

# network_priority_t: enum member -> (index, purpose from its //!< comment)
m = re.search(r"typedef\s+enum[^{]*\{(.*?)\}\s*network_priority_t\s*;", pkg, re.S)
if not m:
    die("network_priority_t")
QUEUES = {}                                   # index -> (enum name, purpose)
for line in m.group(1).splitlines():
    e = re.match(r"\s*(\w+)\s*=\s*\d+'d(\d+)\s*,?\s*(?://!<\s*(.*?)\s*)?$", line)
    if not e:
        continue
    name, idx, doc = e.group(1), int(e.group(2)), (e.group(3) or "")
    # the //!< comment reads "q5: SR class A ... (highest)" — drop the "qN:" tag,
    # it is redundant next to the index we already have.
    doc = re.sub(r"^q\d+\s*:\s*", "", doc)
    QUEUES[idx] = (name, doc)
if sorted(QUEUES) != list(range(NQ)):
    die(f"network_priority_t members ({sorted(QUEUES)}) vs NUMBER_OF_QUEUES={NQ}")

# arbitration direction, straight out of priority_encode's loop
m = re.search(r"function\s+automatic\s+int\s+priority_encode.*?for\s*\(\s*int\s+i\s*=\s*"
              r"(.*?)\s*;.*?;\s*i\s*(--|\+\+)\s*\)", pkg, re.S)
if not m:
    die("priority_encode scan direction")
TOP_WINS = m.group(2) == "--"

# slope arrays, indexed by queue
def slope_array(name: str) -> list[int]:
    """One `[0:NUMBER_OF_QUEUES-1]` slope parameter, proven NQ entries long."""
    m = re.search(rf"parameter\s+int\s+{name}\s*\[0:NUMBER_OF_QUEUES-1\]\s*=\s*'\{{(.*?)\}}\s*;",
                  pkg, re.S)
    if not m:
        die(name)
    vals = [_int(t) for t in re.findall(r"([\d_]+)\s*(?:,|//|$)", m.group(1))]
    vals = vals[:NQ]
    if len(vals) != NQ:
        die(f"{name} has {len(vals)} entries, expected {NQ}")
    return vals

IDLE_1G = slope_array("IDLE_SLOPE_1G")
IDLE_100M = slope_array("IDLE_SLOPE_100M")

m = re.search(r"parameter\s+int\s+MAX_FRAME_SIZE\s*=\s*(\d+)\s*;", pkg)
MAX_FRAME = int(m.group(1)) if m else die("MAX_FRAME_SIZE")

# CSR reset state: hi/lo credit, the shaped-enable mask, the TC -> queue map
def csr_array(name: str) -> list[int]:
    """One per-queue CSR reset array, cut to NQ entries and proven that long."""
    m = re.search(rf"localparam\s+int\s+{name}\s*\[0:\d+\]\s*=\s*'\{{(.*?)\}}\s*;", csr, re.S)
    if not m:
        die(name)
    vals = [_int(t) for t in re.findall(r"(-?[\d_]+)", m.group(1))][:NQ]
    if len(vals) != NQ:
        die(f"{name} has {len(vals)} usable entries, expected {NQ}")
    return vals

HI_RST = csr_array("CBS_HI_RST")
LO_RST = csr_array("CBS_LO_RST")

m = re.search(r"localparam\s+bit\s*\[\d+:\d+\]\s+CBS_EN_RST\s*=\s*\d+'b([01]+)\s*;", csr)
if not m:
    die("CBS_EN_RST")
EN_RST = [int(b) for b in reversed(m.group(1))][:NQ]      # index 0 = q0

m = re.search(r"cls_tcq\s*<=\s*32'h([0-9A-Fa-f]+)\s*;", csr)
if not m:
    die("cls_tcq reset value")
TCQ_RST = int(m.group(1), 16)
QBITS = max(1, (NQ - 1).bit_length())                     # $clog2 of the count
TC_MAP = [(TCQ_RST >> (tc * QBITS)) & ((1 << QBITS) - 1) for tc in range(8)]

# reserved control destination addresses, with the queue each row's comment names
m = re.search(r"CTRL_DMAC_TBL\s*\[CTRL_DMAC_N\]\s*=\s*'\{(.*?)\}\s*;", tcm, re.S)
if not m:
    die("CTRL_DMAC_TBL")
CTRL_ROWS = []
for line in m.group(1).splitlines():
    e = re.match(r"\s*(\w+)\s*,?\s*//!<\s*(\S+)\s+(.*?)\s*$", line)
    if e:
        # the RTL comment marks the shared address with doxygen emphasis; drop it
        CTRL_ROWS.append((e.group(2), e.group(3).replace('*', '')))
if not CTRL_ROWS:
    die("CTRL_DMAC_TBL rows")

# CBS-capable set: REQ-CBS-02 — the SR classes, and only those.
SHAPED = [q for q in range(NQ) if QUEUES[q][0].startswith("SR")]

# ---------------------------------------------------------------------------
# palette (fill, stroke) — DOC_MAP.gen.py family
# ---------------------------------------------------------------------------
GREEN = ("#E8F5E9", "#2E7D32")     # CBS-shaped SR classes
ORANGE = ("#FFF3E0", "#EF6C00")    # time-critical strict priority (gPTP)
BLUE = ("#E3F2FD", "#1565C0")      # control plane
GREY = ("#ECEFF1", "#455A64")      # spare / best effort
PURPLE = ("#F3E5F5", "#6A1B9A")    # classification tables
GOLD = ("#FFF8E1", "#F9A825")      # the arbiter


def qcolour(q: int) -> tuple[str, str]:
    """The (fill, stroke) a queue earns from its enum name: SR, gPTP, control, spare."""
    name = QUEUES[q][0]
    if name.startswith("SR"):
        return GREEN
    if "GPTP" in name:
        return ORANGE
    if "CONTROL" in name:
        return BLUE
    return GREY


def mbps(bps: int) -> str:
    """A slope in Mb/s, the unit 802.1Qav states idleSlope in."""
    return f"{bps / 1e6:g} Mb/s"


def pct(bps: int, port: int = 1_000_000_000) -> str:
    """A slope as its share of the port rate, which is what compares across queues."""
    return f"{100.0 * bps / port:.4g} %"


# geometry — everything derives from NQ so the picture reflows on a queue-count
# change instead of overlapping.
QW, QH, QGAP = 560, 100, 16
LX, LY = 700, 200                                     # ladder origin
LADDER_H = NQ * QH + (NQ - 1) * QGAP
BX = LX + QW + 34                                     # right column (CBS bracket)
BW = 340
W = BX + 26 + BW + 40
H = LY + LADDER_H + 176


def qy(q: int) -> int:
    """Top of queue q's box. Highest priority is drawn topmost."""
    rank = (NQ - 1 - q) if TOP_WINS else q
    return LY + rank * (QH + QGAP)


def _svg_titles():
    """The heading, the provenance note and which index wins the arbitration."""
    o = []
    o.append('<text x="40" y="52" font-size="30" font-weight="bold" fill="#263238">'
             f'Egress queue map - {NQ} traffic classes, 802.1Q order</text>')
    o.append('<text x="40" y="82" font-size="15" fill="#546E7A">GENERATED from '
             'hdl/common/ethernet_packet_pkg.sv (queue count, enum, slopes), '
             'hdl/common/csr/milan_csr.sv (reset credit + shaping mask + TC map) '
             'and hdl/ieee8021q/ts/traffic_class_map.sv (control addresses).</text>')
    o.append('<text x="40" y="106" font-size="15" fill="#546E7A">'
             f'{"HIGHER index = HIGHER priority" if TOP_WINS else "LOWER index = HIGHER priority"}'
             f' - priority_encode scans {"from the top index down" if TOP_WINS else "from index 0 up"},'
             f' so q{NQ-1 if TOP_WINS else 0} is granted first.</text>')
    return o


def _svg_ladder():
    """The strict-priority ladder: one box per queue, with its shaping badge."""
    o = []
    o.append(f'<text x="{LX}" y="{LY-22}" font-size="17" font-weight="bold" fill="#78909C">'
             f'STRICT-PRIORITY LADDER (the arbiter grants top-down)</text>')
    for q in range(NQ):
        fill, stroke = qcolour(q)
        y = qy(q)
        o.append(f'<rect x="{LX}" y="{y}" width="{QW}" height="{QH}" rx="9" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"/>')
        name, doc = QUEUES[q]
        o.append(f'<text x="{LX+14}" y="{y+27}" font-size="17" font-weight="bold" '
                 f'fill="#212121">q{q}  {esc(name)}</text>')
        o.append(f'<text x="{LX+14}" y="{y+48}" font-size="12.5" fill="#37474F">'
                 f'{esc(doc[:60])}</text>')
        o.append(f'<text x="{LX+14}" y="{y+70}" font-size="12" fill="#37474F">'
                 f'idleSlope {esc(mbps(IDLE_1G[q]))} ({esc(pct(IDLE_1G[q]))} of 1G) '
                 f'| {esc(mbps(IDLE_100M[q]))} @100M</text>')
        o.append(f'<text x="{LX+14}" y="{y+88}" font-size="12" fill="#607D8B">'
                 f'reset hiCredit {HI_RST[q]} B / loCredit {LO_RST[q]} B</text>')
        # shaping badge, right-hand gutter
        if q in SHAPED:
            badge, bc = ("CBS-capable", "#2E7D32")
        else:
            badge, bc = ("strict priority", "#78909C")
        o.append(f'<rect x="{LX+QW-150}" y="{y+QH/2-13}" width="138" height="26" rx="13" '
                 f'fill="#FFFFFF" stroke="{bc}" stroke-width="1.6"/>')
        o.append(f'<text x="{LX+QW-81}" y="{y+QH/2+5}" font-size="12" font-weight="bold" '
                 f'fill="{bc}" text-anchor="middle">{esc(badge)}</text>')
        # priority rank marker
        rank = (NQ - q) if TOP_WINS else (q + 1)
        o.append(f'<text x="{LX-14}" y="{y+QH/2+6}" font-size="15" font-weight="bold" '
                 f'fill="#90A4AE" text-anchor="end">#{rank}</text>')
    return o


def _svg_cbs_bracket():
    """The 802.1Qav panel bracketing the shaped-capable band, when there is one."""
    o = []
    if SHAPED:
        top = min(qy(q) for q in SHAPED)
        bot = max(qy(q) for q in SHAPED) + QH
        bx = BX
        o.append(f'<path d="M{bx},{top} L{bx+16},{top} L{bx+16},{bot} L{bx},{bot}" '
                 f'fill="none" stroke="#2E7D32" stroke-width="2.4"/>')
        o.append(f'<rect x="{bx+26}" y="{top}" width="{BW}" height="{bot-top}" rx="9" '
                 f'fill="{GREEN[0]}" stroke="{GREEN[1]}" stroke-width="2"/>')
        o.append(f'<text x="{bx+42}" y="{top+30}" font-size="15" font-weight="bold" '
                 f'fill="#1B5E20">802.1Qav credit-based shaper</text>')
        lines = [
            "REQ-CBS-02: CBS shapes reserved SR classes",
            "only - never best effort.",
            f"Shaped set at reset: CBS_EN_RST = "
            f"{'none' if not any(EN_RST) else ','.join('q%d' % q for q in range(NQ) if EN_RST[q])}",
            "-> every queue is strict priority until",
            "software sets CBS_CTRL[0] for a queue.",
            f"hi/loCredit derived at MAX_FRAME_SIZE = {MAX_FRAME} B.",
        ]
        for i, s in enumerate(lines):
            o.append(f'<text x="{bx+42}" y="{top+56+i*19}" font-size="12" fill="#1B5E20">'
                     f'{esc(s)}</text>')
    return o


def _svg_priority_note():
    """The red panel: why gPTP sits below the shaped classes."""
    o = []
    cy = LY + LADDER_H + 34
    o.append(f'<rect x="{LX}" y="{cy}" width="{BX+26+BW-LX}" height="106" rx="9" '
             f'fill="#FFEBEE" stroke="#C62828" stroke-width="2"/>')
    o.append(f'<text x="{LX+16}" y="{cy+26}" font-size="14.5" font-weight="bold" '
             f'fill="#B71C1C">Why gPTP sits BELOW the shaped classes - correctness, '
             f'not preference</text>')
    for i, s in enumerate([
        "802.1Q-2018 8.6.8.2 assumes the shaped queues are the TOP of the strict-priority order. A",
        "strict-priority queue above them preempts a class-A frame whose credit was already earned, so the",
        "credit accounting no longer bounds class-A latency. gPTP tolerates the demotion because every event",
        "message is hardware-stamped at the egress SFD - queueing moves WHEN it leaves, never the value it "
        "carries."]):
        o.append(f'<text x="{LX+16}" y="{cy+50+i*17}" font-size="11.8" fill="#B71C1C">'
                 f'{esc(s)}</text>')
    return o


def _svg_classification():
    """The left column: how a tagged, control or unmatched frame picks its queue."""
    o = []
    o.append(f'<text x="40" y="{LY-22}" font-size="17" font-weight="bold" fill="#78909C">'
             f'CLASSIFICATION - how a frame picks its queue</text>')

    # tagged path
    ty = LY
    o.append(f'<rect x="40" y="{ty}" width="600" height="196" rx="9" fill="{PURPLE[0]}" '
             f'stroke="{PURPLE[1]}" stroke-width="2"/>')
    o.append(f'<text x="56" y="{ty+26}" font-size="15" font-weight="bold" fill="#4A148C">'
             f'TAGGED frame - 802.1Q decides (three programmable tables)</text>')
    for i, s in enumerate([
            "eff_pcp = vlan_valid ? frame PCP : CLS_DEFAULT_PCP   (0x304)",
            "regen   = CLS_PRIO_REGEN[eff_pcp]                    (0x30C)",
            "tc      = CLS_PCP_TC_MAP[regen]                      (0x308)",
            "queue   = CLS_TC_QUEUE_MAP[tc]                       (0x310)"]):
        o.append(f'<text x="56" y="{ty+50+i*17}" font-size="12" font-family="monospace" '
                 f'fill="#4A148C">{esc(s)}</text>')
    o.append(f'<text x="56" y="{ty+138}" font-size="12" fill="#4A148C">'
             f'reset CLS_TC_QUEUE_MAP = 0x{TCQ_RST:08X}, {QBITS} bits per traffic class:</text>')
    cellw = 66
    for tc in range(8):
        x = 56 + tc * cellw
        tgt = TC_MAP[tc]
        oor = tgt >= NQ
        fill = "#FFCDD2" if oor else qcolour(tgt)[0]
        o.append(f'<rect x="{x}" y="{ty+148}" width="{cellw-6}" height="34" rx="5" '
                 f'fill="{fill}" stroke="{PURPLE[1]}" stroke-width="1.3"/>')
        o.append(f'<text x="{x+(cellw-6)/2}" y="{ty+162}" font-size="11" fill="#37474F" '
                 f'text-anchor="middle">TC{tc}</text>')
        o.append(f'<text x="{x+(cellw-6)/2}" y="{ty+177}" font-size="12.5" font-weight="bold" '
                 f'fill="#212121" text-anchor="middle">'
                 f'{"clamp q0" if oor else "q%d" % tgt}</text>')

    # untagged control path
    uy = ty + 224
    rows_h = 26 + 20 * len(CTRL_ROWS) + 92
    o.append(f'<rect x="40" y="{uy}" width="600" height="{rows_h}" rx="9" fill="{BLUE[0]}" '
             f'stroke="{BLUE[1]}" stroke-width="2"/>')
    o.append(f'<text x="56" y="{uy+26}" font-size="15" font-weight="bold" fill="#0D47A1">'
             f'UNTAGGED control - no PCP exists, so the DESTINATION MAC decides</text>')
    for i, (addr, what) in enumerate(CTRL_ROWS):
        o.append(f'<text x="56" y="{uy+50+i*20}" font-size="12" font-family="monospace" '
                 f'fill="#0D47A1">{esc(addr)}  {esc(what)}</text>')
    for i, s in enumerate([
            "A row hit needs NO EtherType (the next protocol through this door is RSTP,",
            "which has none). The EtherType refines exactly ONE address: at 01-80-C2-00-00-0E,",
            "0x88F7 leaves for gPTP and everything else there - MSRP - stays on control."]):
        o.append(f'<text x="56" y="{uy+60+len(CTRL_ROWS)*20+i*18}" font-size="11.8" '
                 f'fill="#0D47A1">{esc(s)}</text>')

    # fallthrough
    fy = uy + rows_h + 22
    o.append(f'<rect x="40" y="{fy}" width="600" height="58" rx="9" fill="{GREY[0]}" '
             f'stroke="{GREY[1]}" stroke-width="2"/>')
    o.append(f'<text x="56" y="{fy+25}" font-size="14" font-weight="bold" fill="#263238">'
             f'FALLTHROUGH - everything else, and any out-of-range map entry</text>')
    o.append(f'<text x="56" y="{fy+45}" font-size="12" fill="#37474F">'
             f'clamped to q0: an unmapped class rides best effort (observable) rather than '
             f'being silently dropped.</text>')

    # arrows into the ladder
    for y0 in (ty + 98, uy + rows_h / 2, fy + 29):
        o.append(f'<path d="M640,{y0:.0f} L{LX-56},{y0:.0f}" fill="none" stroke="#546E7A" '
                 f'stroke-width="2.2" marker-end="url(#arr)"/>')
    return o


def _svg_arbiter():
    """The arbiter box under the CBS bracket: what grants the next frame."""
    o = []
    ay = (max(qy(q) for q in SHAPED) + QH + 26) if SHAPED else LY
    o.append(f'<rect x="{BX+26}" y="{ay}" width="{BW}" height="104" rx="9" fill="{GOLD[0]}" '
             f'stroke="{GOLD[1]}" stroke-width="2"/>')
    o.append(f'<text x="{BX+42}" y="{ay+26}" font-size="15" font-weight="bold" '
             f'fill="#795548">arbiter -&gt; MAC TX</text>')
    for i, s in enumerate([
            "ethernet_packet_pkg::priority_encode",
            f"scans {'q%d down to q0' % (NQ-1) if TOP_WINS else 'q0 up to q%d' % (NQ-1)},",
            "grants the first requester whose CBS",
            "gate allows it (unshaped = always)."]):
        o.append(f'<text x="{BX+42}" y="{ay+50+i*17}" font-size="12" fill="#795548">'
                 f'{esc(s)}</text>')
    return o


def svg() -> str:
    """The whole rendered map, in the order the reader meets it."""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>',
         '<defs><marker id="arr" markerWidth="12" markerHeight="12" refX="7" refY="4" '
         'orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#546E7A"/></marker></defs>']
    o += _svg_titles()
    o += _svg_ladder()
    o += _svg_cbs_bracket()
    o += _svg_priority_note()
    o += _svg_classification()
    o += _svg_arbiter()
    o.append('</svg>')
    return "\n".join(o)


def drawio() -> str:
    """The same map as an editable .drawio, for annotating without hand-drawing it."""
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    def vertex(nid: str, box: Box, label: str, palette: tuple[str, str],
               fs: int = 12, bold: bool = False) -> None:
        """Append one rounded vertex, in the DOC_MAP.gen.py fill/stroke style."""
        fill, stroke = palette
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                 f"fontSize={fs};align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
                 + ("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="{nid}" value="{esc(label)}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{box.x}" y="{box.y}" width="{box.w}" '
                     f'height="{box.h}" as="geometry"/></mxCell>')

    vertex("title", Box(40, 20, 1500, 40),
           f"Egress queue map - {NQ} traffic classes, 802.1Q order "
           f"(GENERATED from ethernet_packet_pkg.sv + milan_csr.sv)", ("none", "none"),
           20, True)
    for q in range(NQ):
        name, doc = QUEUES[q]
        rank = (NQ - q) if TOP_WINS else (q + 1)
        label = (f"#{rank}  q{q} {name}\n{doc}\n"
                 f"idleSlope {mbps(IDLE_1G[q])} ({pct(IDLE_1G[q])}) | {mbps(IDLE_100M[q])} @100M\n"
                 f"reset hiCredit {HI_RST[q]} B / loCredit {LO_RST[q]} B\n"
                 f"{'CBS-capable (REQ-CBS-02)' if q in SHAPED else 'strict priority - never CBS'}")
        vertex(f"q{q}", Box(LX, qy(q), QW, QH), label, qcolour(q))
    vertex("tagged", Box(40, LY, 600, 196),
           "TAGGED frame - 802.1Q decides\n"
           "eff_pcp = vlan_valid ? PCP : CLS_DEFAULT_PCP (0x304)\n"
           "regen = CLS_PRIO_REGEN[eff_pcp] (0x30C)\n"
           "tc = CLS_PCP_TC_MAP[regen] (0x308)\n"
           "queue = CLS_TC_QUEUE_MAP[tc] (0x310)\n"
           f"reset 0x{TCQ_RST:08X} = "
           + ", ".join(f"TC{tc}->q{TC_MAP[tc]}" for tc in range(8)),
           PURPLE)
    vertex("untagged", Box(40, LY + 224, 600, 26 + 20 * len(CTRL_ROWS) + 40),
           "UNTAGGED control - the DESTINATION MAC decides\n"
           + "\n".join(f"{a}  {w}" for a, w in CTRL_ROWS)
           + "\nA row hit needs no EtherType; 0x88F7 splits the shared address.",
           BLUE)
    vertex("fall", Box(40, LY + 224 + 26 + 20 * len(CTRL_ROWS) + 62, 600, 58),
           "FALLTHROUGH - everything else, and any out-of-range map entry, clamped to q0",
           GREY)
    vertex("cbs",
           Box(LX + QW + 60, min(qy(q) for q in SHAPED) + 8 if SHAPED else LY, 330,
               (max(qy(q) for q in SHAPED) + QH - min(qy(q) for q in SHAPED) - 16)
               if SHAPED else 100),
           "802.1Qav credit-based shaper\nREQ-CBS-02: SR classes only, never best effort.\n"
           f"CBS_EN_RST = "
           f"{'none shaped at reset' if not any(EN_RST) else ','.join('q%d' % q for q in range(NQ) if EN_RST[q])}"
           f"\nhi/loCredit at MAX_FRAME_SIZE = {MAX_FRAME} B",
           GREEN)
    vertex("gptp", Box(LX, LY + LADDER_H + 34, QW + 390, 106),
           "Why gPTP sits BELOW the shaped classes - correctness, not preference.\n"
           "802.1Q-2018 8.6.8.2 assumes the shaped queues are the top of the strict-priority "
           "order; a strict-priority queue above them voids the credit accounting that bounds "
           "class-A latency. gPTP is unharmed - every event message is hardware-stamped at the "
           "egress SFD.", ("#FFEBEE", "#C62828"))
    vertex("arb", Box(LX + QW + 60, LY + LADDER_H + 34, 330, 106),
           "arbiter -> MAC TX\npriority_encode scans "
           + (f"q{NQ-1} down to q0" if TOP_WINS else f"q0 up to q{NQ-1}")
           + ", granting the first requester whose CBS gate allows it.",
           GOLD)
    for i, src in enumerate(("tagged", "untagged", "fall")):
        cells.append(f'<mxCell id="e{i}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                     f'strokeColor=#546E7A;strokeWidth=2;" edge="1" parent="1" source="{src}" '
                     f'target="q{NQ-1}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    body = "\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="egress-queue-map">'
            f'<mxGraphModel dx="1600" dy="1000" grid="0" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{W}" pageHeight="{H}" math="0" shadow="0"><root>{body}</root>'
            f'</mxGraphModel></diagram></mxfile>')


base = sys.argv[1] if len(sys.argv) > 1 else "egress_queue_map"
Path(base + ".svg").write_text(svg(), encoding="utf-8")
Path(base + ".drawio").write_text(drawio(), encoding="utf-8")
print(f"wrote {base}.svg and {base}.drawio "
      f"({NQ} queues, shaped-capable {[f'q{q}' for q in SHAPED]}, "
      f"{'top' if TOP_WINS else 'bottom'} index wins)")
