#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The walk around the ring - predicted half-period vs the one measured.

    python3 docs/diagrams/diag_ts_wrap_walk.py docs/diagrams/ts_wrap_walk.svg

This is the SAME picture as docs/diagrams/ts_modular_ring.svg, at a longer
timescale: the ring of that figure, cut at delta = 0 and laid out against
time. The modular delta falls steadily (the talker's clock is slow), crosses
the 2^31 half-range split, reaches 0, wraps back to 2^32, and does it again -
and every crossing is one flip of the listener's verdict.

Panel A draws two constant-rate walks over the 484 s sweep: the one PREDICTED
by the talker's own measured PHC rate error, and the one whose period matches
what the listener actually reported. Panel B is the measured polarity strip
the observed period is derived FROM, with every derived transition instant and
every gap between them drawn - including the two that do not fit.

Nothing here is fitted: the observed period is computed from the strip below
it, in this script, and printed on stdout.

Inputs, all traceable:
  * WRAP_NS 2**32 ns - avtp_timestamp field width, IEEE 1722-2016 4.4.4.9
  * HALF_NS 2**31 ns - the half-range split (KL_avtp_rx_monitor.sv reads the
    modular difference with a signed cast, which is that convention)
  * RATE_MEASURED 1.0004 % - the talker PHC against its own CLOCK_MONOTONIC
    (261.858 s advanced in 264.504 s, 2026-07-27; no network in the loop)
  * SAMPLES - (t_s, late_pct, early_pct) per 20 s counter sweep of the
    reference listener's STREAM_INPUT.0, 2026-07-27. Only the polarity columns
    are carried here; the full counter record lives in the finding page
    docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svglib import SVG                                        # noqa: E402

WRAP_NS = 2 ** 32
HALF_NS = WRAP_NS // 2
WRAP_S = WRAP_NS / 1e9                  # 4.294967296 s
HALF_S = HALF_NS / 1e9                  # 2.147483648 s
ONTIME_NS = 12_000_000                  # pto 2 ms + EARLY_MARGIN_NS_C 10 ms
RATE_MEASURED = 0.010004                # 1.0004 % = 10,004 ppm

SAMPLES = [
    (20, 98.6, 1.4), (41, 0.0, 100.0), (61, 0.0, 100.0), (81, 0.0, 100.0),
    (101, 0.0, 100.0), (121, 37.9, 56.8), (141, 100.0, 0.0), (161, 3.0, 97.0),
    (181, 56.1, 38.6), (201, 100.0, 0.0), (222, 100.0, 0.0), (242, 100.0, 0.0),
    (262, 100.0, 0.0), (282, 7.1, 92.9), (302, 0.0, 100.0), (322, 0.0, 100.0),
    (342, 0.0, 100.0), (362, 29.5, 65.2), (382, 100.0, 0.0), (403, 100.0, 0.0),
    (423, 100.0, 0.0), (443, 100.0, 0.0), (463, 33.8, 66.2), (483, 0.0, 100.0),
]
T_END = 484.0


def polarity(late, early):
    return "L" if late >= 90 else ("E" if early >= 90 else "M")


def transitions():
    """Transition instants, estimated at the midpoint of the interval the
    polarity changed in - so each carries +/- 10 s from the 20 s cadence."""
    out, tags = [], []
    for i in range(1, len(SAMPLES)):
        t0, l0, e0 = SAMPLES[i - 1]
        t1, l1, e1 = SAMPLES[i]
        c0, c1 = polarity(l0, e0), polarity(l1, e1)
        if c1 == "M" or (c0 in "EL" and c1 in "EL" and c0 != c1):
            out.append((t0 + t1) / 2.0)
            tags.append("mixed" if c1 == "M" else "adjacent")
    return out, tags


TR, TAGS = transitions()
GAPS = [TR[i + 1] - TR[i] for i in range(len(TR) - 1)]
#: the two 20 s-scale gaps straddle the t = 161 s sample that breaks
#: monotonicity; they are an order of magnitude too fast for a walk, so they
#: are excluded from the period estimate - and drawn, labelled, so the
#: exclusion is visible rather than quietly done.
CLEAN = [g for g in GAPS if g > 50.0]
HALF_OBS = sum(CLEAN) / len(CLEAN)
HALF_PRED = HALF_S / RATE_MEASURED
RATE_OBS = HALF_S / HALF_OBS
RATIO = HALF_PRED / HALF_OBS

#: the surviving transitions, in order, with what each one IS. A LATE->EARLY
#: flip is delta crossing 2^31 downward; an EARLY->LATE flip is delta reaching
#: 0 and wrapping to 2^32. Read off the strip, not assumed.
ANCHORS = [(30.5, HALF_NS), (111.0, 0), (171.0, 0), (272.0, HALF_NS),
           (352.0, 0), (453.0, HALF_NS)]
EARLY_BLOCKS = [111.0 - 30.5, 352.0 - 272.0]
LATE_BLOCKS = [272.0 - 171.0, 453.0 - 352.0]

print(f"transitions  : {[round(t, 1) for t in TR]}")
print(f"EARLY blocks : {EARLY_BLOCKS} s     LATE blocks : {LATE_BLOCKS} s")
print(f"gaps         : {[round(x, 1) for x in GAPS]}")
print(f"clean gaps   : {CLEAN}  mean {HALF_OBS:.2f} s")
print(f"predicted    : HALF_S/{RATE_MEASURED} = {HALF_PRED:.2f} s")
print(f"ratio        : {RATIO:.3f} x     implied rate {RATE_OBS*1e6:.0f} ppm")

RED, GREEN, AMBER, VIO, GREY = "#c0392b", "#2b7d46", "#c98a1e", "#7a4fa3", "#8a8a8a"
RED_F, AMBER_F = "#fdecea", "#fdf3e7"

g = SVG(1420, 934,
        "The walk round the ring - 2.4x faster than the clock error explains",
        "the same ring as ts_modular_ring.svg, cut at delta = 0 and laid against time: "
        "predicted from the talker's own PHC rate error vs the period the listener's counters show")


def raw(s):
    g.e.append(s)


PX0, PX1 = 196, 1344
AY0, AY1 = 156, 392                       # delta = 0 at the top, 2^32 at the bottom
AMID = AY0 + (AY1 - AY0) / 2              # delta = 2^31


def xs(t):
    return PX0 + (PX1 - PX0) * t / T_END


def ys(d_ns):
    return AY0 + (AY1 - AY0) * d_ns / WRAP_NS


# ---------------------------------------------------------------- panel A ----
g.box(40, 100, 1340, 366, "", None, fill="#ffffff", stroke="#ddd", r=10, sw=1.4)
raw(f'<rect x="{PX0}" y="{AY0}" width="{PX1-PX0}" height="{AMID-AY0}" fill="{AMBER_F}"/>')
raw(f'<rect x="{PX0}" y="{AMID}" width="{PX1-PX0}" height="{AY1-AMID}" fill="{RED_F}"/>')
raw(f'<rect x="{PX0}" y="{AY0}" width="{PX1-PX0}" height="{AY1-AY0}" fill="none" stroke="#bbb" stroke-width="1"/>')
g.line(PX0, AMID, PX1, AMID, col="#777", w=1.2)
g.label(PX0 + 8, AY0 + 18, "EARLY   -   delta below 2^31 reads AHEAD", fs=11.5, col=AMBER, weight="700")
g.label(PX0 + 8, AY1 - 8, "LATE   -   delta at or above 2^31 reads BEHIND", fs=11.5, col=RED, weight="700")
g.label(PX0 - 12, AY0 + 5, "0", fs=10.5, col="#444", anchor="end")
g.label(PX0 - 12, AMID + 4, "2^31 = 2.147483648 s", fs=10.5, col="#444", anchor="end")
g.label(PX0 - 12, AY1 + 4, "2^32 = 4.294967296 s", fs=10.5, col="#444", anchor="end")
g.label(66, AY0 - 22, "delta = (avtp_timestamp - ptp_now) mod 2^32   -   the whole ring, cut at 0",
        fs=12, col="#333", weight="700")

for t in range(0, 481, 60):
    g.line(xs(t), AY1, xs(t), AY1 + 6, col="#999", w=1)
    g.label(xs(t), AY1 + 22, f"{t}", fs=10.5, col="#666", anchor="middle")
g.label((PX0 + PX1) / 2, AY1 + 42, "t (s) into the 484 s counter sweep", fs=11.5,
        col="#333", anchor="middle", weight="700")


def delta_at(t, rate):
    """delta falls at `rate` s per s and is phase-locked so the FIRST observed
    transition (a LATE->EARLY flip = a downward crossing of 2^31) lands on it."""
    d0 = HALF_NS + rate * 1e9 * TR[0]
    return (d0 - rate * 1e9 * t) % WRAP_NS


def delta_measured(t):
    """delta from the MEASURED block schedule: linear inside each block,
    between the anchors the strip actually fixes."""
    pts = [(-70.5, WRAP_NS)] + ANCHORS + [(533.5, 0)]
    for i in range(len(pts) - 1):
        (ta, da), (tb, db) = pts[i], pts[i + 1]
        if ta <= t <= tb:
            if db > da:                     # a wrap sits on this boundary
                da = WRAP_NS
            f = (t - ta) / (tb - ta)
            return da + (db - da) * f
    return 0.0


def walk(rate, col, width, dash):
    seg, prev = [], None
    for i in range(0, 2425):
        t = T_END * i / 2424.0
        d = delta_at(t, rate)
        if prev is not None and d - prev > HALF_NS:          # wrap 0 -> 2^32
            raw(f'<polyline points="{" ".join(seg)}" fill="none" stroke="{col}" '
                f'stroke-width="{width}"{dash}/>')
            seg = []
        seg.append(f"{xs(t):.2f},{ys(d):.2f}")
        prev = d
    if seg:
        raw(f'<polyline points="{" ".join(seg)}" fill="none" stroke="{col}" '
            f'stroke-width="{width}"{dash}/>')


walk(RATE_MEASURED, GREY, 2.0, ' stroke-dasharray="7 5"')
walk(RATE_OBS, VIO, 2.8, "")

g.box(PX1 - 470, AY0 + 12, 460, 62,
      f"predicted from -10,004 ppm:  half-period {HALF_PRED:.2f} s",
      f"observed, from the strip below:  {HALF_OBS:.1f} s   ->   {RATIO:.2f}x FASTER, unexplained",
      fill="#ffffff", stroke=VIO, tcol=GREY, fs=12, r=6, sw=1.6, subcol=VIO)

# ---------------------------------------------------------------- panel B ----
g.box(40, 496, 1340, 404, "", None, fill="#ffffff", stroke="#ddd", r=10, sw=1.4)
g.label(66, 530, "the same walk as a ring, and what the listener's counters actually did - "
        "each bar is one 20 s GET_COUNTERS sweep",
        fs=12, col="#333", weight="700")

# ---- ring snapshots: the identical picture, sampled ----
RR = 30
RY = 586
for t in (15, 70, 200, 310, 400, 470):
    cx = xs(t)

    def rpt(d_ns, rad=RR):
        th = 2 * math.pi * d_ns / WRAP_NS - math.pi / 2
        return cx + rad * math.cos(th), RY + rad * math.sin(th)

    for a, b, col, fill in ((0, HALF_NS, AMBER, AMBER_F), (HALF_NS, WRAP_NS, RED, RED_F)):
        x0, y0 = rpt(a)
        x1, y1 = rpt(b)
        raw(f'<path d="M {cx} {RY} L {x0:.2f} {y0:.2f} A {RR} {RR} 0 0 1 {x1:.2f} {y1:.2f} Z" '
            f'fill="{fill}" stroke="{col}" stroke-width="1.2"/>')
    px, py = rpt(delta_measured(t))
    raw(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="5" fill="{VIO}" stroke="#ffffff" stroke-width="1.5"/>')
    g.label(cx, RY - RR - 10, f"t = {t} s", fs=10, col="#666", anchor="middle")
g.label(PX0 - 12, RY + 4, "the ring:", fs=11, col="#333", anchor="end", weight="700")

# ---- the measured polarity strip ----
BY, BH = 660, 62
prev_t = 0.0
for t, late, early in SAMPLES:
    x0, x1 = xs(prev_t), xs(t)
    other = max(0.0, 100.0 - late - early)
    he, ho, hl = BH * early / 100.0, BH * other / 100.0, BH * late / 100.0
    raw(f'<rect x="{x0:.2f}" y="{BY}" width="{x1-x0:.2f}" height="{he:.2f}" fill="{AMBER}" opacity="0.9"/>')
    raw(f'<rect x="{x0:.2f}" y="{BY+he:.2f}" width="{x1-x0:.2f}" height="{ho:.2f}" fill="{GREEN}" opacity="0.9"/>')
    raw(f'<rect x="{x0:.2f}" y="{BY+he+ho:.2f}" width="{x1-x0:.2f}" height="{hl:.2f}" fill="{RED}" opacity="0.9"/>')
    raw(f'<rect x="{x0:.2f}" y="{BY}" width="{x1-x0:.2f}" height="{BH}" fill="none" stroke="#ffffff" stroke-width="0.7"/>')
    prev_t = t
raw(f'<rect x="{xs(0)}" y="{BY}" width="{xs(T_END)-xs(0)}" height="{BH}" fill="none" stroke="#999" stroke-width="1"/>')
g.label(PX0 - 12, BY + 16, "EARLY", fs=10.5, col=AMBER, anchor="end", weight="700")
g.label(PX0 - 12, BY + 38, "on time", fs=10.5, col=GREEN, anchor="end", weight="700")
g.label(PX0 - 12, BY + 58, "LATE", fs=10.5, col=RED, anchor="end", weight="700")

for t in TR:
    g.line(xs(t), BY - 14, xs(t), BY + BH + 14, col=VIO, w=1.6, dash="4 3")
    g.label(xs(t), BY - 20, f"{t:.0f}", fs=10.5, col=VIO, anchor="middle", weight="700")
for i, gp in enumerate(GAPS):
    xa, xb, yy = xs(TR[i]), xs(TR[i + 1]), BY + BH + 34
    ok = gp > 50.0
    col = VIO if ok else RED
    g.line(xa, yy, xb, yy, col=col, w=1.6)
    g.line(xa, yy - 5, xa, yy + 5, col=col, w=1.6)
    g.line(xb, yy - 5, xb, yy + 5, col=col, w=1.6)
    g.label((xa + xb) / 2, yy - 9, f"{gp:.0f} s", fs=11, col=col, anchor="middle", weight="700")
    if not ok:
        g.label((xa + xb) / 2, yy + 19, "x", fs=12, col=RED, anchor="middle", weight="700")

g.label(xs(160), BY + BH + 70,
        "the t = 161 s sample breaks monotonicity: a ~20 s excursion, far too fast for a walk - "
        "excluded here, and not explained anywhere",
        fs=11, col=RED, anchor="middle", weight="700")

g.label(xs(300), BY + BH + 88,
        f"and the two polarities are not equal halves: EARLY blocks {EARLY_BLOCKS[0]:.1f} and "
        f"{EARLY_BLOCKS[1]:.1f} s, LATE blocks {LATE_BLOCKS[0]:.1f} and {LATE_BLOCKS[1]:.1f} s - "
        f"also unexplained (+/- 10 s from the sweep cadence)",
        fs=11, col=VIO, anchor="middle", weight="700")
g.box(66, BY + BH + 104, 1278, 58,
      f"half-period from the four surviving gaps {CLEAN} s   ->   mean {HALF_OBS:.1f} s   "
      f"against {HALF_PRED:.1f} s predicted",
      f"the mechanism is settled; the RATE is not. Implied relative rate {RATE_OBS*1e6:.0f} ppm against "
      f"{RATE_MEASURED*1e6:.0f} ppm measured on the talker - a {RATIO:.2f}x gap this record does not close.",
      fill="#f6f0fa", stroke=VIO, tcol="#4a2d66", fs=12.5, r=6)

g.save(sys.argv[1] if len(sys.argv) > 1 else "ts_wrap_walk.svg")
print("ok")
