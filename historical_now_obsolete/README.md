# historical_now_obsolete — superseded & completed-plan documents

Docs that are **superseded, completed plans, or point-in-time snapshots**, moved out of the
active tree (USER decision 2026-07-25; before that they sat at their original paths with
banners). They are kept for history — root-cause trails, measurement discipline, design
rationale — but are **not current state**. This file maps each to its **living successor**.
Every inbound link across the doc set was repaired at move time; `scripts/docs_check.py`
gates link integrity from here on.

Orientation for current docs: [`docs/SYSTEMS_ENGINEER_GUIDE.md`](../docs/SYSTEMS_ENGINEER_GUIDE.md).
Full audit rationale: [`DOC_AUDIT.md`](DOC_AUDIT.md) (archived here 2026-07-27).

## Consolidations (merge groups)

The 2026-07 `>500 Mbit` perf campaign and the DMA-origin design log were frozen at many
dates with conflicting scoreboards. They consolidate to a small living set:

- **`docs/findings/PERFORMANCE_GOAL.md`** = the campaign record · **`CHANGELOG.md`** = the
  lever→effect ledger · **`docs/findings/PERF_ON_MILAN.md`** = the profiling method ·
  **`docs/findings/LATENCY_INVESTIGATION.md`** = the memory-latency root cause ·
  **`docs/fpga/PIPELINE_STAGES.md`** = the living stage-by-stage datapath reference ·
  **`docs/fpga/HEADER_SPLIT_DESIGN.md`** = the unified header-split (hsq4–hsq12) history.

## Moved here → living successor

| Doc (in this folder) | Why superseded | Read instead |
|---|---|---|
| [`findings/CAMPAIGN_500_PLAN.md`](findings/CAMPAIGN_500_PLAN.md) | completed gated plan (self-declared SUPERSEDED) | [`docs/findings/PERFORMANCE_GOAL.md`](../docs/findings/PERFORMANCE_GOAL.md), [`CHANGELOG.md`](../CHANGELOG.md) |
| [`findings/RX_FANOUT_AND_TX_CEILING.md`](findings/RX_FANOUT_AND_TX_CEILING.md) | 07-07 snapshot (TX 186 / RX 223) | [`docs/findings/PERFORMANCE_GOAL.md`](../docs/findings/PERFORMANCE_GOAL.md) |
| [`findings/RX_MEMORY_HIERARCHY_PLAN.md`](findings/RX_MEMORY_HIERARCHY_PLAN.md) | completed L2 disambiguation plan | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md), [`docs/findings/LATENCY_INVESTIGATION.md`](../docs/findings/LATENCY_INVESTIGATION.md) |
| [`findings/RX_OVERLOAD_WEDGE.md`](findings/RX_OVERLOAD_WEDGE.md) | [FIXED] RX-storm post-mortem | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md) |
| [`findings/RX_RING_DMA.md`](findings/RX_RING_DMA.md) | byte-ring era (folded out; `--legacy-ring` restores) | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md) |
| [`findings/RX_TX_PERFORMANCE.md`](findings/RX_TX_PERFORMANCE.md) | merged 2026-07-25: plain-language RX story + diagrams + levers table folded in | [`docs/findings/PERFORMANCE_GOAL.md`](../docs/findings/PERFORMANCE_GOAL.md) |
| [`findings/GIGABIT_HEADROOM_ANALYSIS.md`](findings/GIGABIT_HEADROOM_ANALYSIS.md) | merged 2026-07-25: cycles/byte budget model + "data-plane is already gigabit" verdict folded in | [`docs/findings/PERFORMANCE_GOAL.md`](../docs/findings/PERFORMANCE_GOAL.md) |
| [`findings/SINGLE_PORT_PERF.md`](findings/SINGLE_PORT_PERF.md) | merged 2026-07-25: "second core won't help — latency-bound, measured three ways" folded in as §2.1 | [`docs/findings/LATENCY_INVESTIGATION.md`](../docs/findings/LATENCY_INVESTIGATION.md) |
| [`findings/TX_READER_PREFETCH_PLAN.md`](findings/TX_READER_PREFETCH_PLAN.md) | completed-and-rejected plan (measure-first exemplar) | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md), [`CHANGELOG.md`](../CHANGELOG.md) |
| [`fpga/CPPI_DMA_REDESIGN.md`](fpga/CPPI_DMA_REDESIGN.md) | design-era byte-ring→BD-ring log | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md) |
| [`fpga/HW_GRO_RSC.md`](fpga/HW_GRO_RSC.md) | single-slot RSC + 07-07 campaign log | [`docs/fpga/PIPELINE_STAGES.md`](../docs/fpga/PIPELINE_STAGES.md) (R3), [`docs/fpga/HEADER_SPLIT_DESIGN.md`](../docs/fpga/HEADER_SPLIT_DESIGN.md) |
| [`fpga/HSPLIT14_DESIGN.md`](fpga/HSPLIT14_DESIGN.md) | merged 2026-07-25: hsq12 cut-through chapter folded in (v3 `fill_len`/`hdr_idx` ABI lives there) | [`docs/fpga/HEADER_SPLIT_DESIGN.md`](../docs/fpga/HEADER_SPLIT_DESIGN.md) |
| [`integration/FULLY_FPGA_RISCV_MIGRATION.md`](integration/FULLY_FPGA_RISCV_MIGRATION.md) | completed PS→fabric migration plan | [`docs/litex/LITEX_SOC.md`](../docs/litex/LITEX_SOC.md), [`docs/integration/BOARD_PORTING_AX7101.md`](../docs/integration/BOARD_PORTING_AX7101.md), [`docs/integration/INTEGRATION_GUIDE.md`](../docs/integration/INTEGRATION_GUIDE.md) |
| [`integration/OPEN_SOURCE_MIGRATION.md`](integration/OPEN_SOURCE_MIGRATION.md) | completed de-Xilinx plan | [`docs/integration/PORTING_GUIDE.md`](../docs/integration/PORTING_GUIDE.md) §2 |
| [`DOC_AUDIT.md`](DOC_AUDIT.md) | completed plan — a self-declared "planning + drafting only" frozen record whose §2 archive move was executed 2026-07-25; the living ledger of what is archived is **this page** | [`docs/README.md`](../docs/README.md), [`docs/SYSTEMS_ENGINEER_GUIDE.md`](../docs/SYSTEMS_ENGINEER_GUIDE.md) |

Preserved evergreen nuggets (recorded so nothing is lost): the datapath-input TX-vs-CPU
probe method (RX_FANOUT), the Forencich open-core catalog (OPEN_SOURCE_MIGRATION), the
measure-before-build discipline (TX_READER_PREFETCH / CAMPAIGN_500), the NET_IP_ALIGN +2
misalignment lesson (RX_FANOUT). The cycles/byte budget model (GIGABIT_HEADROOM) and the
hsq12 cut-through ABI (HSPLIT14) were not just preserved — they were folded into their
living successors on 2026-07-25.
