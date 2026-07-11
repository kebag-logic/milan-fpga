# Milan v1.2 → FR/NFR dependency matrix

This matrix traces each **AVnu Milan v1.2** requirement to the
[functional/non-functional requirements](FR_NFR.md) it drives, states **why the
Milan requirement makes that FR/NFR necessary**, and gives the **verification /
test** that proves it.

Read the pair `FR_NFR.md` ⇄ this file: `FR_NFR.md` says *what* the system must do
(+ the `Ver` method letter); this file says *why Milan v1.2 forces it* and *how it
is verified*, and which requirements are **not** Milan-driven.

## How to read  -  dependency types

| Type | Meaning |
|------|---------|
| **MANDATES** | Milan v1.2 **requires** this behavior. Omitting the FR/NFR ⇒ **non-conformant**. |
| **CONSTRAINS** | Milan does **not** require the feature, but *if built* it must respect a Milan invariant. |
| **ENABLES** | A Milan capability a project NFR leverages (informational). |

## Verification method letters (as in `FR_NFR.md`)
**T** = test/interop · **A** = analysis · **D** = demonstration · **I** = inspection.

## Verification artifacts (tokens used in the *Verify* column)

| Token | Artifact | Location |
|-------|----------|----------|
| `avdecc_l2` | ADP watch / GET_COUNTERS / ACMP connect script | `srcs/milan-tests-avb/controller/avdecc_l2.py` |
| `tap_acmp` / `tap_sniff` | ACMP + frame taps | `srcs/milan-tests-avb/controller/` |
| `thdn` | audio THD+N quality check | `.../controller/pipewire_avb_thdn.py` |
| `soak` | pw1↔pw0 stream + clock-recovery soak | `srcs/milan-tests-avb/scripts/pw1-pw0-clockrec-soak.sh` |
| `latency.md` / `gptp-phc-clock.md` | measurement methodology | `srcs/milan-tests-avb/docs/` |
| `tsn-gen` | byte-exact AECP PDU specs + BDD features | `software-defined-tsn-stack/.../1722_1/aecp/*.yaml`, `.../tests/aecp_behave/features/*.feature`, `protocols/milan/aecp_read_descriptor.yaml` |
| `vtb:<n>` | Verilator self-checking harness | `tb/verilator/<n>` (`cbs`, `shaper_core`, `cls`, `ptp`, `ptp_sync`, `csr`; **`adp` = to add**, migration plan §B.2) |
| `Hive` | AVDECC controller (enumerate/lock/connect/identify) | external |
| `ptp4l`/`phc2sys`, `ethtool`, `tc cbs` | linuxptp + Linux net tooling | on-target |
| `mrpd` / `maap` | OpenAvnu MSRP/MVRP + MAAP daemons | on-target |
| `AVnu` | AVnu **Milan test plan** (conformance) | external |

> Clause numbers for AEM (§5.3.3.x) and MVU (§5.4.3.2) are evidence-backed; other
> Milan clause numbers are by **topic**  -  verify against the Milan v1.2 PDF.

---

## A. Discovery  -  ADP  *(Milan v1.2 Discovery; IEEE 1722.1-2021 §6)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| Periodic `ENTITY_AVAILABLE`, `available_index` monotonic per state change | MANDATES | FR-DISC-01, FR-DISC-04 | No advertise / wrong index ⇒ device invisible or controllers act on **stale** models. | T  -  `avdecc_l2 listen`; `vtb:adp` (ADPDU bytes, re-advertise timing, index increment); `AVnu` |
| Answer `ENTITY_DISCOVER` (global + targeted) | MANDATES | FR-DISC-02 | Controllers probe; ignoring DISCOVER ⇒ can't be brought online on demand. | T  -  `Hive` discover; `avdecc_l2 listen`; `vtb:adp` |
| `ENTITY_DEPARTING` on shutdown/link-down | MANDATES | FR-DISC-03 | Otherwise controllers keep dead entities/connections. | T  -  `avdecc_l2 listen` + `tap_sniff` (observe departing on link down) |
| Stable EUI-64 `entity_id` (MAC-derived) | MANDATES | FR-DISC-05 | Fast-connect keys on a stable id; a changing id breaks reconnection. | A,T  -  inspect derivation; power-cycle, confirm id unchanged (`avdecc_l2 listen`) |

## B. AEM descriptor model  *(Milan v1.2 §5.3.3.1–5.3.3.11)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| Mandatory descriptor set (ENTITY…STRINGS) | MANDATES | FR-ENUM-02 | Milan fixes the tree a PAAD exposes; missing descriptors ⇒ unusable/non-conformant. | T,I  -  `Hive` enumerate + `tsn-gen aecp_read_descriptor`; inspect vs entity JSON |
| Media-clock model: CLOCK_DOMAIN over CLOCK_SOURCEs (Internal/stream/CRF) | MANDATES | FR-CLK-03 | Nothing to select/lock without the model. | T  -  `Hive` read + SET_CLOCK_SOURCE; `avdecc_l2` |
| IDENTIFY CONTROL (§5.3.3.10) | MANDATES | FR-MGT-01 | User must physically locate the device. | T,D  -  `Hive` SET_CONTROL identify; observe device |
| Names/config settable & persist | MANDATES/SHOULD | FR-CTRL-02, FR-MGT-02 | Configuration model + labelling. | T  -  `tsn-gen aecp_set_name / set_configuration`; reboot + re-read |

## C. Enumeration & control  -  AECP/AEM  *(Milan v1.2 §5.4)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| `READ_DESCRIPTOR` returns the exact model | MANDATES | FR-ENUM-01 | Byte-wrong descriptors desync controllers. | T  -  `tsn-gen aecp_read_descriptor` (byte-exact) vs entity JSON; `Hive` |
| `ACQUIRE_ENTITY` / `LOCK_ENTITY` (Milan timeouts) | MANDATES | FR-CTRL-01 | Two controllers must not make conflicting changes. | T  -  `tsn-gen aecp_acquire_lock_entity.feature`; two-controller `Hive` test |
| SET/GET config, name, stream_format, clock_source, sampling_rate | MANDATES | FR-CTRL-02 | Connection setup depends on these SETs. | T  -  `tsn-gen aecp_aem_set_{stream_format,clock_source,sampling_rate,name,configuration}` |
| Unsolicited notifications, ≥16 controllers | MANDATES | FR-CTRL-03 | Controllers show stale state without it. | T  -  register (`Hive`), induce change, observe unsolicited response |
| `GET_COUNTERS` (stream/interface sets) | MANDATES | FR-CTRL-04, NFR-OBS-01 | Used in Milan adverse-network/fault tests. | T  -  `avdecc_l2 counters --descriptor stream_input/…` |
| AECP validation & correct status | MANDATES | FR-CTRL-06 | Wrong status on bad commands = conformance fail. | T  -  `tsn-gen aecp_non_aem` / malformed-PDU features |
| `GET_DYNAMIC_INFO` fast enumeration | SHOULD | FR-CTRL-05 | Large-model optimization. | T  -  `Hive` fast-enum |

## D. Milan Vendor Unique  -  MVU  *(Milan v1.2 §5.4.3.2)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| MVU (`00-1B-C5-0A-C1-00`) + `GET_MILAN_INFO` | MANDATES | FR-MVU-01 | The Milan identity handshake; no MVU ⇒ not a Milan device. | T  -  `tsn-gen aecp_vendor_unique.yaml`; `Hive` Milan-info; `AVnu` |
| `GET/SET_SYSTEM_UNIQUE_ID`, `…_MEDIA_CLOCK_REFERENCE_INFO` | MANDATES | FR-MVU-02 | Media-clock-reference mgmt + system grouping. | T  -  MVU command exchange (custom `tsn-gen` case) |
| `features_flags` truthful | MANDATES | FR-MVU-03 | Controllers plan features from these bits. | I,T  -  inspect + read `GET_MILAN_INFO` (`MILAN_REDUNDANCY=0`) |

## E. Connection management  -  ACMP  *(Milan v1.2 §5.5)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| `CONNECT/DISCONNECT/GET_*_STATE` (talker & listener) | MANDATES | FR-CONN-01 | No stream without ACMP. | T  -  `avdecc_l2 connect/disconnect`; `tap_acmp` |
| Program datapath (classifier queue + CBS) on connect | MANDATES | FR-CONN-02 | Stream needs SR class + shaped bandwidth or it misses latency. | T  -  connect, then read CBS/classifier CSR (`vtb:csr` semantics) / `tc cbs` |
| **Fast-connect / saved-state restore** on power/link-up | MANDATES | FR-CONN-03, FR-CONN-04 | Installed systems must recover without a controller. | T,D  -  save connection, power-cycle, observe auto-reconnect (`tap_acmp` + `avdecc_l2 listen`) |

## F. Streaming & stream formats  -  AVTP AAF  *(Milan v1.2 §5.4 format match; §6 Base Audio Formats)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| Talker AAF encapsulation + valid presentation time | MANDATES | FR-STR-01 | Presentation time aligns listener playout. | T  -  `soak` (pw1→pw0); `tap_sniff` AVTP; `thdn` |
| Listener de-encapsulation + de-jitter to presentation time | MANDATES | FR-STR-02, NFR-LAT-01 | Must render at the presentation instant within Class A. | T  -  `soak`; `thdn`; `latency.md` |
| **Listener format-adaptive** (`SET_STREAM_FORMAT` → talker's format; match incoming AAF) | MANDATES | FR-STR-03, FR-STR-03b | A format-locked listener can't connect to a differing talker. | T  -  set talker format, connect, confirm listener `current_format` follows (`Hive`+`avdecc_l2`); packet-match per `stream.c` |
| Talker format is fixed | MANDATES | FR-STR-03a | Only the talker source is singular. | I,T  -  inspect `STREAM_OUTPUT`; `tap_sniff` transmitted format |
| Base Audio Formats (6/12/24 spp @48/96/192k) | MANDATES | FR-STR-03, FR-STR-05 | Cross-vendor interop. | I,T  -  inspect `raw_hex`; interop against a reference talker |
| Stream counters + fault recovery | MANDATES | FR-STR-04, NFR-REL-01 | Milan adverse-network conformance. | T  -  `avdecc_l2 counters` during induced link flap; `AVnu` |

## G. Reservation & addressing  -  MAAP, SRP  *(Milan v1.2 §5.6; 802.1Qat/Qak)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| MAAP dynamic multicast allocation + defend | MANDATES | FR-MAAP-01 | Avoids stream dest-MAC clashes. | T  -  `maap` daemon + `tap_sniff` (PROBE/DEFEND/ANNOUNCE) |
| MSRP Talker Advertise / Listener Ready; MVRP VLAN reg | MANDATES | FR-SRP-01, FR-SRP-02 | Class A needs end-to-end bandwidth reservation. | T  -  `mrpd` + observe reservation on the bridge |
| Reservation gates tx; CBS from the grant; ≤75 % SR | MANDATES | FR-SRP-03, FR-QOS-02, FR-QOS-03 | Over-transmit breaks other streams' guarantees. | T,A  -  `tc cbs offload`; `vtb:cbs` (idleSlope/credit); no-tx-on-fail case |

## H. Media clocking & time  -  gPTP  *(Milan v1.2 §5.7; 802.1AS; 1722-2016 §10 CRF)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| 802.1AS time-aware endpoint (Class A), GM tracking | MANDATES | FR-CLK-01, NFR-TIME-01 | Presentation times live on the gPTP timebase (≤1 µs). | T  -  `ptp4l`/`phc2sys` lock; `ethtool -T`; `gptp-phc-clock.md` (offset ≤1 µs) |
| Media clock from CRF / input stream; CRF talker+recovery | MANDATES | FR-CLK-04, NFR-TIME-02 | Drift ⇒ periodic MEDIA_RESET / artifacts. | T  -  `soak` (clock-recovery); `tap_sniff` CRF |
| HW timestamps at the SFD | MANDATES | FR-CLK-05 | gPTP/AVTP accuracy needs HW capture. | T  -  `ethtool -T` + timestamp capture; `vtb:ptp` |
| PHC on a fixed (speed-independent) clock | MANDATES(impl) | FR-CLK-02, NFR-TIME-03 | Speed-switched PHC ⇒ wrong ns rate at 10/100/1000. | A,T  -  `vtb:ptp` (rate at each speed); analysis (REQ-PTP-07) |

## I. QoS datapath  -  802.1Q / 802.1Qav  *(required by Milan for Class A)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| PCP classification into SR/BE queues | MANDATES | FR-QOS-01 | Class A must land in its shaped queue. | T  -  `vtb:cls` (PCP→TC→queue over random configs) |
| CBS shaping of SR; strict priority for BE | MANDATES | FR-QOS-02, NFR-LAT-01, NFR-DET-01 | CBS bounds queuing latency to the 2 ms budget and isolates media from BE. | T  -  `vtb:cbs`, `vtb:shaper_core`; `tc qdisc … cbs offload` |

## J. Timing / performance NFRs  *(Milan Class A service class)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| Class A latency bound (≈2 ms), configurable | MANDATES | NFR-LAT-01 | Exceeding the presentation offset drops samples. | T  -  `latency.md` (end-to-end measurement) |
| Sustain Class A packet rate (8000 pkt/s/stream) | MANDATES | NFR-PERF-02 | Under-delivery starves the listener ⇒ MEDIA_RESET. | T  -  `soak` (sustained) + `avdecc_l2 counters` |
| Media path undisturbed by control/BE load | MANDATES | NFR-DET-01 | Deterministic streaming regardless of mgmt activity. | T  -  `soak` under injected BE load |
| Control RTT within 1722.1 inflight timeouts | SHOULD | NFR-LAT-02 | Slow responses trigger retries. | T  -  measure AECP/ACMP RTT (`avdecc_l2`/`Hive`) |

---

## K. Milan features intentionally OUT OF SCOPE

| Milan feature | Status | Recorded | Verify |
|---------------|--------|----------|--------|
| Seamless **redundancy** | Out of scope; `MILAN_REDUNDANCY=0` | FR-MVU-03, entity `_redundancy_note` | I  -  `GET_MILAN_INFO` reports 0; single AVB_INTERFACE |
| Rates **> 192 kHz** | Out of scope | entity scope | I  -  AUDIO_UNIT `sampling_rates` |
| **AEM authentication** | Not mandated by Milan | NFR-SEC-01 | I  -  advertises not-required; behaves safely unauthenticated |

## L. Requirements NOT Milan-driven (project / platform)

Milan only **CONSTRAINS** these; it does not require them.

| FR/NFR | Driver | Milan relationship | Verify |
|--------|--------|--------------------|--------|
| NFR-SCUP-01..04 (scale-up) | one design, small↔large | CONSTRAINS: growing `P_CH/P_SR` must not change the control plane / break Class A | A,D  -  build full entity, re-run the whole T-suite at 8-ch/48-96-192k |
| NFR-SCOUT-01..07 (scale-out, >1 softcore) | capacity via N softcores | CONSTRAINS: all cores see **one coherent PHC** (FR-CLK-01) + media stays deterministic (NFR-DET-01) | A,D  -  build `P_CORES=2..N` (SMP **and** AMP), re-run T-suite; single-PHC check; per-core sizing benchmark |
| NFR-RES-01 (fit xc7a100t) | FPGA budget | none | A  -  Vivado utilization report ≤ target |
| NFR-REL-02 (media-core watchdog) | AMP robustness | ENABLES: keeps Milan planes alive on media-core fault | T  -  hang a media core, observe restart w/o dropping control |
| NFR-MAINT-01 (single-source model) | engineering | ENABLES: HW+SW+tests stay Milan-consistent | I  -  CI diff entity JSON vs `entity-model-milan-v12.h` |
| NFR-PORT-01 (RV64/RV32 build) | platform | none | A  -  build both targets |
| NFR-OBS-01 (observability) | ops | ENABLES: surfaces Milan counters (FR-CTRL-04) | D  -  `ethtool -S`/`-T`, per-core load, AVDECC counters |

---

## Coverage & test summary

- **Every Milan area (A–J) maps to ≥1 MANDATES FR** with a named test artifact  -  no
  Milan area is unmapped or unverified.
- **HW-verifiable now (Verilator, no controller):** FR-QOS-\* (`vtb:cbs/shaper_core/cls`),
  FR-CLK-02/05 (`vtb:ptp`), CSR/IRQ (`vtb:csr`), FR-DISC ADPDU (`vtb:adp`, to add).
- **Interop/system:** ADP/AECP/ACMP/MVU via `avdecc_l2`/`tap_acmp`/`tsn-gen`/`Hive`;
  gPTP via `ptp4l`; streaming via `soak`/`thdn`; reservation via `mrpd`/`maap`.
- **Conformance:** the `AVnu` Milan test plan is the acceptance gate.
- **Scale (L):** the same T-suite is re-run at the full profile and at `P_CORES=2..N`
  (SMP, AMP)  -  passing there proves scale-up/out without re-proving Milan logic.

See [`FR_NFR.md`](FR_NFR.md) §6 (forward traceability to milestones) and §7
(verification approach), and [`avdecc/README.md`](../avdecc/README.md) for the entity
model the descriptors trace to.
