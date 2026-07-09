# Documentation index

Documentation for the Milan TSN FPGA network interface (and its evolution toward a
4-port AVB switch). Unsure what a term means? → [GLOSSARY.md](GLOSSARY.md).

## Reading paths

| If you want to… | read, in order |
|---|---|
| **Understand the system** (new contributor) | [FULL_FPGA_SOLUTION](FULL_FPGA_SOLUTION.md) → [ARCHITECTURE](ARCHITECTURE.md) → [SYSTEM_DOMAIN_MAP](SYSTEM_DOMAIN_MAP.md) → [GLOSSARY](GLOSSARY.md) |
| **See where the project is heading** | [AVB_SWITCH_DIRECTION](AVB_SWITCH_DIRECTION.md) (decision matrix + measured scoreboard) → [FULLY_FPGA_RISCV_MIGRATION](FULLY_FPGA_RISCV_MIGRATION.md) |
| **Build / boot / operate the board** | [BOARD_PORTING_AX7101](BOARD_PORTING_AX7101.md) → [QSPI_FLASHBOOT](QSPI_FLASHBOOT.md) → [TROUBLESHOOTING](TROUBLESHOOTING.md) (recipes also in `milan-tests-avb/fpga/skills/milan-fpga-nic/SKILL.md`) |
| **Debug a datapath problem** | [pipeline-telemetry](pipeline-telemetry.md) → the findings docs (§5) for how every past bug was cornered → [SIMULATION](SIMULATION.md) |
| **Write driver / DT / register code** | [REGISTER_MAP](REGISTER_MAP.md) → `../sw/README.md` + `../sw/dts/README.md` |

## 1 — System overview & architecture

| Document | Purpose |
|----------|---------|
| [FULL_FPGA_SOLUTION.md](FULL_FPGA_SOLUTION.md) | **The master guide to the fully-FPGA solution** — high- and medium-level architecture, the three datapath boundaries, build/run, and the roadmap. **Read first.** |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System map: datapath, control plane, clock domains, HDL↔software mapping, and a "where to change things" guide. |
| [SYSTEM_DOMAIN_MAP.md](SYSTEM_DOMAIN_MAP.md) | **Which module lives in which domain/language** — a one-picture map of the whole stack (userspace → kernel → firmware → LiteX → RTL → vendored IP → silicon) plus the host tooling. |
| [GLOSSARY.md](GLOSSARY.md) | **Every term of art in one place** — AVB/Milan, Ethernet/PHY, FPGA/tooling, LiteX/SoC, the ring-DMA vocabulary, Linux networking, and the project shorthand (M-Ax, §A.x, FR/NFR, C/S/I work items). |

## 2 — Design direction & plans

| Document | Purpose |
|----------|---------|
| [AVB_SWITCH_DIRECTION.md](AVB_SWITCH_DIRECTION.md) | **The current direction: endpoint → 4-port GMII-copper AVB switch** (MTU fixed 1500) — where the AVTP/TSO/RSC hooks land, the all-fabric forwarding plane, the memory-bandwidth reality, the full decision matrix (C/S/I tracks) and the measured production scoreboard. Diagram: [AVB_SWITCH_DIRECTION.svg](AVB_SWITCH_DIRECTION.svg) ([.drawio](AVB_SWITCH_DIRECTION.drawio)). |
| [FULLY_FPGA_RISCV_MIGRATION.md](FULLY_FPGA_RISCV_MIGRATION.md) | The deep, step-numbered migration plan (§A.x parts: DDR, clocking, CSR, DMA, MAC, IRQ, wrapper, boot, driver, DT). |
| [CPPI_DMA_REDESIGN.md](CPPI_DMA_REDESIGN.md) | **The DMA/MAC memory-architecture plan + the running perf-campaign log** — the TI-CPSW-style BD-RAM/cut-through/zero-copy plan (2026-07-05) plus dated silicon addenda: BD zero-copy RX bring-up, TX-BD v1/v2/v2b (zero-copy realign + HW checksum-insert, verified 4 ways), and the **2026-07-07 campaign** (dual-hart SMP +66 % TX, the three-copies tick-profile → copybreak/page-frag RX 25→45.6, the TX-stall verdict). |
| [HW_GRO_RSC.md](HW_GRO_RSC.md) | **HW-GRO/RSC — receive-side coalescing in the RX BD engine** (2026-07-07, an early ≥200 Mbit/s workstream (now part of the >500 campaign — see RX_TX_PERFORMANCE.md)): merge rules, BD-v2 format, write-side realign, driver contract, sim plan — plus the implementation status (**phases A+B done, 14/14 sims** incl. the alignment sweep, as-built divergences documented). |
| [AXIS_CORES_ON_NAXRISCV.md](AXIS_CORES_ON_NAXRISCV.md) | How to attach AXI-Stream cores to the NaxRiscv SoC (control/data/event planes). |
| [OPEN_SOURCE_MIGRATION.md](OPEN_SOURCE_MIGRATION.md) | Track 1 (de-Xilinx): vendored `verilog-axis`, XPM removal, Yosys/ECP5 portability checks. |

## 3 — Contracts: ABI, requirements, validation

| Document | Purpose |
|----------|---------|
| [REGISTER_MAP.md](REGISTER_MAP.md) | AXI4-Lite CSR ABI + the ring-DMA CSR windows — the contract shared by HDL, the Linux driver, and the device tree. |
| [PROTOCOL_VALIDATION_MATRIX.md](PROTOCOL_VALIDATION_MATRIX.md) | **Every protocol × where it's implemented × the test that validates it** — the validation contract for the FPGA-only solution. |
| [../REQUIREMENTS.md](../REQUIREMENTS.md) | Normative requirements + the 802.1 gap analysis (what's missing and why). |
| [FR_NFR.md](FR_NFR.md) | Functional / non-functional requirement register (FR-*/NFR-* IDs referenced throughout). |
| [MILAN_V12_DEPENDENCY_MATRIX.md](MILAN_V12_DEPENDENCY_MATRIX.md) | Milan v1.2 → FR/NFR dependency matrix with verification traceability. |
| [../TODO.md](../TODO.md) | Phased, dependency-ordered task list with status. |
| [../aem-and-aecp.md](../aem-and-aecp.md) | AVDECC entity-model / AECP prior work notes (pairs with `avdecc/milan-v12-entity.json`). |

## 4 — Build, boot & operate

| Document | Purpose |
|----------|---------|
| [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) | How the SoC was ported to the Alinx AX7101 — pin extraction from the official constraints, DDR3/LiteDRAM integration, verification. |
| [QSPI_FLASHBOOT.md](QSPI_FLASHBOOT.md) | **Boot Linux from the on-board QSPI flash** instead of the ~4-min serial upload — the 16 MB-flash layout, the `linux_flashboot` BIOS method, `deploy.sh flash-images`, and the path to zero-upload. |
| [SIMULATION.md](SIMULATION.md) | How the design is simulated at all three layers (Verilator RTL harnesses, softcore boot, softcore+NIC M-A2) — step by step. |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Field log of every problem hit bringing up the full-FPGA solution, with symptom → cause → fix. |

## 5 — Findings: bugs cornered and measured on silicon

Chronological; each is a full "symptom → measurement chain → root cause → fix →
verification" write-up with a one-picture diagram. Read these to learn how this
system is debugged.

> **▶ The >500 Mbit/s RX+TX campaign (2026-07).** Start here: **[RX_TX_PERFORMANCE.md](RX_TX_PERFORMANCE.md)**
> (current state, story, diagrams) + **[../CHANGELOG.md](../CHANGELOG.md)** (per-lever measured effect,
> with [perf_campaign.svg](perf_campaign.svg)). Deep dives: [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md)
> (north star), [LSU_NONBLOCKING_DCACHE.md](LSU_NONBLOCKING_DCACHE.md) (non-blocking D$ + RPT prefetcher),
> [RX_MEMORY_HIERARCHY_PLAN.md](RX_MEMORY_HIERARCHY_PLAN.md) (cold-vs-capacity → DDIO),
> [RX_FANOUT_AND_TX_CEILING.md](RX_FANOUT_AND_TX_CEILING.md), [RX_OVERLOAD_WEDGE.md](RX_OVERLOAD_WEDGE.md),
> [CBS_DEFAULT_SHAPING_BUG.md](CBS_DEFAULT_SHAPING_BUG.md). Diagrams in [diagrams/](diagrams/).
> **Result: TX crosses 500; RX 298 with a measured 481 ceiling → next lever DDIO.**

| Document | Finding |
|----------|---------|
| [kl-eth-tx-debug.md](kl-eth-tx-debug.md) | **The TX saga** (2026-07-04) — `last_be` truncation, missing coherent-DMA, cut-through starvation (PacketFIFO fix), skb alignment, IOB/gtx phase. Diagram: [TX_STARVATION_FIX.svg](TX_STARVATION_FIX.svg) ([.drawio](TX_STARVATION_FIX.drawio)). |
| [RX_RING_DMA.md](RX_RING_DMA.md) | **The RX large-frame loss + the ring-DMA engines** (2026-07-04/05) — per-beat Wishbone drained at ~21 MB/s vs the 125 MB/s wire; fixed by AXI-burst ring writers/readers with always-ready ingress; includes the full bandwidth ladder (TX 16→62, RX 58→92 @1500) and both timing-closure lessons. Diagrams: [RX_RING_DMA.svg](RX_RING_DMA.svg), [RX_RING_OPERATION.svg](RX_RING_OPERATION.svg) (mechanism one-pager; [.drawio](RX_RING_OPERATION.drawio)). |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | **The CBS interference TX-wedge** (2026-07-05, FIXED) — classifier `tdest` mis-timing under back-to-back frames + parse-FSM desync + the `PRIO_REGEN` half-swap reset; per-frame tdest sideband redesign; also documents the retired false theories and the harness-sampling trap. |
| [SINGLE_PORT_PERF.md](SINGLE_PORT_PERF.md) | **Would a second core help single-port throughput?** (2026-07-05) — measured three ways (CPU 94 % idle, `rx-usecs` sweep 5 µs→1 ms flat, `-P 4` doesn't aggregate): the single flow is **latency-bound, not CPU-bound**, so a second core and coalescing both do nothing; adds the runtime `ethtool -C rx-usecs` knob and the switch-role implication. Superseded by ↓. |
| [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) | **The full latency & memory investigation** (2026-07-05) — why single-port TCP caps at 30 Mbit/s. Localises it to **memory latency (1424 ns/miss = 50 % TLB walk + 50 % DRAM floor)** via a UDP-flood CPU-saturation test and a hugepage A/B; two retracted theories kept as lessons; the `rx-usecs-low` +32 % win, the pointer-writeback (RTL+sim), the `sys_rst`-fanout timing finding + the 112.5 MHz build (reset replication proved impossible — DONT_TOUCH; built + measured on silicon, then **reverted to 100 MHz**), and the TI CPPI/CPSW blueprint mapping. **Read this for the whole story.** The per-frame cost decomposition was completed by the 2026-07-07 tick-profile (**three copies of every byte** — see the campaign addendum in [CPPI_DMA_REDESIGN.md](CPPI_DMA_REDESIGN.md)). |
| [pipeline-telemetry.md](pipeline-telemetry.md) | The `milan_tlm` in-fabric observability block that powers all of the above — per-stage frame/beat/stall counters, coherent snapshots, Little's-law occupancy/latency, sysfs + BIOS access. |

## 6 — Module & verification docs

| Document | Purpose |
|----------|---------|
| [../hdl/csr/doc/milan_csr.md](../hdl/csr/doc/milan_csr.md) | `milan_csr` module reference (TerosHDL format: generics/ports/signals/processes). |
| [../tb/verilator/README.md](../tb/verilator/README.md) | Runnable self-checking harnesses — how to run and what they prove (16 suites). |
| [../tb/verilator/cbs/README.md](../tb/verilator/cbs/README.md) | 802.1Qav CBS credit-math verification detail. |
| [../tb/verilator/controller_rate/README.md](../tb/verilator/controller_rate/README.md) | End-to-end classify→queue→shape integrity harness (gating; born from the CBS bug). |
| `../tb/verilator/avtp_stream/` | AVTP stream-parser harness — stream-id / presentation-time extraction + programmable stream match (the S1 AVTP-engine foundation). |
| [../tb/verilator/csr/README.md](../tb/verilator/csr/README.md) | CSR verification detail. |
| [../THIRD_PARTY.md](../THIRD_PARTY.md) | Vendored third-party code and licenses. |

New RTL added in the 2026-07 TSN rework: `hdl/802_1q_traffic_shaper/traffic_class_map.sv`
(802.1Q PCP→queue decode), `hdl/ptp_timestamp/ptp_csr_sync.sv` (CSR↔PHC CDC),
and the runtime-config reworks of `credit_based_shaper`, `traffic_shaping_core`,
`traffic_classifier` (per-frame tdest sideband, 2026-07-05), `timestamp_counter`,
`ethernet_events` and `milan_top`.

Existing per-module docs generated by [TerosHDL](https://terostechnology.github.io/)
live next to their RTL under `hdl/**/doc/`. Regenerate any of them (and the
schematic/FSM SVGs) by running the TerosHDL documenter on the corresponding
`.sv`; the in-code `//!` comments are the source.

## Conventions

* **RTL:** SystemVerilog, `` `default_nettype none ``, TerosHDL/Doxygen `//!`
  documentation comments on every generic, port and signal; named `always_*`
  processes with a preceding `//!` description.
* **Register maps:** offsets and reset values are defined once in the RTL and
  documented in `REGISTER_MAP.md`; the CSR harness asserts they agree.
* **Verification:** every DUT change ships with its harness update in the same
  commit.
* **Diagrams:** every `*.svg`/`*.png`/`*.drawio` in this directory is generated —
  edit the sibling `*.gen.py`, never the outputs.
