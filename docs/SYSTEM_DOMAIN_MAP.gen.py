#!/usr/bin/env python3
"""Generate the Milan system domain map as both editable .drawio and rendered .svg."""
import html, sys
from dataclasses import dataclass
from pathlib import Path

# (title, subtitle, fill, stroke, [module lines])
TEAL=("#B2DFDB","#00796B"); ORANGE=("#FFE0B2","#EF6C00")
GREEN=("#C8E6C9","#2E7D32"); BLUE=("#BBDEFB","#1565C0"); PURPLE=("#E1BEE7","#6A1B9A")
DARK=("#CFD8DC","#37474F"); YELLOW=("#FFF9C4","#F9A825")

LAYERS = [
 ("Bare-metal firmware", "on target · C (the one software surface, #259)", TEAL, [
    "Milan UART/CSR firmware: milan_status · milan_gettime · milan_settime · milan_utc",
    "LiteX BIOS (ROM): console + CRC'd copy of the raw AEM image from its QSPI slot"]),
 ("SoC integration: LiteX / Migen", "dev host · Python → Verilog  (sw/litex/milan_soc.py)", GREEN, [
    "MilanSoC (top: VexiiRiscv RV32 + DDR3 + NIC + flash)   ·   _CRG (PLL/clocks/CDC)",
    "MilanNIC / add_milan_datapath   ·   MilanMAC (LiteEth wire glue)",
    "CSR bridge to bare-metal firmware   ·   fabric audio pins to board I/O"]),
 ("Milan datapath: RTL", "FPGA fabric · SystemVerilog / Verilog  (hdl/)", BLUE, [
    "common: milan_datapath · rx_mac_filter · tcam · cdc_*",
    "csr: milan_csr  (the AXI-Lite register ABI shared with bare-metal firmware)",
    "PTP: timestamp_counter · ptp_csr_sync (the PHC) · KL_ptp_clock_validity",
    "stand-alone verified, not in the shipped datapath: 802.1Q CBS/classifier chain",
    "            (traffic_controller_802_1q + queues/shaping core) · ptp_ts_top/ptp_ts_core",
    "1722 AVTP: KL_avtp_common_parser   ·   adp_tx_arbiter (generic 2-in-1-out AXIS mux)",
    "control plane: KL_pp_shadow (protocol-processor submodule: ADP · ACMP · SRP · AECP)",
    "               KL_pp_maap_shim + KL_maap  (MAAP stays in this fabric)",
    "               AECP uCPU: READ_DESCRIPTOR plus mandatory control/state subset",
    "               GET_COUNTERS / GET_AUDIO_MAP / GET_AS_PATH / GET_AVB_INFO / Milan info",
    "               unsupported commands return NOT_IMPLEMENTED",
    "events: ethernet_events · event_counter"]),
 ("Vendored IP", "FPGA fabric · 3rd-party cores", PURPLE, [
    "VexiiRiscv (product RV32I CPU, SpinalHDL)   ·   LiteEth (MAC + GMII PHY)",
    "LiteDRAM (DDR3, A7DDRPHY)   ·   LiteSPI (QSPI flash)   ·   verilog-axis (Forencich)"]),
 ("Board / silicon", "physical", DARK, [
    "XC7A100T-2FGG484 (Artix-7)  ·  DDR3 512 MB (MT41J256M16)",
    "QSPI 16 MB (Micron N25Q128)  ·  RTL8211E GbE PHY  ·  200 MHz clk"]),
]
SIDE = ("Host tooling", "Python / bash", YELLOW, [
    "milan_soc.py: SoC/gateware generator (bare-metal profile only, #259)",
    "endstation_builder.py: AEM image + fabric gPTP ROM from ONE config",
    "deploy.sh: build / load / flash-pair (live QSPI owner proof)",
    "build.sh: named bare-metal configs + flash transaction",
    "crcfbigen: firmware-image wrapper"])

# ---- layout geometry ----
X0, Y0 = 30, 90
LW = 900                 # layer width
HDR = 42                 # layer header height
RH, RGAP = 26, 6         # module row height / gap
LPAD, LGAP = 10, 16      # inner padding / gap between layers
SIDE_X = X0 + LW + 40
SIDE_W = 340


@dataclass(frozen=True)
class Rect:
    """Where one drawn box sits: top-left corner, then width and height."""
    x: int
    y: int
    w: int
    h: int


def layer_height(mods: list[str]) -> int:
    """the height a layer box needs to hold `mods` rows under its header."""
    return HDR + LPAD + len(mods)*(RH+RGAP) - RGAP + LPAD


def esc(s: str) -> str:
    """XML-safe text, quotes included, because every use is an attribute value."""
    return html.escape(s, quote=True)

# compute positions
layers=[]; y=Y0
for (title,sub,(fill,stroke),mods) in LAYERS:
    h=layer_height(mods)
    layers.append((title,sub,fill,stroke,mods,Rect(X0,y,LW,h)))
    y+=h+LGAP
total_h=y+40
side_h=layer_height(SIDE[3]); side_y=Y0
SIDE_RECT=Rect(SIDE_X,side_y,SIDE_W,side_h)

# ---------- SVG ----------
def svg() -> str:
    """the published .svg: the stacked domain layers, the host-tooling column
    beside them, and the dashed arrow from tooling into the stack."""
    W=SIDE_X+SIDE_W+30; H=max(total_h, side_y+side_h+40)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"'
       f' viewBox="0 0 {W} {H}"'
       f' font-family="Helvetica,Arial,sans-serif">']
    o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    o.append(f'<text x="{X0}" y="40" font-size="24" font-weight="bold"'
             f' fill="#263238">Milan TSN NIC: system domain map</text>')
    o.append(f'<text x="{X0}" y="66" font-size="13" fill="#546E7A">'
             f'every module by domain / language · software (top) → silicon'
             f' (bottom) · host tooling generates &amp; deploys the stack'
             f'</text>')
    def box(rect: Rect, fill: str, stroke: str, title: str, sub: str,
            mods: list[str]) -> None:
        """one domain layer: header, right-aligned subtitle, one white row per module."""
        x,y,w,h = rect.x,rect.y,rect.w,rect.h
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"'
                 f' fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        o.append(f'<text x="{x+14}" y="{y+25}" font-size="16" font-weight="bold" fill="#212121">{esc(title)}</text>')
        o.append(f'<text x="{x+14}" y="{y+25}" font-size="16" fill="#212121"><tspan> </tspan></text>')
        o.append(f'<text x="{x+w-14}" y="{y+25}" font-size="11.5" fill="{stroke}" text-anchor="end">{esc(sub)}</text>')
        my=y+HDR+LPAD
        for m in mods:
            o.append(f'<rect x="{x+LPAD}" y="{my}" width="{w-2*LPAD}"'
                     f' height="{RH}" rx="4" fill="#ffffff"'
                     f' fill-opacity="0.72" stroke="{stroke}"'
                     f' stroke-opacity="0.5" stroke-width="1"/>')
            o.append(f'<text x="{x+LPAD+10}" y="{my+17}" font-size="12.5" fill="#212121">{esc(m)}</text>')
            my+=RH+RGAP
    for (t,s,f,st,m,r) in layers: box(r,f,st,t,s,m)
    # side tooling
    box(SIDE_RECT,SIDE[2][0],SIDE[2][1],SIDE[0],SIDE[1],SIDE[3])
    # arrow tooling -> stack, routed down the empty right column (no row overlap)
    mx=SIDE_X+SIDE_W//2; ty=side_y+side_h; ey=760
    o.append(f'<defs><marker id="a" markerWidth="10" markerHeight="10"'
             f' refX="8" refY="3" orient="auto">'
             f'<path d="M0,0 L8,3 L0,6 Z" fill="#F9A825"/></marker></defs>')
    o.append(f'<path d="M{mx} {ty} L{mx} {ey} L{X0+LW+8} {ey}" fill="none"'
             f' stroke="#F9A825" stroke-width="2.5" marker-end="url(#a)"'
             f' stroke-dasharray="6 4"/>')
    o.append(f'<text x="{SIDE_X}" y="{ty+28}" font-size="12" fill="#F57F17">'
             f'generates · flashes · boots the whole stack</text>')
    o.append('</svg>')
    return "\n".join(o)

# ---------- drawio ----------
def drawio() -> str:
    """the same map as an editable .drawio, one vertex per layer with its
    modules carried inside it as bullet lines."""
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']
    cid=[1]
    def add(rect: Rect, label: str, fill: str, stroke: str, fs: int = 12,
            fw: int = 0) -> str:
        """one drawio vertex; its id is returned, though this map draws no edges."""
        x,y,w,h = rect.x,rect.y,rect.w,rect.h
        cid[0]+=1; i=cid[0]
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
               f"fontSize={fs};align=left;verticalAlign=top;spacingLeft=8;spacingTop=6;"
               + ("fontStyle=1;" if fw else ""))
        cells.append(f'<mxCell id="n{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return f"n{i}"
    add(Rect(X0,20,700,30),"Milan TSN NIC: system domain map","none","none",20,1)
    for (t,s,f,st,m,r) in layers:
        add(r,f"{t}   |   {s}\n\n"+"\n".join("• "+mm for mm in m),f,st,12,1)
    add(SIDE_RECT,f"{SIDE[0]}   |   {SIDE[1]}\n\n"+"\n".join("• "+mm for mm in SIDE[3]),
        SIDE[2][0],SIDE[2][1],12,1)
    body="\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="domain-map">'
            f'<mxGraphModel dx="1200" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1400" pageHeight="{total_h+60}" '
            f'math="0" shadow="0"><root>{body}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1]
Path(base+".svg").write_text(svg())
Path(base+".drawio").write_text(drawio())
print("wrote", base+".svg", "and", base+".drawio")
