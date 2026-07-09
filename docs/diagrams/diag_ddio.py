import sys; sys.path.insert(0,"/tmp/scratch/-home-alex-prjs-avb-on-fpga-milan-fpga/e2f37f43-41eb-4959-ab3e-979ecb25f127/scratchpad")
from svglib import SVG
g = SVG(1180, 520, "DDIO — the next RX lever: land the DMA payload WARM",
        "the copy is 51% of RX CPU because it reads the payload COLD from DRAM; DDIO makes that read a cache HIT")
def panel(px, title, tcol, sfill, sstroke):
    pw=520
    g.box(px, 84, pw, 396, "", None, fill="#ffffff", stroke="#ddd", r=10, sw=1.4)
    g.label(px+pw/2, 112, title, fs=15, col=tcol, anchor="middle", weight="700")
    return px, pw
# ---- TODAY ----
px,pw = panel(50, "TODAY  —  cold copy  (mlp3)", "#c0392b", None, None)
g.box(px+40, 140, 200, 60, "RX DMA writer", "burst-writes payload", fill="#eef3f8", stroke="#33628f", fs=13)
g.box(px+280, 140, 200, 60, "DDR3 DRAM", "payload (cold)", fill="#fdf3e7", stroke="#c98a1e", fs=13)
g.arrow(px+240,170, px+276,170)
g.label(px+258,160,"write",fs=10,col="#888")
g.box(px+40, 300, 200, 60, "copy_to_user", "the recv copy", fill="#fdecea", stroke="#c0392b", tcol="#c0392b", fs=13, sw=2.2)
g.arrow(px+380,200, px+160,296, red=True, w=2.4)
g.label(px+270,258,"COLD read",fs=12,col="#c0392b",weight="700")
g.label(px+270,274,"~1424 ns / miss",fs=11,col="#c0392b")
g.box(px+40, 398, 440, 54, "= 51% of RX −P2 CPU  →  RX −P2 = 298 Mbit/s", None, fill="#fdecea", stroke="#c0392b", tcol="#7a1c12", fs=13.5, r=6)
# ---- WITH DDIO ----
px,pw = panel(610, "WITH DDIO  —  warm copy", "#2b7d46", None, None)
g.box(px+40, 140, 200, 60, "RX DMA writer", "allocate-on-write", fill="#eef3f8", stroke="#33628f", fs=13)
g.box(px+280, 140, 200, 60, "L2 / stash", "payload (WARM)", fill="#eaf5ee", stroke="#3fae6a", tcol="#155", fs=13, sw=2.2)
g.arrow(px+240,170, px+276,170, col="#2b7", w=2.4)
g.label(px+250,160,"stash",fs=10,col="#2b7",weight="700")
g.box(px+280, 300, 200, 60, "DDR3 DRAM", "backing store", fill="#f6f0fa", stroke="#7a4fa3", fs=12)
g.arrow(px+380,200, px+380,296, col="#999", w=1.6, dash="4 4")
g.label(px+388,254,"backed by",fs=10,col="#999")
g.box(px+40, 300, 200, 60, "copy_to_user", "the recv copy", fill="#eef7f0", stroke="#3fae6a", tcol="#155", fs=13)
g.arrow(px+276,326, px+244,326, col="#2b7", w=2.4)
g.label(px+150,290,"WARM hit ~178 ns",fs=11,col="#2b7",weight="700")
g.box(px+40, 398, 440, 54, "copy now fast  →  toward the 481 ceiling  (+61%)", None, fill="#eaf5ee", stroke="#2b7", tcol="#063", fs=13.5, r=6)
# center arrow between panels
g.arrow(578, 280, 606, 280, col="#c0392b", w=3)
g.save(sys.argv[1]); print("ok")
