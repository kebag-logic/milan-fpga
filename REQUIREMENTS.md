# TSN/Milan FPGA requirements

This document is the normative product contract for VERSION `0x0002_0060`.
The supported product is an Artix-7 end station with RV32I bare-metal firmware,
a memory-mapped CSR plane at `0x9000_0000`, fabric protocol processing, and a
1-Gbit/s MAC datapath. Superseded platform briefs and campaign narratives are
kept in Git history rather than the tracked product tree (#259).

## Contents

- **[1. Product ownership](#1-product-ownership)** -- Defines the one supported bare-metal target and its fabric/firmware responsibilities.
- **[2. Reference standards](#2-reference-standards)** -- Names the IEEE, Milan and interface specifications that constrain the design.
- **[3. CSR plane](#3-csr-plane)** -- Requires a stable, coherent AXI-Lite register ABI and explicit access semantics.
- **[4. Time synchronization and timestamping](#4-time-synchronization-and-timestamping)** -- Assigns the PHC, gPTP publication and AVTP uncertainty contracts to fabric.
- **[5. Credit-based shaping](#5-credit-based-shaping)** -- Specifies fixed-point CBS behavior, limits and runtime configuration.
- **[6. Classification and queues](#6-classification-and-queues)** -- Defines class mapping, control traffic treatment and queue ordering.
- **[7. MAC and PHY management](#7-mac-and-phy-management)** -- Covers frame integrity, filtering, link recovery and timestamp boundaries.
- **[8. Verification and release acceptance](#8-verification-and-release-acceptance)** -- Sets the local, remote and exact-candidate evidence bar.
- **[9. Out of scope](#9-out-of-scope)** -- Records deliberately unsupported profiles without creating alternate product paths.

## 1. Product ownership

- Bare-metal firmware owns boot policy, CSR initialization, identity,
  saved-state boot read/apply and write-back, and UART diagnostics.
- The control functions are ADP, ACMP, AECP, MAAP and SRP.
  AECP includes unsolicited notifications and counter serving.
- Until the switch-over, each MUST have build-selectable placement.
  The all-fabric build is the shipping default until then.
- The switch-over needs F2 to F5 suites and bench acceptance.
  Acceptance covers all streams, counters and audio soak.
- Requirement approval precedes the switch-over (#664, #665).
  Mark II then runs these functions as firmware only.
- After the switch-over, no all-fabric build remains (#665).
- Until F6, the fabric gPTP plane is the sole owner.
  It owns the product PHC, protocol, servo and public state.
- After F6, firmware owns the gPTP protocol and servo (#665).
  The PHC and timestamps stay in fabric, on both ports.
- `GPTP_PLANE_EN_P=0` is verification-only hardware. It has no product image
  and zero runtime gPTP owners: GM, parent, PathTrace and peer delay are zero;
  sync/asCapable are zero; `tu` is one; retained writes are inert.
- The fabric MUST retain framing, timestamps and the ingress filter.
  It MUST retain the AVTP/AAF/CRF and physical-media paths.
- Until F6, the fabric MUST also retain the gPTP plane.
- Audio deadlines MUST remain independent of firmware service.
  Until F6, gPTP deadlines MUST also remain independent of it.
- After F6, each gPTP path states and tests its firmware bound.
- Reservation protocol control follows its selected placement.
  Media admission enforcement and any shaping remain in fabric.
  The mailbox ingress filter MUST enforce the acceptance rules below.
  Tagged frames MUST NOT reach any mailbox.
  Each channel MUST match its full tuple, then its identity term.
  Own unicast means the receiving AVB interface's MAC only.
  AECP MUST accept own-target commands or own-controller responses.
  Untagged control frames failing their tuple MUST increment `FILTER_MISMATCH`.
  Per-channel token buckets MUST remain in force.
- Each selected function MUST have exactly one authoritative state owner.
- Until the switch-over, both placements MUST preserve wire behavior.
  They MUST also preserve ordering and normative timeouts.
- Firmware service MUST satisfy NFR-SCOUT-03 and its path-specific hooks
  in the [requirements register](docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing).
- Required Milan state must survive power loss.
  The shipping backend is partial; #70 remains a release blocker.
  F1 supplies the split store without integrating a shipping image.
  Its [boot contract](sw/firmware/ctrl_nvm/README.md#boot) governs validation and apply.

**Mailbox ingress acceptance (NFR-SCOUT-08).**
The [owner filter decision](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014311316)
requires this exact channel table.
Each row matches VLAN tag, destination MAC, EtherType and subtype.
The `maap` own-unicast destination also matches message_type MAAP_DEFEND.
The identity term then restricts which matching frames are delivered.
All rows require untagged frames; tagged frames retain the fabric path.
AAF/CRF media use the SR class VLAN and have no mailbox channel.
Stray untagged AAF/CRF frames therefore cannot reach the core either.

| Channel | VLAN tag | Destination MAC | EtherType | AVTP subtype | Identity term |
|---|---|---|---|---|---|
| `adp` | absent | `91:E0:F0:01:00:00` | `0x22F0` | `0xFA` | ENTITY_DISCOVER for entity_id 0 or own; F3 adds bound talkers' ENTITY_AVAILABLE/ENTITY_DEPARTING |
| `acmp` | absent | `91:E0:F0:01:00:00`; own unicast as a receive tolerance | `0x22F0` | `0xFC` | talker_entity_id or listener_entity_id = own |
| `aecp` | absent | own unicast MAC on the receiving AVB interface | `0x22F0` | `0xFB` | (command AND target_entity_id = own) OR (response AND controller_entity_id = own) |
| `maap` | absent | `91:E0:F0:00:FF:00`; own unicast on the receiving AVB interface for MAAP_DEFEND only | `0x22F0` | `0xFE` | overlaps own range |
| `srp` MSRP | absent | `01:80:C2:00:00:0E` | `0x22EA` | not applicable | all |
| `srp` MVRP | absent | `01:80:C2:00:00:21` | `0x88F5` | not applicable | all |

A frame failing its tuple or identity term MUST be dropped.
A different unicast destination MUST NOT reach the core.
The record's interface index selects the own-MAC comparison.
This preserves the future redundancy seam without enabling that feature.
Control EtherTypes here are `0x22F0`, `0x22EA` and `0x88F5`.
An untagged frame with one failing its tuple increments `FILTER_MISMATCH`.
Tagged frames stay outside this counter's untagged-control definition.

IEEE 802.1Q-2018 Table 10-1 assigns the Customer Bridge MVRP address.
IEEE 1722.1-2021 8.2.1 requires multicast transmission of all ACMPDUs.
Table B.1 assigns that multicast address.
Own-unicast ACMP reception is the owner's tolerance, not normative transmission.
Milan v1.2 5.4.5.3 requires the CONTROLLER_AVAILABLE liveness exchange.
Its response must pass the own-controller AECP term.
IEEE 1722-2016 B.2.1 sends MAAP_PROBE and MAAP_ANNOUNCE to the MAAP multicast address.
It sends MAAP_DEFEND to the source MAC of the triggering MAAP_PROBE.
A MAAP_DEFEND answering this entity's probe therefore arrives as own unicast.
A MAAP_PROBE or MAAP_ANNOUNCE to own unicast fails its tuple.

[The filter requirement](docs/reference/FR_NFR.md#34-fabric-scale-out-and-future-ports)
traces this table to the mailbox YAML and acceptance hooks.
PR #685 (#665 lane FC) implements this table, before F2 to F5.
The [mailbox design](docs/design/MAILBOX_SPLIT.md#the-ingress-filter) describes the implemented filter.

Until the switch-over, the [split architecture](docs/ARCHITECTURE_HW_SW_SPLIT.md) defines both placements.

Major `0x0003` identifies only images running the split.
The major changes with the default-flip implementation, not this document change.
MINOR remains flat and continuous across majors.
The [landing plan](docs/ARCHITECTURE_HW_SW_SPLIT.md#7-version-and-default-flip) pins the simulations and firmware string.
The current VERSION remains `0x0002_0060`.

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
| Milan v1.2 | non-redundant PAAD-AE product profile (Section 9) and validation obligations |

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

Until F6, the fabric plane owns this section's gPTP duties.
After F6, firmware owns the gPTP protocol and servo (#665).

The PHC and timestamps stay in fabric, on both ports.

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
  is added at the documented timestamp boundary. The fabric gPTP plane is the
  sole owner: the two corrections are per-board elaboration constants declared
  in the end-station configuration and applied inside `KL_gptp_shadow`, and
  the applied pair is published read-only at `GPTP_LAT` (`0x7F0`). The legacy
  `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` words are NOT that control and must not
  become it, so no correction can be applied twice. A board whose plane is on
  and whose configuration omits either key is refused. #64 owns physical
  measurement of the split; the sum is measured per board.
- **REQ-PTP-07 (MUST):** GM, parent, PathTrace, peer delay, sync and asCapable
  publish atomically from the fabric bank to every CSR/protocol consumer.
- **REQ-PTP-08 (MUST):** AVTP `tu` asserts on loss of sync and on the same edge
  as a GM/sync discontinuity, remains asserted for the Milan holdover interval,
  and is never used to stop a licensed stream.
- **REQ-PTP-09 (MUST):** No write outside the fabric engine can manufacture
  live gPTP health. Option OFF remains ownerless under adversarial writes.

Scope note (VERSION `0x0002_0060`): the shipping datapath instantiates the PHC
(`timestamp_counter` + `ptp_csr_sync`) and the fabric engine's own ingress and
egress stamps. The `ptp_ts_top`/`ptp_ts_core` record path that carried
REQ-PTP-03, REQ-PTP-04 and REQ-PTP-06 in the retired product is no longer
instantiated: its records had no consumer once #259 removed the transmit path.
REQ-PTP-03 and REQ-PTP-04 bind the record cores stand-alone (`ptp_ts` suite)
and are not product claims: `IRQ_STATUS[0]` is a structural zero. REQ-PTP-06
IS a product claim again at this VERSION, but its owner is the fabric plane
and not those cores, so `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` remain readable,
inert scratch (plain RW, the last written value returned, no
timestamp-correction consumer; the live publication is `GPTP_LAT` at `0x7F0`,
[REGISTER_MAP.md](docs/reference/REGISTER_MAP.md)). Per-frame pairing and the
latency reference plane of the shipped gPTP path are the fabric engine's
(REQ-PTP-05) and #117's to measure.

Scope note (egress reference plane, #360): the egress timestamp is the
frame's LAUNCH, observed by `KL_gptp_gmii_launch` at the MAC's own transmit
stream one register stage before the pads, reported back as one ordered
record per frame, and reconstructed by `KL_gptp_txret` as the PHC at that
record minus a sum of register stages (426 ns at the shipping shape). It is
NOT a capture at the MAC boundary and NOT a queue allowance: the
store-and-forward wait sits between the ledger entry and the launch, outside
the reconstructed interval. A frame whose launch cannot be reconstructed is
published as an explicit loss at `GPTP_DROPE[31:16]`, never as a substitute
time. The DIGITAL bound is verified in `tb/verilator/gptp_txts` against an
independent pad oracle over the product's own converted MAC; the remaining
offset from that register stage to the pad, and every physical term with it,
is #117's and #64's to measure.

Scope note (propagation asymmetry, #511): the product does not model IEEE
802.1AS-2011 `delayAsymmetry`. Section 8.3 does not require it to be measured,
and Section 10.2.4.8 makes an unmodelled value zero, so the value is zero here.
The product has one cabled port, and the two REQ-PTP-06 elaboration constants
remain its only timestamp corrections. No configuration key, CSR or runtime path
sets an asymmetry. The gPTP processor's live UART tuner stays a donor-bench
instrument and never becomes a product control. A one-way error left by the
assigned ingress/egress split (#64, #488) is corrected by re-measuring those
constants, never by a second asymmetry term. This is a directed limitation
recorded by the
[owner decision on #511](https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5789766257)
(2026-09-23). Revisit it before a profile adds a second cabled port, such as
Section 8 redundancy under #394, and before the product claims IEEE 802.1AS
management: 802.1AS-2011 Table 14-6 then requires a read-write
`delayAsymmetry` object on each time-aware IEEE 802.3 full-duplex port
(conformance `Tdot3FD`). A runtime correction, including a write to that
object, first needs an amendment of REQ-PTP-06. The
[gPTP plane record](docs/design/GPTP_PLANE.md#propagation-asymmetry-is-not-modelled)
lists what an adoption must define and prove.

Acceptance combines the focused PHC, timestamp, gPTP-plane, publication,
clock-validity, CSR, and full-datapath benches with #117's wire and
publication correlation of the one AX7101 DUT against the Milan-validated
reference peer.

## 5. Credit-based shaping

Scope note (VERSION `0x0002_0060`): the 802.1Q classifier / queue / 802.1Qav
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
  UART diagnostics, gPTP, persistent state, and audio operation.
  Until F6, that gPTP is fabric-owned.

  The one AX7101 DUT against the Milan-validated reference peer additionally
  demonstrates asCapable, GM transition/recovery, publication/`tu` correlation,
  conformance, and latency (#117).
- **REQ-VER-06 (MUST):** Each shipping candidate passes both release campaigns.
  The [owner decisions of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465) set their values.
  The soak lasts at least 24 continuous hours.
  Streams remain bound in both directions with the reference peer.
  CRF participates alongside AAF.
  Every declared stream index receives periodic counter observations.
  The sampling interval must not exceed 60 seconds.
  Counter authority: Milan v1.2 5.3.7.7/5.3.8.10, Tables 5.4/5.6.
  `SEQ_NUM_MISMATCH` and `STREAM_INTERRUPTED` must never increase.
  `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` must never increase either.
  These hold on every Stream Input, CRF included.
  Sequence authority: IEEE 1722-2016 4.4.4.6.
  `MEDIA_UNLOCKED` must not increase outside a recorded planted event.
  That holds whatever the cause, explained or not.
  An increment is excused only between two reads inside its input's planted window.
  Each planted event excuses at most one increment per input.
  Any counter decrease is a reset and fails the soak.
  `check_release_soak_counters` grades these counter rules.
  No `asCapable` loss is permitted.
  `asCapable` authority: Milan v1.2 4.2.6.2.4.
  Every `mr` toggle requires a recorded media-clock cause.
  Allowed causes: clock-source change, CRF disruption, or CRF `mr` toggle.
  CRF causes apply only to streams deriving timestamps from it.
  GM change alone never excuses an `mr` toggle.
  Match each cause within the recorded relative timestamp resolution.
  Each cause excuses at most one toggle per stream.
  Its two-sided window must be shorter than one second.
  Thus require resolution below half the counter-update ceiling.
  Coarser resolution yields NOT RUN.
  Every toggle holds for at least eight AVTPDUs of its stream.
  Every MEDIA_RESET increment requires a distinct, cause-correlated wire toggle.
  Multiple toggles can share one device observation interval.
  Counter updates may lag toggles by at most one second.
  Authority: IEEE 1722-2016 4.4.4.3; Milan Tables 5.4/5.6, Annex B.1.2.
  Retain timestamped source events, packet indices, and counter reads.
  Captures span the counter window, including delayed updates.
  A MEDIA_RESET decrease is a reset, requiring counter-walk investigation.
  Missing evidence for these checks is NOT RUN.
  The [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355) excludes PHC-only re-bases as `mr` causes.
  A PHC-only re-base leaves `mr` unchanged.
  The existing `tu` path signals that gPTP discontinuity.
  It adds no step-only MEDIA_RESET increment.
  Each `tu` interval contains at least one recorded discontinuity.
  Containment uses `[observed_start - observation_resolution_s, clear)`.
  The observed start is the first captured `tu=1` packet.
  Its first discontinuity must occur within resolution of that rise.
  Accepted kinds include GM-identity and GM time-source changes.
  Other detected gPTP discontinuities include PHC settime/adjtime and fabric discontinuities.
  Measure from the last recorded discontinuity before `tu` clears.
  It clears within 0.5 seconds plus stated observation resolution.
  Any `tu` without a recorded discontinuity fails.
  Resolution comes from wire capture and correlated event timestamps.
  It includes launch-to-capture latency and event-to-capture correlation error.
  Periodic counter-read cadence cannot supply that resolution.
  The [round-4 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855792297) defines this anchor.
  The [round-5 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5856062292) defines start-edge containment.
  Uncertainty authority: IEEE 1722-2016 4.4.4.7; Milan Annex B.1/B.1.1.
  After every GM change, `tu` remains set for 0.25 seconds.
  The project treats that duration as a minimum.
  Require `clear + observation_resolution_s >= last_GM_change + 0.25`.
  Grade every GM change against the complete interval history.
  A GM change without a covering interval fails.
  Record GM history separately; missing history is NOT RUN.
  Let R be the recorded relative event/capture error bound.
  True hold d is observed as h within `d +/- R`.
  The minimum accepts `h + R >= 0.25 s`.
  Consequently, a PASS guarantees only `d >= 0.25 s - 2R`.
  Require `2R < 0.25 s` so an instant clear fails.
  Thus `resolution_limit_s` is 0.125 seconds, with equality refused.
  The upper check requires `h + R <= 0.5 s + R`.
  Equivalently, require `h <= 0.5 s`, guaranteeing `d <= 0.5 s + R`.
  No additional resolution ceiling applies.
  Coarser resolution yields NOT RUN, even with no intervals.
  Resolution appears in every timing verdict.
  The [corrected decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857765949) governs these `mr`/`tu` checks.
  Clock validity implements 0.25-0.5 seconds of discontinuity holdover.
  B.1's five-second media-clock holdover never bounds `tu`.
  Observe gPTP publication, `AVTPRX_TSD` margin, and monotonic uptime.
  An audio-integrity run rides inside the same 24-hour soak window.
  Its [signal design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444) is a bit-exact sample counter.
  The counter never repeats within a run; its period is 2^43 samples.
  That is about 530 days at 192 kHz, the highest Milan v1.2 6.2 (Table 6.1) rate.
  Every channel of every bound AAF stream carries it, in both directions.
  The paths are the DUT talker to the reference peer to an external digital capture.
  They include the reference peer to the DUT listener and its TDM output.
  They include the DUT's TDM loop too.
  Every capture meets one property: a capture with a DUT event the bytes show never grades PASS.
  Each such event is covered, on each channel it changes, by at least one listing.
  A listing covers it when the listing's samples overlap the event's first word minus 63 to its last word plus 63.
  A listing's samples are its words, and for a slip the samples `located_within` names as well.
  A DUT event inside a constant-mask excursion on the same channel may be covered by that excursion's listing alone.
  The exception is an event that masks a planted arm at its sample; the run is then void, and its reason names that cause.
  A seeded fuzz over compositions of DUT events and planted arms is the gate for this property.
  Exact classification is claimed only inside a stated scope, which TESTING 6d lists.
  The scope is one event at a time, away from the planted arms, and the compositions the self-test sweeps grade.
  Inside it, each discontinuity is classified at its sample, and every slip is sized exactly.
  Each listing there begins within 63 samples of the event's first word.
  Outside it, the property promises coverage, not position.
  The classes are n dropped, n repeated, n samples of silence, a bit-flip mask and a channel swap.
  Only a reciprocal exchange is a swap; a corrupted or copied channel number is a bit-flip.
  A channel swapped from the first frame fails as a swap, its counter still tracked.
  An excursion that returns to its track under one XOR mask is one bit-flip, at any length.
  That holds unless the mask clears its channel number, which is outside the scope.
  On every channel, the reported slips sum to the shift the bytes decode.
  A window no reading balances is one unresolved event, never an unbalanced slip.
  Outside the scope, a composition may read in other classes, or void the run.
  Two examples are a DUT event over or beside a planted arm and a multi-word excursion beside other events.
  Where the bytes allow two readings, the planted-arm log decides at a logged arm, never at the cost of another DUT event.
  Patterns the signal cannot tell apart follow the rules and limits of [TESTING.md 6d](docs/testing/TESTING.md#6d-unattended-campaign-vehicle).
  A slip of whole blocks shows only within 63 samples, so each verdict states its qualified interval.
  It runs from 63 samples after the last channel's acquisition to 63 samples before the capture's end.
  Nothing outside it is proved clean.
  At either end, a stretch that differs from its track only in the code bit is one unresolved event.
  It may be a slip of whole blocks or a code-bit corruption, so it never claims an exact class.
  The source plants a drop, a repeat and a bit flip at both ends of the run.
  Both ends are the first and the last tenth of the capture, inside the qualified interval.
  A missed planted arm voids the run.
  Capture-side losses are logged by the capture tool and reported apart.
  A loss still advances the acquisition index and both clocks.
  It is not observed time, so it never counts toward the qualified interval.
  Each event records wall and gPTP times, capture index, words and class.
  Its times are interpolated between the capture tool's anchors, never invented.
  Counter, `SLIP_*` and gPTP walks bracket each event.
  The run passes with zero DUT-attributed events on every bound channel.
  Its qualified interval must also hold at least 24 hours of observed samples.
  So each capture runs past the 24 hours at both ends.
  `grade_audio_counter_capture` grades the counter captures.
  A sine pair, 997 Hz and 9,973 Hz, crosses the analog path.
  THD+N and the sample-exact predictor residual grade it.
  Their limits are not yet decided, so that check is NOT RUN until set.
  The power campaign completes 200 unattended cycles.
  150 are cold cuts from the power strip: 100 idle, 50 inside journal commits.
  50 are soft resets with power held on.
  A soft reset never counts as a cold cut, nor a cut as a reset.
  Soft-reset authority: Milan v1.2 5.5.1.4, "a power cycle or a simple reset".
  Every cycle restores the eight Milan items of #70's inventory and the binding.
  Each item is set away from its default before the cycle.
  A restore that writes nothing then reads back as a failure.
  Binding authority: Milan v1.2 5.3.8.2/5.3.8.3/5.3.8.7.
  The plan receives that inventory as data.
  Remaining authority: Milan v1.2 5.3.5.1, 5.3.7.1/5.3.7.6,
  5.3.8.1, 5.3.9.1, 5.3.10.1, 5.3.11.1, and 5.3.13.
  The current configuration is #70's item 1.
  Milan v1.2 states no separate non-volatile clause for it.
  Any additional declared state follows the project persistence inventory.
  Commit cuts recover complete old or new committed snapshots.
  Every pending value is set away from its default too.
  The cut instant must lie inside the recorded commit window.
  A cut outside it hit no journal commit and cannot count.
  `check_release_state_restored` grades every cycle's readback.
  T0 is the host-timestamped power-strip ON command.
  For a soft reset, T0 is the host-timestamped reset command.
  Record `power_off_hold_s`, default eight seconds, and verify discharge.
  Its default follows the `phys.dut-cycle.power-cycle` contract.
  Capture the last pre-cut `ENTITY_AVAILABLE`, including its timestamp.
  Decode its `valid_time` in two-second units.
  Milan 5.6.2 requires `valid_time=10`, giving twenty seconds.
  The first post-cut advertisement must arrive before T0 plus twenty seconds.
  Boot therefore counts against that entire window.
  Power-off hold and pre-cut advertisement age do not count.
  Retain them as provenance rather than subtracting them.
  Missing capture, invalid `valid_time`, or deadline expiry fails.
  ADP authority: IEEE 1722.1-2021 6.2.2.5 and 6.2.4/6.2.5;
  Milan v1.2 5.6.2/5.6.3 defines its values and advertiser.
  Restoration is automatic; controller repair cannot satisfy it.
  Each persisted binding must resume valid AVTP within `restore_bound_s`.
  Measure from T0, including both directions and CRF.
  The bound is provisionally 30 seconds; overruns fail.
  `RELEASE_RESTORE_BOUND_S = 30` is the release eligibility ceiling.
  Larger `restore_bound_s` values make a plan ineligible.
  Tighter bounds remain eligible when other prerequisites hold.
  The manager ratifies it using #397 and #75 measurements.
  These measure boot-to-entity-enabled and restart latency, respectively.
  Auto Connect authority: Milan v1.2 5.5.1.4/5.5.2.6.
  After restoration succeeds, run #75's additional controller reconnect check.
  Measure successful `CONNECT_RX` to first valid AVTP.
  That interval must remain below one second.
  Controller Bind authority: Milan v1.2 5.5.2.4.
  Observe boot for `restore_bound_s + boot_margin_s` from T0.
  The margin defaults to five seconds, without relaxing deadlines.
  Require one BIOS pass and no additional restart.
  Continue observation until the next cut or campaign end.
  These timing rules follow the
  [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5855515133).
  Release planning requires explicit topology and the complete nine-item inventory.
  Both campaigns use one DUT and the reference peer.
  Negative controls prove the gate can fail.
  The #366 first-boot restart fails the single-boot check.
  A persistence-disabled build fails the state restore.
  A planted audio drop fails the audio run, classified exactly.
  Retain exact-image evidence under [TESTING.md 6b](docs/testing/TESTING.md#6b-bench-evidence-retention).
  Execute the plan contract in [TESTING.md 6d](docs/testing/TESTING.md#6d-unattended-campaign-vehicle).
  Missing measurements and desk-only passes cannot qualify a release.

Release acceptance requires all requirements above or an explicit standards-
cited deviation in the traceability table. At the current candidate, #70 and
#117 remain hard blockers; desk checks cannot substitute for their power-cycle
and physical measurements. REQ-VER-05 also requires REQ-VER-06 campaign evidence:
the 24-hour soak with its audio-integrity run and the 200-cycle power campaign.
Issue #396's physical campaigns and negative controls remain open.

## 9. Out of scope

802.1Qbv time-aware scheduling, Qci per-stream filtering/policing, frame
preemption, one-step timestamping, routed PTP transport, stacked VLAN service
tags, and unrelated HDL modernization are not part of this release.

The exclusions below are directed limitations, each with its revisit trigger.
They are recorded decisions, not omissions.

- **Milan v1.2 Section 8 seamless network redundancy.** The product is a
  declared non-redundant end station: one AVB_INTERFACE on one cabled port,
  and `GET_MILAN_INFO` reports the `features_flags` REDUNDANCY bit as 0 (Milan
  v1.2 Section 5.4.4.1, Table 5.20). Milan v1.2 Sections 4.2.5 and 8.1 make
  redundancy optional. It is out of scope for the October release by the
  [owner decision on #394](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5789765478)
  (2026-09-23) and is revisited with the P4/P5 PCB (#416/#417). Adopting it
  needs a second AVB_INTERFACE with its own MAC, gPTP port, MAAP and SRP
  contexts and paired streams, and that design is approved before any RTL
  lane opens.
- **IEEE 802.1AS-2011 `delayAsymmetry` modelling.** Not modelled, so its value
  is zero (Sections 8.3 and 10.2.4.8), and the gPTP processor's live UART
  tuner stays donor-bench-only. See the Section 4 scope note and the
  [owner decision on #511](https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5789766257)
  (2026-09-23).
