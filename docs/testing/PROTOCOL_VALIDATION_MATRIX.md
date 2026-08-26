[OBSOLETE + 2026-08-16]

# Protocol validation matrix  -  every protocol, and every test that validates it

The full-FPGA Milan solution implements a stack of AVB/TSN/AVDECC protocols. This
document is the **validation contract**: for each protocol it names the standard,
the layer, the HW/SW split, the implementing module(s), the current status, and  - 
crucially  -  **the test(s) that validate it**. It is the checklist to drive the
FPGA-only solution to done.

> ## STATUS 2026-08-13 — the control plane moved, the AECP uCPU landed, and most AECP functions are still absent
>
> This repository's own **ADP advertiser, AECP/AEM engine, ACMP talker and
> listener, and lwSRP applicant are DELETED** — no parameter, no fallback, no
> shadow arm (USER, explicit and repeated: *"remove the old code AECP/ACMP/ADP
> the lwSRP shall be removed as well. Only use the uCPU code"*). Their
> replacement is the **protocol processor**, wrapped by
> `hdl/milan/KL_pp_shadow.sv` and instantiated **unconditionally** by
> `hdl/milan/milan_datapath.sv`. It owns **ADP, ACMP (talker and listener), SRP
> and AECP**, and publishes a class-D wire face the fabric consumes every clock
> (bind record, talker declaration, SRP reservation/slope/domain). MAAP stays in
> this fabric (`KL_maap`), bridged by `hdl/milan/KL_pp_maap_shim.sv`, because the
> processor implements no MAAP by design.
>
> **CORRECTION.** An earlier revision of this page, written the same day, said
> the processor's AECP engine had not landed and that this entity answered no
> AECP/AEM command at all. **That was false.** The AECP uCPU **has landed**. In
> one sentence: *this entity answers `READ_DESCRIPTOR`, and answers every other
> AECP command with a conformant `NOT_IMPLEMENTED` echo.* Specifically —
>
> * `READ_DESCRIPTOR` (0x0004): `SUCCESS` with `configuration_index`, the
>   reserved field and the descriptor; `NO_SUCH_DESCRIPTOR` on a locate miss;
>   `BAD_ARGUMENTS` on a bad configuration index, both error paths carrying the
>   IEEE 1722.1 §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub;
> * `IDENTIFY_NOTIFICATION` (0x0026) arriving as a **command** → `BAD_ARGUMENTS`
>   (§7.4.39.2's opcode-specific rule beats §9.3.5.3.3);
> * everything else, AEM / ADDRESS_ACCESS / MVU alike → a conformant
>   `NOT_IMPLEMENTED` echo with the right `message_type`+1, length and
>   `controller_data_length`, discharging §9.3.5's duty to respond;
> * silently refused, freed and counted with no reply: a command whose
>   `target_entity_id` is not ours, and any AECP **response** arriving as input.
>
> **A `NOT_IMPLEMENTED` echo is not coverage.** Rows **A-6, A-8 and A-9 below
> stay NOT IMPLEMENTED**: `SET/GET_STREAM_FORMAT`, the whole MVU family and
> `GET_COUNTERS` each draw a well-formed refusal and serve no function. **A-5 is
> re-graded to a split verdict** — the descriptor-read path is implemented and
> owned by the uCPU, the rest of AEM is not. Rows A-1..A-4, A-7 and R-2/R-3 are
> re-graded to the protocol processor. The open-gap ledger is
> [`MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md).
>
> **Descriptor enumeration is reachable once the descriptor image is in DRAM.**
> The tracked builder/rootfs handoff supplies it only on an explicit deployment
> transfer; inspection-only/custom flows that skip that handoff still answer
> `BAD_ARGUMENTS`. See A-5. **Known
> gap, kept visible:** Milan Δ7 `ACQUIRE_ENTITY` (`NOT_SUPPORTED` with
> `owner_id` = 0) is **not** distinguished from the generic echo.

Read with:
- [`FULL_FPGA_SOLUTION.md`](../overview/FULL_FPGA_SOLUTION.md)  -  the architecture these protocols live in.
- [`MILAN_V12_DEPENDENCY_MATRIX.md`](../reference/MILAN_V12_DEPENDENCY_MATRIX.md)  -  *why* Milan v1.2
  requires each, mapped to FR/NFR.
- [`FR_NFR.md`](../reference/FR_NFR.md)  -  the normative requirement text (`REQ-*`, `FR-*`).

## Contents

- **[Legend](#legend)** — Read this first or the rows are unreadable: the six status glyphs — including the ❌ that now means "a conformant refusal and no function", not silence — and the six test kinds (`RTL`/`SYN`/`SIM`/`ELAB`/`BOARD`/`SW`) that say what level of evidence a row actually has. Ends with the standing caveat on the parenthetical check counts — they are historical snapshots, and the harness's own printout is the only figure that cannot rot.
- **[1. L1 / L2  -  Ethernet, filtering, stats](#1-l1--l2-----ethernet-filtering-stats)** — Six rows from the MAC to RMON, each naming its module and CSR group, followed by the note on why L2-1 says GMII: the RGMII PHY it used to name cost four rebuilds and one preamble error per frame before it was retired.
- **[2. Shaping / QoS  -  802.1Qav CBS](#2-shaping--qos-----8021qav-cbs)** — Five CBS rows with the harness check-counts behind them (87 k on the shaper against fixed-point *and* ideal models). Includes a deliberately empty row: 802.1Qbv time-aware shaping, kept only to record that it is out of scope.
- **[3. Timing  -  gPTP / 802.1AS + PHC](#3-timing-----gptp--8021as--phc)** — The PHC, its clock-domain crossing, hardware timestamping and the 125 MHz reference — all hardware. The one software row, T-5, records the explicit software-owner option-off `ptp4l` comparison: locked on silicon through the reference switch, carrying the page's only two bench-blocked riders (AS-4 latency calibration, AS-6 DUT-wins-BMCA). The product-default owner is the fabric `gptp-processor`.
- **[4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2)](#4-discovery--control-----avdecc-ieee-17221-2021--milan-v12)** — Ten rows, A-1 to A-10, and the shortest summary of the page after 2026-08-13: **ADP, ACMP, SRP and AECP all moved to the protocol processor, whose AECP uCPU answers `READ_DESCRIPTOR` and refuses everything else conformantly.** A-5 is a split verdict; A-6, A-8 and A-9 carry a ❌ because their functions are absent. The `SW` entries name the controller-side test, not an implementation.
- **[5. Reservation + address allocation](#5-reservation--address-allocation)** — Three rows: MAAP (still this fabric's `KL_maap`), MSRP/MVRP and the 75 % admission bound (both now the protocol processor's SRP face), with the note that the admission grant is not just a number: it gates TX and paces the talker. Ends on the one open clause, SR class B provisioned but never declared, and on the honest slope-ordering change the substitution brought.
- **[6. Media transport  -  AVTP (IEEE 1722)](#6-media-transport-----avtp-ieee-1722)** — Four rows for AAF, CRF and the NxN talker/listener pair, plus the one explicit exclusion on the page: media redundancy, out of scope by decision, not by omission. The row worth reading is M-2, the only split verdict in the table — the CRF engine and its servo are silicon-proven, while the CRF *stream* is still not carried under a reservation.
- **[7. Host / SoC / driver](#7-host--soc--driver)** — The longest table here. H-11 to H-14 are the throughput lineage — soft-TSO, checksum across BD chains, multi-flow stability, ACK-run merging — each pinned to the bitstream and commit it needs. H-10 is the place-&-route row: three seeds placed and met timing at `0x0014`, and the flashed one reads its own version back off the board.
- **[8. Test inventory (how to run every automated test today)](#8-test-inventory-how-to-run-every-automated-test-today)** — Four commands, all runnable with no hardware and no vendor tools, and what each one actually proves.
- **[9. Coverage summary](#9-coverage-summary)** — The whole matrix folded into six buckets: silicon-validated, moved to the protocol processor, the exactly-bounded set the AECP uCPU really implements, **not implemented — a well-formed refusal and no function**, the genuinely open clauses, and out of scope.

## Legend

**Status:** ✅ done+verified · 🟩 assembled/elaborates (board-gated) · 🟡 partial/prior-work ·
⏳ planned · ➖ out of scope · ❌ **NOT IMPLEMENTED — nothing serves this function**
(introduced 2026-08-13; it is deliberately not the same glyph as "planned",
because a controller issuing one of these commands gets a conformant
`NOT_IMPLEMENTED` refusal and no behaviour — a well-formed answer to a question
this device cannot answer, which is not the same as a partial implementation).
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
| T-5 | gPTP daemon lock (explicit software-owner option-off comparison: BMCA, sync/pdelay) | 802.1AS | SW | `ptp4l`/linuxptp on the softcore, over the fabric PHC; never active in the product-default fabric-owner image | ✅ on silicon · 🟡 AS-4/AS-6 | `BOARD` `asCapable` + full sync through the reference AVB switch, pdelay both ways, offset rms 2-4 ns, HW timestamps with zero config overrides  -  the retired RX-pad root-cause finding (#259, in git history), [`TIME_SYNC.md` §5](../design/TIME_SYNC.md#5-status-updated-2026-08-23). Open: **AS-4** per-unit ingress/egress latency calibration, **AS-6** DUT-wins-BMCA (switch outranks every Milan-legal value) |

## 4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| A-1 | ADP advertise (ENTITY_AVAILABLE / DEPARTING) | 1722.1 §6 | HW | **OWNED BY THE PROTOCOL PROCESSOR** — `KL_pp_shadow` wrapping `protocol_processor_top`'s ADP engine; its packed TX rides the control lane | ✅ | `RTL` pp_shadow, milan_dp; `BOARD` ADP census (`ether[14]==0xfa`) |
| A-2 | ADP `available_index` semantics (bump-on-change) | 1722.1/Milan | HW | **OWNED BY THE PROTOCOL PROCESSOR** (`adp_next_avail_index_o` → the `0x600` `A_ADP` word, which is the one live word in that group) | ✅ | `RTL` pp_shadow, milan_dp |
| A-3 | ADP TX merge into MAC stream |  -  | HW | `adp_tx_arbiter` — the generic 2-in-1-out AXIS arbiter, which SURVIVES the plane deletion and is used on the data lane too | ✅ | `RTL` adp_tx; milan_dp |
| A-4 | ADP discover (rcv DISCOVER → advertise) | 1722.1 | **HW** | **OWNED BY THE PROTOCOL PROCESSOR** — its own validator does the DA work; `KL_pp_shadow` classifies EtherType `0x22F0` (any DA) into the control-frame FIFO ahead of the byte serializer | ✅ | `RTL` pp_shadow, milan_dp; `BOARD` ADP census |
| A-5 | AECP / AEM  -  entity model, READ_DESCRIPTOR, GET/SET | 1722.1 §7 | **HW** (descriptor read) · **none** (the rest) | **SPLIT VERDICT.** `KL_aecp_top` and its whole plane — ingress, packet validator, common parser, L0 state, timers, accessor, AEM store, dynamic-map mux, the response builder, `KL_aem_patch`, `KL_persist_journal` and the generated descriptor ROM — are DELETED. **The protocol processor's AECP uCPU is landed and serves `READ_DESCRIPTOR` (0x0004)** with all three status paths (`SUCCESS` + `configuration_index` + reserved + descriptor; `NO_SUCH_DESCRIPTOR`; `BAD_ARGUMENTS`, the two error paths carrying the §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub), plus `IDENTIFY_NOTIFICATION`-as-command → `BAD_ARGUMENTS`, the conformant `NOT_IMPLEMENTED` echo for everything else, and the two silent-refusal rules (foreign `target_entity_id`, response-as-input: freed, counted, no reply). **Every AEM GET/SET is still absent.** The store fetches the model over a read-only master at a compile-time base (`DESC_BASE_P` → the parent's `PP_DESC_BASE_P`, derived by the SoC as the top 1 MiB of `main_ram`); **nothing in this repository builds or loads the image** — the generator is in the submodule, no builder or boot step writes it, and `sw/builder/endstation_builder.py`'s `aecp_aem_rom.svh` is an orphan of the deleted store. So enumeration is *reachable*, and on a stock build **every `READ_DESCRIPTOR` answers `BAD_ARGUMENTS`**, not `NO_SUCH_DESCRIPTOR`: the header magic `"AEMI"` (`0x41454D49`) fails first on a zeroed region, an invalid image then reports `configurations_count` = 0, and the microprogram's `configuration_index < configurations_count` check runs *before* the locate — so every index including 0 is refused and the locate is never reached (a late load heals without a reset; the 4096-cycle watchdog abandons a stalled burst rather than hanging). The two error statuses therefore discriminate: `BAD_ARGUMENTS` to every read = no image or a corrupt one; `NO_SUCH_DESCRIPTOR` = image loaded, that descriptor genuinely absent | 🟡 | **no Verilator suite grades the landed engine**, and no result against this build is recorded in this corpus; `ls tests/features/` for the behave side. The engine's own counters (command, response, drop, locate-miss, last status, last length, image-valid, image-fault) live in the **processor's side-port snapshot window** via `KL_pp_shadow`'s side-port host bridge, **not** at `0x648`: that group stays a structural zero, `aecp_locked` tied 0 (no ACQUIRE/LOCK, lock manager unwired) and `current_config` tied 0 (no SET_CONFIGURATION). The `0x768` BDBG words are structural zeros too |
| A-6 | AECP SET/GET_STREAM_FORMAT (listener format adaptation, FR-STR-03) | 1722.1/Milan | **none** | **❌ NOT IMPLEMENTED** — both draw the generic `NOT_IMPLEMENTED` echo. The only writer of the RX monitor's format-compare reference is gone, so a listener still cannot be told to follow a talker's format; a well-formed refusal does not adapt a format | ❌ | none |
| A-7 | ACMP  -  stream connection management | 1722.1 §8 | **HW** | **OWNED BY THE PROTOCOL PROCESSOR** — talker and listener both, republished as a class-D bind record the fabric consumes every clock. The DA gate IS the talker gate: `acmp_declaring_o` asserts only after a MAAP `ALLOC_DA` success | ✅ | `RTL` pp_shadow, milan_dp, maap; `SW` `tap_acmp` connect/disconnect |
| A-8 | MVU  -  Milan vendor-unique (protocol_id 00-1B-C5-0A-C1-00) | Milan v1.2 | **none** | **❌ NOT IMPLEMENTED** — MVU rides AECP and is an unimplemented message type, so GET_MILAN_INFO, SET/GET_SYSTEM_UNIQUE_ID and SET/GET_MEDIA_CLOCK_REFERENCE_INFO all draw the generic `NOT_IMPLEMENTED` echo. A controller still cannot complete the Milan identity handshake: it receives a refusal instead of a timeout, and no `features_flags`, no `protocol_version`, no identity | ❌ | none |
| A-9 | GET_COUNTERS / diagnostic counters | 1722.1/Milan | **HW** | **IMPLEMENTED FOR SUPPORTED TARGETS.** Every declared Stream Output has a live five-counter bank and returns the compact Milan layout. Stream Input, AVB Interface and Clock Domain retain their served processor paths. The Table 5.22 unsolicited change producer remains open | ✅ solicited | `RTL` pp_top, milan_dp, tkdiag; pinned la_avdecc decoder |
| A-10 | Entity identity (EUI-64 from MAC) | 1722.1 | SW→HW | driver writes CSR `0x600` once per boot; `entity_id` is handed to the protocol processor and goes out in the ADPDU. The AEM half of "ADP and AEM read the same wires" is no longer a shared-wire fact: the AEM side is whatever the descriptor image in DRAM says, and nothing in this repo writes that image | ✅ ADP half | `RTL` csr (`0x600`), pp_shadow; `SW` verify advertised id |

> **§4 is fabric, not daemon — and the AECP quarter of it is one implemented
> command and a refusal.** Every A-row except the once-per-boot identity write
> is a zero-CPU in-fabric responder, per
> [`ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md) rev 2. "In
> fabric" still does not imply "present": A-6, A-8 and A-9 have no function
> behind them, only the conformant `NOT_IMPLEMENTED` echo, and A-5 is present
> only for the descriptor read. The `SW` entries that remain name the
> *controller-side* test that exercises the fabric, not an implementation.
>
> **Two `0x600` traps for anyone writing an A-row test.** The whole
> `A_ADP_DIAG` / `A_ADP_DIAG2` sub-group (depart count, rearm count, depart
> source, sent count, discover-rx count, discover-seen, last message, advertiser
> state) is a **structural zero** — the advertiser that fed it is deleted, so a
> test must observe the wire. And **entity_capabilities, valid_time,
> association_id, controller_capabilities, interface_index** plus the
> advertise/depart strobes are **write-only scratch**: they read back what
> software wrote and the value no longer reaches the wire, because the
> processor's ADP engine holds them as internal constants and exposes no port.
> Writing them changes nothing observable.
>
> **`PP_CTRL[0]` and `ADP_CTRL.en` (`0x600` bit 0) are ORed** — either one
> enables the entity, because `ADP_CTRL.en` is the bit every existing board
> script writes and there is only one control plane now. The `0x920`-`0x930`
> protocol-processor window is **unconditional**: `milan_csr`'s `PP_PLANE_P`
> parameter is gone, the window is always decoded, and `PP_STAT` always carries
> its `0x5B` tag.

## 5. Reservation + address allocation

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| R-1 | MAAP  -  multicast address allocation | 1722 | **HW** | `KL_maap` - probe / defend / announce, CSR `0x6CC`-`0x6D4`; the claimed address feeds `rx_mac_filter`'s TCAM. **Still this fabric's**, because the protocol processor implements no MAAP by design; `KL_pp_maap_shim` bridges its per-source ALLOC/RELEASE face to the block allocator | ✅ fabric, silicon | `RTL` maap, hostplane, milan_dp, tcam (filter install); `BOARD` claim/defend on the wire |
| R-2 | MSRP / MVRP  -  stream reservation | 802.1Q | **HW** | **OWNED BY THE PROTOCOL PROCESSOR.** The whole lwSRP applicant / registrar / TA-registrar / walker / ctx / ctx_tx / rx / ingress / timers / bw_gate is DELETED; SRP is now the processor's, published on the class-D face (reservation, granted slope, domain). Its MRP frames are classified into `KL_pp_shadow`'s FIFO by the two DA+EtherType pairs its V9 rule passes: `01-80-C2-00-00-0E` + `0x22EA` (MSRP) and `01-80-C2-00-00-21` + `0x88F5` (MVRP) | ✅ | `RTL` pp_shadow, milan_dp; `BOARD` reserve → RSV_OK |
| R-3 | SRP bandwidth admission (75 % CBS bound) | 802.1Q/Qav | **HW** | **OWNED BY THE PROTOCOL PROCESSOR** — `srp_granted_slope_bps_o` drives the CBS idleSlope and `srp_active_o` gates TX (FR-SRP-03) | ✅ | `RTL` pp_shadow, milan_dp; `BOARD` reserve then verify CBS idleSlope ≤ 75 % |

> **What survives at `0x680`, and what does not.** The lwSRP CSR group is an
> ABI and no register was removed, but the MRPDU tx/rx counts and rx drops are
> now **structural zeros** — the serializer that fed them is deleted. The
> **DOMAIN word (adopted / priority / VID), the granted slope and the
> over-limit bit are still live**, repointed to the processor's class-D SRP
> face. The provisioning words the deleted applicant read — **DMAC,
> MaxFrameSize, MaxIntervalFrames and the declare-bypass bit** — are
> **write-only scratch**: they read back what software wrote and change nothing
> observable. The `0x800` window's SRP attribute-row port grants nothing and
> reads back zero.

> **An honest ordering change on the CBS slope, not a regression.**
> `KL_lwsrp_bw_gate` joined a stream's idleSlope into the running sum BEFORE
> opening its gate and closed the gate BEFORE removing the slope. The processor
> asserts `srp_active_o` and `srp_granted_slope_bps_o` in the SAME cycle. On the
> opening edge that is at worst equal, never worse; on the closing edge the sum
> is briefly high for zero traffic — conservative, not permissive. Neither edge
> lets a stream transmit against an un-budgeted slope.

> **Open per-clause gap in §5:** SR **class B** is provisioned (q3, reset
> idleSlope 150 Mb/s) but never *declared or used* - class A only, and that is
> unchanged by the substitution. Tracked as row **SRP-8** in
> [`SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md); it does not qualify R-1..R-3,
> which are class-A paths.

## 6. Media transport  -  AVTP (IEEE 1722)

| # | Protocol / feature | Std | HW/SW | Module(s) | Status | Validating test(s) |
|---|--------------------|-----|-------|-----------|--------|--------------------|
| M-1 | AVTP AAF audio format (48/96/192 kHz) | 1722 | **HW** | talker `KL_aaf_packetizer` (presentation time stamped from the PTP counter → class-A CBS queue); listener `avtp_stream_parser` → `KL_avtp_rx_monitor` → `KL_aaf_rx_depacketizer`; CSR `0x654` + the `0x800` per-stream window | ✅ fabric, silicon | `RTL` aaf, aaf_audio_loop, avtp_parser, avtp_rxmon, avtp_stream, tsn_fuzz `make aaf`; `BOARD` board↔board E2E, `thdn` (THD+N), `soak` |
| M-2 | AVTP CRF media clock reference | 1722 | **HW** engines · **❌** selection | `KL_crf_tx` / `KL_crf_rx` + `KL_mmcm_drp_servo` (CSR `0x738`-`0x74C`) | 🟡 the engines parse, count and report · ❌ **the CRF media clock can never be SELECTED**: AECP `SET_CLOCK_SOURCE` was the only writer of the live CLOCK_DOMAIN `clock_source_index`, which is now pinned at 0 (INTERNAL) for the life of the build, so `KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are **structurally off** and `A_MCSRV_STAT` (`0x8F8`) reads its idle · 🟡 **M-CLK-2** also still open | `RTL` crf_tx, crf_rx, mmcm_servo, mmcm_servo_autorepair, media_nco, hostplane, milan_dp; `BOARD` the pre-deletion servo lock at the converter floor is a **historical** measurement — it is not reachable from this build |
| M-3 | NxN talkers/listeners, format-adaptive listener | Milan | **HW** streams · **❌** adaptation | `N_STREAMS` talker/listener contexts (AX 8×8, Arty 4×4); per-stream binds and SRP rows now come from the protocol processor's class-D face | 🟡 the streams are fabric and silicon-proven · ❌ **format adaptation is gone with A-6** — nothing can `SET_STREAM_FORMAT` a listener, so a bound listener keeps its elaborated format | `RTL` aaf, csr (N=4/8 window), milan_dp nxn, pp_shadow; `BOARD` 8×8 E2E |
| M-4 | Media redundancy (1722.1 seamless) | Milan |  -  |  -  | ➖ out of scope | (explicitly excluded  -  see dependency matrix) |

## 7. Host / SoC / driver

| # | Feature | HW/SW | Module(s) | Status | Validating test(s) |
|---|---------|-------|-----------|--------|--------------------|
| H-1 | VexiiRiscv RV32IMA + sv32 MMU boot contract (RV64/sv39 and NaxRiscv historical) | HW | `milan_soc.py` (LiteX + VexiiRiscv), bound layout + DTB/OpenSBI preflight | ✅ | `BOARD` VexiiRiscv Linux lineage; `SW` exact RV32/sv32 DTB and embedded-OpenSBI FDT checks reject RV64/sv39; `SIM` litex_sim boot to `litex>` (evidence) |
| H-2 | CPU reaches milan_csr, reads ID="MILN" (M-A2) | HW | `milan_datapath` + LiteX bus | ✅ | `SIM` `milan_sim.py` mem_read (evidence log) |
| H-3 | `milan_datapath` §A.9 wrapper integrity | HW | `milan_datapath.sv` | ✅ | `RTL` milan_dp (11: ID + TX/RX byte-exact); `SYN` |
| H-4 | AXIS↔memory DMA, simple-mode CSRs (§A.6) | HW | `MilanDMA` (WishboneDMA ×3) | 🟩 | `ELAB` `--with-dma` (CSRs in csr.csv); `BOARD` loopback (M-A3) |
| H-5 | IRQ → PLIC (tx/rx/ts-dma + csr) | HW | `EventManager` → PLIC | 🟩 | `ELAB`; `BOARD` `/proc/interrupts` increments |
| H-6 | Full SoC assembly (NIC+DMA+MAC) | HW | `milan_soc.py --full` | 🟩 | `ELAB` gateware export (all instances present) |
| H-7 | Device portability (non-Xilinx) | HW | all `hdl/` | ✅ | `SYN` all tops incl. Lattice ECP5 (the [`syn/yosys/run.sh`](../../syn/yosys/run.sh) `tops` array is authoritative) |
| H-8 | Linux driver: NAPI/XDP/PTP/ethtool | SW | `kl-eth` (the retired driver record) | 🟡 ABI | `BOARD` bring-up (M-A5) |
| H-9 | Device tree `kl,dma-ether` | SW | the retired node include + binding | ✅ struct | `dtc` parse; `BOARD` driver binds |
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
  blocks, the MAC + GMII PHY, MAAP, the AAF talker/listener pair, the CRF
  engines, the §A.9 wrapper, the full SoC, the bitstream and the driver  -  rows
  tagged ✅. Note the AVDECC control plane is no longer in this bucket as a
  whole; it splits into the next two.
- **Moved to the protocol processor (2026-08-13):** ADP (A-1, A-2, A-4), ACMP
  talker and listener (A-7), SRP/MSRP/MVRP with its admission grant (R-2, R-3),
  and — with the uCPU landing — AECP (A-5). One wrapper,
  `hdl/milan/KL_pp_shadow.sv`, instantiated unconditionally by
  `hdl/milan/milan_datapath.sv`, publishing a class-D wire face the fabric
  consumes every clock. Verification lane: `tb/verilator/pp_shadow` plus the
  datapath suite — **neither of which grades the AECP engine yet.**
- **Implemented on AECP, and exactly this much (A-5):** `READ_DESCRIPTOR` and
  its three status paths; `IDENTIFY_NOTIFICATION`-as-command → `BAD_ARGUMENTS`;
  the conformant `NOT_IMPLEMENTED` echo, which is a *protocol-conformance*
  behaviour (IEEE 1722.1 §9.3.5's duty to respond) and not coverage of any
  command; the two silent-refusal rules. Descriptor enumeration is reachable
  **once the descriptor image is in DRAM.** The explicit builder/rootfs
  deployment handoff now supplies it; a flow that skips that transfer still
  answers `BAD_ARGUMENTS`,
  because the configuration range check runs before the locate and an invalid
  image reports `configurations_count` = 0. That makes the two error statuses a
  discriminator: `BAD_ARGUMENTS` everywhere means no image (or a corrupt one),
  while `NO_SUCH_DESCRIPTOR` means the image is loaded and that descriptor is
  genuinely not in the model. Known gap kept visible: Milan Δ7 `ACQUIRE_ENTITY`
  (`NOT_SUPPORTED`, `owner_id` = 0) is not distinguished from the generic echo.
- **NOT IMPLEMENTED — a well-formed refusal and no function:** every AEM getter
  and setter, the whole **MVU** family (A-8) and `GET_COUNTERS` (A-9), plus
  `SET/GET_STREAM_FORMAT` (A-6). Three consequences deserve naming rather than
  aggregating: **(i)** the CRF media clock can never be selected
  (`SET_CLOCK_SOURCE` is absent, `clock_source_index` pinned at INTERNAL, so the
  MMCM-DRP and packet-grid servos are structurally off); **(ii)** every Stream
  Output's presentation offset is pinned at the Milan **2 ms default** — a
  DEFAULT, not a zero, because 0 ns would be a presentation time in the past and
  every listener would drop every frame as late; **(iii)** the Milan Table 5.4
  **per-STREAM_OUTPUT** counters are live for solicited GET_COUNTERS reads, while
  the Table 5.22 unsolicited push has no producer. STREAM_INPUT counters remain
  live. Saved-state persistence is gone with the deleted journal:
  nothing restores a binding across a power cycle.
- **Proven in the open toolchain, not yet exercised on a board:** the mcast hash
  filter and the fixed-125 MHz PHC reference  -  rows tagged 🟩 (`ELAB`).
- **Genuinely open, per clause, not per subsystem:**
  CRF-as-a-reserved-class-A-stream (M-2, Milan 7.3.3 / `M-CLK-2`), SR class B
  provisioned but never declared (`SRP-8`), and the two gPTP riders on T-5
  (`AS-4` per-unit latency calibration, `AS-6` DUT-wins-BMCA, bench-blocked).
- **Out of scope (recorded, not built):** 802.1Qbv TAS, media redundancy  -  rows ➖.

There is no longer a "software protocols, planned" bucket. Per
[`ARCHITECTURE_HW_SW_SPLIT.md`](../ARCHITECTURE_HW_SW_SPLIT.md) rev 4,
product-default normal operation uses the fabric `gptp-processor` owner plus
the `kl-eth` driver, the PCM producer and a once-per-boot identity write.
`linuxptp` is confined to the explicit software-owner option-off comparison.
The full open-gap
ledger for the AECP boundary — every Milan v1.2 clause that lost its
implementation — is [`MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md).

**One decode trap this page cannot leave implicit.** The TX arbiter cascade
collapsed from EIGHT muxes to FOUR when the planes that fed four control merges
were deleted. `A_TXARB_DIAG` at `0x784` now reads, LSB first: **0 = `ctl_tx`
(protocol processor + MAAP → the control lane), 1 = `aaf_final`, 2 = `crf_dp`,
3 = `adp_tx` (the MAC boundary mux); bits 7:4 read a structural zero.** It was
0 aecp_acmp, 1 ctl_tx, 2 srp_ctl, 3 lstn_ctl, 4 maap_ctl, 5 aaf_final,
6 crf_dp, 7 adp_tx. Anything decoding `0x784` by the old numbers now reads the
WRONG mux.
