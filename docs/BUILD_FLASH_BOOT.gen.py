#!/usr/bin/env python3
"""Generate the AX7101 build→flash→boot→verify pipeline as editable .drawio +
rendered .svg. One picture for the integrator: the end-to-end flow that is
otherwise scattered across BUILDING / LITEX_SOC / QSPI_FLASHBOOT / BENCH_TOPOLOGY.
Render PNG: rsvg-convert -w 2400 BUILD_FLASH_BOOT.svg -o BUILD_FLASH_BOOT.png
"""
import html, sys

GREEN =("#E8F5E9","#2E7D32"); ORANGE=("#FFF3E0","#EF6C00")
BLUE  =("#E3F2FD","#1565C0"); PURPLE=("#F3E5F5","#6A1B9A")
RED   =("#FFEBEE","#C62828"); GREY  =("#ECEFF1","#455A64")
def esc(s): return html.escape(s, quote=True)

# (stage, tool, colour, [ (line, is_cmd) ... ])
STAGES = [
 ("1 · BUILD", "dev host · Vivado", GREEN, [
   ("sw/litex/build.sh ax7101", 1),
   ("mandatory: --coherent-dma", 0),
   ("--gtx-tx-invert --all-blocks", 0),
   ("--with-spiflash --flashboot full", 1),
   ("  → pins BITSTREAM COMPRESS", 0),
   ("3×32-thread seed sweep", 0),
   ("GATE: WNS ≥ 0", 0),
 ], "compressed .bit ~1.74 MiB (60% off 3.65)\n+ kernel · dtb · rootfs · opensbi"),
 ("2 · FLASH", "JTAG → QSPI (16 MB)", ORANGE, [
   ("deploy.sh flash  (bitstream @0)", 1),
   ("deploy.sh flash-images", 1),
   ("  matched set, FBI-wrapped", 0),
   ("  per-slot budget + --verify", 0),
   ("openFPGALoader -c ft232", 0),
   ("RULE: flash the WHOLE set —", 0),
   ("a gateware-only load won't boot", 0),
 ], "persistent QSPI image:\nbitstream@0 · kernel · dtb · rootfs"),
 ("3 · BOOT", "on target · self-configures", BLUE, [
   ("power on / power-cycle", 1),
   ("FPGA config-boots from QSPI", 0),
   ("LiteX BIOS → DDR3 init", 0),
   ("linux_flashboot QSPI→DRAM", 0),
   ("OpenSBI (M-mode) → Linux", 0),
   ("S50milan provisions CSRs", 0),
   ("ptp4l · phc2sys · linkmon up", 0),
 ], "buildroot Linux on VexiiRiscv,\nMilan NIC live"),
 ("4 · VERIFY", "on the bench", PURPLE, [
   ("devmem 0x90000000 == 'MILN'", 1),
   ("  (M-A2 first-silicon smoke)", 0),
   ("link up · GM / talker / listener", 0),
   ("CERT 63/63", 1),
   ("behave · TB · audio E2E", 0),
   ("REGISTER_MAP.md = the ABI", 0),
   ("BENCH_TOPOLOGY.md = the rig", 0),
 ], "a validated Milan end-station"),
]
RECOVERY = "Recovery — board wedged or won't boot:  amx-pi powerstrip off 0 && powerstrip on 0  (reverts to the known-good QSPI gateware) · JTAG-load a bitstream to SRAM to test without flashing · never openFPGALoader -f a bitstream onto a kernel-at-0 layout"

X0,Y0=40,150; CW,CG=440,54; HDR=56; RH,RGAP=30,7; PAD=12; OUT_H=64
def stage_h(lines): return HDR+PAD+len(lines)*(RH+RGAP)-RGAP+PAD
maxlines=max(len(s[3]) for s in STAGES)
box_h=stage_h(STAGES[0][3]); box_h=HDR+PAD+maxlines*(RH+RGAP)-RGAP+PAD
col_x=lambda i:X0+i*(CW+CG)
W=col_x(len(STAGES)-1)+CW+X0
out_y=Y0+box_h+22
rec_y=out_y+OUT_H+34
H=rec_y+96

def svg():
    o=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Helvetica,Arial,sans-serif">'%(W,H,W,H)]
    o.append('<defs><marker id="fa" markerWidth="16" markerHeight="16" refX="4" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#455A64"/></marker></defs>')
    o.append('<rect width="%d" height="%d" fill="#FAFAFA"/>'%(W,H))
    o.append('<text x="%d" y="56" font-size="30" font-weight="bold" fill="#263238">Build → Flash → Boot → Verify — the AX7101 pipeline</text>'%X0)
    o.append('<text x="%d" y="88" font-size="15" fill="#546E7A">One flow, four stages. Each stage lists the real commands (bold) and the load-bearing rules. Details: docs/integration/BUILDING · LITEX_SOC · QSPI_FLASHBOOT · findings/BENCH_TOPOLOGY.</text>'%X0)
    o.append('<text x="%d" y="112" font-size="15" fill="#546E7A">The one rule that costs a session if missed: build with --with-spiflash --flashboot full and flash the MATCHED image set together.</text>'%X0)
    for i,(name,tool,(fill,stroke),lines,out) in enumerate(STAGES):
        x=col_x(i)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="2"/>'%(x,Y0,CW,box_h,fill,stroke))
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s"/>'%(x,Y0,CW,HDR,stroke,stroke))
        o.append('<rect x="%d" y="%d" width="%d" height="12" fill="%s"/>'%(x,Y0+HDR-12,CW,stroke))
        o.append('<text x="%d" y="%d" font-size="19" font-weight="bold" fill="#ffffff">%s</text>'%(x+18,Y0+27,esc(name)))
        o.append('<text x="%d" y="%d" font-size="12.5" fill="#ffffff" fill-opacity="0.92">%s</text>'%(x+18,Y0+45,esc(tool)))
        my=Y0+HDR+PAD
        for (ln,cmd) in lines:
            if cmd:
                o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="#263238"/>'%(x+PAD,my,CW-2*PAD,RH))
                o.append('<text x="%d" y="%d" font-size="12.5" font-family="Menlo,Consolas,monospace" fill="#B9F6CA">%s</text>'%(x+PAD+9,my+20,esc(ln)))
            else:
                o.append('<text x="%d" y="%d" font-size="13" fill="#37474F">%s</text>'%(x+PAD+6,my+20,esc(ln)))
            my+=RH+RGAP
        # output chip
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="#ffffff" stroke="%s" stroke-width="1.6" stroke-dasharray="5 3"/>'%(x,out_y,CW,OUT_H,stroke))
        o.append('<text x="%d" y="%d" font-size="11.5" font-weight="bold" fill="%s">OUTPUT</text>'%(x+14,out_y+20,stroke))
        for k,seg in enumerate(out.split("\n")):
            o.append('<text x="%d" y="%d" font-size="12.5" fill="#212121">%s</text>'%(x+14,out_y+38+k*17,esc(seg)))
        # arrow to next
        if i<len(STAGES)-1:
            ax0=x+CW+6; ay=Y0+box_h//2
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#455A64" stroke-width="3.5" marker-end="url(#fa)"/>'%(ax0,ay,ax0+CG-14,ay))
    # recovery banner
    o.append('<rect x="%d" y="%d" width="%d" height="72" rx="10" fill="%s" stroke="%s" stroke-width="2"/>'%(X0,rec_y,W-2*X0,RED[0],RED[1]))
    o.append('<text x="%d" y="%d" font-size="15" font-weight="bold" fill="%s">↩ Recovery — the board is not a brick</text>'%(X0+20,rec_y+26,RED[1]))
    o.append('<text x="%d" y="%d" font-size="12.8" fill="#37474F">amx-pi powerstrip off 0 &amp;&amp; powerstrip on 0  reverts to the known-good QSPI gateware  ·  JTAG-load to SRAM tests a bitstream without flashing</text>'%(X0+20,rec_y+48))
    o.append('<text x="%d" y="%d" font-size="12.8" fill="#37474F">never  openFPGALoader -f  a bitstream onto a kernel-at-0 flash layout  ·  full field log: docs/limitations/TROUBLESHOOTING.md</text>'%(X0+20,rec_y+66))
    o.append('</svg>')
    return "\n".join(o)

def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=13,fw=0,font="#212121",mono=0):
        cid[0]+=1; i=cid[0]
        st=("rounded=1;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontSize=%d;align=left;verticalAlign=top;spacingLeft=10;spacingTop=6;fontColor=%s;"%(fill,stroke,fs,font))+("fontStyle=1;" if fw else "")+("fontFamily=Courier New;" if mono else "")
        cells.append('<mxCell id="n%d" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'%(i,esc(label),st,x,y,w,h))
        return "n%d"%i
    def edge(a,b):
        cid[0]+=1; i=cid[0]
        cells.append('<mxCell id="e%d" style="endArrow=block;html=1;strokeColor=#455A64;strokeWidth=3;" edge="1" parent="1" source="%s" target="%s"><mxGeometry relative="1" as="geometry"/></mxCell>'%(i,a,b))
    add(X0,20,1200,34,"Build → Flash → Boot → Verify — the AX7101 pipeline","none","none",22,1)
    ids=[]
    for i,(name,tool,(fill,stroke),lines,out) in enumerate(STAGES):
        x=col_x(i)
        body="\n".join(("$ "+ln if cmd else "  "+ln) for ln,cmd in lines)
        nid=add(x,Y0,CW,box_h,"%s   —   %s\n\n%s"%(name,tool,body),fill,stroke,13,1); ids.append(nid)
        add(x,out_y,CW,OUT_H,"OUTPUT\n"+out,"#ffffff",stroke,12,0)
    for a,b in zip(ids,ids[1:]): edge(a,b)
    add(X0,rec_y,W-2*X0,72,"↩ Recovery — the board is not a brick\namx-pi powerstrip off 0 && powerstrip on 0 (known-good QSPI) · JTAG-load to SRAM tests without flashing · never openFPGALoader -f onto a kernel-at-0 layout",RED[0],RED[1],13,1)
    body="\n".join(cells)
    return ('<mxfile host="app.diagrams.net"><diagram name="build-flash-boot">'
            '<mxGraphModel dx="1400" dy="900" grid="0" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            'page="1" pageScale="1" pageWidth="%d" pageHeight="%d" math="0" shadow="0"><root>%s</root></mxGraphModel></diagram></mxfile>'%(W,H,body))

base=sys.argv[1] if len(sys.argv)>1 else "BUILD_FLASH_BOOT"
open(base+".svg","w").write(svg()); open(base+".drawio","w").write(drawio())
print("wrote",base+".svg","and",base+".drawio")
