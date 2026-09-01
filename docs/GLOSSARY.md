# Glossary

Current product terminology for the bare-metal Milan v1.2 end station.

## Contents

- **[AVB, TSN, and Milan](#avb-tsn-and-milan)** — Expands the networking and profile terms used throughout the repository.
- **[Time synchronization](#time-synchronization)** — Defines PHC, BMCA, gPTP state and timestamp-uncertainty vocabulary.
- **[FPGA and interfaces](#fpga-and-interfaces)** — Covers RTL, AXI, streaming, clock and board-interface terminology.
- **[Product architecture](#product-architecture)** — Names the bare-metal firmware, fabric and protocol-processor ownership layers.
- **[Evidence shorthand](#evidence-shorthand)** — Explains simulation, synthesis, board and external-validation labels.

## AVB, TSN, and Milan

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
<!-- milan-feature-status:end -->

| Term | Meaning |
|---|---|
| **AVB** | The IEEE 802.1 family for synchronized, bounded-latency media over Ethernet. |
| **TSN** | Time-Sensitive Networking, the broader family containing AVB functions. |
| **Milan** | The professional-audio interoperability profile targeted at version 1.2. |
| **AVTP** | IEEE 1722 media transport carrying presentation timestamps and validity fields. |
| **AVDECC** | IEEE 1722.1 discovery, enumeration, control, and connection management. |
| **ADP** | Entity discovery and advertise/depart protocol, implemented by the protocol processor. |
| **AECP/AEM** | Enumeration/control protocol and its descriptor model. The processor serves the command inventory recorded in the feature ledger. |
| **ACMP** | Stream connection protocol. The processor publishes settled binding records to the fabric. |
| **SRP/MSRP/MVRP** | Reservation and VLAN registration protocols implemented by the protocol processor. |
| **MAAP** | Multicast address acquisition for AVTP stream destinations. |
| **AAF** | AVTP Audio Format transport for sampled audio. |
| **CRF** | Clock Reference Format transport used to convey media-clock timing. |
| **CBS** | Credit-Based Shaper for stream-reservation traffic classes. |
| **Talker / Listener** | AVTP stream source / sink. |
| **Presentation time** | The gPTP time at which a listener renders media. |
| **PCP / VID** | VLAN priority code point / VLAN identifier. |
| **Structural zero** | A documented unsupported or ownerless field tied to zero, distinguishable from an implemented engine reporting no events. |

## Time synchronization

| Term | Meaning |
|---|---|
| **gPTP** | IEEE 802.1AS generalized precision time protocol. The fabric plane is the sole product owner. |
| **PHC** | The in-fabric PTP Hardware Clock from which event and presentation timestamps are drawn. |
| **Grandmaster (GM)** | The selected source of domain time. |
| **Peer delay (pdelay)** | Link-delay measurement between adjacent time-aware ports. |
| **asCapable** | Qualification that an adjacent link can participate in the time-aware system. |
| **PathTrace** | Ordered clock identities traversed by the selected Announce. |
| **`tu`** | AVTP timestamp-uncertain flag. It asserts when fabric synchronization is not trustworthy and through the required holdover. |
| **Option OFF** | Verification-only `GPTP_PLANE_EN_P=0` elaboration with zero gPTP owners, zero publications, and `tu=1`. It is not a product image. |

## FPGA and interfaces

| Term | Meaning |
|---|---|
| **Artix-7 / xc7a100t** | FPGA family and device used on the AX7101 product board. |
| **LUT / FF / BRAM** | Logic table, flip-flop, and block-memory resources. |
| **WNS / TNS / WHS** | Setup and hold timing verdicts; negative slack is a failure. |
| **CDC** | Clock-domain crossing implemented with a reviewed synchronizer, toggle, handshake, or asynchronous FIFO. |
| **AXI4 / AXI-Lite / AXIS** | Burst memory, register-access, and streaming interfaces. |
| **CSR** | Control/status register. The Milan window starts at `0x9000_0000`; LiteX peripheral CSRs occupy a separate space. |
| **GMII** | Parallel MAC-to-PHY interface used by the product board. |
| **MDIO** | Clause-22 PHY management interface. |
| **FCS** | Ethernet frame check sequence. |
| **MTU** | Maximum frame payload size; the product uses 1500 bytes. |
| **Verilator** | Simulator used by the self-checking RTL benches. |
| **Yosys / sv2v** | Open synthesis/lowering flow used by the portability gate. |
| **Vivado** | Tool used for final Xilinx implementation and bitstream generation. |

## Product architecture

| Term | Meaning |
|---|---|
| **Bare-metal firmware** | RV32I program that owns boot policy, identity, CSR setup, diagnostics, and persistence orchestration. |
| **VexiiRiscv** | Cacheless RV32I softcore used by shipping configurations. |
| **LiteX** | SoC construction framework used to integrate the softcore, memories, UART, flash, and Milan datapath. |
| **Protocol processor** | Pinned fabric engine implementing IEEE 1722.1 and SRP, wrapped by `KL_pp_shadow`. |
| **Class-D face** | Per-cycle processor publication bundle consumed directly by the datapath. |
| **Descriptor image** | Generated AEM image loaded into the processor's descriptor memory before entity enable. |
| **Publication bank** | Atomic fabric-owned GM, parent, path, delay, sync, asCapable, and related status snapshot. |
| **QSPI flash** | Nonvolatile device holding bitstream, firmware, descriptors, and the state region required by #70. |

## Evidence shorthand

| Term | Meaning |
|---|---|
| **Desk evidence** | Deterministic simulation, generation, lint, elaboration, and synthesis checks on one exact source candidate. |
| **Physical evidence** | Booted-board result tied to exact source, generated image, topology, capture point, method, and raw artifacts. |
| **#117** | Two-board fabric-gPTP, GM transition, conformance, latency, and audio acceptance campaign. |
| **#70** | Persistent-state implementation and power-cut acceptance. |
| **#259** | Bare-metal-only product and repository migration. |
