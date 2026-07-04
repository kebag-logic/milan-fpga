#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Generate RX_RING_DMA.{svg,drawio} — why RX lost every large frame (drain-rate deficit
on the coherent bus) and how the v2 ring writer (drop-FIFO ingress + AXI bursts) fixes it.

Usage: python3 RX_RING_DMA.gen.py RX_RING_DMA && rsvg-convert -o RX_RING_DMA.png RX_RING_DMA.svg
Edit THIS generator, not the outputs. Numbers measured on silicon 2026-07-04.
"""
import html, sys

RED=("#FFCDD2","#C62828"); GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0")
GREY=("#ECEFF1","#546E7A"); AMBER=("#FFE0B2","#EF6C00"); PURPLE=("#E1BEE7","#6A1B9A")
W,H=1500,620
def esc(s): return html.escape(s)
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
   '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#37474F"/></marker></defs>']
boxes=[]
def box(x,y,w,h,fill,stroke,title,lines,tfs=13):
    boxes.append((x,y,w,h,fill,stroke,title,lines))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    o.append(f'<text x="{x+w/2}" y="{y+19}" font-size="{tfs}" font-weight="bold" fill="#212121" text-anchor="middle">{esc(title)}</text>')
    yy=y+36
    for ln in lines:
        o.append(f'<text x="{x+w/2}" y="{yy}" font-size="11.5" fill="#37474F" text-anchor="middle">{esc(ln)}</text>'); yy+=15
def arrow(x1,y1,x2,y2,label=None,color="#37474F",ly=None):
    o.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.2" fill="none" marker-end="url(#a)"/>')
    if label: o.append(f'<text x="{(x1+x2)/2}" y="{ly or (y1+y2)/2-7}" font-size="11" fill="{color}" text-anchor="middle">{esc(label)}</text>')
def text(x,y,s,fs=13,color="#263238",bold=0):
    b=' font-weight="bold"' if bold else ""
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{color}"{b}>{esc(s)}</text>')

text(24,36,"RX ring DMA — the drain-rate deficit that lost EVERY large frame, and the AXI-burst fix",20,"#263238",1)
text(24,58,"measured on silicon 2026-07-04 (AX7101, NaxRiscv 100 MHz sys / 50 MHz datapath, GMII 1 Gbps)",12,"#546E7A")

# ---- panel 1: v1, why it corrupts ----
text(24,92,"① v1 (wishbone ring writer): the wire outruns the DMA INSIDE every large frame",14.5,"#C62828",1)
y=108
box( 24,y,130,88,GREY[0],GREY[1],"wire","1 Gbps|8 B / 64 ns".split("|"))
box(194,y,170,88,GREY[0],GREY[1],"LiteEth MAC RX","eth_rx 125 MHz|CANNOT stall the wire".split("|"))
box(404,y,170,88,RED[0],RED[1],"CDC + dp FIFOs","~70 beats elastic|overflow = beats lost|SILENTLY (incl. last)".split("|"))
box(614,y,190,88,AMBER[0],AMBER[1],"RingDMA v1","1 Wishbone write / beat|adapter waits B each time|~38 sys-cycles / 8 B".split("|"))
box(844,y,200,88,GREY[0],GREY[1],"NaxRiscv dma_bus","coherent (snoops L1/L2)|the port is FULL AXI4 —|wishbone was the adapter".split("|"))
arrow(154,y+44,190,y+44); arrow(364,y+44,400,y+44); arrow(574,y+44,610,y+44,"stalls",RED[1]); arrow(804,y+44,840,y+44)
box(1084,y,392,88,RED[0],RED[1],"measured drain: ~21 MB/s  (need 125)",
 ["telemetry rx_dma: 9,805,345 stalls / 542,240 beats",
  "= 18 stall-cycles per beat @ 50 MHz -> 380 ns/beat",
  "backlog grows ~0.83 beat/beat inside a frame"])

# ---- panel 2: evidence ----
ey=y+112
text(24,ey,"② the failure signature (why it looked like 'RX at rate' but was 'RX any large frame')",14.5,"#EF6C00",1)
box( 40,ey+14,450,96,AMBER[0],AMBER[1],"ping payload sweep (peer->FPGA)",
 ["200/400/600 B: 0% loss   |   800/1000/1200 B: 100% loss",
  "threshold ~700 B frame = the ~70-beat elasticity",
  "small frames fit the FIFOs; large frames overflow mid-frame"])
box(510,ey+14,450,96,RED[0],RED[1],"merged frames (ring desync)",
 ["lost `last` merges two wire frames into one ring frame:",
  "hdr len=2608 B == wr-rd-8 exactly (writer honest, input corrupt)",
  "iperf3 TCP: control OK, bulk 0 B  |  UDP 10M: 0 delivered"])
box(980,ey+14,496,96,GREY[0],GREY[1],"v1 also had a latent stale-data bug",
 ["the wishbone cycle wasn't gated on sink.valid — a mid-frame",
  "bubble wrote stale sink.data as an extra beat. Never hit in",
  "sim (source never bubbled) -> now a regression test."])

# ---- panel 3: v2 ----
fy=ey+134
text(24,fy,"③ v2 (this fix): always-ready drop-FIFO ingress + native AXI4 burst drain",14.5,"#2E7D32",1)
y2=fy+16
box( 24,y2,130,96,GREY[0],GREY[1],"wire","1 Gbps".split("|"))
box(194,y2,180,96,GREY[0],GREY[1],"MAC + CDC + dp","never backpressured|-> can never lose|mid-frame beats".split("|"))
box(414,y2,240,96,GREEN[0],GREEN[1],"ingress frame FIFO (16 KB)","sink.ready == 1 ALWAYS|store-and-forward; drop decision|at frame START, WHOLE frames|dropped++ when full".split("|"))
box(694,y2,250,96,GREEN[0],GREEN[1],"AXI burst engine","length known up front -> header|streams FIRST in the burst chain|16-beat INCR bursts, split at|ring-wrap + 4 KB boundaries".split("|"))
box(984,y2,200,96,BLUE[0],BLUE[1],"dma_bus (AXI4)","bursts amortize the|coherency round trip|~6x fewer transactions".split("|"))
box(1224,y2,252,96,GREEN[0],GREEN[1],"commit rule (ABI unchanged)","wr_ptr moves only after the|LAST B response -> software|never sees a partial frame|seq/len header format identical".split("|"))
arrow(154,y2+48,190,y2+48); arrow(374,y2+48,410,y2+48); arrow(654,y2+48,690,y2+48); arrow(944,y2+48,980,y2+48); arrow(1184,y2+48,1220,y2+48)

# ---- panel 4: invariants ----
iy=y2+120
box( 40,iy,700,104,PURPLE[0],"#6A1B9A","what did NOT change (zero driver/DT churn)",
 ["CSR block: base[64] | mask | wr_ptr | rd_ptr | enable | dropped — same 7 words @0xf000301c",
  "ring format: [8 B header {rsvd,seq,len}] + payload padded to 8 B, frames wrap, sw splits the copy",
  "kl-eth walks the ring exactly as before; overload now = clean whole-frame drops in",
  "rx_missed_errors (RING_DROPPED), never corruption"])
box(780,iy,696,104,GREY[0],GREY[1],"verification",
 ["sim (test_ring_dma.py): content/seq, mid-frame bubbles, slow-drain whole-frame drops,",
  "ring-full discard, wrap + rd-release, 4 KB burst split — ALL PASS, sink.ready monitored ==1",
  "silicon acceptance: large-ping sweep clean, iperf3 -R + UDP envelope, telemetry rx_dma",
  "stalls ~= 0 under load, rx_missed_errors counts drops (not desyncs) at overload"])
o.append('</svg>')

def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=11,bold=0):
        cid[0]+=1
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={fs};"
               f"verticalAlign=top;spacingTop=4;"+("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="n{cid[0]}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    add(20,10,1000,30,"RX ring DMA — drain-rate deficit root cause + AXI-burst fix (silicon 2026-07-04)","none","none",16,1)
    for (x,y,w,h,fill,stroke,title,lines) in boxes:
        add(x,y,w,h,title+"\n"+"\n".join(lines),fill,stroke)
    return (f'<mxfile host="app.diagrams.net"><diagram name="RX_RING_DMA">'
            f'<mxGraphModel dx="1400" dy="900" grid="0" page="1" pageWidth="{W}" pageHeight="{H}">'
            f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1] if len(sys.argv)>1 else "RX_RING_DMA"
open(base+".svg","w").write("\n".join(o))
open(base+".drawio","w").write(drawio())
print("wrote",base+".svg",base+".drawio")
