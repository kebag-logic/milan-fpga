# Findings log - bugs cornered and campaigns measured on silicon

Chronological engineering record: every entry is a "symptom → measurement
chain → root cause → fix → verification" write-up (or a campaign plan with
its measured verdicts). Read these to learn *how this system is debugged*;
read [the dated Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md)
for what is still open, and the [historical performance ledger](../history/v1/PERFORMANCE_CHANGELOG.md) for the
per-lever measured ledger.

Many entries carry **superseded/historical banners** - that is deliberate:
they are kept as the evidence trail (including retracted theories), not as
current-state documentation. The fully-superseded ones now live in
[historical v1](../history/v1/README.md) (their
rows below link there); the last pending merge sources were folded into
their living successors on 2026-07-25.

Nine entries left this log on 2026-08-25 (#259): the MAC TX bring-up saga, the
RX-pad root cause, the timestamp record contract, the GM-loss-under-load
reproduction, the 2026-08-03 throughput-collapse and playback-path audits, the
2026-07-27 reference-listener sweep, and the two archived RX studies. Each was
measured on the retired host path, which #259 removes from the checkout; the
write-ups stay in git history.

A tenth entry moved on 2026-08-31.

It preserves the retired runtime profiling method.

## Contents

- **[Fixed-bug post-mortems](#fixed-bug-post-mortems)** -- The closed root causes in one table -- the classifier `tdest` wedge, credit-paced best-effort TX, ADP falling dormant, the 8x8 board advertising the 1x1 shape -- each with its status and, where one exists, the gating harness that keeps it fixed.
- **[Performance investigations & campaigns](#performance-investigations--campaigns)** -- Nine rows of measurement work, including the ones whose verdict was *do not build it*: the TX reader prefetch plan is kept solely as a refutation record. Several rows are merge sources folded into their living successors on 2026-07-25 and now link into the archive.
- **[Bench operations](#bench-operations)** -- Bench-ops onboarding, the two 2026-07-26 campaigns (an adversarial sweep that triggered the entry-0 blocker *on purpose* to prove the root cause by causation, and a live health sweep showing 0 format errors over ~2 G frames), and the 07-27 area-round flash.
- **[Conventions](#conventions)** -- The two rules for adding to this log. The one that surprises people: nothing is ever deleted, and refuted theories stay in, because the refutation is the value.

## Fixed-bug post-mortems

| Doc | Finding | Status |
|---|---|---|
| [RX_RING_DMA.md (archived)](../history/v1/findings/RX_RING_DMA.md) | RX large-frame loss: per-beat Wishbone drained ~21 MB/s vs the 125 MB/s wire → AXI-burst ring engines | FIXED (byte-ring era, historical) |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Classifier `tdest` mis-timing under back-to-back frames → TX wedge; per-frame tdest sideband redesign | FIXED (gating harness: [`tb/verilator/controller_rate`](../../tb/verilator/controller_rate)) |
| [CBS_DEFAULT_SHAPING_BUG.md](CBS_DEFAULT_SHAPING_BUG.md) | Reset defaults credit-paced ALL best-effort TX at ~300 Mb/s | FIXED |
| [RX_OVERLOAD_WEDGE.md (archived)](../history/v1/findings/RX_OVERLOAD_WEDGE.md) | Two storm-lethal RX wedges (BD-order inversion; `drops` field aliasing the v2 marker) | FIXED |
| [ADP_DORMANCY.md](ADP_DORMANCY.md) | ADP advertiser fell dormant on silicon; self-re-arm + `A_ADP_DIAG` forensics and fix | FIXED |
| [Historical ADP shape finding](../history/v1/findings/ADP_SHAPE_STATIC_0727.md) | The 8x8 board advertised the 1x1 shape: `ADP_TALKER`/`ADP_LISTENER` were RW registers filled in by a boot script frozen at 1x1, so it offered 1 talker source / 2 listener sinks beside a reference device offering 4/10 - and the CRF talker at uid 8 was outside the advertised range. The counts are now read-only AND generated from the end-station config, by the same builder pass that emits the AEM descriptor ROM; `milan_datapath` includes the same file to size its ACMP context arrays | FIXED (gate: [`scripts/check_entity_shape.py`](../../scripts/check_entity_shape.py), incl. a pre-build refusal in `build.sh`/`sweep.sh`) |
| [DEFECT_CLASSES_0802.md](DEFECT_CLASSES_0802.md) | **Three wire-truth defect classes in one day (2026-08-02):** the board's own `promisc on` voided the TCAM stream shield it installs (Sync cadence median 398 ms/max 3001 ms under load → 101/200 ms after the driver-side shield); every raw AECP/ACMP builder over-declared `control_data_length` by the 8-octet id field for years, hidden by Ethernet's 60-byte padding until a length validator silently dropped the big payloads; and the reference device's per-frame FRAMES counters now get *attributed* per side instead of smearing the pair | FIXED (shield + cdl in tools/board software; harness attributes per side) |
| [Historical physical-family triage](../history/v1/findings/PHYSICAL_FAMILY_TRIAGE_0802.md) | **The first silicon run of the powerstrip `physical` family (`ax-phys-a`, 2026-08-02), both FAILs triaged clause-first.** (1) `GPTP_GM_CHANGED` "never advanced" was a **wrong assertion**: 1722.1-2021 Table 7-153 counts *changes of the grandmaster*, and the AX holds `priority1` 238 against the bridge's 246, so it is GM before, alone-GM during and GM after, which makes zero the conformant delta. Replaced by a topology-graded continuity/advance split plus the peer-side counter, with `LINK_UP` demoted to INFO because the inline tap holds the DUT's PHY up. (2) The lost stream format is a **real open gap**: Milan 5.3.8.1 is an unconditional *shall* and the board's `/proc/mtd` is empty, so it now grades `KNOWN-PENDING` naming what must persist and where. Also: the peer's index 8 is the **CRF** input, which is why 32 of the run's 45 SKIPs were a bind that was never bindable | (1) FIXED, assertion corrected and bitten; (2) **OPEN**, needs a writable flash partition plus boot replay |

## Performance investigations & campaigns

| Doc | What it holds |
|---|---|
| [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) | The consolidated >500 campaign record: goal, forced-march log, close-out scoreboard, plain-language RX story + diagrams, gigabit headroom analysis |
| [CAMPAIGN_500_PLAN.md (archived)](../history/v1/findings/CAMPAIGN_500_PLAN.md) | The campaign plan + status ledger (superseded banners intact) |
| [RX_TX_PERFORMANCE.md (archived)](../history/v1/findings/RX_TX_PERFORMANCE.md) | The 07-09 campaign narrative (merged into [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) 2026-07-25) |
| [GIGABIT_HEADROOM_ANALYSIS.md (archived)](../history/v1/findings/GIGABIT_HEADROOM_ANALYSIS.md) | Headroom at 100 MHz; wire-rate tables (merged into [PERFORMANCE_GOAL.md](PERFORMANCE_GOAL.md) 2026-07-25) |
| [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) | Why single-port TCP capped at 30 Mbit/s: memory latency decomposition (1424 ns/miss), the 112.5 MHz build-and-revert, retracted theories kept as lessons; Section 2.1 = the folded second-core prequel |
| [SINGLE_PORT_PERF.md (archived)](../history/v1/findings/SINGLE_PORT_PERF.md) | Would a second core help a single flow? (No - latency-bound; merged into [LATENCY_INVESTIGATION.md](LATENCY_INVESTIGATION.md) 2026-07-25) |
| [TX_READER_PREFETCH_PLAN.md (archived)](../history/v1/findings/TX_READER_PREFETCH_PLAN.md) | A full plan whose measured verdict is **do not build it** (kept as the refutation record) |
| [Historical RX performance tuning map](../history/v1/findings/RX_PERF_TUNING_MAP.md) | Retired host-driver pairings and measurements |
| [Historical board profiling method](../history/v1/findings/PERF_ON_MILAN.md) | Retired runtime measurements and attribution method |

On-silicon evidence logs live in
[`sw/litex/evidence/`](../../sw/litex/evidence) (BIOS banners, memtest, the
M-A3 DMA write-up [`hw_ma3_dma_datapath_100mhz.md`](../../sw/litex/evidence/hw_ma3_dma_datapath_100mhz.md)).

## Bench operations

| Doc | What it holds |
|---|---|
| [BENCH_TOPOLOGY.md](BENCH_TOPOLOGY.md) | Bench-ops onboarding: where-is-what + the physical/tap topology |
| [FLASH_0x0014_0727.md](FLASH_0x0014_0727.md) | 2026-07-27 the area round on silicon: 3 seeds placed and ALL MET TIMING (best WNS +0.147), -5,216 LUT delivered vs -4,847 estimated, but slice occupancy only 99.93 % -> 99.65 % (55 free) so the design is still slice-bound; flashed bitstream-only, VERSION 0x0001_0014 and the five-queue map read back from hardware, smoke 5/5, parsed == matched exactly |
| [STRESS_0726.md](STRESS_0726.md) | 2026-07-26 adversarial campaign: 19 checks, 0 failures — stop/start storms, illegal CSR access, engine cycling, boundary sids, and the entry-0 blocker triggered ON PURPOSE to prove the root cause by causation |
| [LIVE_BENCH_0726.md](LIVE_BENCH_0726.md) | 2026-07-26 live health + function sweep of both boards: gPTP converged, bidirectional streaming, 0 format errors over ~2 G frames, live audio capture, and the two known tie-offs observed on silicon |

## Conventions

* Every finding doc opens with its date and, when superseded, a banner
  naming what replaced it. Nothing here is deleted - refuted theories are
  retained and marked, because the refutations are the value. The one
  exception is #259: a finding measured on the retired host path leaves the
  checkout for git history, and this page records that it did.
* Diagrams are generated: edit the sibling `*.gen.py` under `docs/`, never
  the `.svg`/`.png` outputs.
