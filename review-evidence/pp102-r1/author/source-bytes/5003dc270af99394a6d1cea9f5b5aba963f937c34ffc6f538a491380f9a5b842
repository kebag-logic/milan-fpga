<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Protocol Processor, a hardware AVB/Milan control plane

A compact, deterministic **IEEE 1722.1-2021 (ATDECC) protocol processor**. It implements the
control plane of a **non-redundant Milan v1.2 PAAD** (Professional Audio AVB Device):

* ADP discovery
* Milan ACMP binding and probing
* AECP/AEM and Milan Vendor Unique execution
* an MSRP/MVRP endpoint participant

**It runs without a CPU.** A management side port carries the non-real-time plumbing, and
the integrating fabric consumes its decisions as wires.

## Start here

Pick the door that matches what you are doing. Each guide is written for that reader alone,
so you should not need the other two.

| You are | Guide | What it covers |
|---|---|---|
| Modifying a module | [HDL engineer](docs/guides/hdl-engineer.md) | conventions, block structure, shared-service contracts, running the testbenches |
| Integrating this into an SoC | [Integrator](docs/guides/integrator.md) | ports, parameters, clocking and reset, the two main-memory masters, what to reserve, what a tied-off face does |
| Bringing a device up | [Operator](docs/guides/operator.md) | what appears on the wire, what a controller sees, the bring-up ladder, every diagnostic counter |
| Browsing all three | [Guide index](docs/guides/README.md) | the three guides plus the diagram inventory |

## Diagrams

Every diagram is drawn against the landed RTL, not against the specification.

| Diagram | What it answers |
|---|---|
| [Dataflow of the landed RTL](docs/diagrams/20-rtl-dataflow.svg) | every module in the top, and how a frame moves through them |
| [The integrator's contract](docs/diagrams/21-integration-faces.svg) | every external face, with tie-off behaviour |
| [READ_DESCRIPTOR through main memory](docs/diagrams/22-aecp-descriptor-fetch.svg) | the AECP path, and what the wire shows when memory fails |
| [Bring-up ladder](docs/diagrams/23-bringup-decision.svg) | telling working from broken, one question at a time |
| [The two observable state machines](docs/diagrams/24-adp-acmp-states.svg) | advertise and listener binding, as an operator sees them |

## Repository map

| Path | What it is |
|---|---|
| [`hdl/`](hdl/README.md) | the SystemVerilog implementation: layout, rules, and the submodule consumption contract |
| [`tb/`](docs/architecture/09_verification.md) | one self-checking Verilator suite per module. Each carries its own `README.md` |
| [`docs/guides/`](docs/guides/README.md) | the three persona guides |
| [`docs/architecture/`](docs/architecture/) | the normative architecture: overview, interfaces, packet engine, ADP/ACMP/AECP/SRP engines, memory, timing, verification |
| [`docs/README.md`](docs/README.md) | documentation conventions: ID registries, figure rules, citation and editing workflow |
| [`docs/00_MILAN_COMPLIANCE_REVIEW.md`](docs/00_MILAN_COMPLIANCE_REVIEW.md) | review against Milan v1.2: gap register and requirement matrix |
| [`docs/10_RESOURCE_AND_EFFORT.md`](docs/10_RESOURCE_AND_EFFORT.md) | resource-saving and implementation-effort analysis against the reference platform |
| [`docs/traceability/MODULE_MATRIX.md`](docs/traceability/MODULE_MATRIX.md) | generated module to testbench matrix. The untested budget is zero |
| [`docs/diagrams/`](docs/diagrams/README.md) | diagram sources, exports and the toolchain |
| [`syn/ooc/`](syn/ooc/README.md) | out-of-context synthesis measurements |
| [`IEEE_1722_1_Hardware_Protocol_Processor.md`](IEEE_1722_1_Hardware_Protocol_Processor.md) | the original concept document. **Historical input, superseded.** See its own header |

## Building and checking

```sh
./scripts/run_suites.sh                  # every Verilator suite under tb/
./scripts/lint_hdl.sh                    # Verilator lint over every module, zero tolerance
make check                               # documentation gates: figures, links, matrix, freshness
python3 scripts/gen_matrix.py --check    # module to testbench matrix drift
```

The reference platform consumes this repository as a **git submodule**. The pin is only
moved to a commit where all of the above are green here first.

## Specifications targeted

| Specification | Scope |
|---|---|
| AVnu **Milan Specification, Consolidated v1.2** (Final, 2023-11-30) | non-redundant PAAD |
| **IEEE Std 1722.1-2021** (ATDECC) | the protocol this implements |
| IEEE 1722-2016, IEEE 802.1AS-2011, IEEE 802.1Q-2014 | referenced throughout |

Where Milan differs from IEEE 1722.1, **Milan wins** (Milan §5.5.2.1). Every such point is
tagged in the delta table at
[`01_overview.md` F01.4](docs/architecture/01_overview.md#fig-01-deltas).

The specification PDFs are not distributed in this repository, because they are copyrighted
documents.

## License

Licensed under the **CERN Open Hardware Licence Version 2, Weakly Reciprocal**
(CERN-OHL-W-2.0). See [`LICENSE`](LICENSE).
