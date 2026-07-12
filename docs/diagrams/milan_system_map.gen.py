#!/usr/bin/env python3
# Generate docs/diagrams/milan_system_map.drawio — THE GIANT system map,
# HIERARCHICAL: parent containers with children nested inside (block-in-block),
# every wire with its bus width, every register file / BRAM as its own block
# with size and address, clock domains by colour. Every number mirrors the
# sources: milan_soc.py / milan_datapath.sv / milan_csr.sv /
# gen/aecp_aem_rom.svh / build.sh cfg_ax7101. Board of record: AX7101.
#
# Regenerate: python3 milan_system_map.gen.py milan_system_map.drawio
# Render:     python3 ../../hdl/aecp/doc/atdecc_architecture.render.py milan_system_map.drawio
import html, re, sys

cells = []
def esc(s):
    t = html.escape(s, quote=True).replace("\n", "&#10;")
    return re.sub(r"  +", lambda m: "&#160;" * len(m.group(0)), t)
def box(i, x, y, w, h, label, fill="#dae8fc", stroke="#6c8ebf", font=11,
        rounded=1, dashed=0, align="center", mono=0, bold=0, parent="1"):
    style = (f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"fontSize={font};verticalAlign=middle;align={align};spacingLeft=6;spacingRight=6;")
    if dashed: style += "dashed=1;"
    if mono:   style += "fontFamily=Courier New;"
    if bold:   style += "fontStyle=1;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def cont(i, x, y, w, h, label, stroke="#666666", fill="#fbfbfb", font=13, parent="1"):
    """a CONTAINER: children nest inside (drawio container=1, geometry-relative)"""
    style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"verticalAlign=top;align=left;fontSize={font};fontStyle=1;spacingLeft=10;"
             f"spacingTop=2;container=1;collapsible=0;")
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="{parent}">'
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
def mem(i, x, y, w, h, label, parent="1", font=10):
    """register file / BRAM / DRAM region — its own green block"""
    box(i, x, y, w, h, label, fill="#d5e8d4", stroke="#82b366", font=font,
        align="left", parent=parent)

SYS   = ("#e1d5e7", "#9673a6")
MIL   = ("#dae8fc", "#6c8ebf")
ETH   = ("#ffe6cc", "#d79b00")
EXT   = ("#f5f5f5", "#666666")
CTL   = ("#fff2cc", "#d6b656")
NOTE  = ("#fff9d6", "#b3a100")
# container tints (lighter than the child blocks of the same domain)
SYSC  = ("#f4eef8", "#9673a6")
MILC  = ("#eef4fc", "#6c8ebf")
ETHC  = ("#fdf3e7", "#d79b00")

W, H = 5240, 2640

box("title", 40, 16, W-80, 44,
    "MILAN AVB NIC on VexiiRiscv SoC — FULL SYSTEM MAP (hierarchical)  ·  AX7101 xc7a100t (Arty deltas noted)  ·  "
    "block-in-block: memories live INSIDE their owner  ·  every wire: bus width  ·  colours = clock domains  ·  2026-07-12",
    fill="#e8e8e8", stroke="#333", font=20, rounded=0, bold=1)

# ---- legend + clock tree --------------------------------------------------- #
box("lg1", 60, 80, 190, 26, "sys @ 100 MHz (cd_sys)", fill=SYS[0], stroke=SYS[1], font=11)
box("lg2", 262, 80, 214, 26, "milan datapath @ 100 MHz (cd_milan)", fill=MIL[0], stroke=MIL[1], font=11)
box("lg3", 488, 80, 200, 26, "eth 125 MHz (LiteEth MAC/PHY)", fill=ETH[0], stroke=ETH[1], font=11)
box("lg4", 700, 80, 100, 26, "off-chip", fill=EXT[0], stroke=EXT[1], font=11)
box("lg5", 812, 80, 200, 26, "register file / BRAM / DRAM", fill="#d5e8d4", stroke="#82b366", font=11)
box("lg6", 1024, 80, 90, 26, "arbiter", fill=CTL[0], stroke=CTL[1], font=11)
box("lg7", 60, 114, 1054, 26,
    "lanes: LE = little (tdata[7:0] = first wire byte) · BE = big (tdata[63:56] first — AECP parser chain only)",
    fill=NOTE[0], stroke=NOTE[1], font=10, align="left")
table("t_clk", 1160, 80, 1240, [
 "clocks: osc 200 -> PLL: cd_sys 100 · cd_sys4x 400+dqs90 (DDR3-800) · cd_idelay 200 · cd_milan 100 (Arty 50) · eth_rx/eth_tx 125",
 "crossings: AXI-Lite CSR sys<->milan · MAC dual-clock FIFOs eth<->milan · DMA engines in sys, AXIS FIFOs to milan",
], font=10)

# =========================================================================== #
#  SoC container (everything cd_sys)
# =========================================================================== #
cont("c_soc", 40, 180, 1700, 1000, "SoC / softcore — LiteX, cd_sys 100 MHz", stroke=SYS[1], fill=SYSC[0])

cont("c_cpu", 20, 40, 520, 260, "VexiiRiscv cluster (RV64IMA)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("hart0", 20, 40, 230, 80, "hart 0\n(lsu refill 8,\nprefetch rpt)", fill=SYS[0], stroke=SYS[1], parent="c_cpu")
box("hart1", 270, 40, 230, 80, "hart 1\n(1-hart decision pending:\n58% LUTs datapoint)", fill=SYS[0], stroke=SYS[1], font=10, parent="c_cpu")
mem("l2", 20, 135, 480, 70, "L2 cache — 64 KB shared (l2-bytes 65536)\ndown-pending 8 · general-slots 16 · coherent DMA lands here", parent="c_cpu")
box("plic", 20, 210, 480, 40, "PLIC + CLINT — IRQs: kl-eth per-queue · milan_csr o_irq_csr · UART · timer", fill=SYS[0], stroke=SYS[1], font=10, parent="c_cpu")

box("bus", 580, 40, 210, 260, "LiteX interconnect\n\nWishbone/AXI\nCSR bus 32b +\ncoherent DMA port\ninto the L2\n(--coherent-dma)", fill=SYS[0], stroke=SYS[1], parent="c_soc")
box("dramc", 830, 40, 280, 120, "LiteDRAM controller\nA7DDRPHY (sys4x 400 + DQS 90°,\n200 MHz IDELAYCTRL)", fill=SYS[0], stroke=SYS[1], font=10, parent="c_soc")

cont("c_per", 1130, 40, 550, 260, "peripherals", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("uart", 20, 35, 240, 55, "UART 115200 (litex_term)", fill=SYS[0], stroke=SYS[1], font=10, parent="c_per")
box("jtag", 280, 35, 250, 55, "JTAG — openFPGALoader\nft232 210512180081", fill=SYS[0], stroke=SYS[1], font=10, parent="c_per")
mem("qspi", 20, 105, 510, 140,
    "QSPI flash N25Q128 16 MB (off-chip, flashboot)\n"
    "kernel   @ 0x00_0000  (8.5 MiB budget)\n"
    "opensbi  @ 0x88_0000  (512 KiB, fw_jump)\n"
    "dtb      @ 0x90_0000\n"
    "rootfs   @ 0x94_0000  (6.75 MiB)", parent="c_per")

cont("c_dma", 20, 340, 780, 620, "kl-eth DMA engines (fabric, cd_sys, coherent port into L2)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("txrd", 20, 40, 360, 280,
    "TX descriptor reader + HW-TSO\n\nfetches the 512x8B ring —\nbase/length in BYTES (trap!) ·\nAXI bursts 16-64 beats x 64b\n(128-512 B) · TSO header-gen (MSS\nsegmentation, chain-csum; TX\n143->186 zc) · reader-bound wall\n(starve 70% -> prefetch next)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_dma")
mem("stag", 30, 330, 340, 60, "TX staging FIFO — BRAM\n2048 beats x 64b = 16 KB", parent="c_dma")
box("rxwr", 400, 40, 360, 280,
    "RX writer\n\nRSC TCP coalescer (RING_RSC_TOUT,\n100 MHz ticks, default 250 us) ·\nheader-split v3 (fill len in\nw0[31:16], page <= 32 KB) · 4-slot\nwriter + pop-ordered CQ",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_dma")
box("steer", 410, 330, 340, 90,
    "RX flow steer (2 queues)\n4-tuple hash -> q0/q1 · hash_sel=1\nforces q0 (set BEFORE TCP runs)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_dma")
mem("csrjson", 30, 410, 340, 100,
    "LiteX CSR block @ 0xf000_0000\nring ctl · RSC tout · steer/hash · IRQ status\noffsets BUILD-DEPENDENT: read csr.json!", parent="c_dma")
box("irqn", 410, 440, 340, 70, "IRQ fan-in -> PLIC\nper-queue RX complete + TX done\n(rx-usecs-low moderation: +32%)", fill=SYS[0], stroke=SYS[1], font=10, parent="c_dma")

cont("c_drv", 820, 340, 860, 620, "software (Linux on the softcore)", stroke=SYS[1], fill="#faf6fc", parent="c_soc")
box("kleth", 20, 40, 820, 280,
    "kl-eth driver (kl,dma-ether · silicon; MODULE_VERSION gates identity)\n\n"
    "• 2 RX queues x threaded NAPI · RSC ON @250 us (ethtool -C rx-usecs live)\n"
    "• hs_pgsz=16384 <-> gateware --hs-page-bytes 16384 (STRICT pairing)\n"
    "• 4-slot RX + pop-ordered CQ · 60 KB order-4 buffers (mslot60)\n"
    "• HW-TSO · chain-csum · ack-merge tout 512 us\n"
    "• identity provisioning once/boot: devmem 0x9000_0600 (aecp_csr_setup.sh)\n"
    "• NEXT: PHC /dev/ptpN + SO_TIMESTAMPING (gPTP gate — HW_SW_SPLIT.md)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_drv")
box("ptpd", 20, 340, 820, 90,
    "linuxptp: ptp4l (802.1AS BMCA, servo) + phc2sys — in the rootfs, unvalidated until the PHC lands;\nthen a small bridge writes GM id/domain -> CSR 0x624/0x628 on change (fabric re-advertises + AS_PATH truth)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_drv")
box("pw", 20, 445, 820, 80,
    "PipeWire module-avb (future media plane): crafts AAF frames -> kl-eth -> fabric CBS class-A queue ·\nSRP/MSRP state machines · ACMP connection POLICY via mailbox (HW answers / SW decides)",
    fill=SYS[0], stroke=SYS[1], font=10, align="left", parent="c_drv")
box("peers", 20, 540, 820, 60,
    "validation peers (via the AVB switch): milan_controller.py · la_avdecc enum-probe (Hive's library) · tsn-gen",
    fill=EXT[0], stroke=EXT[1], font=10, align="left", parent="c_drv")

# =========================================================================== #
#  DRAM chip container (off-chip)
# =========================================================================== #
cont("c_dram", 1780, 180, 620, 660,
     "DDR3 SDRAM — MT41K256M16 x16 · 512 MB @ 0x4000_0000 (off-chip, DDR3-800)",
     stroke="#82b366", fill="#f0f7ee")
mem("bootimg", 20, 50, 580, 110,
    "boot images (from QSPI flashboot)\nkernel @ 0x4000_0000 · dtb @ 0x40EF_0000 ·\nopensbi fw_jump @ 0x40F0_0000 · initrd @ 0x4100_0000", parent="c_dram")
mem("txring", 20, 180, 580, 90,
    "TX descriptor ring — 512 x 8 B = 4 KB\n(>= 2 max-size frames; 8 frame slots) · driver-allocated\ndescriptor: {addr, len, flags, TX ts window @ +0x3100}", parent="c_dram")
mem("rxrings", 20, 290, 580, 130,
    "RX rings (per queue x2) — 4 slots x 60 pages x 16 KB = 960 KB\n+ completion queue 8 entries, POP-ORDERED (mslot60 <->\nbuild_r2slots STRICT pairing) · header-split pages: header in\nslot, payload in 16 KB pages · RX ts in descriptor window", parent="c_dram")
box("dramnote", 20, 440, 580, 60,
    "any DRAM row miss costs 1424 ns (50% TLB + 50% DRAM) —\nthe measured single-port latency ceiling", fill=NOTE[0], stroke=NOTE[1], font=10, align="left", parent="c_dram")

# off-chip PHY
box("phy", 1780, 880, 620, 160,
    "RTL8211E PHY (off-chip) — GMII-strapped, 8-bit SDR (an RGMII read corrupts every byte: hardware-confirmed)\n1000BASE-T to the AVB switch  ·  Arty: DP83848 MII 10/100",
    fill=EXT[0], stroke=EXT[1], font=10, align="left")

# =========================================================================== #
#  Fabric container (everything cd_milan) — block-in-block
# =========================================================================== #
cont("c_fab", 2460, 180, 2740, 2160,
     "milan_datapath — fabric, cd_milan 100 MHz (Arty: 50 MHz)  ·  ALL AXIS links: 64b tdata + 8b tkeep + tvalid/tready/tlast, LE unless marked BE",
     stroke=MIL[1], fill=MILC[0])

# --- MAC container --- #
cont("c_mac", 20, 50, 620, 500, "MilanMAC (LiteEth) — eth 125 MHz island", stroke=ETH[1], fill=ETHC[0], parent="c_fab")
box("phyif", 20, 40, 580, 80, "LiteEthPHYGMII — gtx 125 MHz, tx_clk_invert,\nlaunch FFs IOB-packed (silicon placement rule)", fill=ETH[0], stroke=ETH[1], font=10, parent="c_mac")
box("maccore", 20, 135, 580, 80, "LiteEthMACCore — preamble/SFD · CRC32 · padding ·\nPHY-width conversion 8b <-> 64b", fill=ETH[0], stroke=ETH[1], font=10, parent="c_mac")
box("macfifo", 20, 230, 580, 70, "dual-clock stream FIFOs — eth_rx/eth_tx 125 <-> cd_milan 100", fill=ETH[0], stroke=ETH[1], font=10, parent="c_mac")
box("lastbe", 20, 315, 580, 90, "stream <-> AXIS adapter\nlast_be (one-hot) <-> tkeep (mask)\n— the M-A3 'no frame on the wire' root cause", fill=ETH[0], stroke=ETH[1], font=10, parent="c_mac")
box("macnote", 20, 420, 580, 60, "Arty: LiteEthPHYMII (100M) · is_1g=0 -> CBS slope wiring pending", fill=NOTE[0], stroke=NOTE[1], font=10, align="left", parent="c_mac")

# --- RX pipeline container --- #
cont("c_rx", 680, 50, 2040, 500, "RX pipeline (post-MAC -> DMA)", stroke=MIL[1], fill="#f5f9ff", parent="c_fab")
box("ptprx", 20, 40, 440, 200,
    "ptp_ts_top — RX timestamping\n\nper-frame RX timestamp captured into\nthe DMA descriptor ts window\n(dts kl,dma-ts @ +0x3100)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_rx")
mem("ptpcnt", 30, 150, 420, 80, "PTP counter + CSR regs — 64b counter FF\nCSR 0x500-0x544: CTRL/INCR/ADJ/TWlo·hi/\nOFlo·hi/CMD/TRlo·hi/ILAT/ELAT", parent="c_rx")
box("tcam", 520, 40, 460, 200,
    "rx_mac_filter — TCAM dest-MAC filter\n\nternary match · default-pass CSR bit ·\nmiss + no-default -> drop\n(never backpressures)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_rx")
mem("tcamarr", 530, 150, 440, 80, "TCAM entry array — 16 x {key 48b + mask 48b\n+ action 8b} = 1664 b FF · programmed\n@ 0x700-0x718 (CTRL/K/M/ACT/CMD)", parent="c_rx")
box("tap", 1040, 90, 320, 90, "rx_axis_to_dma\nTHE TAP POINT (post-filter)\ntaps are copies — never stall", fill=MIL[0], stroke=MIL[1], font=11, bold=1, parent="c_rx")
box("rmon", 1420, 40, 560, 200,
    "ethernet_events — RMON counters\n\nevent capture fed by MAC pulses\n(rx/tx frames, CRC err, ...)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_rx")
mem("rmonregs", 1430, 150, 540, 70, "event counters — 9 x 32b FF · RO @ 0x210-0x230\n(STAT0..8, stride 4)", parent="c_rx")

# --- ATDECC container --- #
cont("c_atdecc", 680, 590, 2040, 900, "ATDECC control plane — zero-CPU responders (ADP · AECP · ACMP)", stroke=MIL[1], fill="#f5f9ff", parent="c_fab")

cont("c_aecp", 20, 40, 660, 840, "KL_aecp_top — AECP/AEM entity (§5.4, la_avdecc-clean)", stroke=MIL[1], fill="#eef4fc", parent="c_atdecc")
box("aecppipe", 15, 35, 630, 260,
    "ingress MONITOR tap (registered) -> packet_validator ->\ncommon_parser [internal links 64b AXIS BE] -> l0_state\n(LOCK 60 s / ACQUIRE=NOT_SUPPORTED) -> response_builder\n(segment engine NONE/ECHO/STORE/CONST x4 · CDL = frame-26)\n\ncommands: READ_DESCRIPTOR · GET/SET names · config ·\nsampling-rate · stream-format · GET_STREAM_INFO (56 B) ·\nGET_AVB_INFO · GET_COUNTERS (136 B, full-size on errors) ·\nGET_AS_PATH · MVU GET_MILAN_INFO",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_aecp")
mem("aecpbuf", 15, 310, 300, 80, "ingress frame buf\n128 B LUTRAM (MAX_FRAME_BYTES)", parent="c_aecp")
mem("aecpwork", 340, 310, 305, 80, "builder working set\nbuf_r 64 B FF (capture) ·\nconst_q 64 B FF (payloads)", parent="c_aecp")
mem("aemstore", 15, 405, 630, 190,
    "AEM store — BRAM 808 B (byte port 8b, addr 16b, 1-cycle latency)\n"
    "directory 5 x 64b FF {type, idx, base, len}:\n"
    "  ENTITY@0x000/312 · CONFIG@0x138/86 · AUDIO_UNIT@0x18E/156 ·\n"
    "  STREAM_OUTPUT@0x22A/156 · AVB_INTERFACE@0x2C6/98\n"
    "write-back (volatile): names @48/180/316/402/558/714 (64 B each) ·\n"
    "  sampling_rate @534 (4 B) · stream_format @628 (8 B)\n"
    "overlay: live CSR wins (eid, MAC, caps, avail_idx, cfg, clock_id)", parent="c_aecp")
box("aecpcsr", 15, 610, 630, 60, "status -> CSR: 0x648 {locked, cmd_count} · 0x64C {resp_count, cfg}", fill=MIL[0], stroke=MIL[1], font=10, parent="c_aecp")

cont("c_acmp", 710, 40, 620, 420, "KL_acmp_responder — ACMP stateless talker (§5.5)", stroke=MIL[1], fill="#eef4fc", parent="c_atdecc")
box("acmppipe", 15, 35, 590, 230,
    "same registered-tap pattern · 70 B ACMPDU (CDL 44)\n\nGET_TX_STATE -> SUCCESS, count=0, stream fields zeroed,\nprobe flags cleared (uid != 0 -> TALKER_UNKNOWN_ID)\nGET_TX_CONNECTION -> NOT_SUPPORTED (Milan 5.5.4.4)\nCONNECT/DISCONNECT_TX -> NOT_SUPPORTED until the\nsoftcore policy mailbox (HW answers / SW decides)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_acmp")
mem("acmpbuf", 15, 280, 280, 70, "frame buf — 72 B LUTRAM\n(9 beats x 8 B)", parent="c_acmp")
box("acmpcsr", 315, 280, 290, 70, "status -> CSR 0x650\n{resp_count[31:16], cmd_count[15:0]}", fill=MIL[0], stroke=MIL[1], font=10, parent="c_acmp")

cont("c_adp", 710, 480, 620, 400, "adp_advertiser — ADP (§6.2)", stroke=ETH[1], fill=ETHC[0], parent="c_atdecc")
box("adppipe", 15, 35, 590, 230,
    "82 B ADPDU (CDL 0x38) · periodic every valid_time s\n(vt=31 -> validity 62 s) · AVAILABLE / DEPARTING /\ndiscover response · available_index +1 on EVERY ADPDU\n(la_avdecc strict rule) · trigger priority: depart >\nlink_up > info/gm change > discover > timer ·\nenable-edge with link already up == link_up (boot-order fix)",
    fill=ETH[0], stroke=ETH[1], font=10, align="left", parent="c_adp")
mem("adpidx", 15, 280, 290, 60, "available_index — 32b FF\nRO @ 0x644 (live counter)", parent="c_adp")
box("adpid", 325, 280, 280, 90, "identity inputs = the CSR 0x600\ngroup (shared with the AEM\noverlay -> cannot diverge)", fill=ETH[0], stroke=ETH[1], font=10, parent="c_adp")

box("mux1", 1400, 120, 280, 90, "aecp_acmp_mux (adp_tx_arbiter)\nframe-atomic round-robin", fill=CTL[0], stroke=CTL[1], font=10, parent="c_atdecc")
box("mux2", 1400, 300, 280, 90, "ctl_tx_mux\nADP + (AECP|ACMP)\nframe-atomic round-robin", fill=CTL[0], stroke=CTL[1], font=10, parent="c_atdecc")
mem("csr", 1400, 480, 600, 400,
    "milan_csr — REGISTER FILE (~46 x 32b FF)\nAXI-Lite slave @ 0x9000_0000 (64 KB window, data 32b,\naddr 16b) · cd_sys side, CDC into cd_milan\n(cdc_pulse / cdc_handshake for strobes)\n\ngroups:\n  0x000 ID/VERSION/CAP        0x108 station MAC\n  0x210 RMON STAT0..8         0x300 classifier maps\n  0x400 CBS slopes (x4 q)     0x500 PTP group\n  0x600 ADP identity          0x640 ADP cmd/status\n  0x648/0x64C AECP status     0x650 ACMP status\n  0x700 TCAM programming\n\no_irq_csr -> PLIC · identity fans out to ADP + AEM +\nACMP: ONE source of wire truth", parent="c_atdecc", font=10)

# --- TX pipeline container --- #
cont("c_tx", 20, 1520, 2700, 560, "TX pipeline (DMA -> shaped wire; control merged in gaps)", stroke=MIL[1], fill="#f5f9ff", parent="c_fab")
box("cls", 20, 50, 480, 220,
    "traffic_classifier (802.1Q)\n\nVLAN TPID 0x8100 parse · PCP[3b] ->\nregen -> traffic class -> queue select ·\nAVTP ethertype 0x22F0 -> class A/B",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_tx")
mem("clsregs", 30, 170, 460, 90, "classifier map registers (FF)\nPCP regen 8x3b · prio->TC 8x2b · TC->queue 4x2b\n@ 0x300 CTRL · 0x308 MAP · 0x30C REGEN · 0x310 TCQ", parent="c_tx")
mem("queues", 540, 50, 480, 220,
    "traffic_queues — BRAM\n\n4 x axis_fifo, 16 KB each\n(DEPTH 16384 bytes @ 64b) = 64 KB total\nper-queue depth/empty -> shaper gating\n(fabric-internal, no bus address)", parent="c_tx")
box("cbs", 1060, 50, 480, 220,
    "traffic_shaping_core + CBS\n\ncredit gate + strict-priority across 4\nqueues (802.1Q Table 8-5) · sequential\nslope engine (-8K LUTs, bit-exact, config\nlatency 2 us) · NEVER removed (user rule)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_tx")
mem("cbsregs", 1070, 170, 460, 90, "CBS register file (per queue x4)\nidleSlope 32b + credit/limit regs · @ 0x400 stride 0x20\nreset idleSlopes {300,200,150,100} Mb/s", parent="c_tx")
box("ptptx", 1580, 50, 420, 220,
    "ptp_ts_top — TX timestamping\n\nsame 64b counter · per-frame TX\ntimestamp -> ts window -> driver\n(SO_TIMESTAMPING once the PHC lands)",
    fill=MIL[0], stroke=MIL[1], font=10, align="left", parent="c_tx")
box("dparb", 2040, 50, 400, 220,
    "adp_tx_mux — datapath merge\n\nshaped data has priority; control\n(ADP/AECP/ACMP) inserted in inter-\nframe gaps only: zero mid-frame jitter ·\nframe-atomic",
    fill=CTL[0], stroke=CTL[1], font=10, align="left", parent="c_tx")
box("txnote", 20, 300, 2420, 60,
    "order on the wire: TX reader (SoC, cd_sys) -> async FIFO -> classifier -> queues -> CBS -> PTP TX stamp -> datapath merge -> MAC -> PHY  ·  all hops 64b AXIS LE k8",
    fill=NOTE[0], stroke=NOTE[1], font=10, align="left", parent="c_tx")

# =========================================================================== #
#  edges (absolute routing between nested blocks)
# =========================================================================== #
edge("es1", "c_cpu", "bus", "ibus/dbus 64b")
edge("es2", "bus", "dramc", "membus 64b")
edge("es2b", "dramc", "c_dram", "DDR3 x16 @ 400 MHz (DQ 16b DDR)", color=SYS[1])
edge("es3", "bus", "c_dma", "CSR 32b · coherent DMA 64b (via L2)")
edge("es4", "txrd", "txring", "AXI reads 64b, bursts 16-64 beats", color=SYS[1])
edge("es4b", "rxwr", "rxrings", "AXI writes 64b", color=SYS[1])
edge("es5", "kleth", "csrjson", "ring ctl / doorbells 32b", dashed=1)
edge("es7", "irqn", "plic", "irq lines")
edge("es8", "txrd", "stag", "64b", dashed=1)
edge("ec1", "bus", "csr", "AXI-Lite 32b @ sys (CDC)", color=SYS[1])

edge("er0", "phy", "c_mac", "GMII 8b @ 125", color=ETH[1])
edge("er1", "c_mac", "ptprx", "64b AXIS LE k8", color=MIL[1])
edge("er2", "ptprx", "tcam", "64b AXIS LE k8", color=MIL[1])
edge("er3", "tcam", "tap", "64b AXIS LE k8", color=MIL[1])
edge("er4", "tap", "rxwr", "64b AXIS LE k8 (async FIFO -> cd_sys)", color=MIL[1])
edge("ev1", "c_mac", "rmon", "event pulses 1b each", dashed=1)

edge("et1", "tap", "c_aecp", "tap (copy) 64b LE", dashed=1)
edge("et2", "tap", "c_acmp", "tap (copy) 64b LE", dashed=1)
edge("et3", "c_aecp", "c_adp", "ENTITY_DISCOVER pulse 1b", dashed=1)
edge("em1", "c_aecp", "mux1", "resp 64b AXIS LE")
edge("em2", "c_acmp", "mux1", "resp 64b AXIS LE")
edge("em3", "mux1", "mux2", "64b AXIS LE")
edge("em4", "c_adp", "mux2", "advertise 64b AXIS LE")
edge("em5", "mux2", "dparb", "control 64b AXIS LE (IFG insert)")
edge("ec2", "csr", "adpid", "identity fields (CDC)", dashed=1)

edge("ex0", "txrd", "cls", "64b AXIS LE k8 (async FIFO -> cd_milan)", color=SYS[1])
edge("ex1", "cls", "queues", "64b AXIS LE k8 + queue 2b", color=MIL[1])
edge("ex2", "queues", "cbs", "4 x 64b AXIS LE", color=MIL[1])
edge("ex3", "cbs", "ptptx", "64b AXIS LE k8", color=MIL[1])
edge("ex4", "ptptx", "dparb", "64b AXIS LE k8", color=MIL[1])
edge("ex6", "dparb", "c_mac", "64b AXIS LE k8", color=MIL[1])
edge("ex7", "c_mac", "phy", "GMII 8b @ 125 (gtx, IOB FFs)", color=ETH[1])

# =========================================================================== #
#  frame formats + state (flat bands below)
# =========================================================================== #
table("t_frames", 40, 2400, 1700, [
 "ADPDU   82 B  subtype 0xFA · CDL 0x38(56) · entity_id@18 · caps@34 · avail_idx@50 · gm@54 ·",
 "              domain@62 · cfg@64 · identify@66 · iface@68 · assoc@70",
 "AECPDU  var.  subtype 0xFB · CDL = frame-26 (base 12; counts after target_eid@18) · controller@26 ·",
 "              seq@34 · u/cmd@36 · payload@38 · LE on wire (parser chain BE) · runt pad to 60",
 "ACMPDU  70 B  subtype 0xFC · CDL 44 · stream_id@18 · controller@26 · talker@34 · listener@42 ·",
 "              uids@50/52 · dmac@54 · count@60 · seq@62 · flags@64 · vlan@66 · rsvd@68",
 "multicast 91:E0:F0:01:00:00 (ADP+ACMP) · AVTP ethertype 0x22F0 · min wire frame 60 B",
], font=10, title="control-plane frame formats (wire offsets)")

table("t_state", 1780, 2400, 1700, [
 "keeper: build_ax7101_eto_aecp7 (WNS +0.091) la_avdecc AECP-clean · acmp2 sweep IN FLIGHT (Milan=1 gate)",
 "sim: aecp 68/68 · acmp 41/41 · adp 121/121 · milan_dp 26/26 · cosim 42/42 · lint 11/11 · yosys 20/20",
 "silicon: controller 26/26 (31 w/ ACMP staged) · la_avdecc ONLINE, IEEE17221=1, zero AEM complaints",
 "perf: TX 186 (reader-bound) · RX 223 (-P2) / 209 · ADP through the switch TX 83 / RX 94 (100M port)",
 "next: ACMP silicon (Milan=1) · kl-eth PHC (gPTP) · TX reader prefetch · AF_XDP · 1-hart decision",
], font=10, title="state (2026-07-12)")

table("t_arty", 3520, 2400, 1660, [
 "Arty A7-100 deltas: sys 83.333 MHz · cd_milan 50 MHz · LiteEthPHYMII (DP83848, 100M) · is_1g=0",
 "CBS slope wiring pending · keeper build_arty_v7 (WNS +0.018) · QSPI S25FL128S (1-1-1 0x03 reads)",
 "boot: flashboot full set (opensbi_arty: 2 harts, timer 83333000, arty dtb embedded)",
 "driver pairing: insmod kl-eth hs_pgsz=16384 rsc_clk_mhz=50 · two-node ADP discovery VERIFIED",
], font=10, title="Arty board deltas")

xml = ('<mxfile host="app.diagrams.net"><diagram name="milan-system-map">'
       f'<mxGraphModel dx="2000" dy="1400" grid="0" gridSize="10" guides="1" tooltips="1" '
       f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
       'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')
open(sys.argv[1], "w").write(xml)
print("wrote", sys.argv[1], len(cells), "cells")
