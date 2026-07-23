> ⚠️ **SUPERSEDED / HISTORICAL** — archived 2026-07-23. Kept for history; **not current state**.
> Living successor: `findings/PERFORMANCE_GOAL.md` + `CHANGELOG.md`. Index: `docs/archive/README.md`; orientation: `docs/SYSTEMS_ENGINEER_GUIDE.md`.

# Campaign plan: >500 Mbit/s TX *and* RX  -  every step gated by a gateware measurement

> **STATUS: SUPERSEDED by the measured record (2026-07-11).** Outcome: TX 582–646 ✓; TCP-socket RX plateaus at 381/374 (ACK-hold law  -  see RX_PERF_TUNING_MAP.drawio); the >500 RX lane is the no-copy consumer (MSG_TRUNC ceiling 585–594 measured; recv_zc on hs@4K = the open experiment). Current plan lives in SESSION_HANDOFF.md.


> 📌 **Current state lives in [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md)** (+ [`../CHANGELOG.md`](../../CHANGELOG.md)). This doc's older scoreboard rows/roadmap predate the mlp3 + perf findings (RX −P2 298, ceiling 481; TX −P2 crosses 500; next RX lever = DDIO).

*Successor plan to the 2026-07-07/08 sessions (CBS default bug, both RX wedges  -  see
[`PERFORMANCE_GOAL.md`](PERFORMANCE_GOAL.md), [`RX_OVERLOAD_WEDGE.md`](RX_OVERLOAD_WEDGE.md),
[`CBS_DEFAULT_SHAPING_BUG.md`](CBS_DEFAULT_SHAPING_BUG.md)). Written 2026-07-08.*

## DECISION (2026-07-08): stay at 100 MHz; next lever = L2/memory

Phase X measured 112.5 MHz = only **+4–8 %** TX (508 projection refuted) at real cost
(thin timing, SPI-read workaround, wrong board timebase). **100 MHz (`build_dp100_m1`) is
the standard baseline.** The two RTL changes 112.5 forced  -  reader-source `stream.Buffer`
(critical-path relief) and single-lane SPI flash read (robust boot)  -  are committed and
carry forward (harmless at 100 MHz). **More cores rejected**: TX isn't hart-bound (proven),
and RX BRAM won't fit (m1 already 76 %) + 2-hart RX scaling is only +24 % (memory-contended,
not core-bound). **Next lever = grow the shared L2 (32 KB → 64 KB)** to open the +24%-not-2×
RX fan-out gap  -  orthogonal to sys clock, the measured memory wall is the real ceiling. Full memory-hierarchy
decision tree (cold vs capacity, and the dedicated-network-cache branch): **`RX_MEMORY_HIERARCHY_PLAN.md`**.

## STATUS LEDGER (2026-07-08, end of first execution day)

| phase | status | gate outcome |
|---|---|---|
| M1 instrumentation | ✅ `7c024b3` | `build_dp100_m1` WNS +0.056, §V clean, 17 CSRs appended-only |
| R0 re-baseline | ✅ `a3492fd` | 12-cell signed table, zero wedges, books balance |
| R1 2-queue fan-out | ✅ `599fb00` | LIVE at 100 MHz, 10/10 storm rounds; split rounds 230–238 0-retr; **238 = both-harts-99 % CPU ceiling** (hands ≥300 to X/cost cuts) |
| R2 RSC geometry | ⚠ partially refuted | close-reasons: **park 58 %/psh 41 %/cap 0 %**, ratio 7.8–9.5 → window/cap tuning buys nothing; copybreak sweep hash-lottery-confounded  -  redo split-classified if revisited |
| T1 TX levers | ✅ **452 Mbit** `44e785c` | gate ≥420 MET; real levers = **board `rx-usecs` 2000 + softirq NAPI**; peer knob mild ±5 % (first sweep was phantom  -  peer ethtool needs `sudo -n`) |
| T2 completion-IRQ | ⏸ deprioritized by measurement | IRQ fires per packet; delivery ~1.0 ms fixed, poll-independent (threaded-NAPI wake was 0.65 ms  -  `threaded=0` now standard); **latency is not the 500-blocker** |
| T3 2nd TX queue | ⛔ refuted by proxy | dual-process at the operating point = 341 < 417 single-process −P4 |
| X clock | 🟡 **RTL WIN, measurement blocked** | 106.25 REFUTED (no PLL config: sys must coexist w/ milan=100 from 200 MHz → only 100/112.5 valid). **112.5 MHz now CLOSES: WNS +0.038** via a `stream.Buffer` register between the TX reader source and the CDC (`d35f666`) that cuts the assembly-cone violators  -  reader RTL untouched, CSR identical, sims pass. **Throughput unmeasured: QSPI flashboot fails CRC at 112.5** (SPI-flash read clock marginal). Fix = `add_spi_flash(clk_freq=25e6)` (cap SPI clk independent of sys) or serial-boot → one rebuild. **TX ~508 stays a PROJECTION until booted.** |

**Scoreboard (updated 2026-07-09): TX −P2 525–536 (✓ crosses 500) · RX −P2 298 (ceiling 481 once the copy is removed). Next RX lever = DDIO  -  see [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md).** (Historical below: TX 452 / RX 238.)** Operating point: peer(sudo) `rx-usecs` 50–200,
board `rx-usecs` 2000, `threaded=0`, `hash_sel=0`, MTU 1500.

**Honest gap assessment:** TX closes with X (106.25 + top-of-band, or the 112.5 unlock).
RX cannot reach 500 on this 2-hart/100-ish-MHz CPU by tuning  -  the measured ceiling is
CPU per-frame cost with both harts pegged; beyond X (~253), RX needs structural work:
the reader-cone pipeline (enables 112.5), >2 queues or per-queue aggregate slots (park
58 % tax), or delivery-path cost cuts  -  all RTL-scale, all now precisely quantified.

## The rule (what "carefully" means here)

Three sessions of evidence say intuition on this platform is wrong more often than right
(prefetch refuted; CBS default; two invisible wedges; the 256-BD landmine). Therefore this
plan is a **measurement contract**:

1. **No lever is built before its gateware measurement exists.** If the deciding number
   cannot be read from a CSR today, the instrumentation ships (and is validated) first.
2. **Every phase has a numeric gate** read from HW counters *and* `/proc/stat` together  - 
   the books must balance (Σ cycle-buckets == cyc; frames conserved across stages).
3. **Every bitstream passes the validation checklist** (§V) before its numbers count.
4. Fixes/levers land one per build wherever possible, so WNS and behavior changes stay
   attributable.

## Where we are (all measured on silicon, 2026-07-08, `build_dp100_v2fix`, WNS +0.123)

| metric | value | evidence |
|---|---|---|
| TX best stable | **354** (2-proc) / 339 (−P4 u1000) / 265 single | CPU 84–96 % busy (`/proc/stat`), reader idle 809 ‰ (`txrd_*`) |
| RX single (rsc=1) | **192–202** | v2fix storm run |
| RX parallel (1 queue) | **145 (−P2) / 112 (−P4)**  -  *stable at last* | v2fix storm run, canary 0, drops 4792 |
| Storm safety | previously-fatal storm sequence passes end-to-end | `RX_OVERLOAD_WEDGE.md` §Status |
| Idle RTT | 3–11 ms (delivery rides the 5 ms fallback poll) | irq 13 fires; `rx-usecs-low` ≤200 µs = CPU storm |
| Deep limit | 1424 ns/miss memory latency | `LATENCY_INVESTIGATION.md` |

**Gap arithmetic:** TX 354 → 500 = **+41 %** against a CPU wall. RX 202 → 500 = **+150 %**,
which no single-queue tuning can reach  -  it *requires* the 2-queue fan-out (×~2 across
harts) plus per-aggregate cost cuts. Parallel RX today (145 < 192 single) splits one
queue's capacity; the fan-out is where parallel gains live.

## Existing gateware measurement surface (validated this campaign)

- **Stage probes** (frames/beats/stalls): `tx_dma/tx_dp/tx_core` @`0xf0004010–30`,
  `rx_core/rx_dp/rx_dma(q0)` @`0xf0004034–54`, wire @`0xf0004058/5c`.
- **Datapath-input probe** `txdp_in` busy/stall/starve/cyc @`0xf0004060–6c`.
- **Reader Phase-0 probes**: `txrd_lat_*` (AR→R latency) @`f0004088–a0`; `txrd_*`
  7-bucket cycle breakdown @`f00040a4–c0`; `rxw/rx1w_out_hi` @`f00040c4/c8`.
- **Writer telemetry per queue**: wr/rd/dropped/frames/occ_hi/posted/rsc_dbg/acks_merged
  (q0 @`f0003024–74`, q1 @`f0003084–…`), steer `q0/q1_frames` @`f0003078/7c`,
  `hash_sel` @`f0003080`, `irqs` (empty→non-empty edges) @`f0003050`.
- **Coherent capture**: `reset` @`f0004000`, `capture` @`f0004004` (rising edge).
- **Sim regression net**: `test_ring_bd.py` 27 tests (StormModel: conservation,
  byte-exact content, FIFO-quiesce), reader/writeback/steer suites, `csr` 76 checks.

## Phase M1  -  instrumentation build (FIRST: the probes the plan needs)

**Goal:** one build (`build_dp100_m1`) adding every counter the later phases gate on.
All sys-domain `MilanDebug` extras (~a few hundred FFs, off critical paths  -  the Phase-0
pattern, which cost 0 WNS).

| new probe | what it answers | consumer phase |
|---|---|---|
| `rx1_dma` stage probe (`sys_probe` on `rx1.sink`) | do frames reach queue 1 / where do they stall | R1 |
| steer output stall counters (`source0/1` valid&~ready) | does the steer back-pressure (steer vs writer attribution) | R1 |
| **RSC close-reason counters** (psh / seg-cap / timeout / newcomer / famine) in `RingDMAWriter` | which close path bounds aggregate size → what to tune (window vs cap vs flow-churn) | R2 |
| v2 BD count + Σsegs (aggregation ratio = Σsegs/v2) | measured coalesce factor per config | R2 |
| **TX ring occupancy high-water** (reader `wr−rd` max) | is the CPU keeping the TX ring fed (complements `txrd_idle`) | T1/T2/T3 |
| TX doorbell count (wr_ptr writes) | xmit batching factor (frames/doorbell) | T1/T3 |
| per-queue IRQ counter (q1 `irqs` exists  -  verify wired) | IRQ-NAPI validation | T2 |

**Gate to proceed:** 27/27 + reader sims green; elaboration CSR map appended-only
(existing addresses unchanged); build WNS ≥ +0.05; checklist §V passes on silicon.
**This build is also the standing baseline bitstream for the whole campaign.**

## Phase R0  -  full re-baseline on the instrumented, storm-proof gateware

Everything measured before v2fix predates the wedge fixes and (for TX) predates storm
safety. **Re-baseline TX and RX on `build_dp100_m1` before touching any lever** so every
later delta is attributable.

- Protocol: orchestrated matrix  -  TX {single, −P4, −P8, dual-proc} × u{500,1000},
  RX {single, −P2, −P4} × u{500,1000}; probes captured per run; `/proc/stat` per run;
  canary + drops read after every test. (TX −P8 was never stably measurable before  - 
  it may already beat 354.)
- **Gateware measurement:** full probe capture per cell; books-balance assert
  (`txrd` Σbuckets == cyc; stage frame conservation wire→dma; steer q0+q1 == rx frames).
- **Gate:** a signed-off baseline table in `PERFORMANCE_GOAL.md`; no unexplained
  counter imbalance. Duration ≈ 1 session.

## Phase R1  -  RX 2-queue fan-out at 100 MHz (the mandatory RX lever)

**Hypothesis:** the historical "RxSteer hangs at 100 MHz" was the (now-fixed) wedges, not
timing  -  v2fix's +0.123 margin and the storm-proof BD path make the fan-out viable; two
queues → two NAPIs → two harts ≈ 2× the 145 −P2 number.

- Steps: `hash_sel=0`, 2-queue driver paths (rsc per queue), −P2/−P4 with flows split.
- **Gateware measurement:** steer `q0/q1_frames` split ratio; `rx1_dma` stage probe
  (frames flow / stalls); per-queue `dropped/occ_hi/irqs`; canary on BOTH queues;
  steer-output stall counters (if the steer itself back-pressures → RTL attention).
- **Gate:** RX −P2 ≥ **300** with both queues delivering (each ≥40 % of frames), zero
  wedge across 10 consecutive storm rounds. **Fallback** if it hangs: the wedge-forensics
  toolkit (stage probes + BD dumps + canary) now localizes in minutes; fix-in-sim first
  (`test_rx_steer.py` gets a StormModel-style checker).

## Phase R2  -  RX per-aggregate cost: RSC geometry + delivery tuning

**Hypothesis:** with 2 queues live, the wall returns to per-aggregate CPU cost; the close
-reason counters say which knob buys aggregation (bigger window? seg-cap 16 → RTL bump?
flow churn?). Driver-side: `copybreak` linear-size sweep, GRO interplay.

- **Gateware measurement:** close-reason histogram + aggregation ratio (Σsegs/v2) per
  config  -  the DIRECT measure of coalescing; per-queue frames/s vs CPU %.
- Levers in measured order: `rx-usecs` per-queue sweep on m1; if timeout-closes dominate
  → window up; if seg-cap dominates → RTL `agg_segs` cap 16→32 (BD `segs` field is 8-bit,
  driver handles ≥16 already)  -  **one-line RTL, but only if the counter says so**;
  copybreak sweep (128/192/256).
- **Gate:** RX −P2 ≥ **400**; books balance. If CPU saturates both harts before 400 →
  jump to Phase X (clock) with the evidence in hand.

## Phase T1  -  TX cheap levers on the storm-proof board (no code changes)

Storm safety unlocks configs that previously wedged the ACK path.

- Matrix: −P8/−P16, dual-process × {u1000, u2000}, **peer-side `rx-usecs` 100–200**
  (moderate ACK batching at the source  -  peer 1000 over-batched to collapse, peer 3
  is too chatty; the sweet spot was never measured cleanly), TSQ/wmem nudges.
- **Gateware measurement:** `txrd_*` breakdown (idle must fall if a lever works),
  TX-ring occupancy high-water (ring should stay non-empty), doorbell batching factor,
  ACK-side: q0 `acks_merged` + RX frame rate during TX.
- **Gate:** TX ≥ **420** stable → T2 next. If `txrd_idle` stays >700 ‰ while CPU <90 % →
  latency-bound, prioritize T2.

## Phase T2  -  completion-IRQ NAPI (driver; helps both directions)

**Hypothesis:** delivery rides the 5 ms fallback poll (idle RTT 3–11 ms) although irq 13
fires; IRQ-driven `napi_schedule` with the poll demoted to a true fallback cuts RTT
~30× → TCP cwnd ramps and TX-completion reap latency drops; RX batching becomes
IRQ-paced instead of timer-paced.

- Driver work: trust `kl_irq` → NAPI as the primary path; re-enable per the level/edge
  semantics measured on the PLIC ("3 Edge"); `rx-usecs-low` becomes a safety net (≥5 ms).
- **Gateware measurement:** `irqs` counter delta vs frames (batching factor), poll-count
  (`hb n`) collapse, idle RTT before/after (3–11 ms → target <1 ms), and the T1/R1
  matrices re-run  -  deltas attributed to latency.
- **Gate:** idle RTT < 1 ms AND (TX single ≥ 300 or measured cwnd-limit removal);
  no wedge in 10 storm rounds (the IRQ path reorders reap timing  -  canary watches).

## Phase T3 (conditional)  -  second TX queue (RTL) if T1+T2 < 500 TX

Only if the **measured** signature says xmit-path serialization binds: dual-process
scaling efficiency <1.3× AND both harts <90 % CPU AND TX ring occupancy high-water low
(CPU can't feed one ring from two sockets). RTL: second `RingDMAReader` + TX BD ring +
netdev `mq` (XPS hart-per-queue)  -  mirrors the RX fan-out design. **Instrumentation
ships in the same build**: tx1 ring CSRs + `tx1_dma` stage probe + per-queue doorbells.
Gate: TX ≥ 500 dual-socket; datapath merge (classifier accepts 2 sources or round-robin
mux before `s_axis`) validated by `tb/verilator` first.

## Phase X (conditional)  -  clock/memory, the deep levers

If either direction stalls short of 500 with CPU saturated (the honest possibility:
2×100 MHz in-order RV64 may cap near ~450 RX / ~450 TX):

1. **sys 100 → 112.5 MHz** floorplan build (`build_vexii_fp` precedent exists)  - 
   +12.5 % CPU across the board. Gate: WNS ≥ 0, DDR3 timing clean, full storm checklist.
2. L2 32 KB → 64 KB (config knob; measured via the 1424 ns/miss profile re-run).
3. Only then: bigger guns (3rd hart / higher-IPC config)  -  out of scope for this plan.

**Gateware measurement:** same probe surface re-based; the per-frame cycle costs
(`txrd` buckets, aggregation ratio) are the before/after units, not just Mbit/s.

## §V  -  bitstream validation checklist (every flash, before any numbers count)

1. `devmem 0x90000000` == `MILN`; CBS `en q0–q3 == 0` at reset (the default stays fixed).
2. `test_ring_bd.py` 27/27 + `tb/verilator/csr` 76/76 green at the matching commit.
3. Post-route **WNS ≥ +0.05** recorded in the build log and the session notes.
4. Storm smoke: the GSEQ sequence (single→P2→P4→P2→single) passes with pings alive,
   **canary == 0**, and sane drops.
5. Probe sanity: `capture` pulse → books balance on an idle window (Σbuckets == cyc).
6. CSR map diff vs previous build: appended-only (driver ABI intact).

## Gate summary (the plan on one line each)

| phase | lever | gateware gate | target |
|---|---|---|---|
| M1 | instrumentation build | checklist §V; probes readable; WNS ≥ +0.05 |  -  |
| R0 | re-baseline | books balance across full matrix | signed baseline |
| R1 | RX 2-queue @100 MHz | q0/q1 split healthy, canary 0, 10 storm rounds | RX −P2 ≥ 300 |
| R2 | RSC geometry + copybreak | close-reason histogram drives each knob | RX ≥ 400 |
| T1 | TX config levers (−P8, peer coalesce) | `txrd_idle` falls; ring occ high | TX ≥ 420 |
| T2 | completion-IRQ NAPI | `irqs`/poll deltas; RTT < 1 ms | TX single ≥ 300; both directions lifted |
| T3* | 2nd TX queue (RTL) | dual-scaling proxy demands it | TX ≥ 500 |
| X* | 112.5 MHz / L2 | per-frame cycle costs re-measured | close the last gap |

\* conditional  -  built only if the preceding gates' measurements demand it.

**Sequencing:** M1 → R0 → (R1‖T1 interleaved on the board) → R2 → T2 → gates decide
T3/X. Expected: RX crosses 500 via R1+R2+T2 (2×192 with cheaper aggregates and IRQ
pacing); TX crosses via T1+T2 (+T3 if the proxy demands). If both saturate CPU short of
500, Phase X carries the remainder  -  with the per-frame cycle evidence to prove it's
the CPU and not another hidden shaper.
