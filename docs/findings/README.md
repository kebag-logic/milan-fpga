# Findings log - bugs cornered and campaigns measured on silicon

Chronological engineering record: every entry is a "symptom → measurement
chain → root cause → fix → verification" write-up (or a campaign plan with
its measured verdicts). Read these to learn *how this system is debugged*;
read [../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md)
for what is still open, and [`CHANGELOG.md`](../../CHANGELOG.md) for the
per-lever measured ledger.

Many entries carry **superseded/historical banners** - that is deliberate:
they are kept as the evidence trail (including retracted theories), not as
current-state documentation. The fully-superseded ones now live in
[`historical_now_obsolete/`](../../historical_now_obsolete/README.md) (their
rows below link there); the last pending merge sources were folded into
their living successors on 2026-07-25.

## Contents

- **[Fixed-bug post-mortems](#fixed-bug-post-mortems)** — Nine closed root causes in one table — TX `last_be` truncation, the classifier `tdest` wedge, ADP falling dormant, gPTP frames delivered 8-byte-padded — each with its status and, where one exists, the gating harness that keeps it fixed.
- **[Performance investigations & campaigns](#performance-investigations--campaigns)** — Eleven rows of measurement work, including the ones whose verdict was *do not build it*: the TX reader prefetch plan is kept solely as a refutation record. Several rows are merge sources folded into their living successors on 2026-07-25 and now link into the archive.
- **[Handover & bench](#handover--bench)** — Bench-ops onboarding plus the two 2026-07-26 campaigns: an adversarial sweep that triggered the entry-0 blocker *on purpose* to prove the root cause by causation, and a live health sweep showing 0 format errors over ~2 G frames.
- **[Conventions](#conventions)** — The two rules for adding to this log. The one that surprises people: nothing is ever deleted, and refuted theories stay in, because the refutation is the value.

## Fixed-bug post-mortems

| Doc | Finding | Status |
|---|---|---|
| [kl-eth-tx-debug.md](kl-eth-tx-debug.md) | The TX saga (2026-07-04): `last_be` truncation, missing coherent-DMA, cut-through starvation, skb alignment, IOB/gtx phase | FIXED |
| [RX_RING_DMA.md (archived)](../../historical_now_obsolete/findings/RX_RING_DMA.md) | RX large-frame loss: per-beat Wishbone drained ~21 MB/s vs the 125 MB/s wire → AXI-burst ring engines | FIXED (byte-ring era, historical) |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Classifier `tdest` mis-timing under back-to-back frames → TX wedge; per-frame tdest sideband redesign | FIXED (gating harness: `tb/verilator/controller_rate`) |
| [CBS_DEFAULT_SHAPING_BUG.md](CBS_DEFAULT_SHAPING_BUG.md) | Reset defaults credit-paced ALL best-effort TX at ~300 Mb/s | FIXED |
| [RX_OVERLOAD_WEDGE.md (archived)](../../historical_now_obsolete/findings/RX_OVERLOAD_WEDGE.md) | Two storm-lethal RX wedges (BD-order inversion; `drops` field aliasing the v2 marker) | FIXED |
| [ADP_DORMANCY.md](ADP_DORMANCY.md) | ADP advertiser fell dormant on silicon; self-re-arm + `A_ADP_DIAG` forensics and fix | FIXED |
| [GPTP_RXPAD_ROOTCAUSE.md](GPTP_RXPAD_ROOTCAUSE.md) | gPTP "bad message": RX DMA delivered 8-byte-padded frames; gateware pad-strip fix + switch-behavior matrix | FIXED |
| [PTP_TS_METADATA_FIX.md](PTP_TS_METADATA_FIX.md) | HW-timestamp metadata pipeline root cause + the DMA record contract (v2.1) | FIXED |
| [ADP_SHAPE_STATIC_0727.md](ADP_SHAPE_STATIC_0727.md) | The 8x8 board advertised the 1x1 shape: `ADP_TALKER`/`ADP_LISTENER` were RW registers filled in by a boot script frozen at 1x1, so it offered 1 talker source / 2 listener sinks beside a reference device offering 4/10 - and the CRF talker at uid 8 was outside the advertised range. The counts are now read-only, elaborated from the same localparams that size the ACMP context arrays | FIXED (gate: `scripts/check_entity_shape.py`) |

## Performance investigations & campaigns

| Doc | What it holds |
|---|---|
| [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) | The consolidated >500 campaign record: goal, forced-march log, close-out scoreboard, plain-language RX story + diagrams, gigabit headroom analysis |
| [CAMPAIGN_500_PLAN.md (archived)](../../historical_now_obsolete/findings/CAMPAIGN_500_PLAN.md) | The campaign plan + status ledger (superseded banners intact) |
| [RX_TX_PERFORMANCE.md (archived)](../../historical_now_obsolete/findings/RX_TX_PERFORMANCE.md) | The 07-09 campaign narrative (merged into [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) 2026-07-25) |
| [GIGABIT_HEADROOM_ANALYSIS.md (archived)](../../historical_now_obsolete/findings/GIGABIT_HEADROOM_ANALYSIS.md) | Headroom at 100 MHz; wire-rate tables (merged into [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) 2026-07-25) |
| [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) | Why single-port TCP capped at 30 Mbit/s: memory latency decomposition (1424 ns/miss), the 112.5 MHz build-and-revert, retracted theories kept as lessons; §2.1 = the folded second-core prequel |
| [SINGLE_PORT_PERF.md (archived)](../../historical_now_obsolete/findings/SINGLE_PORT_PERF.md) | Would a second core help a single flow? (No - latency-bound; merged into [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) 2026-07-25) |
| [RX_FANOUT_AND_TX_CEILING.md (archived)](../../historical_now_obsolete/findings/RX_FANOUT_AND_TX_CEILING.md) | HW-TSO, 2-queue RX fan-out, the TX ceiling |
| [RX_MEMORY_HIERARCHY_PLAN.md (archived)](../../historical_now_obsolete/findings/RX_MEMORY_HIERARCHY_PLAN.md) | Cold-vs-capacity decision tree → the DDIO choice |
| [TX_READER_PREFETCH_PLAN.md (archived)](../../historical_now_obsolete/findings/TX_READER_PREFETCH_PLAN.md) | A full plan whose measured verdict is **do not build it** (kept as the refutation record) |
| [RX_PERF_TUNING_MAP.md](RX_PERF_TUNING_MAP.md) | The tuning-map maintainer notes + STRICT gateware⇄driver pairing hazards |
| [PERF_ON_MILAN.md](PERF_ON_MILAN.md) | How to run `perf` on the board (no kallsyms) |

On-silicon evidence logs live in
[`sw/litex/evidence/`](../../sw/litex/evidence/) (BIOS banners, memtest, the
M-A3 DMA write-up [`hw_ma3_dma_datapath_100mhz.md`](../../sw/litex/evidence/hw_ma3_dma_datapath_100mhz.md)).

## Handover & bench

| Doc | What it holds |
|---|---|
| [BENCH_TOPOLOGY.md](BENCH_TOPOLOGY.md) | Bench-ops onboarding: where-is-what + the physical/tap topology |
| [FLASH_0x0014_0727.md](FLASH_0x0014_0727.md) | 2026-07-27 the area round on silicon: 3 seeds placed and ALL MET TIMING (best WNS +0.147), -5,216 LUT delivered vs -4,847 estimated, but slice occupancy only 99.93 % -> 99.65 % (55 free) so the design is still slice-bound; flashed bitstream-only, VERSION 0x0001_0014 and the five-queue map read back from hardware, smoke 5/5, parsed == matched exactly |
| [STRESS_0726.md](STRESS_0726.md) | 2026-07-26 adversarial campaign: 19 checks, 0 failures — stop/start storms, illegal CSR access, engine cycling, boundary sids, and the entry-0 blocker triggered ON PURPOSE to prove the root cause by causation |
| [LIVE_BENCH_0726.md](LIVE_BENCH_0726.md) | 2026-07-26 live health + function sweep of both boards: gPTP converged, bidirectional streaming, 0 format errors over ~2 G frames, live audio capture, and the two known tie-offs observed on silicon |

## Conventions

* Every finding doc opens with its date and, when superseded, a banner
  naming what replaced it. Nothing here is deleted - refuted theories are
  retained and marked, because the refutations are the value.
* Diagrams are generated: edit the sibling `*.gen.py` under `docs/`, never
  the `.svg`/`.png` outputs.
