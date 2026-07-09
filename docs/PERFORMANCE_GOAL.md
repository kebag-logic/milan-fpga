# Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s

> 📌 **Current state lives in [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md)** (+ [`../CHANGELOG.md`](../CHANGELOG.md)). This doc's older scoreboard rows/roadmap predate the mlp3 + perf findings (RX −P2 298, ceiling 481; TX −P2 crosses 500; next RX lever = DDIO).

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

## Where we are (measured on silicon, 2026-07-09)

| path | best measured | ≥500? | bound by | next lever toward 500+ |
|------|:-------------:|:-----:|----------|------------------------|
| **TX TCP** (100 MHz dp, CBS unshaped)³ | **−P2 525–536** · −P4 ~410–475 | **✓** | **datapath/shaper-bound**, not CPU (the refill/RPT change was TX-neutral) | done — TX crosses 500 at −P2 |
| TX TCP, CBS default (historical²) | 238–247 | ✗ | CBS shaper pacing BE at 300 Mb/s (config bug — fixed³) | — (fixed) |
| **RX TCP parallel (−P2)** | **316** (build_l2deep: mlp3 + L2 `downPendingMax` 4→8)⁵ | ✗ | **the recv payload copy = 51% of RX CPU** (cold DRAM read; perf-verified); memory-depth levers exhausted at ~316 (L2=16 flat, LiteDRAM cmd=16 flat) | **copy removal** — header-split + app zero-copy, or a residency-winning stash (ceiling 481, task #17) |
| RX TCP single | **277** (build_mlp2: RPT prefetcher, +34% over 207)⁵ | ✗ | same recv copy (cold read) | DDIO / app zero-copy (single ceiling 427) |
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
⁵ **RX memory levers, MEASURED 2026-07-08** (`RX_MEMORY_HIERARCHY_PLAN.md` + `LSU_NONBLOCKING_DCACHE.md`). Chain: −P2 was 238 (2-hart fan-out). (a) **64 KB L2** (`build_l2x2`) → −P2 278–280 (+17 %, L2 *capacity* lever, single flat). (b) **Non-blocking D$ alone** (`build_mlp1`, `lsuL1RefillCount=8`, 0 BRAM) → **no gain** (229≈238): on the in-order core the demand miss REDO-replays, so 8 refill slots sit empty without a filler. (c) **RPT hardware prefetcher** (`build_mlp2`, `--lsu-hardware-prefetch=rpt`, +2 BRAM tiles) *fills* the slots by stride-prefetching the payload copy → **single-flow RX 207→277 (+34 %)**, −P2 +7 %. (d) **Combination** (`build_mlp3`, refill+rpt+64 KB L2) → **−P2 298 (best, §V canary=0, split-verified)** + best TX−P4 431 — the two levers compound (capacity + latency-hiding). RPT=single/latency, L2=aggregate/capacity. The 2-hart aggregate remains a *shared-resource* wall (~1.2× single); >500 needs more queues/harts or fewer memory touches, not more cache.

**Status vs goal (>500):** **TX ✅ done (−P2 525–536). RX = 316 — and RX > 500 is a HARD GOAL:
the campaign does not close without it** (goal reasserted 2026-07-09 evening). Position: the RX
wall is the **recv payload copy** (`copy_to_user`, ~35–51 % of RX CPU, cold DRAM reads, perf-
proven); the `recv(MSG_TRUNC)` ceiling says the *rest* of the stack tops at **481** — so **no
copy trick alone can cross 500**: the path must both close the copy tax *and* raise the stack
ceiling. Refuted (measured, do not retry): page-flip zero-copy recv (flip 44.9 vs copy 25.0
µs/page), BRAM stash (residency 1–3 MB), *unscoped* shared-L2 DDIO at default rmem (pollution),
depth-2 interconnect, L2 > 64 KB for capacity, software prefetch, deeper LiteDRAM cmd queues.
1 Gbit/s remains the stretch. UDP is a separate (offload) problem. Every step measured on silicon.

## The path to RX > 500 (forced march — each phase gated by silicon numbers)

Budget logic: `RX = min(stack-ceiling, stack-ceiling − copy-tax)`. Today: ceiling 481 (MSG_TRUNC),
copy-tax ≈ 165 (481−316). 500 requires ceiling ≈ 550+ *and* copy-tax ≤ ~50. Three stacked phases:

| phase | lever | why the refuted-list doesn't block it | gate (measure!) | expected |
|---|---|---|---|---|
| **R1 — warm copy** (days, sw + existing bitstreams) | **`build_ddio` (exists) + SMALL receive queue** (`tcp_rmem`/`SO_RCVBUF` ≈ 24–48 KB/flow) + low `rx-usecs` (small BDP needs small RTT; threaded=0). The DDIO flat result was measured at **default rmem = 1–3 MB Recv-Q** — residency was impossible *by configuration*. Cap the queue so in-flight payload **fits the 64 KB L2**, and allocate-on-DMA-write finally lands warm for a copy that runs at L2 speed (~5 µs/page vs 25). Sub-options: 96 KB L2 rebuild (new justification: residency headroom, not capacity), completion-IRQ NAPI (T2, re-entered: cuts RTT → smaller BDP → tighter cap without throttling). | DDIO was never measured with a bounded residency window | perf copy-share < 25 %; **RX −P2 ≥ 380** | 316 → 380–450 |
| **R2 — raise the ceiling: RSC multi-slot** (RTL + driver, sim-first vs `test_ring_bd.py`) | Kill **park (58–66 % of aggregate closes)** — the single aggregate slot forces early closes whenever flows interleave. 2–4 slots/queue + longer `rsc_tout` ⇒ aggregates 2–3× larger ⇒ fewer skbs/GRO merges/BD reaps per byte — this **raises the 481 no-copy ceiling itself** (and cuts with-copy cost the same way). Buffers are DRAM-side (`KL_RSC_BUFSZ` is a driver alloc) — 0 BRAM. | park% is a measured counter (`rsc_close park=…`), not a hypothesis | park < 10 %; **MSG_TRUNC −P2 ≥ 550**; TCP −P2 ≥ 450 with R1 | ceiling 481 → ~550+; TCP → 450–520 |
| **R3 — clock 112.5 MHz** (1 build, final mile) | +4–8 % measured system-wide. The earlier "stay at 100" was a *convenience* call — its blocker (QSPI CRC) is already fixed (1×-SPI, `a80c955`; reader-Buffer `d35f666` closes timing) | it was deprioritized, never refuted | WNS ≥ 0, QSPI boot clean, §V; **RX −P2 ≥ 500** | ×1.04–1.08 ⇒ crossing margin |

Fallbacks if a gate fails: R1-miss → 96 KB-L2 residency rebuild, then RX-scoped `allocateOnMiss`
(only the RX writer's Puts, not all DMA); R2-miss → per-flow aggregate hashing instead of slots;
final-mile-miss → `AF_PACKET` `PACKET_RX_RING` demonstrator (copy-free by design, the real AVTP
path) recorded *alongside* — but the socket-TCP number remains the goal of record.

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

## Phase X MEASURED (2026-07-08) — clock uplift REFUTES the linear projection

**112.5 MHz is reached on silicon** — closed timing (WNS +0.038 via the reader-source
`stream.Buffer` cut, `d35f666`) AND boots clean from QSPI (single-lane SPI-flash read,
`a80c955`, after the 4x quad read CRC-failed non-deterministically at the faster sys clock).
Measured on `build_dp100_x1125d`, **guarded driver verified loaded** (`rsc_clk_mhz=100`,
`hwtso=Y`, `rsc=Y` — the same stack as the 100 MHz baseline), **peer-side rates** (clock-
correct; the serial-boot images carried a stale built-in driver — caught and discarded):

| path | 100 MHz | **112.5 MHz** | Δ | vs +12.5% ideal |
|---|:--:|:--:|:--:|:--:|
| TX −P4 (operating point) | 452 | **459–479** (avg ~470) | **+4 %** | ⅓ of ideal |
| TX single | 350 | **379** | **+8 %** | ⅔ of ideal |

**The +12.5 % CPU clock yields only +4 % (−P4) / +8 % (single) — the 508 projection is
REFUTED.** Measured TX at 112.5 is ~470–479, **still short of 500.** The reason is
structural: `--milan-clk-freq` keeps the **datapath at 100 MHz** (only sys/CPU moved to
112.5), so any datapath- or TCP-dynamics-bound fraction of TX does not scale with sys — and
−P4 (more of that fraction) scales worse than single-flow (more purely CPU-bound). This is
the measure-don't-assume payoff: the clean CPU-bound story at 452 (reader 66 % idle) does
**not** translate to linear clock scaling; the operating-point ceiling is a CPU/datapath/TCP
*mix*, not pure CPU. Caveat: the board ran a 100 MHz-timebase dtb (its own clock miscalibrated
12.5 %); peer-side rates are unaffected, but a fully-clean run wants the dtb rebuilt for 112.5.

**Consequence for the goal:** neither direction reaches 500 by clock alone. TX needs the
datapath at a higher clock too (the dense-datapath timing problem that drove the split-clock
architecture in the first place) or per-frame CPU-cost cuts; RX needs the structural work
(per-queue aggregate slots vs the park-58 % tax, >2 queues). The single-lane SPI fix and the
reader-cone cut are permanent wins that make 112.5 usable; the throughput lift it buys is
real but modest (~+4–8 %), not the projected ~+12.5 %.

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
| RX RSC coalescing + `ethtool -C rx-usecs` (default 250 µs) | `../the-private-test-repo/fpga/kl-eth/README.md` |

## Ground rules for this campaign

- **MTU stays 1500** everywhere. Best-effort TCP is the primary metric.
- **Measure both HW and SW at every step** — `milan_tlm` counters (incl. the datapath-input
  and RX-pipeline probes) read alongside `/proc/stat` + `/proc/profile`; "the books must balance."
- **Verify the driver identity** (`MODULE_VERSION`) and measure over a clean path — console
  garble and stale drivers have produced phantom regressions before.
