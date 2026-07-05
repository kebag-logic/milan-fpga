#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Generate AVB_SWITCH_DIRECTION.{svg,drawio} — where each proposed change lands in the
current endpoint datapath (AVTP engine, TSO, RSC), what TSO/RSC are, and the 8-port
AVB-switch data plane with its memory-bandwidth reality.

Usage: python3 AVB_SWITCH_DIRECTION.gen.py AVB_SWITCH_DIRECTION && rsvg-convert -o AVB_SWITCH_DIRECTION.png AVB_SWITCH_DIRECTION.svg
Edit THIS generator, not the outputs.
"""
import html, sys

RED=("#FFCDD2","#C62828"); GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0")
GREY=("#ECEFF1","#546E7A"); AMBER=("#FFE0B2","#EF6C00"); PURPLE=("#E1BEE7","#6A1B9A")
CYAN=("#B2EBF2","#00838F")
W,H=1540,975
def esc(s): return html.escape(s)
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
   '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#37474F"/></marker>'
   '<marker id="g" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#2E7D32"/></marker></defs>']
boxes=[]
def box(x,y,w,h,fill,stroke,title,lines,tfs=12.5,lfs=11):
    boxes.append((x,y,w,h,fill,stroke,title,lines))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    o.append(f'<text x="{x+w/2}" y="{y+17}" font-size="{tfs}" font-weight="bold" fill="#212121" text-anchor="middle">{esc(title)}</text>')
    yy=y+32
    for ln in lines:
        o.append(f'<text x="{x+w/2}" y="{yy}" font-size="{lfs}" fill="#37474F" text-anchor="middle">{esc(ln)}</text>'); yy+=14
def arrow(x1,y1,x2,y2,label=None,color="#37474F",ly=None,marker="a"):
    o.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.2" fill="none" marker-end="url(#{marker})"/>')
    if label: o.append(f'<text x="{(x1+x2)/2}" y="{ly or (y1+y2)/2-7}" font-size="11" fill="{color}" text-anchor="middle">{esc(label)}</text>')
def text(x,y,s,fs=13,color="#263238",bold=0,anchor=None):
    b=' font-weight="bold"' if bold else ""
    an=f' text-anchor="{anchor}"' if anchor else ""
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{color}"{b}{an}>{esc(s)}</text>')
def badge(x,y,label,fill="#2E7D32"):
    o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}"/>')
    o.append(f'<text x="{x}" y="{y+4}" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">{esc(label)}</text>')

text(24,34,"From 1-NIC endpoint to an 8-port AVB switch — where each change lands",20,"#263238",1)
text(24,55,"MTU stays 1500 everywhere; the CPU leaves the per-packet path — that is the whole architecture",12,"#546E7A")

# ---- panel 1: current endpoint + change hooks ----
text(24,86,"① TODAY'S ENDPOINT DATAPATH + the three hooks (A = AVTP engine, T = TSO, R = RSC)",14,"#1565C0",1)
y=100
box( 24,y,120,74,GREY[0],GREY[1],"CPU / Linux","sockets|PipeWire".split("|"))
box(184,y,150,74,GREEN[0],GREEN[1],"TX ring DMA","AXI read bursts|(done tonight)".split("|"))
box(374,y,190,74,AMBER[0],AMBER[1],"datapath (50 MHz SV)","classifier -> CBS queues|-> PTP ts -> arbiter".split("|"))
box(604,y,130,74,GREY[0],GREY[1],"MAC + PHY","GMII 1G".split("|"))
box(774,y,80,74,GREY[0],GREY[1],"wire","1500 B".split("|"))
arrow(144,y+37,180,y+37); arrow(334,y+37,370,y+37); arrow(564,y+37,600,y+37); arrow(734,y+37,770,y+37)
y2=y+92
box(184,y2,150,74,GREEN[0],GREEN[1],"RX ring DMA","drop-FIFO ingress +|AXI bursts + csum ✓".split("|"))
box(374,y2,190,74,AMBER[0],AMBER[1],"datapath RX","PTP ts -> classifier|-> filter".split("|"))
box(604,y2,130,74,GREY[0],GREY[1],"MAC + PHY","".split("|"))
arrow(180,y2+37,148,y2+37); arrow(370,y2+37,338,y2+37); arrow(600,y2+37,568,y2+37); arrow(770,y2+37,738,y2+37)
# hooks: T lands in the TX ring reader, R in the RX ingress FIFO, A off the classifier
badge(330,y+6,"T","#C62828")
badge(330,y2+6,"R","#EF6C00")
text(24,y2+92,"T = TSO slots into the TX ring reader   ·   R = RSC slots into the RX ingress drop-FIFO   ·   both detailed in ② — the wire keeps MTU 1500",11.5,"#546E7A")
badge(940,y+50,"A","#2E7D32")
box(880,y+66,300,118,GREEN[0],GREEN[1],"AVTP stream engine (NEW block)",
 ["taps the classifier: matched stream IDs never",
  "reach the ring/stack. RX: strip AVTP, write raw",
  "samples + presentation ts into per-stream sample",
  "rings (PipeWire mmaps; wakes per PERIOD ~375/s,",
  "not per packet 8000/s). TX: samples -> AVTP",
  "frames + gPTP ts, CBS-shaped. CPU media cost ~0."])
arrow(564,y+64,880,y+110,None,"#2E7D32",None,"g")

# ---- panel 2: TSO + RSC explainer ----
ey=y2+116
text(24,ey,"② TSO + RSC in one line each — the wire NEVER sees anything but 1500 B",14,"#EF6C00",1)
box( 40,ey+14,710,96,GREY[0],GREY[1],"TSO — TCP Segmentation Offload (TX)",
 ["the stack builds ONE 64 KB TCP super-packet and traverses TCP/IP/qdisc/driver ONCE;",
  "hardware slices it into ~43 wire frames of 1500 B, cloning the headers and fixing",
  "IP len/id, TCP seq/flags and both checksums per slice.",
  "-> per-packet stack cost /43 at unchanged wire MTU. (Every commercial NIC does this.)"])
box(790,ey+14,710,96,GREY[0],GREY[1],"RSC/LRO — Receive Segment Coalescing (RX)",
 ["hardware recognises consecutive in-order segments of the same TCP flow and merges",
  "them into ONE large frame (up to 64 KB) before the driver sees it; flushed on a",
  "sequence gap, PSH/FIN, other-flow interleave, or a short timer.",
  "-> the stack pays once per 64 KB — the hardware twin of what GRO does in software."])

# ---- panel 3: switch ----
sy=ey+140
text(24,sy,"③ THE 8-PORT AVB SWITCH — forwarding lives ENTIRELY in fabric; the endpoint above becomes the CPU port",14,"#6A1B9A",1)
sy2=sy+16
for i in range(8):
    yy = sy2 + i*40
    box(40, yy, 150, 34, GREY[0], GREY[1], f"port {i}: MAC + PTP ts", [], tfs=11)
    arrow(190, yy+17, 226, yy+17)
box(230,sy2,190,314,BLUE[0],BLUE[1],"per-port ingress",
 ["PCP classify (802.1Q)","+ TCAM dst-MAC lookup","(hdl/common/tcam.sv ✓)","+ SRP stream police","","learning: CPU writes","TCAM via CSR"])
arrow(420,sy2+157,456,sy2+157)
box(460,sy2,250,314,CYAN[0],CYAN[1],"shared-BRAM switch fabric",
 ["output-queued, segmented","shared buffer 256-512 KB BRAM","","aggregate need: 8x1G in +","8x1G out = 2 GB/s sustained","= 128-bit @ 125-200 MHz","internal bus - comfortable in","fabric, IMPOSSIBLE via DDR3","","CBS bounds AVB queue depth,","so BRAM suffices; BE spills","-> drop (counted), never DRAM"])
arrow(710,sy2+157,746,sy2+157)
box(750,sy2,190,314,PURPLE[0],"#6A1B9A","per-port egress",
 ["8 queues x CBS shaper","(credit_based_shaper.sv ✓)","","class A/B shaped,","best-effort strict-low","","gPTP: per-port ts ✓","-> transparent-clock","residence-time correction"])
for i in range(8):
    yy = sy2 + i*40
    arrow(940, yy+17, 976, yy+17)
    box(980, yy, 150, 34, GREY[0], GREY[1], f"port {i}: MAC + PHY", [], tfs=11)
box(1170,sy2,330,150,GREEN[0],GREEN[1],"CPU port (= the whole endpoint, panel ①)",
 ["the existing rings/datapath attach to the fabric",
  "as internal port 8. CPU sees ONLY:",
  "gPTP event frames (servo), MSRP/MVRP, AVDECC,",
  "management. It touches ZERO forwarded frames -",
  "the 100 MHz RV64 is comfortably enough for a",
  "full Milan control plane."])
box(1170,sy2+164,330,150,AMBER[0],AMBER[1],"hardware reality (AX7101 = ONE PHY)",
 ["8 external ports need new I/O: the xc7a100t has",
  "4 GTP transceivers -> 2 lanes of QSGMII = 8x1G",
  "via two quad PHYs (daughter board), or a new",
  "carrier (Artix-200T/Kintex) for margin: 8 MACs +",
  "fabric + 8x8 CBS queues will crowd the 100T.",
  "Prototype path: 2-3 ports on GTP SGMII first."])

# ---- panel 4: memory answer ----
my=sy2+340
text(24,my,"④ 'WOULD A WIDER MEMORY BUS HELP?'",14,"#C62828",1)
box( 40,my+14,710,104,GREY[0],GREY[1],"endpoint today: NO",
 ["the socket path is CPU-bound: at 92 Mbit/s the DMA moves ~12 MB/s through",
  "DDR3-800 x16 (~1.2 GB/s effective) = <2 % utilisation. Widening the bus",
  "changes nothing; the 100 MHz core saturates first (measured ~86 % busy).",
  "Telemetry: 0 RX stalls at every stage across 35 M frames."])
box(790,my+14,710,104,RED[0],RED[1],"switch forwarding through DRAM: NEVER",
 ["8 ports store-and-forward via DRAM would need ~2 GB/s sustained + CPU + refresh",
  "arbitration — over the DDR3-800 x16 ceiling and latency-jittery (AVB latency",
  "guarantees die). The fix is not a wider DRAM bus: it is keeping forwarding in",
  "on-chip BRAM (panel ③) where 2 GB/s is one 128-bit internal path. DRAM stays",
  "for the CPU + control plane only."])
o.append('</svg>')

def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=11,bold=0):
        cid[0]+=1
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={fs};"
               f"verticalAlign=top;spacingTop=4;"+("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="n{cid[0]}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    add(20,10,1100,30,"Endpoint -> 8-port AVB switch: change hooks (AVTP/TSO/RSC), fabric forwarding, memory reality","none","none",16,1)
    for (x,y,w,h,fill,stroke,title,lines) in boxes:
        add(x,y,w,h,title+("\n"+"\n".join(lines) if lines else ""),fill,stroke)
    return (f'<mxfile host="app.diagrams.net"><diagram name="AVB_SWITCH_DIRECTION">'
            f'<mxGraphModel dx="1400" dy="900" grid="0" page="1" pageWidth="{W}" pageHeight="{H}">'
            f'<root>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1] if len(sys.argv)>1 else "AVB_SWITCH_DIRECTION"
open(base+".svg","w").write("\n".join(o))
open(base+".drawio","w").write(drawio())
print("wrote",base+".svg",base+".drawio")
