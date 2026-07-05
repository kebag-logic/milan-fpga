# Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)

**System:** a small **Milan v1.2** audio endpoint (PAAD — Professional Audio AVB
Device) — a **stereo (2-channel) talker + listener at 48 kHz** — implemented on
the fully-FPGA RISC-V platform (VexiiRiscv + LiteX on Alinx AX7101; NaxRiscv historical), designed to
**scale up** (more channels / streams / sample rates) and **scale out** (more than
one softcore).

- **Milan v1.2 → FR/NFR dependency matrix (why each is necessary):** [`MILAN_V12_DEPENDENCY_MATRIX.md`](MILAN_V12_DEPENDENCY_MATRIX.md)
- **Baseline entity:** [`avdecc/milan-v12-entity-small-48k.json`](../avdecc/milan-v12-entity-small-48k.json)
- **Full/scaled entity:** [`avdecc/milan-v12-entity.json`](../avdecc/milan-v12-entity.json) (8-ch, 48/96/192 kHz)
- **Platform & phasing:** [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md)
- **HW AEM/AECP design:** [`../aem-and-aecp.md`](../aem-and-aecp.md)

Requirement keywords per RFC 2119 (**MUST / SHOULD / MAY**). Each requirement has a
**priority** (M=MUST, S=SHOULD, C=MAY), a **source**, and a **verification method**
(T=test, A=analysis, D=demonstration, I=inspection).

---

## 1. Scope, actors, and the baseline system

### 1.1 Baseline (the "small" endpoint)
One entity, one network port, on **one softcore**:

```
   Controller (Hive / avdecc_l2.py)                Media (PipeWire / UAC2)
            │  1722.1 AVDECC (L2)                          │ audio
            ▼                                              ▼
   ┌───────────────────────── AX7101 (xc7a100t) ────────────────────────┐
   │  VexiiRiscv core0 + Linux                                          │
   │   • PipeWire module-avb: ADP/AECP/ACMP/MAAP + AVDECC entity        │
   │   • OpenAvnu mrpd: MSRP/MVRP   • linuxptp: gPTP (802.1AS)          │
   │   • kl-eth driver: PHC, HW timestamps, CBS offload                 │
   ├───────────────────────────────────────────────────────────────────┤
   │  FPGA datapath (HW): RGMII MAC ─ 802.1Q classifier ─ 802.1Qav CBS  │
   │                       ─ PTP timestamp ─ (AVTP talker/listener)     │
   └───────────────────────────────────────────────────────────────────┘
                                   │ RGMII 1 GbE
                                   ▼  AVB/TSN network (bridge)
```
Baseline stream profile, 48 kHz, 32-bit, Class A (2 ms, 8000 pkt/s), + a CRF
media-clock stream:
- **Talker:** 1 AAF source, **fixed stereo (2 ch)** — "stereo" is a talker property.
- **Listener:** 1 AAF sink, **format-adaptive** — advertises the Milan Base Audio
  Formats (1/2/4/8 ch @48 kHz) and adapts `current_format` to the connected talker
  via `SET_STREAM_FORMAT` (Milan v1.2 §5.4), rendering the mapped stereo subset.

### 1.2 Scaling parameters (referenced throughout)
| Param | Meaning | Baseline | Scale-up target | Scale-out lever |
|-------|---------|----------|-----------------|-----------------|
| `P_CH` | channels per stream | 2 | 8 → 64 | — |
| `P_SI` / `P_SO` | stream sinks / sources | 1 / 1 | 8 / 8 | per-core streams |
| `P_SR` | sample-rate set | {48k} | {48,96,192k} | — |
| `P_CORES` | RISC-V softcores | 1 | 1 (faster) | **2 … N** |
| `P_PORTS` | AVB interfaces / entities | 1 | 1 | **2 … N** (scale-out) |

### 1.3 Actors
AVDECC **Controller**; peer **Talker**/**Listener** entities; **802.1AS**
grandmaster/bridge; **SRP** bridge; local **media** app.

---

## 2. Functional Requirements (FR)

### 2.1 Discovery — ADP  *(1722.1-2021 §6; Milan v1.2 §5.2)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-DISC-01 | The entity MUST advertise `ENTITY_AVAILABLE` ADPDUs and re-advertise within `valid_time`, incrementing `available_index` on every state change. | M | T |
| FR-DISC-02 | The entity MUST answer `ENTITY_DISCOVER` (global and targeted) with an advertisement. | M | T |
| FR-DISC-03 | The entity MUST send `ENTITY_DEPARTING` on shutdown / link down. | M | T |
| FR-DISC-04 | Advertised fields (`entity_id`, `entity_model_id`, capabilities, talker/listener counts, `gptp_grandmaster_id`, `identify_control_index`, `interface_index`) MUST equal the ENTITY descriptor in the entity model. | M | T,I |
| FR-DISC-05 | `entity_id` MUST be an EUI-64 derived from the AVB_INTERFACE MAC and be stable across reboots. | M | A |

### 2.2 Enumeration & control — AECP/AEM  *(1722.1-2021 §7,§9; Milan v1.2 §5.3–5.4)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-ENUM-01 | The entity MUST serve every descriptor in the model via `READ_DESCRIPTOR`, byte-matching the JSON entity model. | M | T |
| FR-ENUM-02 | The AEM descriptor tree MUST include the Milan-mandatory set: ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT (AAF + CRF), STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN, CLOCK_SOURCE, STREAM_PORT_IN/OUT, AUDIO_CLUSTER, AUDIO_MAP, CONTROL(IDENTIFY), LOCALE, STRINGS. | M | I |
| FR-CTRL-01 | `ACQUIRE_ENTITY` and `LOCK_ENTITY` MUST be supported with the Milan timeouts; a locked entity MUST reject conflicting SETs with `ENTITY_LOCKED`. | M | T |
| FR-CTRL-02 | `GET/SET_CONFIGURATION`, `GET/SET_NAME`, `GET/SET_STREAM_FORMAT`, `GET/SET_CLOCK_SOURCE`, `SET_SAMPLING_RATE` MUST be supported for the descriptors that expose them (per the model's `dynamic`/`nonvolatile` fields). | M | T |
| FR-CTRL-03 | `REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION` MUST be supported for ≥ 16 controllers; state changes MUST emit unsolicited responses to registered controllers. | M | T |
| FR-CTRL-04 | `GET_COUNTERS` MUST return the 1722.1-2021/Milan counter sets for STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE (see model `counters`), throttled ≤ 1/s. | M | T |
| FR-CTRL-05 | `GET_DYNAMIC_INFO` (fast enumeration) SHOULD be supported. | S | T |
| FR-CTRL-06 | AECP MUST validate `control_data_length`, `message_type=AEM_COMMAND`, and target `entity_id`; malformed/unsupported commands MUST return the correct AECP status (`NOT_IMPLEMENTED`, `BAD_ARGUMENTS`, `ENTITY_LOCKED`, …). | M | T |

### 2.3 Milan Vendor Unique — MVU  *(Milan v1.2 §5.4.3)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MVU-01 | The entity MUST implement the MVU protocol (`protocol_id 00-1B-C5-0A-C1-00`) and answer `GET_MILAN_INFO` with `protocol_version`, `features_flags`, `certification_version`. | M | T |
| FR-MVU-02 | `GET/SET_SYSTEM_UNIQUE_ID` and `GET/SET_MEDIA_CLOCK_REFERENCE_INFO` MUST be supported. | M | T |
| FR-MVU-03 | `features_flags.MILAN_REDUNDANCY` MUST report 0 (redundancy out of scope). | M | I |

### 2.4 Connection management — ACMP  *(1722.1-2021 §8; Milan v1.2 §5.5)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-CONN-01 | The entity MUST support `CONNECT_TX/RX`, `DISCONNECT_TX/RX`, `GET_TX/RX_STATE` as talker and listener. | M | T |
| FR-CONN-02 | On a successful connection the entity MUST program the HW datapath: classifier queue for the stream's VLAN/PCP and CBS idleSlope/hi/lo for the reservation. | M | T |
| FR-CONN-03 | ACMP MUST implement the Milan **fast-connect** / state-restore behavior (re-establish saved connections on power-up/link-up). | M | T |
| FR-CONN-04 | Connection state MUST persist (nonvolatile) across reboot for fast-connect. | S | T |

### 2.5 Addressing & reservation — MAAP, SRP  *(1722 Annex B; 802.1Qat/Qak; Milan §5.6)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MAAP-01 | The talker MUST allocate stream destination multicast MACs via MAAP (PROBE/DEFEND/ANNOUNCE) and defend them. | M | T |
| FR-SRP-01 | The entity MUST register/deregister SRP (MSRP) Talker Advertise / Listener Ready and reserve bandwidth for Class A streams. | M | T |
| FR-SRP-02 | The entity MUST register the stream VLAN via MVRP. | M | T |
| FR-SRP-03 | On reservation grant the CBS shaper MUST be configured to the reserved idleSlope; on failure the stream MUST NOT transmit. | M | T |

### 2.6 Time & media clock — gPTP, CRF  *(802.1AS; 1722-2016 §10; Milan §5.7)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-CLK-01 | The entity MUST run 802.1AS gPTP as a time-aware endpoint (Class A), sync to the grandmaster, and report GM changes. | M | T |
| FR-CLK-02 | The PHC MUST be disciplined from a fixed 125 MHz free-running clock (REQ-PTP-07), independent of link speed. | M | A,T |
| FR-CLK-03 | The media clock MUST be selectable (CLOCK_DOMAIN → CLOCK_SOURCE) among Internal, input-stream (AAF), and CRF. | M | T |
| FR-CLK-04 | As a media-clock talker the entity MUST source a CRF stream; as a follower it MUST recover media clock from CRF or the input stream. | M | T |
| FR-CLK-05 | HW ingress/egress timestamps MUST be captured at the GMII SFD and exposed to the driver for `SO_TIMESTAMPING`. | M | T |

### 2.7 Streaming — AVTP AAF talker/listener  *(1722-2016 §7; Milan §6)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-STR-01 | The talker MUST encapsulate `P_CH`-channel AAF PCM (48 kHz, 32-bit, 6 samples/frame, Class A) with a valid AVTP presentation time = capture time + offset. | M | T |
| FR-STR-02 | The listener MUST de-encapsulate AAF, validate `avtp_timestamp`, de-jitter to presentation time, and render at the media clock. | M | T |
| FR-STR-03 | The **listener MUST be format-adaptive**: STREAM_INPUT MUST advertise every supported format (the Milan Base Audio Formats, `number_of_formats > 1`) and set its `current_format` to the **connected talker's** format via `SET_STREAM_FORMAT` at connection — it MUST NOT be fixed. A received AAF AVTPDU MUST match the adapted `current_format` (subtype/format/nsr/bit-depth/channels/sparse); mismatches MUST count `UNSUPPORTED_FORMAT`. | M | T |
| FR-STR-03a | The **talker** sources a **fixed** format (this device: stereo/2 ch); "stereo" is a talker property only. A talker with multiple producible formats MAY list them, but the transmitted format is fixed per connection. | M | I,T |
| FR-STR-03b | When adapting to a talker with more channels than the device renders, the listener MUST render the mapped subset (AUDIO_MAP) and MUST still lock/validate the full advertised format. | M | T |
| FR-STR-04 | The listener MUST maintain the STREAM_INPUT counters (MEDIA_LOCKED/UNLOCKED, LATE/EARLY_TIMESTAMP, SEQ_NUM_MISMATCH, UNSUPPORTED_FORMAT, …) and recover from stream faults (MEDIA_RESET) per Milan. | M | T |
| FR-STR-05 | Baseline: `P_SI=1`, `P_SO=1`, talker `P_CH=2`, listener advertises the base set; the design MUST be parameterized so `P_CH`, `P_SI`, `P_SO`, `P_SR` scale without protocol changes (see §4). | M | I,A |

### 2.8 QoS datapath — 802.1Q / 802.1Qav  *(already in HW)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-QOS-01 | Frames MUST be classified by PCP into traffic classes/queues (programmable tables) with Class A → its shaped queue. | M | T |
| FR-QOS-02 | The CBS (802.1Qav) MUST shape SR queues to their idleSlope with hi/lo credit; non-SR traffic MUST use strict priority (unshaped). | M | T |
| FR-QOS-03 | Σ idleSlope of shaped queues MUST NOT exceed 75 % of port rate. | M | A,T |

### 2.9 Management  *(Milan §5.3.3.10)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-MGT-01 | The IDENTIFY CONTROL MUST put the device into identification mode while its value ≠ 0. | M | T |
| FR-MGT-02 | Names (entity/group/config) MUST be settable and persisted; factory reset MUST restore defaults. | S | T |

### 2.10 Host Linux driver  *(Phase 7 / `REQ-DRV-*`; needs a kernel tree — not buildable in this repo)*

The `kl,dma-ether` platform net driver (`../kl-linux-drivers`). Extends the existing
`REQ-DRV-01..08` with the explicitly-requested NAPI/XDP/PTP/ethtool surface.

| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-DRV-N1 | RX/TX MUST use **NAPI** poll (IRQ→poll, budgeted `napi_poll`, GRO on RX) over the fabric DMA rings; per-queue NAPI contexts for the N HW queues. | M | T |
| FR-DRV-N2 | The netdev MUST expose the **N HW queues** as real TX/RX queues (`netif_set_real_num_{tx,rx}_queues`), so `tc mqprio`/CBS map to hardware. | M | T |
| FR-DRV-X1 | The driver MUST support **XDP**: `ndo_bpf`/`ndo_xdp_xmit`, the `XDP_{PASS,DROP,TX,REDIRECT,ABORTED}` actions, page-pool RX buffers, and headroom for `bpf_xdp_adjust_head`. | M | T |
| FR-DRV-X2 | **AF_XDP zero-copy** (`XDP_ZEROCOPY`, `xsk_pool` per queue) SHOULD be supported for kernel-bypass RX/TX to the media plane. | S | T |
| FR-DRV-P1 | The driver MUST register a **PHC** (`ptp_clock_info`: `gettimex64`/`settime64`/`adjfine`/`adjtime`, `enable` for PPS/perout) backed by the `0x500` PTP CSRs; `gettimex64` MUST return the paired host/PHC crosstimestamp. | M | T |
| FR-DRV-P2 | **HW timestamping** MUST be wired: `SIOCSHWTSTAMP`/`ndo_hwtstamp_set`, TX/RX descriptor timestamps from the PTP metadata stream into `skb_hwtstamps`/`skb_tstamp_tx`, and `ethtool -T` MUST advertise the PHC + `SOF_TIMESTAMPING_{TX,RX}_HARDWARE|RAW_HARDWARE`. | M | T |
| FR-DRV-E1 | **ethtool_ops** MUST provide: `get_ts_info` (`-T`), `get/set_channels` (`-l`/`-L`), `get/set_ringparam` (`-g`/`-G`), `get/set_coalesce` (`-c`/`-C`), `get_strings`/`get_sset_count`/`get_ethtool_stats` (`-S`, from the RMON CSRs), `get_link_ksettings`/`nway_reset`. | M | T |
| FR-DRV-E2 | **CBS / TSN offload** MUST be exposed via `ndo_setup_tc` (`TC_SETUP_QDISC_CBS` → the `0x400` CBS CSRs, `mqprio`; `taprio` MAY). | M | T |
| FR-DRV-C1 | **MDIO/phylib**: register the fabric MDIO bus, `phy_connect` (rgmii-id), `adjust_link` drives MAC speed/duplex + PHY-reset GPIO. | M | T |
| FR-DRV-R1 | RX **dest-MAC filter** programming MUST be exposed: `ndo_set_rx_mode` maps the multicast/unicast list onto the HW filter (MC_HASH and/or the TCAM `0x700` group). | S | T |

### 2.11 Device tree  *(Phase 8 / `REQ-DT-*`; the DT contract the driver binds to)*

The `kl,dma-ether` node describes the HW to the driver. Binding schema:
[`sw/dts/bindings/kl,dma-ether.yaml`](../sw/dts/bindings/kl,dma-ether.yaml); node:
[`sw/dts/milan.dtsi`](../sw/dts/milan.dtsi).

| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| FR-DT-01 | The node MUST set `compatible = "kl,dma-ether-0.9"` (matches the driver `of_match` + the CSR `VERSION`); the DT `reg` MUST cover the **CSR window** (`0x43C0_0000`/64 KB) and the **DMA register blocks**, each with `reg-names`. | M | I,T |
| FR-DT-02 | `interrupts` (or `interrupts-extended`) MUST list the four sources (tx-dma, rx-dma, ts-dma, csr) against the SoC interrupt controller (`&plic` on the RISC-V SoC, `&intc`/`IRQ_F2P` on Zynq), with `interrupt-names`. | M | I,T |
| FR-DT-03 | Queue counts MUST be declared: `kl,txq-cnt`/`kl,rxq-cnt` (= `CAP.num_queues`), and **`kl,shaped-queues`** MUST list which queues are CBS-shaped (a bitmap/phandle-list) — reset **`<0 1>`** (only q0,q1), consistent with `CBS_EN_RST` and `REGISTER_MAP` §0x400. | M | I,T |
| FR-DT-04 | PHY MUST be described: a child `mdio` bus with the PHY node, `phy-handle`, `phy-mode = "rgmii-id"`, and `phy-reset-gpios` (`REQ-MAC-06`). | M | I,T |
| FR-DT-05 | `local-mac-address`/`mac-address` MUST be honoured (else derive from a stable source); the driver seeds the AVDECC `entity_id` (EUI-64) from it (`FR-DISC-05`). | M | T |
| FR-DT-06 | PTP MUST be discoverable: a `ptp` sub-node or `kl,ptp` props so the driver registers the PHC on the `0x500` CSRs (fixed-125 MHz clock ref, `FR-CLK-02`). | S | I |
| FR-DT-07 | Optional `clocks`/`clock-names` for `axis`/`gtx`/`ptp`; the node MUST bind with them absent (driver falls back to the fixed rates). | S | T |
| FR-DT-08 | On the fully-FPGA build the DT MUST be generated by **LiteX** (`litex_json2dts_linux` from `--csr-json`) with the `kl,dma-ether` node overlaid. The overlay itself MUST be produced by the platform-convergent generator (`sw/dts/milan_dt.py`) from a per-platform intermediate JSON (IR, schema `sw/dts/milan-dt.schema.json`) — the LiteX extractor reads the addresses/IRQ from `csr.json`; other SoCs supply their own IR. The Xilinx `device-tree-xlnx` dtg path is retired (`REQ-DT-02`). | S | I |

---

## 3. Non-Functional Requirements (NFR)

### 3.1 Performance & real-time
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-PERF-01 | The datapath MUST sustain line-rate 1 GbE for the shaped streams without frame loss at baseline load. | M | T |
| NFR-PERF-02 | The AVTP talker/listener MUST sustain the Class A packet rate (8000 pkt/s per stream) continuously. | M | T |
| NFR-LAT-01 | End-to-end (talker capture → listener render) latency MUST meet the Milan Class A presentation-time bound (2 ms default), configurable per stream. | M | T |
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
| NFR-SCUP-01 | The entity model, driver, and datapath MUST be parameterized by `P_CH`, `P_SI`, `P_SO`, `P_SR` so a larger endpoint (e.g. 8-ch, 48/96/192 kHz — the full entity model) is a configuration change, not a redesign. | M | A,I |
| NFR-SCUP-02 | Increasing `P_CH`/`P_SR` MUST only linearly increase bandwidth, buffer, and DSP; the control plane (ADP/AECP/ACMP) MUST be unaffected. | M | A |
| NFR-SCUP-03 | FPGA resource use MUST stay within the `xc7a100t` budget at the largest supported single-node profile (document the profile that first exceeds it). | S | A |
| NFR-SCUP-04 | The AEM memory (HW 4-level, `aem-and-aecp.md`) MUST size from the JSON model at build time so more descriptors need no RTL edit. | S | I |

### 3.4 Scale-**out** (more than one softcore)  *(the key architectural NFR)*
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-SCOUT-01 | The architecture MUST support `P_CORES ≥ 2` RISC-V softcores. Two models MUST both be buildable: **(a) SMP** (NaxRiscv coherent multi-core, one Linux image) and **(b) AMP** (independent cores by plane, see §4.3). | M | A,D |
| NFR-SCOUT-02 | Work MUST partition across cores along the **control / media / time** planes with well-defined interfaces, so adding a core adds capacity without reworking protocol logic. | M | A |
| NFR-SCOUT-03 | Inter-core communication MUST use a defined shared-memory + mailbox/IPI mechanism with bounded latency; the real-time media plane MUST NOT block on the control plane. | M | A,T |
| NFR-SCOUT-04 | Shared HW resources (PHC, MAC, CSR, DMA queues) MUST be safely arbitrated across cores (single owner or lock-free per-core queues); the PHC MUST present a single coherent time to all cores. | M | A,T |
| NFR-SCOUT-05 | The design MUST also scale out to `P_PORTS ≥ 2` **independent entities** (each its own AVB_INTERFACE + softcore + entity_id), so a multi-port device is N replicated endpoints on one FPGA. | S | A,D |
| NFR-SCOUT-06 | Adding cores/ports MUST NOT change the ABI (CSR register map, entity model schema, driver DT bindings) — only instance counts. | M | I |
| NFR-SCOUT-07 | Per-core/per-stream capacity MUST be documented so the number of cores needed for a target stream/channel count is computable (a sizing formula/table). | S | A |

### 3.5 Resource, reliability, and the rest
| ID | Requirement | Pri | Ver |
|----|-------------|-----|-----|
| NFR-RES-01 | Baseline (1 core, stereo 48 k) MUST fit `xc7a100t` with headroom (target ≤ 60 % LUT) to leave room for scale-out. | M | A |
| NFR-REL-01 | A stream fault (link flap, GM change, talker loss) MUST auto-recover without a reboot; counters MUST record the event. | M | T |
| NFR-REL-02 | Watchdog/keepalive MUST detect a hung media core (AMP) and restart it without dropping the control plane. | S | T |
| NFR-OBS-01 | The system MUST expose observability: `ethtool -S`, `ethtool -T`, `ptp4l` metrics, AVDECC counters, and per-core load. | S | D |
| NFR-MAINT-01 | The entity model MUST be single-source (JSON) and shared HW/SW/test; divergence MUST be caught in CI. | M | I |
| NFR-PORT-01 | The control/media software (PipeWire module-avb, mrpd, linuxptp) MUST build for RV64 Linux; RV32 fallback MUST remain possible. | S | A |
| NFR-SEC-01 | Milan v1.2 does not mandate AEM authentication; the entity MUST advertise `AEM_AUTHENTICATION` = not-required and behave safely when unauthenticated. | M | I |

---

## 4. Scalability architecture

### 4.1 One design, three axes
- **Scale up (workload):** grow `P_CH`, `P_SI/P_SO`, `P_SR`. The JSON entity model
  is the knob — the small (stereo/48k) and full (8-ch/48-96-192k) models are the
  same schema; the driver and datapath read counts/rates from it. HW cost grows
  ~linearly with channels × sample-rate; control plane is unchanged.
- **Scale out (compute):** grow `P_CORES` — multiple NaxRiscv softcores (SMP or AMP).
- **Scale out (ports/entities):** grow `P_PORTS` — replicate the endpoint (MAC +
  interface + softcore + entity) N times on one FPGA.

### 4.2 Plane partitioning (the basis for scale-out)
| Plane | Functions | Real-time? | Baseline core | Scales to |
|-------|-----------|-----------|---------------|-----------|
| **Control** | ADP, AECP/AEM+MVU, ACMP, MAAP, MSRP/MVRP, driver mgmt | soft (ms) | core0 (Linux) | 1 core (rarely the bottleneck) |
| **Media** | AVTP talker/listener, sample transport, presentation-time, media-clock | hard (µs) | core0 (Linux RT thread) | **1 core per K streams** (AMP cores) |
| **Time** | gPTP servo, PHC discipline, CRF gen/recover | hard (µs) | core0 + HW PHC | HW-assisted; 1 core |

### 4.3 SMP vs AMP (both required by NFR-SCOUT-01)
- **SMP** — NaxRiscv coherent multi-core, one Linux image, LiteX SMP config. Media
  threads pinned to cores, `isolcpus`/`SCHED_FIFO` for determinism. *Easiest scale-up
  of stream/channel count; good for `P_CORES` 2–4.*
- **AMP** — core0 runs Linux + the whole control/time plane; cores 1..N run a
  bare-metal/RTOS **media engine** (AVTP encode/decode, DMA to the audio interface),
  no OS jitter. Control↔media via a shared-memory ring + IPI mailbox
  (NFR-SCOUT-03). *Best determinism; each media core adds a fixed stream budget.*

```
  AMP scale-out (P_CORES = 3, P_PORTS = 1):
    core0  Linux: ADP/AECP/ACMP/MAAP/MSRP + gPTP servo + driver   (control+time)
    core1  bare-metal media engine: AVTP talker/listener  stream set A
    core2  bare-metal media engine: AVTP talker/listener  stream set B
      │ shared-mem rings + IPI                     │ per-core DMA queues
      └──────────────► single coherent PHC ◄───────┘  (NFR-SCOUT-04)
                       single MAC / CBS / classifier (HW, arbitrated)
```

### 4.4 Multi-entity scale-out (`P_PORTS`)
Each port = an independent replicated slice: MAC + AVB_INTERFACE + softcore +
`entity_id` (distinct EUI-64) + its own entity model instance. Shared: the FPGA,
the build, the CSR ABI (instanced). This grows a **switchless multi-port** or
**multi-endpoint** device without touching protocol code (NFR-SCOUT-06).

### 4.5 Sizing (NFR-SCOUT-07)
Provide a table `cores = ceil(total_streams / streams_per_core)` where
`streams_per_core` is measured per media-core at each `P_CH`/`P_SR`. Populate from
benchmarks during bring-up; publish alongside the resource report.

---

## 5. Steps to comply with Milan v1.2 (procedure)

The ordered path from the baseline endpoint to a Milan-conformant device. Each step
cites the FRs it satisfies and the milestone in
[`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md).

1. **Platform up** — RISC-V Linux on the AX7101 with the HW datapath (MAC/CBS/
   classifier/PHC) and the driver (PHC, HW timestamps, CBS offload). *(M-A5)*
2. **gPTP (802.1AS)** — run `linuxptp` as a time-aware endpoint on a fixed 125 MHz
   PHC; verify ≤ 1 µs sync. *(FR-CLK-01/02, NFR-TIME-01)*
3. **Entity model** — load `avdecc/milan-v12-entity-small-48k.json`; generate the
   AEM (SW descriptors or HW 4-level memory). *(FR-ENUM-01/02)*
4. **ADP** — advertise/discover/depart with correct `available_index`. *(FR-DISC-\*)*
5. **AECP/AEM + MVU** — enumerate (READ_DESCRIPTOR byte-match), acquire/lock,
   set/get, GET_COUNTERS, GET_MILAN_INFO. *(FR-ENUM/CTRL/MVU)*
6. **Media clock** — CLOCK_DOMAIN/CLOCK_SOURCE selection; CRF talker + recovery.
   *(FR-CLK-03/04)*
7. **AVTP streaming** — AAF stereo 48 k talker + listener with presentation time.
   *(FR-STR-\*)*
8. **MAAP + SRP/MVRP** — allocate multicast, reserve Class A bandwidth, program CBS.
   *(FR-MAAP/SRP, FR-CONN-02)*
9. **ACMP** — connect/disconnect + Milan fast-connect/state-restore. *(FR-CONN-\*)*
10. **Fault behavior** — stream-interruption/redundancy-off recovery, counters,
    IDENTIFY. *(FR-STR-04, NFR-REL-01, FR-MGT-01)*
11. **Conformance** — run the AVnu Milan test plan + `srcs/milan-tests-avb`
    (`avdecc_l2.py`, `ptp4l`, `tc cbs`) and the `tsn-gen` AECP PDU checks. *(all Ver=T)*
12. **Scale** — re-run with the full entity model (8-ch, 48/96/192k) and with
    `P_CORES ≥ 2` (SMP then AMP) to prove §3.3/§3.4. *(NFR-SCUP/SCOUT)*

> Milan features intentionally **out of scope for now** (documented, not required
> here): seamless network **redundancy** (single interface), sample rates beyond
> 48/96/192 kHz, and AEM authentication.

---

## 6. Traceability (summary)

| Area | FR/NFR | Milan v1.2 | Entity model | Plan milestone |
|------|--------|-----------|--------------|----------------|
| Discovery | FR-DISC-\* | §5.2 | `adp`, ENTITY | M-B2 |
| Enum/Control | FR-ENUM/CTRL | §5.3–5.4 | full descriptor tree | M-B3 |
| MVU | FR-MVU-\* | §5.4.3 | `milan_mvu` | M-B3 |
| Connection | FR-CONN-\* | §5.5 | STREAM_\*, CBS CSR | M-B4 |
| MAAP/SRP | FR-MAAP/SRP | §5.6 | STREAM_\*, classifier/CBS | M-B5 |
| Time/clock | FR-CLK-\* | §5.7 | CLOCK_DOMAIN/SOURCE, CRF | M-A5, M-B4 |
| Streaming | FR-STR-\* | §6 | STREAM_INPUT/OUTPUT | (D5) |
| QoS | FR-QOS-\* | 802.1Q/Qav | — (HW) | M-A5 |
| Scale-up | NFR-SCUP-\* | — | small ↔ full JSON | §A/§B params |
| Scale-out | NFR-SCOUT-\* | — | replicated entity | §4 (SMP/AMP) |

## 7. Verification approach
- **HW leaf blocks:** Verilator self-checking harnesses (CBS, classifier, PTP, CSR,
  + new ADP advertiser).
- **Integration/interop:** Hive + `srcs/milan-tests-avb/controller/avdecc_l2.py`
  (ADP, GET_COUNTERS, ACMP), `ptp4l`/`phc2sys`, `tc qdisc … cbs offload`.
- **PDU byte-exactness:** `software-defined-tsn-stack/.../1722_1/aecp/*.yaml` +
  `protocols/milan/aecp_read_descriptor.yaml`.
- **Conformance:** AVnu Milan test plan.
- **Scale:** repeat the suite at the full profile and at `P_CORES=2..N` (SMP, AMP).
