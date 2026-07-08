# RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision

*Sub-plan of [`CAMPAIGN_500_PLAN.md`](CAMPAIGN_500_PLAN.md), opened 2026-07-08. RX at the
2-hart fan-out ceiling is memory-bound; this plan disambiguates **which** memory problem and
picks the lever by measurement, because the candidate fixes range from a 1-hour L2 rebuild to
a weeks-long coherency-path RTL change. Same rule as the parent: no big build on a hunch.*

## The measured wall

| fact | value | source |
|---|---|---|
| L1 D$ hit | ~36 ns (~3.6 cyc @100 MHz) | pointer-chase (`sw/litex/tools_lat_mem_rd.c`) |
| **L2 (32 KB) hit** | **227 ns** | pointer-chase, WS=32 KB |
| **DRAM (past 32 KB)** | **340–409 ns**, →834 ns w/ TLB | pointer-chase, WS 48 KB→1 MB |
| single-flow RX | 192–206 | R0/R1 |
| **RX −P2 (2 harts, both 99–100 %)** | **238 = only +24 %, not 2×** | R1 |
| per-miss cost (scattered) | 1424 ns (≈50 % TLB + 50 % DRAM) | `LATENCY_INVESTIGATION.md` |

There is a **sharp 32 KB L2 cliff** and RX saturates 2 harts at +24 %, not 2× — the shared
memory subsystem (32 KB L2 + DDR3-800 + depth-2 DMA interconnect) is the ceiling, not cores
(see `CAMPAIGN_500_PLAN.md` "more cores rejected": TX not hart-bound, RX BRAM won't fit + this
sub-linear scaling).

## The question this plan answers

RX cache misses are **two kinds**, and the fixes are *disjoint*:

- **Cold / producer→consumer misses** — HW DMA-writes each frame to DRAM; the CPU's first
  touch is *always* a miss (this **is** the 1424 ns/miss cold read). **A bigger shared L2
  cannot fix these** — the data was never cached.
- **Capacity misses** — BD rings, code, socket/skb state, aggregate buffers re-referenced
  across frames and **evicted when two harts' hot-sets exceed 32 KB**. **A bigger L2 fixes
  these.**

The +24%-not-2× is consistent with **either** (capacity thrash) **or** DRAM-bandwidth
saturation (both harts' cold reads saturating DDR3-800) — and **we cannot measure which
directly**: `perf` is absent, and `perf_event_open` returns ENOENT (the SBI PMU exposes no HW
cache events; `taskset` is also absent — see the M1 driver notes). So the plan **infers**
cold-vs-capacity from controlled experiments, cheapest first.

## Tooling (perf-free, on-silicon)

- **`sw/litex/tools_lat_mem_rd.c`** — pointer-chase latency vs working-set; maps the cache
  hierarchy (already used: found the 32 KB cliff). Cross-compile static with
  `riscv64-buildroot-linux-gnu-gcc -O2 -static`, stage to the peer, wget to the board.
- **`pmu.c`** (scratchpad) — `perf_event_open` reader; **currently returns ENOENT** on this
  kernel. Kept for when/if opensbi is rebuilt with a PMU event table (see Phase C.0).

## Phase L2 RESULT (2026-07-08) — CAPACITY-bound CONFIRMED; L2 is the lever

`build_l2x2` (64 KB L2, WNS **+0.140** — best margin of the campaign, the L2 *helped* timing;
BRAM 81.85 %). §V clean (4/4 storm stages delivered, canary 0). Measured:

| | m1 (32 KB L2) | **l2x2 (64 KB L2)** | Δ |
|---|:--:|:--:|:--:|
| pointer-chase 32 KB | 227 ns | **178 ns** | −22 % |
| pointer-chase 48 KB | 340 ns | **306 ns** | −10 % |
| RX single | 206 | 208 | ~0 |
| **RX −P2 (split rounds)** | **238** | **278–280** | **+17 %** |

**Verdict: the RX 2-hart contention was CAPACITY misses, not cold.** Doubling the L2 lifted
−P2 +17 % (single unchanged — one flow's hot-set already fit 32 KB; only *two* harts spilled
it). A bigger *shared* L2 helping is the definitional signature of a capacity, not cold,
bottleneck. **So the dedicated network cache (Branch B) is DEFERRED** — the cheap L2 doubling
is the confirmed RX lever, and it did not require a coherency-path RTL project. → **Branch A.**

## (superseded plan) Phase L2 (IN FLIGHT) — the disambiguator: 32 → 64 KB shared L2

`build_l2x2` (100 MHz, `--l2-bytes 65536`, from HEAD incl. the reader-Buffer + 1x-SPI
keepers). **Fits: BRAM 81.85 % (110.5/135)**, +8 tiles over m1's 76 %.

- **Gateware measurement:** re-run the RX fan-out matrix (single, −P2 split, −P4) + the
  pointer-chase (L2 cliff must move 32 KB→64 KB, confirming the L2 grew); `/proc/stat` CPU%.
- **The gate splits the whole plan:**
  - **RX −P2 rises meaningfully above 238** ⇒ **CAPACITY-bound** → Branch A (grow/partition L2).
  - **RX −P2 ~unchanged** ⇒ **COLD / bandwidth-bound** → Branch B (dedicated network cache).
- Duration: ~1 build + a matrix. **This must land before any Branch-B commitment.**

## Branch A — capacity-bound: grow / partition the L2

Only if Phase L2 helped.

- **A.1 push L2 further** — 64 → 96 KB if BRAM allows (128 KB won't: 82 % + another 32 KB
  overflows 135 tiles; would need to free BRAM elsewhere first). Measure diminishing returns:
  each step's RX −P2 gain vs BRAM spent; stop when the curve flattens.
- **A.2 way-partition / stream-reserve** (if the L2 supports it) — reserve ways so the two
  harts' hot-sets don't evict each other, cheaper than raw capacity. Needs VexiiRiscv L2
  partition support (audit first; likely absent → skip).
- **Gate:** RX −P2 ≥ 300 with the L2 growth curve flat (no cheap capacity left).

## Architecture finding (2026-07-08) — why a network *scratchpad* is the wrong lever HERE

Investigated in response to "use on-chip BRAM, bypass DRAM for the network path." The instinct
is right in principle (DRAM cold-miss latency **is** the RX wall) but the naive scratchpad form
is blocked by two verified facts:

1. **The RX buffers are already in DRAM and cost ZERO FPGA BRAM.** They are `page_pool` +
   `dma_alloc_coherent` kernel pages (kl-eth.c:351–367, `DMA_FROM_DEVICE`). So a scratchpad
   would *move* 768 KB of buffers *into* the ~100 KB of free BRAM — it **adds** BRAM demand and
   doesn't fit. It is the opposite of "keep BRAM for logic." The network path does **not**
   compete with the AVDECC logic for BRAM today; only the **L2** and the **TX shaper FIFOs**
   (`traffic_queues.sv FIFO_DEPTH=16384`) do.
2. **The +17 % the L2 gave is kernel-owned state a driver scratchpad cannot relocate.** The
   reused hot-set that thrashed at 2 harts is socket/TCP/skb/GRO state + code + page-pool
   metadata — kernel slab/text, not driver buffers. A NIC driver can only place its *own*
   structures (BD rings, 2 KB — already L2-resident) in a scratchpad. So a scratchpad
   physically cannot hold the thing that bottlenecks. A **transparent cache (the L2) is the
   correct tool** precisely because the hot data is kernel-owned and scattered.

**Corollary — prefetch (B.0) viability is unverified on this core.** The CPU is VexiiRiscv
"linux" = **in-order** (milan_soc.py:2718). Software prefetch only hides latency if the D$ is
**non-blocking** (hit-under-miss / multiple outstanding refills). If it is blocking, a prefetch
load just moves the stall earlier — a no-op. **Verify the lsuL1 refill/outstanding config
before trusting B.0.** On an in-order blocking D$ the only lever is "make the read a hit"
(cache / stash), not "overlap the miss."

**Therefore the form of the idea that actually works is DDIO / allocate-on-DMA-write (B.3
below)** — land the DMA data warm in the L2/a stash so the CPU read is a *hit*, DRAM stays the
backing store. It does not save BRAM (it uses the L2/stash) and it is coherency-path RTL, but
it is the *architecturally* correct "on-chip for network" and the only one that addresses the
cold payload. The frugal, zero-BRAM RX lever meanwhile is **B.4 (fewer touches per frame** —
bigger RSC coalescing cuts the cold-miss *count*), which honors "keep BRAM for logic."

## Branch B — cold / bandwidth-bound: the dedicated network cache

Only if Phase L2 did **not** help. This is the user's "dedicated cache only for network"
idea — architecturally correct for cold misses (cf. Intel **DDIO** / ARM **cache stashing**:
land NIC DMA data where the CPU reads it warm). Ordered cheapest-first:

- **B.0 (software, no bitstream) — driver RX prefetch.** In `kl_rx_one_bd`, software-prefetch
  the next frame's header/first line (and the next BD) before processing the current one, so
  the cold-miss latency is *hidden* behind useful work. RISC-V `prefetch.r`/a dummy load, or
  restructure the reap loop to touch N+1 while N is in the stack. **The poor-man's stashing** —
  try this FIRST; a driver change, measured by RX −P2 delta + the reap-stage ns/frame timer
  already in the driver. If it recovers a big fraction, Branch B may not need RTL at all.
- **B.1 DRAM-bandwidth check (measurement, gates B.2/B.3).** Distinguish cold-latency from
  bandwidth: run the pointer-chase at a DRAM-sized WS on one flow while RX −P4 runs; if the
  benchmark's ns/access *rises* under RX load, the memory *bus* is contended (bandwidth) →
  favors reducing traffic (B.4) or faster DRAM; if it's unchanged, it's *latency* per cold
  miss → favors stashing/scratchpad (B.2/B.3). (No `taskset` → interpret with care, or add a
  tiny cpu-affinity syscall to the tool.)
- **B.2 SRAM scratchpad for network buffers (RTL, FPGA-native).** Put the RX ring / posted
  buffers in on-chip BRAM instead of DRAM → CPU reads at ~L1 latency, **zero DRAM for network
  data**. **BRAM budget is the constraint:** with the 64 KB L2 the board is at 82 % → ~110 KB
  BRAM free; the current RSC set is 48 × 16 KB = 768 KB → *won't fit*. Feasible variants:
  (a) revert the L2 and spend that BRAM here; (b) shrink RSC buffers (smaller aggregates);
  (c) **hybrid**: frame *headers* (the part the CPU touches for classification/GRO) in SRAM,
  payload stays in DRAM as a frag — headers are the hot, cold-miss-heavy part. Gate: RX −P2
  up with the pointer-chase showing header touches at SRAM latency.
- **B.3 DMA-stashing / write-allocate (RTL, coherency path — the "real" DDIO).** Make the RX
  writer's DMA writes *allocate* into the L2 (or a small dedicated stash cache) so the CPU
  reads warm, keeping DRAM as backing. **Requires L2-controller allocate-on-DMA-write** —
  VexiiRiscv's L2 almost certainly lacks it and today's `--coherent-dma` likely
  write-*invalidates* without allocating. This is weeks of coherency-path RTL, highest risk,
  highest ceiling. Only pursue if B.0/B.2 are insufficient and B.1 says latency (not
  bandwidth) is the wall. Sim-first against a coherency model before any bitstream.
- **B.4 fewer touches per frame (software/RTL, orthogonal helper).** Bigger RSC coalescing
  (fewer, larger frames = fewer cold misses per byte) and per-queue aggregate slots. Attacks
  both cold-miss count and bandwidth; complements B.0. Gated by the close-reason counters
  (`rsc_close_*`) already built in M1 (park 58 % today → per-queue slots cut the park tax).

## BRAM budget (the shared constraint — L2 and network-SRAM compete)

| config | BRAM tiles | % of 135 |
|---|---|---|
| m1 (32 KB L2) | 102.5 | 76 % |
| + 64 KB L2 (Phase L2) | 110.5 | **82 %** |
| headroom left @64 KB L2 | ~24.5 tiles ≈ **~110 KB** | — |

**Implication:** a full network-SRAM scratchpad (B.2) and a grown L2 (Branch A) cannot both be
large. The Phase-L2 A/B is therefore also a *resource-allocation* decision: spend the scarce
BRAM on L2 (capacity) **or** on a network cache (cold), not both — measurement picks.

## Decision tree (one glance)

```
Phase L2 (64 KB) — RX −P2 vs 238 ?
├─ >238  → CAPACITY-bound → Branch A: grow L2 (A.1) → gate RX −P2 ≥ 300
└─ ≈238  → COLD/BW-bound → B.0 driver prefetch (cheap, first)
                          → B.1 bandwidth-vs-latency check
                          ├─ bandwidth → B.4 fewer touches / faster DRAM
                          └─ latency   → B.2 SRAM scratchpad (hdr-in-SRAM hybrid)
                                       → B.3 DMA-stashing (RTL, last resort, sim-first)
```

## Gates & rule

Every step keeps the campaign contract: a numeric gateware/software gate read from HW counters
+ `/proc/stat`, §V on every bitstream, one lever per build. The expensive Branch-B RTL
(B.2/B.3) is **explicitly gated** on Phase-L2 showing cold-bound *and* B.0/B.1 — the dedicated
network cache is the right idea for cold misses, but it is a large investment that only the
measurement authorizes.
