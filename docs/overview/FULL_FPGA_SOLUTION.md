# Full FPGA solution

The current shipping image uses the all-fabric control placement.
One bare-metal RV32 core boots and configures that image.
Mark II defaults control protocols to the core through packet mailboxes.
ADP, ACMP, AECP, MAAP and SRP remain selectable per function.
Audio, gPTP, framing, timestamps and ingress filtering remain in fabric.
All-fabric remains supported and the shipping default until F2 to F5 acceptance.
That acceptance covers all streams, counters and the audio soak.
The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) defines these requirements.
The implementation inventory below describes the current shipping build.

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
| `crf.media-clock-consumption` | `implemented` | - |
| `state.nonvolatile-persistence` | `partial` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
<!-- milan-feature-status:end -->

<!-- solution-cpu-contract:start -->
| Invocation | CPU | Harts | XLEN | Firmware | L2 bytes | Datapath clock |
|---|---|---:|---:|---|---:|---:|
| CLI defaults | `vexiiriscv` | `1` | `32` | `baremetal` | `unset` | `unset` |
| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `50 MHz` |
<!-- solution-cpu-contract:end -->

## Contents

- **[1. Included functions](#1-included-functions)** -- The protocol, time, media, shaping, identity, boot, and diagnostic functions in the release image.
- **[2. Runtime flow](#2-runtime-flow)** -- The all-fabric packet and audio paths from ingress observation to MAC egress.
- **[3. Software responsibility](#3-software-responsibility)** -- The bounded boot, provisioning, time-init, and UART duties of firmware, plus the explicit #70 persistence gap.
- **[4. Build identity](#4-build-identity)** -- How one configuration binds generated sources, bitstream, entity image, plan, and hashes.
- **[5. Performance model](#5-performance-model)** -- Why fabric timing and wire measurements, rather than firmware throughput, grade the product.
- **[6. Compliance evidence](#6-compliance-evidence)** -- The canonical ledger and layered evidence used for Milan claims.
- **[7. Board integration](#7-board-integration)** -- The AX7101 as release platform and one DUT, the retired Arty recipe, and the physical resource selections.
- **[8. Release boundaries](#8-release-boundaries)** -- What is product-supported, verification-only, or still outside the candidate.
- **[9. What remains and how to finish it - the roadmap](#9-what-remains-and-how-to-finish-it---the-roadmap)** -- The remaining protocol, media, timing, and physical acceptance work.

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
MAAP, and gPTP sources arbitrate onto MAC egress. The generic
classifier/shaper chain is not instantiated in release builds.

## 3. Software responsibility

Firmware verifies and copies the paired AEM image, establishes the PHC epoch,
enables fabric blocks, and exposes a narrow UART diagnostic surface. It
journals the processor's saved-state records A/B into flash and starts the
restore walk on every boot; issue #70 owns the writers still missing (names
and channel maps) and the power-cut proof. All protocol timers, packet
construction, media movement, and PHC discipline remain hardware-owned.

## 4. Build identity

An end-station YAML drives descriptor generation, gPTP ROM generation, fabric
shape, board pins, and the SoC command line. The bitstream, raw AEM image,
generated plan, and hashes are one candidate set. Paired-image update tooling
refuses a set whose installed or target identity cannot be proven.

<!-- solution-memory-faces:start -->
| Memory face | RTL prefix | Direction | Purpose |
|---|---|---|---|
| Descriptor memory | `desc_mem_*` | Read-only | Fetch the verified entity image |
| Response memory | `resp_mem_*` | Read-write | Build AECP responses |
| Record image memory | `nvm_mem_*` | Read-write | Keep the saved-state record image |
<!-- solution-memory-faces:end -->

## 5. Performance model

Audio payload stays on deterministic fabric paths in both placements.
Mark II control throughput must also meet NFR-SCOUT-03.
Its [service hooks](../reference/FR_NFR.md#342-control-service-test-hooks) measure worst-case firmware latency.
Timing closure and board-wire evidence remain required for release.

## 6. Compliance evidence

The canonical status is in the [Milan feature status](../reference/MILAN_FEATURE_STATUS.md)
and the protocol-validation matrix. Verilator, processor-native suites, generated wire
campaigns, Yosys, placed reports, UART grading, and external packet captures
form the evidence chain.

## 7. Board integration

AX7101 is the release platform and the one DUT; the Arty is a retired DUT whose
recipe only elaborates. Each build selects a physical Ethernet port and audio
pin shape. Clock/reset, DDR3, QSPI, LiteEth, and the Milan fabric are
integrated by `sw/litex/milan_soc.py`.

## 8. Release boundaries

The direct fabric-gPTP option-OFF shape is verification-only. It publishes no
GM, parent, path, or peer-delay state and cannot be flashed as a product image.
External physical testing and interoperability with the Milan-validated
reference peer remain separate from digital simulation evidence.

## 9. What remains and how to finish it - the roadmap

The remaining release work is tracked in the issue board, with Milan 1.2 and
its protocol dependencies at urgent priority. Physical acceptance (including
the #74 bench probe of the recovered media clock), and the persistent-state
implementation plus bench
validation require exact candidate hardware and retained raw evidence. Digital
completion must not be reported as physical closure.
