# Full FPGA solution

The release architecture is a self-contained Milan fabric datapath with a
bare-metal RV32 control CPU. The CPU boots and configures the design; it does
not carry product packets or audio samples.

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
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. Included functions](#1-included-functions)** — The protocol, time, media, shaping, identity, boot, and diagnostic functions in the release image.
- **[2. Runtime flow](#2-runtime-flow)** — The all-fabric packet and audio paths from ingress observation to MAC egress.
- **[3. Software responsibility](#3-software-responsibility)** — The bounded boot, provisioning, time-init, and UART duties of firmware, plus the explicit #70 persistence gap.
- **[4. Build identity](#4-build-identity)** — How one configuration binds generated sources, bitstream, entity image, plan, and hashes.
- **[5. Performance model](#5-performance-model)** — Why fabric timing and wire measurements, rather than firmware throughput, grade the product.
- **[6. Compliance evidence](#6-compliance-evidence)** — The canonical ledger and layered evidence used for Milan claims.
- **[7. Board integration](#7-board-integration)** — The release and bring-up platforms and their physical resource selections.
- **[8. Release boundaries](#8-release-boundaries)** — What is product-supported, verification-only, or still outside the candidate.
- **[9. What remains and how to finish it - the roadmap](#9-what-remains-and-how-to-finish-it---the-roadmap)** — The remaining protocol, media, timing, and physical acceptance work.

## 1. Included functions

- IEEE 802.1AS/gPTP hardware clock, timestamping, and fabric discipline;
- protocol-processor ADP, ACMP, AECP, and SRP integration;
- fabric MAAP allocation;
- AAF talker/listener packetization, validation, channel mapping, I2S/TDM
  capture, and I2S/TDM render;
- CRF talker/listener measurement engines;
- MAC-facing classification, filtering, counters, and queue/CBS logic;
- generated AEM identity and one AXI-Lite CSR contract;
- verified QSPI boot and a diagnostic UART.

## 2. Runtime flow

Wire ingress fans out entirely in fabric: one branch feeds media parsing and
render, another feeds addressed protocol observation. Fabric AAF/CRF, control,
MAAP, and gPTP sources arbitrate onto MAC egress. The retained generic
classifier/shaper input is inactive in release builds.

## 3. Software responsibility

Firmware verifies and copies the paired AEM image, establishes the PHC epoch,
enables fabric blocks, and exposes a narrow UART diagnostic surface. It does
not yet record protocol state across power cycles; issue #70 owns the missing
backend, restore walk, and power-cut proof. All protocol timers, packet
construction, media movement, and PHC discipline remain hardware-owned.

## 4. Build identity

An end-station YAML drives descriptor generation, gPTP ROM generation, fabric
shape, board pins, and the SoC command line. The bitstream, raw AEM image,
generated plan, and hashes are one candidate set. Paired-image update tooling
refuses a set whose installed or target identity cannot be proven.

## 5. Performance model

Audio payload stays on deterministic fabric paths. The CPU's current workload
is bounded to initialization, infrequent control operations, and diagnostics;
#70 will add persistence management. Timing closure and board-wire
measurements, rather than firmware throughput, are the relevant release
metrics.

## 6. Compliance evidence

The canonical status is in the [Milan feature status](../reference/MILAN_FEATURE_STATUS.md)
and the protocol-validation matrix. Verilator, processor-native suites, generated wire
campaigns, Yosys, placed reports, UART grading, and external packet captures
form the evidence chain.

## 7. Board integration

AX7101 is the release platform and Arty is the bring-up platform. Each build
selects a physical Ethernet port and audio pin shape. Clock/reset, DDR3, QSPI,
LiteEth, and the Milan fabric are integrated by `sw/litex/milan_soc.py`.

## 8. Release boundaries

The direct fabric-gPTP option-OFF shape is verification-only. It publishes no
GM, parent, path, or peer-delay state and cannot be flashed as a product image.
External physical testing and two-board interoperability remain separate from
digital simulation evidence.

## 9. What remains and how to finish it - the roadmap

The remaining release work is tracked in the issue board, with Milan 1.2 and
its protocol dependencies at urgent priority. Physical acceptance, recovered
media-clock selection, and the persistent-state implementation plus bench
validation require exact candidate hardware and retained raw evidence. Digital
completion must not be reported as physical closure.
