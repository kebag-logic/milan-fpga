#!/usr/bin/env python3
# Generate the campaign performance chart as SVG (measured 2026-07, deterministic harness).
import sys

# --- measured data (Mbit/s) ---
configs = ["m1", "l2x2", "mlp1", "mlp2", "mlp3", "copy‑removed"]
sub     = ["32K L2\nblocking D$", "+64K L2", "+refill=8", "+RPT pref.", "+RPT+64K", "(MSG_TRUNC)"]
rx_s    = [206, 207, 198, 277, 259, 427]
rx_p2   = [238, 280, 229, 246, 298, 481]
tx_p4   = [None, 405, None, 375, 414, None]   # TX −P4 median of 3 rounds (l2x2 vs mlp3 ≈ equal)
GOAL = 500

# --- layout ---
W, H = 1080, 600
ML, MR, MT, MB = 74, 300, 92, 118          # margins (MR wide for the side legend)
PW, PH = W-ML-MR, H-MT-MB                   # plot area
YMAX = 550
def y(v): return MT + PH*(1 - v/YMAX)
def bx(gi, bi, nb, bw, gap):                # group i, bar i
    gwidth = PW/len(configs)
    gx = ML + gi*gwidth
    total = nb*bw + (nb-1)*gap
    return gx + (gwidth-total)/2 + bi*(bw+gap)

BW, GAP = 26, 6
COL = {"s":"#7db8e8", "p2":"#1f6fb2", "tx":"#3fae6a"}
s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
# title
s.append(f'<text x="{W/2}" y="34" text-anchor="middle" font-size="23" font-weight="700" fill="#111">Milan FPGA NIC — RX/TX throughput by lever</text>')
s.append(f'<text x="{W/2}" y="58" text-anchor="middle" font-size="13.5" fill="#555">2026-07 campaign · 100 MHz · dual VexiiRiscv · deterministic split harness · goal &gt;500 Mbit/s RX+TX</text>')
# gridlines + y labels
for gv in range(0, YMAX+1, 100):
    yy = y(gv)
    s.append(f'<line x1="{ML}" y1="{yy:.1f}" x2="{ML+PW}" y2="{yy:.1f}" stroke="#e6e6e6" stroke-width="1"/>')
    s.append(f'<text x="{ML-10}" y="{yy+4:.1f}" text-anchor="end" font-size="12" fill="#888">{gv}</text>')
s.append(f'<text x="20" y="{MT+PH/2}" text-anchor="middle" font-size="13" fill="#555" transform="rotate(-90 20 {MT+PH/2})">Mbit/s</text>')
# goal line
yg = y(GOAL)
s.append(f'<line x1="{ML}" y1="{yg:.1f}" x2="{ML+PW}" y2="{yg:.1f}" stroke="#d1495b" stroke-width="2" stroke-dasharray="8 5"/>')
s.append(f'<text x="{ML+PW-4}" y="{yg-7:.1f}" text-anchor="end" font-size="12.5" font-weight="700" fill="#d1495b">GOAL 500</text>')
# bars
def bar(gi, bi, nb, val, col, lbl):
    if val is None: return
    xx = bx(gi, bi, nb, BW, GAP); yy = y(val); hh = MT+PH-yy
    s.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{BW}" height="{hh:.1f}" fill="{col}" rx="2"/>')
    s.append(f'<text x="{xx+BW/2:.1f}" y="{yy-5:.1f}" text-anchor="middle" font-size="11.5" font-weight="700" fill="#333">{val}</text>')
for gi in range(len(configs)):
    present = [("s",rx_s[gi],COL["s"]), ("p2",rx_p2[gi],COL["p2"])]
    if tx_p4[gi] is not None: present.append(("tx",tx_p4[gi],COL["tx"]))
    nb = len(present)
    for bi,(k,v,c) in enumerate(present):
        bar(gi, bi, nb, v, c, k)
    # x labels
    gwidth = PW/len(configs); cx = ML+gi*gwidth+gwidth/2
    s.append(f'<text x="{cx:.1f}" y="{MT+PH+22:.1f}" text-anchor="middle" font-size="13.5" font-weight="700" fill="#222">{configs[gi]}</text>')
    for j,ln in enumerate(sub[gi].split("\n")):
        s.append(f'<text x="{cx:.1f}" y="{MT+PH+38+j*14:.1f}" text-anchor="middle" font-size="10.5" fill="#777">{ln}</text>')
# axis baseline
s.append(f'<line x1="{ML}" y1="{MT+PH}" x2="{ML+PW}" y2="{MT+PH}" stroke="#999" stroke-width="1.3"/>')
# legend (right side)
lx, ly = ML+PW+26, MT+8
for i,(lab,col) in enumerate([("RX single-flow",COL["s"]),("RX −P2  (2 harts)",COL["p2"]),("TX −P4",COL["tx"])]):
    yy=ly+i*26
    s.append(f'<rect x="{lx}" y="{yy}" width="16" height="16" fill="{col}" rx="2"/>')
    s.append(f'<text x="{lx+23}" y="{yy+13}" font-size="12.5" fill="#333">{lab}</text>')
# callouts (right side, below legend)
cy = ly+3*26+22
s.append(f'<text x="{lx}" y="{cy-4}" font-size="12.5" font-weight="700" fill="#333">What moved the needle</text>')
notes = [
  ("#1f6fb2","RX −P2:  238 →280 (L2) →298 (RPT)"),
  ("#7db8e8","RX single:  207 →277  (+34% RPT)"),
  ("#3fae6a","TX −P4 ≈410 both (UNAFFECTED)"),
  ("#3fae6a","TX −P2 peaks 525–536  (&gt;500!)"),
  ("#d1495b","RX ceiling 481 (copy removed)"),
  ("#666","recv copy = 51% of RX CPU"),
]
for i,(col,t) in enumerate(notes):
    s.append(f'<text x="{lx}" y="{cy+18+i*20}" font-size="11.5" fill="{col}">{t}</text>')
# bottom caption
s.append(f'<text x="{ML}" y="{H-34}" font-size="12" fill="#444">Levers: 64K L2 (capacity, +18% RX−P2) · non-blocking D$ refill=8 (0 gain alone) · RPT hardware prefetcher (fills the slots → +34% single) · both compound in mlp3.</text>')
s.append(f'<text x="{ML}" y="{H-16}" font-size="12" fill="#444">RX −P2 wall = the recv payload copy (cold DRAM reads); removing it (MSG_TRUNC) reaches 481 = 96% of goal. TX crosses 500 at mlp3 −P2.</text>')
s.append('</svg>')
open(sys.argv[1] if len(sys.argv)>1 else "chart.svg","w").write("\n".join(s))
print("wrote", sys.argv[1] if len(sys.argv)>1 else "chart.svg")
