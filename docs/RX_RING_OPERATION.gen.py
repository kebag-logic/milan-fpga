#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Generate RX_RING_OPERATION.{svg,drawio} — how the v2 RX ring DMA works end-to-end:
ingress drop-FIFO, AXI burst drain FSM, the ring memory layout (header/seq/wrap,
wr/rd pointers, commit rule) and the kl-eth driver walk.

Usage: python3 RX_RING_OPERATION.gen.py RX_RING_OPERATION && rsvg-convert -o RX_RING_OPERATION.png RX_RING_OPERATION.svg
Edit THIS generator, not the outputs.
"""
import html, sys

RED=("#FFCDD2","#C62828"); GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0")
GREY=("#ECEFF1","#546E7A"); AMBER=("#FFE0B2","#EF6C00"); PURPLE=("#E1BEE7","#6A1B9A")
W,H=1500,900
def esc(s): return html.escape(s)
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
   '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#37474F"/></marker>'
   '<marker id="r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#C62828"/></marker></defs>']
boxes=[]
def box(x,y,w,h,fill,stroke,title,lines,tfs=13):
    boxes.append((x,y,w,h,fill,stroke,title,lines))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    o.append(f'<text x="{x+w/2}" y="{y+19}" font-size="{tfs}" font-weight="bold" fill="#212121" text-anchor="middle">{esc(title)}</text>')
    yy=y+36
    for ln in lines:
        o.append(f'<text x="{x+w/2}" y="{yy}" font-size="11.5" fill="#37474F" text-anchor="middle">{esc(ln)}</text>'); yy+=15
def seg(x,y,w,h,fill,stroke,label,sub=None):
    # a ring segment (flat box, small font, centered)
    boxes.append((x,y,w,h,fill,stroke,label,[sub] if sub else []))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
    o.append(f'<text x="{x+w/2}" y="{y+h/2-2}" font-size="11" font-weight="bold" fill="#212121" text-anchor="middle">{esc(label)}</text>')
    if sub: o.append(f'<text x="{x+w/2}" y="{y+h/2+13}" font-size="10" fill="#37474F" text-anchor="middle">{esc(sub)}</text>')
def arrow(x1,y1,x2,y2,label=None,color="#37474F",ly=None,marker="a"):
    o.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.2" fill="none" marker-end="url(#{marker})"/>')
    if label: o.append(f'<text x="{(x1+x2)/2}" y="{ly or (y1+y2)/2-7}" font-size="11" fill="{color}" text-anchor="middle">{esc(label)}</text>')
def text(x,y,s,fs=13,color="#263238",bold=0,anchor=None):
    b=' font-weight="bold"' if bold else ""
    an=f' text-anchor="{anchor}"' if anchor else ""
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{color}"{b}{an}>{esc(s)}</text>')

text(24,36,"RX ring DMA v2 — how it works (RingDMAWriter in milan_soc.py ⇄ kl-eth ring walk)",20,"#263238",1)
text(24,58,"one shared contract: 7 CSRs + the ring memory format; HW commits whole frames, SW consumes and releases space",12,"#546E7A")

# ---- ① gateware pipeline ----
text(24,92,"① GATEWARE: always-ready ingress -> store-and-forward -> AXI bursts",14.5,"#1565C0",1)
y=108
box( 24,y,170,92,GREY[0],GREY[1],"datapath m_axis_rx","64-bit AXIS @50 MHz|(frames, tlast)".split("|"))
box(234,y,120,92,GREY[0],GREY[1],"CDC","async FIFO|50 -> 100 MHz".split("|"))
box(394,y,250,92,GREEN[0],GREEN[1],"ingress (sink.ready == 1)","frame START decision:|free < 256 beats? len queue full?|disabled?  -> swallow WHOLE frame|else store beats; push len at tlast".split("|"),12.5)
box(684,y,210,92,BLUE[0],BLUE[1],"BRAM buffers","data FIFO 2048 x 64 b (16 KB)|+ length FIFO 64 x 9 b|(a frame is complete before|its length is visible)".split("|"),12.5)
box(934,y,250,92,AMBER[0],AMBER[1],"drain FSM (burst engine)","pops one length, checks ring fit,|streams header+payload as|INCR bursts <= 16 beats,|split at ring-wrap + 4 KB".split("|"),12.5)
box(1224,y,252,92,GREY[0],GREY[1],"NaxRiscv dma_bus (AXI4)","coherent: snoops L1/L2,|CPU sees DMA data without|cache maintenance|B response = write done".split("|"),12.5)
arrow(194,y+46,230,y+46); arrow(354,y+46,390,y+46); arrow(644,y+46,680,y+46); arrow(894,y+46,930,y+46); arrow(1184,y+46,1220,y+46,"AW/W/B")
arrow(519,y+92,519,y+124,"drop: dropped++",RED[1],None,"r")
arrow(1059,y+92,1059,y+124,"ring full: DISCARD, dropped++",RED[1],None,"r")

# ---- ② FSM ----
fy=y+152
text(24,fy,"② the drain FSM, per frame",14.5,"#EF6C00",1)
fyy=fy+14
box( 40,fyy,190,84,GREY[0],GREY[1],"IDLE","length FIFO non-empty?|fit: free >= 8+len+8|no fit / disabled -> DISCARD".split("|"),12.5)
box(280,fyy,190,84,AMBER[0],AMBER[1],"AW","addr = base+((wr+done)&mask)|len = blen-1, INCR, 8 B/beat|blen = min(rem, 16, wrap, 4K)".split("|"),12.5)
box(520,fyy,190,84,AMBER[0],AMBER[1],"W  (x blen)","beat 0 of frame = HEADER|{rsvd, seq, len_bytes}|then payload from data FIFO".split("|"),12.5)
box(760,fyy,190,84,GREEN[0],GREEN[1],"WAIT_B","all B responses in|(outstanding == 0) ->|COMMIT: wr += 8+len; seq++".split("|"),12.5)
box(1000,fyy,190,84,RED[0],RED[1],"DISCARD","pop len beats from FIFO|dropped++ -> IDLE|(committed data untouched)".split("|"),12.5)
arrow(230,fyy+42,276,fyy+42,"fit"); arrow(470,fyy+42,516,fyy+42,"aw.ready"); arrow(710,fyy+42,756,fyy+42,"last beat")
arrow(615,fyy+84,615,fyy+112); arrow(615,fyy+112,375,fyy+112); arrow(375,fyy+112,375,fyy+88,"more bursts")
arrow(855,fyy+84,855,fyy+120); arrow(855,fyy+120,135,fyy+120); arrow(135,fyy+120,135,fyy+88,"next frame")
o.append(f'<path d="M135 {fyy} L135 {fyy-8} L1095 {fyy-8} L1095 {fyy-2}" stroke="#C62828" stroke-width="2.2" fill="none" marker-end="url(#r)"/>')
text(640,fyy-13,"no fit / disabled",11,"#C62828",0,"middle")
box(1240,fyy,236,84,PURPLE[0],"#6A1B9A","why commit-after-B","software polls wr_ptr; it moves|only when the frame is fully in|DRAM -> a partial frame is|never observable".split("|"),12.5)

# ---- ③ ring memory ----
ry=fyy+164
text(24,ry,"③ the ring in DRAM (base, size = mask+1 = 256 KB; all offsets byte, 8-aligned)",14.5,"#2E7D32",1)
ryy=ry+36
# ring bar
bx, bw, bh = 40, 1200, 46
seg(bx,      ryy, 60,bh,GREY[0],GREY[1],"consumed","(free)")
seg(bx+60,   ryy, 40,bh,GREEN[0],GREEN[1],"hdr","seq=41")
seg(bx+100,  ryy,150,bh,GREEN[0],GREEN[1],"payload 1514 B","(stored as 1520)")
seg(bx+250,  ryy, 40,bh,GREEN[0],GREEN[1],"hdr","seq=42")
seg(bx+290,  ryy, 90,bh,GREEN[0],GREEN[1],"payload 176 B","")
seg(bx+380,  ryy, 40,bh,AMBER[0],AMBER[1],"hdr","seq=43")
seg(bx+420,  ryy,140,bh,AMBER[0],AMBER[1],"being written (bursts)","wr_ptr NOT yet advanced")
seg(bx+560,  ryy,420,bh,GREY[0],GREY[1],"free","(>= 8 spare kept: wr never catches rd)")
seg(bx+980,  ryy,110,bh,GREEN[0],GREEN[1],"tail of frame seq=40","wraps ->")
seg(bx+1090, ryy,110,bh,GREY[0],GREY[1],"","")
text(bx+1090+55,ryy+bh/2+2,"(same frame continues at offset 0)",10,"#546E7A","middle")
arrow(bx+60,ryy+bh+26,bx+60,ryy+bh+2,None,BLUE[1])
text(bx+70,ryy+bh+24,"rd_ptr (SW writes back)",11,BLUE[1])
arrow(bx+380,ryy-16,bx+380,ryy-2,None,"#2E7D32")
text(bx+390,ryy-12,"wr_ptr (HW commit point)",11,"#2E7D32")
# header format + rules
hy2=ryy+86
box( 40,hy2,460,86,BLUE[0],BLUE[1],"header word (8 B, written as burst beat 0)",
 ["bits [15:0]  len   — payload bytes, 8-aligned (padded)",
  "bits [31:16] seq   — increments per committed frame",
  "bits [63:32] rsvd — 0"])
box(540,hy2,440,86,GREY[0],GREY[1],"space rule",
 ["a frame needs 8 + len + 8 spare bytes free:",
  "free = size - ((wr - rd) & mask); no fit -> whole-frame",
  "DISCARD (never a partial write, never overwrite)"])
box(1020,hy2,456,86,GREY[0],GREY[1],"wrap rule",
 ["frames may cross the ring end: addresses are masked,",
  "bursts are split at the boundary; software does the",
  "mirror: two memcpys when rd + len > size"])

# ---- ④ driver ----
dy=hy2+118
text(24,dy,"④ DRIVER (kl-eth NAPI poll) — the consumer side of the same contract",14.5,"#6A1B9A",1)
dyy=dy+14
box( 40,dyy,300,96,GREY[0],GREY[1],"poll (adaptive 20/200 us)","read RING_WR (one CSR read)|frames pending if rd != wr|mirror RING_DROPPED into|rx_missed_errors".split("|"),12.5)
box(380,dyy,300,96,BLUE[0],BLUE[1],"walk headers rd -> wr","hdr = ring[rd]; sanity: 0 < len|<= 2048 and len % 8 == 0|(else desync recovery: rd = wr,|count rx_length_errors)".split("|"),12.5)
box(720,dyy,300,96,GREEN[0],GREEN[1],"copy out + deliver","memcpy to skb (2 copies if the|frame wraps), strip pad via|eth_type_trans + IP length|netif_receive_skb".split("|"),12.5)
box(1060,dyy,300,96,PURPLE[0],"#6A1B9A","release space","rd = (rd + 8 + len) & mask|write back RING_RD ->|HW sees the freed bytes|on its next fit check".split("|"),12.5)
arrow(340,dyy+48,376,dyy+48); arrow(680,dyy+48,716,dyy+48); arrow(1020,dyy+48,1056,dyy+48)
box(40,dyy+116,1320,58,GREY[0],GREY[1],"CSR block (kl-eth regs.h names, byte offsets in the dma-rx window @ 0xf000301c)",
 ["+0x00 RING_BASE_HI  +0x04 RING_BASE_LO  +0x08 RING_MASK  +0x0c RING_WR (RO)  +0x10 RING_RD (RW)  +0x14 RING_EN  +0x18 RING_DROPPED (RO)",
  "identical footprint to the old simple-mode block -> device tree and driver probe unchanged"])
o.append('</svg>')

def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=11,bold=0):
        cid[0]+=1
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={fs};"
               f"verticalAlign=top;spacingTop=4;"+("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="n{cid[0]}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    add(20,10,1100,30,"RX ring DMA v2 — how it works (gateware writer + ring format + kl-eth walk)","none","none",16,1)
    for (x,y,w,h,fill,stroke,title,lines) in boxes:
        add(x,y,w,h,title+("\n"+"\n".join(lines) if lines else ""),fill,stroke)
    return (f'<mxfile host="app.diagrams.net"><diagram name="RX_RING_OPERATION">'
            f'<mxGraphModel dx="1400" dy="900" grid="0" page="1" pageWidth="{W}" pageHeight="{H}">'
            f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1] if len(sys.argv)>1 else "RX_RING_OPERATION"
open(base+".svg","w").write("\n".join(o))
open(base+".drawio","w").write(drawio())
print("wrote",base+".svg",base+".drawio")
