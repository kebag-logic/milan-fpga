#!/usr/bin/env python3
"""Generate the Milan system domain map as both editable .drawio and rendered .svg."""
import html, sys

# (title, subtitle, fill, stroke, [module lines])
TEAL=("#B2DFDB","#00796B"); RED=("#F8BBD0","#AD1457"); ORANGE=("#FFE0B2","#EF6C00")
GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0"); PURPLE=("#E1BEE7","#6A1B9A")
DARK=("#CFD8DC","#37474F"); YELLOW=("#FFF9C4","#F9A825")

LAYERS = [
 ("Userspace", "on target · C / config", TEAL, [
    "PipeWire + module-avb (AVB talker/listener)",
    "alsa-lib · buildroot rootfs (busybox init, cpio→tmpfs)"]),
 ("Linux kernel", "on target · C (in-tree + out-of-tree)", RED, [
    "kl-eth — out-of-tree Milan NIC driver (TX/RX DMA, telemetry sysfs, PTP)",
    "in-tree: liteuart, litex-soc-controller, sifive-plic, clint-timer",
    "net: PTP-1588 core · sch_cbs + mqprio qdisc · AF_PACKET · 8021Q",
    "device tree: milan_ax7101_linux.dts  ·  kernel .config: linux.fragment"]),
 ("Boot firmware", "on target · C", ORANGE, [
    "LiteX BIOS (ROM) + linux_flashboot (QSPI→DRAM image copy)",
    "OpenSBI — custom litex_nax platform (M-mode fw_jump, embedded DTB)"]),
 ("SoC integration — LiteX / Migen", "dev host · Python → Verilog  (sw/litex/milan_soc.py)", GREEN, [
    "MilanSoC (top: NaxRiscv + DDR3 + NIC + flash)   ·   _CRG (PLL/clocks/CDC)",
    "MilanNIC / add_milan_datapath   ·   MilanMAC (LiteEth glue)",
    "MilanDMA (WishboneDMA engines)   ·   MilanDebug (pipeline telemetry)"]),
 ("Milan datapath — RTL", "FPGA fabric · SystemVerilog / Verilog  (hdl/)", BLUE, [
    "common: milan_top · milan_datapath · rx_mac_filter · tcam · milan_dma_wrapper · cdc_*",
    "csr: milan_csr  (the AXI-Lite register ABI shared with the driver + DT)",
    "802.1Q CBS: credit_based_shaper · traffic_classifier · traffic_class_map ·",
    "            traffic_controller_802_1q · traffic_queues · traffic_shaping_core",
    "PTP: ptp_ts_top · ptp_ts_core · timestamp_counter · ptp_csr_sync",
    "1722 AVTP: KL_avtp_common_parser   ·   ADP: adp_advertiser · adp_tx_arbiter · KL_adp_parser",
    "events: ethernet_events · event_counter"]),
 ("Vendored IP", "FPGA fabric · 3rd-party cores", PURPLE, [
    "NaxRiscv (RV64GC/sv39 CPU, SpinalHDL)   ·   LiteEth (MAC + GMII/RGMII PHY)",
    "LiteDRAM (DDR3, A7DDRPHY)   ·   LiteSPI (QSPI flash)   ·   verilog-axis (Forencich)"]),
 ("Board / silicon", "physical", DARK, [
    "XC7A100T-2FGG484 (Artix-7)  ·  DDR3 512 MB (MT41J256M16)",
    "QSPI 16 MB (Micron N25Q128)  ·  RTL8211E GbE PHY  ·  200 MHz clk"]),
]
SIDE = ("Host tooling", "Python / bash", YELLOW, [
    "milan_soc.py — SoC/gateware generator",
    "milan_dt.py — device-tree generator (csr.json→dts)",
    "deploy.sh — build / load / flash / flash-images",
    "boot.sh — serialboot (+ FLASH_KERNEL mode)",
    "patches/apply.sh — BIOS linux_flashboot",
    "crcfbigen — FBI image wrapper"])

# ---- layout geometry ----
X0, Y0 = 30, 90
LW = 900                 # layer width
HDR = 42                 # layer header height
RH, RGAP = 26, 6         # module row height / gap
LPAD, LGAP = 10, 16      # inner padding / gap between layers
SIDE_X = X0 + LW + 40
SIDE_W = 340

def layer_height(mods): return HDR + LPAD + len(mods)*(RH+RGAP) - RGAP + LPAD
def esc(s): return html.escape(s, quote=True)

# compute positions
layers=[]; y=Y0
for (title,sub,(fill,stroke),mods) in LAYERS:
    h=layer_height(mods); layers.append((title,sub,fill,stroke,mods,X0,y,LW,h)); y+=h+LGAP
total_h=y+40
side_h=layer_height(SIDE[3]); side_y=Y0

# ---------- SVG ----------
def svg():
    W=SIDE_X+SIDE_W+30; H=max(total_h, side_y+side_h+40)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">']
    o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    o.append(f'<text x="{X0}" y="40" font-size="24" font-weight="bold" fill="#263238">Milan TSN NIC — system domain map</text>')
    o.append(f'<text x="{X0}" y="66" font-size="13" fill="#546E7A">every module by domain / language · software (top) → silicon (bottom) · host tooling generates &amp; deploys the stack</text>')
    def box(x,y,w,h,fill,stroke,title,sub,mods):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        o.append(f'<text x="{x+14}" y="{y+25}" font-size="16" font-weight="bold" fill="#212121">{esc(title)}</text>')
        o.append(f'<text x="{x+14}" y="{y+25}" font-size="16" fill="#212121"><tspan> </tspan></text>')
        o.append(f'<text x="{x+w-14}" y="{y+25}" font-size="11.5" fill="{stroke}" text-anchor="end">{esc(sub)}</text>')
        my=y+HDR+LPAD
        for m in mods:
            o.append(f'<rect x="{x+LPAD}" y="{my}" width="{w-2*LPAD}" height="{RH}" rx="4" fill="#ffffff" fill-opacity="0.72" stroke="{stroke}" stroke-opacity="0.5" stroke-width="1"/>')
            o.append(f'<text x="{x+LPAD+10}" y="{my+17}" font-size="12.5" fill="#212121">{esc(m)}</text>')
            my+=RH+RGAP
    for (t,s,f,st,m,x,yy,w,h) in layers: box(x,yy,w,h,f,st,t,s,m)
    # side tooling
    box(SIDE_X,side_y,SIDE_W,side_h,SIDE[2][0],SIDE[2][1],SIDE[0],SIDE[1],SIDE[3])
    # arrow tooling -> stack, routed down the empty right column (no row overlap)
    mx=SIDE_X+SIDE_W//2; ty=side_y+side_h; ey=760
    o.append(f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#F9A825"/></marker></defs>')
    o.append(f'<path d="M{mx} {ty} L{mx} {ey} L{X0+LW+8} {ey}" fill="none" stroke="#F9A825" stroke-width="2.5" marker-end="url(#a)" stroke-dasharray="6 4"/>')
    o.append(f'<text x="{SIDE_X}" y="{ty+28}" font-size="12" fill="#F57F17">generates · flashes · boots the whole stack</text>')
    o.append('</svg>')
    return "\n".join(o)

# ---------- drawio ----------
def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']
    cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=12,fw=0,align="left",vparent="1"):
        cid[0]+=1; i=cid[0]
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
               f"fontSize={fs};align={align};verticalAlign=top;spacingLeft=8;spacingTop=6;"
               + ("fontStyle=1;" if fw else ""))
        cells.append(f'<mxCell id="n{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{vparent}">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return f"n{i}"
    add(X0,20,700,30,"Milan TSN NIC — system domain map","none","none",20,1)
    for (t,s,f,st,m,x,yy,w,h) in layers:
        add(x,yy,w,h,f"{t}   —   {s}\n\n"+"\n".join("• "+mm for mm in m),f,st,12,1)
    add(SIDE_X,side_y,SIDE_W,side_h,f"{SIDE[0]}   —   {SIDE[1]}\n\n"+"\n".join("• "+mm for mm in SIDE[3]),
        SIDE[2][0],SIDE[2][1],12,1)
    body="\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="domain-map">'
            f'<mxGraphModel dx="1200" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="{total_h+60}" '
            f'math="0" shadow="0"><root>{body}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1]
open(base+".svg","w").write(svg())
open(base+".drawio","w").write(drawio())
print("wrote", base+".svg", "and", base+".drawio")
