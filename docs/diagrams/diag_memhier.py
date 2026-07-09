import sys; sys.path.insert(0,"/tmp/scratch/-home-alex-prjs-avb-on-fpga-milan-fpga/e2f37f43-41eb-4959-ab3e-979ecb25f127/scratchpad")
from svglib import SVG
g = SVG(1180, 640, "Memory hierarchy & the three RX levers",
        "dual VexiiRiscv @100 MHz · latencies from the perf-free pointer-chase (tools_lat_mem_rd)")
# central column of hierarchy levels; levers annotated on the right, latency on the left
cx=380; cw=380; x=cx
def lvl(y,h,lb,sub,fill,stroke):
    g.box(x,y,cw,h,lb,sub,fill=fill,stroke=stroke)
# harts
g.box(cx+30,90,150,58,"Hart 0","in-order",fill="#eef3f8",stroke="#33628f",fs=13)
g.box(cx+cw-180,90,150,58,"Hart 1","in-order",fill="#eef3f8",stroke="#33628f",fs=13)
g.arrow(cx+105,148,cx+150,196); g.arrow(cx+cw-105,148,cx+cw-150,196)
# L1 D$ (per hart)
g.box(cx+30,196,150,52,"L1 D$ 16 KB","~36 ns",fill="#f4f7fa",stroke="#7aa0c4",fs=12.5)
g.box(cx+cw-180,196,150,52,"L1 D$ 16 KB","~36 ns",fill="#f4f7fa",stroke="#7aa0c4",fs=12.5)
# refill engine (the non-blocking D$)
ry=280
g.box(cx,ry,cw,68,"",None,fill="#eaf5ee",stroke="#3fae6a",r=8)
g.label(cx+cw/2,ry+20,"REFILL ENGINE  ·  8 outstanding-miss slots",fs=13,col="#155",anchor="middle",weight="700")
# draw 8 slots
for i in range(8):
    sx=cx+30+i*(40)
    g.box(sx,ry+34,30,24,str(i),None,fill="#cdebd7",stroke="#3fae6a",fs=10,r=3,sw=1)
g.arrow(cx+105,248,cx+150,ry-2); g.arrow(cx+cw-105,248,cx+cw-150,ry-2)
# shared L2
l2y=384
g.box(cx,l2y,cw,54,"Shared L2  64 KB","~178 ns   (both harts)",fill="#fdf3e7",stroke="#c98a1e",fs=13.5)
g.arrow(cx+cw/2,ry+64+2,cx+cw/2,l2y-2)
# litedram L2 + DDR3
g.box(cx,468,cw,44,"LiteDRAM L2  8 KB","controller cache",fill="#f6f0fa",stroke="#7a4fa3",fs=12)
g.arrow(cx+cw/2,l2y+54+2,cx+cw/2,468-2)
g.box(cx,540,cw,52,"DDR3-800  DRAM","~340 ns  (→ 1424 ns w/ TLB miss)   ← cold RX payload lives here",fill="#fdecea",stroke="#c0392b",tcol="#7a1c12",fs=13.5)
g.arrow(cx+cw/2,468+44+2,cx+cw/2,540-2)
# ---- LEFT: latency scale ----
g.label(60,80,"LATENCY per access",fs=12,col="#888",weight="700")
for y,t in [(222,"L1  ~36 ns"),(410,"L2  ~178 ns"),(566,"DRAM 340–1424 ns")]:
    g.label(60,y,t,fs=12.5,col="#444")
    g.line(180,y-4,cx-6,y-4,col="#eee",w=1)
# ---- RIGHT: the three levers (card = empty box + top title + bullets) ----
lx=cx+cw+40; lw=300
g.label(lx,80,"THE THREE LEVERS",fs=13,col="#111",weight="700")
def card(y,h,title,tcol,stroke,fill,bullets):
    g.box(lx,y,lw,h,"",None,fill=fill,stroke=stroke,r=8)
    g.label(lx+14,y+20,title,fs=12.5,col=tcol,weight="700")
    for i,(t,c,w) in enumerate(bullets):
        g.label(lx+14,y+40+i*16,t,fs=10.5,col=c,weight=w)
card(96,98,"1 · Non-blocking D$  (refill 1→8)","#155","#3fae6a","#f7fbf8",
     [("• was 1 slot = BLOCKING","#444","400"),("• → 8 slots = up to 8 in flight (MLP)","#444","400"),
      ("  BUT 0 gain ALONE (in-order core)","#c0392b","700"),("  — the slots need a FILLER","#666","400")])
card(206,80,"2 · RPT hardware prefetcher","#124","#1f6fb2","#eef5fb",
     [("• learns the stride, FILLS the slots","#444","400"),("• hides the payload cold read","#444","400"),
      ("  → RX single  207 → 277  (+34%)","#c0392b","700")])
card(298,64,"3 · 64 KB L2  (capacity)","#634","#c98a1e","#fdf6ec",
     [("• cuts the 2-hart capacity misses","#444","400"),("  → RX −P2  238 → 280","#c0392b","700")])
card(374,58,"mlp3 = all three combined","#063","#2b7","#eaf5ee",
     [("RX −P2 = 298 (best) · slots cost 0 BRAM","#155","700")])
card(444,150,"NEXT LEVER · DDIO  (task #15)","#7a1c12","#c0392b","#fdecea",
     [("allocate-on-DMA-write: the RX writer","#444","400"),("lands the payload WARM in L2 / a stash","#444","400"),
      ("so copy_to_user hits cache, not DRAM","#444","400"),("→ removes the 51% cold-read wall","#c0392b","700"),
      ("(the user's original 'network cache')","#666","400")])
g.arrow(lx-4,540,cx+cw+4,556,red=True,w=2)
g.save(sys.argv[1]); print("ok")
