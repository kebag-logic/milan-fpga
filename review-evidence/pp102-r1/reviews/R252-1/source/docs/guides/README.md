<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Guides — pick the door that matches your job

This repository holds a hardware control plane for a Milan v1.2 audio end-station: it
speaks IEEE 1722.1-2021 ADP, ACMP and AECP on the wire, participates in MSRP/MVRP, and
publishes the result to an integrating fabric as wires and as a management side port.

There are three very different reasons to open it. Each has its own door.

| If you are… | …you want | Start at |
|---|---|---|
| **modifying a module** — changing an FSM, adding a counter, touching a package | conventions, block structure, the shared-service contracts, how to run the testbenches | [HDL engineer guide](hdl-engineer.md) |
| **dropping this into an SoC** — wiring the top into a fabric | ports, parameters, clocking and reset, the two main-memory masters, what to reserve, what a tied-off face does | [Integrator guide](integrator.md) |
| **bringing a device up** — cabling it, pointing a controller at it, working out why it is silent | what appears on the wire, what a controller sees, the bring-up ladder, what every diagnostic counter means | [Operator guide](operator.md) |

The guides are entry points, not replacements. They tell you what is true of the tree as
it stands and then hand you to the document that owns each subject.

## The layer below: the architecture specification

[`../architecture/`](../architecture/) is the normative specification — it is
HDL-agnostic and it is where clause-by-clause behaviour, transition matrices, PDU
layouts, timing constants and memory records are defined. The guides link into it
constantly. Its own reading order, ID registries and figure conventions are in
[`../README.md`](../README.md).

| Document | Owns |
|---|---|
| [01 overview](../architecture/01_overview.md) | scope, top-level blocks, the Milan↔IEEE delta table, the parameter master table |
| [02 interfaces](../architecture/02_interfaces.md) | every external contract, by interface class |
| [03 packet engine](../architecture/03_packet_engine.md) | the shared RX/TX datapath, transaction records, hazard classes |
| [04 ADP](../architecture/04_adp_engine.md) | discovery — advertise and talker-discovery machines |
| [05 ACMP](../architecture/05_acmp_engine.md) | Milan binding and probing, including the authoritative listener transition matrix |
| [06 AECP](../architecture/06_aecp_engine.md) | AEM and Milan Vendor Unique execution, the µISA, counters, lock, notifications |
| [07 memory maps](../architecture/07_memory_maps.md) | the entity model, records, the side-port windows, persistence |
| [08 timing](../architecture/08_timing.md) | every timing constant and the timer-slot allocation |
| [09 verification](../architecture/09_verification.md) | verification strategy and the documentation gates |
| [10 SRP](../architecture/10_srp_engine.md) | the MSRP/MVRP endpoint participant |
| [00 compliance review](../00_MILAN_COMPLIANCE_REVIEW.md) | why the architecture looks the way it does — gap register and requirement matrix |

## Diagrams

These four are drawn against the RTL as it stands, rather than against the
specification, and each is referenced from the guide that needs it.

| Figure | Shows | Used by |
|---|---|---|
| [`20-rtl-dataflow.svg`](../diagrams/20-rtl-dataflow.svg) | every module in the top and how a frame moves through them | HDL engineer, integrator |
| [`21-integration-faces.svg`](../diagrams/21-integration-faces.svg) | the complete external contract, with tie-off behaviour | integrator |
| [`22-aecp-descriptor-fetch.svg`](../diagrams/22-aecp-descriptor-fetch.svg) | how a READ_DESCRIPTOR reaches the entity model in main memory | HDL engineer, integrator |
| [`23-bringup-decision.svg`](../diagrams/23-bringup-decision.svg) | the bring-up ladder, with the counter to read at each failure | operator |
| [`24-adp-acmp-states.svg`](../diagrams/24-adp-acmp-states.svg) | the two state machines an operator can observe live | operator |

Diagram sources, formats and the toolchain are described in
[`../diagrams/README.md`](../diagrams/README.md).

## The rule these guides follow

**The tree wins.** Where a guide and the RTL disagree, the RTL is right and the guide is
a defect — report it. Where something could not be established from the RTL or from a
standard, the guides say so rather than writing plausible prose. Divergences between the
specification documents and the landed RTL that are known today are listed in the
[HDL engineer guide](hdl-engineer.md#9-where-the-specification-and-the-tree-still-disagree).
