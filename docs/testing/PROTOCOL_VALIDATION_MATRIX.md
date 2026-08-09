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

## Contents

- **[Legend](#legend)** — Read this first or the rows are unreadable: the five status glyphs, and the six test kinds (`RTL`/`SYN`/`SIM`/`ELAB`/`BOARD`/`SW`) that say what level of evidence a row actually has. Ends with the standing caveat on the parenthetical check counts — they are historical snapshots, and the harness's own printout is the only figure that cannot rot.
- **[1. L1 / L2  -  Ethernet, filtering, stats](#1-l1--l2-----ethernet-filtering-stats)** — Six rows from the MAC to RMON, each naming its module and CSR group, followed by the note on why L2-1 says GMII: the RGMII PHY it used to name cost four rebuilds and one preamble error per frame before it was retired.
- **[2. Shaping / QoS  -  802.1Qav CBS](#2-shaping--qos-----8021qav-cbs)** — Five CBS rows with the harness check-counts behind them (87 k on the shaper against fixed-point *and* ideal models). Includes a deliberately empty row: 802.1Qbv time-aware shaping, kept only to record that it is out of scope.
- **[3. Timing  -  gPTP / 802.1AS + PHC](#3-timing-----gptp--8021as--phc)** — The PHC, its clock-domain crossing, hardware timestamping and the 125 MHz reference — all hardware. The one software row, T-5, is the `ptp4l` daemon: locked on silicon through the reference switch, carrying the page's only two bench-blocked riders (AS-4 latency calibration, AS-6 DUT-wins-BMCA).
- **[4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2)](#4-discovery--control-----avdecc-ieee-17221-2021--milan-v12)** — Ten rows, A-1 to A-10, and the shortest summary of the page: **all of it is fabric**. ADP, AECP/AEM, the ACMP responder *and* listener/talker state machines, and the Milan MVU commands are zero-CPU responders in [`hdl/ieee17221/`](../../hdl/ieee17221); the only software left is the once-per-boot identity write. The `SW` entries name the controller-side test, not an implementation.
- **[5. Reservation + address allocation](#5-reservation--address-allocation)** — Three rows: MAAP, MSRP/MVRP and the 75 % admission bound — all three in fabric (`KL_maap`, the 11-module lwSRP engine, `KL_lwsrp_bw_gate`), with the note that the admission grant is not just a number: it gates TX and paces the talker. Ends on the one open clause, SR class B provisioned but never declared.
- **[6. Media transport  -  AVTP (IEEE 1722)](#6-media-transport-----avtp-ieee-1722)** — Four rows for AAF, CRF and the NxN talker/listener pair, plus the one explicit exclusion on the page: media redundancy, out of scope by decision, not by omission. The row worth reading is M-2, the only split verdict in the table — the CRF engine and its servo are silicon-proven, while the CRF *stream* is still not carried under a reservation.
- **[7. Host / SoC / driver](#7-host--soc--driver)** — The longest table here. H-11 to H-14 are the throughput lineage — soft-TSO, checksum across BD chains, multi-flow stability, ACK-run merging — each pinned to the bitstream and commit it needs. H-10 is the place-&-route row: three seeds placed and met timing at `0x0014`, and the flashed one reads its own version back off the board.
- **[8. Test inventory (how to run every automated test today)](#8-test-inventory-how-to-run-every-automated-test-today)** — Four commands, all runnable with no hardware and no vendor tools, and what each one actually proves.
- **[9. Coverage summary](#9-coverage-summary)** — The whole matrix folded into four buckets: silicon-validated, proven in the open toolchain but not yet exercised on a board, the two genuinely open clauses, and out of scope. The bucket that used to say "software protocols, planned" is empty.

## Legend

**Status:** ✅ done+verified · 🟩 assembled/elaborates (board-gated) · 🟡 partial/prior-work ·
⏳ planned · ➖ out of scope.
**Test kind:** `RTL` = Verilator self-checking harness (`tb/verilator/<name>`) ·
`SYN` = Yosys device-portability ([`syn/yosys`](../../syn/yosys)) · `SIM` = softcore Verilator sim
([`sw/litex/milan_sim.py`](../../sw/litex/milan_sim.py)) · `ELAB` = LiteX elaboration + gateware export ·
`BOARD` = on-hardware bring-up test (needs the bitstream) ·
`SW` = software/controller test (scripts in the AVB test suite).

**On the parenthetical check counts.** Where a row still carries one - `cls
(200 k)`, `ptp (201 k)`, `tcam (19)` - treat it as a historical order-of-magnitude
snapshot, not a current figure. Every harness prints its own
`checks: <n>  failures: 0` line when it runs, and that printout is the only
number that cannot be stale; new rows on this page do not add one.

---

## 1. L1 / L2  -  Ethernet, filtering, stats

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| L2-1 | 1G Ethernet MAC + **GMII** PHY | 802.3 | HW | `MilanMAC` (LiteEth `LiteEthMACCore` + `LiteEthPHYGMII`) | ✅ on silicon | `ELAB` `milan_soc.py --with-mac`; `BOARD` correct frames both directions (M-A3), `ping`, `ethtool eth0` link |
| L2-2 | 802.1Q VLAN tag + PCP decode | 802.1Q | HW | `traffic_classifier`, `traffic_class_map` | ✅ | `RTL` cls (200 k), datapath (15), milan_dp (11); `SYN` classifier_wrap |
| L2-3 | Priority regeneration + PCP→TC→queue map | 802.1Q | HW | `traffic_class_map` (CSR `0x300`) | ✅ | `RTL` cls (200 k); `SIM` classifier programmed over CSR |
| L2-4 | Dest-MAC filtering (ternary CAM) |  -  (Milan MAAP/mcast) | HW | `tcam`, `rx_mac_filter` (CSR `0x700`) | ✅ | `RTL` tcam (19), rx_filter (14); `SYN` both |
| L2-5 | RMON statistics counters | RFC 2819-ish | HW | `ethernet_events` (CSR `0x200`) | ✅ | `RTL` csr, mac_rmon; `BOARD` `ethtool -S eth0` |
| L2-6 | Multicast hash filter |  -  | HW | `milan_csr` MC_HASH (`0x114/0x118`) | 🟩 | `RTL` csr; `BOARD` `ndo_set_rx_mode` |

> **L2-1 is GMII, not RGMII.** This row used to name LiteEth's `s7rgmii`. The
> AX7101's RTL8211E is strapped for 8-bit SDR GMII, and the RGMII PHY produced
> *exactly one* preamble error per frame until it was retired -
> [`TROUBLESHOOTING.md` §17](../limitations/TROUBLESHOOTING.md#section-17-on-hardware-nic-bring-up-----dma-works-but-no-packet-on-the-wire-its-gmii-not-rgmii)
> is the root-cause write-up.

## 2. Shaping / QoS  -  802.1Qav CBS

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| Q-1 | Credit-based shaper (idleSlope/credit math) | 802.1Qav | HW | `credit_based_shaper` (CSR `0x400`) | ✅ | `RTL` cbs (87 k, vs fixed-point + ideal models); `SYN` |
| Q-2 | Per-queue arbitration + strict-priority bypass | 802.1Qav/Q | HW | `traffic_shaping_core` | ✅ | `RTL` shaper_core (61 k); datapath (15) |
| Q-3 | Shaping only on shaped+activated queues (q4 SR class A / q3 SR class B) | Milan/Qav | HW | `credit_based_shaper` (`CBS_EN`) | ✅ | `RTL` cbs, datapath; `BOARD` `tc qdisc … cbs offload` |
| Q-4 | Live CBS reconfiguration (hiCredit clamp) | 802.1Qav | HW | `credit_based_shaper` | ✅ | `RTL` cbs (reconfig scenarios) |
| Q-5 | 802.1Qbv time-aware shaper (TAS) | 802.1Qbv |  -  |  -  | ➖ future | (not in scope; row tracks intent) |

## 3. Timing  -  gPTP / 802.1AS + PHC

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| T-1 | PTP hardware clock (adjfine/adjtime/settime/gettime) | 1588/802.1AS | HW | `timestamp_counter` (CSR `0x500`) | ✅ | `RTL` ptp (201 k, vs 128-bit accumulator) |
| T-2 | CSR↔PHC clock-domain crossing |  -  | HW | `ptp_csr_sync`, `cdc_pulse/handshake` | ✅ | `RTL` ptp_sync, cdc (16); `SYN` |
| T-3 | TX/RX hardware timestamping + metadata stream | 802.1AS | HW | `ptp_ts_top`, `ptp_ts_core` | ✅ | `RTL` ptp, milan_dp (TS AXIS path) |
| T-4 | PHC on a fixed 125 MHz reference (REQ-PTP-07) | Milan | HW | `_CRG` gtx clock (§A.4) | 🟩 | `ELAB`; `BOARD` `ethtool -T eth0` PHC present |
| T-5 | gPTP daemon lock (BMCA, sync/pdelay) | 802.1AS | SW | `ptp4l`/linuxptp on the softcore, over the fabric PHC | ✅ on silicon · 🟡 AS-4/AS-6 | `BOARD` `asCapable` + full sync through the reference AVB switch, pdelay both ways, offset rms 2-4 ns, HW timestamps with zero config overrides  -  [`GPTP_RXPAD_ROOTCAUSE.md`](../findings/GPTP_RXPAD_ROOTCAUSE.md), [`TIME_SYNC.md` §5](../design/TIME_SYNC.md#5-status-2026-07-25). Open: **AS-4** per-unit ingress/egress latency calibration, **AS-6** DUT-wins-BMCA (switch outranks every Milan-legal value) |

## 4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| A-1 | ADP advertise (ENTITY_AVAILABLE / DEPARTING) | 1722.1 §6 | HW | `adp_advertiser` (CSR `0x600`) | ✅ | `RTL` adp (byte-exact ADPDU), adp_tx, tsn_fuzz `make adp`; `SYN` |
| A-2 | ADP `available_index` semantics (bump-on-change) | 1722.1/Milan | HW | `adp_advertiser` | ✅ | `RTL` adp (index scenarios), tsn_fuzz `make adp` |
| A-3 | ADP TX merge into MAC stream |  -  | HW | `adp_tx_arbiter` | ✅ | `RTL` adp_tx; milan_dp |
| A-4 | ADP discover (rcv DISCOVER → advertise) | 1722.1 | **HW** | `KL_aecp_ingress` decodes ENTITY_DISCOVER → `adp_advertiser.rcv_discover_i` (wired in `milan_datapath`) | ✅ | `RTL` adp (discover input), milan_dp; `BOARD` ADP census (`ether[14]==0xfa`) |
| A-5 | AECP / AEM  -  entity model, READ_DESCRIPTOR, GET/SET | 1722.1 §7 | **HW** | [`hdl/ieee17221/aecp/`](../../hdl/ieee17221/aecp) - `KL_aecp_top` over ingress / validator / response-builder / AEM store / timers, CSR `0x648`+`0x64C`; descriptor ROM generated from [`avdecc/milan-v12-entity.json`](../../avdecc/milan-v12-entity.json) ([`AEM_AND_AECP.md`](../design/AEM_AND_AECP.md)) | ✅ fabric, silicon | `RTL` aecp, hostplane, milan_dp, tsn_fuzz `make aecp`; `SW` la_avdecc enumerate |
| A-6 | AECP SET/GET_STREAM_FORMAT (listener format adaptation, FR-STR-03) | 1722.1/Milan | **HW** | `KL_aecp_response_builder` - validated write-back into the RX monitor's format-compare reference | ✅ | `RTL` aecp, tsn_fuzz `make aecp` (setter legal/illegal + SET→GET); `SW` set format 48/96/192 k |
| A-7 | ACMP  -  stream connection management | 1722.1 §8 | **HW** | `KL_acmp_responder` (stateless GET_TX_*), `KL_acmp_listener` + `KL_acmp_lstn_ctx` (listener SM), `KL_acmp_tlkr_ctx` (PROBE_TX); CSR `0x650`/`0x670`, bind-restore `0x7A0`, per-stream window `0x800` | ✅ fabric, silicon | `RTL` acmp, acmp_lstn, csr (live ctx), persist, hostplane, milan_dp, tsn_fuzz `make acmp`; `SW` `tap_acmp` connect/disconnect |
| A-8 | MVU  -  Milan vendor-unique (protocol_id 00-1B-C5-0A-C1-00) | Milan v1.2 | **HW** | `KL_aecp_response_builder` - GET_MILAN_INFO, SET/GET_SYSTEM_UNIQUE_ID, SET/GET_MEDIA_CLOCK_REFERENCE_INFO (protocol_id checked; non-Milan VU ignored silently) | ✅ | `RTL` aecp, tsn_fuzz `make aecp` (**Milan v1.2 mandatory census 10/10**) |
| A-9 | GET_COUNTERS / diagnostic counters | 1722.1/Milan | **HW** | `KL_aecp_response_builder` `CMD_GET_COUNTERS` (also GET_AVB_INFO / GET_AS_PATH) over the `milan_csr` stat lanes | ✅ | `RTL` aecp, tsn_fuzz `make aecp`; `SW` `avdecc_l2` GET_COUNTERS |
| A-10 | Entity identity (EUI-64 from MAC) | 1722.1 | SW→HW | driver writes CSR `0x600` once per boot; ADP and AEM read the same wires, so wire truth cannot diverge | ✅ | `RTL` csr (`0x600`), aecp; `SW` verify advertised id |

> **§4 is fabric, not daemon.** Every A-row except the once-per-boot identity
> write is a zero-CPU in-fabric responder, per
> [`ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md) rev 2. The
> `SW` entries that remain name the *controller-side* test that exercises the
> fabric, not an implementation.

## 5. Reservation + address allocation

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| R-1 | MAAP  -  multicast address allocation | 1722 | **HW** | `KL_maap` - probe / defend / announce, CSR `0x6CC`-`0x6D4`; the claimed address feeds `rx_mac_filter`'s TCAM | ✅ fabric, silicon | `RTL` maap, hostplane, milan_dp, tcam (filter install); `BOARD` claim/defend on the wire |
| R-2 | MSRP / MVRP  -  stream reservation | 802.1Q | **HW** | **lwSRP** - [`hdl/ieee8021q/srp/`](../../hdl/ieee8021q/srp) (11 modules + pkg, CSR `0x680`): Talker Advertise TX, Listener Ready RX, MVRP VLAN registration | ✅ fabric, silicon | `RTL` lwsrp, lwsrp_ctx, lwsrp_rx, lwsrp_tx, lwsrp_switchpdu, csr (live engine), hostplane, milan_dp; `BOARD` reserve → RSV_OK |
| R-3 | SRP bandwidth admission (75 % CBS bound) | 802.1Q/Qav | **HW** | `KL_lwsrp_bw_gate` - the grant drives the CBS idleSlope **and gates TX** (FR-SRP-03); the gate is also the talker's pacer | ✅ fabric, silicon | `RTL` lwsrp, lwsrp_ctx; `BOARD` reserve then verify CBS idleSlope ≤ 75 % |

> **Open per-clause gap in §5:** SR **class B** is provisioned (q3, reset
> idleSlope 150 Mb/s) but never *declared or used* - the lwSRP engine declares
> class A only. Tracked as row **SRP-8** in
> [`SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md); it does not qualify R-1..R-3,
> which are class-A paths.

## 6. Media transport  -  AVTP (IEEE 1722)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| M-1 | AVTP AAF audio format (48/96/192 kHz) | 1722 | **HW** | talker `KL_aaf_packetizer` (presentation time stamped from the PTP counter → class-A CBS queue); listener `avtp_stream_parser` → `KL_avtp_rx_monitor` → `KL_aaf_rx_depacketizer`; CSR `0x654` + the `0x800` per-stream window | ✅ fabric, silicon | `RTL` aaf, aaf_audio_loop, avtp_parser, avtp_rxmon, avtp_stream, tsn_fuzz `make aaf`; `BOARD` board↔board E2E, `thdn` (THD+N), `soak` |
| M-2 | AVTP CRF media clock reference | 1722 | **HW** | `KL_crf_tx` / `KL_crf_rx` + `KL_mmcm_drp_servo` (CSR `0x738`-`0x74C`) | ✅ fabric; servo locked on silicon at the converter floor · 🟡 **M-CLK-2 open**: the CRF stream is emitted but is not yet VLAN-tagged into the class-A lane under a reservation | `RTL` crf_tx, crf_rx, mmcm_servo, mmcm_servo_autorepair, hostplane, milan_dp; `BOARD` servo lock, `soak` clock-recovery |
| M-3 | NxN talkers/listeners, format-adaptive listener | Milan | **HW** | `N_STREAMS` talker/listener contexts (AX 8×8, Arty 4×4) with per-stream ACMP + lwSRP rows; format adaptation lands via A-6 | ✅ fabric, silicon | `RTL` aaf, acmp_lstn, csr (N=4/8 window), milan_dp nxn; `BOARD` 8×8 E2E |
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
| H-7 | Device portability (non-Xilinx) | HW | all `hdl/` | ✅ | `SYN` all tops incl. Lattice ECP5 (the [`syn/yosys/run.sh`](../../syn/yosys/run.sh) `tops` array is authoritative) |
| H-8 | Linux driver: NAPI/XDP/PTP/ethtool | SW | `kl-eth` ([`sw/driver/`](../../sw/driver)) | 🟡 ABI | `BOARD` bring-up (M-A5) |
| H-9 | Device tree `kl,dma-ether` | SW | [`sw/dts/milan.dtsi`](../../sw/dts/milan.dtsi) + binding | ✅ struct | `dtc` parse; `BOARD` driver binds |
| H-10 | Artix-7 bitstream (place & route) | HW | `--full --build` | ✅ | `BOARD`  -  Vivado 2026.1 has Artix-7 (+Zynq) installed; both boards build and run on silicon. Latest: `0x0014`, three seeds placed and **all three met timing** (WNS +0.147/+0.115/+0.074 ns), flashed seed reads back `VERSION 0x0001_0014`  -  [`FLASH_0x0014_0727.md`](../findings/FLASH_0x0014_0727.md) |
| H-11 | Soft-TSO via BD chains (driver-segmented GSO: header arena + zero-copy frag BDs) | SW | `kl-eth` (the-private-test-repo `e7b9c77`) + `RingDMAReader` continuity | ✅ | `BOARD` iperf3 @ MTU 1500: TX 58→88 single-flow (103 w/ `-l 1M`) |
| H-12 | TX cs-across-BDs (chain-wide csum pre-pass + BD-ring rewind + published-rd) | HW+SW | `RingDMAReader` v2b (`milan_soc.py`, `e633032`, bitstream rsc6) | ✅ | `SIM` `test_tx_bd.py::test_bd_csum_chain` (suite 8/8); `BOARD` rsc6 iperf3 |
| H-13 | Multi-flow (`-P4`) stability (doorbell-before-stop, reaper-owned cursor, DISCARD black-hole fix, single-seg RSC clamp) | HW+SW | `kl-eth` + `RingDMAWriter` (`9584927`, bitstream rsc5) | ✅ | `SIM` `test_ring_bd.py::test_rsc_tiny_drop_recovers`; `BOARD` iperf3 `-P4` stable |
| H-14 | ACK-run merging (RSC pending-ACK slot: pure-ACK runs → latest-only v1 BD, SACK passthrough) | HW+SW | `RingDMAWriter` (`ee52742`, bitstream rsc7) + `kl-eth` `rsc_tout=25600` (the-private-test-repo `85122fa`) | ✅ | `SIM` `test_ring_bd.py::test_rsc_ack_merge` + `::test_rsc_ack_passthrough_and_ts`; `BOARD` rsc7, `rsc_tout` sweep validated (TX 109→121) |

---

## 8. Test inventory (how to run every automated test today)

| Suite | Command | Proves |
|-------|---------|--------|
| RTL harnesses (`ls tb/verilator/` is authoritative) | `cd tb/verilator && for d in */ ; do (cd $d && make) || break; done` | every HW block above (rows tagged `RTL`) |
| Yosys portability (the `run.sh` `tops` array is authoritative) | `cd syn/yosys && ./run.sh` | every block synthesizes device-independently (`SYN`) |
| Softcore sim (M-A1/M-A2) | `./sw/litex/milan_sim.py --xlen 32` then `mem_read 0x90000000` | CPU boots + reaches the NIC CSR (`SIM`) |
| SoC elaboration | `./sw/litex/milan_soc.py --full` | the full FPGA design assembles + exports gateware (`ELAB`) |

`BOARD` and `SW` rows are the on-hardware / controller tests. The bitstream they
were once waiting on exists and both boards run it (see H-10), so these are
regressions now, not future work; the on-hardware sweep and its evidence live in
[`TESTING.md`](TESTING.md). The controller-side scripts and their tokens
(`avdecc_l2`, `tap_acmp`, `maap`, `thdn`, `soak`, `ptp`, `ethtool`, …) are
catalogued in
[`MILAN_V12_DEPENDENCY_MATRIX.md`](../reference/MILAN_V12_DEPENDENCY_MATRIX.md).

## 9. Coverage summary

- **Silicon-validated (in fabric, running on a board):** the L2/QoS/timing HW
  blocks, the MAC + GMII PHY, the whole AVDECC control plane (ADP, AECP/AEM,
  ACMP, MVU), MAAP, lwSRP with its admission gate, the AAF talker/listener pair
  and the CRF engine + media-clock servo, the §A.9 wrapper, the full SoC, the
  bitstream and the driver  -  rows tagged ✅.
- **Proven in the open toolchain, not yet exercised on a board:** the mcast hash
  filter and the fixed-125 MHz PHC reference  -  rows tagged 🟩 (`ELAB`).
- **Genuinely open, per clause, not per subsystem:**
  CRF-as-a-reserved-class-A-stream (M-2, Milan 7.3.3 / `M-CLK-2`), SR class B
  provisioned but never declared (`SRP-8`), and the two gPTP riders on T-5
  (`AS-4` per-unit latency calibration, `AS-6` DUT-wins-BMCA, bench-blocked).
  These are the rows to attack; everything else in §§3-6 is done.
- **Out of scope (recorded, not built):** 802.1Qbv TAS, media redundancy  -  rows ➖.

There is no longer a "software protocols, planned" bucket. Per
[`ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md) rev 2, the only
software left in the end-station's normal operation is linuxptp, the `kl-eth`
driver, the PCM producer and a once-per-boot identity write.
