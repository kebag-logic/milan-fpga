# Archive — superseded & historical documents

Index of docs that are **superseded, completed plans, or point-in-time snapshots**. They
are kept for history (root-cause trails, measurement discipline, design rationale) but are
**not current state**. Each is marked in place with a `⚠️ SUPERSEDED` banner (they stay at
their original paths so the ~79 inbound cross-links across the doc set do not break); this
file is the consolidated map from each to its **living successor**.

Orientation for current docs: [`../SYSTEMS_ENGINEER_GUIDE.md`](../SYSTEMS_ENGINEER_GUIDE.md).
Full audit rationale: [`../DOC_AUDIT.md`](../DOC_AUDIT.md).

## Consolidations (merge groups)

The 2026-07 `>500 Mbit` perf campaign and the DMA-origin design log were frozen at many
dates with conflicting scoreboards. They consolidate to a small living set:

- **`findings/PERFORMANCE_GOAL.md`** = the campaign record · **`CHANGELOG.md`** = the
  lever→effect ledger · **`findings/PERF_ON_MILAN.md`** = the profiling method ·
  **`findings/LATENCY_INVESTIGATION.md`** = the memory-latency root cause ·
  **`fpga/PIPELINE_STAGES.md`** = the living stage-by-stage datapath reference ·
  **`fpga/HEADER_SPLIT_DESIGN.md`** = the unified header-split (hsq4–hsq12) history.

## Superseded documents → living successor

| Archived doc | Why superseded | Read instead |
|---|---|---|
| `findings/SESSION_HANDOFF.md` | 07-11 live-state; HANDOVER labels it historical | `findings/HANDOVER_SMALL.md`, `findings/BENCH_TOPOLOGY.md` |
| `findings/CAMPAIGN_500_PLAN.md` | completed gated plan (self-declared SUPERSEDED) | `findings/PERFORMANCE_GOAL.md`, `CHANGELOG.md` |
| `findings/RX_FANOUT_AND_TX_CEILING.md` | 07-07 snapshot (TX 186 / RX 223) | `findings/PERFORMANCE_GOAL.md` |
| `findings/RX_TX_PERFORMANCE.md` | 07-09 duplicate campaign scoreboard | `findings/PERFORMANCE_GOAL.md` |
| `findings/GIGABIT_HEADROOM_ANALYSIS.md` | 2-hart budget model, superseded numbers | `findings/PERFORMANCE_GOAL.md` |
| `findings/SINGLE_PORT_PERF.md` | 07-05 prequel; defers to the deeper doc | `findings/LATENCY_INVESTIGATION.md` |
| `findings/RX_MEMORY_HIERARCHY_PLAN.md` | completed L2 disambiguation plan | `fpga/PIPELINE_STAGES.md`, `findings/LATENCY_INVESTIGATION.md` |
| `findings/RX_OVERLOAD_WEDGE.md` | [FIXED] RX-storm post-mortem | `fpga/PIPELINE_STAGES.md` |
| `findings/RX_RING_DMA.md` | byte-ring era (folded out; `--legacy-ring` restores) | `fpga/PIPELINE_STAGES.md` |
| `findings/TX_READER_PREFETCH_PLAN.md` | completed-and-rejected plan (measure-first exemplar) | `fpga/PIPELINE_STAGES.md`, `CHANGELOG.md` |
| `fpga/CPPI_DMA_REDESIGN.md` | design-era byte-ring→BD-ring log | `fpga/PIPELINE_STAGES.md` |
| `fpga/HW_GRO_RSC.md` | single-slot RSC + 07-07 campaign log | `fpga/PIPELINE_STAGES.md` (R3), `fpga/HEADER_SPLIT_DESIGN.md` |
| `fpga/HSPLIT14_DESIGN.md` | continuation folded into the unified doc | `fpga/HEADER_SPLIT_DESIGN.md` |
| `integration/FULLY_FPGA_RISCV_MIGRATION.md` | completed PS→fabric migration plan | `litex/LITEX_SOC.md`, `integration/BOARD_PORTING_AX7101.md`, `integration/INTEGRATION_GUIDE.md` |
| `integration/OPEN_SOURCE_MIGRATION.md` | completed de-Xilinx plan | `integration/PORTING_GUIDE.md` §2 |

Preserved evergreen nuggets (recorded so nothing is lost): the datapath-input TX-vs-CPU
probe method (RX_FANOUT), the cycles/byte budget model (GIGABIT_HEADROOM), the Forencich
open-core catalog (OPEN_SOURCE_MIGRATION), the measure-before-build discipline
(TX_READER_PREFETCH / CAMPAIGN_500), the NET_IP_ALIGN +2 misalignment lesson (RX_FANOUT).
