[OBSOLETE + 2026-09-01]

> Status: Historical
>
> Original path: `docs/findings/PERFORMANCE_GOAL.md`
>
> Archived: 2026-09-02
>
> Relocated: 2026-09-02
>
> Current successor: [open current documentation](../../../overview/FULL_FPGA_SOLUTION.md)

<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Throughput campaign record — >500 Mbit/s RX and TX (closed 2026-07-10/11)

This page is the archived measurement record of the 2026-07 throughput
campaign. The campaign ran on the **retired measured platform**: two RV64
harts at 100 MHz servicing packets through the removed target stack on the
AX7101 board, MTU 1500 everywhere. The shipping product is a self-contained
fabric datapath with a single bare-metal RV32 control CPU that carries no
product packets, so nothing here describes current behavior — the
[current performance model](../../../overview/FULL_FPGA_SOLUTION.md#5-performance-model)
grades the product by timing closure and board-wire measurements instead.
Every number below is a silicon measurement from the campaign and is
preserved unchanged. The full original page, with its complete phase-by-phase
prose, remains in Git history only (the #259 completion removed the retired
platform's documentation from the checkout; the file is present at commit
`59ba6ffb`).

## Contents

- **[Goal and platform](#goal-and-platform)** — What the campaign chased and what it measured on.
- **[Final scoreboard — reconciled at campaign close (2026-07-11)](#final-scoreboard--reconciled-at-campaign-close-2026-07-11)** — The one reconciled record table, its close-out method, and the verdict.
- **[Waypoint lineage](#waypoint-lineage)** — Every dated RX and TX waypoint from R0 to close, per build.
- **[Dated phase results](#dated-phase-results)** — R0 baseline matrix, the fan-out, the TX ladder, the 112.5 MHz refutation, and the two structural RX wins.
- **[The lever ledger and the campaign chart](#the-lever-ledger-and-the-campaign-chart)** — The measured effect of each memory-hierarchy lever, with the archived chart and its generator.
- **[Budget model at close](#budget-model-at-close)** — Cycles-per-byte accounting that explains why the residual was not silicon.
- **[Refuted levers (measured — the campaign said do not retry)](#refuted-levers-measured--the-campaign-said-do-not-retry)** — Everything measured flat or dead, with the numbers that killed it.
- **[Commit and build references](#commit-and-build-references)** — The gateware builds, driver revisions, and commits the record cites.

## Goal and platform

1. **Sustain > 500 Mbit/s best-effort TCP in both directions** (RX and TX) at
   MTU 1500. Raised 2026-07-07 from the prior ≥200 milestone, which was met
   (measured: TX 238–247, RX 209/223).
2. **Reach toward 1 Gbit/s (PHY line rate)** wherever the hardware allows.

The PHY is 1 GbE and the 64-bit datapath has ample raw bandwidth
(3.2 Gbit/s at 50 MHz, 6.4 Gbit/s at 100 MHz), so the gap was a *system*
problem — per-frame CPU cost, DMA and memory latency — never a wire limit.
Ground rules held for every cell: MTU stays 1500; hardware and stack counters
are read side by side and the books must balance; the driver identity is
verified on every run.

## Final scoreboard — reconciled at campaign close (2026-07-11)

Three documents froze this campaign's scoreboard at different dates with
conflicting numbers; each was a dated waypoint of a moving system. This table
is the one reconciled record. Close-out method for every record row: peer
`tx_bytes` 5-second deltas, first and last intervals excluded, fresh client
ports per cell, TX gate after every RX change.

| metric | record | date | build (gateware + driver) |
|---|:--:|:--:|---|
| **TX TCP** | **582–646** | 2026-07-10/11 | `build_hsq8`/`build_hsq10` TX gates + driver `hsplit11`/`hsplit12` |
| **RX TCP, real `recv()` copies** | **381 steady / 374 over a 120 s soak** (−P4 2:2) | 2026-07-10/11 | `build_hsq10` (16 KB pages) + `hsplit12` |
| RX TCP single-flow | **329** (cut-through) | 2026-07-11 | `build_hsq12` + `hsplit14` |
| **RX no-copy stack ceiling, page-split era** | **585–594** (`MSG_TRUNC`, sustained) | 2026-07-11 | `build_hsq10` keeper + `recv_trunc` |
| RX no-copy stack ceiling, multi-slot era | **925** (`MSG_TRUNC` −P2, ~98 % of the ~941 wire ceiling) | 2026-07-09 eve | `build_r2slots` + `mslot60c` (60 KB receive aggregates) |
| RX steady, multi-slot keeper | 368–407 (−P8, peer time-series) | 2026-07-09/10 | `build_r2slots` + `mslot60d` |
| UDP TX / RX goodput | 24 / 65 | 2026-07-11 | keeper (no UDP segmentation or coalescing offloads) |

**Verdict: both directions crossed 500** — TX 582–646, RX 585–594 no-copy.
The socket `recv()` path closed at 381/374: the residual was the retired
runtime's socket layer — its payload copy and per-call envelope on two
100 MHz in-order harts — not the silicon. The data plane itself measured 925
of a ~941 wire ceiling. The two no-copy ceilings are different buffer
geometries, not a contradiction: 925 was measured on the 60 KB multi-slot
receive-coalescing generation, 585–594 on the 16 KB page-split keeper
generation.

## Waypoint lineage

RX −P2/−P4: 165 (07-08, `build_dp100_m1` R0) → 230–238 (07-08, m1 + 2-queue
fan-out) → 280 (`build_l2x2`) → 298 (`build_mlp3`) → 316 (07-09,
`build_l2deep`) → 368–407 −P8 steady (07-09/10, `build_r2slots`) →
**381/374** (07-10/11, `build_hsq10`).

TX: 238–247 (07-07, `build_dp100_p0`, CBS-paced) → 452 −P4 (07-08,
`build_dp100_m1` T1) → 525–536 −P2 (07-09, `build_l2x2`/`build_mlp3` A/B) →
513 −P4 (07-09, `build_r2slots`) → **582–646** (07-10/11, hsq series).

## Dated phase results

**R0 baseline (signed 2026-07-08, `build_dp100_m1`, WNS +0.056).** 12-cell
matrix, per-cell coherent probe capture, zero wedges, canary 0 throughout.

| cell | u500 | u1000 | evidence highlights |
|---|:--:|:--:|---|
| TX single | 174 | **253** | wakeup-cost effect confirmed on m1 |
| TX −P4 | **~306** | ~283 | reader idle 73 % — CPU feed still the wall |
| TX −P8 | ~294 | ~249 | first stable −P8 numbers |
| RX single | **206** | 191 | |
| RX −P2 | 165 (1172 retr) | 140 (1682 retr) | famine drops 13k/cell → retransmit tax |
| RX −P4 | 106 (2173 retr) | 103 (1934 retr) | famine drops 15.7k/cell |

R0's close-reason counters read: park 58 %, psh 41 %, timeout 1 %, seg-cap
0 %; coalesce ratio 7.8 segments per aggregate — parallel RX paid a measured
famine-plus-retransmit tax and a park-close tax.

**R1 — 2-queue fan-out (2026-07-08, `build_dp100_m1`, hash_sel=0).** The
fan-out works: 15/15 cells plus 10/10 −P2 storm rounds healthy, canary 0.
Results are bimodal on the 4-tuple hash: a clean split (52/48 measured)
gives **RX −P2 230–238 with 0 retransmits** (+22 % over single-flow 195);
a collision (~50 % of 2-flow rounds) gives 133–144 with 1.2–1.7 k
retransmits. Split rounds cap at 238 with both harts 99–100 % busy — the
2-hart CPU ceiling at the then-current per-frame cost.

**T1 — TX coalesce ladder (2026-07-08, corrected).** The genuine peer-side
sweep at the real operating point measured 437/435/452/424 Mbit/s (peer
3/50/200/1000 µs, all 0 retransmits): the peer knob is mild (±5 %). The real
levers were board-side — the board coalesce ladder 500 → 1000 → 2000 µs
scaled TX −P4 236 → 352 → 415/417, and the corrected record is **TX 452**
(gate ≥420 met). Single-flow TX 350. The first sweep's peer cells had never
applied (suppressed permission errors); the correction is part of the record.

**Phase X — 112.5 MHz refutes the linear projection (2026-07-08).** The
higher system clock closed timing (WNS +0.038 after a one-stage buffer cut
the TX reader's cone, commit `d35f666`) and booted after the single-lane
SPI-flash fix (`a80c955`).

| path | 100 MHz | 112.5 MHz | Δ | vs +12.5 % ideal |
|---|:--:|:--:|:--:|:--:|
| TX −P4 (operating point) | 452 | **459–479** (avg ~470) | **+4 %** | ⅓ of ideal |
| TX single | 350 | **379** | **+8 %** | ⅔ of ideal |

The datapath stayed at 100 MHz, so neither direction reaches 500 by CPU
clock alone; the 508 projection was refuted by measurement.

**R1 warm-copy — refuted with a mechanism (2026-07-09 eve).** Bounded
receive windows are throttled by a structural ~1 ms receive-window
turnaround cycle at 100 MHz (ICMP turnaround 0.574 ms tight; sleep-wake
340–560 µs per leg), so rate ≈ window/1.2 ms ≈ 100–240 Mbit for 48–384 KB
buffers regardless of copy warmth; unbounded windows self-defeat cache
residency (1–3 MB standing receive queue ⇒ cold copy). A busy-poll receiver
measured +8 % over the baseline load generator.

**R2 — multi-slot receive coalescing, the structural win (2026-07-09 eve,
`build_r2slots`, WNS +0.018, driver commits
`a238f84`/`98b9708`/`b880cdf`/`5c6f1a6`).** Park was 90 % of aggregate
closes at −P2 and aggregates were 16 KB-buffer-bound at 10.6 segments; four
aggregate slots × 60 KB buffers (segment cap 60, age max 2 ms) with a
pop-ordered completion queue took the no-copy ceiling **458 → 925 Mbit**
(~93 % of line rate), coalesce ratio 10.6 → 22.8, TX −P4 513 with no
regression. Close-reason histogram at −P2 after the win: psh 55 %,
rollover-park 45 %, timeout 0.2 %, cap/age 0.

**Close — page-aligned payload split in the RX writer (2026-07-10/11, `hsq`
build series).** Splitting headers from page-aligned payload carried RX
with-copy to 381/374 and no-copy to 585–594, and TX to 582–646. The
page-flip consumer itself measured 110–113 Mbit at 87 % flipped — the flip
loses to the aligned copy on this core — so what landed was the aligned-copy
win: the misaligned copy path (5 operations per 8 bytes, 83.2 % of the app
hart's cycles at steady −P8 334 Mbit) became the aligned path
(~0.25–0.3 cycles/byte versus the misaligned 0.64).

## The lever ledger and the campaign chart

The whole campaign on one chart (archived render; regenerate with
`python3 docs/history/v1/diagrams/perf_campaign_chart.py docs/history/v1/diagrams/perf_campaign.svg`):

![campaign chart](../diagrams/perf_campaign.svg)

| lever | effect | note |
|---|---|---|
| 64 KB L2 | RX −P2 238 → **280** | capacity (both harts) |
| refill=8 alone | 229 ≈ 238 (**no gain**) | in-order core; slots need a filler |
| **RPT prefetcher** | RX single 207 → **277** (+34 %) | fills the slots; +2 BRAM tiles |
| mlp3 (all three) | RX −P2 = **298** | slots cost 0 BRAM |
| **L2→DRAM depth 8** (l2deep) | RX −P2 = **316** | `downPendingMax` 4→8; knee at 8 (16 flat) |
| shared-L2 DDIO | ~300 (**flat**) | allocate-on-DMA-write pollutes without warming |
| *ceiling if copy removed* | RX −P2 = **481** | via `recv(MSG_TRUNC)` on the pre-multi-slot stack |

The deep limit under every lever: memory latency measured **1424 ns per
miss** (≈50 % address-translation walk + 50 % DRAM) on DDR3-800 with the
32 KB L2 — both directions were ultimately gated by how fast a 100 MHz
in-order core touches uncached DMA memory per frame.

## Budget model at close

Two harts × 100 MHz = 200 M cycles/s. Wire ceiling at MTU 1500: ~941 Mbit/s
TCP goodput.

| regime | throughput | system cycles/byte |
|---|:--:|:--:|
| no-copy stack (925 Mbit) | 115.6 MB/s | **1.73** |
| with-copy steady (400 Mbit) | 50 MB/s | **4.0** |
| wire (941 Mbit) | 117.6 MB/s | 1.70 |

Of the with-copy 4.0 cycles/byte, the raw cold copy was only 0.64 (26.37
µs/4 KB measured); the rest was the per-call envelope and a ~25 % full-queue
tax (steady 390 versus ≥520 transient on identical machinery). Batched
trap-free page-table moves measured 1.22 µs/page — 21.5× cheaper than the
copy — which is what justified the closing page-split lever. Even a free
copy inside the unmodified receive path left ~3.4 cycles/byte ≈ ~470 Mbit:
reaching the wire meant removing bytes from that path, not polishing it.

## Refuted levers (measured — the campaign said do not retry)

- TX reader prefetch (2026-07-07): reader only 3.8 % busy; payload latency
  45 cycles (450 ns, not the ~140 ns assumed); the walls were back-pressure (39 % stall)
  and ring-empty idle (39 %).
- The 39–42 % stall itself: the CBS reset configuration paced best-effort
  traffic at 300 Mb/s (fixed — all queues strict-priority at reset,
  `build_dp100_cbs0`, WNS +0.031; transmit stalls dropped 418‰ → 4‰ live).
- Page-flip zero-copy receive: flip 44.9 µs/page versus cold copy 25.0 —
  flipping loses on this 100 MHz sv39 core.
- BRAM stash for payload residency: standing receive queue 1–3 MB ≫ BRAM.
- Unscoped shared-L2 DDIO: −P2 ~300, flat versus mlp3's 298; single and −P4
  dipped.
- Depth-2 interconnect, L2 > 64 KB, software prefetch, deeper LiteDRAM
  command queues: all flat.
- Prefetch block-ahead 8: copy 27.04 versus 26.37 µs/4 KB, steady −P8
  371–394 ≈ keeper (`build_r2rpt`, WNS −0.077, not a keeper).
- 112.5 MHz as a throughput lever: +4–8 % measured against +12.5 % ideal;
  three later rebuilds at best WNS −0.036 corrupted QSPI reads on-die.
- A third hart: slices 98.24 %, LUTs 82.7 %, BRAM 83.3 % — does not fit
  beside this datapath on the xc7a100t.
- Aggregates past 64 KB: 16-bit length fields and the 64 KB delivery cap
  make 60 KB the practical maximum.

## Commit and build references

| reference | what it names |
|---|---|
| `34cc2bc` | CBS reset-shaping fix (best effort unshaped at reset) |
| `09e3a09` | RX completion-order wedge fix (aggregate-open gate) |
| `2c44757` | second RX wedge fix (drops-field marker alias) |
| `83aa7ec` | driver address-verify realign guard kept as defense-in-depth |
| `d35f666` | TX reader source buffer stage (112.5 MHz timing) |
| `a80c955` | single-lane SPI-flash read (112.5 MHz boot) |
| `a238f84`/`98b9708`/`b880cdf`/`5c6f1a6` | multi-slot receive-coalescing driver series |
| `build_dp100_p0`/`_m1`/`_cbs0`/`_wfix`/`_v2fix`/`_x1125d` | dated 100/112.5 MHz gateware builds |
| `build_l2x2`/`build_mlp1`/`build_mlp2`/`build_mlp3`/`build_l2deep`/`build_r2slots`/`build_r2rpt` | memory-hierarchy lever builds |
| `build_hsq8`/`build_hsq10`/`build_hsq12` | closing page-split build series |
| `hsplit11`/`hsplit12`/`hsplit14`, `mslot60c`/`mslot60d`, `recv_trunc` | driver and tool revisions at the records |

The complete original page — every phase plan, footnote, and evidence index
in full prose — is in Git history only, per the #259 removal of the retired
platform's documentation: `git show 59ba6ffb:docs/findings/PERFORMANCE_GOAL.md`.
The archived chart source and render beside this page reproduce byte-for-byte
(`perf_campaign_chart.py` regenerates `perf_campaign.svg`).
