# Findings log - bugs cornered and campaigns measured on silicon

Chronological engineering record: every entry is a "symptom → measurement
chain → root cause → fix → verification" write-up (or a campaign plan with
its measured verdicts). Read these to learn *how this system is debugged*;
read [../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md)
for what is still open, and [`CHANGELOG.md`](../../CHANGELOG.md) for the
per-lever measured ledger.

Many entries carry **superseded/historical banners** - that is deliberate:
they are kept as the evidence trail (including retracted theories), not as
current-state documentation.

## Fixed-bug post-mortems

| Doc | Finding | Status |
|---|---|---|
| [kl-eth-tx-debug.md](kl-eth-tx-debug.md) | The TX saga (2026-07-04): `last_be` truncation, missing coherent-DMA, cut-through starvation, skb alignment, IOB/gtx phase | FIXED |
| [RX_RING_DMA.md](RX_RING_DMA.md) | RX large-frame loss: per-beat Wishbone drained ~21 MB/s vs the 125 MB/s wire → AXI-burst ring engines | FIXED (byte-ring era, historical) |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Classifier `tdest` mis-timing under back-to-back frames → TX wedge; per-frame tdest sideband redesign | FIXED (gating harness: `tb/verilator/controller_rate`) |
| [CBS_DEFAULT_SHAPING_BUG.md](CBS_DEFAULT_SHAPING_BUG.md) | Reset defaults credit-paced ALL best-effort TX at ~300 Mb/s | FIXED |
| [RX_OVERLOAD_WEDGE.md](RX_OVERLOAD_WEDGE.md) | Two storm-lethal RX wedges (BD-order inversion; `drops` field aliasing the v2 marker) | FIXED |
| [ADP_DORMANCY.md](ADP_DORMANCY.md) | ADP advertiser fell dormant on silicon; self-re-arm + `A_ADP_DIAG` forensics and fix | FIXED |
| [GPTP_RXPAD_ROOTCAUSE.md](GPTP_RXPAD_ROOTCAUSE.md) | gPTP "bad message": RX DMA delivered 8-byte-padded frames; gateware pad-strip fix + switch-behavior matrix | FIXED |
| [PTP_TS_METADATA_FIX.md](PTP_TS_METADATA_FIX.md) | HW-timestamp metadata pipeline root cause + the DMA record contract (v2.1) | FIXED |

## Performance investigations & campaigns

| Doc | What it holds |
|---|---|
| [RX_TX_PERFORMANCE.md](RX_TX_PERFORMANCE.md) | The >500 Mbit/s campaign narrative: current state, story, diagrams |
| [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) | The >500 north star + forced-march results |
| [CAMPAIGN_500_PLAN.md](CAMPAIGN_500_PLAN.md) | The campaign plan + status ledger (superseded banners intact) |
| [GIGABIT_HEADROOM_ANALYSIS.md](GIGABIT_HEADROOM_ANALYSIS.md) | Headroom at 100 MHz; wire-rate percentage tables |
| [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) | Why single-port TCP capped at 30 Mbit/s: memory latency decomposition (1424 ns/miss), the 112.5 MHz build-and-revert, retracted theories kept as lessons |
| [SINGLE_PORT_PERF.md](SINGLE_PORT_PERF.md) | Would a second core help a single flow? (No - latency-bound; measured three ways) |
| [RX_FANOUT_AND_TX_CEILING.md](RX_FANOUT_AND_TX_CEILING.md) | HW-TSO, 2-queue RX fan-out, the TX ceiling |
| [RX_MEMORY_HIERARCHY_PLAN.md](RX_MEMORY_HIERARCHY_PLAN.md) | Cold-vs-capacity decision tree → the DDIO choice |
| [TX_READER_PREFETCH_PLAN.md](TX_READER_PREFETCH_PLAN.md) | A full plan whose measured verdict is **do not build it** (kept as the refutation record) |
| [RX_PERF_TUNING_MAP.md](RX_PERF_TUNING_MAP.md) | The tuning-map maintainer notes + STRICT gateware⇄driver pairing hazards |
| [PERF_ON_MILAN.md](PERF_ON_MILAN.md) | How to run `perf` on the board (no kallsyms) |

On-silicon evidence logs live in
[`sw/litex/evidence/`](../../sw/litex/evidence/) (BIOS banners, memtest, the
M-A3 DMA write-up `hw_ma3_dma_datapath_100mhz.md`).

## Handover & bench

| Doc | What it holds |
|---|---|
| [BENCH_TOPOLOGY.md](BENCH_TOPOLOGY.md) | Bench-ops onboarding: where-is-what + the physical/tap topology |

## Conventions

* Every finding doc opens with its date and, when superseded, a banner
  naming what replaced it. Nothing here is deleted - refuted theories are
  retained and marked, because the refutations are the value.
* Diagrams are generated: edit the sibling `*.gen.py` under `docs/`, never
  the `.svg`/`.png` outputs.
