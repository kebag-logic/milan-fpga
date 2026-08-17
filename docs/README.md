# Documentation index

This index contains the current entry points for the Milan TSN FPGA network
interface. Pages whose first line is `[OBSOLETE + 2026-08-16]` are historical
evidence, not current authorities. A current page may cite one only when the
link is explicitly identified as historical evidence.

The implementation is not yet fully Milan v1.2 compliant. The current audit
records verified behavior and the remaining mandatory gaps:
[Milan v1.2 audit, 2026-08-16](testing/MILAN_V12_AUDIT_2026-08-16.md).

## Start here

| Need | Current document |
|---|---|
| Understand the design | [Architecture](overview/ARCHITECTURE.md) |
| Locate each subsystem | [System domain map](overview/SYSTEM_DOMAIN_MAP.md) |
| Run a boardless check | [Quickstart](../QUICKSTART.md) |
| Assess Milan v1.2 status | [Current Milan v1.2 audit](testing/MILAN_V12_AUDIT_2026-08-16.md) |
| Find a requirement | [FR/NFR register](reference/FR_NFR.md) |
| Find a CSR | [Register map](reference/REGISTER_MAP.md) |
| Run verification | [Testing guide](testing/TESTING.md) |
| Build and deploy | [Building](integration/BUILDING.md) and [QSPI flash boot](integration/QSPI_FLASHBOOT.md) |
| Diagnose a failure | [Troubleshooting](limitations/TROUBLESHOOTING.md) |

## Current control-plane boundary

`hdl/milan/KL_pp_shadow.sv` wraps the pinned `protocol-processor` submodule and
is the only IEEE 1722.1 and SRP control plane. MAAP remains in this repository.
The exact served AECP command inventory, root integration seams, counter
coverage, and mandatory gaps are recorded in the current audit.

The entity model is served from main memory. An ordinary run of
`sw/builder/endstation_builder.py` generates review artifacts under
`sw/builder/out/`. An explicit `--write-fragment` or `--write-rtl` deployment
ownership transfer also generates the paired `aem_desc.bin`, `aem_desc.json`,
and `aem_desc.map` files in the sibling rootfs overlay when it is present.
`aemi-load` verifies and loads that image before entity enable. See the
[end-station builder](ENDSTATION_BUILDER.md) and
[architecture](overview/ARCHITECTURE.md).

## Integration and software

| Document | Purpose |
|---|---|
| [Integration guide](integration/INTEGRATION_GUIDE.md) | `milan_datapath` boundary contract |
| [Porting guide](integration/PORTING_GUIDE.md) | Non-Xilinx and non-Vivado integration |
| [Building](integration/BUILDING.md) | Board builds and build gates |
| [QSPI flash boot](integration/QSPI_FLASHBOOT.md) | Matched image deployment and recovery |
| [LiteX SoC](litex/LITEX_SOC.md) | Softcore host integration |
| [Software index](../sw/README.md) | Driver, device tree, builder, and utility entry points |
| [Register map](reference/REGISTER_MAP.md) | AXI4-Lite ABI shared by RTL and software |

## RTL and design

| Document | Purpose |
|---|---|
| [FPGA design](fpga/FPGA_DESIGN.md) | Live HDL module map |
| [Pipeline stages](fpga/PIPELINE_STAGES.md) | RX and TX datapath stages |
| [Time synchronization](design/TIME_SYNC.md) | PHC, CRF, and media-clock design |
| [MAAP fabric](design/MAAP_FABRIC.md) | MAAP engine design and PDU contract |
| [Channel map](CHANNEL_MAP_64.md) | Render and capture channel mapping |
| [End-station builder](ENDSTATION_BUILDER.md) | Declarative configuration and deployment artifacts |
| [Area budget](design/AREA_BUDGET.md) | Current resource accounting |
| [AAF latency taps](AAF_LATENCY_TAPS.md) | Per-stage latency observations |
| [Latency history ring](LATENCY_HISTORY_RING.md) | Long-term latency capture |
| [Trace logging](design/TRACE_LOGGING.md) | Trace event storage and use |

## Verification

| Document | Purpose |
|---|---|
| [Testing guide](testing/TESTING.md) | Verification layers and exact commands |
| [Running tests](testing/RUNNING_TESTS.md) | Layered execution runbook |
| [Simulation](testing/SIMULATION.md) | RTL and SoC simulation boundaries |
| [BDD suite](../tests/README.md) | 15 features, 320 scenarios, and 1504 steps in the 2026-08-17 run |
| [Verilator suites](../tb/verilator/README.md) | RTL harness inventory |
| [Generated module matrix](traceability/MODULE_MATRIX.md) | Module to specification to test roll-up |
| [Current Milan v1.2 audit](testing/MILAN_V12_AUDIT_2026-08-16.md) | Exact results, limitations, and mandatory gaps |

## Operations and engineering records

| Document | Purpose |
|---|---|
| [Troubleshooting](limitations/TROUBLESHOOTING.md) | Current symptom, cause, and recovery guidance |
| [Recurring defect patterns](limitations/RECURRING_DEFECT_PATTERNS.md) | Review and test hazards seen repeatedly |
| [Bench topology](findings/BENCH_TOPOLOGY.md) | Reference-lab topology and operating notes |
| [Findings index](findings/README.md) | Dated investigations and measurements |
| [Change log](../CHANGELOG.md) | Measured results and implementation history |

## Documentation rules

- Treat the current audit as the compliance verdict.
- Treat generated matrices as current only when their check command passes.
- Treat pages with an obsolete marker as historical evidence.
- Treat board measurements as dated evidence, not a general product claim.
- A DUT change must update its harness in the same commit.
- Edit diagram sources, not rendered SVG or PNG files.
- Use [documentation generation](DOC_GENERATION.md) for regeneration commands.
