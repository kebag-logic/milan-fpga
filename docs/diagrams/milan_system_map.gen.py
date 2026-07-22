#!/usr/bin/env python3
# docs/diagrams/milan_system_map.drawio — THE FULL SYSTEM MAP, v5.
#   · hierarchical: blocks nested inside their owner containers
#   · every address entry is its OWN cell (register-map rows)
#   · straight LEFT->RIGHT data lanes (RX top; TX bottom returns), so BIG data
#     arrows never cross a block; thin dashed = configuration/status
#   · square rectangles everywhere; edges pinned (exitX/entryX) + waypointed
# Values mirror the sources: milan_soc.py / milan_datapath.sv / milan_csr.sv /
# gen/aecp_aem_rom.svh / build.sh cfg_ax7101. Board of record: AX7101.
#
# Regenerate: python3 milan_system_map.gen.py milan_system_map.drawio
# Render:     python3 ../../hdl/ieee17221/aecp/doc/atdecc_architecture.render.py milan_system_map.drawio
import html, re, sys

cells = []
def esc(s):
    t = html.escape(s, quote=True).replace("\n", "&#10;")
    return re.sub(r"  +", lambda m: "&#160;" * len(m.group(0)), t)
def box(i, x, y, w, h, label, fill="#dae8fc", stroke="#6c8ebf", font=10,
        dashed=0, align="center", mono=0, bold=0, parent="1", valign="middle"):
    style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"fontSize={font};verticalAlign={valign};align={align};spacingLeft=5;spacingRight=5;")
    if dashed: style += "dashed=1;"
    if mono:   style += "fontFamily=Courier New;"
    if bold:   style += "fontStyle=1;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def cont(i, x, y, w, h, label, stroke="#666666", fill="#fbfbfb", font=13, parent="1"):
    style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"verticalAlign=top;align=left;fontSize={font};fontStyle=1;spacingLeft=8;"
             f"spacingTop=2;container=1;collapsible=0;")
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def edge(i, s, t, label="", color="#333333", kind="data",
         ex=None, ey=None, nx=None, ny=None, vx=None, vy=None):
    if kind == "data":   width, dash, arrow = 4.5, "", "endArrow=block;endFill=1;"
    elif kind == "copy": width, dash, arrow = 4.5, "dashed=1;", "endArrow=block;endFill=1;"
    else:                width, dash, arrow = 1.1, "dashed=1;", "endArrow=open;"
    pins = ""
    for k, v in (("exitX", ex), ("exitY", ey), ("entryX", nx), ("entryY", ny)):
        if v is not None: pins += f"{k}={v};"
    st = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;{arrow}"
          f"strokeColor={color};strokeWidth={width};fontSize=11;labelBackgroundColor=#ffffff;{dash}{pins}")
    geo = '<mxGeometry relative="1" as="geometry">'
    if vx is not None:
        geo += f'<Array as="points"><mxPoint x="{vx}"/></Array>'
    elif vy is not None:
        geo += f'<Array as="points"><mxPoint y="{vy}"/></Array>'
    geo += '</mxGeometry>'
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" '
                 f'source="{s}" target="{t}">{geo}</mxCell>')
def rows(prefix, x, y, w, items, parent, h=26, font=9, fill="#d5e8d4", stroke="#82b366"):
    """one CELL per entry — the register-map look (address rows)"""
    for n, txt in enumerate(items):
        box(f"{prefix}{n}", x, y + n*h, w, h, txt, fill=fill, stroke=stroke,
            font=font, align="left", mono=1, parent=parent)
    return y + len(items)*h

SYS   = ("#e1d5e7", "#9673a6")
MIL   = ("#dae8fc", "#6c8ebf")
ETH   = ("#ffe6cc", "#d79b00")
EXT   = ("#f5f5f5", "#666666")
CTL   = ("#fff2cc", "#d6b656")
NOTE  = ("#fff9d6", "#b3a100")

W, H = 5680, 2400

box("title", 40, 14, W-80, 42,
    "MILAN AVB NIC on VexiiRiscv SoC — FULL SYSTEM MAP  ·  AX7101 xc7a100t  ·  data flows LEFT->RIGHT (RX lane top; TX lane bottom returns to the wire)  ·  "
    "BIG arrows = frame/bus data · thin dashed = configuration/status · big dashed = monitor copy  ·  every address = its own cell  ·  2026-07-12",
    fill="#e8e8e8", stroke="#333", font=18, bold=1)

box("lg1", 40, 70, 180, 26, "sys @ 100 MHz (cd_sys)", fill=SYS[0], stroke=SYS[1], font=10)
box("lg2", 232, 70, 210, 26, "milan datapath @ 100 MHz (cd_milan)", fill=MIL[0], stroke=MIL[1], font=10)
box("lg3", 454, 70, 190, 26, "eth 125 MHz (LiteEth MAC/PHY)", fill=ETH[0], stroke=ETH[1], font=10)
box("lg4", 656, 70, 90, 26, "off-chip", fill=EXT[0], stroke=EXT[1], font=10)
box("lg5", 758, 70, 210, 26, "memory / register cell (w/ address)", fill="#d5e8d4", stroke="#82b366", font=10)
box("lg6", 980, 70, 80, 26, "arbiter", fill=CTL[0], stroke=CTL[1], font=10)
box("lg7", 1072, 70, 720, 26,
    "lanes: LE = little (tdata[7:0] = first wire byte) · BE = big (AECP parser chain only) · clocks: sys 100 / milan 100 (Arty 50) / eth 125 / DDR3-800",
    fill=NOTE[0], stroke=NOTE[1], font=9, align="left")

# =========================================================================== #
#  PHY (off-chip, far left — the wire)
# =========================================================================== #
box("phy", 40, 140, 220, 1980,
    "RTL8211E PHY\n(off-chip)\n\nGMII-strapped\n8-bit SDR\n(an RGMII read\ncorrupts every\nbyte — hardware-\nconfirmed)\n\n1000BASE-T\nto the AVB\nswitch\n\nRX out @ top\nTX in @ bottom\n\nArty: DP83848\nMII 10/100",
    fill=EXT[0], stroke=EXT[1], font=10, align="left", valign="top")

# =========================================================================== #
#  FABRIC container
# =========================================================================== #
cont("c_fab", 300, 140, 3260, 1980,
     "milan_datapath — fabric, cd_milan 100 MHz (Arty 50)  ·  every AXIS hop: 64b tdata + 8b tkeep + valid/ready/last, LE unless marked BE",
     stroke=MIL[1], fill="#f4f8fd")

# ---- MilanMAC (tall, left: RX out top / TX in bottom) ---- #
cont("c_mac", 20, 60, 540, 1880, "MilanMAC (LiteEth) — eth 125 MHz island", stroke=ETH[1], fill="#fdf6ec", parent="c_fab")
box("phyif", 15, 40, 510, 90, "LiteEthPHYGMII\ngtx 125 MHz · tx_clk_invert · launch FFs\nIOB-packed (silicon placement rule)", fill=ETH[0], stroke=ETH[1], parent="c_mac")
box("maccore", 15, 150, 510, 90, "LiteEthMACCore\npreamble/SFD · CRC32 · padding ·\nwidth conversion 8b <-> 64b", fill=ETH[0], stroke=ETH[1], parent="c_mac")
box("macfifo", 15, 260, 510, 70, "dual-clock stream FIFOs\neth_rx / eth_tx 125 <-> cd_milan 100", fill=ETH[0], stroke=ETH[1], parent="c_mac")
box("lastbe", 15, 350, 510, 90, "stream <-> AXIS adapter\nlast_be (one-hot) <-> tkeep (mask)\n(the M-A3 no-frame-on-wire root cause)", fill=ETH[0], stroke=ETH[1], parent="c_mac")
box("macnote", 15, 1790, 510, 70, "TX side: same core, reverse path\n(padding + CRC insert, IOB launch)", fill=ETH[0], stroke=ETH[1], parent="c_mac")

# ---- RX lane (abs band y 240..580; lane wire ~y 390) ---- #
box("ptprx", 620, 100, 400, 200,
    "ptp_ts_top — RX stamp\n\nper-frame RX timestamp ->\ndescriptor ts window (@ +0x3100)",
    fill=MIL[0], stroke=MIL[1], parent="c_fab", valign="top")
rows("r_ptp", 630, 172, 380, [
 "counter: 64b FF (cd_milan)",
 "0x500-0x51C CTRL·INCR·ADJ·TW·OF",
 "0x520-0x544 CMD·TR·ILAT·ELAT",
], parent="c_fab")
box("tcam", 1080, 100, 420, 200,
    "rx_mac_filter — TCAM dst-MAC filter\n\nternary match · default-pass bit ·\nmiss + no-default -> drop, never stalls",
    fill=MIL[0], stroke=MIL[1], parent="c_fab", valign="top")
rows("r_tcam", 1090, 172, 400, [
 "array: 16 x {key48+mask48+act8} FF",
 "0x700-0x714 CTRL·KLO/KHI·MLO/MHI·ACT",
 "0x718       CMD (write-entry strobe)",
], parent="c_fab")
box("tap", 1560, 150, 300, 100, "rx_axis_to_dma\nTHE TAP POINT (post-filter)\ntaps are copies — never stall",
    fill=MIL[0], stroke=MIL[1], bold=1, parent="c_fab")
box("rmon", 2160, 440, 320, 106, "ethernet_events — RMON", fill=MIL[0], stroke=MIL[1], parent="c_fab", valign="top")
rows("r_rmon", 2170, 468, 300, [
 "counters: 9 x 32b FF",
 "0x210-0x230 STAT0..8 (RO)",
], parent="c_fab", h=25)

# ---- ATDECC container ---- #
cont("c_atdecc", 620, 520, 2060, 940,
     "ATDECC control plane — zero-CPU responders (taps in, one merged control stream out)",
     stroke=MIL[1], fill="#eef4fc", parent="c_fab")

cont("c_aecp", 20, 40, 680, 860, "KL_aecp_top — AECP/AEM (§5.4, la_avdecc-clean)", stroke=MIL[1], fill="#f4f8fd", parent="c_atdecc")
box("aecppipe", 15, 35, 650, 190,
    "ingress tap (registered) -> validator -> parser [64b BE] ->\nl0 (LOCK 60 s · ACQUIRE=NOT_SUPPORTED) -> response builder\n(segments NONE/ECHO/STORE/CONST x4 · CDL = frame-26)\n\ncommands: READ_DESCRIPTOR · names · config · rate · format ·\nSTREAM_INFO 56 B · AVB_INFO · COUNTERS 136 B (errors too) ·\nAS_PATH · MVU GET_MILAN_INFO",
    fill=MIL[0], stroke=MIL[1], align="left", parent="c_aecp")
box("aehdr1", 15, 240, 650, 24, "working memories:", fill="#f4f8fd", stroke=MIL[1], font=9, align="left", parent="c_aecp")
rows("r_ae", 15, 264, 650, [
 "ingress frame buf  128 B LUTRAM",
 "builder buf_r 64 B FF · const_q 64 B FF",
], parent="c_aecp")
box("aehdr2", 15, 330, 650, 24, "AEM store — BRAM 808 B (byte port 8b · addr 16b · 1 cy):", fill="#f4f8fd", stroke=MIL[1], font=9, align="left", parent="c_aecp")
rows("r_dir", 15, 354, 650, [
 "dir  ENTITY        @ 0x000  len 312",
 "dir  CONFIGURATION @ 0x138  len 86",
 "dir  AUDIO_UNIT    @ 0x18E  len 156",
 "dir  STREAM_OUTPUT @ 0x22A  len 156",
 "dir  AVB_INTERFACE @ 0x2C6  len 98",
 "wb   names @ 48·180·316·402·558·714 (64 B)",
 "wb   rate @ 534 (4 B) · format @ 628 (8 B)",
 "ovl  live CSR wins: eid·MAC·caps·idx·cfg·clk",
], parent="c_aecp")
box("aehdr3", 15, 570, 650, 24, "status cells (read over AXI-Lite):", fill="#f4f8fd", stroke=MIL[1], font=9, align="left", parent="c_aecp")
rows("r_aest", 15, 594, 650, [
 "0x648  {locked[16], cmd_count[15:0]}  RO",
 "0x64C  {resp_count[31:16], config[15:0]}  RO",
], parent="c_aecp")

cont("c_acmp", 740, 40, 640, 400, "KL_acmp_responder — ACMP stateless talker (§5.5)", stroke=MIL[1], fill="#f4f8fd", parent="c_atdecc")
box("acmppipe", 15, 35, 610, 230,
    "registered tap · 70 B ACMPDU (CDL 44)\n\nGET_TX_STATE -> SUCCESS, count=0, stream fields zeroed,\nprobe flags cleared (uid!=0 -> TALKER_UNKNOWN_ID)\nGET_TX_CONNECTION -> NOT_SUPPORTED (Milan 5.5.4.4)\nCONNECT/DISCONNECT_TX -> NOT_SUPPORTED until the\nsoftcore policy mailbox (HW answers / SW decides)\nSILICON: la_avdecc Milan=1 CLEAN (eto_acmp2, 31/31)",
    fill=MIL[0], stroke=MIL[1], align="left", parent="c_acmp")
rows("r_ac", 15, 280, 610, [
 "frame buf: 72 B LUTRAM (9 beats x 8 B)",
 "0x650  {resp_count[31:16], cmd_count[15:0]}  RO",
], parent="c_acmp")

cont("c_adp", 740, 480, 640, 420, "adp_advertiser — ADP (§6.2)", stroke=ETH[1], fill="#fdf6ec", parent="c_atdecc")
box("adppipe", 15, 35, 610, 230,
    "82 B ADPDU (CDL 0x38) · periodic every valid_time s\n(vt=31 -> validity 62 s) · AVAILABLE / DEPARTING /\ndiscover response · available_index +1 on EVERY ADPDU\n(la_avdecc strict rule) · priority: depart > link_up >\ninfo/gm change > discover > timer · enable-edge with\nlink already up == link_up (boot-order fix)",
    fill=ETH[0], stroke=ETH[1], align="left", parent="c_adp")
rows("r_adp", 15, 280, 610, [
 "0x644  available_index 32b (RO, live)",
 "identity in = CSR 0x600 group (= AEM overlay)",
], parent="c_adp")

box("mux1", 1480, 120, 240, 90, "aecp_acmp_mux\nframe-atomic RR", fill=CTL[0], stroke=CTL[1], parent="c_atdecc")
box("mux2", 1480, 320, 240, 90, "ctl_tx_mux\nADP + (AECP|ACMP)\nframe-atomic RR", fill=CTL[0], stroke=CTL[1], parent="c_atdecc")

# ---- milan_csr register-map column ---- #
cont("c_csr", 2760, 520, 460, 940,
     "milan_csr @ 0x9000_0000 — AXI-Lite 64 KB (32b/16b) · ~46 x 32b FF · CDC sys->milan",
     stroke="#82b366", fill="#f0f7ee", parent="c_fab")
rows("r_csr", 15, 70, 430, [
 "0x000 ID 'MILN' · 0x004 VER · 0x008 CAP",
 "0x108/0x10C  station MAC ALO/AHI",
 "0x210-0x230  RMON STAT0..8 (RO)",
 "0x300-0x310  classifier CTRL·MAP·REGEN·TCQ",
 "0x400+q*0x20 CBS idleSlope/credit (q0..q3)",
 "0x500-0x544  PTP group",
 "0x600  ADP_CTRL {vt[12:8], enable[0]}",
 "0x604-0x610  ENTITY_ID · MODEL_ID",
 "0x614  CAPS 0x8588 (no IDENTIFY bit!)",
 "0x618/0x61C  TALKER · LISTENER",
 "0x620  CTRL_CAPS · 0x624/0x628 gPTP GM",
 "0x62C  domain · 0x630/0x634 IDX0/IDX1",
 "0x638/0x63C  ASSOCIATION_ID",
 "0x640  ADP_CMD W1S [0]adv [1]depart",
 "0x644  avail_idx RO · 0x648/64C AECP RO",
 "0x650  ACMP RO · 0x700-0x718 TCAM",
], parent="c_csr", h=27)
box("csrirq", 15, 520, 430, 70, "o_irq_csr -> PLIC · identity fans out to\nADP + AEM + ACMP: ONE source of wire truth",
    fill="#f0f7ee", stroke="#82b366", font=9, align="left", parent="c_csr")

# ---- TX lane (abs band y 1700..2020; lane wire ~y 1880) ---- #
box("dparb", 620, 1560, 380, 320,
    "adp_tx_mux — datapath merge\n\nshaped data has priority;\ncontrol inserted in inter-\nframe gaps only (zero mid-\nframe jitter) · frame-atomic",
    fill=CTL[0], stroke=CTL[1], align="left", parent="c_fab", valign="top")
box("ptptx", 1060, 1560, 380, 320,
    "ptp_ts_top — TX stamp\n\nsame 64b counter · per-frame\nTX timestamp -> ts window ->\ndriver (SO_TIMESTAMPING after\nthe PHC lands)",
    fill=MIL[0], stroke=MIL[1], align="left", parent="c_fab", valign="top")
box("cbs", 1500, 1560, 460, 320,
    "traffic_shaping_core + CBS\n\ncredit gate + strict priority x4\n(802.1Q Table 8-5) · sequential\nslope engine (-8K LUTs, bit-exact,\nconfig 2 us) · NEVER removed",
    fill=MIL[0], stroke=MIL[1], align="left", parent="c_fab", valign="top")
rows("r_cbs", 1510, 1800, 440, [
 "0x400+q*0x20 idleSlope 32b + credit (x4)",
 "reset slopes {300,200,150,100} Mb/s",
], parent="c_fab", h=25)
box("queues", 2020, 1560, 440, 320,
    "traffic_queues — BRAM\n\n4 x axis_fifo · 16 KB each\n(DEPTH 16384 B @ 64b) = 64 KB\ndepth/empty -> shaper gating\n(fabric-internal, no bus addr)",
    fill="#d5e8d4", stroke="#82b366", align="left", parent="c_fab", valign="top")
box("cls", 2520, 1560, 460, 320,
    "traffic_classifier (802.1Q)\n\nVLAN TPID 0x8100 · PCP[3b] ->\nregen -> TC -> queue select ·\nAVTP 0x22F0 -> class A/B",
    fill=MIL[0], stroke=MIL[1], align="left", parent="c_fab", valign="top")
rows("r_cls", 2530, 1800, 440, [
 "maps: regen 8x3b · prio->TC 8x2b · TC->q 4x2b",
 "0x300 CTRL · 0x308 MAP · 0x30C REGEN · 0x310 TCQ",
], parent="c_fab", h=25)

# =========================================================================== #
#  SoC container
# =========================================================================== #
cont("c_soc", 3660, 140, 1560, 1980, "SoC / softcore — LiteX, cd_sys 100 MHz", stroke=SYS[1], fill="#f7f2fa")

cont("c_rxdma", 20, 60, 740, 400, "RX DMA writer (coherent port)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("rxwr", 15, 35, 710, 190,
    "RSC TCP coalescer — RING_RSC_TOUT in 100 MHz ticks\n(default 250 us; ethtool -C rx-usecs live) ·\nheader-split v3 (fill len in w0[31:16], page <= 32 KB) ·\n4-slot writer + pop-ordered CQ(8) · 60 KB order-4 buffers",
    fill=SYS[0], stroke=SYS[1], align="left", parent="c_rxdma")
rows("r_steer", 15, 240, 710, [
 "flow steer: 4-tuple hash -> q0/q1 · hash_sel=1 forces q0 (BEFORE TCP)",
 "LiteX CSRs @ 0xf000_3xxx — BUILD-DEPENDENT: read csr.json!",
], parent="c_rxdma", h=26)
box("rxirq", 15, 310, 710, 60, "per-queue IRQ -> PLIC (rx-usecs-low moderation: +32%)",
    fill=SYS[0], stroke=SYS[1], font=9, parent="c_rxdma")

cont("c_cpu", 800, 60, 740, 400, "VexiiRiscv cluster (RV64IMA)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("hart0", 15, 35, 340, 80, "hart 0\nlsu refill 8 · prefetch rpt", fill=SYS[0], stroke=SYS[1], parent="c_cpu")
box("hart1", 375, 35, 350, 80, "hart 1\n(1-hart decision pending:\n58% LUTs datapoint)", fill=SYS[0], stroke=SYS[1], font=9, parent="c_cpu")
rows("r_cpu", 15, 130, 710, [
 "L2 cache 64 KB shared · down-pending 8 · slots 16 (coherent DMA lands here)",
], parent="c_cpu", h=26)
box("plic", 15, 172, 710, 50, "PLIC + CLINT — kl-eth per-queue · milan_csr · UART · timer",
    fill=SYS[0], stroke=SYS[1], font=9, parent="c_cpu")
box("bus", 15, 238, 710, 60, "LiteX interconnect — Wishbone/AXI · CSR 32b ·\ncoherent DMA port 64b into the L2 (--coherent-dma)",
    fill=SYS[0], stroke=SYS[1], font=9, parent="c_cpu")
box("uart", 15, 314, 340, 60, "UART 115200 (litex_term)", fill=SYS[0], stroke=SYS[1], font=9, parent="c_cpu")
box("jtag", 375, 314, 350, 60, "JTAG — openFPGALoader\nft232 210512180081", fill=SYS[0], stroke=SYS[1], font=9, parent="c_cpu")

cont("c_drv", 20, 520, 1520, 780, "software (Linux on the softcore)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("kleth", 15, 35, 1490, 280,
    "kl-eth driver (kl,dma-ether · silicon; MODULE_VERSION gates identity)\n\n"
    "• 2 RX queues x threaded NAPI · RSC ON @250 us · hs_pgsz=16384 <-> gateware --hs-page-bytes 16384 (STRICT)\n"
    "• 4-slot RX + pop-ordered CQ (wedge-free) · HW-TSO · chain-csum · ack-merge tout 512 us\n"
    "• identity provisioning once/boot: devmem 0x9000_0600 group (aecp_csr_setup.sh, caps 0x8588)\n"
    "• NEXT: PHC /dev/ptpN + SO_TIMESTAMPING — the gPTP gate (ARCHITECTURE_HW_SW_SPLIT.md)",
    fill=SYS[0], stroke=SYS[1], align="left", parent="c_drv")
box("ptpd", 15, 335, 1490, 110,
    "linuxptp: ptp4l (802.1AS BMCA + servo) + phc2sys — in the rootfs, unvalidated until the PHC lands;\nthen a small bridge writes GM id/domain -> CSR 0x624/0x628 on change (fabric re-advertises, AS_PATH stays true)",
    fill=SYS[0], stroke=SYS[1], align="left", parent="c_drv")
box("pw", 15, 465, 1490, 110,
    "media rev 2 (2026-07-12, user directive: EVERYTHING FPGA + lwSRP): softcore only fills a DMA PCM ring (ms cadence);\nfabric does lwSRP (MSRP/MVRP + bandwidth gate) · AAF framer (PTP presentation time) · ACMP connection table",
    fill=SYS[0], stroke=SYS[1], align="left", parent="c_drv")
box("qspihdr", 15, 595, 1490, 24, "QSPI flash N25Q128 16 MB (off-chip, flashboot slots):",
    fill="#faf6fc", stroke=SYS[1], font=9, align="left", parent="c_drv")
rows("r_qspi", 15, 619, 1490, [
 "FLASHED v1: kernel@0 · opensbi@0x88_0000 · dtb@0x90_0000 · rootfs@0x94_0000 — STAGED v2: BITSTREAM@0 (2.25MiB) + shifted images (QSPI_FLASHBOOT.md)",
 "validation peers via the AVB switch: milan_controller.py · la_avdecc enum-probe (Hive) · tsn-gen",
], parent="c_drv", h=26)

cont("c_txdma", 20, 1520, 740, 420, "TX DMA reader + HW-TSO (coherent port)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("txrd", 15, 35, 710, 210,
    "descriptor fetch from the 512x8B ring — base/length in\nBYTES (trap!) · AXI bursts 16-64 beats x 64b (128-512 B) ·\nTSO header-gen (MSS segmentation, chain-csum; TX 143->186\nzc) · reader-bound wall (starve 70% -> prefetch next)",
    fill=SYS[0], stroke=SYS[1], align="left", parent="c_txdma")
rows("r_stag", 15, 260, 710, [
 "TX staging FIFO — BRAM 2048 beats x 64b = 16 KB",
 "ring ctl / doorbells: LiteX CSRs (csr.json)",
], parent="c_txdma", h=26)

# =========================================================================== #
#  DRAM container (far right)
# =========================================================================== #
cont("c_dram", 5280, 140, 360, 1980,
     "DDR3 SDRAM — 512 MB @ 0x4000_0000 (off-chip; LiteDRAM + A7DDRPHY, sys4x 400 + DQS 90°)",
     stroke="#82b366", fill="#f0f7ee")
box("rxrhdr", 15, 120, 330, 24, "RX rings (per queue x2):", fill="#f0f7ee", stroke="#82b366", font=9, align="left", parent="c_dram")
rows("r_rxr", 15, 144, 330, [
 "4 slots x 60 pages x 16 KB = 960 KB",
 "CQ 8 entries POP-ORDERED (mslot60)",
 "desc: addr·len·flags·ts @ +0x3100",
], parent="c_dram")
box("bihdr", 15, 700, 330, 24, "boot images (from QSPI):", fill="#f0f7ee", stroke="#82b366", font=9, align="left", parent="c_dram")
rows("r_boot", 15, 724, 330, [
 "kernel  @ 0x4000_0000",
 "dtb     @ 0x40EF_0000",
 "opensbi @ 0x40F0_0000 (fw_jump)",
 "initrd  @ 0x4100_0000",
], parent="c_dram")
box("dramnote", 15, 880, 330, 80, "row miss costs 1424 ns (50% TLB +\n50% DRAM) — the measured single-\nport latency ceiling",
    fill=NOTE[0], stroke=NOTE[1], font=9, align="left", parent="c_dram")
box("txrhdr", 15, 1680, 330, 24, "TX ring:", fill="#f0f7ee", stroke="#82b366", font=9, align="left", parent="c_dram")
rows("r_txr", 15, 1704, 330, [
 "512 x 8 B = 4 KB (8 frame slots)",
 "driver-allocated (dma_alloc_coherent)",
], parent="c_dram")

# =========================================================================== #
#  EDGES
# =========================================================================== #
# RX lane: straight left->right at abs y ~390
edge("er0", "phy", "c_mac", "GMII 8b @125", color=ETH[1], kind="data", ex=1.0, ey=0.08, nx=0.0, ny=0.13)
edge("er1", "c_mac", "ptprx", "64b AXIS LE", color=MIL[1], kind="data", ex=1.0, ey=0.13, nx=0.0, ny=0.5)
edge("er2", "ptprx", "tcam", "64b AXIS LE", color=MIL[1], kind="data", ex=1.0, ey=0.5, nx=0.0, ny=0.5)
edge("er3", "tcam", "tap", "64b AXIS LE", color=MIL[1], kind="data", ex=1.0, ey=0.5, nx=0.0, ny=0.5)
edge("er4", "tap", "rxwr", "64b AXIS LE (async FIFO -> cd_sys)", color=MIL[1], kind="data", ex=1.0, ey=0.5, nx=0.0, ny=0.5)
edge("er5", "c_rxdma", "rxrhdr", "coherent AXI writes 64b (via L2)", color=SYS[1], kind="data", ex=0.7, ey=0.0, nx=0.5, ny=0.0, vy=185)
# TX lane: straight right->left at abs y ~1880
edge("ex9", "txrhdr", "c_txdma", "AXI reads 64b (bursts 16-64 beats)", color=SYS[1], kind="data", ex=0.0, ey=0.5, nx=1.0, ny=0.45)
edge("ex0", "c_txdma", "cls", "64b AXIS LE (async FIFO -> cd_milan)", color=SYS[1], kind="data", ex=0.0, ey=0.45, nx=1.0, ny=0.55)
edge("ex1", "cls", "queues", "64b AXIS LE + q 2b", color=MIL[1], kind="data", ex=0.0, ey=0.55, nx=1.0, ny=0.55)
edge("ex2", "queues", "cbs", "4 x 64b AXIS LE", color=MIL[1], kind="data", ex=0.0, ey=0.55, nx=1.0, ny=0.55)
edge("ex3", "cbs", "ptptx", "64b AXIS LE", color=MIL[1], kind="data", ex=0.0, ey=0.55, nx=1.0, ny=0.55)
edge("ex4", "ptptx", "dparb", "64b AXIS LE", color=MIL[1], kind="data", ex=0.0, ey=0.55, nx=1.0, ny=0.55)
edge("ex6", "dparb", "c_mac", "64b AXIS LE", color=MIL[1], kind="data", ex=0.0, ey=0.55, nx=1.0, ny=0.92)
edge("ex7", "c_mac", "phy", "GMII 8b @125 (gtx)", color=ETH[1], kind="data", ex=0.0, ey=0.95, nx=1.0, ny=0.93)
# taps (big dashed copies) via shelves in the RX/ATDECC corridor
edge("et1", "tap", "c_aecp", "tap copy 64b LE", kind="copy", ex=0.25, ey=1.0, nx=0.5, ny=0.0, vy=640)
edge("et2", "tap", "c_acmp", "tap copy 64b LE", kind="copy", ex=0.75, ey=1.0, nx=0.5, ny=0.0, vy=672)
# responses into the mux column (aecp over the top shelf; acmp/adp direct)
edge("em1", "c_aecp", "mux1", "resp 64b LE", color=MIL[1], kind="data", ex=0.9, ey=0.0, nx=0.5, ny=0.0, vy=690)
edge("em2", "c_acmp", "mux1", "resp 64b LE", color=MIL[1], kind="data", ex=1.0, ey=0.4, nx=0.0, ny=0.5)
edge("em3", "mux1", "mux2", "64b LE", color=MIL[1], kind="data", ex=0.5, ey=1.0, nx=0.5, ny=0.0)
edge("em4", "c_adp", "mux2", "advertise 64b LE", color=ETH[1], kind="data", ex=1.0, ey=0.3, nx=0.0, ny=0.5)
# control out: mux2 -> dparb via the shelf under the ATDECC container
edge("em5", "mux2", "dparb", "control 64b LE (IFG insert)", color=MIL[1], kind="data", ex=0.5, ey=1.0, nx=0.5, ny=0.0, vy=1650)
# thin config
edge("et3", "c_aecp", "c_adp", "ENTITY_DISCOVER 1b", kind="cfg", ex=1.0, ey=0.75, nx=0.0, ny=0.5)
edge("ev1", "c_mac", "rmon", "event pulses 1b", kind="cfg", ex=0.7, ey=0.0, nx=0.5, ny=0.0, vy=185)
edge("ec1", "bus", "c_csr", "AXI-Lite 32b (CDC sys->milan)", kind="cfg", ex=0.5, ey=1.0, nx=0.9, ny=0.0, vy=640)
edge("ec2", "c_csr", "c_atdecc", "identity 0x600 + status (CDC)", kind="cfg", ex=0.0, ey=0.5, nx=1.0, ny=0.5)
edge("ec3", "c_csr", "cls", "0x300 maps", kind="cfg", ex=0.3, ey=1.0, nx=0.7, ny=0.0)
edge("ec4", "c_csr", "tcam", "0x700 · 0x500 · 0x210", kind="cfg", ex=0.3, ey=0.0, nx=0.7, ny=1.0, vy=480)
edge("es5", "kleth", "c_rxdma", "", kind="cfg", ex=0.15, ey=0.0, nx=0.5, ny=1.0)
edge("es7", "c_rxdma", "plic", "IRQ", kind="cfg", ex=1.0, ey=0.85, nx=0.0, ny=0.5)

xml = ('<mxfile host="app.diagrams.net"><diagram name="milan-system-map">'
       f'<mxGraphModel dx="2000" dy="1400" grid="0" gridSize="10" guides="1" tooltips="1" '
       f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
       'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')
open(sys.argv[1], "w").write(xml)
print("wrote", sys.argv[1], len(cells), "cells")
