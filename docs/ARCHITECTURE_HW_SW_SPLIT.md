# Fabric and bare-metal firmware ownership

Mark II selects each control protocol's placement at build time.
Its default is bare-metal control through packet mailboxes.
The all-fabric build remains supported.
It remains the shipping default at VERSION `0x0002_0060`.
The default flips only after F2 to F5 pass acceptance.
That includes their suites, all streams, counters and audio soak.
Requirement approval precedes the flip.

The [#664 ownership decision](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009576644)
and [service-budget ruling](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009675758) govern this contract.
F0 and F1 are implemented foundations, not a shipping split.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gptp.fabric-product-owner` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. Ownership rule](#1-ownership-rule)** -- Assigns one state owner per function and placement.
- **[2. Boot sequence](#2-boot-sequence)** -- Orders image validation, saved-state apply and entity enable.
- **[3. Fabric publication boundary](#3-fabric-publication-boundary)** -- Keeps gPTP and media observations coherent for either control owner.
- **[4. Verification-only option OFF](#4-verification-only-option-off)** -- Separates ownerless gPTP test hardware from supported control placements.
- **[5. Known incomplete boundaries](#5-known-incomplete-boundaries)** -- Distinguishes merged foundations from integration and physical proof.
- **[6. Verification boundary](#6-verification-boundary)** -- Defines unit tests, service hooks and the acceptance sequence.
- **[7. Version and default flip](#7-version-and-default-flip)** -- Reserves major 3 for split images and pins the landing checks.

## 1. Ownership rule

Each selected function has exactly one authoritative state owner.
Selection is per function, at build time, never concurrent ownership.
Both placements preserve the same wire semantics and normative timing.
Mixed placements preserve cross-function response, state and notification ordering.
Configuration selects placement without rewriting protocol code.

| Function | All-fabric placement | Mark II default placement | Shared contract |
|---|---|---|---|
| ADP | protocol processor | bare-metal core | Advertise/discover/depart; no independent advertiser conceals a stopped core |
| ACMP | protocol processor | bare-metal core | Binding and probing state; commit applied state before successful responses |
| AECP/AEM and MVU | protocol processor | bare-metal core | Descriptor serving, commands, locks, unsolicited notifications and counter serving |
| MAAP | selected fabric allocator | bare-metal core | Allocate, defend, announce and withdraw addresses |
| SRP (MRP, MSRP, MVRP) | protocol processor | bare-metal core using lwSRP | Registration and admission decisions; coherent licence updates |
| Boot, identity, diagnostics and saved-state orchestration | bare-metal core | bare-metal core | Generated image identity and transactional persistence |
| Framing, timestamps and ingress filtering | fabric | fabric | Only relevant control input reaches the core; rate limits bound load |
| gPTP, PHC, servo, BMCA and peer delay | fabric | fabric | One time owner, atomic public state |
| AVTP/AAF/CRF, physical audio and media clocks | fabric | fabric | Audio and gPTP deadlines have no firmware service dependency |
| Media counters and admission enforcement | fabric | fabric | Coherent observations and applied licences; firmware serves protocol views |
| Control timer deadlines and elapsed-time source | fabric | fabric, posting events to the core | Firmware handles events within the control-service bound |

The protocol owner holds state, rather than a second writable replica.
Fabric observations remain authoritative even when AECP serves their counters.
State-apply acknowledgements must precede responses promising that state.
Response transmission must precede the unsolicited notification it causes.
This includes ACMP responses followed by AECP notifications (#653).
Milan v1.2 5.4.5.2 and IEEE 1722.1-2021 7.5.2 remain normative.

[NFR-SCOUT-01..03](reference/FR_NFR.md#34-fabric-scale-out-and-future-ports)
constrain capacity, placement and service timing.
One cacheless RV32I control hart remains the release target.
Media capacity grows through fabric contexts, channels and sample rates.
Protocol state grows through static pools sized from the entity model.
Every supported shape must meet the same service bound.

### Packet mailbox interface

[F0's design](design/MAILBOX_SPLIT.md) defines several packet mailboxes.
Its [generated contract](reference/MAILBOX_CONTRACT.md) defines the byte-exact interface.
The single source is [the mailbox YAML](../sw/mailbox/mailbox.yaml).
It generates the fabric skeleton/package, C header and reference documentation.
Those outputs must remain mutually consistent.

Each protocol channel has receive and transmit block RAM rings.
Counter writes act as doorbells; one interrupt combines enabled causes.
The host uses 32-bit accesses only, with no DMA.
Records publish atomically after their payload words are complete.
TX records leave in commit order across channels, using `SEQ`.
This preserves response-before-notification order despite egress stalls.

An ingress filter applies protocol-specific acceptance and rate limits.
It delivers only frames relevant to the selected control function.
The fabric also posts timer, GM-change, link and tick events.
Coalesced events retain their defined state and elapsed tick count.
The [F0 contract](design/MAILBOX_SPLIT.md#rings-records-and-events) defines those details.

A publication block carries firmware-owned class-D state to the fabric.
It holds the talker DA gate, each sink's bound state and stream_id, and the SRP licence, idle slope and Domain.
Each owner writes a value before the response that promises it.
The split placement's datapath reads the block through a build-time selection, never a runtime multiplexer.
The [publication contract](design/MAILBOX_SPLIT.md#the-publication-block) defines its layout and writers.

Each host supplies a bus adapter to the same window.
F0 implements Wishbone and AXI4-Lite adapters.
A hard-core AXI4 host requires its own conforming adapter.
Portable C11 protocol modules use a small HAL.
Target MMIO and host mailbox models implement the same seam.
Doorbell ordering requires device memory or the platform's explicit barrier.
No compiler intrinsics belong in protocol code.

### Bare-metal-first firmware

The [bare-metal directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5992455815)
requires one event loop, no OS, heap or dynamic threads.
Mailbox interrupts, doorbells and fabric timer events drive bounded passes.
All state and allocations come from model-sized static pools.
SRP integrates lwSRP through its ports, rather than a private rewrite.
Integration fixes belong upstream; the project tests its adapter.
The fabric centisecond event drives the timer port without lost ticks.

The [control firmware](../sw/firmware/ctrl/README.md) supplies F0's HAL and ADP slice.
The [saved-state store](../sw/firmware/ctrl_nvm/README.md) supplies F1's separate flash port.
They share a monotonic elapsed-time requirement, independent of PHC steps.
NVM work must fit the event loop's total service bound.

## 2. Boot sequence

1. Configure the FPGA from the paired bitstream.
2. Keep ADP advertising and AECP service disabled during validation.
3. Program generated identity and static product policy.
4. Verify the paired generated AEM image and its CRC.
5. Install it for the selected AECP owner's descriptor access.
6. Read and validate saved state before releasing AECP.
7. Apply accepted bindings, then the model-validated D3 state transaction.
8. Release AECP only at an accepted boot terminal.
9. Start ADP only when AECP and ACMP can accept requests.

Milan v1.2 5.6.1 requires that final readiness ordering.
The current all-fabric image provisions the processor descriptor window.
It restores through the processor and the shipping NVM backend.
For the split, F1's [boot contract](../sw/firmware/ctrl_nvm/README.md#boot)
validates KLJ2 slots and applies state through the state port.
Bindings precede formats, maps, their settle step and names.
A failed D3 apply rolls back that transaction to defaults.
An unproven model or failed rollback remains CLOSED.
COMPLETE, DEFAULTS and BLANK permit AECP release as specified there.
An UNREAD slot holds write-back; it supplies no trusted generation.

Changed persisted state is latched from its authoritative owner.
F1 writes the inactive slot and verifies the committed container.
Its [write-back contract](../sw/firmware/ctrl_nvm/README.md#write-back)
preserves complete-old-or-new recovery across power loss.
The existing capture bound and boot deadlines remain integration obligations.
F1 is not yet linked into a shipping image.

The gPTP engine and PHC run independently of descriptor enumeration.
A missing AEM image does not create another time owner.

## 3. Fabric publication boundary

The fabric commits its selected gPTP state atomically.
GM, parent, PathTrace, delay, sync and asCapable share that transaction.
CSR and either protocol placement consume the same authoritative snapshot.
ADP and AECP answers cannot mix generations of that snapshot.
The selected AECP owner generates corresponding Table 5.22 notifications.

The publication feeds:

- CSR `0x624/0x628`, `0x6E4`, `0x730/0x734`, `0x77C`, and `0x7E4`;
- ADP and AECP `GET_AVB_INFO` / `GET_AS_PATH` answers;
- observed-change notification signatures; and
- the fabric AVTP `tu` decision used by every talker.

Paired CSR reads retain the documented snapshot semantics.
Path count and tail remain one generation during protocol serving.
Firmware cannot manufacture live gPTP health by writing a publication.

## 4. Verification-only option OFF

`GPTP_PLANE_EN_P=0` remains verification-only, with no product image.
This is independent of control-protocol placement.
Both supported control placements retain the product fabric gPTP owner.

In the ownerless test form:

- GM, parent, PathTrace and peer delay read zero;
- sync and asCapable are zero;
- AVTP `tu` is one;
- retired publication writes remain inert; and
- writes cannot create notifications, counters or ownership changes.

## 5. Known incomplete boundaries

F0's `--ctrl-mailbox` switch is default-off.
Its datapath inputs remain idle until protocol integration connects them.
The publication block's outputs remain unread until the placement switch selects them.
F1's flash and state ports await integration with those owners.
Access counts and model time do not prove target service latency.
F2 to F5 must close the [timing hooks](reference/FR_NFR.md#342-control-service-test-hooks).

The all-fabric backend remains partially implemented under #70.
Physical gPTP acceptance remains #117.
Media-clock bench acceptance remains with #74 and #629.
Timestamp-latency measurements remain #64 and #213.
The [feature ledger](reference/MILAN_FEATURE_STATUS.md) records current implementation status.
The Mark II requirements do not upgrade those verdicts.

## 6. Verification boundary

The [unit-test directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385)
applies to all Mark II software.
Protocol code remains C11; tests use GoogleTest and GoogleMock.
C++ tests include C interfaces through `extern "C"`.
Mocks cover the mailbox HAL, flash port and lwSRP adapter.
Every public function, state transition and error return requires coverage.
CI records gcov line and branch coverage for each change.
The protocol and saved-state target is 100% branch coverage.
Each exclusion needs a reason in the relevant test README.
A ratchet refuses coverage reductions.
The test listener prints `checks: N   failures: M`.
Existing mutation arms remain graded.
lwSRP's upstream suites run unchanged at the pinned revision.
Coverage fixes for that upstream code go upstream.

F0 and F1 merged with their existing tests and mutations.
FT adds the framework, tally listener, coverage gate and CI wiring.
FT also ports F0/F1 tests before F2 to F5 begin.
This document does not claim that FT has landed.

Each moved path must pass its named NFR-SCOUT-03 hook.
Host-model checks must include planted late-service and ordering defects.
Target measurements must cover the full composition at each supported shape.
Bench acceptance must exercise all streams, counters and the audio soak.
All-fabric and mixed placements retain equivalent PDU and state-transaction behavior.
The [#640 latency ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268)
also preserves restart, fast-connect and saved-state capture bounds.

Documentation gates establish document consistency, not those runtime claims.
The [verification contract](../CONTRIBUTING.md#3-verification-bar) remains applicable to implementation.
Physical acceptance needs exact image hashes and measured wire evidence.

## 7. Version and default flip

Major `0x0003` identifies only images that run the split.
Merely building the idle F0 skeleton cannot claim major 3.
An all-fabric image retains its architecture identity.
MINOR remains a flat ordinal, continuous across majors.
The split firmware string is `3.<minor>.<patch>`, derived from CSR identity.
The [VERSION policy](reference/REGISTER_MAP.md#version-is-also-what-every-atdecc-controller-is-told-2026-07-28)
remains the single source for that derivation.
This documents-only change leaves VERSION at `0x0002_0060`.

The default-flip PR must land the version chain together:

1. Record approved requirements and F2 to F5 bench evidence.
2. Select the split default and bind identity to actual placement.
3. Update the CSR version and regenerated ENTITY firmware string.
4. Pin and run all five current VERSION simulation assertions below.
5. Preserve a `VERSION >> 16` major-only assertion for each placement.
6. Update the CSR documentation, feature ledger and changelog together.
7. Run the full local and hosted implementation gates on that head.

| Current VERSION simulation | Required landing assertion |
|---|---|
| `tb/verilator/csr/sim_main.cpp` | Complete CSR version for the selected architecture |
| `tb/verilator/milan_dp/sim_main.cpp` | Integrated datapath version |
| `tb/verilator/milan_dp/sim_nxn.cpp` | Every supported stream shape's version |
| `tb/verilator/milan_dp/sim_gptp.cpp` | Product gPTP option and version |
| `tb/verilator/milan_dp/sim_prune.cpp` | Pruning cannot misidentify the selected architecture |

The assignment also names a retired major-only simulation.
That suite is absent from this base under #259's retirement.
The flip must carry its `>> 16` assertion into a live suite.
It must test major 3 for split and major 2 for all-fabric.
Do not restore a retired runtime merely to restore that assertion.
No simulation, firmware or RTL changes are made here.
