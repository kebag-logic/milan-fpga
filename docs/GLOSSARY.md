# Glossary

Every term of art used across this repo's documentation, grouped by domain. One line
each; deeper treatment is linked where a dedicated doc exists.

## AVB / TSN / Milan

| Term | Meaning |
|------|---------|
| **AVB** | Audio Video Bridging — the IEEE 802.1 suite (gPTP + SRP + CBS + AVTP) for synchronized, bounded-latency media over Ethernet. |
| **TSN** | Time-Sensitive Networking — the successor umbrella to AVB (adds preemption, TAS, per-stream policing, …). |
| **Milan** | AVnu Alliance's interoperability profile of AVB/AVDECC for pro audio (this project targets **Milan v1.2**). See `MILAN_V12_DEPENDENCY_MATRIX.md`. |
| **AVTP** | Audio Video Transport Protocol (IEEE 1722) — the L2 media transport; carries streams with presentation timestamps. |
| **AVDECC** | Device discovery/enumeration/control (IEEE 1722.1) on top of AVTP; comprises ADP, AECP, ACMP. |
| **ADP** | AVDECC Discovery Protocol — entity advertise/depart (implemented in RTL: `hdl/adp/adp_advertiser.sv`). |
| **AECP** | AVDECC Enumeration & Control Protocol — AEM command/response. |
| **ACMP** | AVDECC Connection Management Protocol — stream connect/disconnect handshakes. |
| **AEM** | AVDECC Entity Model — the descriptor tree describing an entity (`avdecc/milan-v12-entity.json` mirrors ours). |
| **gPTP** | Generalized PTP (IEEE 802.1AS) — network time sync; the basis for presentation time and CBS coordination. |
| **PTP / PHC** | Precision Time Protocol / PTP Hardware Clock — the adjustable in-fabric clock (`ptp_timestamp/`). |
| **Grandmaster (GM)** | The gPTP time source the domain syncs to. |
| **Transparent clock** | A bridge that corrects gPTP event frames for their *residence time* inside the switch (per-port timestamps required). |
| **CBS** | Credit-Based Shaper (IEEE 802.1Qav) — per-queue rate shaper for SR classes (`credit_based_shaper.sv`). |
| **SR class A/B** | Stream-Reservation traffic classes (A: 2 ms, B: 50 ms latency targets); shaped by CBS, mapped via PCP. |
| **SRP / MSRP / MVRP** | Stream Reservation Protocol family — talker/listener bandwidth admission (MSRP) and VLAN registration (MVRP). |
| **Talker / Listener** | AVTP stream source / sink. |
| **Presentation time** | gPTP timestamp inside AVTP packets telling the listener when to render the media. |
| **PCP** | Priority Code Point — the 3-bit priority field in the 802.1Q VLAN tag; classifies traffic to queues. |
| **802.1Q** | VLAN tagging standard (the tag carries VID + PCP). |
| **Best effort (BE)** | Untagged/unshaped traffic — whatever bandwidth the shaped classes leave over. |

## Ethernet / PHY / wire

| Term | Meaning |
|------|---------|
| **MAC** | Media Access Controller — the framing layer (ours: LiteEth `LiteEthMACCore` wrapped by `MilanMAC`). |
| **PHY** | The physical-layer transceiver chip (this board: Realtek **RTL8211E**, copper gigabit). |
| **GMII / RGMII / MII** | (Reduced/) Gigabit Media-Independent Interface — parallel MAC⇄PHY pin protocols; RGMII is DDR-clocked GMII at half the pins. |
| **gtx_clk / gtx-invert** | The MAC-driven 125 MHz GMII TX clock; `--gtx-tx-invert` forwards it 180° shifted so the PHY samples mid-bit — **required** on this board with IOB-packed TX FFs (see `kl-eth-tx-debug.md`). |
| **MDIO** | Two-wire MAC⇄PHY management bus (link status, PHY registers). |
| **FCS / CRC** | Frame Check Sequence — the CRC32 trailer; `rx_crc_errors` at a peer is the wire-integrity truth. |
| **MTU / MSS** | Maximum Transmission Unit (L3 payload per frame; product-pinned to **1500** here) / Maximum Segment Size (TCP payload per segment). |
| **Jumbo frame** | Frame beyond 1500 B MTU (we validated up to 4074 but the product keeps 1500). |
| **Runt** | Frame under the 64-byte Ethernet minimum; receivers drop it silently. |
| **i210** | The Intel gigabit NIC in the peer test host (`amx-pw0`, `enp6s0`) — its `ethtool -S` counters are our wire ground truth. |
| **QSGMII / SGMII** | SerDes-based 1G PHY interfaces (4 ports / 1 port per lane) — *not* used in the 4-port copper plan. |

## FPGA / tooling

| Term | Meaning |
|------|---------|
| **Artix-7 / xc7a100t** | The FPGA family/part on the Alinx AX7101 board (speed grade -2, FGG484 package). |
| **LUT / FF / BRAM** | The FPGA's logic / register / block-RAM resources (100T: ~63k LUT, 135 RAMB36 = ~600 KB). |
| **IOB (packing)** | Placing an interface flip-flop inside the I/O block for deterministic pad timing — `set_property IOB TRUE`; note XDC ignores TCL `if` guards silently. |
| **ODDR** | Dual-data-rate output primitive; forwards clocks (e.g. gtx_clk) cleanly. |
| **XDC** | Xilinx Design Constraints file (pins, clocks, properties). |
| **P&R** | Place and route (the long Vivado phase). |
| **WNS / TNS / WHS** | Worst/Total Negative Slack (setup) and Worst Hold Slack — timing-closure verdicts; negative = failed. |
| **Timing closure** | Getting all paths to meet the clock period; see `RX_RING_DMA.md` for the two lessons this repo paid for (register burst-geometry cones; never load BRAM outputs with adder trees). |
| **DCP** | Design checkpoint — a snapshot Vivado can reopen to inspect placement/routing post-hoc. |
| **CDC** | Clock-domain crossing (async FIFOs, synchronizers); sys 100 MHz ⇄ milan 50 MHz ⇄ eth 125 MHz here. |
| **PLL / MMCM** | On-chip clock synthesis (S7PLL in LiteX). |
| **Verilator** | Open-source SV simulator — every RTL block has a self-checking harness under `tb/verilator/`. |
| **Yosys / sv2v / ECP5** | Open synthesis flow used as a device-portability check (`syn/yosys`). |
| **XPM** | Xilinx Parameterized Macros — removed from `hdl/` (Track 1 de-Xilinx) in favor of open equivalents. |
| **TerosHDL** | The documenter generating per-module docs from `//!` comments (`hdl/**/doc/`). |

## LiteX / SoC / boot

| Term | Meaning |
|------|---------|
| **LiteX / Migen** | The Python SoC builder and its HDL eDSL — `sw/litex/milan_soc.py` is the SoC. |
| **LiteEth / LiteDRAM / LiteSPI** | LiteX ecosystem cores: Ethernet MAC+PHY glue, DDR3 controller, (Q)SPI flash. |
| **VexiiRiscv** | The **current** AVB-switch soft CPU: in-order RISC-V (RV64IMA, sv39 MMU, Linux-capable) from the same SpinalHDL author/flow — smaller and higher-fmax than NaxRiscv, so it leaves fabric for the 4-port switch; exposes the same coherent `dma_bus` + mem-map (drop-in). See `AVB_SWITCH_DIRECTION.md`. |
| **NaxRiscv** | The out-of-order RISC-V soft CPU (RV64GC, MMU, Linux-capable) generated from SpinalHDL/Scala; the **historical** core, now retained only as a pure-NIC/FPU bitstream (`~/litex-milan/work/fpu32.bit`) — superseded by VexiiRiscv for the switch. Netlists regenerate via sbt (`--scala-args`, `--l2-bytes`). |
| **SpinalHDL** | The Scala HDL NaxRiscv and VexiiRiscv are written in. |
| **CSR** | Control/Status Register. Two spaces here: the `milan_csr` AXI-Lite window (`0x9000_0000`, `REGISTER_MAP.md`) and the LiteX CSR bus (`0xf000_xxxx`, DMA/telemetry). |
| **Wishbone / AXI4 / AXI-Lite / AXIS** | Bus protocols: LiteX's native bus; ARM's memory-mapped burst bus (the coherent dma_bus is AXI4); its register-access subset; and AXI-Stream for the datapath. |
| **tvalid/tready/tlast/tkeep** | AXI-Stream handshake, end-of-frame, and byte-enable mask signals. |
| **last_be** | LiteEth's one-hot pointer to the last valid byte — *not* a keep mask; conversion in `MilanMAC` (`keep & ~(keep>>1)`). |
| **Endianness (word-order)** | LiteX 64-bit CSRs split MS-word-first (`base_hi` at +0); DMA `endianness="big"` = **no byte-swap** so memory order == wire order. |
| **Coherent DMA / dma_bus** | NaxRiscv's cache-snooping AXI4 slave (`--coherent-dma`) — DMA sees CPU caches; **not implied by `--all-blocks`** (forgetting it = stale-DRAM bugs). |
| **PLIC / CLINT** | RISC-V platform interrupt controller / core-local timer block. |
| **EventManager** | LiteX per-peripheral IRQ aggregator (our single NIC interrupt line). |
| **OpenSBI** | The RISC-V supervisor firmware (custom `litex_nax` platform) that boots the kernel. |
| **LiteX BIOS** | The ROM bootloader; extended with `linux_flashboot` (patch 0001). |
| **serialboot / flashboot** | Boot-image delivery over UART (litex_term `--images`) vs from QSPI flash (`QSPI_FLASHBOOT.md`). |
| **FBI / crcfbigen** | The LiteX flash-boot image format `[length][crc32][data]` and the tool that wraps images in it. |
| **QSPI / N25Q128** | Quad-SPI flash interface / the board's 16 MB Micron flash chip (needs the `A13` LiteSPI module name for quad mode). |
| **Device tree (DTS/DTB)** | Hardware description passed to Linux; our node is `kl,dma-ether`; per-platform generation via `sw/dts/milan_dt.py`. |
| **Buildroot** | The embedded-Linux build system producing kernel + rootfs (`milan-tests-avb/fpga/buildroot`); NB `linux-reconfigure` does **not** rebuild out-of-tree modules. |
| **litex_term** | The UART console + serialboot uploader (needs a real pty — run in tmux; open the CP2102N via `/dev/serial/by-id`, ttyUSBn shuffles). |

## This design (datapath, DMA, driver)

| Term | Meaning |
|------|---------|
| **milan_datapath** | The §A.9 SystemVerilog wrapper: classifier → CBS queues → PTP timestamping → arbiter, both directions (`hdl/common/milan_datapath.sv`). |
| **MilanMAC / MilanDMA** | The LiteX glue wrapping LiteEth (+ PacketFIFO, IOB constraints) / the three DMA engines (`milan_soc.py`). |
| **MILN** | The CSR ID magic (`0x4D494C4E`) proving the CPU⇄NIC path. |
| **Ring DMA** | The circular coherent-DRAM frame rings (`RingDMAWriter` RX / `RingDMAReader` TX) walked by AXI-burst engines — see `RX_RING_DMA.md` + `RX_RING_OPERATION.svg`. |
| **wr_ptr / rd_ptr / seq** | Ring producer/consumer byte offsets (one side per direction is HW-owned) and the per-frame sequence counter. |
| **Ingress drop-FIFO** | The always-ready store-and-forward front of the RX writer: upstream is *never* backpressured; overload = counted whole-frame drops. |
| **Store-and-forward vs cut-through** | Buffer the whole frame before launching vs stream-as-it-arrives; bare LiteEthMACCore is cut-through, which is why TX needs the PacketFIFO (`TX_STARVATION_FIX.svg`). |
| **PacketFIFO** | LiteX packet-granular FIFO used as the TX store-and-forward stage. |
| **Commit-after-B** | The ring writer advances `wr_ptr` only after the frame's last AXI write response — software can never see a partial frame. |
| **Burst geometry / PREP state** | The per-burst address/length computation (capped by 16 beats, ring wrap, 4 KB AXI rule), registered in a dedicated FSM state for timing. |
| **Whole-frame drop** | The overload contract: a frame is delivered intact or dropped entirely and counted (`dropped` CSR == `rx_missed_errors`); mid-frame corruption is impossible by construction. |
| **Simple-mode DMA** | The old LiteX single-buffer `base/length/enable/done` engines (still used by `dma-ts`). |
| **TCAM** | Ternary CAM (`hdl/common/tcam.sv`) — masked MAC-address matching for steering/switching. |
| **Telemetry (milan_tlm)** | In-fabric frame/beat/stall counters at every pipeline stage + coherent snapshot (`pipeline-telemetry.md`; sysfs `telemetry/snapshot`). |
| **Stall (telemetry)** | A cycle where a stage held valid data the next stage didn't accept — the bottleneck localizer (the RX ring's headline metric is *0 stalls*). |
| **kl-eth** | The Linux platform driver for the NIC (in `milan-tests-avb/fpga/kl-eth/`). |

## Linux networking / performance

| Term | Meaning |
|------|---------|
| **skb** | `struct sk_buff` — the kernel's packet object; `skb->data` is IP-aligned (addr%8==2), which is why DMA paths copy through aligned rings. |
| **NAPI** | The kernel's polled RX/TX servicing context; ours is scheduled by an adaptive hrtimer (20/200 µs) since the rings have no IRQ. |
| **GRO / GSO** | Generic Receive Offload / Generic Segmentation Offload — *software* coalescing: merge RX segments before the stack; segment TX super-packets after it. GSO needs `NETIF_F_SG` + checksum offload declared. |
| **TSO / RSC (LRO)** | The *hardware* twins of GSO/GRO (see `AVB_SWITCH_DIRECTION.md` panel ②) — wire stays MTU 1500, stack pays per-64 KB. |
| **Interrupt coalescing** | Batching many packets per interrupt; our IRQ-less polling is its limit case. |
| **CHECKSUM_PARTIAL / COMPLETE / UNNECESSARY** | skb checksum states: TX "please compute at (start,offset)"; RX "here is the raw sum over the payload" (what our HW delivers in the ring header); RX "already verified". |
| **csum offload** | Computing the ones-complement Internet checksum in hardware; ours rides free in the RX ingress FIFO. |
| **cwnd / RTO / dupACK / TLP** | TCP congestion window; retransmission timeout; duplicate-ACK loss signal; Tail Loss Probe (suspected source of the "531 spurious retransmits" at MTU 1500 — see the C2 investigation). |
| **BDP** | Bandwidth-delay product — the window needed to fill a path (tiny at 0.9 ms RTT / 100 Mbit). |
| **iperf3** | The throughput measurement tool used for every number in these docs. |
| **rx_missed_errors / InCsumErrors / RcvbufErrors** | netdev "HW dropped whole frames" (== `RING_DROPPED`); L4 checksum failures (0 = no corruption); socket-buffer overflow (app can't drain — a CPU limit, not a NIC one). |

## Project shorthand

| Term | Meaning |
|------|---------|
| **M-A1 … M-A6** | The hardware bring-up milestones: A1 boot, A2 CPU reads MILN, A3 DMA/datapath on silicon, A4 …, A5 Linux driver bring-up, A6 descriptor rings/IRQ (largely superseded by the ring DMA engines). |
| **§A.x** | Section numbers of the migration plan in `FULLY_FPGA_RISCV_MIGRATION.md` (e.g. §A.6 DMA, §A.7 MAC/PHY, §A.9 datapath wrapper). |
| **FR-… / NFR-…** | Functional / non-functional requirement IDs (`FR_NFR.md`, `../REQUIREMENTS.md`) — e.g. FR-DRV-* driver features, NFR-LAT-01 latency. |
| **Option 6b** | The descriptor/scatter-gather multi-queue DMA upgrade path (deferred; rings cover today's needs). |
| **Track 1 (de-Xilinx)** | The vendor-independence workstream (vendored `verilog-axis`, XPM removal, Yosys/ECP5 checks). |
| **C1/C2, S1-S5, I1-I6** | The decision-matrix work items in `AVB_SWITCH_DIRECTION.md` (CPU-port, Switch, IPC tracks). |
| **build_ringN** | The overnight bitstream lineage (ring2 = RX ring … ring7 = +csum offload, ring8 = +256 KB L2); copies kept as `~/litex-milan/work/ringN_test.bit`. |
| **amx-pw0** | The peer test host (i210 NIC, `192.168.127.2`) used for all wire-truth measurements. |
