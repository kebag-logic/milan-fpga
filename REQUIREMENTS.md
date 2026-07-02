# TSN on FPGA — Requirements

## 1. Goal and scope

Turn the Milan FPGA design (Zynq-7020, custom 1 G RGMII MAC) into a **real,
software-configurable TSN network interface** that complies with the relevant
IEEE 802 standards and is driven by a Linux network driver:

* **IEEE 802.1Q** traffic classification and queuing (PCP → traffic class).
* **IEEE 802.1Qav** credit-based shaper (CBS) for the SR classes.
* **IEEE 802.1AS / IEEE 1588** gPTP hardware timestamping (**timestamp + a
  disciplinable clock**; transport/BMCA stay in software).
* **IEEE 802.3** MAC configuration and management so the block also behaves like
  a traditional MAC (station address, filters, speed/duplex, statistics),
  configurable over a **memory-mapped** register interface (and/or MDIO).

Software deliverables (sibling repos under `../`):

* A **Linux driver** (`../kl-linux-drivers`) implementing PTP/PHC + hardware
  timestamping, the traffic classifier config, the CBS config, and **N** hardware
  queues (as many as the HDL exposes).
* A **device-tree generator** integrated into `../fpga-ps-tools`, reusing the
  Xilinx `device-tree-xlnx` (dtg) and overlaying the TSN driver node.

> This document is the normative requirements spec. The concrete, ordered work
> items live in [`TODO.md`](TODO.md). The prior free-form brief is preserved in
> §9. The gap analysis backing every requirement is summarised in §3.

## 2. Reference standards

| Ref | Standard |
|-----|----------|
| 802.1Q | IEEE 802.1Q-2018/2022 — Bridges and Bridged Networks (classification, queuing, §8.6.8 CBS, §34 deltaBandwidth, clause 12 managed objects) |
| 802.1Qav | IEEE 802.1Qav (Forwarding and Queuing for Time-Sensitive Streams — CBS), folded into 802.1Q §8.6.8 |
| 802.1AS | IEEE 802.1AS-2020 — gPTP (timing and synchronization) |
| 1588 | IEEE 1588-2019 — Precision Time Protocol |
| 802.3 | IEEE 802.3-2022 — Ethernet MAC, Clause 22 (MDIO), Clause 28 (autoneg), Clause 30 (management), Clause 31 (PAUSE) |
| Linux | Kernel contracts: `net_device_ops`, `ptp_clock_info`, `ethtool_ops`, `ndo_setup_tc` (CBS/mqprio/taprio), phylib, `SIOCSHWTSTAMP` |

## 3. Missing elements to comply with the 802.1 configuration standards (gap analysis)

A structured, multi-domain audit of the current RTL/driver was performed (with
adversarial verification of the CBS arithmetic). **60 gaps** were identified.
The single root cause behind most blockers: **there is no memory-mapped
control/status-register (CSR) plane anywhere in the design** — every TSN knob is
a compile-time parameter or a tied constant, so nothing can be configured at
runtime, and the driver has nothing to bind to.

| Domain | Blockers | High | Med | Low | Headline finding |
|--------|:---:|:---:|:---:|:---:|------------------|
| Control plane / CSR | 3 | 3 | 2 | – | No AXI4-Lite CSR block exists; PS reaches only the two DMAs + DDR (`bd/milan-dma.tcl`). |
| gPTP / 1588 / PHC | 5 | 1 | 5 | 1 | Timestamp counter is a fixed free-running adder — no adjfine/adjtime/settime/gettime, no IRQ. |
| 802.1Q classification | 2 | 2 | 4 | 2 | PCP is decoded but **never used**; class is picked by EtherType; no PCP→TC table, no default priority. |
| 802.1Qav CBS | 1 | 4 | 4 | – | Math is dimensionally sound but all knobs compile-time; all queues credit-limited; SR idleSlope sums to 100 %. |
| 802.3 MAC / mgmt | 2 | 4 | 3 | 1 | MAC cfg tied constant (`cfg_ifg/tx_en/rx_en`, `is_1g`); no address filter; stats invisible to SW; no MAC IRQ. |
| Linux driver / DT | 8 | 3 | – | – | `kl-eth.c` is a non-compiling stub; no netdev datapath, PHC, MDIO, ethtool, tc-CBS, DT node, or dtg wiring. |

### CBS math verification (the flagged concern)

Each CBS correctness claim was independently checked from three lenses
(units / 802.1Qav conformance / RTL simulation) **and** with a new runnable
Verilator harness ([`tb/verilator/cbs`](tb/verilator/cbs)):

* **Confirmed real:** no runtime config; all queues credit-limited; SR idleSlope
  = 100 % of link (violates §34 deltaBandwidth ≤ 75 %); ~2-cycle credit/transmit
  pipeline skew; credit frozen during grant-with-backpressure; idle-per-cycle vs
  send-per-byte decoupled from real line occupancy; stale/non-self-checking TB.
* **Latent:** chained integer-division truncation in the slope terms — **zero
  error for today's evenly-divisible slopes** (the harness measures 0.0 bytes of
  quantization for the queue-0 config) but real once idleSlope is arbitrary/
  runtime-programmable.
* **Refuted (not a defect):** "hiCredit/loCredit wrong at 100 M." Because
  hiCredit/loCredit depend on the *ratio* idleSlope/portRate, which is preserved
  (500 M/1 G = 50 M/100 M = 0.5), the value 761 is correct at both rates.

## 4. Requirements (normative)

Keywords **MUST / SHOULD / MAY** per RFC 2119. Each item lists a standard ref
and the acceptance criterion. IDs are stable and referenced from `TODO.md`.

### 4.A Control plane — memory-mapped CSR (foundation)

* **REQ-CSR-01 (MUST)** The design MUST expose an **AXI4-Lite CSR slave** mapped
  into PS `M_AXI_GP0` (e.g. `0x43C0_0000`, 64 KB) carrying all TSN configuration
  and status. *(802.1Q clause 12; 802.3 Clause 30)* — *Accept:* driver `reg`
  region reads back an ID/version register.
* **REQ-CSR-02 (MUST)** The CSR block MUST provide read-only **ID / VERSION /
  CAPABILITIES** registers; CAPABILITIES MUST encode `NUMBER_OF_QUEUES` and
  feature bits (CBS, PTP, timestamp width) so the driver self-describes. —
  *Accept:* driver sizes its queue/CBS tables from CAPABILITIES.
* **REQ-CSR-03 (MUST)** CSR fields consumed in the `gtx_clk` (PTP/TX) domain MUST
  cross clock domains safely (multi-bit value + synchronized apply-strobe;
  single-bit via 2-FF). — *Accept:* CDC constraints + no metastability in review.
* **REQ-CSR-04 (MUST)** The CSR block MUST provide **IRQ_STATUS (W1C)** and
  **IRQ_MASK** registers and drive a PS interrupt line, aggregating: TX
  timestamp available, link/speed change, RMON counter rollover. — *Accept:*
  masked events raise IRQ_F2P and are cleared W1C.
* **REQ-CSR-05 (MUST)** The register map MUST be documented as a stable **ABI**
  (`docs/REGISTER_MAP.md`) shared by HDL, driver, and device tree.

### 4.B gPTP / IEEE 1588 hardware clock (PHC)

* **REQ-PTP-01 (MUST)** The timestamp counter MUST become a **register-controlled
  accumulator**: a SW-writable nominal increment with **fractional-ns** bits
  (phase accumulator) so frequency can be tuned. *(1588 §11.2; Linux `adjfine`)*
  — *Accept:* writing ±ppm changes the measured rate accordingly.
* **REQ-PTP-02 (MUST)** The clock MUST support **offset add/subtract (adjtime)**
  and **absolute set (settime)** via a load register + apply strobe. *(1588
  §7.2.1; Linux `adjtime`/`settime64`)* — *Accept:* PHC_SET then gettime returns
  the set value + elapsed.
* **REQ-PTP-03 (MUST)** The clock MUST support **snapshot-on-read (gettime)** —
  a read strobe latches the 64-bit TOD (ideally paired with the ARM global-timer
  for `gettimex64`). *(Linux `gettimex64`)* — *Accept:* two reads differ by the
  elapsed interval within jitter.
* **REQ-PTP-04 (MUST)** TX egress timestamp completion MUST be signalled to
  software (IRQ + status) and each metadata record MUST carry an unambiguous
  TX-to-skb key (messageType + seq_id, ideally a HW cookie). *(1588 two-step;
  Linux `skb_tstamp_tx`)* — *Accept:* driver matches every TX event frame to its
  timestamp with no aliasing under 2 in-flight event messages.
* **REQ-PTP-05 (SHOULD)** Only **event** PTP messages (Sync, Delay_Req,
  Pdelay_Req/Resp) SHOULD be timestamped; general messages SHOULD NOT consume
  the metadata FIFO. Parse `messageType[3:0]` (+ optional domain). *(1588 §7.3.4)*
* **REQ-PTP-06 (SHOULD)** The PHC SHOULD provide SW-programmable per-port
  **ingress/egress latency correction** registers; the capture point SHOULD be
  characterized against the GMII SFD. *(802.1AS §8.4/§11.3.2)* — the current
  AXIS-SOP capture has fixed, uncorrected asymmetric latency.
* **REQ-PTP-07 (SHOULD)** The PHC counter SHOULD be clocked from a **fixed
  125 MHz** free-running clock (not the speed-switched `gtx_clk`) so the ns rate
  is correct at 10/100/1000, or make the increment link-speed/`adjfine` driven.
* **REQ-PTP-08 (MAY)** Provide **1PPS output** / external timestamp capture /
  periodic output for PHC validation. *(Linux `n_ext_ts`/`n_per_out`/`pps`)*
* **REQ-PTP-09 (SHOULD)** Handle **C-VLAN-tagged gPTP**: detect 0x8100 and shift
  the PTP field offsets by the tag width (today offsets assume untagged).

### 4.C IEEE 802.1Qav credit-based shaper

* **REQ-CBS-01 (MUST)** Per-traffic-class **idleSlope, hiCredit, loCredit** MUST
  be runtime-writable via CSR (sendSlope derived), plus a **per-queue CBS
  enable**. *(802.1Q §8.6.8.2, §12.20, §34)* — *Accept:* `tc qdisc … cbs`
  parameters take effect without re-synthesis.
* **REQ-CBS-02 (MUST)** **Non-SR classes (best-effort, and gPTP/control unless
  explicitly shaped) MUST NOT be credit-limited** — they use strict priority
  (`allow_transmit` forced high). *(802.1Q §8.6.8)* — *Accept:* BE uses the full
  idle link when SR queues are empty.
* **REQ-CBS-03 (MUST)** Total configured SR idleSlope MUST be bounded by the
  **deltaBandwidth** limit (default ≤ 75 % of port rate). *(802.1Q §34.3)* —
  *Accept:* default config reserves ≤ 75 %; excess is rejected by the driver.
* **REQ-CBS-04 (SHOULD)** Credit MUST continue to **accrue at idleSlope while a
  queue is queued-and-blocked**, including *grant-with-backpressure* (not frozen).
  *(802.1Q §8.6.8.2)* — fixes `credit-frozen-during-backpressure`.
* **REQ-CBS-05 (SHOULD)** Credit accounting MUST track real transmission with
  minimal skew: collapse the double registration of `is_transmitting`/`bytes_sent`
  and make arbitration see non-stale `allow_transmit`. *(802.1Q §8.6.8.2)*
* **REQ-CBS-06 (SHOULD)** Slope fixed-point conversion SHOULD **round** (or use a
  combined divisor / wider fraction) so credit does not drift for arbitrary
  runtime idleSlope. *(precision)* — verified 0-error only for today's slopes.
* **REQ-CBS-07 (SHOULD)** The `m_axis` egress MUST be **paced to true line rate**
  (or line-occupancy time modelled) so idle accrual and send debit correspond to
  real occupancy; document the upstream pacing assumption. *(802.1Q §8.6.8.2)*
* **REQ-CBS-08 (MUST)** hiCredit/loCredit MUST track the **active port rate**
  (already correct today via the preserved idleSlope/portRate ratio — keep this
  invariant when values become runtime-writable). *(802.1Q §8.6.8.2)*

### 4.D IEEE 802.1Q classification and queuing

* **REQ-CLS-01 (MUST)** Classification MUST derive priority from the received
  **PCP** (`vlan_tci[15:13]`) for tagged frames, then map priority → traffic
  class via a **programmable PCP→TC table** (Table 8-5), replacing the
  EtherType-based decision. *(802.1Q §6.9.3, §8.6.6)* — *Accept:* two AVTP
  streams with different PCP land in different queues.
* **REQ-CLS-02 (MUST)** The PCP→TC map, priority-regeneration table, and TC→queue
  map MUST be **software-writable** via CSR. *(802.1Q clause 12)*
* **REQ-CLS-03 (MUST)** Untagged/priority-tagged frames MUST use a configurable
  **default port priority**, not a hardwired Best-Effort. *(802.1Q §6.9.3)*
* **REQ-CLS-04 (SHOULD)** The class→queue ordering MUST be configurable and its
  defaults MUST follow the standard (network-control/gPTP ranked per Table 8-5,
  not fixed below SR-A). *(802.1Q Table 8-5)*
* **REQ-CLS-05 (SHOULD)** Extract and propagate **DEI** (`vlan_tci[12]`) as
  sideband for policing/drop decisions. *(802.1Q §6.9.4)*
* **REQ-CLS-06 (SHOULD)** The classifier MUST parse frames **back-to-back at line
  rate** without requiring an inter-frame idle beat. *(802.3 min IFG)* — fixes the
  documented "one clock cycle delay" limitation.
* **REQ-CLS-07 (SHOULD)** gPTP/AVTP identification SHOULD validate the reserved
  **destination multicast** (01-80-C2-00-00-0E for gPTP), not trust EtherType
  alone. *(802.1AS §10.5)*
* **REQ-CLS-08 (MAY)** Recognize the configurable **S-TAG (0x88A8)** and stacked
  C/S-TAG (802.1ad). *(802.1Q §9.5)*
* **REQ-CLS-09 (MAY)** Per-stream filtering and policing (**802.1Qci**) —
  stream gates + flow meters — is future scope.

### 4.E IEEE 802.3 MAC configuration and management

* **REQ-MAC-01 (MUST)** MAC control (`IFG`, `TX_ENABLE`, `RX_ENABLE`,
  link-speed/`is_1g`, `stats_reset`) MUST be driven from CSR, not tied constants.
  *(802.3 §4.2, §30.3.1)* — *Accept:* interface up/down and IFG change from SW.
* **REQ-MAC-02 (MUST)** The RX path MUST provide a **station-MAC address filter**
  (exact-match unicast + multicast hash/CAM + promiscuous/allmulti) fed by CSR.
  *(802.3 §4.2.4.2.2; Linux `ndo_set_mac_address`/`ndo_set_rx_mode`)* — *Accept:*
  non-matching unicast is dropped in HW unless promiscuous.
* **REQ-MAC-03 (MUST)** The PHY autoneg result MUST configure the MAC speed/duplex
  and **link state MUST be reported** to SW (status bit + IRQ). *(802.3 Clause 28)*
* **REQ-MAC-04 (MUST)** MAC statistics (`ethernet_events`: tx/rx good/bad frame,
  FCS error, FIFO over/underflow) MUST be **readable via CSR** with a coherent
  **snapshot latch** and a `stats_reset` bit. *(802.3 Clause 30 / RMON;
  `ethtool -S`)* — replaces the ILA/VIO-only `mark_debug` regs.
* **REQ-MAC-05 (SHOULD)** MAC error/link events (RX overrun, TX underrun,
  bad-FCS, link change) SHOULD raise a **PS interrupt** (via REQ-CSR-04).
* **REQ-MAC-06 (SHOULD)** Provide a **software-controllable PHY reset** GPIO
  (EMIO) described as `phy-reset-gpios` in DT. *(802.3 §22.2.4.1.1)*
* **REQ-MAC-07 (MAY)** 802.3 **PAUSE** flow control and configurable **MTU/jumbo**.
  *(802.3 Clause 31; `ethtool -A`, `ndo_change_mtu`)*
* **REQ-MAC-08 (SHOULD)** PHY management (**MDIO**) MUST be reachable by the
  driver (PS GEM1 EMIO MDIO referenced by `phy-handle`, or a fabric MDIO master),
  bound to phylib. *(802.3 Clause 22)*

### 4.F Linux driver (`../kl-linux-drivers`)

* **REQ-DRV-01 (MUST)** Replace the non-compiling `kl-eth.c` stub with a coherent
  **platform driver** that compiles and registers a `net_device` with consistent
  `probe/remove/shutdown`. *(kernel netdev model)*
* **REQ-DRV-02 (MUST)** Implement the **datapath**: `ndo_open/stop/start_xmit`,
  DMA ring (dmaengine/`xilinx_dma` or custom), TX/RX **NAPI**, IRQ handlers.
* **REQ-DRV-03 (MUST)** Expose **N TX/RX queues** (`alloc_etherdev_mq` +
  `netif_set_real_num_tx/rx_queues`) mapped to the HW queues/shaper instances;
  requires multi-channel DMA (e.g. `axi_mcdma`) or a documented single-queue
  reduction. *(802.1Q TC-to-queue)*
* **REQ-DRV-04 (MUST)** Register a **PHC** (`ptp_clock_register` /
  `ptp_clock_info`: `adjfine/adjtime/gettime64/settime64/enable`) against the CSR
  PTP registers. *(1588; Linux PTP)*
* **REQ-DRV-05 (MUST)** Implement **hardware timestamping**: `ndo_eth_ioctl`
  (`SIOCSHWTSTAMP`/`SIOCGHWTSTAMP`), consume the ts-metadata S2MM stream,
  `skb_hwtstamps` on RX and `skb_tstamp_tx` on TX. *(Linux timestamping)*
* **REQ-DRV-06 (MUST)** Implement **CBS offload** via
  `ndo_setup_tc(TC_SETUP_QDISC_MQPRIO / TC_SETUP_QDISC_CBS)` translating
  `tc_cbs_qopt_offload` to shaper CSR writes; optional `TC_SETUP_QDISC_TAPRIO`.
  *(802.1Qav; Linux tc)*
* **REQ-DRV-07 (MUST)** Register the **MDIO bus** + **phylib** (`phy_connect`
  RGMII, `adjust_link` → MAC speed register), read `local-mac-address` from DT.
* **REQ-DRV-08 (MUST)** Provide **ethtool_ops**: `get_ts_info` (PHC index, caps,
  tx_types, rx_filters), `-S` stats/strings from CSR counters, coalescing; fix
  the broken ops table.

### 4.G Device tree and generator tooling (`../fpga-ps-tools`)

* **REQ-DT-01 (MUST)** Provide a **DT binding** (yaml) and a board `.dtsi` node:
  `compatible = "kl,dma-ether-0.9"`, `reg` = CSR + DMA regions, `interrupts` =
  tx/rx/ptp-ts/link, `kl,txq-cnt`/`kl,rxq-cnt`, `phy-handle` + `mdio` subnode,
  `local-mac-address`, `clocks`. *(Linux DT bindings)*
* **REQ-DT-02 (MUST)** Integrate the Xilinx **`device-tree-xlnx` (dtg)** into
  `fpga-ps-tools`: check out the submodule, run `xsct`/`hsi` against the
  `.xsa`/`.hwh` to emit the base `pl.dtsi`, then **overlay** the `kl,dma-ether`
  TSN node (dtg alone emits generic `xlnx,axi-dma`). *(REQUIREMENTS goal)*
* **REQ-DT-03 (SHOULD)** The generator SHOULD emit the CBS/TC-to-queue and PHC
  properties consistently with the CSR ABI (REQ-CSR-05).

### 4.H Verification

* **REQ-VER-01 (MUST — DONE)** A **self-checking, runnable CBS harness** MUST
  verify idle accrual→hiCredit, sendSlope→loCredit, empty reset-to-zero,
  negative-credit recovery, grant/backpressure, 1 G & 100 M, against a reference
  model. — *Done:* [`tb/verilator/cbs`](tb/verilator/cbs) (`make` → PASS, CI exit
  code). Supersedes the stale `tb/utests/.../tb_credit_based_shaper.sv`.
* **REQ-VER-02 (SHOULD)** A harness for **multi-queue arbitration**
  (`traffic_shaping_core`) — one-hot grant, hold-until-`tlast`, eligibility,
  priority, passthrough. *(approach proven; see TODO)*
* **REQ-VER-03 (SHOULD)** A **classifier** harness (PCP→TC table, VLAN offsets,
  default priority, back-to-back frames).
* **REQ-VER-04 (SHOULD)** A **CSR/register-map** testbench (reset values, W1C,
  RO/RW masks, CDC apply-strobe) checked against `docs/REGISTER_MAP.md`.
* **REQ-VER-05 (SHOULD)** Driver bring-up validation: `ethtool -T`, `phc2sys`/
  `ptp4l` lock, `tc qdisc … cbs offload`, `ethtool -S`.

## 5. Priority / phasing

The CSR plane (§4.A) is the **critical path** — it unblocks PTP, CBS, classifier,
MAC config, the driver, and the device tree. Ordered work items, dependencies,
effort, and status are in [`TODO.md`](TODO.md).

## 6. Out of scope (future work)

802.1Qbv/TAS (time-aware shaper) beyond a `taprio` hook; 802.1Qci PSFP; one-step
PTP / transparent clock; UDP/IPv4 PTP transport; 802.1ad provider bridging;
frame preemption (802.1Qbu/802.3br).

## 7. Traceability

Every requirement traces to a standard clause (above) and to a gap ID from the
§3 audit. The audit's full per-gap detail (current file:line, required behavior,
recommendation) is retained in the project analysis output and mirrored by the
`TODO.md` task descriptions.

## 8. Acceptance (end-to-end)

The interface is "done" when: (a) the driver binds via the generated DT and
brings the link up through phylib; (b) `ethtool -T` advertises the PHC and
`ptp4l`/`phc2sys` discipline the clock; (c) `tc qdisc … cbs offload 1` programs
the HW shaper and SR streams meet their reservation while BE uses the remainder;
(d) `ethtool -S` returns HW counters; (e) the CBS and CSR harnesses pass in CI.

## 9. Original brief (preserved)

> The goal is to create a TSN network interface that complies with 802.1Qav,
> gPTP (timestamp only) and traffic classification, and the 802.1 standard
> overall; adding configuration features to behave like a traditional MAC over
> MDIO or memory-mapped configuration. A Linux driver implementing PTP
> config/timestamping, traffic-classifier config, CBS config, and N hardware
> queues. A tool to generate the device-tree for the driver, reusing the Xilinx
> dtg inside `fpga-ps-tools`.
>
> **Status (original):** code in good shape but missing pieces to be usable as a
> NIC. gPTP tested but needs a Linux driver. CBS math is complex — needs a way to
> verify and run it. Memory-mapped configuration not done.
>
> **What was to do →** ① list the missing elements for 802.1 compliance → **done
> (§3)**; ② add standards-compliant requirements → **done (§4)**; ③ create
> `TODO.md` → **done**; ④ tackle the tasks → **in progress**. Delivered so far:
> the CBS verification harness (`tb/verilator/cbs`, REQ-VER-01), the CSR register
> ABI (`docs/REGISTER_MAP.md`, REQ-CSR-05), the AXI4-Lite control-plane RTL
> (`hdl/csr/milan_csr.sv`, REQ-CSR-01/02/04) — the previously-missing
> memory-mapped configuration — and its verification harness
> (`tb/verilator/csr`, REQ-VER-04). Remaining work is tracked in `TODO.md`
> (block-design integration, then PTP/CBS/classifier/MAC wiring, driver, DT).
