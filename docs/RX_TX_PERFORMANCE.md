# RX / TX performance — what we improved, how, and what's next

*Authoritative current-state reference (2026-07-09). Plain-language story of the >500 Mbit/s
campaign, with the measurements and diagrams. For the per-commit log see [`../CHANGELOG.md`](../CHANGELOG.md);
for the deep mechanism see [`LSU_NONBLOCKING_DCACHE.md`](LSU_NONBLOCKING_DCACHE.md) and
[`RX_MEMORY_HIERARCHY_PLAN.md`](RX_MEMORY_HIERARCHY_PLAN.md). Older phase docs are point-in-time
snapshots — trust the numbers here.*

## The goal, in one line

Best-effort TCP throughput **>500 Mbit/s in both directions** on the fully-FPGA Milan NIC
(Alinx AX7101, dual VexiiRiscv RV64 @ 100 MHz, DDR3-800, MTU 1500).

## Where we are

| direction | best measured (2026-07-09) | goal | verdict |
|---|:--:|:--:|---|
| **TX** | **−P2 525–536**, −P4 ~410–475 | 500 | ✅ **crosses 500** (at −P2) |
| **RX** | **−P2 298** (mlp3) · single 277 | 500 | ⏳ copy-bound; **481 ceiling** once the copy is removed |

The whole campaign on one chart:

![campaign chart](perf_campaign.svg)

---

## Part 1 — how we explained the RX improvements (the short version)

Think of RX as a bucket brigade: the NIC drops each frame into DRAM, then the CPU has to pick it
up and hand it to the application. We made the *pickup* faster in three ways, then found the real
wall.

![RX path and the wall](diagrams/rx_path_wall.svg)

1. **Bigger shared L2 (64 KB).** With two harts both doing RX, their working sets were evicting
   each other out of the 32 KB cache. Doubling it stopped the thrash → **RX −P2 238 → 280**.
2. **Non-blocking data cache (8 refill slots).** The CPU's L1 could only have *one* cache miss
   outstanding at a time — every miss stalled the core until DRAM answered (~1424 ns). We widened
   it to 8. **On its own this did nothing** (229 ≈ 238): an in-order core replays the missing load,
   it doesn't run ahead, so the 8 slots sat empty. Capacity for parallelism isn't parallelism.
3. **RPT hardware prefetcher — this is the one that worked.** It watches the access pattern, learns
   the stride, and *fills* those 8 slots ahead of the CPU, so the data is already on its way before
   the CPU asks. **RX single-flow 207 → 277 (+34%).**

![memory hierarchy and the three levers](diagrams/memory_hierarchy_levers.svg)

Combined (config **mlp3** = 64 KB L2 + refill=8 + RPT), **RX −P2 = 298** — the best so far, and
the refill slots cost **zero BRAM** (they're flip-flops), so the AVDECC logic budget is untouched.

### Then `perf` told us the truth

We cross-built `perf` for the board and profiled RX. **51% of the RX CPU is one line: the
`copy_to_user` in `recv()`** — the kernel copying the payload from DRAM into the app's buffer. And
it's slow (~18 cycles per 8-byte word) because it reads the payload **cold** — the NIC DMA'd it to
DRAM and this is the CPU's first touch, so every line misses.

We proved it with a ceiling test: a receiver that drains the socket with `recv(MSG_TRUNC)` (which
skips the copy) hits **RX single 427, −P2 481** — **+61%, i.e. 96% of the 500 goal.** So the copy
*is* the wall, and removing it essentially reaches the target.

---

## Part 2 — TX (and why our RX change didn't touch it)

TX already **crosses 500** — a back-to-back A/B of the pre-change (l2x2) and post-change (mlp3)
gateware showed TX is **unaffected** by the refill/RPT change (ranges overlap; both −P2 peak
525–536). That's expected: **TX is datapath/shaper-bound, not CPU-bound**, so a CPU-memory lever
doesn't move it. The RX-targeted change carries **no TX regression** — good.

TX got to 500 earlier in the campaign via: the CBS default-shaping bug fix (`34cc2bc`, it had been
pacing best-effort traffic at 300 Mb/s), HW TSO, and softirq-NAPI + peer receive-coalescing.

---

## Part 3 — what's next: DDIO (the vindicated "network cache")

The copy is fundamental to the socket API — the driver can't remove it (its zero-copy path is dead
code and wouldn't help the `copy_to_user` anyway). Two ways to beat it:

- **App zero-copy recv** (`MSG_ZEROCOPY`/mmap) → the 481 ceiling, but the *application* must opt in.
- **DDIO / allocate-on-DMA-write** → make the copy's read a cache **hit** by landing the DMA'd
  payload *warm* in the L2 (or a small dedicated stash) instead of cold in DRAM. Works for any app.

![DDIO before and after](diagrams/ddio_before_after.svg)

This is the **"dedicated cache for the network"** idea from the very start of the campaign — first
dismissed, then vindicated once `perf` showed the dominant cost is the copy's cold reads of the
DMA'd payload. VexiiRiscv's L2 has no allocate-on-DMA-write today, so this is a coherency-path RTL
change (or a stash cache on the `dma_bus`), sim-first — tracked as the open RX lever.

---

## The levers at a glance (measured)

| lever | effect | note |
|---|---|---|
| 64 KB L2 | RX −P2 238 → **280** | capacity (both harts) |
| refill=8 alone | 229 ≈ 238 (**no gain**) | in-order core; slots need a filler |
| **RPT prefetcher** | RX single 207 → **277** (+34%) | fills the slots; +2 BRAM tiles |
| mlp3 (all three) | RX −P2 = **298** (best) | slots cost 0 BRAM |
| *ceiling if copy removed* | RX −P2 = **481** | via `recv(MSG_TRUNC)` |
| DDIO (next) | → toward 481 | warm the copy's reads |

**Refuted along the way** (so we don't retry them): the depth-2 DMA interconnect (RX writer has
30× headroom), growing L2 past 64 KB, a BRAM buffer scratchpad, software prefetch (blocking D$),
and 112.5 MHz (only +4–8%). See [`../CHANGELOG.md`](../CHANGELOG.md).
