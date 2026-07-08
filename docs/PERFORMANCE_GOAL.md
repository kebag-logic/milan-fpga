# Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s

**North star for the performance campaign on the fully-FPGA Milan NIC** (Alinx AX7101,
dual VexiiRiscv RV64IMA @100 MHz, 64-bit datapath, MTU 1500 everywhere).

## The goal

1. **Sustain > 500 Mbit/s best-effort TCP in *both* directions** (RX and TX) at MTU 1500.
   **Raised 2026-07-07** from the prior **≥200 milestone, now MET** (measured: TX 238–247, RX
   209/223). 500 needs roughly **2×** the current best in each direction.
2. **Reach toward 1 Gbit/s (PHY line rate)** on both directions wherever the hardware allows.

The NIC's PHY is 1 GbE and the 64-bit datapath has ample raw bandwidth (3.2 Gbit/s @ 50 MHz,
6.4 Gbit/s @ 100 MHz), so 1 Gbit/s is a *system* problem (CPU per-frame cost, DMA latency,
memory latency), not a wire limit. Every step is measured on silicon with HW counters +
CPU profile side by side — no blind changes.

## Where we are (measured on silicon, 2026-07-08)

| path | best measured | ≥500? | bound by | next lever toward 500+ |
|------|:-------------:|:-----:|----------|------------------------|
| TX TCP, 100 MHz dp, **CBS unshaped**³ | **339** (−P4) / **354** (2 proc) / 265 single | ✗ (✓200) | **CPU-saturated** (84–96% both harts) | plan T1/T2/T3: peer-coalesce + −P8 (storms now safe⁴), completion-IRQ, 2nd TX queue if the proxy demands |
| TX TCP, 100 MHz dp, CBS default (historical²) | 238–247 | ✗ | **CBS shaper pacing BE at 300 Mb/s** (config bug — fixed³) | — (fixed) |
| RX TCP single (RSC on) | **192–202** (v2fix, 100 MHz gw) / 209 (50 MHz gw, hist.) | ✗ (✓200) | per-frame CPU, amortized by RSC | plan R2: RSC geometry (close-reason counters) + completion IRQ |
| RX TCP parallel | **145 (−P2) / 112 (−P4), STABLE** (v2fix — both wedges fixed⁴) | ✗ | single queue splits capacity | plan R1: **2-queue fan-out @100 MHz** (≈2× across harts) |
| TX TCP single, 50 MHz (historical) | 145–186¹ | ✗ | superseded by the 100 MHz datapath | — |
| UDP TX / RX | 19.5 / 40 | ✗ | no TSO / no coalescing | USO / UDP-GRO offloads (not built) |

¹ 145 unpinned / 186 pinned-SSH with HW-TSO zerocopy; the datapath-input probe proved the
50 MHz shaper stage was the wall.
² **MEASURED 2026-07-07** on `build_dp100_p0` (reader latency/starve probes, `phase0_measure.sh`,
two runs, rsc250 hwtso+rsc_clk_mhz=100, hash_sel=1): TX **238/247 Mbit/s, 0 retr**. Reader is only
**3.8% busy**; `L_pay = 45 cyc` (450 ns, NOT the ~140 assumed); prefetchable read-latency stall is
only **~13%** and interconnect depth (`rxw_out_hi`) is **2**. So **reader prefetch was refuted** —
the walls were datapath back-pressure (`stall` 39%) and CPU/ring-empty (`idle` 39%). Full evidence:
`docs/TX_READER_PREFETCH_PLAN.md` (MEASURED VERDICT + Appendix A). "Never assume, always measure."
³ **CBS root cause, MEASURED + FIXED 2026-07-08.** The 39–42% datapath-input `stall` was the
**802.1Qav CBS shaper actively pacing best-effort traffic**: `milan_csr` reset `CBS_EN_RST=0011`
shaped **q0 at idleSlope 300 Mb/s** while the default class map (`cls_dpcp=0`, `cls_tcq=0xE4`)
routes untagged/BE traffic exactly to q0 — two defaults contradicting each other (the comment even
says BE stays unshaped per REQ-CBS-02). Verified live on silicon (q0 read back idle=0x11E1A300,
en=1), then clearing en via `devmem 0x9000_040C` dropped `tx_dma` stalls **418‰ → 4‰** on the spot.
Permanent fix: **`CBS_EN_RST = 4'b0000`** (all queues strict-priority at reset; SRP/AVDECC opts SR
classes into shaping) — `tb/verilator/csr` updated (76 checks green), built as `build_dp100_cbs0`
(WNS **+0.031**), **verified at reset on silicon** (q0–q3 en=0). Un-paced TX then measured
265 single / **339 −P4 @ rx-usecs 1000** / **354 dual-process** — now genuinely **CPU-bound**
(`/proc/stat` 84–96% busy; the +23% from rx-usecs 500→1000 = fewer ACK-batch wakeups; iperf3 −P is
single-threaded, hence the dual-process-per-hart test; noZ costs ~20% → zerocopy is load-bearing).
⁴ **RX overload wedge — ROOT-CAUSED IN SIM AND FIXED (2026-07-08, commit `09e3a09`).** Symptom:
parallel RX (−P2) reliably killed RX **delivery** while **every HW stage kept flowing** (stage
probes wire=core=dp=dma in lockstep; writer still committing BDs). Root cause, reproduced by a
minimal deterministic sim (`test_bd_ack_flush_vs_open_agg_order`): the **pending-ACK timeout
flush (`ACK_POP`) pops a NEW posted buffer and completes its v1 BD while an OPEN RSC aggregate
still holds an EARLIER buffer whose v2 BD only comes at close** — completion order inverts
posted-buffer pop order, and the driver's FIFO page pairing (`page[comp_i++]`) then mispairs
every later completion: RX delivery dead, HW healthy. −P2 made it near-certain (two data flows
churn the single aggregate slot so one is almost always open; the iperf control connection's
pure ACKs sit in the merge slot and expire mid-aggregate); single-flow rarely hit the window.
**Fix:** never flush the pending ACK while an aggregate is open — IDLE gates `ack_expired` on
`~agg_open`, and DISPATCH closes the aggregate first for a different-flow mack newcomer (the
extra ACK delay is bounded by the aggregate's own `rsc_tout`). BD order == pop order by
construction. Verified: `test_ring_bd.py` **22/22** — 17 pre-existing + minimal repro + −P2
storm cocktail + heal-race (5 disable phases) + seeded fuzz ×2 against a `DriverModel` that
mirrors kl-eth's reap bit-for-bit. Driver keeps the v1 address-verify realign guard
(`kl-eth 83aa7ec`) as defense-in-depth. Gateware with the fix: `build_dp100_wfix`.
Also seen: idle RTT is 3–11 ms (irq 13 fires but delivery rides the 5 ms fallback poll;
`rx-usecs-low` 200 µs storms the CPU) — a completion-IRQ NAPI is the latency fix, now unblocked.
**UPDATE (later 2026-07-08): a SECOND wedge was subsequently root-caused and fixed** — the v1
BD's 16-bit `drops` field aliased bit 56 (the v2 marker) at drops ≥ 256, making every v1
completion parse as a v2 aggregate under parallel-storm famine (`2c44757`). **Both fixes are
silicon-validated on `build_dp100_v2fix` (WNS +0.123)**: the previously-fatal storm sequence
runs clean (192/145/112/142/196 Mbit, canary 0, drops 4792). Full record:
`docs/RX_OVERLOAD_WEDGE.md`.

**Status vs goal (>500):** ≥200 holds with margin on TX (**354** best stable — was 172 at the
start of the campaign: **2×**, via the measured CBS root cause + coalesce tuning + dual-process).
**Neither direction is at 500 yet — but the wedges that gated every parallel measurement are
fixed and silicon-validated⁴**, so the campaign can finally run. TX is honestly CPU-bound: the
remaining ~40% comes from per-unit CPU cost cuts (peer ACK batching, completion-IRQ, xmit path).
RX needs the 2-queue fan-out (parallel currently splits one queue: 145 −P2 vs 192 single) plus
cheaper aggregates. **The execution plan with per-phase gateware gates is
`docs/CAMPAIGN_500_PLAN.md`.** Reader prefetch stays **refuted**². 1 Gbit/s remains the stretch.
UDP is a separate (offload) problem. Every step measured on silicon — HW counters + `/proc/stat`
side by side; the books must balance.

## R0 baseline (signed, 2026-07-08, `build_dp100_m1` WNS +0.056 — CAMPAIGN_500_PLAN)

12-cell matrix, per-cell coherent probe capture, **zero wedges, canary 0 throughout**;
`txrd` books balance (Σbuckets == cyc); steered/coalesce-ratio ≈ committed BDs.

| cell | u500 | u1000 | evidence highlights |
|---|:--:|:--:|---|
| TX single | 174 | **253** | wakeup-cost effect confirmed on m1 |
| TX −P4 | **~306**¹ | ~283¹ | `txrd` idle 73 % — CPU-feed still the wall |
| TX −P8 | ~294¹ | ~249¹ | first stable −P8 numbers ever |
| RX single | **206** | 191 | |
| RX −P2 | 165 (1172 retr) | 140 (1682 retr) | **famine drops 13k/cell** → retransmit tax |
| RX −P4 | 106 (2173 retr) | 103 (1934 retr) | famine drops 15.7k/cell |

¹ counter-derived (tx_dma frames × 12112 b / txrd_cyc); iperf summary lines lost to a
harvest nit, hardware numbers authoritative.

**What R0 tells the plan:** (a) RX parallel is stable but pays a measured **famine +
retransmit tax** and a **park-close tax** (close reasons: park 58 %, psh 41 %, timeout 1 %,
**seg-cap 0 %**; coalesce ratio 7.8 segs/agg) — R1's 2-queue fan-out attacks *both*
(per-queue buffer pools + per-queue aggregate slots); window/cap tuning would buy nothing,
exactly what the close-reason counters were built to decide. (b) TX −P4 ≈ 306 is the new
single-process reference; T1 starts there toward the 420 gate. (c) The wedge fixes hold
under the full battery.

## R1 result (2026-07-08, `build_dp100_m1`, hash_sel=0 — 2-queue fan-out LIVE)

**The fan-out works and is stable** — the historical "RxSteer hangs at 100 MHz" is gone
(it was the wedges): 15/15 cells + **10/10 −P2 storm rounds healthy, canary 0**. Results
are bimodal on the 4-tuple hash: when 2 flows split (52/48 measured, e.g. steer
q0=107.5k/q1=99.7k), **RX −P2 = 230–238 Mbit with 0 retransmits** (+22 % over single's
195, famine tax eliminated); when both flows collide on one queue (~50 % of 2-flow
rounds), 133–144 with 1.2–1.7 k retr — use ≥4 flows or controlled source ports for
deterministic splits in benchmarks.

**Why split rounds cap at 238, not 2×195:** `/proc/stat` during the 238-Mbit round shows
**both harts 99–100 % busy** — the 2-hart CPU ceiling at the current per-frame cost, read
directly off the counters. The R1 ≥300 gate therefore hands off to **R2** (cheaper
aggregates) and **T2** (completion-IRQ pacing), with **X** (112.5 MHz) as the measured
backstop. Fan-out itself is done and validated.

## T1 result — CORRECTED (2026-07-08): TX **452**, gate ≥420 MET

**Correction (measure-don't-assume applied to ourselves):** the first T1 sweep's
"peer rx-usecs" cells never applied — peer-side `ethtool -C` needs sudo and errors were
suppressed; the peer sat at 1000 µs throughout. The genuine (sudo'd) sweep at the real
operating point (board `rx-usecs=2000`, softirq NAPI `threaded=0`, steer on, −P4):
peer 3/50/200/1000 = **437/435/452/424 Mbit/s, all 0 retr** (repeat band 398–452) —
the peer knob is mild (±5 %); the real levers were **board-side u2000 + softirq**.
Single-flow TX 350. The threaded→softirq switch also cut idle RTT 1.7→1.08 ms
(threaded-NAPI wakeup ≈ 0.65 ms; ~1.0 ms fixed remains, poll-independent, IRQ-per-packet
verified — latency is NOT the 500-blocker, so T2 driver surgery is deprioritized).
**T3 refuted by its proxy**: dual-process at the operating point = 341 < 417 single-process
−P4 — a second TX queue is not the binder; CPU per-byte is.

### (original T1 notes below)
## T1 result (2026-07-08, `build_dp100_m1` — TX gate ≥420 MET at 417)

The never-measured **peer-side coalesce zone** was the lever: peer `rx-usecs` 50 µs +
board `rx-usecs` 2000 µs (steer on) scales TX monotonically — board u500→u1k→u2k =
236→352→**415/417** (−P4, 0 retr, repro band 378–417; u5k 392). **Single-flow TX = 350**
(from 253). Peer 100/200 µs ≈ 293 (too coarse begins ~100); peer 1000 collapses (207,
historical). Fewer, larger ACK batches at BOTH ends = less per-wakeup CPU on the board.

**Still CPU-feed-bound**: at 387 Mbit the reader (`txrd`) is 5.8 % busy / **65.8 % idle**
— T2 (completion-IRQ) and X (112.5 MHz) keep their headroom toward 500. RX stands at 238
(2-hart ceiling, R1); its next lift is also T2/X. Operating point recorded: peer=50,
board=2000, hash_sel=0.

## Phase X status + T2 latency decomposition (2026-07-08)

**X (sys clock) — RTL WIN, throughput measurement pending a boot fix.**
112.5's first build failed WNS −0.226 with **every violator in the TX reader's byte-assembly
cone** (`blen_r → in_last → a_nxt → CDC FIFO write` — the CPU itself closed). A `stream.Buffer`
register stage between the reader `source` and the CDC (`d35f666`) cuts that cone off the
FIFO write-setup path — reader RTL untouched, +1 cycle TX latency, CSR map identical, 28/28
sims — and **112.5 MHz now CLOSES at WNS +0.038** (`build_x1125b`). (106.25 was refuted at
elaboration: no PLL config exists with sys≠100 sharing the 200 MHz input against milan=100 —
only 100 and 112.5 are legal.) **But the throughput number is not yet measured**: QSPI
flashboot fails a CRC at 112.5 (the SPI-flash memory-mapped read clock is sys-derived and
marginal at the higher rate; DRAM/memtest pass, so DRAM is fine). Fix = cap the SPI clock
independent of sys (`add_spi_flash(clk_freq=25e6)`) or serial-boot — one rebuild. **TX ≈ 508
(452 × 1.125) remains a PROJECTION until booted and measured** — never-assume applies to our
own optimism too. RX ≈ 268 likewise. The engineering result (112.5 is reachable) is banked;
the measurement is the immediate next step.

**T2 (latency), decomposed and deprioritized:** with per-packet IRQs verified (`irqs`
delta == ping count) the delivery latency is **poll-independent**: peer→board 1.7 ms at
any active `rx-usecs`. Switching threaded NAPI off (`/sys/class/net/eth0/threaded=0`)
removes 0.65 ms (kthread wakeup) → **1.08 ms, mdev 36 µs**; the remaining ~1.0 ms is a
tight unexplained constant (not the poll, not the IRQ, not the peer — peer localhost
0.058 ms). Throughput A/B: threaded on/off is neutral → **`threaded=0` is the standard
operating mode** (latency win, no cost). Since TCP runs 0-retr and CPU-pegged at the
records, **latency is not the 500-blocker** — T2 driver surgery is parked.

**T3 (2nd TX queue): refuted by its proxy** — dual-process at the operating point totals
341 vs 417 single-process −P4: the xmit path is not the serializer; CPU per-byte is.

**Ops gotcha for the record:** peer-side `ethtool -C` requires `sudo -n` — the first T1
"peer sweep" silently never applied (peer sat at 1000 µs); always verify with
`ethtool -c` readback. The genuine peer knob is mild (437/435/452/424 at 3/50/200/1000).

## Why we are not at 1 Gbit/s yet — the bottleneck map

The datapath is never the raw-bandwidth limit (64-bit × 50–100 MHz ≫ 1 Gbit). The real walls,
in the order they surface as load rises:

- **TX ≤ ~186:** the 50 MHz CBS-shaper stage adds per-frame grant latency (datapath-input
  probe: 60% stall). Raising the datapath to 100 MHz halved that (→27% stall) and moved the
  wall to the **RingDMAReader**, which is serial/latency-exposed — one outstanding coherent
  DMA read at a time (70% starve). See `RX_FANOUT_AND_TX_CEILING.md`, `tx-datapath-limit`.
- **RX per-frame CPU cost:** each RX frame pays DMA cache ops + skb alloc + stack traversal;
  a single flow saturates one hart in `sys` at ~40 Mbit/s. **RSC** (HW receive coalescing)
  amortizes this and lifts single-flow RX to 209; the 2-queue fan-out reaches 223. Beyond
  that, the ceiling is CPU per-frame cost again.
- **Memory latency is the deep limit** (`LATENCY_INVESTIGATION.md`): **1424 ns/miss**
  (≈50% TLB walk + 50% DRAM), DDR3-800, 32 KB L2. Both directions are ultimately gated by
  how fast a 100 MHz RV64 core can touch uncached DMA memory per frame.

## Roadmap toward >500 Mbit/s, then 1 Gbit/s (ordered, each independently measurable)

**Immediate bar: >500 both directions** (≥200 met; TX at 354). The phased, gateware-gated
execution plan is **`docs/CAMPAIGN_500_PLAN.md`** (M1 instrumentation → R0 re-baseline →
R1 2-queue fan-out → R2 RSC geometry → T1/T2 TX levers + completion-IRQ → conditional
T3/X) — every phase has a numeric gate read from HW counters. The levers below are the
same ones that carry on to 1 Gbit.

0. ~~**Fix the RX overload wedge**~~ — **DONE in sim (2026-07-08, `09e3a09`)**: root cause was
   the pending-ACK flush popping a buffer while an open aggregate held an earlier one (BD order
   inverted pop order → driver mispaired forever); fixed by gating the flush on `~agg_open` +
   close-first in DISPATCH (footnote ⁴). `test_ring_bd.py` 22/22 incl. storm/heal-race/fuzz.
   **Remaining: silicon validation** — flash `build_dp100_wfix`, re-run the −P2 trigger that
   wedged 100% before, then the full RX matrix and TX −P4/−P8 stability.
1. ~~**TX reader prefetch**~~ — **REFUTED by measurement (2026-07-07)**; and the `stall` half of
   the old bottleneck map is **also resolved**: it was the CBS default shaping BE (footnote ³,
   fixed in `milan_csr`). The measured TX levers now: cut per-ACK/per-reap/per-wakeup CPU cost
   (rx-usecs 1000 already buys +23%), a second TX queue for dual-hart xmit, completion-IRQ
   latency. See `TX_READER_PREFETCH_PLAN.md` MEASURED VERDICT.
2. **Recover 100 MHz timing margin:** +0.031 ns on `build_dp100_cbs0`; **2-queue RxSteer at
   100 MHz** still needs re-validation once the wedge (item 0) is fixed — it may have been the
   wedge all along. Then run both directions at 100 MHz with the fan-out intact.
3. **Cut RX per-frame cost further:** wire a completion IRQ (drop the hrtimer poll — idle RTT is
   3–11 ms today and `rx-usecs-low=200` storms the CPU), scale the RX fan-out to more
   queues/harts, and lean on RSC + GRO. Line-rate RX needs fewer frames or more parallel harts.
4. **Attack memory latency:** faster DRAM (DDR3-800 → higher), bigger/smarter L2, huge-page or
   pinned DMA arenas to cut the 50% TLB-walk component. This is what ultimately unlocks 1 Gbit.
5. **UDP offloads (separate track):** USO (TX segmentation) + UDP-GRO (RX) to bring UDP off the
   per-frame path. Until then UDP is inherently ~20 (TX) / ~40 (RX) Mbit/s.
6. **More/faster cores:** a higher-clock or higher-IPC RV64 (or >2 harts) shortens the per-frame
   critical path directly — the single biggest lever, at the cost of timing closure.

## Detailed investigations (read these for the evidence)

| topic | doc |
|-------|-----|
| **RX overload wedge**: completion-order inversion, sim repro + fix (2026-07-08) | `docs/RX_OVERLOAD_WEDGE.md` |
| **CBS default-shaping bug**: reset config paced BE TX at 300 Mb/s (2026-07-08) | `docs/CBS_DEFAULT_SHAPING_BUG.md` |
| Reader-prefetch refutation (Phase-0 probes, MEASURED VERDICT) | `docs/TX_READER_PREFETCH_PLAN.md` |
| HW-TSO, single-flow ceiling, RX fan-out, datapath-input probe, 100 MHz datapath | `docs/RX_FANOUT_AND_TX_CEILING.md` |
| Memory-latency root cause (1424 ns/miss), floorplan/clock experiments | `docs/LATENCY_INVESTIGATION.md`, `docs/SINGLE_PORT_PERF.md` |
| RX RSC coalescing + `ethtool -C rx-usecs` (default 250 µs) | `../milan-tests-avb/fpga/kl-eth/README.md` |

## Ground rules for this campaign

- **MTU stays 1500** everywhere. Best-effort TCP is the primary metric.
- **Measure both HW and SW at every step** — `milan_tlm` counters (incl. the datapath-input
  and RX-pipeline probes) read alongside `/proc/stat` + `/proc/profile`; "the books must balance."
- **Verify the driver identity** (`MODULE_VERSION`) and measure over a clean path — console
  garble and stale drivers have produced phantom regressions before.
