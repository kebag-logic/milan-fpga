import sys; sys.path.insert(0,"/tmp/scratch/-home-alex-prjs-avb-on-fpga-milan-fpga/e2f37f43-41eb-4959-ab3e-979ecb25f127/scratchpad")
from svglib import SVG
g = SVG(1280, 560, "RX receive path — where the CPU time goes, and the wall",
        "measured with perf on mlp3 · RX −P2 (2-hart) · 100 MHz")
# ---- HW ingress lane (top) ----
g.label(60, 92, "HARDWARE  (datapath, gateware)", fs=12, col="#33628f", weight="700")
hw = [("1 GbE\nwire", None, "#f4f7fa"),
      ("RGMII\nPHY", None, "#f4f7fa"),
      ("MilanMAC\n+ HW RSC", "coalesces N\nframes → 1", "#eef3f8"),
      ("RX DMA\nwriter", "burst-writes\nto DRAM", "#eef3f8")]
x=60; y=104; bw=150; bh=76; gap=42
xs=[]
for i,(lb,sub,fill) in enumerate(hw):
    g.box(x, y, bw, bh, lb, sub, fill=fill); xs.append(x)
    if i: g.arrow(xs[i-1]+bw+4, y+bh/2, x-4, y+bh/2)
    x += bw+gap
# DRAM buffer (center, spans)
dram_x = x+6; dram_w=168
g.box(dram_x, y, dram_w, bh, "DRAM\nRX buffer", "payload lands here\n(cold — never cached)", fill="#fdf3e7", stroke="#c98a1e")
g.arrow(xs[-1]+bw+4, y+bh/2, dram_x-4, y+bh/2)
# ---- SW/CPU lane (bottom) ----
yb=340
g.label(60, yb-16, "SOFTWARE  (Linux kernel, 2 harts)", fs=12, col="#7a4fa3", weight="700")
sw = [("NAPI poll\n+ GRO", "reads BD +\nheaders (cold)", "#f3eef8", "#7a4fa3"),
      ("tcp_recvmsg", "receive queue", "#f3eef8", "#7a4fa3"),
      ("copy_to_user", "reads payload\nCOLD from DRAM", "#fdecea", "#c0392b"),
      ("userspace\napp  (recv)", None, "#eef7f0", "#3fae6a")]
x=60; xs2=[]
for i,(lb,sub,fill,st) in enumerate(sw):
    tcol = "#c0392b" if lb=="copy_to_user" else "#123"
    sw_=2.4 if lb=="copy_to_user" else 1.6
    g.box(x, yb, bw, bh, lb, sub, fill=fill, stroke=st, tcol=tcol, sw=sw_); xs2.append(x)
    if i: g.arrow(xs2[i-1]+bw+4, yb+bh/2, x-4, yb+bh/2)
    x += bw+gap
# DRAM -> CPU read (down/left arrow into copy_to_user + NAPI)
copy_x = xs2[2]
g.arrow(dram_x+dram_w*0.35, y+bh+4, copy_x+bw/2, yb-4, red=True, w=2.4)
g.label(dram_x+dram_w*0.35+8, (y+bh+yb)/2, "cold read", fs=11, col="#c0392b", weight="700")
g.arrow(dram_x+8, y+bh+4, xs2[0]+bw/2, yb-4, col="#999", w=1.6, dash="4 4")
# THE WALL callout
g.box(copy_x-6, yb+bh+22, bw+12, 56, "THE WALL", "51% of RX −P2 CPU\n~18 cyc / 8-byte word", fill="#c0392b", stroke="#8e1e12", tcol="#fff", subcol="#ffd9d4", fs=13, r=6)
# levers callout (right)
lx=dram_x+dram_w+40
g.box(lx, y-6, 210, 150, "", None, fill="#f7fbf8", stroke="#3fae6a", r=8)
g.label(lx+14, y+18, "Levers on this cold read", fs=12.5, col="#2b6", weight="700")
for i,t in enumerate([("• RPT prefetcher HIDES it","#1f6fb2"),
                      ("  → single 207→277 (+34%)","#666"),
                      ("• 64K L2 cuts capacity miss","#1f6fb2"),
                      ("  → −P2 238→280","#666"),
                      ("• DDIO would WARM it","#c0392b"),
                      ("  (next lever, task #15)","#666")]):
    g.label(lx+14, y+40+i*17, t[0], fs=11, col=t[1])
# bottom result bar
g.line(60, 500, 1080, 500, col="#ddd")
g.label(60, 524, "RX −P2 WITH the copy = 298 Mbit/s", fs=14, col="#c0392b", weight="700")
g.label(470, 524, "→  WITHOUT it (MSG_TRUNC ceiling) = 481", fs=14, col="#2b7", weight="700")
g.label(900, 524, "= 96% of the 500 goal", fs=13, col="#444")
g.save(sys.argv[1])
print("ok")
