# Protocol validation matrix  -  every protocol, and every test that validates it

The full-FPGA Milan solution implements a stack of AVB/TSN/AVDECC protocols. This
document is the **validation contract**: for each protocol it names the standard,
the layer, the HW/SW split, the implementing module(s), the current status, and  - 
crucially  -  **the test(s) that validate it**. It is the checklist to drive the
FPGA-only solution to done.

Read with:
- [`FULL_FPGA_SOLUTION.md`](../overview/FULL_FPGA_SOLUTION.md)  -  the architecture these protocols live in.
- [`MILAN_V12_DEPENDENCY_MATRIX.md`](../reference/MILAN_V12_DEPENDENCY_MATRIX.md)  -  *why* Milan v1.2
  requires each, mapped to FR/NFR.
- [`FR_NFR.md`](../reference/FR_NFR.md)  -  the normative requirement text (`REQ-*`, `FR-*`).

## Legend

**Status:** ✅ done+verified · 🟩 assembled/elaborates (board-gated) · 🟡 partial/prior-work ·
⏳ planned · ➖ out of scope.
**Test kind:** `RTL` = Verilator self-checking harness (`tb/verilator/<name>`) ·
`SYN` = Yosys device-portability (`syn/yosys`) · `SIM` = softcore Verilator sim
(`sw/litex/milan_sim.py`) · `ELAB` = LiteX elaboration + gateware export ·
`BOARD` = on-hardware bring-up test (needs the bitstream) ·
`SW` = software/controller test (scripts in the AVB test suite).

---

## 1. L1 / L2  -  Ethernet, filtering, stats

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| L2-1 | 1G Ethernet MAC + RGMII PHY | 802.3 | HW | `MilanMAC` (LiteEth `LiteEthMACCore` + `s7rgmii`) | 🟩 elaborates | `ELAB` `milan_soc.py --with-mac`; `BOARD` `ping`, `ethtool eth0` link |
| L2-2 | 802.1Q VLAN tag + PCP decode | 802.1Q | HW | `traffic_classifier`, `traffic_class_map` | ✅ | `RTL` cls (200 k), datapath (15), milan_dp (11); `SYN` classifier_wrap |
| L2-3 | Priority regeneration + PCP→TC→queue map | 802.1Q | HW | `traffic_class_map` (CSR `0x300`) | ✅ | `RTL` cls (200 k); `SIM` classifier programmed over CSR |
| L2-4 | Dest-MAC filtering (ternary CAM) |  -  (Milan MAAP/mcast) | HW | `tcam`, `rx_mac_filter` (CSR `0x700`) | ✅ | `RTL` tcam (19), rx_filter (14); `SYN` both |
| L2-5 | RMON statistics counters | RFC 2819-ish | HW | `ethernet_events` (CSR `0x200`) | ✅ | `RTL` csr (46); `BOARD` `ethtool -S eth0` |
| L2-6 | Multicast hash filter |  -  | HW | `milan_csr` MC_HASH (`0x114/0x118`) | 🟩 | `RTL` csr; `BOARD` `ndo_set_rx_mode` |

## 2. Shaping / QoS  -  802.1Qav CBS

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| Q-1 | Credit-based shaper (idleSlope/credit math) | 802.1Qav | HW | `credit_based_shaper` (CSR `0x400`) | ✅ | `RTL` cbs (87 k, vs fixed-point + ideal models); `SYN` |
| Q-2 | Per-queue arbitration + strict-priority bypass | 802.1Qav/Q | HW | `traffic_shaping_core` | ✅ | `RTL` shaper_core (61 k); datapath (15) |
| Q-3 | Shaping only on shaped+activated queues (q0/q1) | Milan/Qav | HW | `credit_based_shaper` (`CBS_EN`) | ✅ | `RTL` cbs, datapath; `BOARD` `tc qdisc … cbs offload` |
| Q-4 | Live CBS reconfiguration (hiCredit clamp) | 802.1Qav | HW | `credit_based_shaper` | ✅ | `RTL` cbs (reconfig scenarios) |
| Q-5 | 802.1Qbv time-aware shaper (TAS) | 802.1Qbv |  -  |  -  | ➖ future | (not in scope; row tracks intent) |

## 3. Timing  -  gPTP / 802.1AS + PHC

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| T-1 | PTP hardware clock (adjfine/adjtime/settime/gettime) | 1588/802.1AS | HW | `timestamp_counter` (CSR `0x500`) | ✅ | `RTL` ptp (201 k, vs 128-bit accumulator) |
| T-2 | CSR↔PHC clock-domain crossing |  -  | HW | `ptp_csr_sync`, `cdc_pulse/handshake` | ✅ | `RTL` ptp_sync, cdc (16); `SYN` |
| T-3 | TX/RX hardware timestamping + metadata stream | 802.1AS | HW | `ptp_ts_top`, `ptp_ts_core` | ✅ | `RTL` ptp, milan_dp (TS AXIS path) |
| T-4 | PHC on a fixed 125 MHz reference (REQ-PTP-07) | Milan | HW | `_CRG` gtx clock (§A.4) | 🟩 | `ELAB`; `BOARD` `ethtool -T eth0` PHC present |
| T-5 | gPTP daemon lock (BMCA, sync/pdelay) | 802.1AS | SW | `ptp4l`/linuxptp | ⏳ | `BOARD` `ptp4l -i eth0 -m` reaches locked |

## 4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| A-1 | ADP advertise (ENTITY_AVAILABLE / DEPARTING) | 1722.1 §6 | HW | `adp_advertiser` (CSR `0x600`) | ✅ | `RTL` adp (121, byte-exact ADPDU), adp_tx (26); `SYN` |
| A-2 | ADP `available_index` semantics (bump-on-change) | 1722.1/Milan | HW | `adp_advertiser` | ✅ | `RTL` adp (index scenarios) |
| A-3 | ADP TX merge into MAC stream |  -  | HW | `adp_tx_arbiter` | ✅ | `RTL` adp_tx (26); milan_dp |
| A-4 | ADP discover (rcv DISCOVER → advertise) | 1722.1 | HW+SW | `adp_advertiser.rcv_discover_i` + parser | 🟡 wire-up | `RTL` adp (discover input); `SW` `avdecc_l2` watch |
| A-5 | AECP / AEM  -  entity model, READ_DESCRIPTOR, GET/SET | 1722.1 §7 | SW | entity model `avdecc/milan-v12-entity.json`; `aem-and-aecp.md` | 🟡 model+prior | `SW` `avdecc_l2` enumerate; `raw_hex` |
| A-6 | AECP SET_STREAM_FORMAT (listener format adaptation) | 1722.1/Milan | SW | entity model (adaptive listener) | 🟡 | `SW` set format 48/96/192 k; `sampling_rates` |
| A-7 | ACMP  -  stream connection management | 1722.1 §8 | SW | controller/daemon | ⏳ | `SW` `tap_acmp` connect/disconnect |
| A-8 | MVU  -  Milan vendor-unique (protocol_id 00-1B-C5-0A-C1-00) | Milan v1.2 | SW | daemon | ⏳ | `SW` `avdecc_l2` MVU commands |
| A-9 | GET_COUNTERS / diagnostic counters | 1722.1/Milan | HW+SW | `milan_csr` stats + daemon | 🟡 | `SW` `avdecc_l2` GET_COUNTERS |
| A-10 | Entity identity (EUI-64 from MAC) | 1722.1 | SW→HW | driver → ADP `ENTITY_ID` | 🟩 | `RTL` csr (0x600); `SW` verify advertised id |

## 5. Reservation + address allocation

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| R-1 | MAAP  -  multicast address allocation | 1722 | SW+HW | daemon + `rx_mac_filter` TCAM | ⏳ | `SW` `maap` claim/defend; `RTL` tcam (filter install) |
| R-2 | MSRP / MVRP  -  stream reservation | 802.1Q | SW | `mrpd`/daemon | ⏳ | `SW` `mrpd` reserve; talker/listener declaration |
| R-3 | SRP bandwidth admission (75% CBS bound) | 802.1Q/Qav | SW+HW | daemon + CBS idleSlope | ⏳ | `SW` reserve then `BOARD` verify CBS idleSlope ≤ 75% |

## 6. Media transport  -  AVTP (IEEE 1722)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| M-1 | AVTP AAF audio format (48/96/192 kHz) | 1722 | SW/HW | entity model formats; talker/listener | ⏳ (D5) | `SW` `thdn` (THD+N), `soak` |
| M-2 | AVTP CRF media clock reference | 1722 | SW/HW | talker/listener | ⏳ (D5) | `SW` `soak` clock-recovery |
| M-3 | Stereo talker (fixed) + adaptive listener | Milan | SW | entity model (`-small-48k.json`) | 🟡 | `SW` format adaptation test |
| M-4 | Media redundancy (1722.1 seamless) | Milan |  -  |  -  | ➖ out of scope | (explicitly excluded  -  see dependency matrix) |

## 7. Host / SoC / driver

| # | Feature | HW/SW | Module(s) | Status | Validating test(s) |
|---|---------|-------|-----------|--------|--------------------|
| H-1 | VexiiRiscv RV64IMA + sv39 MMU boot (NaxRiscv RV64GC historical) | HW | `milan_soc.py` (LiteX + VexiiRiscv) | ✅ | `BOARD` boots Linux on silicon; `SIM` litex_sim boot to `litex>` (evidence) |
| H-2 | CPU reaches milan_csr, reads ID="MILN" (M-A2) | HW | `milan_datapath` + LiteX bus | ✅ | `SIM` `milan_sim.py` mem_read (evidence log) |
| H-3 | `milan_datapath` §A.9 wrapper integrity | HW | `milan_datapath.sv` | ✅ | `RTL` milan_dp (11: ID + TX/RX byte-exact); `SYN` |
| H-4 | AXIS↔memory DMA, simple-mode CSRs (§A.6) | HW | `MilanDMA` (WishboneDMA ×3) | 🟩 | `ELAB` `--with-dma` (CSRs in csr.csv); `BOARD` loopback (M-A3) |
| H-5 | IRQ → PLIC (tx/rx/ts-dma + csr) | HW | `EventManager` → PLIC | 🟩 | `ELAB`; `BOARD` `/proc/interrupts` increments |
| H-6 | Full SoC assembly (NIC+DMA+MAC) | HW | `milan_soc.py --full` | 🟩 | `ELAB` gateware export (all instances present) |
| H-7 | Device portability (non-Xilinx) | HW | all `hdl/` | ✅ | `SYN` 18 tops incl. Lattice ECP5 |
| H-8 | Linux driver: NAPI/XDP/PTP/ethtool | SW | `kl-eth` (`sw/driver/`) | 🟡 ABI | `BOARD` bring-up (M-A5) |
| H-9 | Device tree `kl,dma-ether` | SW | `sw/dts/milan.dtsi` + binding | ✅ struct | `dtc` parse; `BOARD` driver binds |
| H-10 | Artix-7 bitstream (place & route) | HW | `--full --build` | ⛔ blocked | `BOARD`  -  needs Vivado Artix-7 device install |
| H-11 | Soft-TSO via BD chains (driver-segmented GSO: header arena + zero-copy frag BDs) | SW | `kl-eth` (the-private-test-repo `e7b9c77`) + `RingDMAReader` continuity | ✅ | `BOARD` iperf3 @ MTU 1500: TX 58→88 single-flow (103 w/ `-l 1M`) |
| H-12 | TX cs-across-BDs (chain-wide csum pre-pass + BD-ring rewind + published-rd) | HW+SW | `RingDMAReader` v2b (`milan_soc.py`, `e633032`, bitstream rsc6) | ✅ | `SIM` `test_tx_bd.py::test_bd_csum_chain` (suite 8/8); `BOARD` rsc6 iperf3 |
| H-13 | Multi-flow (`-P4`) stability (doorbell-before-stop, reaper-owned cursor, DISCARD black-hole fix, single-seg RSC clamp) | HW+SW | `kl-eth` + `RingDMAWriter` (`9584927`, bitstream rsc5) | ✅ | `SIM` `test_ring_bd.py::test_rsc_tiny_drop_recovers`; `BOARD` iperf3 `-P4` stable |
| H-14 | ACK-run merging (RSC pending-ACK slot: pure-ACK runs → latest-only v1 BD, SACK passthrough) | HW+SW | `RingDMAWriter` (`ee52742`, bitstream rsc7) + `kl-eth` `rsc_tout=25600` (the-private-test-repo `85122fa`) | ✅ | `SIM` `test_ring_bd.py::test_rsc_ack_merge` + `::test_rsc_ack_passthrough_and_ts`; `BOARD` rsc7, `rsc_tout` sweep validated (TX 109→121) |

---

## 8. Test inventory (how to run every automated test today)

| Suite | Command | Proves |
|-------|---------|--------|
| RTL harnesses (17) | `cd tb/verilator && for d in */ ; do (cd $d && make) || break; done` | every HW block above (rows tagged `RTL`) |
| Yosys portability (18) | `cd syn/yosys && ./run.sh` | every block synthesizes device-independently (`SYN`) |
| Softcore sim (M-A1/M-A2) | `./sw/litex/milan_sim.py --xlen 32` then `mem_read 0x90000000` | CPU boots + reaches the NIC CSR (`SIM`) |
| SoC elaboration | `./sw/litex/milan_soc.py --full` | the full FPGA design assembles + exports gateware (`ELAB`) |

`BOARD` and `SW` rows are the on-hardware / controller tests that light up once the
Artix-7 bitstream exists (roadmap step 1 in [`FULL_FPGA_SOLUTION.md`](../overview/FULL_FPGA_SOLUTION.md) §9).
The controller-side scripts and their tokens (`avdecc_l2`, `tap_acmp`, `maap`,
`mrpd`, `thdn`, `soak`, `ptp`, `ethtool`, …) are catalogued in
[`MILAN_V12_DEPENDENCY_MATRIX.md`](../reference/MILAN_V12_DEPENDENCY_MATRIX.md).

## 9. Coverage summary

- **Fully verified in the open toolchain (no hardware):** all L2/QoS/timing HW
  blocks, the HW ADP advertiser, the §A.9 wrapper, device portability, and the
  softcore CPU⇄CSR path  -  rows tagged ✅ (`RTL`/`SYN`/`SIM`).
- **Assembled + elaborating, awaiting the board:** DMA, MAC/PHY, full-SoC, PHC
  reference, mcast/identity  -  rows tagged 🟩 (`ELAB`).
- **Software protocols (prior work / planned):** AVDECC AECP/ACMP/MVU/MAAP,
  SRP/MSRP/MVRP, AVTP media  -  rows tagged 🟡/⏳, validated by the `SW`/`BOARD` suite
  once bring-up starts.
- **Out of scope (recorded, not built):** 802.1Qbv TAS, media redundancy  -  rows ➖.
