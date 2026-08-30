# Milan v1.2 endpoint  -  Functional & Non-Functional Requirements (FR/NFR)

**System:** a small **Milan v1.2** audio endpoint (PAAD  -  Professional Audio AVB
Device)  -  a **stereo (2-channel) talker + listener at 48 kHz**  -  implemented on
the fully-FPGA RISC-V platform (VexiiRiscv + LiteX on Alinx AX7101). The
release uses one cacheless RV32I control hart and scales media capacity through
fabric stream contexts, channels, sample rates, and, in future profiles,
replicated physical ports.

- **Current Milan v1.2 implementation verdict:** [`../testing/MILAN_V12_AUDIT_2026-08-16.md`](../testing/MILAN_V12_AUDIT_2026-08-16.md)
- **Current entity definitions:** [`configs/endstation_*.yaml`](../../configs) through the [end-station builder](../ENDSTATION_BUILDER.md)
- **Platform & phasing:** the completed PS-to-fabric migration plan (#259, in git history)
- **HW AEM/AECP design:** the fabric AECP/AEM engine and its design page are
  **deleted** (2026-08-13); AECP now lives in the pinned `protocol-processor`
  submodule's AECP uCPU. The current served-command inventory and root
  integration boundaries are recorded in the implementation-status ledger in
  Section 2.0.

Requirement keywords per RFC 2119 (**MUST / SHOULD / MAY**). Each requirement has a
**priority** (M=MUST, S=SHOULD, C=MAY), a **source**, and a **verification method**
(T=test, A=analysis, D=demonstration, I=inspection).

---

## Contents

- **[1. Scope, actors, and the baseline system](#1-scope-actors-and-the-baseline-system)** -- What "the baseline endpoint" concretely means, plus the `P_CH`/`P_SI`/`P_SO`/`P_SR`/`P_PORTS` parameter table every later requirement is written against. States the asymmetry that drives Section 2.7: the talker is fixed stereo, the listener is format-adaptive.
- **[2. Functional Requirements (FR)](#2-functional-requirements-fr)** -- Opens with **[Section 2.0, the implementation-status ledger](#20-implementation-status-after-the-protocol-processor-substitution-2026-08-13)**: which groups the protocol processor owns, which AECP commands it serves, which dynamic outputs the root integration does not yet consume, and which mandatory requirements remain open. Read it before any row, and read a refusal as a refusal. Then nine subsections of MUST/SHOULD rows with priority and verification method, covering ADP through AECP/MVU, ACMP, MAAP/SRP, clocking, streaming, QoS and management.
- **[3. Non-Functional Requirements (NFR)](#3-non-functional-requirements-nfr)** -- The line-rate, packet-rate, timing, resource, fabric scale-up, and future multi-port bounds for the one-hart bare-metal product.
- **[4. Scalability architecture](#4-scalability-architecture)** -- How configuration grows fabric streams, channels, rates, and optional endpoint replicas while the CPU remains a single boot-and-policy controller outside packet and media deadlines.
- **[5. Steps to comply with Milan v1.2 (procedure)](#5-steps-to-comply-with-milan-v12-procedure)** -- The ordered twelve-step path from bare platform to conformance run, each step citing the FRs it discharges. Ends with the explicit out-of-scope list -- redundancy, rates beyond 192 kHz, AEM authentication.
- **[6. Traceability (summary)](#6-traceability-summary)** -- One compact table joining each functional area to its Milan clause, its entity-model artifact, and its plan milestone -- the index to use when you need "which requirement covers this".
- **[7. Verification approach](#7-verification-approach)** -- Which evidence class answers which kind of requirement: Verilator harnesses for leaf blocks, controller, fabric-gPTP and CSR tooling for interop, YAML models for PDU byte-exactness, and repetition at full profile for the scale claims.

## 1. Scope, actors, and the baseline system

### 1.1 Baseline (the "small" endpoint)
One entity, one network port, on **one softcore**:

```
   Controller (Hive / avdecc_l2.py)                Media (AVB peer / DAC)
            │  1722.1 AVDECC (L2)                          │ audio
            ▼                                              ▼
   ┌───────────────────────── AX7101 (xc7a100t) ────────────────────────┐
   │  VexiiRiscv core0, bare-metal RV32I firmware                       │
   │   • boot policy, CSR init, identity, persistence, UART diagnostics │
   │   • ADP/AECP/ACMP/MAAP + SRP: the protocol processor, in fabric    │
   ├───────────────────────────────────────────────────────────────────┤
   │  FPGA datapath (HW): integrated gPTP default owner + PHC steering  │
   │    GMII MAC ─ 802.1Q classifier ─ CBS ─ AVTP talker/listener       │
   └───────────────────────────────────────────────────────────────────┘
                                   │ GMII 1 GbE
                                   ▼  AVB/TSN network (bridge)
```
Baseline stream profile, 48 kHz, 32-bit, Class A (2 ms, 8000 pkt/s), + a CRF
media-clock stream:
- **Talker:** 1 AAF source, **fixed stereo (2 ch)**  -  "stereo" is a talker property.
- **Listener:** 1 AAF sink, **format-adaptive**  -  advertises the Milan Base Audio
  Formats (1/2/4/8 ch @48 kHz) and adapts `current_format` to the connected talker
  via `SET_STREAM_FORMAT` (Milan v1.2 Section 5.4), rendering the mapped stereo subset.

### 1.2 Scaling parameters (referenced throughout)
| Param | Meaning | Baseline | Scale-up target | Scale-out lever |
|-------|---------|----------|-----------------|-----------------|
| `P_CH` | channels per stream | 2 | 8 → 64 |  -  |
| `P_SI` / `P_SO` | stream sinks / sources | 1 / 1 | 8 / 8 | fabric contexts |
| `P_SR` | sample-rate set | {48k} | {48,96,192k} |  -  |
| `P_PORTS` | AVB interfaces / entities | 1 | 1 | future replicated fabric endpoint |

The release CPU count is fixed at one. It is not a media-capacity parameter:
all per-frame protocol, time, packet, and audio work is fabric-owned.

### 1.3 Actors
AVDECC **Controller**; peer **Talker**/**Listener** entities; **802.1AS**
grandmaster/bridge; **SRP** bridge; local **media** app.

---

## 2. Functional Requirements (FR)

### 2.0 Implementation status after the protocol-processor substitution (2026-08-13)

**Read this before any row below.** A requirement is what the system must do;
this ledger is what it currently does. **No requirement has been deleted or
downgraded to make the page look green** — several are simply not met, and
say so.

On 2026-08-13 this repository's own ADP advertiser, ACMP talker and listener,
AECP/AEM engine and lwSRP applicant were **deleted** and replaced by the
pinned `protocol-processor` submodule (architecture of record v2.0), wrapped
by `hdl/milan/KL_pp_shadow.sv` and instantiated unconditionally. The
processor owns **ADP, ACMP, SRP — and now AECP**: its AECP uCPU has landed and
the entity is reachable on AECP.

**What that engine does, exactly.** The processor's concrete operation decode is
the `OP_*_C` table in `protocol-processor/hdl/aecp/KL_aecp_engine.sv`. The
canonical documented inventory is the Milan feature status ledger, whose check
also matches the compliant bench's served-operation table. The engine includes
`READ_DESCRIPTOR`, `ACQUIRE_ENTITY`, `LOCK_ENTITY`, entity and configuration
operations, stream and clock getters, sampling-rate operations,
`SET_CLOCK_SOURCE`, Identify control, `GET_STREAM_INFO`,
`GET_AVB_INFO`, `GET_AS_PATH`, `GET_COUNTERS`, `GET_AUDIO_MAP`, unsolicited
registration, and Milan `GET_MILAN_INFO`. `READ_DESCRIPTOR` has command-specific
`SUCCESS`, `NO_SUCH_DESCRIPTOR`, and `BAD_ARGUMENTS` paths. `ACQUIRE_ENTITY`
returns `NOT_SUPPORTED`, never `SUCCESS`, with the zero-owner command form
required by Milan Delta 7. The validator silently refuses a foreign target and
an AECP response presented as input. Unsupported commands receive a conformant
fallback response, but that fallback does not implement their required behavior.

**Read the ledger with that in mind: an echo is not an implementation.** A row
below that reads NOT IMPLEMENTED is not describing silence. It describes a
device that answers "no" correctly and does not perform the operation. The
end-station builder generates `aem_desc.bin`, `aem_desc.json`, and
`aem_desc.map` from the selected configuration. The tracked bare-metal deployment
packages the paired artifacts; firmware verifies the generated length and CRC and copies the image to
`PP_DESC_BASE_P` before entity enable. A custom integration that omits that step
still fails closed with `BAD_ARGUMENTS`. The Table 5.22 counter-change producer,
the other root-observed notification triggers, and the departing-controller
monitor are implemented at 0x0055. Saved-state persistence remains open.

These repeated claims are checked against the
[Milan feature status ledger](MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
<!-- milan-feature-status:end -->

| Requirement group | Verdict | Where it lives now |
|---|---|---|
| **FR-DISC-01..05** (ADP) | **OWNED BY THE PROTOCOL PROCESSOR** | `KL_adp_engine`. Advertisement content is the entity model via `adp_shape_defaults.svh`; `available_index` is published to the CSR plane. The historic `ADP_CTRL.en` still enables the entity (ORed with `PP_CTRL[0]`), but the ADPDU *content* CSR words are write-only scratch that reach nothing |
| **FR-ENUM-01** (`READ_DESCRIPTOR`) | **IMPLEMENTED AND SUPPLIED** | The uCPU's descriptor store fetches over a read-only master at compile-time `PP_DESC_BASE_P`. The builder generates the image, JSON manifest, and map; bare-metal firmware verifies and copies the paired image from QSPI before entity enable. An omitted or invalid image fails closed with `BAD_ARGUMENTS`, a locate miss returns `NO_SUCH_DESCRIPTOR`, a late load heals without reset, and the 4096-cycle watchdog prevents a stalled memory path from hanging the responder |
| **FR-ENUM-02** (the Milan-mandatory descriptor tree) | **IMPLEMENTED IN THE TRACKED BUILD FLOW** | The selected entity configuration generates the mandatory descriptor tree and flat image artifacts. The tracked board flow packages and loads them. Custom integrations must preserve the same load-before-enable ordering |
| **FR-CTRL-01..05** (acquire/lock, get/set, unsolicited, counters, fast enumeration) | **PARTLY MET** | The processor serves the mandatory command inventory. `ACQUIRE_ENTITY` returns Milan Delta 7 `NOT_SUPPORTED` with no owner. FR-CTRL-03's registration, successful-command notifications, Table 5.22 scheduler, and departing-controller monitor are implemented. FR-CTRL-04 serves every supported counter bank and rate-limits each descriptor's push to at most once per second. Persistence remains open, and the declared CRF Stream Input still has no served counter bank |
| **FR-CTRL-06** (validate cdl / message_type / target, correct status) | **PARTLY MET** | Met: the duty to answer, correct response shape and identity fields, silent refusal of a foreign target or response-as-input, command-specific `BAD_ARGUMENTS`, `NOT_SUPPORTED`, and descriptor-locate statuses, and lock conflict behavior within the served inventory. The mandatory commands listed in the current audit still need their own payload validation and behavior before this group can be closed |
| **FR-MVU-01..03** (Milan Vendor Unique, GET_MILAN_INFO) | **PARTLY MET** | The engine recognizes the Milan protocol ID and serves `GET_MILAN_INFO`, including a zero redundancy feature flag. The system/media-clock reference operations in FR-MVU-02 remain outside the served inventory and receive the conformant fallback |
| **FR-CONN-01/02** (ACMP connect/disconnect/state, program the datapath) | **OWNED BY THE PROTOCOL PROCESSOR** | `KL_acmp_talker` + the listener half; the bind record and the talker declaration reach the fabric as class-D wires, and the CBS/classifier programming follows the reservation |
| **FR-CONN-03/04** (fast-connect, nonvolatile connection state) | **NOT MET** | The persistence journal and the bind-restore port are structural zeros: writes are accepted, nothing is restored, **no binding survives a power cycle**. Milan v1.2 5.3.8.2 wants saved state; this build does not have it and says so structurally |
| **FR-MAAP-01** | **MET, in this fabric** | `KL_maap` remains the shipping allocator. The processor also contains `KL_pp_maap`, but this integration disables it with `cfg_maap_internal_i = 0` and reaches the selected fabric engine through `KL_pp_maap_shim`. The talker cannot declare without an `ALLOC_DA` success, so the DA gate *is* the talker gate |
| **FR-SRP-01/02/03** | **OWNED BY THE PROTOCOL PROCESSOR** | Its SRP engine registers/deregisters and admits; the granted slope, adopted domain and admission bit drive the CBS mux and the AAF gate exactly as before. The slope/gate *ordering* changed shape and not safety — see [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md) |
| **FR-CLK-01/02/05** (gPTP, PHC, HW timestamps) | **MET** | Untouched by the substitution |
| **FR-CLK-03/04** (select and recover the media clock from Internal / input-stream / CRF sources) | **NOT MET AT THE ROOT INTEGRATION** | The processor accepts and stores `SET_CLOCK_SOURCE`, and `KL_pp_shadow.sv` exports `aecp_clk_src_index_o` to the root. The media plane does not consume that selection, so `CRF_CLK_SELECTED_C` remains zero (INTERNAL) and the MMCM-DRP and packet-grid NCO servos stay idle. `KL_crf_rx` still parses, counts and reports, but cannot steer the media clock |
| **FR-STR-01/02/04/05** (AAF encapsulation, de-encapsulation, listener counters, parameterisation) | **MET** | The media plane is intact |
| **FR-STR-03/03a/03b** (listener format adaptation via SET_STREAM_FORMAT) | **MET AT THE CONTROL PLANE (0x0053); wire reshape deferred** | `SET_STREAM_FORMAT` is served for both stream directions with the Milan 5.4.2.7 refusals and a per-row format verdict; a stored setting becomes the served current format and drives STREAM_INPUT 0's acceptance filter. The *wire-truth* rule still governs de-interleaving, so render adaptation follows channels_per_frame off the wire; what remains deferred is the framers re-shaping from a stored format, recorded in the audit with the SET_CONFIGURATION precedent |
| **FR-QOS-01..03** | **MET** | Classifier + CBS untouched; the Σ idleSlope ceiling is enforced by the processor's admission now |
| **FR-MGT-01** (IDENTIFY) | **IMPLEMENTED IN THE PROCESSOR, UNCONSUMED AT ROOT** | Identify `SET_CONTROL` and `GET_CONTROL` are served by the processor, and `KL_pp_shadow.sv` exports `aecp_identify_o` to the root wire `pp_aecp_identify_w`. Nothing consumes the wire and the root ties `o_identify` low. The controller-visible state exists while the physical Identify output remains dark. An inbound `IDENTIFY_NOTIFICATION` command is separately refused with `BAD_ARGUMENTS` as required by Section 7.4.39.2 |
| **FR-MGT-02** (names settable and persisted) | **PARTLY MET** | `SET_NAME` and `GET_NAME` are served for every generated semantic name, and SET is coherent with READ_DESCRIPTOR. The writable names are volatile because nonvolatile restoration remains open |
| **NFR-\*** | unchanged in kind | The budgets and bounds still apply. Two are worth re-reading against the new plane: **NFR-LAT-01** (the presentation-time bound is now the Milan **2 ms default and is not configurable**, since `SET_MAX_TRANSIT_TIME` is unimplemented — a default, not a zero) and **NFR-SCUP-04** (the AEM memory it sizes has moved out of the gateware into main memory) |

The honest one-line summary: **this device discovers over ADP, connects over
ACMP, reserves over SRP, streams audio and serves the processor's AECP command
inventory, including READ_DESCRIPTOR and GET_COUNTERS.** The tracked builder
and board flow supply the descriptor image. Unsupported commands receive the
conformant fallback, and the current audit lists the remaining mandatory gaps.

### 2.1 Discovery  -  ADP  *(1722.1-2021 Section 6; Milan v1.2 Section 5.2)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-DISC-01 | The entity MUST advertise `ENTITY_AVAILABLE` ADPDUs and re-advertise within `valid_time`, incrementing `available_index` on every state change. | M | T |
| FR-DISC-02 | The entity MUST answer `ENTITY_DISCOVER` (global and targeted) with an advertisement. | M | T |
| FR-DISC-03 | The entity MUST send `ENTITY_DEPARTING` on shutdown / link down. | M | T |
| FR-DISC-04 | Advertised fields (`entity_id`, `entity_model_id`, capabilities, talker/listener counts, `gptp_grandmaster_id`, `identify_control_index`, `interface_index`) MUST equal the ENTITY descriptor in the entity model. | M | T,I |
| FR-DISC-05 | `entity_id` MUST be an EUI-64 derived from the AVB_INTERFACE MAC and be stable across reboots. | M | A |

### 2.2 Enumeration & control  -  AECP/AEM  *(1722.1-2021 Sections 7 and 9; Milan v1.2 Section 5.3–5.4)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-ENUM-01 | The entity MUST serve every descriptor in the model via `READ_DESCRIPTOR`, byte-matching the JSON entity model. | M | T |
| FR-ENUM-02 | The AEM descriptor tree MUST include the Milan-mandatory set: ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT (AAF + CRF), STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN, CLOCK_SOURCE, STREAM_PORT_IN/OUT, AUDIO_CLUSTER, AUDIO_MAP, CONTROL(IDENTIFY), LOCALE, STRINGS. | M | I |
| FR-CTRL-01 | `ACQUIRE_ENTITY` and `LOCK_ENTITY` MUST be supported with the Milan timeouts; a locked entity MUST reject conflicting SETs with `ENTITY_LOCKED`. | M | T |
| FR-CTRL-02 | `GET/SET_CONFIGURATION`, `GET/SET_NAME`, `GET/SET_STREAM_FORMAT`, `GET/SET_CLOCK_SOURCE`, `SET_SAMPLING_RATE` MUST be supported for the descriptors that expose them (per the model's `dynamic`/`nonvolatile` fields). | M | T |
| FR-CTRL-03 | `REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION` MUST be supported for ≥ 16 controllers; state changes MUST emit unsolicited responses to registered controllers. | M | T |
| FR-CTRL-04 | `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE (see model `counters`), throttled ≤ 1/s. | M | T |
| FR-CTRL-05 | `GET_DYNAMIC_INFO` (fast enumeration) MUST be supported per Milan v1.2 5.4.2.29. | M | T |
| FR-CTRL-06 | AECP MUST validate `control_data_length`, `message_type=AEM_COMMAND`, and target `entity_id`; malformed/unsupported commands MUST return the correct AECP status (`NOT_IMPLEMENTED`, `BAD_ARGUMENTS`, `ENTITY_LOCKED`, …). | M | T |

### 2.3 Milan Vendor Unique  -  MVU  *(Milan v1.2 Section 5.4.3)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MVU-01 | The entity MUST implement the MVU protocol (`protocol_id 00-1B-C5-0A-C1-00`) and answer `GET_MILAN_INFO` with `protocol_version`, `features_flags`, `certification_version`. | M | T |
| FR-MVU-02 | `GET/SET_SYSTEM_UNIQUE_ID` and `GET/SET_MEDIA_CLOCK_REFERENCE_INFO` MUST be supported. | M | T |
| FR-MVU-03 | `features_flags.MILAN_REDUNDANCY` MUST report 0 (redundancy out of scope). | M | I |

### 2.4 Connection management  -  ACMP  *(1722.1-2021 Section 8; Milan v1.2 Section 5.5)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-CONN-01 | The entity MUST support `CONNECT_TX/RX`, `DISCONNECT_TX/RX`, `GET_TX/RX_STATE` as talker and listener. | M | T |
| FR-CONN-02 | On a successful connection the entity MUST program the HW datapath: classifier queue for the stream's VLAN/PCP and CBS idleSlope/hi/lo for the reservation. | M | T |
| FR-CONN-03 | ACMP MUST implement the Milan **fast-connect** / state-restore behavior (re-establish saved connections on power-up/link-up). | M | T |
| FR-CONN-04 | Connection state MUST persist (nonvolatile) across reboot for fast-connect. | S | T |

### 2.5 Addressing & reservation  -  MAAP, SRP  *(1722 Annex B; 802.1Qat/Qak; Milan Section 5.6)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MAAP-01 | The talker MUST allocate stream destination multicast MACs via MAAP (PROBE/DEFEND/ANNOUNCE) and defend them. | M | T |
| FR-SRP-01 | The entity MUST register/deregister SRP (MSRP) Talker Advertise / Listener Ready and reserve bandwidth for Class A streams. | M | T |
| FR-SRP-02 | The entity MUST register the stream VLAN via MVRP. | M | T |
| FR-SRP-03 | On reservation grant the CBS shaper MUST be configured to the reserved idleSlope; on failure the stream MUST NOT transmit. | M | T |

### 2.6 Time & media clock  -  gPTP, CRF  *(802.1AS; 1722-2016 Section 10; Milan Section 5.7)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-CLK-01 | The entity MUST run 802.1AS gPTP as a time-aware endpoint (Class A), sync to the grandmaster, and report GM changes. | M | T |
| FR-CLK-02 | The PHC MUST be disciplined from a fixed 125 MHz free-running clock (REQ-PTP-07), independent of link speed. | M | A,T |
| FR-CLK-03 | The media clock MUST be selectable (CLOCK_DOMAIN → CLOCK_SOURCE) among Internal, input-stream (AAF), and CRF. | M | T |
| FR-CLK-04 | As a media-clock talker the entity MUST source a CRF stream; as a follower it MUST recover media clock from CRF or the input stream. | M | T |
| FR-CLK-05 | HW ingress/egress timestamps MUST be captured at the GMII SFD and delivered directly to the fabric gPTP plane and diagnostic counters. | M | T |

### 2.7 Streaming  -  AVTP AAF talker/listener  *(1722-2016 Section 7; Milan Section 6)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-STR-01 | The talker MUST encapsulate `P_CH`-channel AAF PCM (48 kHz, 32-bit, 6 samples/frame, Class A) with a valid AVTP presentation time = capture time + offset. | M | T |
| FR-STR-02 | The listener MUST de-encapsulate AAF, validate `avtp_timestamp`, de-jitter to presentation time, and render at the media clock. | M | T |
| FR-STR-03 | The **listener MUST be format-adaptive**: STREAM_INPUT MUST advertise every supported format (the Milan Base Audio Formats, `number_of_formats > 1`) and set its `current_format` to the **connected talker's** format via `SET_STREAM_FORMAT` at connection  -  it MUST NOT be fixed. A received AAF AVTPDU MUST match the adapted `current_format` (subtype/format/nsr/bit-depth/channels/sparse); mismatches MUST count `UNSUPPORTED_FORMAT`. | M | T |
| FR-STR-03a | The **talker** sources a **fixed** format (this device: stereo/2 ch); "stereo" is a talker property only. A talker with multiple producible formats MAY list them, but the transmitted format is fixed per connection. | M | I,T |
| FR-STR-03b | When adapting to a talker with more channels than the device renders, the listener MUST render the mapped subset (AUDIO_MAP) and MUST still lock/validate the full advertised format. | M | T |
| FR-STR-04 | The listener MUST maintain the STREAM_INPUT counters (MEDIA_LOCKED/UNLOCKED, LATE/EARLY_TIMESTAMP, SEQ_NUM_MISMATCH, UNSUPPORTED_FORMAT, …) and recover from stream faults (MEDIA_RESET) per Milan. | M | T |
| FR-STR-05 | Baseline: `P_SI=1`, `P_SO=1`, talker `P_CH=2`, listener advertises the base set; the design MUST be parameterized so `P_CH`, `P_SI`, `P_SO`, `P_SR` scale without protocol changes (see Section 4). | M | I,A |

### 2.8 QoS datapath  -  802.1Q / 802.1Qav  *(already in HW)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-QOS-01 | Frames MUST be classified by PCP into traffic classes/queues (programmable tables) with Class A → its shaped queue. | M | T |
| FR-QOS-02 | The CBS (802.1Qav) MUST shape SR queues to their idleSlope with hi/lo credit; non-SR traffic MUST use strict priority (unshaped). | M | T |
| FR-QOS-03 | Σ idleSlope of shaped queues MUST NOT exceed 75 % of port rate. | M | A,T |

### 2.9 Management  *(Milan Section 5.3.3.10)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MGT-01 | The IDENTIFY CONTROL MUST put the device into identification mode while its value ≠ 0. | M | T |
| FR-MGT-02 | Names (entity/group/config) MUST be settable and persisted; factory reset MUST restore defaults. | S | T |

---

## 3. Non-Functional Requirements (NFR)

### 3.1 Performance & real-time
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-PERF-01 | The datapath MUST sustain line-rate 1 GbE for the shaped streams without frame loss at baseline load. | M | T |
| NFR-PERF-02 | The AVTP talker/listener MUST sustain the Class A packet rate (8000 pkt/s per stream) continuously. | M | T |
| NFR-LAT-01 | End-to-end (talker capture → listener render) latency MUST meet the Milan Class A presentation-time bound using the product's 2 ms per-output default. | M | T |
| NFR-LAT-02 | AVDECC control command→response round-trip SHOULD be < 250 ms (well within 1722.1 inflight timeouts). | S | T |
| NFR-DET-01 | The media/AVTP path MUST be deterministic: bounded, jitter-controlled processing independent of best-effort/management load. | M | T |

### 3.2 Time accuracy
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-TIME-01 | gPTP synchronization error to the grandmaster MUST be ≤ 1 µs (Milan endpoint target). | M | T |
| NFR-TIME-02 | Media-clock recovery MUST hold long-term rate error within the AAF/CRF tolerance (no periodic MEDIA_RESET during a healthy stream). | M | T |
| NFR-TIME-03 | PHC frequency-adjust (adjfine) resolution MUST be ≤ 1 ppb-class (Q8.24 ns increment). | S | A |

### 3.3 Scale-**up** (same node, bigger workload)
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-SCUP-01 | The end-station model, generated artifacts, and fabric datapath MUST be parameterized by `P_CH`, `P_SI`, `P_SO`, `P_SR` so a larger endpoint (for example 8-channel, 48/96/192 kHz) is a configuration change, not a redesign. | M | A,I |
| NFR-SCUP-02 | Increasing `P_CH`/`P_SR` MUST only linearly increase bandwidth, buffer, and DSP; the control plane (ADP/AECP/ACMP) MUST be unaffected. | M | A |
| NFR-SCUP-03 | FPGA resource use MUST stay within the `xc7a100t` budget at the largest supported single-node profile (document the profile that first exceeds it). | S | A |
| NFR-SCUP-04 | The builder MUST generate and size the flat AEM image from the selected end-station model, and bare-metal boot MUST validate and install it at the processor's compile-time descriptor base without an RTL edit as descriptor counts grow. | S | I |

### 3.4 Fabric scale-out and future ports
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-SCOUT-01 | The release architecture MUST use one cacheless RV32I control hart; increasing stream capacity MUST elaborate additional fabric contexts rather than create a software packet or media plane. | M | A,D |
| NFR-SCOUT-02 | Protocol control, media movement, and time discipline MUST retain their explicit fabric owners as stream counts grow. | M | A |
| NFR-SCOUT-03 | Packet and audio deadlines MUST depend only on bounded fabric handshakes, never on firmware service latency. | M | A,T |
| NFR-SCOUT-04 | The PHC, MAC trunk, CSR window, and fabric egress arbiter MUST each have one coherent owner and deterministic arbitration across all elaborated streams. | M | A,T |
| NFR-SCOUT-05 | A future `P_PORTS ≥ 2` profile MAY replicate complete fabric endpoint instances with distinct AVB interfaces and entity identities; the current release profile remains one port. | S | A,D |
| NFR-SCOUT-06 | Increasing stream or endpoint instance counts MUST NOT change the CSR register definitions or end-station configuration schema. | M | I |
| NFR-SCOUT-07 | Per-stream and per-port fabric resource costs MUST be documented so a target stream/channel/port shape can be checked against the device budget. | S | A |

### 3.5 Resource, reliability, and the rest
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-RES-01 | Baseline (1 core, stereo 48 k) MUST fit `xc7a100t` with headroom (target ≤ 60 % LUT) to leave room for scale-out. | M | A |
| NFR-REL-01 | A stream fault (link flap, GM change, talker loss) MUST auto-recover without a reboot; counters MUST record the event. | M | T |
| NFR-REL-02 | Fabric liveness monitors SHOULD detect a stalled protocol, time, or media engine and recover or report it without requiring a full-board reboot. | S | T |
| NFR-OBS-01 | The system MUST expose fabric-gPTP status/publication counters and CSRs, AVDECC counters, MAC/RMON counters, and protocol/media liveness through the CSR contract. | S | D |
| NFR-MAINT-01 | The entity model MUST be single-source (JSON) and shared HW/SW/test; divergence MUST be caught in CI. | M | I |
| NFR-PORT-01 | The firmware MUST build for the shipping RV32I bare-metal profile with no OS dependency, and MUST stay buildable for a wider core should the profile grow. | S | A |
| NFR-SEC-01 | Milan v1.2 does not mandate AEM authentication; the entity MUST advertise `AEM_AUTHENTICATION` = not-required and behave safely when unauthenticated. | M | I |

---

## 4. Scalability architecture

### 4.1 One design, three axes
- **Scale streams:** grow `P_SI/P_SO`; shared engines retain one context record
  per stream and generated descriptors advertise the same shape.
- **Scale media:** grow `P_CH` and `P_SR`; capture, packetize, map, and render
  remain fabric paths whose resource and bandwidth costs are measured.
- **Scale ports/entities:** a future `P_PORTS` profile may replicate a complete
  fabric endpoint and physical interface. The current product remains one port
  and one RV32 control hart.

### 4.2 Plane partitioning (the basis for scale-out)
| Plane | Functions | Real-time? | Product owner | Scales to |
|-------|-----------|-----------|---------------|-----------|
| **Control** | ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP | bounded protocol deadlines | protocol processor plus fabric MAAP | generated stream contexts |
| **Media** | AVTP talker/listener, sample transport, presentation-time, media-clock | hard (µs) | AAF/CRF and physical-audio fabric | channels and stream contexts |
| **Time** | gPTP state machines/servo, PHC discipline, CRF generate/observe | hard (µs) | integrated fabric gPTP owner + PHC | one coherent time domain per endpoint |
| **Boot/policy** | image verification, CSR initialization, persistence, diagnostics | not per frame | one bare-metal RV32I hart | fixed at one in release profiles |

### 4.3 One control CPU, fabric capacity

The control CPU never becomes a packet or sample worker. Increasing stream or
channel count changes generated fabric context counts and the descriptor image;
it does not add firmware workers, packet queues, or a CPU-to-CPU transport.
This preserves bounded media and protocol behavior independently of firmware
load.

```
  one-port release endpoint:
    RV32 firmware: boot policy · identity · persistence · diagnostics
                       │ AXI-Lite CSR + descriptor-image provisioning
    protocol fabric: ADP · ACMP · AECP · SRP · MAAP
    media fabric:    AAF/CRF capture · packetize · map · render
    time fabric:     gPTP owner + single coherent PHC
                       │ deterministic fabric egress arbitration
                    one GMII MAC / physical port
```

### 4.4 Multi-entity scale-out (`P_PORTS`)
Any future additional port is an independent fabric endpoint slice: MAC,
AVB_INTERFACE, distinct `entity_id`, protocol/media/time context, and generated
entity model. The current release does not claim this profile; it is accepted
only after the replicated source, clock, CSR, and wire evidence closes.

### 4.5 Sizing (NFR-SCOUT-07)
For every supported `P_SI/P_SO`, `P_CH`, `P_SR`, and `P_PORTS` shape, publish
the builder estimate, open-synthesis delta, placed utilization, timing, and
wire-rate result. The supported ceiling is the largest shape that fits and
passes those gates; CPU count is not part of the formula.

---

## 5. Steps to comply with Milan v1.2 (procedure)

The ordered path from the baseline endpoint to a Milan-conformant device. Each step
cites the FRs it satisfies and the milestone in
the completed PS-to-fabric migration plan (#259, in git history).

1. **Platform up**  -  bare-metal RV32I firmware on the AX7101 with the HW
   datapath (MAC/CBS/classifier/PHC). *(M-A5)*
2. **gPTP (802.1AS)**  -  enable the integrated fabric owner and verify its
   wire/CSR/publication behavior plus ≤ 1 µs sync. Booted and two-board
   acceptance remains #117. *(FR-CLK-01/02, NFR-TIME-01)*
3. **Entity model**  -  select an `endstation_*.yaml` configuration. The
   builder generates `aem_desc.bin`, `aem_desc.json`, and `aem_desc.map`; the
   tracked bare-metal boot verifies and copies the paired image from QSPI to
   `PP_DESC_BASE_P` before enabling the entity. Verify a byte-exact
   `READ_DESCRIPTOR` walk. *(FR-ENUM-01/02)*
4. **ADP**  -  advertise/discover/depart with correct `available_index`. *(FR-DISC-\*)*
5. **AECP/AEM + MVU**  -  enumerate (READ_DESCRIPTOR byte-match), acquire/lock,
   set/get, GET_COUNTERS, GET_MILAN_INFO. *(FR-ENUM/CTRL/MVU)*
6. **Media clock**  -  CLOCK_DOMAIN/CLOCK_SOURCE selection; CRF talker + recovery.
   *(FR-CLK-03/04)*
7. **AVTP streaming**  -  AAF stereo 48 k talker + listener with presentation time.
   *(FR-STR-\*)*
8. **MAAP + SRP/MVRP**  -  allocate multicast, reserve Class A bandwidth, program CBS.
   *(FR-MAAP/SRP, FR-CONN-02)*
9. **ACMP**  -  connect/disconnect + Milan fast-connect/state-restore. *(FR-CONN-\*)*
10. **Fault behavior**  -  stream-interruption/redundancy-off recovery, counters,
    IDENTIFY. *(FR-STR-04, NFR-REL-01, FR-MGT-01)*
11. **Conformance**  -  run the internal Milan conformance plan (bench suite) + `srcs/the-private-test-repo`
    (`avdecc_l2.py`, fabric-gPTP capture/CSR oracles) and the `tsn-gen` AECP PDU
    checks. *(all Ver=T)*
12. **Scale**  -  re-run with every claimed fabric stream/channel/rate shape
    and any future replicated-port profile to prove Sections 3.3/3.4.
    *(NFR-SCUP/SCOUT)*

> Milan features intentionally **out of scope for now** (documented, not required
> here): seamless network **redundancy** (single interface), sample rates beyond
> 48/96/192 kHz, and AEM authentication.

---

## 6. Traceability (summary)

| Area | FR/NFR | Milan v1.2 | Entity model | Plan milestone |
|------|--------|-----------|--------------|----------------|
| Discovery | FR-DISC-\* | Section 5.2 | `adp`, ENTITY | M-B2 -- processor (Section 2.0) |
| Enum/Control | FR-ENUM/CTRL | Section 5.3–5.4 | full descriptor tree | M-B3, processor AECP uCPU plus the builder-generated image copied by bare-metal firmware; the served inventory and mandatory gaps are listed in Section 2.0 |
| MVU | FR-MVU-\* | Section 5.4.3 | `milan_mvu` | M-B3 -- **NOT IMPLEMENTED**, no `protocol_id` recognised (Section 2.0) |
| Connection | FR-CONN-\* | Section 5.5 | STREAM_\*, CBS CSR | M-B4 -- processor; fast-connect/persistence **NOT MET** |
| MAAP/SRP | FR-MAAP/SRP | Section 5.6 | STREAM_\*, classifier/CBS | M-B5 -- MAAP in fabric, SRP on the processor |
| Time/clock | FR-CLK-\* | Section 5.7 | CLOCK_DOMAIN/SOURCE, CRF | M-A5, M-B4 |
| Streaming | FR-STR-\* | Section 6 | STREAM_INPUT/OUTPUT | (D5) |
| QoS | FR-QOS-\* | 802.1Q/Qav |  -  (HW) | M-A5 |
| Scale-up | NFR-SCUP-\* |  -  | small ↔ full JSON | Section A/Section B params |
| Scale-out | NFR-SCOUT-\* |  -  | fabric contexts / replicated endpoint | Section 4 |

## 7. Verification approach
- **HW leaf blocks:** Verilator self-checking harnesses (CBS, classifier, PTP,
  CSR, the AAF/CRF chain). **The 13 suites that covered the deleted control
  plane — aecp, acmp, adp, lwsrp and their siblings — are deleted with it**;
  the processor's own verification lives in the pinned submodule, and the
  datapath-level coverage is `tb/verilator/milan_dp`.
- **Integration/interop:** Hive + `srcs/the-private-test-repo/controller/avdecc_l2.py`
  (ADP and ACMP; on AECP, GET_COUNTERS serves the declared counter banks and
  the tracked flow loads the descriptor image before entity enable), and fabric
  gPTP wire/CSR/publication checks.
- **PDU byte-exactness:** the AECP PDU model campaigns have a responder again.
  `aecp_read_descriptor` is a real byte-exact test **once an image is in DRAM**;
  the rest measure the echo's header discipline, which is the conformance floor
  and not command coverage. The AAF campaign survives unchanged.
- **Conformance:** the internal Milan conformance plan (bench suite). Expect
  the AECP/AEM clause rows to fail, and record them as failing -- Section 2.0 is the
  reason, not an excuse to re-grade them. **A conformant refusal is not a pass**:
  a row asking what a command DOES is not answered by the fact that it replies.
- **Scale:** repeat the suite at every claimed fabric stream/channel/rate shape
  and at any future replicated-port profile.
