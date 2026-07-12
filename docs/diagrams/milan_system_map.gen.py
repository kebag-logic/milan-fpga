#!/usr/bin/env python3
# Generate docs/diagrams/milan_system_map.drawio — THE GIANT system map:
# one oversized page with the complete datapath (RX + TX end to end), every
# block, bus widths + byte-lane convention on every edge, clock domains by
# colour, DMA/ring geometry, and all address mappings (SoC map, milan_csr map,
# AEM store map, QSPI flash slots). Every number mirrors the sources:
# milan_soc.py / milan_datapath.sv / milan_csr.sv / gen/aecp_aem_rom.svh /
# build.sh cfg_ax7101. Board of record: AX7101 (xc7a100t).
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
          f"strokeColor={color};strokeWidth={width};fontSize=11;")
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

# clock-domain palette
SYS   = ("#e1d5e7", "#9673a6")   # sys 100 MHz (CPU/LiteX/DMA engines)
MIL   = ("#dae8fc", "#6c8ebf")   # milan datapath 100 MHz (cd_milan)
ETH   = ("#ffe6cc", "#d79b00")   # eth_rx / eth_tx 125 MHz (LiteEth MAC/PHY)
EXT   = ("#f5f5f5", "#666666")   # off-chip
MEM   = ("#d5e8d4", "#82b366")   # memories / tables
CTL   = ("#fff2cc", "#d6b656")   # arbiters / muxes
NOTE  = ("#fff9d6", "#b3a100")

W, H = 4640, 2980

box("title", 40, 16, W-80, 44,
    "MILAN AVB NIC on VexiiRiscv SoC — THE FULL SYSTEM MAP  ·  AX7101 xc7a100t (board of record; Arty deltas noted)  ·  "
    "every edge: width + lane convention  ·  colours = clock domains  ·  2026-07-12",
    fill="#e8e8e8", stroke="#333", font=20, rounded=0, bold=1)

# ---- legend -------------------------------------------------------------- #
grp("g_leg", 40, 76, 1180, 96, "legend")
box("lg1", 60, 106, 190, 26, "sys @ 100 MHz (cd_sys)", fill=SYS[0], stroke=SYS[1], font=11)
box("lg2", 262, 106, 210, 26, "milan datapath @ 100 MHz (cd_milan)", fill=MIL[0], stroke=MIL[1], font=11)
box("lg3", 484, 106, 210, 26, "eth_rx / eth_tx @ 125 MHz (LiteEth)", fill=ETH[0], stroke=ETH[1], font=11)
box("lg4", 706, 106, 120, 26, "off-chip", fill=EXT[0], stroke=EXT[1], font=11)
box("lg5", 838, 106, 150, 26, "memory / table", fill=MEM[0], stroke=MEM[1], font=11)
box("lg6", 1000, 106, 100, 26, "arbiter", fill=CTL[0], stroke=CTL[1], font=11)
box("lg7", 60, 138, 1040, 26,
    "lane conventions:  LE = little lane (tdata[7:0] = first wire byte, Forencich/MAC)   BE = big lane (tdata[63:56] first — AECP parser chain only)",
    fill=NOTE[0], stroke=NOTE[1], font=10, align="left")

# ---- clock tree ----------------------------------------------------------- #
grp("g_clk", 1260, 76, 1150, 96, "clock tree (S7 PLL, from 200 MHz osc)")
table("t_clk", 1280, 106, 1110, [
 "osc 200 MHz -> PLL: cd_sys 100 MHz · cd_sys4x 400 + dqs(90deg) (DDR3-800) · cd_idelay 200 · cd_milan 100 (own domain since M-A2; Arty: 50)",
 "LiteEth PHY: eth_rx = PHY rx_clk 125 · eth_tx = gtx 125 (tx_clk_invert on AX7101; GMII launch FFs IOB-packed — silicon rule)",
 "crossings: AXI-Lite CSR sys<->milan (bus CDC) · MAC core async FIFOs eth<->milan · DMA engines in sys, AXIS FIFOs to milan",
], font=10)

# ---- SoC / softcore band -------------------------------------------------- #
grp("g_soc", 40, 200, 2360, 560, "SoC / softcore  (LiteX, cd_sys 100 MHz)")

box("cpu", 70, 250, 330, 150,
    "VexiiRiscv x2 harts (RV64IMA)\n\nL2 64 KB (l2-bytes 65536)\nlsu-l1-refill-count=8\nlsu-hardware-prefetch=rpt\nl2-down-pending=8 · l2-general-slots=16\n(1-hart decision pending: 58% LUTs datapoint)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("plic", 70, 416, 330, 54, "PLIC + CLINT  (IRQs: milan_csr o_irq_csr,\nkl-eth DMA per-queue, UART, timer)", fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("bus", 430, 250, 210, 220, "LiteX interconnect\n\nWishbone/AXI\n32-bit CSR bus\n+ coherent DMA port\ninto the CPU L2\n(--coherent-dma)", fill=SYS[0], stroke=SYS[1], font=10)
box("dram", 670, 250, 300, 110, "LiteDRAM  DDR3-800\nMT41K256M16 x16 · 512 MB\n(sys4x 400 MHz + DQS 90°, A7DDRPHY,\n200 MHz IDELAYCTRL)", fill=MEM[0], stroke=MEM[1], font=10)
box("uart", 670, 372, 140, 44, "UART 115200\n(litex_term)", fill=SYS[0], stroke=SYS[1], font=10)
box("jtag", 822, 372, 148, 44, "JTAG (openFPGALoader\nft232 210512180081)", fill=SYS[0], stroke=SYS[1], font=9)
box("qspi", 670, 428, 300, 60, "QSPI N25Q128 16 MB (flashboot full)\nkernel@0 (8.5MiB) · opensbi@0x880000 ·\ndtb@0x900000 · rootfs@0x940000", fill=MEM[0], stroke=MEM[1], font=9, align="left")

table("t_socmap", 1000, 250, 660, [
 "SoC address map (VexiiRiscv view)",
 "0x4000_0000  DRAM 512 MB   kernel@+0 · dtb@0x40EF_0000 ·",
 "             opensbi fw_jump@0x40F0_0000 · initrd@0x4100_0000",
 "0x9000_0000  milan_csr AXI-Lite window (64 KB, ADDR_WIDTH=16)",
 "             == the NIC datapath CSR block (map below)",
 "0xf000_0000  LiteX CSRs: UART/timer/SPI/ctrl + kl-eth DMA block",
 "             (ring ctl, RSC tout, steer/hash, IRQ status —",
 "             offsets are BUILD-DEPENDENT: read csr.json, never",
 "             hardcode; e.g. steer q0/q1 telemetry moved between",
 "             P4/P8 cells)",
], font=10, title="memory map")

box("kleth", 1690, 250, 690, 240,
    "kl-eth Linux driver  (kl,dma-ether · silicon; MODULE_VERSION gates identity)\n\n"
    "• 2 RX queues (flow-steered) x threaded NAPI; RX rings in DRAM; budget/gro knobs\n"
    "• RSC ON by default @250 us (ethtool -C rx-usecs retunes RING_RSC_TOUT live; rsc_clk_mhz=100)\n"
    "• header-split hs_pgsz=16384 — MUST match gateware --hs-page-bytes 16384 (STRICT pairing)\n"
    "• multi-slot RX: 4 slots, pop-ordered CQ (wedge-free by construction), 60 KB order-4 buffers\n"
    "• HW-TSO on TX (header-gen in fabric) · chain-csum · ethtool -C ack-merge tout 512 us\n"
    "• identity provisioning once per boot: devmem into 0x9000_0600 group (aecp_csr_setup.sh)\n"
    "• NEXT: PHC /dev/ptpN + SO_TIMESTAMPING (gPTP gate — ARCHITECTURE_HW_SW_SPLIT.md)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")

box("sw2", 1690, 506, 690, 80,
    "userspace: linuxptp ptp4l+phc2sys (present, unvalidated until PHC) · PipeWire module-avb (future media: AAF frames -> kl-eth -> CBS class-A queue) · milan_controller.py / la_avdecc / Hive on the peer validate over the AVB switch",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")

box("dmaeng", 430, 500, 540, 240,
    "kl-eth DMA engines (fabric, cd_sys, coherent port)\n\n"
    "TX reader: descriptor ring 512 x 8 B = 4 KB (>= 2 max frames,\n"
    "8 frame slots) · staging FIFO 2048 beats (16 KB) · AXI bursts\n"
    "16-64 beats (128-512 B) · base/length in BYTES (trap!)\n"
    "+ HW-TSO header generator (validated TX 143->186 zc)\n\n"
    "RX writer: per-queue 4 slots x 60 pages x 16 KB = 960 KB/queue\n"
    "· completion queue depth 8, pop-ordered (mslot60) ·\n"
    "RSC coalescer (tout in 100 MHz ticks) · header-split v3\n"
    "(page fill length in w0[31:16], page <= 32 KB)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")

box("steer", 1000, 500, 330, 130,
    "RX flow steer (2 queues)\n4-tuple hash (IPv4/TCP ihl5) -> q0/q1;\nhash_sel=1 forces q0 (set BEFORE TCP\nruns — silicon rule) · q0/q1 frame\ntelemetry CSRs (csr.json)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("irqn", 1000, 644, 330, 96, "IRQ fan-in\nper-queue RX complete + TX done +\nmilan_csr o_irq_csr -> PLIC\n(rx-usecs-low moderation: +32%)", fill=SYS[0], stroke=SYS[1], font=10, align="left")

edge("es1", "cpu", "bus", "ibus/dbus")
edge("es2", "bus", "dram", "LiteDRAM port")
edge("es3", "bus", "dmaeng", "CSR + coherent DMA (via L2)")
edge("es4", "dmaeng", "dram", "AXI bursts 128-512 B", color=SYS[1])
edge("es5", "kleth", "dmaeng", "rings/doorbells (csr.json offsets)", dashed=1)
edge("es6", "plic", "cpu", "M/S-ext IRQ")
edge("es7", "irqn", "plic", "")
edge("es8", "dmaeng", "steer", "")

# ---- fabric datapath band -------------------------------------------------- #
grp("g_dp", 40, 800, 4560, 1130,
    "milan_datapath (fabric, cd_milan 100 MHz — Arty: 50 MHz)   ·   ALL internal links: AXI4-Stream 64-bit tdata + 8-bit tkeep + tvalid/tready/tlast, LITTLE lane unless marked BE")

# PHY + MAC (left edge, spans RX/TX rows)
box("phy", 70, 900, 190, 560,
    "RTL8211E PHY\n(GMII-strapped,\n8-bit SDR — an\nRGMII read corrupts\nevery byte:\nhardware-confirmed)\n\n1000BASE-T\nto the AVB switch\n(MOTU/peer segment)",
    fill=EXT[0], stroke=EXT[1], font=10, align="left")
box("mac", 300, 900, 330, 560,
    "MilanMAC  (LiteEth)\n\nLiteEthPHYGMII (gtx 125, tx_clk_invert,\nlaunch FFs IOB-packed — placement rule)\n+ LiteEthMACCore: preamble/SFD, CRC32,\npadding, PHY-width conversion 8b<->64b,\nasync FIFOs eth_rx/eth_tx <-> cd_milan\n+ stream<->AXIS adapter:\nlast_be (one-hot) <-> tkeep (mask)\n(the M-A3 no-frame-on-wire root cause)\n\nArty: LiteEthPHYMII (DP83848, 100M,\nis_1g=0 -> CBS slope wiring pending)",
    fill=ETH[0], stroke=ETH[1], font=10, align="left")

# ---- RX row (left -> right), y=900 ---- #
RXY = 900
box("ptprx", 680, RXY, 300, 130,
    "ptp_ts_top — RX stamp\n\n64-bit free-running counter (cd_milan)\nper-frame RX timestamp captured ->\nDMA descriptor ts window\nptp_csr_sync: counter readable over CSR",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("tcam", 1030, RXY, 320, 130,
    "rx_mac_filter (TCAM)\n\n16 entries x {key 48b, mask 48b} on dst\nMAC + action 8b · ternary match ·\ndefault-pass CSR bit · programmed at\n0x700-0x718 (CTRL/KLO/KHI/MLO/MHI/ACT/CMD)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("rxnode", 1400, RXY+35, 260, 60, "rx_axis_to_dma\n(the tap point — post-filter)", fill=MIL[0], stroke=MIL[1], font=11, bold=1)
box("rsc", 1710, RXY, 330, 130,
    "RX DMA front (cd_sys side)\n\nRSC TCP coalescer (RING_RSC_TOUT,\n100 MHz ticks; default 250 us) ·\nheader-split v3 (16 KB pages) ·\n4-slot writer + CQ(8) pop-ordered",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("rxring", 2090, RXY, 300, 130,
    "RX rings in DRAM (per queue)\n\n4 slots x 60 pages x 16 KB = 960 KB\ndescriptors: {addr, len, flags, ts window\n(w/ RX timestamp), page-fill w0[31:16]}",
    fill=MEM[0], stroke=MEM[1], font=10, align="left")

edge("er0", "phy", "mac", "GMII 8b @125 (rx_clk)", color=ETH[1])
edge("er1", "mac", "ptprx", "64b AXIS LE k8", color=MIL[1])
edge("er2", "ptprx", "tcam", "64b AXIS LE k8", color=MIL[1])
edge("er3", "tcam", "rxnode", "64b AXIS LE k8", color=MIL[1])
edge("er4", "rxnode", "rsc", "64b AXIS LE k8 (async FIFO to cd_sys)", color=MIL[1])
edge("er5", "rsc", "rxring", "coherent AXI (via L2)", color=SYS[1])

# ---- ATDECC taps (below RX row) ---- #
TY = 1090
box("aecp", 1400, TY, 430, 260,
    "KL_aecp_top — AECP/AEM entity (Milan v1.2 §5.4, la_avdecc-clean)\n\n"
    "ingress MONITOR tap (registered, never backpressures)\n"
    "-> validator -> parser [64b AXIS BE internally] -> l0 (LOCK 60s /\n"
    "ACQUIRE=NOT_SUPPORTED) -> response_builder (segment engine:\n"
    "NONE/ECHO/STORE/CONST x4, CDL=frame-26)\n"
    "<-> accessor/store/dyn_mux: dir 5 x 64b {type,idx,base,len} ·\n"
    "ROM 808 B x 8b byte port (1-cycle) · write-back names/rate/fmt ·\n"
    "live overlay (entity_id, MAC, caps, avail_idx, cfg, clock_id)\n"
    "commands: READ_DESCRIPTOR · names · config · rate · format ·\n"
    "STREAM_INFO(56B) · AVB_INFO · COUNTERS(136B) · AS_PATH · MVU",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("acmp", 1880, TY, 380, 260,
    "KL_acmp_responder — ACMP stateless talker (§5.5)\n\n"
    "same registered-tap pattern · 70 B ACMPDU (CDL 44)\n"
    "GET_TX_STATE -> SUCCESS, count=0, stream fields\n"
    "zeroed, probe flags cleared (uid!=0 -> TALKER_\n"
    "UNKNOWN_ID) · GET_TX_CONNECTION -> NOT_SUPPORTED\n"
    "(Milan 5.5.4.4) · CONNECT/DISCONNECT_TX -> NOT_\n"
    "SUPPORTED until the softcore policy mailbox\n"
    "(HW answers / SW decides — HW_SW_SPLIT.md)\n"
    "counters -> CSR 0x650",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("adp", 2310, TY, 360, 260,
    "adp_advertiser — ADP (§6.2)\n\n"
    "82 B ADPDU (CDL 0x38) · periodic every\nvalid_time s (vt=31 -> validity 62 s) ·\n"
    "ENTITY_AVAILABLE / DEPARTING / discover\nresponse · available_index +1 on EVERY\n"
    "ADPDU (la_avdecc strict rule) · trigger\npriority: depart > link_up > info/gm\n"
    "change > discover > timer · enable-edge\nwith link up == link_up (boot-order fix)\n"
    "identity: the 0x600 CSR group (shared\nwith AEM overlay — cannot diverge)",
    fill=ETH[0], stroke=ETH[1], font=10, align="left")

edge("et1", "rxnode", "aecp", "tap (copy) 64b LE", dashed=1)
edge("et2", "rxnode", "acmp", "tap (copy) 64b LE", dashed=1)
edge("et3", "aecp", "adp", "ENTITY_DISCOVER pulse", dashed=1)

# ---- control TX merge column ---- #
box("mux1", 2720, TY+20, 250, 90, "aecp_acmp_mux\n(adp_tx_arbiter)\nframe-atomic RR\n64b AXIS LE", fill=CTL[0], stroke=CTL[1], font=10)
box("mux2", 2720, TY+140, 250, 90, "ctl_tx_mux\nADP + (AECP|ACMP)\nframe-atomic RR\n64b AXIS LE", fill=CTL[0], stroke=CTL[1], font=10)
edge("em1", "aecp", "mux1", "resp 64b LE")
edge("em2", "acmp", "mux1", "resp 64b LE")
edge("em3", "mux1", "mux2", "")
edge("em4", "adp", "mux2", "advertise")

# ---- TX row (right -> left), y=1550 ---- #
TXY = 1560
box("txreader", 4130, TXY, 420, 200,
    "TX DMA reader + HW-TSO (cd_sys)\n\ndescriptor ring 512 x 8 B (base/len BYTES!) ·\nstaging 2048 beats (16 KB) · bursts 16-64 beats ·\nTSO header-gen (MSS segmentation in fabric,\nchain-csum) · reader-bound wall @100 MHz\n(starve 70% — prefetch/multi-outstanding = next perf lane)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
box("cls", 3660, TXY, 400, 200,
    "traffic_classifier (802.1Q)\n\nVLAN TPID 0x8100 parse · PCP[3b] ->\nregen table -> traffic class -> queue\n(CSR 0x300 group: CTRL/MAP/REGEN/TCQ;\nidentity map programmed by kl-eth)\n+ AVTP ethertype -> class A/B",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("queues", 3210, TXY, 380, 200,
    "traffic_queues\n\n4 x axis_fifo, 16 KB each (DEPTH\n16384 bytes @ 64b) · per-queue\ndepth/empty status -> shaper\ngating · BRAM",
    fill=MEM[0], stroke=MEM[1], font=10, align="left")
box("cbs", 2760, TXY, 380, 200,
    "traffic_shaping_core + CBS\n\ncredit_based_shaper per class:\nidleSlope/sendSlope (sequential slope\nengine, -8K LUTs, config latency 2 us,\nbit-exact) · credit gate + strict-prio\nacross 4 queues (802.1Q Table 8-5)\nNEVER removed (user rule)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("ptptx", 2310, TXY, 360, 200,
    "ptp_ts_top — TX stamp\n\nsame 64-bit counter · per-frame TX\ntimestamp -> ts FIFO/window ->\ndriver (SO_TIMESTAMPING once the\nPHC lands)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
box("dparb", 1890, TXY, 330, 200,
    "adp_tx_mux (datapath merge)\n\ndata stream (shaped) has priority;\ncontrol (ADP/AECP/ACMP) inserted in\ninter-frame gaps only — zero mid-\nframe jitter · frame-atomic\n64b AXIS LE",
    fill=CTL[0], stroke=CTL[1], font=10, align="left")

edge("ex0", "txreader", "cls", "64b AXIS LE k8 (async to cd_milan)", color=SYS[1])
edge("ex1", "cls", "queues", "64b AXIS LE k8 + queue id", color=MIL[1])
edge("ex2", "queues", "cbs", "4 x 64b AXIS LE", color=MIL[1])
edge("ex3", "cbs", "ptptx", "64b AXIS LE k8", color=MIL[1])
edge("ex4", "ptptx", "dparb", "64b AXIS LE k8", color=MIL[1])
edge("ex5", "mux2", "dparb", "control 64b LE (IFG insert)")
edge("ex6", "dparb", "mac", "64b AXIS LE k8", color=MIL[1])
edge("ex7", "mac", "phy", "GMII 8b @125 (gtx, IOB FFs)", color=ETH[1])
edge("ex8", "txreader", "dram", "coherent AXI reads", color=SYS[1], dashed=1)

# events/counters strip
box("rmon", 680, 1090, 300, 130,
    "ethernet_events + event_counter\n\nRMON-style counters fed by MAC event\npulses (rx/tx frames, CRC err, ...) ->\nCSR STAT0..8 @ 0x210 stride 4",
    fill=MIL[0], stroke=MIL[1], font=10, align="left")
edge("ev1", "mac", "rmon", "event pulses", dashed=1)

# CSR block
box("csr", 680, 1560, 520, 200,
    "milan_csr (AXI-Lite slave @ 0x9000_0000, 32b data / 16b addr)\n\n"
    "sys-side bus, CDC into cd_milan (cdc_pulse/cdc_handshake\nfor strobes) · o_irq_csr -> PLIC · full register map in the\ntable band below · identity 0x600 group fans out to\nADP + AECP + ACMP (single source of wire truth)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left")
edge("ec1", "bus", "csr", "AXI-Lite 32b @sys", color=SYS[1])
edge("ec2", "csr", "adp", "identity/ctrl (CDC)", dashed=1)
edge("ec3", "csr", "aecp", "identity + status", dashed=1)
edge("ec4", "csr", "acmp", "identity + 0x650", dashed=1)
edge("ec5", "csr", "cls", "0x300 classify map", dashed=1)
edge("ec6", "csr", "tcam", "0x700 TCAM prog", dashed=1)
edge("ec7", "csr", "ptprx", "0x2xx? counter rd", dashed=1)

# ---- mapping tables band --------------------------------------------------- #
grp("g_maps", 40, 1980, 4560, 440, "address maps · geometries · frame formats  (all values from the sources)")

table("t_csr", 70, 2020, 1080, [
 "0x000 ID='MILN'  0x004 VERSION  0x008 CAP (bit12 ADP, bit13 TCAM)",
 "0x108/0x10C MAC_ALO/AHI  station MAC ([7:0]=first wire byte)",
 "0x210+4n     STAT0..8 RMON counters (ethernet_events)",
 "0x300 CLS_CTRL [0]use_pcp   0x308 CLS_MAP prio->TC",
 "0x30C CLS_REGEN PCP regen   0x310 CLS_TCQ TC->queue (2b x4)",
 "0x600 ADP_CTRL [12:8]valid_time [0]enable   (reset 0x00001F00)",
 "0x604/608 ENTITY_ID lo/hi    0x60C/610 MODEL_ID lo/hi",
 "0x614 ENTITY_CAPS (0x8588: AEM|CLASS_A|gPTP; no IDENTIFY bit!)",
 "0x618 TALKER {caps[31:16], sources[15:0]}  0x61C LISTENER {caps,sinks}",
 "0x620 CTRL_CAPS   0x624/628 gPTP GM lo/hi   0x62C [7:0] gPTP domain",
 "0x630 IDX0 {identify_idx[31:16], current_cfg[15:0]}  0x634 IDX1 iface",
 "0x638/63C ASSOCIATION_ID lo/hi",
 "0x640 ADP_CMD W1S [0]advertise-now(+bump) [1]depart   (reads 0)",
 "0x644 ADP_STATUS RO live available_index",
 "0x648 AECP_STAT0 RO {[16]locked, [15:0]cmd_count}",
 "0x64C AECP_STAT1 RO {resp_count[31:16], current_config[15:0]}",
 "0x650 ACMP_STAT  RO {resp_count[31:16], cmd_count[15:0]}",
 "0x700-0x718 TCAM: CTRL(default-pass) KLO KHI MLO MHI ACT CMD",
], font=10, title="milan_csr @ 0x9000_0000 (AXI-Lite, 64 KB window)")

table("t_aem", 1190, 2020, 1000, [
 "directory AEM_DIR_C: 5 x 64b {type[63:48], index[47:32], base[31:16], len[15:0]}",
 "  0x0000 ENTITY        @ 0x000  len 312     0x0001 CONFIGURATION @ 0x138  len 86",
 "  0x0002 AUDIO_UNIT    @ 0x18E  len 156     0x0006 STREAM_OUTPUT @ 0x22A  len 156",
 "  0x0009 AVB_INTERFACE @ 0x2C6  len 98      ROM total: 808 B, network byte order",
 "write-back (volatile): names ENT0@48 grp@180 CFG@316 AU@402 SO@558 AVBIF@714 (64 B",
 "  each) · sampling_rate@534 (4 B, {0xBB80,0x17700,0x2EE00}=48/96/192k) · fmt@628 (8 B, 3xAAF)",
 "overlay (live CSR wins): ENTITY 4-11 eid · 12-19 model · 20-23 caps · 24-31 talker/",
 "  listener · 32-35 ctrl_caps · 36-39 avail_idx · 40-47 assoc · 310-311 cfg;",
 "  AVB_IF 782-787 MAC · 790-797 clock_id = {MAC[47:24],FFFE,MAC[23:0]} (= AS_PATH path[0])",
 "generation: avdecc/milan-v12-entity.json -> gen_aem_store.py -> gen/aecp_aem_rom.svh",
], font=10, title="AEM store (BRAM) — the entity model")

table("t_dma", 2230, 2020, 1130, [
 "TX: descriptor ring 512 x 8 B = 4 KB (>= 2 max-size frames; 8 frame slots) ·",
 "    base/length registers are BYTES (devmem trap: 64-bit CSR high-word first) ·",
 "    staging FIFO 2048 beats (16 KB) · AXI bursts 16-64 beats (128-512 B)",
 "RX (per queue, x2 flow-steered): 4 slots x 60 pages x 16 KB page = 960 KB ·",
 "    completion queue depth 8, POP-ORDERED (wedge-invariant by construction;",
 "    driver mslot60 <-> gateware build_r2slots STRICT pairing) ·",
 "    header-split v3: page fill length in w0[31:16] -> page <= 32 KB; 16 KB chosen",
 "    (--hs-page-bytes 16384 <-> insmod hs_pgsz=16384 STRICT pairing; 256-desc ring",
 "    FORBIDDEN on <=hsq5 gateware — BD-ring lap collapse) ·",
 "    RSC coalescer: RING_RSC_TOUT in 100 MHz ticks (ethtool -C rx-usecs; default 250 us)",
 "descriptor: {addr, len, flags, RX/TX timestamp window (dts kl,dma-ts @ 0x3100)}",
], font=10, title="DMA geometry (kl-eth <-> fabric contracts)")

table("t_frames", 3400, 2020, 1150, [
 "ADPDU   82 B  subtype 0xFA · CDL 0x38(56) · entity_id@18 · caps@34 · avail_idx@50 ·",
 "              gm@54 · domain@62 · cfg@64 · identify@66 · iface@68 · assoc@70",
 "AECPDU  var.  subtype 0xFB · CDL=frame-26 (base 12; counts after target_eid@18) ·",
 "              controller@26 · seq@34 · u/cmd@36 · payload@38 (little lane on wire;",
 "              parser chain internally BIG lane) · runt pad to 60, CDL unpadded",
 "ACMPDU  70 B  subtype 0xFC · CDL 44 · stream_id@18 · controller@26 · talker@34 ·",
 "              listener@42 · uids@50/52 · dmac@54 · count@60 · seq@62 · flags@64 ·",
 "              vlan@66 · rsvd@68  (responses multicast, like commands)",
 "multicast 91:E0:F0:01:00:00 (ADP+ACMP) · AVTP ethertype 0x22F0 · min wire frame 60 B",
 "TCAM default entries: station MAC + AVDECC multicast (ADP discovery reaches the taps)",
], font=10, title="control-plane frame formats (wire offsets)")

# ---- bottom band: build/verify state -------------------------------------- #
grp("g_state", 40, 2460, 4560, 400, "build + verification state (2026-07-12)")
table("t_builds", 70, 2500, 1400, [
 "AX7101 keeper: build_ax7101_eto_aecp7 (WNS +0.091) — la_avdecc AECP-clean;",
 "  acmp1 sweep (this ACMP responder) IN FLIGHT: expect Milan=1 CLEAN",
 "cfg: vexii x2 · 100 MHz sys + 100 MHz milan · rx-queues 2 · hs 16 KB ·",
 "  QSPI flashboot · gtx-tx-invert · timing-opt + floorplan · 3-seed sweeps,",
 "  32 threads/instance (96 aborts P&R), keep best WNS >= 0",
 "Arty keeper: build_arty_v7 (WNS +0.018) — sys 83.333 / milan 50 / MII 100M",
], font=10, title="gateware builds")
table("t_verif", 1510, 2500, 1500, [
 "Verilator: aecp 68/68 · acmp 41/41 · adp 121/121 · milan_dp 26/26 (incl. full-datapath",
 "  ACMP exchange) · classifier/queues/cbs/ptp/tcam harnesses · lint 11/11",
 "co-sim: tsn-gen <-> real RTL over AxiStreamBeat socket 42/42 (CDL oracle: spec, NOT tsn-gen)",
 "portability: Yosys+sv2v generic synth 20/20 (KL_aecp_top 33.6K cells, acmp 8.8K) — device-",
 "  independent (ECP5 target proven); sv2v v0.0.13 traps documented (interfaces, $error)",
 "silicon: controller 26/26 (31 with ACMP staged) · la_avdecc: ONLINE, IEEE17221=1, zero AEM",
 "  complaints; Milan=1 gated by ACMP GET_TX_STATE (this build)",
], font=10, title="verification ladder")
table("t_perf", 3050, 2500, 1500, [
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
