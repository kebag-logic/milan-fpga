#!/usr/bin/env python3
# Generate docs/diagrams/milan_system_map.drawio — THE GIANT system map:
# one oversized page with the complete datapath (RX + TX end to end), every
# block, bus width on every wire, every register file / BRAM as its OWN block
# with size and address, clock domains by colour, DMA/ring geometry, and all
# address mappings. Every number mirrors the sources: milan_soc.py /
# milan_datapath.sv / milan_csr.sv / gen/aecp_aem_rom.svh / build.sh
# cfg_ax7101. Board of record: AX7101 (xc7a100t).
#
# Regenerate: python3 milan_system_map.gen.py milan_system_map.drawio
# Render:     python3 ../../hdl/aecp/doc/atdecc_architecture.render.py milan_system_map.drawio
import html, re, sys

cells = []
def esc(s):
    t = html.escape(s, quote=True).replace("\n", "&#10;")
    return re.sub(r"  +", lambda m: "&#160;" * len(m.group(0)), t)
def box(i, x, y, w, h, label, fill="#dae8fc", stroke="#6c8ebf", font=12,
        rounded=1, dashed=0, align="center", mono=0, bold=0):
    style = (f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"fontSize={font};verticalAlign=middle;align={align};spacingLeft=6;spacingRight=6;")
    if dashed: style += "dashed=1;"
    if mono:   style += "fontFamily=Courier New;"
    if bold:   style += "fontStyle=1;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def grp(i, x, y, w, h, label, stroke="#999999", fill="none", font=15):
    style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};dashed=1;"
             f"verticalAlign=top;align=left;fontSize={font};fontStyle=1;spacingLeft=8;spacingTop=4;")
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def edge(i, s, t, label="", dashed=0, color="#333333", width=1.6):
    st = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;"
          f"strokeColor={color};strokeWidth={width};fontSize=11;labelBackgroundColor=#ffffff;")
    if dashed: st += "dashed=1;endArrow=open;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" '
                 f'source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')
def table(i, x, y, w, rows, font=10, title=None, fill="#f5f5f5", stroke="#666666", rh=16):
    label = "\n".join(rows)
    h = rh * len(rows) + 12
    if title:
        box(i + "_t", x, y, w, 24, title, fill="#e8e8e8", stroke=stroke, font=font+2,
            rounded=0, bold=1)
        y += 24
    box(i, x, y, w, h, label, fill=fill, stroke=stroke, font=font, rounded=0,
        align="left", mono=1)
    return y + h
def mem(i, x, y, w, h, label):
    """a register file / BRAM / DRAM region — always its own block"""
    box(i, x, y, w, h, label, fill="#d5e8d4", stroke="#82b366", font=10, align="left")

SYS   = ("#e1d5e7", "#9673a6")   # sys 100 MHz (CPU/LiteX/DMA engines)
MIL   = ("#dae8fc", "#6c8ebf")   # milan datapath 100 MHz (cd_milan)
ETH   = ("#ffe6cc", "#d79b00")   # eth_rx / eth_tx 125 MHz (LiteEth MAC/PHY)
EXT   = ("#f5f5f5", "#666666")   # off-chip
MEMC  = ("#d5e8d4", "#82b366")   # memories / register files
CTL   = ("#fff2cc", "#d6b656")   # arbiters / muxes
NOTE  = ("#fff9d6", "#b3a100")

W, H = 5560, 3170

box("title", 40, 16, W-80, 44,
    "MILAN AVB NIC on VexiiRiscv SoC — THE FULL SYSTEM MAP  ·  AX7101 xc7a100t (board of record; Arty deltas noted)  ·  "
    "every wire: bus width  ·  every register file / BRAM: own block with size + address  ·  colours = clock domains  ·  2026-07-12",
    fill="#e8e8e8", stroke="#333", font=20, rounded=0, bold=1)

# ---- legend + clock tree --------------------------------------------------- #
grp("g_leg", 40, 76, 1180, 104, "legend")
box("lg1", 60, 106, 190, 26, "sys @ 100 MHz (cd_sys)", fill=SYS[0], stroke=SYS[1], font=11)
box("lg2", 262, 106, 214, 26, "milan datapath @ 100 MHz (cd_milan)", fill=MIL[0], stroke=MIL[1], font=11)
box("lg3", 488, 106, 214, 26, "eth_rx / eth_tx @ 125 MHz (LiteEth)", fill=ETH[0], stroke=ETH[1], font=11)
box("lg4", 714, 106, 112, 26, "off-chip", fill=EXT[0], stroke=EXT[1], font=11)
box("lg5", 838, 106, 190, 26, "register file / BRAM / DRAM", fill=MEMC[0], stroke=MEMC[1], font=11)
box("lg6", 1040, 106, 90, 26, "arbiter", fill=CTL[0], stroke=CTL[1], font=11)
box("lg7", 60, 142, 1140, 26,
    "lanes:  LE = little (tdata[7:0] = first wire byte, Forencich/MAC)   BE = big (tdata[63:56] first — AECP parser chain only)",
    fill=NOTE[0], stroke=NOTE[1], font=10, align="left")

grp("g_clk", 1260, 76, 1180, 104, "clock tree (S7 PLL, from 200 MHz osc)")
table("t_clk", 1280, 108, 1140, [
 "osc 200 -> PLL: cd_sys 100 · cd_sys4x 400 + dqs 90deg (DDR3-800) · cd_idelay 200 · cd_milan 100 (own domain; Arty: 50)",
 "LiteEth: eth_rx = PHY rx_clk 125 · eth_tx = gtx 125 (tx_clk_invert; GMII launch FFs IOB-packed — silicon rule)",
 "crossings: AXI-Lite CSR sys<->milan (bus CDC) · MAC async FIFOs eth<->milan · DMA in sys, AXIS FIFOs to milan",
], font=10)

# ---- SoC / softcore band --------------------------------------------------- #
grp("g_soc", 40, 210, 3060, 600, "SoC / softcore  (LiteX, cd_sys 100 MHz)")

box("cpu", 70, 260, 330, 160,
    "VexiiRiscv x2 harts (RV64IMA)\n\nL1 caches + L2 64 KB shared\n(l2-bytes 65536)\nlsu-l1-refill-count=8 · prefetch rpt\nl2-down-pending=8 · general-slots=16\n(1-hart decision pending: 58% LUTs)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("plic", 70, 460, 330, 60, "PLIC + CLINT\nIRQs: milan_csr o_irq_csr · kl-eth DMA\nper-queue · UART · timer", fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("bus", 520, 260, 210, 260, "LiteX interconnect\n\nWishbone/AXI\nCSR bus 32b\n+ coherent DMA\nport into the L2\n(--coherent-dma)", fill=SYS[0], stroke=SYS[1], font=10)
box("dramc", 850, 260, 280, 120, "LiteDRAM controller\nA7DDRPHY (sys4x 400 + DQS 90°,\n200 MHz IDELAYCTRL)", fill=SYS[0], stroke=SYS[1], font=10)
mem("ddr", 1290, 260, 310, 130,
    "DDR3 SDRAM (off-chip)\nMT41K256M16 x16 · 512 MB\n@ 0x4000_0000 (CPU view)\nkernel@+0 · dtb@0x40EF_0000 ·\nopensbi@0x40F0_0000 · initrd@0x4100_0000")
mem("txring", 1290, 430, 310, 70,
    "TX descriptor ring (in DRAM)\n512 x 8 B = 4 KB (>= 2 max frames,\n8 frame slots) · driver-allocated")
mem("rxrings", 1290, 520, 310, 90,
    "RX rings (in DRAM, per queue x2)\n4 slots x 60 pages x 16 KB = 960 KB\n+ completion queue 8 entries,\nPOP-ORDERED (mslot60) · driver-alloc")
box("uart", 850, 420, 140, 50, "UART 115200\n(litex_term)", fill=SYS[0], stroke=SYS[1], font=10)
box("jtag", 1010, 420, 150, 50, "JTAG (openFPGALoader\nft232 210512180081)", fill=SYS[0], stroke=SYS[1], font=9)
mem("qspi", 850, 490, 310, 80,
    "QSPI flash N25Q128 16 MB (off-chip)\nflashboot slots: kernel@0 (8.5 MiB) ·\nopensbi@0x88_0000 (512 KiB) ·\ndtb@0x90_0000 · rootfs@0x94_0000 (6.75 MiB)")

box("dmaeng", 70, 560, 660, 230,
    "kl-eth DMA engines (fabric, cd_sys, coherent port)\n\n"
    "TX reader: fetches the 512x8B ring (base/length in BYTES — trap!),\n"
    "AXI bursts 16-64 beats x 64b (128-512 B) · + HW-TSO header generator\n"
    "(MSS segmentation, chain-csum; validated TX 143->186 zc)\n\n"
    "RX writer: RSC TCP coalescer (RING_RSC_TOUT, 100 MHz ticks, default\n"
    "250 us) · header-split v3 (fill length in w0[31:16], page <= 32 KB) ·\n"
    "4-slot writer + pop-ordered CQ · 2-queue flow steer (4-tuple hash;\n"
    "hash_sel=1 forces q0 — set BEFORE TCP runs)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
mem("stag", 790, 590, 240, 70, "TX staging FIFO\nBRAM 2048 beats x 64b = 16 KB")
mem("csrjson", 790, 690, 240, 100, "LiteX CSR block @ 0xf000_0000\n(ring ctl, RSC tout, steer/hash,\nIRQ status) — offsets BUILD-\nDEPENDENT: read csr.json!")

box("kleth", 1690, 260, 690, 250,
    "kl-eth Linux driver  (kl,dma-ether · silicon; MODULE_VERSION gates identity)\n\n"
    "• 2 RX queues (flow-steered) x threaded NAPI · budget/gro knobs\n"
    "• RSC ON by default @250 us (ethtool -C rx-usecs retunes live; rsc_clk_mhz=100)\n"
    "• header-split hs_pgsz=16384 <-> gateware --hs-page-bytes 16384 (STRICT pairing)\n"
    "• 4-slot RX + pop-ordered CQ (wedge-free by construction) · 60 KB order-4 buffers\n"
    "• HW-TSO on TX · chain-csum · ethtool -C ack-merge tout 512 us\n"
    "• identity provisioning once/boot: devmem 0x9000_0600 group (aecp_csr_setup.sh)\n"
    "• NEXT: PHC /dev/ptpN + SO_TIMESTAMPING (gPTP gate — HW_SW_SPLIT.md)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("sw2", 1690, 540, 690, 70,
    "userspace: linuxptp ptp4l+phc2sys (present, unvalidated until PHC) · PipeWire module-avb (future media:\nAAF frames -> kl-eth -> CBS class-A queue) · la_avdecc / Hive / milan_controller.py validate from the peer",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("irqn", 2440, 640, 330, 100, "IRQ fan-in\nper-queue RX complete + TX done +\nmilan_csr o_irq_csr -> PLIC\n(rx-usecs-low moderation: +32%)", fill=SYS[0], stroke=SYS[1], font=10, align="left")

edge("es1", "cpu", "bus", "ibus/dbus 64b")
edge("es2", "bus", "dramc", "membus 64b")
edge("es2b", "dramc", "ddr", "DDR3 x16 @ 400 MHz (DQ 16b DDR)", color=SYS[1])
edge("es3", "bus", "dmaeng", "CSR 32b · coherent DMA 64b (via L2)")
edge("es4", "dmaeng", "txring", "AXI reads 64b, bursts 16-64 beats", color=SYS[1])
edge("es4b", "dmaeng", "rxrings", "AXI writes 64b", color=SYS[1])
edge("es5", "kleth", "csrjson", "ring ctl / doorbells 32b", dashed=1)
edge("es6", "plic", "cpu", "M/S-ext IRQ")
edge("es7", "irqn", "plic", "irq lines")
edge("es8", "dmaeng", "stag", "64b")
edge("es9", "ddr", "txring", "", dashed=1)
edge("es10", "ddr", "rxrings", "", dashed=1)

# ---- fabric datapath band --------------------------------------------------- #
grp("g_dp", 40, 850, 5480, 1340,
    "milan_datapath (fabric, cd_milan 100 MHz — Arty: 50 MHz)   ·   ALL AXIS links: 64-bit tdata + 8-bit tkeep + tvalid/tready/tlast, LITTLE lane unless marked BE")

# PHY + MAC (left edge, spans RX/TX rows)
box("phy", 70, 950, 190, 620,
    "RTL8211E PHY\n(GMII-strapped,\n8-bit SDR — an\nRGMII read corrupts\nevery byte:\nhardware-confirmed)\n\n1000BASE-T\nto the AVB switch",
    fill=EXT[0], stroke=EXT[1], font=10, align="left")
box("mac", 330, 950, 330, 620,
    "MilanMAC  (LiteEth)\n\nLiteEthPHYGMII (gtx 125, tx_clk_invert,\nlaunch FFs IOB-packed — placement rule)\n+ LiteEthMACCore: preamble/SFD, CRC32,\npadding, width conversion 8b<->64b,\ndual-clock stream FIFOs eth<->cd_milan\n+ stream<->AXIS adapter:\nlast_be (one-hot) <-> tkeep (mask)\n(the M-A3 no-frame-on-wire root cause)\n\nArty: LiteEthPHYMII (DP83848, 100M,\nis_1g=0 -> CBS slope wiring pending)",
    fill=ETH[0], stroke=ETH[1], font=10, align="left")

# ---- RX row + its memory row ---- #
RXY = 950
box("ptprx", 820, RXY, 280, 130,
    "ptp_ts_top — RX stamp\n\nper-frame RX timestamp captured\ninto the DMA descriptor ts window\n(dts kl,dma-ts @ +0x3100)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("ptpregs", 820, RXY+180, 280, 90,
    "PTP counter + CSR regs\n64b counter FF (cd_milan) ·\nCSR 0x500-0x544: CTRL/INCR/ADJ/\nTW lo·hi/OF lo·hi/CMD/TR lo·hi/LATs")
box("tcam", 1340, RXY, 300, 130,
    "rx_mac_filter (TCAM logic)\n\nternary match on dst MAC ·\ndefault-pass CSR bit · miss+no-\ndefault -> drop (never backpressures)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("tcamregs", 1340, RXY+180, 300, 90,
    "TCAM entry array\n16 x {key 48b + mask 48b + action 8b}\n= 1664 b FF · programmed @ 0x700-\n0x718 (CTRL/KLO/KHI/MLO/MHI/ACT/CMD)")
box("rxnode", 1900, RXY+35, 260, 60, "rx_axis_to_dma\n(the tap point — post-filter)", fill=MIL[0], stroke=MIL[1], font=11, bold=1)
box("rsc", 2440, RXY, 340, 130,
    "RX DMA front (cd_sys side)\n\nRSC coalescer · header-split v3\n(16 KB pages) · 4-slot writer +\nCQ(8) pop-ordered · 2-queue steer",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")

edge("er0", "phy", "mac", "GMII 8b @ 125 (rx_clk)", color=ETH[1])
edge("er1", "mac", "ptprx", "64b AXIS LE k8", color=MIL[1])
edge("er2", "ptprx", "tcam", "64b AXIS LE k8", color=MIL[1])
edge("er3", "tcam", "rxnode", "64b AXIS LE k8", color=MIL[1])
edge("er4", "rxnode", "rsc", "64b AXIS LE k8 (async FIFO -> cd_sys)", color=MIL[1])
edge("er5", "rsc", "rxrings", "coherent AXI 64b (via L2)", color=SYS[1])
edge("er6", "ptprx", "ptpregs", "ts 64b · CSR 32b", dashed=1)
edge("er7", "tcam", "tcamregs", "16 x key/mask 48b", dashed=1)

# RMON counters
box("rmon", 330, 1640, 330, 110,
    "ethernet_events (logic)\nRMON-style event capture fed by MAC\npulses (rx/tx frames, CRC err, ...)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("rmonregs", 330, 1790, 330, 60,
    "event counters: 9 x 32b FF\nRO @ 0x210-0x230 (STAT0..8, stride 4)")
edge("ev1", "mac", "rmon", "event pulses 1b each", dashed=1)
edge("ev2", "rmon", "rmonregs", "9 x 32b", dashed=1)

# ---- ATDECC taps row ---- #
TY = 1330
box("aecp", 1500, TY, 430, 270,
    "KL_aecp_top — AECP/AEM entity (Milan v1.2 §5.4, la_avdecc-clean)\n\n"
    "ingress MONITOR tap (registered, never backpressures)\n"
    "-> validator -> parser [internal links 64b AXIS BE] -> l0\n"
    "(LOCK 60 s / ACQUIRE=NOT_SUPPORTED) -> response_builder\n"
    "(segment engine NONE/ECHO/STORE/CONST x4 · CDL = frame-26)\n"
    "commands: READ_DESCRIPTOR · names · config · sampling-rate ·\n"
    "stream-format · STREAM_INFO(56B) · AVB_INFO · COUNTERS(136B,\n"
    "full-size on errors) · AS_PATH · MVU GET_MILAN_INFO",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("aecpbuf", 1500, TY+310, 200, 70, "ingress frame buf\n128 B LUTRAM\n(MAX_FRAME_BYTES)")
mem("aecpwork", 1720, TY+310, 210, 70, "builder working set\nbuf_r 64 B FF (capture) ·\nconst_q 64 B FF (payloads)")
mem("aemstore", 1990, TY+310, 400, 110,
    "AEM store — BRAM 808 B (byte port 8b, addr 16b, 1-cycle)\n"
    "directory 5 x 64b FF {type,idx,base,len}\n"
    "ENTITY@0x000/312 · CONFIG@0x138/86 · AUDIO@0x18E/156 ·\n"
    "STREAM_OUT@0x22A/156 · AVB_IF@0x2C6/98\n"
    "wb: names@48/180/316/402/558/714 · rate@534 · fmt@628")
box("acmp", 2480, TY, 380, 270,
    "KL_acmp_responder — ACMP stateless talker (§5.5)\n\n"
    "same registered-tap pattern · 70 B ACMPDU (CDL 44)\n"
    "GET_TX_STATE -> SUCCESS, count=0, stream fields\n"
    "zeroed, probe flags cleared (uid!=0 ->\n"
    "TALKER_UNKNOWN_ID) · GET_TX_CONNECTION ->\n"
    "NOT_SUPPORTED (Milan 5.5.4.4) · CONNECT/\n"
    "DISCONNECT_TX -> NOT_SUPPORTED until the softcore\n"
    "policy mailbox (HW answers / SW decides)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("acmpbuf", 2480, TY+310, 200, 70, "frame buf\n72 B LUTRAM (9 beats)")
box("adp", 2940, TY, 370, 270,
    "adp_advertiser — ADP (§6.2)\n\n82 B ADPDU (CDL 0x38) · periodic every\nvalid_time s (vt=31 -> validity 62 s) ·\nAVAILABLE / DEPARTING / discover response ·\navailable_index +1 on EVERY ADPDU\n(la_avdecc strict rule) · priority: depart >\nlink_up > info/gm change > discover > timer ·\nenable-edge with link up == link_up\n(boot-order fix) · identity: 0x600 CSR group\n(shared with AEM overlay — cannot diverge)",
    fill=ETH[0], stroke=ETH[1], font=10, align="left")
mem("adpidx", 2940, TY+310, 250, 60, "available_index 32b FF\nRO @ 0x644 (live counter)")

box("mux1", 3440, TY+30, 250, 90, "aecp_acmp_mux\n(adp_tx_arbiter)\nframe-atomic RR", fill=CTL[0], stroke=CTL[1], font=10)
box("mux2", 3440, TY+170, 250, 90, "ctl_tx_mux\nADP + (AECP|ACMP)\nframe-atomic RR", fill=CTL[0], stroke=CTL[1], font=10)

edge("et1", "rxnode", "aecp", "tap (copy) 64b LE", dashed=1)
edge("et2", "rxnode", "acmp", "tap (copy) 64b LE", dashed=1)
edge("et3", "aecp", "adp", "ENTITY_DISCOVER pulse 1b", dashed=1)
edge("et4", "aecp", "aecpbuf", "8b", dashed=1)
edge("et5", "aecp", "aemstore", "byte port 8b · addr 16b", dashed=1)
edge("et6", "acmp", "acmpbuf", "8b", dashed=1)
edge("et7", "adp", "adpidx", "32b", dashed=1)
edge("em1", "aecp", "mux1", "resp 64b AXIS LE")
edge("em2", "acmp", "mux1", "resp 64b AXIS LE")
edge("em3", "mux1", "mux2", "64b AXIS LE")
edge("em4", "adp", "mux2", "advertise 64b AXIS LE")

# ---- TX row + its memory row ---- #
TXY = 1910
box("dparb", 1500, TXY, 330, 190,
    "adp_tx_mux (datapath merge)\n\ndata stream (shaped) has priority;\ncontrol (ADP/AECP/ACMP) inserted in\ninter-frame gaps only — zero mid-\nframe jitter · frame-atomic",
    fill=CTL[0], stroke=CTL[1], font=10, align="left")
box("ptptx", 2080, TXY, 340, 190,
    "ptp_ts_top — TX stamp\n\nsame 64b counter · per-frame TX\ntimestamp -> ts window -> driver\n(SO_TIMESTAMPING once the PHC lands)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("cbs", 2670, TXY, 380, 190,
    "traffic_shaping_core + CBS (logic)\n\ncredit gate + strict-priority across 4\nqueues (802.1Q Table 8-5) · sequential\nslope engine (-8K LUTs, bit-exact,\nconfig latency 2 us) · NEVER removed\n(user rule)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("cbsregs", 2670, TXY+230, 380, 70,
    "CBS register file (per queue x4)\nidleSlope 32b + credit/limit regs · @ 0x400 stride 0x20\nreset idleSlopes {300,200,150,100} Mb/s")
mem("queues", 3300, TXY, 380, 190,
    "traffic_queues — BRAM\n\n4 x axis_fifo, 16 KB each (DEPTH 16384\nbytes @ 64b) = 64 KB total · per-queue\ndepth/empty status -> shaper gating\n(no bus address — fabric-internal)")
box("cls", 3930, TXY, 400, 190,
    "traffic_classifier (802.1Q logic)\n\nVLAN TPID 0x8100 parse · PCP[3b] ->\nregen -> traffic class -> queue select\n+ AVTP ethertype 0x22F0 -> class A/B",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
mem("clsregs", 3930, TXY+230, 400, 70,
    "classifier map registers (FF)\nPCP regen 8x3b · prio->TC 8x2b · TC->queue 4x2b\n@ 0x300 CTRL · 0x308 MAP · 0x30C REGEN · 0x310 TCQ")
box("txreader", 4580, TXY, 420, 190,
    "TX DMA reader + HW-TSO (cd_sys)\n\ndescriptor fetch from the 512x8B ring ·\nTSO header-gen (MSS segmentation,\nchain-csum) · reader-bound wall @100 MHz\n(starve 70% — prefetch = next perf lane)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")

edge("ex0", "txreader", "cls", "64b AXIS LE k8 (async FIFO -> cd_milan)", color=SYS[1])
edge("ex1", "cls", "queues", "64b AXIS LE k8 + queue 2b", color=MIL[1])
edge("ex2", "queues", "cbs", "4 x 64b AXIS LE", color=MIL[1])
edge("ex3", "cbs", "ptptx", "64b AXIS LE k8", color=MIL[1])
edge("ex4", "ptptx", "dparb", "64b AXIS LE k8", color=MIL[1])
edge("ex5", "mux2", "dparb", "control 64b AXIS LE (IFG insert)")
edge("ex6", "dparb", "mac", "64b AXIS LE k8", color=MIL[1])
edge("ex7", "mac", "phy", "GMII 8b @ 125 (gtx, IOB FFs)", color=ETH[1])
edge("ex8", "txreader", "txring", "coherent AXI reads 64b", color=SYS[1], dashed=1)
edge("ex9", "cbs", "cbsregs", "4 x 32b slope", dashed=1)
edge("ex10", "cls", "clsregs", "map bits", dashed=1)
edge("ex11", "queues", "cbs", "depth status x4", dashed=1)

# ---- CSR block (register file) ---- #
mem("csr", 620, 1940, 560, 190,
    "milan_csr — REGISTER FILE (~46 x 32b FF) + AXI-Lite slave\n"
    "@ 0x9000_0000, 64 KB window (data 32b, addr 16b), cd_sys side,\n"
    "CDC into cd_milan (cdc_pulse/cdc_handshake for strobes)\n"
    "groups: ID/VER/CAP@0x000 · MAC@0x108 · STATS@0x210 · CLS@0x300 ·\n"
    "CBS@0x400 · PTP@0x500 · ADP identity@0x600 · AECP@0x648 ·\n"
    "ACMP@0x650 · TCAM@0x700 (full map in the table below)\n"
    "o_irq_csr -> PLIC · identity fans out to ADP+AECP+ACMP:\n"
    "one source of wire truth")
edge("ec1", "bus", "csr", "AXI-Lite 32b @ sys", color=SYS[1])
edge("ec2", "csr", "adp", "identity fields (CDC)", dashed=1)
edge("ec3", "csr", "aecp", "identity 4 x 64b + status 32b", dashed=1)
edge("ec4", "csr", "acmp", "identity + counters 2 x 16b", dashed=1)

# ---- mapping tables band ---------------------------------------------------- #
grp("g_maps", 40, 2240, 5480, 480, "address maps · geometries · frame formats  (all values from the sources)")

table("t_csr", 70, 2280, 1120, [
 "0x000 ID='MILN'   0x004 VERSION   0x008 CAP (bit12 ADP, bit13 TCAM)",
 "0x108/0x10C MAC_ALO/AHI ([7:0] = first wire byte)",
 "0x210+4n     STAT0..8 RMON counters (RO)",
 "0x300 CLS_CTRL [0]use_pcp · 0x308 MAP · 0x30C REGEN · 0x310 TCQ",
 "0x400+q*0x20 CBS queue q: idleSlope/credit regs (reset 300/200/150/100 Mb/s)",
 "0x500-0x544  PTP: CTRL INCR ADJ TWLO/HI OFLO/HI CMD TRLO/HI ILAT ELAT",
 "0x600 ADP_CTRL [12:8]valid_time [0]enable  (reset 0x00001F00)",
 "0x604/608 ENTITY_ID · 0x60C/610 MODEL_ID · 0x614 CAPS (0x8588, no",
 "  IDENTIFY bit — no CONTROL descriptor!) · 0x618 TALKER {caps,sources}",
 "0x61C LISTENER {caps,sinks} · 0x620 CTRL_CAPS · 0x624/628 gPTP GM",
 "0x62C [7:0] domain · 0x630 IDX0 {identify,current_cfg} · 0x634 IDX1 iface",
 "0x638/63C ASSOCIATION_ID · 0x640 ADP_CMD W1S [0]advertise [1]depart",
 "0x644 ADP_STATUS RO avail_idx · 0x648 AECP {[16]locked,[15:0]cmds}",
 "0x64C AECP {resps,cfg} · 0x650 ACMP {resps,cmds} · 0x700-0x718 TCAM",
], font=10, title="milan_csr @ 0x9000_0000 (AXI-Lite, 64 KB window)")

table("t_aem", 1230, 2280, 1030, [
 "directory: 5 x 64b {type[63:48], index[47:32], base[31:16], len[15:0]}",
 "  0x0000 ENTITY        @ 0x000  len 312    0x0001 CONFIGURATION @ 0x138  len 86",
 "  0x0002 AUDIO_UNIT    @ 0x18E  len 156    0x0006 STREAM_OUTPUT @ 0x22A  len 156",
 "  0x0009 AVB_INTERFACE @ 0x2C6  len 98     ROM total 808 B, network byte order",
 "write-back (volatile): names ENT0@48 grp@180 CFG@316 AU@402 SO@558 AVBIF@714",
 "  (64 B each) · rate@534 (4 B: 0xBB80/0x17700/0x2EE00 = 48/96/192 k) · fmt@628 (8 B)",
 "overlay (live CSR wins): ENTITY 4-11 eid · 12-19 model · 20-23 caps · 24-31 talker/",
 "  listener · 32-35 ctrl · 36-39 avail_idx · 40-47 assoc · 310-311 cfg;  AVB_IF",
 "  782-787 MAC · 790-797 clock_id {MAC[47:24],FFFE,MAC[23:0]} (= AS_PATH path[0])",
 "generation: avdecc/milan-v12-entity.json -> gen_aem_store.py -> gen/aecp_aem_rom.svh",
], font=10, title="AEM store BRAM — the entity model")

table("t_dma", 2300, 2280, 1150, [
 "TX: ring 512 x 8 B = 4 KB (>= 2 max frames; 8 frame slots) · base/length in BYTES",
 "    (devmem trap: 64-bit CSR high word first) · staging 2048 x 64b (16 KB BRAM) ·",
 "    AXI bursts 16-64 beats x 64b (128-512 B)",
 "RX (per queue x2): 4 slots x 60 pages x 16 KB = 960 KB · CQ depth 8 POP-ORDERED",
 "    (driver mslot60 <-> gateware build_r2slots STRICT pairing) · header-split v3:",
 "    fill length in w0[31:16] -> page <= 32 KB; 16 KB chosen (--hs-page-bytes 16384",
 "    <-> insmod hs_pgsz=16384 STRICT; 256-desc ring FORBIDDEN on <=hsq5 gateware)",
 "RSC: RING_RSC_TOUT in 100 MHz ticks (ethtool -C rx-usecs; default 250 us)",
 "descriptor: {addr, len, flags, RX/TX timestamp window (dts kl,dma-ts @ +0x3100)}",
], font=10, title="DMA geometry (kl-eth <-> fabric contracts)")

table("t_frames", 3510, 2280, 1180, [
 "ADPDU   82 B  subtype 0xFA · CDL 0x38(56) · entity_id@18 · caps@34 · avail_idx@50 ·",
 "              gm@54 · domain@62 · cfg@64 · identify@66 · iface@68 · assoc@70",
 "AECPDU  var.  subtype 0xFB · CDL = frame-26 (base 12; counts after target_eid@18) ·",
 "              controller@26 · seq@34 · u/cmd@36 · payload@38 · LE on wire (parser",
 "              chain internally BE) · runt pad to 60, CDL counts unpadded",
 "ACMPDU  70 B  subtype 0xFC · CDL 44 · stream_id@18 · controller@26 · talker@34 ·",
 "              listener@42 · uids@50/52 · dmac@54 · count@60 · seq@62 · flags@64 ·",
 "              vlan@66 · rsvd@68  (responses multicast, like commands)",
 "multicast 91:E0:F0:01:00:00 (ADP+ACMP) · AVTP ethertype 0x22F0 · min wire frame 60 B",
], font=10, title="control-plane frame formats (wire offsets)")

# ---- state band -------------------------------------------------------------- #
grp("g_state", 40, 2760, 5480, 380, "build + verification state (2026-07-12)")
table("t_builds", 70, 2800, 1400, [
 "AX7101 keeper: build_ax7101_eto_aecp7 (WNS +0.091) — la_avdecc AECP-clean;",
 "  acmp2 sweep (ACMP responder) IN FLIGHT: expect Milan=1 CLEAN",
 "cfg: vexii x2 · 100 MHz sys + 100 MHz milan · rx-queues 2 · hs 16 KB ·",
 "  QSPI flashboot · gtx-tx-invert · timing-opt + floorplan · 3-seed sweeps,",
 "  32 threads/instance (96 aborts P&R), keep best WNS >= 0",
 "Arty keeper: build_arty_v7 (WNS +0.018) — sys 83.333 / milan 50 / MII 100M",
], font=10, title="gateware builds")
table("t_verif", 1510, 2800, 1500, [
 "Verilator: aecp 68/68 · acmp 41/41 · adp 121/121 · milan_dp 26/26 (incl. full-datapath",
 "  ACMP exchange) · classifier/queues/cbs/ptp/tcam harnesses · lint 11/11",
 "co-sim: tsn-gen <-> real RTL over AxiStreamBeat socket 42/42 (CDL oracle: spec, NOT tsn-gen)",
 "portability: Yosys+sv2v generic synth 20/20 (KL_aecp_top 33.6K cells, acmp 8.8K) —",
 "  device-independent (ECP5 proven); sv2v v0.0.13 traps documented",
 "silicon: controller 26/26 (31 with ACMP staged) · la_avdecc: ONLINE, IEEE17221=1, zero AEM",
 "  complaints; Milan=1 gated by ACMP GET_TX_STATE (the acmp2 build)",
], font=10, title="verification ladder")
table("t_perf", 3050, 2800, 1500, [
 "measured ceilings (100 MHz): TX 186 Mbit (TSO zc; reader-bound, starve 70%) · RX 223 (-P2",
 "  steered) / 209 single (RSC) · two-node ADP through the AVB switch TX 83 / RX 94 (100M port)",
 "latency: single-port ceiling = memory (1424 ns/miss: 50% TLB + 50% DRAM) · rx-usecs-low +32%",
 "next perf lanes: TX reader prefetch/multi-outstanding · AF_XDP ZC (RX>500) · 1-hart <70% slices",
 "gPTP: HW timestamps + linuxptp present; kl-eth PHC = the gate (HW_SW_SPLIT next item)",
], font=10, title="performance truth (HW counters, not models)")

xml = ('<mxfile host="app.diagrams.net"><diagram name="milan-system-map">'
       f'<mxGraphModel dx="2000" dy="1400" grid="0" gridSize="10" guides="1" tooltips="1" '
       f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
       'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')
open(sys.argv[1], "w").write(xml)
print("wrote", sys.argv[1], len(cells), "cells")
