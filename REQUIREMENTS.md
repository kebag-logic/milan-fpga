# TSN/Milan FPGA requirements

This document is the normative product contract for VERSION `0x0002_0057`.
The supported product is an Artix-7 end station with RV32I bare-metal firmware,
a memory-mapped CSR plane at `0x9000_0000`, fabric protocol processing, and a
1-Gbit/s MAC datapath. Superseded platform briefs and campaign narratives are
kept in Git history rather than the tracked product tree (#259).

## Contents

- **[1. Product ownership](#1-product-ownership)** — Defines the one supported bare-metal target and its fabric/firmware responsibilities.
- **[2. Reference standards](#2-reference-standards)** — Names the IEEE, Milan and interface specifications that constrain the design.
- **[3. CSR plane](#3-csr-plane)** — Requires a stable, coherent AXI-Lite register ABI and explicit access semantics.
- **[4. Time synchronization and timestamping](#4-time-synchronization-and-timestamping)** — Assigns the PHC, gPTP publication and AVTP uncertainty contracts to fabric.
- **[5. Credit-based shaping](#5-credit-based-shaping)** — Specifies fixed-point CBS behavior, limits and runtime configuration.
- **[6. Classification and queues](#6-classification-and-queues)** — Defines class mapping, control traffic treatment and queue ordering.
- **[7. MAC and PHY management](#7-mac-and-phy-management)** — Covers frame integrity, filtering, link recovery and timestamp boundaries.
- **[8. Verification and release acceptance](#8-verification-and-release-acceptance)** — Sets the local, remote and exact-candidate evidence bar.
- **[9. Out of scope](#9-out-of-scope)** — Records deliberately unsupported profiles without creating alternate product paths.

## 1. Product ownership

- Bare-metal firmware owns boot policy, CSR initialization, identity,
  persistence orchestration, UART diagnostics, and remaining software-visible
  control.
- The fabric gPTP plane is the sole product PHC, protocol, servo, and public
  state owner.
- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image
  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;
  sync/asCapable are zero; `tu` is one; retained writes are inert.
- The fabric owns per-frame classification, reservation, shaping,
  timestamping, AVTP/AAF/CRF, MAAP, and IEEE 1722.1 processing.
- Required Milan state must survive power loss. The current blank-flash NVM
  face does not satisfy this requirement and is the release blocker in #70.

## 2. Reference standards

| Ref | Product use |
|---|---|
| IEEE 802.1Q-2018/2022 | classification, queuing, managed objects, and Section 34 bandwidth rules |
| IEEE 802.1Qav | credit-based shaping, folded into IEEE 802.1Q Section 8.6.8 |
| IEEE 802.1AS-2011 with Cor1/Cor2 | Milan v1.2 gPTP wire profile and state machines |
| IEEE 802.1AS-2020 | PHC/timestamp-assist semantics and traceability context |
| IEEE 1588-2019 | timestamp representation and PTP terminology |
| IEEE 802.3-2022 | MAC, MDIO, autonegotiation, counters, and PAUSE |
| IEEE 1722-2016 | AVTP/AAF/CRF transport and timestamp-validity fields |
| IEEE 1722.1-2021 | discovery, connection management, descriptors, commands, and counters |
| Milan v1.2 | PAAD-AE product profile and validation obligations |

The fabric gPTP transmitter follows the Milan-selected 802.1AS-2011 control
field values. Receivers ignore that deprecated field as required by the later
1588 edition.

## 3. CSR plane

- **REQ-CSR-01 (MUST):** One documented AXI4-Lite CSR plane exposes version,
  capabilities, interrupts, MAC, queues, PHC, protocol state, audio state, and
  diagnostics. Acceptance: [`docs/reference/REGISTER_MAP.md`](docs/reference/REGISTER_MAP.md) matches RTL decode
  and the CSR bench exercises every implemented group.
- **REQ-CSR-02 (MUST):** Multiword live values use an explicit snapshot or
  commit rule; no consumer may observe a torn identity, timestamp, path, or
  counter set.
- **REQ-CSR-03 (MUST):** Every clock-domain crossing uses a reviewed pulse,
  toggle, handshake, or asynchronous-FIFO contract and survives independent
  clock ratios and reset order.
- **REQ-CSR-04 (MUST):** Interrupt status is latched, maskable, readable, and
  clearable without losing a simultaneous event.
- **REQ-CSR-05 (MUST):** `ID`, `VERSION`, and `CAP` are read-only authorities;
  unsupported functionality is explicit rather than represented by a
  plausible zero.

## 4. Time synchronization and timestamping

- **REQ-PTP-01 (MUST):** The PHC supports enable, nominal increment, and
  signed rate adjustment in Q8.24 nanoseconds per datapath tick.
- **REQ-PTP-02 (MUST):** Absolute set, signed offset adjustment, and coherent
  snapshot reads cross into the PHC domain exactly once per command.
- **REQ-PTP-03 (MUST):** RX and TX event timestamps include direction,
  sequence ID, and message type and cannot be re-paired across frames.
- **REQ-PTP-04 (MUST):** Timestamp-ready events are observable through the CSR
  interrupt contract.
- **REQ-PTP-05 (MUST):** The fabric engine implements the Milan gPTP message
  set, best-master selection, peer delay, receipt timers, and PHC servo.
- **REQ-PTP-06 (MUST):** Ingress correction is subtracted and egress correction
  is added at the documented timestamp boundary. #64 owns physical measurement
  of the split.
- **REQ-PTP-07 (MUST):** GM, parent, PathTrace, peer delay, sync and asCapable
  publish atomically from the fabric bank to every CSR/protocol consumer.
- **REQ-PTP-08 (MUST):** AVTP `tu` asserts on loss of sync and on the same edge
  as a GM/sync discontinuity, remains asserted for the Milan holdover interval,
  and is never used to stop a licensed stream.
- **REQ-PTP-09 (MUST):** No write outside the fabric engine can manufacture
  live gPTP health. Option OFF remains ownerless under adversarial writes.

Scope note (VERSION `0x0002_0057`): the shipping datapath instantiates the PHC
(`timestamp_counter` + `ptp_csr_sync`) and the fabric engine's own ingress and
egress stamps. The `ptp_ts_top`/`ptp_ts_core` record path that carried
REQ-PTP-03, REQ-PTP-04 and REQ-PTP-06 in the retired product is no longer
instantiated: its records had no consumer once #259 removed the transmit path.
Those three requirements bind the record cores stand-alone (`ptp_ts` suite)
and are not product claims: `IRQ_STATUS[0]` is a structural zero and
`PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` are write-only scratch
([REGISTER_MAP.md](docs/reference/REGISTER_MAP.md)). Per-frame pairing and the
latency reference plane of the shipped gPTP path are the fabric engine's
(REQ-PTP-05) and #117's to measure.

Acceptance combines the focused PHC, timestamp, gPTP-plane, publication,
clock-validity, CSR, and full-datapath benches with #117's two-board wire and
publication correlation.

## 5. Credit-based shaping

Scope note (VERSION `0x0002_0057`): the 802.1Q classifier / queue / 802.1Qav
shaper chain (`traffic_controller_802_1q`) is verified stand-alone (the
`classifier`, `queues`, `cbs`, `shaper_core`, `datapath` and `controller_rate`
suites) and is **not instantiated in the shipping datapath**: its only packet
source was the transmit path retired by #259, and every product source (AAF,
CRF, MAAP, the protocol processor, fabric gPTP) joins the TX trunk after the
point it occupied. REQ-CBS-* and the queue rows of REQ-CLS-* therefore bind the
retained blocks, not the shipped wire behaviour; `CAP.CBS` reads 0 and the
`0x300`/`0x400` words are write-only scratch
([REGISTER_MAP.md](docs/reference/REGISTER_MAP.md)). Credit-shaping the
fabric's own class-A sources is a separate lane.

- **REQ-CBS-01 (MUST):** Each implemented shaped traffic class has independent
  idleSlope, sendSlope, hiCredit, loCredit, enable, and reset controls.
- **REQ-CBS-02 (MUST):** Credit accrues, freezes, transmits, and returns toward
  zero according to IEEE 802.1Qav, including downstream backpressure.
- **REQ-CBS-03 (MUST):** The sum of reserved idleSlope values does not exceed
  the configured link budget; invalid programming is refused or flagged.
- **REQ-CBS-04 (MUST):** Best-effort traffic receives the unreserved bandwidth
  and is not credit-limited at reset.
- **REQ-CBS-05 (MUST):** Queue priority and the configured SR class mapping are
  stable across every shipping shape.
- **REQ-CBS-06 (MUST):** Credit width and saturation prevent overflow at the
  supported line rates and frame sizes.
- **REQ-CBS-07 (SHOULD):** Configuration changes take effect at a documented
  safe boundary and expose their active values.
- **REQ-CBS-08 (MUST):** Focused arithmetic tests use an oracle independent of
  the RTL implementation and include mutation-sensitive backpressure cases.

## 6. Classification and queues

Scope note: see section 5 - the classifier and queue bank are retained,
verified blocks outside the shipping datapath; the station-address rules
(REQ-CLS-03) and the reserved-destination handling of fabric-originated traffic
(REQ-CLS-09/10) are implemented in `rx_mac_filter` and at the fabric merges.

- **REQ-CLS-01 (MUST):** VLAN PCP maps through a programmable PCP-to-traffic-
  class table.
- **REQ-CLS-02 (MUST):** Untagged traffic uses an explicit default class.
- **REQ-CLS-03 (MUST):** Station unicast, multicast, broadcast, and
  promiscuous/all-multicast controls have documented precedence.
- **REQ-CLS-04 (MUST):** Reserved protocol destinations are classified without
  relying on a VLAN tag.
- **REQ-CLS-05 (MUST):** Each frame's class sideband remains stable from the
  classification decision through end-of-frame.
- **REQ-CLS-06 (MUST):** Queue selection cannot change mid-frame under
  back-to-back traffic or downstream stalls.
- **REQ-CLS-07 (MUST):** Queue capacity, drops, and overflow conditions are
  observable and cannot silently wrap.
- **REQ-CLS-08 (SHOULD):** Runtime table updates are atomic from the frame's
  point of view.
- **REQ-CLS-09 (MUST):** Fabric-originated protocol traffic joins at the
  documented priority boundary and cannot be starved by bulk traffic.
- **REQ-CLS-10 (MUST):** Untagged gPTP and control PDUs are classified by
  destination address and EtherType where required; PCP is not invented for
  an untagged frame.

## 7. MAC and PHY management

- **REQ-MAC-01 (MUST):** IFG, TX/RX enable, link speed, and statistics reset
  are controlled through the CSR contract.
- **REQ-MAC-02 (MUST):** The RX path filters station unicast and programmable
  multicast traffic, with explicit diagnostic bypass controls.
- **REQ-MAC-03 (MUST):** Autonegotiated speed/duplex and link state reach the
  MAC and firmware-visible status/interrupt paths.
- **REQ-MAC-04 (MUST):** Good/bad frame, FCS, FIFO, and supported MAC events
  feed coherent counters; `STATS_CAP` distinguishes unsupported lanes from
  valid zero counts.
- **REQ-MAC-05 (SHOULD):** Link and error events raise maskable interrupts.
- **REQ-MAC-06 (SHOULD):** Bare-metal firmware can assert the PHY reset through
  the SoC GPIO/CSR contract.
- **REQ-MAC-07 (MAY):** PAUSE and jumbo-frame controls may be exposed when the
  selected MAC implements them.
- **REQ-MAC-08 (SHOULD):** Bare-metal firmware can access Clause-22 MDIO through
  a fabric management master.

## 8. Verification and release acceptance

- **REQ-VER-01 (MUST):** Focused Verilator suites cover CSR, PHC, timestamp,
  gPTP, shaping, classification, protocol, persistence, and audio behavior.
- **REQ-VER-02 (MUST):** The complete first-party RTL passes lint, elaboration,
  and the pinned Yosys portability gate on the exact candidate.
- **REQ-VER-03 (MUST):** Builder tests elaborate every shipping configuration,
  refuse unsupported product options, and bind generated firmware/AEM/gPTP
  images to the manifest.
- **REQ-VER-04 (MUST):** Documentation, generated artifacts, source lists,
  feature status, traceability, and the repository-wide bare-metal-only gate
  are green with zero policy findings.
- **REQ-VER-05 (MUST):** A booted shipping board demonstrates firmware startup,
  UART diagnostics, fabric-owned gPTP, persistent state, and audio operation.
  Two matched boards additionally demonstrate asCapable, GM transition/recovery,
  publication/`tu` correlation, conformance, and latency (#117).

Release acceptance requires all requirements above or an explicit standards-
cited deviation in the traceability table. At the current candidate, #70 and
#117 remain hard blockers; desk checks cannot substitute for their power-cycle
and physical measurements.

## 9. Out of scope

802.1Qbv time-aware scheduling, Qci per-stream filtering/policing, frame
preemption, one-step timestamping, routed PTP transport, stacked VLAN service
tags, and unrelated HDL modernization are not part of this release.
