# Architecture

Milan FPGA is a fabric-first Milan 1.2 end station. A small bare-metal RV32
CPU performs boot, policy setup, and diagnostics; packet protocols, gPTP, AAF,
CRF, MAAP, shaping, and physical audio movement execute in FPGA logic.

Machine-checked status rows are defined by the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `stream-input.start-stop` | `implemented` | - |
| `stream-input.stopped-crf-observation` | `implemented` | - |
| `stream-format.set` | `implemented` | - |
| `stream-info.set-acc-lat` | `implemented` | - |
| `soc.baremetal-profile` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. Product boundary](#1-product-boundary)** — The supported datapath, LiteX shell, flash, CSR, audio, and firmware surfaces.
- **[2. Data flow](#2-data-flow)** — The fabric-only ingress observations and egress-source merge at the MAC.
- **[3. Control and identity](#3-control-and-identity)** — Protocol-processor ownership and boot-time installation of the generated entity image.
- **[4. Time and media clocks](#4-time-and-media-clocks)** — Fabric gPTP discipline, published state, and the configured audio grid.
- **[5. Clock domains & CDC](#5-clock-domains--cdc)** — The principal domains, approved crossing mechanisms, and generated census.
- **[6. Persistent state](#6-persistent-state)** — Paired image updates and the still-missing protocol-state backend owned by #70.
- **[7. Verification architecture](#7-verification-architecture)** — How unit, integration, synthesis, timing, UART, and wire evidence compose.
- **[8. Where to change things (maintainability)](#8-where-to-change-things-maintainability)** — The source-of-truth locations for behavior, integration, configuration, and evidence.

## 1. Product boundary

The supported integration is `milan_datapath` inside the LiteX SoC. LiteEth
provides the MAC/PHY boundary, an AXI-Lite bridge exposes Milan CSRs, QSPI holds
the paired bitstream and AEM image, and board pins carry I2S/TDM audio. There is
one target software surface: `sw/firmware/milan_baremetal`.

## 2. Data flow

Ingress wire traffic is timestamped and split into two fabric observations.
The pre-filter media tap parses, validates, depacketizes, maps, and renders AAF.
The filtered tap lets the protocol processor observe addressed control frames.
No packet payload is delivered to target memory.

Egress AAF/CRF, MAAP, protocol-processor, and fabric-gPTP sources merge in
fabric before the MAC. The classifier/queue/CBS chain is not instantiated in
the product datapath (its only source was the retired transmit path); its CSR
words remain as write-only scratch and the blocks stay verified stand-alone.

## 3. Control and identity

The pinned protocol processor owns ADP, ACMP, AECP, and SRP. `KL_pp_shadow`
adapts its class-D and descriptor-memory interfaces to the Milan datapath.
The firmware verifies and installs the generated AEM image before enabling the
entity. `KL_maap` remains the fabric multicast allocator through
`KL_pp_maap_shim`.

## 4. Time and media clocks

The fabric gPTP plane is the sole release-image PHC discipline owner. Its
published GM, parent, path, peer-delay, synchronization, AS-capable, and
time-uncertain state feeds the CSR and protocol surfaces directly. A direct
option-OFF elaboration is deliberately ownerless and inert.

AAF capture and render share a configured media grid. CRF receive/transmit
engines remain present, while selection of a recovered CRF clock is tracked as
an explicit compliance gap.

## 5. Clock domains & CDC

The principal domains are LiteX `sys`, Milan `axis_clk`, Ethernet TX/RX clocks,
the 125 MHz timestamp clock, and the audio clock. Crossings use explicit
AXI-Lite/stream adapters, `cdc_pulse`, `cdc_handshake`, `cdc_pair_fifo`, or
`ptp_csr_sync`; generated constraints must name the same clocks and false paths.
The derived crossing census in `docs/diagrams/cdc_census.*` is gated for drift.

## 6. Persistent state

The offset-zero bitstream and raw AEM slot form one release image set. The
transactional flash path verifies the installed bitstream and target artifacts,
writes the AEM image first, and commits the bitstream last. Saved protocol
state does not yet have a nonvolatile backend: the processor's NVM face remains
a blank-flash responder. Issue #70 owns the raw-flash journal implementation,
power-cut behavior, restore walk, and board evidence described in
[`../design/SAVED_STATE_FASTCONNECT.md`](../design/SAVED_STATE_FASTCONNECT.md).

## 7. Verification architecture

Focused Verilator harnesses establish cycle-accurate module contracts;
`milan_dp` establishes the complete fabric boundary. Processor-native suites
cover protocol engines, generated wire campaigns cover AAF and gPTP, Yosys
checks portability, and placed plus board evidence closes the release lane.

## 8. Where to change things (maintainability)

| Intent | Owning area | Required companion evidence |
|---|---|---|
| protocol behavior | pinned processor + `hdl/milan/KL_pp_shadow.sv` | processor suite and `pp_shadow` integration |
| gPTP ownership/publication | `gptp-processor/` + Milan CSR wiring | gPTP wire campaign, CSR and `milan_dp` option matrix |
| AAF/CRF/media routing | `hdl/ieee1722/` | focused harness plus `milan_dp` |
| queue/shaper logic | `hdl/ieee8021q/ts/` | classifier/queue/CBS suites and synthesis |
| SoC clocks, pins, flash | `sw/litex/` and platform files | elaboration, source closure, placed build, board check |
| register contract | `hdl/common/csr/` | CSR suite and regenerated register documentation |
| end-station shape | `configs/` + builder | builder tests and sweep-shape gate |

Keep policy in one owner, regenerate derived artifacts, and update the test in
the same change as the implementation.
