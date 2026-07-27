#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The mod-2^32 ring and the half-range convention the listener reads it with.

    python3 docs/diagrams/diag_ts_modular_ring.py docs/diagrams/ts_modular_ring.svg

There is no signed quantity anywhere in the presentation-time path. The
avtp_timestamp is a 32-bit UNSIGNED absolute time - the low 32 bits of the
gPTP nanosecond count plus the presentation offset:

  * IEEE 1722-2016 4.4.4.9 (docs/traceability/ieee1722-2016.md row AVTP-10)
  * hdl/ieee1722/aaf/aaf_talker_i2s.sv    reg   [31:0] ts_r  <= ptp_ns_i[31:0]
                                                              + transit_ns_i
  * hdl/ieee1722/aaf/KL_aaf_packetizer.sv logic [31:0] ets_r -> frame bytes 30..33
  * hdl/ieee1722/avtp/avtp_stream_parser.sv wire [31:0] ats  <- AVTP bytes 12..15
  * hdl/milan/milan_datapath.sv           wire  [63:0] ptp_now_w, and the
                                          monitor is handed ptp_now_w[31:0]

What the listener does is a MODULAR comparison, delta = (ts - now) mod 2^32,
read with a HALF-RANGE convention: below 2^31 means "ahead of me", at or above
2^31 means "behind me". Our own RTL spells that convention as a signed cast,
hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:

    wire signed [31:0] ts_delta_w = avtp_ts_i - ptp_now_i;
    wire late_w  = ts_delta_w < 0;
    wire early_w = !late_w && unsigned'(ts_delta_w) > (pres_ofs_i + EARLY_MARGIN_NS_C);

A signed read of an unsigned modular difference IS the half-range convention.

Every proportion drawn is COMPUTED from the constants below, so the picture
cannot disagree with the arithmetic in the prose.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svglib import SVG                                        # noqa: E402

WRAP_NS = 2 ** 32                       # 4,294,967,296 ns = 4.294967296 s
HALF_NS = WRAP_NS // 2                  # 2,147,483,648 ns - the convention's split
PRES_OFS_NS = 2_000_000                 # 2 ms  - talker transit_ns_i reset default
EARLY_MARGIN_NS = 10_000_000            # 10 ms - EARLY_MARGIN_NS_C
ONTIME_NS = PRES_OFS_NS + EARLY_MARGIN_NS   # 12 ms

#: the measured talker-vs-domain separation, 2026-07-27 (three back-to-back
#: PHC reads); LAPS is how many whole rings that is
TRUE_OFFSET_S = 216_446.0
LAPS = int(TRUE_OFFSET_S / (WRAP_NS / 1e9))

PCT_LATE = 100.0 * HALF_NS / WRAP_NS
PCT_ONTIME = 100.0 * ONTIME_NS / WRAP_NS
PCT_EARLY = 100.0 - PCT_LATE - PCT_ONTIME
DEG_ONTIME = 360.0 * ONTIME_NS / WRAP_NS

RED, GREEN, AMBER, VIO = "#c0392b", "#2b7d46", "#c98a1e", "#7a4fa3"
RED_F, GREEN_F, AMBER_F = "#fdecea", "#eaf5ee", "#fdf3e7"

g = SVG(1440, 810,
        "The 4.294967296 s ring, and the half-range convention that reads it",
        "avtp_timestamp is a 32-bit UNSIGNED absolute time - the listener compares it modulo 2^32 "
        "and splits the result at 2^31")


def raw(s):
    g.e.append(s)


# ============================================================ panel A: ring ===
CX, CY, R = 400, 396, 158
g.box(40, 100, 700, 596, "", None, fill="#ffffff", stroke="#ddd", r=10, sw=1.4)
g.label(390, 130, "A.  the ring", fs=15, col="#111", anchor="middle", weight="700")
g.label(390, 150, "one lap = 2^32 ns = 4.294967296 s; 0 at the top, delta increasing clockwise",
        fs=11, col="#666", anchor="middle")


def pt(d_ns, rad=None):
    """modular delta in ns [0, 2^32) -> ring point; 0 at the top, clockwise."""
    rad = R if rad is None else rad
    th = 2 * math.pi * d_ns / WRAP_NS - math.pi / 2
    return CX + rad * math.cos(th), CY + rad * math.sin(th)


def wedge(a_ns, b_ns, col, fill):
    x0, y0 = pt(a_ns)
    x1, y1 = pt(b_ns)
    large = 1 if (b_ns - a_ns) > HALF_NS else 0
    raw(f'<path d="M {CX} {CY} L {x0:.2f} {y0:.2f} A {R} {R} 0 {large} 1 {x1:.2f} {y1:.2f} Z" '
        f'fill="{fill}" stroke="{col}" stroke-width="1.8"/>')


wedge(ONTIME_NS, HALF_NS, AMBER, AMBER_F)        # reads AHEAD, past the margin
wedge(HALF_NS, WRAP_NS, RED, RED_F)              # reads BEHIND - the whole far half
wedge(0, ONTIME_NS, GREEN, GREEN)                # on time; to scale, 1.01 degrees

g.label(CX + 84, CY - 88, "EARLY", fs=16, col=AMBER, anchor="middle", weight="700")
g.label(CX + 84, CY - 70, f"{PCT_EARLY:.2f} %", fs=11, col=AMBER, anchor="middle")
g.label(CX + 84, CY - 54, "reads AHEAD", fs=10, col=AMBER, anchor="middle")
g.label(CX - 84, CY - 88, "LATE", fs=16, col=RED, anchor="middle", weight="700")
g.label(CX - 84, CY - 70, f"{PCT_LATE:.2f} %", fs=11, col=RED, anchor="middle")
g.label(CX - 84, CY - 54, "reads BEHIND", fs=10, col=RED, anchor="middle")

g.line(CX, CY - R - 2, CX, CY - R - 24, col=GREEN, w=1.8)
g.label(CX, CY - R - 56, "delta = 0", fs=12.5, col=GREEN, anchor="middle", weight="700")
g.label(CX, CY - R - 41, f"ON TIME {PCT_ONTIME:.4f} % of the lap", fs=11.5, col=GREEN,
        anchor="middle", weight="700")
g.label(CX, CY - R - 27, f"drawn to scale: {DEG_ONTIME:.2f} degrees of arc", fs=9.5,
        col="#888", anchor="middle")
g.line(CX, CY + R + 2, CX, CY + R + 22, col="#555", w=1.8)
g.label(CX, CY + R + 38, "delta = 2^31 = 2.147483648 s", fs=11.5, col="#333",
        anchor="middle", weight="700")
g.label(CX, CY + R + 53, "the half-range split - the ONLY thing that decides ahead vs behind",
        fs=10.5, col="#666", anchor="middle")

# ---- the laps that are not observable ----------------------------------------
sp = []
for i in range(0, 481):
    frac = i / 480.0
    th = 2 * math.pi * 3.6 * frac - math.pi / 2
    rr = 16 + (R - 46) * frac
    sp.append(f"{CX + rr*math.cos(th):.2f},{CY + rr*math.sin(th):.2f}")
raw(f'<polyline points="{" ".join(sp)}" fill="none" stroke="{VIO}" stroke-width="1.5" '
    f'opacity="0.55" marker-end="url(#arr)"/>')
g.label(CX, CY + 6, f"{LAPS:,} laps", fs=13, col=VIO, anchor="middle", weight="700")
g.label(CX, CY + 22, "none observable", fs=10.5, col=VIO, anchor="middle")

# ---- where it lands, and that it keeps moving --------------------------------
LAND = int(0.63 * HALF_NS)
lx, ly = pt(LAND)
raw(f'<circle cx="{lx:.2f}" cy="{ly:.2f}" r="8" fill="{VIO}" stroke="#ffffff" stroke-width="2"/>')
g.label(lx + 14, ly + 4, "lands here", fs=11.5, col=VIO, anchor="start", weight="700")


def walk_arrow(a_ns, b_ns):
    """outer dashed arc a -> b in the direction the delta actually moves."""
    x0, y0 = pt(a_ns, R + 22)
    x1, y1 = pt(b_ns, R + 22)
    sweep = 1 if b_ns > a_ns else 0
    raw(f'<path d="M {x0:.2f} {y0:.2f} A {R+22} {R+22} 0 0 {sweep} {x1:.2f} {y1:.2f}" '
        f'fill="none" stroke={chr(34)}{VIO}{chr(34)} stroke-width="2.4" '
        f'stroke-dasharray="6 4" marker-end="url(#arr)"/>')


# talker PHC runs SLOW (-10,004 ppm vs its own CLOCK_MONOTONIC, 2026-07-27), so
# ts - now falls every second: the modular delta DECREASES and wraps at 0.
walk_arrow(int(0.80 * HALF_NS), int(0.34 * HALF_NS))     # up the EARLY side
walk_arrow(int(1.66 * HALF_NS), int(1.20 * HALF_NS))     # up the LATE side
g.box(96, 636, 590, 46,
      "the landing point is arbitrary, and the drift keeps it moving",
      "talker PHC slewed -10,004 ppm  ->  delta falls, wraps through 0, and comes round again",
      fill="#f6f0fa", stroke=VIO, tcol="#4a2d66", fs=12, r=6)

# ======================================================= panel B: unrolled ====
g.box(770, 100, 630, 596, "", None, fill="#ffffff", stroke="#ddd", r=10, sw=1.4)
g.label(1085, 130, "B.  the same ring, unrolled", fs=15, col="#111", anchor="middle", weight="700")
g.label(1085, 150, "delta = (avtp_timestamp - ptp_now) mod 2^32, in ns", fs=11,
        col="#666", anchor="middle")

BX, BW, BY0 = 900, 96, 180
BH = 280                                    # full 2^32 drawn top (0) to bottom


def by(d_ns):
    return BY0 + BH * d_ns / WRAP_NS


ONT_H = max(2.0, BH * ONTIME_NS / WRAP_NS)
raw(f'<rect x="{BX}" y="{by(0)}" width="{BW}" height="{ONT_H}" fill="{GREEN}" stroke="{GREEN}"/>')
raw(f'<rect x="{BX}" y="{by(ONTIME_NS)}" width="{BW}" height="{by(HALF_NS)-by(ONTIME_NS)}" '
    f'fill="{AMBER_F}" stroke="{AMBER}" stroke-width="1.6"/>')
raw(f'<rect x="{BX}" y="{by(HALF_NS)}" width="{BW}" height="{by(WRAP_NS)-by(HALF_NS)}" '
    f'fill="{RED_F}" stroke="{RED}" stroke-width="1.6"/>')
g.label(BX + BW / 2, by(HALF_NS / 2) + 4, "EARLY", fs=15, col=AMBER, anchor="middle", weight="700")
g.label(BX + BW / 2, by(HALF_NS / 2) + 20, f"{PCT_EARLY:.2f} %", fs=11, col=AMBER, anchor="middle")
g.label(BX + BW / 2, by(HALF_NS + HALF_NS / 2) + 4, "LATE", fs=15, col=RED, anchor="middle", weight="700")
g.label(BX + BW / 2, by(HALF_NS + HALF_NS / 2) + 20, f"{PCT_LATE:.2f} %", fs=11, col=RED, anchor="middle")

for d, txt in ((0, "0"), (HALF_NS, "2^31  =  2.147483648 s"),
               (WRAP_NS, "2^32  =  4.294967296 s   (= 0 again)")):
    g.line(BX - 8, by(d), BX, by(d), col="#999", w=1)
    g.label(BX - 12, by(d) + 4, txt, fs=10.5, col="#444", anchor="end")
g.label(BX + BW + 12, by(HALF_NS / 2), "reads AHEAD of me", fs=11, col=AMBER, weight="700")
g.label(BX + BW + 12, by(HALF_NS + HALF_NS / 2), "reads BEHIND me", fs=11, col=RED, weight="700")

# the on-time sliver, magnified
MY, MX0, MX1 = 556, 830, 1350
g.line(BX, by(0), MX0, MY - 24, col="#bbb", w=1, dash="3 3")
g.line(BX, by(ONTIME_NS), MX0, MY + 24, col="#bbb", w=1, dash="3 3")
g.label(1090, 500, f"the on-time band magnified: {ONTIME_NS/1e6:.0f} ms of {WRAP_NS/1e9:.9f} s = {PCT_ONTIME:.4f} %",
        fs=11.5, col=GREEN, anchor="middle", weight="700")


def mx(ms):
    return MX0 + (MX1 - MX0) * (ms + 1.0) / 15.0


raw(f'<rect x="{mx(-1)}" y="{MY-24}" width="{mx(0)-mx(-1)}" height="48" fill="{RED_F}" stroke="{RED}" stroke-width="1.4"/>')
raw(f'<rect x="{mx(0)}" y="{MY-24}" width="{mx(12)-mx(0)}" height="48" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="1.8"/>')
raw(f'<rect x="{mx(12)}" y="{MY-24}" width="{mx(14)-mx(12)}" height="48" fill="{AMBER_F}" stroke="{AMBER}" stroke-width="1.4"/>')
g.label(mx(7), MY + 5, "ON TIME", fs=13, col=GREEN, anchor="middle", weight="700")
raw(f'<circle cx="{mx(2)}" cy="{MY}" r="5.5" fill="{GREEN}"/>')
g.label(mx(2), MY - 34, "a synced talker lands here (pto = 2 ms)", fs=10.5, col=GREEN,
        anchor="middle", weight="700")
for ms, txt in ((0, "0"), (2, "2 ms"), (12, "12 ms")):
    g.line(mx(ms), MY + 24, mx(ms), MY + 34, col="#999", w=1)
    g.label(mx(ms), MY + 48, txt, fs=10.5, col="#444", anchor="middle")
g.label(mx(12), MY + 62, "pto + EARLY_MARGIN_NS_C", fs=10, col=AMBER, anchor="middle")

g.box(800, 630, 570, 56,
      "late  = ts_delta < 0\nearly = !late && ts_delta > pres_ofs + EARLY_MARGIN_NS_C",
      "KL_avtp_rx_monitor.sv - the signed cast of an unsigned modular difference IS this convention",
      fill="#eef3f8", stroke="#33628f", tcol="#123", fs=11.5, r=6)

# ==================================================================== banner ==
g.box(40, 712, 1360, 66,
      "the listener is not measuring a wrong offset - it is measuring a meaningless one, correctly",
      f"once the true separation exceeds one lap, the modular difference carries NO information about the "
      f"direction or the magnitude of the clock error; at {LAPS:,} laps it is simply a point on the ring",
      fill="#f6f0fa", stroke=VIO, tcol="#4a2d66", fs=14, r=8, sw=2.0, subcol="#5b4272")

g.save(sys.argv[1] if len(sys.argv) > 1 else "ts_modular_ring.svg")
print("ok")
