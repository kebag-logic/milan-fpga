#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Generate docs/TX_STARVATION_FIX.{svg,drawio} — the TX-silence root cause + fix diagram.

Usage: python3 docs/TX_STARVATION_FIX.gen.py docs/TX_STARVATION_FIX
       rsvg-convert -o docs/TX_STARVATION_FIX.png docs/TX_STARVATION_FIX.svg
Edit THIS generator, not the outputs.
"""
import html, sys

RED=("#FFCDD2","#C62828"); GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0")
GREY=("#ECEFF1","#546E7A"); AMBER=("#FFE0B2","#EF6C00"); PURPLE=("#E1BEE7","#6A1B9A")

W,H = 1500, 892
def esc(s): return html.escape(s)

o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">']
o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
o.append(f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#37474F"/></marker>'
         f'<marker id="r" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#C62828"/></marker></defs>')

boxes=[]   # collect for drawio: (x,y,w,h,fill,stroke,title,lines,bold)
def box(x,y,w,h,fill,stroke,title,lines,fs=12,tfs=13):
    boxes.append((x,y,w,h,fill,stroke,title,lines))
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    o.append(f'<text x="{x+w/2}" y="{y+19}" font-size="{tfs}" font-weight="bold" fill="#212121" text-anchor="middle">{esc(title)}</text>')
    yy=y+36
    for ln in lines:
        o.append(f'<text x="{x+w/2}" y="{yy}" font-size="{fs}" fill="#37474F" text-anchor="middle">{esc(ln)}</text>')
        yy+=15
def arrow(x1,y1,x2,y2,color="#37474F",m="a",dash=None,label=None,lx=None,ly=None):
    d=f' stroke-dasharray="6 4"' if dash else ""
    o.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2.4" fill="none" marker-end="url(#{m})"{d}/>')
    if label:
        o.append(f'<text x="{lx or (x1+x2)/2}" y="{ly or (y1+y2)/2-7}" font-size="11.5" fill="{color}" text-anchor="middle">{esc(label)}</text>')
def text(x,y,s,fs=13,color="#263238",bold=0,anchor="start"):
    b=' font-weight="bold"' if bold else ""
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{color}"{b} text-anchor="{anchor}">{esc(s)}</text>')

text(28,38,"TX-to-wire silence — root cause & fix (measured on silicon, 2026-07-04)",22,"#263238",1)
text(28,62,"symptom: fabric counters perfect (tx_dma=tx_dp=tx_core=tx_wire), peer i210 sees NOTHING — no rx, no CRC errors, empty promisc tcpdump",12.5,"#546E7A")

# ---- Panel 1: the broken pipeline ----
text(28,100,"① WHAT HAPPENED — a cut-through MAC fed by a source slower than the wire",15,"#C62828",1)
y0=118
box( 28,y0,150,88,GREY[0],GREY[1],"TX DMA","Wishbone reads|DRAM wait states|→ BURSTY".split("|"))
box(218,y0,150,88,GREY[0],GREY[1],"Milan datapath","50 MHz CDC|classifier/CBS|(cut-through)".split("|"))
box(408,y0,168,88,RED[0],RED[1],"LiteEthMACCore","BARE core =|CUT-THROUGH|(no frame buffer!)".split("|"))
box(616,y0,178,88,RED[0],RED[1],"GMII PHY TX","tx_en = valid|cycle-by-cycle|NO mid-frame pause".split("|"))
box(834,y0,158,88,GREY[0],GREY[1],"RTL8211E","sees tx_en glitch|→ aborts frame|→ emits fragment".split("|"))
box(1032,y0,180,88,RED[0],RED[1],"peer i210","fragment = PCS noise|dropped WITHOUT|any counter ➜ SILENCE".split("|"))
arrow(178,y0+44,214,y0+44); arrow(368,y0+44,404,y0+44,label="< 1 Gbps",ly=y0+34)
arrow(576,y0+44,612,y0+44,"#C62828","r",label="valid BUBBLE",ly=y0+34)
arrow(794,y0+44,830,y0+44,"#C62828","r",label="tx_en glitch",ly=y0+34)
arrow(992,y0+44,1028,y0+44,"#C62828","r")

# waveform strip
wy=y0+118
text(28,wy+12,"tx_en on the wire (broken):",12.5,"#C62828",1)
o.append(f'<path d="M240 {wy+18} h60 v-14 h70 v14 h24 v-14 h60 v14 h20 v-14 h90 v14 h180" stroke="#C62828" stroke-width="2.5" fill="none"/>')
text(510,wy+2,"gaps INSIDE the frame = fragments",11.5,"#C62828")
text(760,wy+12,"sim proof: starved source → 6 bubbles/frame; dense source → 0  (sim_tx64.py)",12,"#546E7A")

# ---- Panel 2: why it hid ----
py=wy+44
text(28,py,"② WHY IT HID — two other bugs stacked on top",15,"#EF6C00",1)
box( 28,py+14,440,92,AMBER[0],AMBER[1],"mask #1 — the last_be truncation bug",
    ["ungated last_be cut every frame to 8 bytes at the LastBE stage;",
     "padding + CRC are then LOCALLY generated in eth_tx",
     "→ immune to source bubbles → 'worked' (truncated!)"])
box(496,py+14,440,92,AMBER[0],AMBER[1],"mask #2 — dst-keyed counters lie",
    ["peer rx_broadcast counts a truncated frame as happily as",
     "a full one (dst MAC survives in beat 0) — 'verified TX'",
     "twice on frames that carried 8 real bytes"])
box(964,py+14,440,92,AMBER[0],AMBER[1],"mask #3 — non-coherent DMA builds",
    ["--coherent-dma is NOT implied by --all-blocks: TX read stale",
     "DRAM → garbage dst-MAC frames that the peer address-filters",
     "silently → looked like a PHY bug; wasn't"])

# ---- Panel 3: the wrong turns (measured away) ----
ry=py+130
text(28,ry,"③ RULED OUT BY MEASUREMENT — the red herrings",15,"#6A1B9A",1)
box( 28,ry+14,300,74,PURPLE[0],PURPLE[1],"gtx clock phase (for SILENCE)",
    ["edge vs 180°: both silent — phase was","NOT the silence bug. (It IS the margin","fix once FFs are IOB-packed — see ⑤)"])
box(352,ry+14,300,74,PURPLE[0],PURPLE[1],"TX FF placement",
    ["fabric X14 vs OLOGIC (IOB-packed,","DCP-verified): both silent —","placement wasn't the killer"])
box(676,ry+14,360,74,PURPLE[0],PURPLE[1],"XDC trap found on the way",
    ["set_property inside if {...} is SILENTLY","ignored — XDC executes no TCL control flow.","Verify constraints in the routed .dcp"])
box(1060,ry+14,344,74,PURPLE[0],PURPLE[1],"sim harness trap",
    ["a sys-domain monitor on an eth_tx stream","ALIASES (samples 8ns data at 10ns = drops","1-in-5) — run monitors in the right domain"])

# ---- Panel 4: the fix ----
fy=ry+112
text(28,fy,"④ THE FIX — store-and-forward: release a frame only when it is COMPLETELY buffered",15,"#2E7D32",1)
y1=fy+16
box( 28,y1,150,88,GREY[0],GREY[1],"TX DMA","bursty|(unchanged)".split("|"))
box(218,y1,150,88,GREY[0],GREY[1],"Milan datapath","bursty|(unchanged)".split("|"))
box(408,y1,190,88,GREEN[0],GREEN[1],"PacketFIFO 4 KB","store-and-forward|releases only|COMPLETE frames".split("|"))
box(638,y1,168,88,BLUE[0],BLUE[1],"LiteEthMACCore","cut-through is now|fine: its source is|gapless by construction".split("|"))
box(846,y1,158,88,BLUE[0],BLUE[1],"GMII PHY TX","tx_en solid high|for every frame".split("|"))
box(1044,y1,170,88,GREEN[0],GREEN[1],"peer i210","full 64-byte payload|in tcpdump +|counters move".split("|"))
arrow(178,y1+44,214,y1+44); arrow(368,y1+44,404,y1+44,label="bubbles OK here",ly=y1+34)
arrow(598,y1+44,634,y1+44,"#2E7D32",label="≥ 1 Gbps, gapless",ly=y1+34)
arrow(806,y1+44,842,y1+44,"#2E7D32"); arrow(1004,y1+44,1040,y1+44,"#2E7D32")
wy2=y1+114
text(28,wy2+12,"tx_en on the wire (fixed):",12.5,"#2E7D32",1)
o.append(f'<path d="M240 {wy2+18} h40 v-14 h180 v14 h60 v-14 h180 v14 h100" stroke="#2E7D32" stroke-width="2.5" fill="none"/>')
text(560,wy2+2,"one clean burst per frame + inter-frame gap",11.5,"#2E7D32")
text(830,wy2+12,"MilanMAC: PacketFIFO(eth_phy_description(64), payload_depth=512) → core.sink",12,"#546E7A")

# ---- Panel 5: rules ----
ky=wy2+40
text(28,ky,"⑤ RULES THIS BURNS IN",15,"#1565C0",1)
rules=[
 "GMII/RGMII MAC cores need a gapless TX source — bare LiteEthMACCore is cut-through; buffer frames (PacketFIFO) or use full LiteEthMAC (SRAM buffers).",
 "Prove TX with raw payload capture (tcpdump -e -xx) — never with dst-keyed counters; a truncated or garbage frame can still count.",
 "'Peer sees nothing at all' (no CRC errors either) means framing/PCS-level breakage or filtered garbage — not sampling margin.",
 "Verify every constraint in the routed .dcp and every sim monitor's clock domain — both lied once today.",
 "--coherent-dma is mandatory for the NIC; it is NOT implied by --all-blocks.",
 "With IOB-packed TX FFs (skew≈0) use --gtx-tx-invert: edge-aligned = hold-marginal (25-40% corrupt frames); mid-bit = 20/20 pings, 0 CRC errors.",
 "Linux skbs are IP-aligned (data%8==2) — an 8-byte-word DMA needs an aligned bounce buffer or frames shift 2 bytes on the wire.",
]
yy=ky+22
for r in rules:
    o.append(f'<circle cx="36" cy="{yy-4}" r="3" fill="#1565C0"/>')
    text(48,yy,r,12.5); yy+=21
o.append('</svg>')

# ---------- drawio ----------
def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=11,bold=0):
        cid[0]+=1
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={fs};"
               f"verticalAlign=top;spacingTop=4;"+("fontStyle=1;" if bold else ""))
        cells.append(f'<mxCell id="n{cid[0]}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    add(20,10,900,30,"TX-to-wire silence — root cause & fix (silicon, 2026-07-04)","none","none",16,1)
    for (x,y,w,h,fill,stroke,title,lines) in boxes:
        add(x,y,w,h,title+"\n"+"\n".join(lines),fill,stroke)
    body="".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="tx-starvation-fix">'
            f'<mxGraphModel dx="1400" dy="1000" grid="0" page="1" pageWidth="{W}" pageHeight="{H}">'
            f'<root>{body}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1] if len(sys.argv)>1 else "TX_STARVATION_FIX"
open(base+".svg","w").write("\n".join(o))
open(base+".drawio","w").write(drawio())
print("wrote",base+".svg",base+".drawio")
