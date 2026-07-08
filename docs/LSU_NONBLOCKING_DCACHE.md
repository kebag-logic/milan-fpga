# VexiiRiscv LSU & the non-blocking D-cache: how the 8 refill slots work

*Written 2026-07-08 as the mechanism reference behind the `build_mlp1` lever
(`--lsu-l1-refill-count=8`). Sub-doc of [`RX_MEMORY_HIERARCHY_PLAN.md`](RX_MEMORY_HIERARCHY_PLAN.md)
and [`CAMPAIGN_500_PLAN.md`](CAMPAIGN_500_PLAN.md). Everything here is read from the VexiiRiscv
source we actually build — `pythondata-cpu-vexiiriscv/.../ext/VexiiRiscv/src/main/scala/vexiiriscv/`
— and cross-checked against the generated netlist, not from a textbook. Source citations are
`File.scala:line` against commit `235753e2` (pinned in `core.py:287`).*

---

## 0. Why this exists

The RX −P2 wall is **serial cold-miss latency**: HW DMAs each frame to DRAM, the CPU's first
touch always misses, and each miss pays ~1424 ns (≈50 % TLB + 50 % DRAM,
`LATENCY_INVESTIGATION.md`). The question was whether we can *overlap* those misses instead of
paying them one-at-a-time. The answer lives in the load/store unit's **refill engine**, whose
depth is the config knob `lsuL1RefillCount` — **1 by default in LiteX's "linux" variant, which
makes the D-cache blocking.** This doc explains the machinery that knob controls.

---

## 1. The LSU and its L1 D-cache at a glance

The core is **VexiiRiscv "linux" — a single-issue, in-order RV64GC-minus core**
(`core.py:257`, no C/F/D). Its data L1 is described by its own author as
(`LsuL1Plugin.scala:64`):

> *"It is non-blocking, can support multiple outstanding refill/writeback and is tightly
> coupled to the CPU pipeline to save area."*

Geometry we build (`core.py:262` + `Param.scala` defaults, line size `LsuL1Plugin.scala:86`):

| parameter | value | source |
|---|---|---|
| ways | 4 | `--lsu-l1-ways=4` |
| sets | 64 | `lsuL1Sets` default |
| line size | 64 B | `lineSize=64` |
| **total L1 D$** | **16 KB** | 4 × 64 × 64 B |
| refill slots | **8** (was 1) | `--lsu-l1-refill-count=8` |
| writeback slots | 1 (default) | `lsuL1WritebackCount` |
| store-to-load | bypass | `--with-lsu-bypass` |
| coherency | on | SMP + `--with-dma` |

The refill and writeback slots are **flip-flop/LUT state machines, not RAM** — this is why
growing refill 1→8 costs **0 BRAM** (§7). That is the entire point: it buys memory-level
parallelism out of the FF/LUT budget (32 %/77 % used) while leaving BRAM for the AVDECC logic.

---

## 2. The load pipeline and what "miss" means

A load flows through fixed pipeline stages (`LsuL1Plugin.scala:87-93`, `ctrlAt=2`):

```
   AGU            PMA/PMP + MMU         L1 tag+data read         hit/miss decide (ctrlAt=2)
 address   ->   translate & check  ->  read 4 ways in parallel -> compare tags -> HIT: forward data
 (Agu.scala)     (onPma / pmpPort)      (bankReadAt/wayReadAt)     (hitsAt=1,hitAt=2)  MISS: see below
```

On a **hit**, data is forwarded and the instruction retires — one access, no stall.

On a **miss**, the LSU does **not** stall the whole machine waiting for DRAM. Instead
(`LsuPlugin.scala:775-779`):

```scala
val l1Failed = l1.SEL && (... (l1.MISS || l1.MISS_UNIQUE) && (l1.LOAD || l1.STORE))
when(... l1Failed ...) {
  lsuTrap := True
  trapPort.code := TrapReason.REDO   // <-- the missing instruction is REPLAYED, not frozen
}
```

The miss (a) **allocates a refill slot** to fetch the 64 B line in the background, and (b)
raises a lightweight **REDO** — the load is re-executed from its own PC a few cycles later.
It keeps REDO-ing (cheaply) until the line has landed, then hits. **In-order order is
preserved** — a later instruction never commits ahead of the missing load. Hold this fact; it
governs §5.

---

## 3. The refill engine — the "8 refills"

The heart is an array of `refillCount` **refill slots** (`LsuL1Plugin.scala:315-354`). Each
slot is an independent little state machine tracking one in-flight 64 B line fetch:

```
refill.slots[0..7]  each = {
   valid       : this slot is tracking a live refill                 (:319)
   address     : the physical line being fetched                     (:320)
   way         : which of the 4 ways this line will fill             (:321)
   cmdSent     : the read request has been accepted by the L2 bus    (:322)
   priority    : ordering vs the other slots (fairness/lock)         (:323)
   loaded      : data has fully arrived & tag written                (:343)
   loadedCounter: retry-coordination timer (see hazard below)        (:345)
   victim      : wait for this dirty eviction's writeback first      (:353)
   c.{unique,data,ackId,ackValid,ackTimer} : coherency permissions   (:324-338)
}
```

### Lifecycle of one refill

```
  ┌ 1. ALLOCATE ──────────────────────────────────────────────────────────┐
  │ miss (or prefetch) issues push{address, way, victim}   (:366)          │
  │ first FREE slot captures it:  valid=1, loaded=0, cmdSent=0  (:356,382) │
  └───────────────────────────────────────────────────────────────────────┘
           │
  ┌ 2. ARBITRATE + SEND READ ─────────────────────────────────────────────┐
  │ PriorityArea picks a slot that is valid && !cmdSent && victim==0 (:402)│
  │ drive L2 read:  bus.read.cmd.id = slotIndex, .address = line   (:410)  │
  │ on cmd.ready -> cmdSent=1.  Up to 8 reads outstanding on the bus       │
  │ (readIdCount = refillCount, :113) — the slot index IS the bus tag      │
  └───────────────────────────────────────────────────────────────────────┘
           │
  ┌ 3. RECEIVE RESPONSE (may come back out of order, keyed by rsp.id) ─────┐
  │ each beat -> write one word into the data bank, wordIndex++  (:430-465)│
  │ responses for DIFFERENT slots may interleave — that is the parallelism │
  └───────────────────────────────────────────────────────────────────────┘
           │
  ┌ 4. COMPLETE (last word) ──────────────────────────────────────────────┐
  │ write the tag: tag.loaded=1, tag.address  (:466-475)                   │
  │ refillCompletions(id)=1 ; slot.loadedSet=1  (:469,480)                 │
  └───────────────────────────────────────────────────────────────────────┘
           │
  ┌ 5. RETIRE ────────────────────────────────────────────────────────────┐
  │ loadedSet -> loaded=1 ; loadedCounter guards in-flight overlappers     │
  │ fire = valid && loadedDone -> valid=0  -> slot FREE again  (:350-351)  │
  └───────────────────────────────────────────────────────────────────────┘
```

### The one line that defines "blocking" vs "non-blocking"

```scala
val full = slots.map(!_.free).andR          // LsuL1Plugin.scala:357
```

The cache can only refuse to start a **new** miss when **every** slot is busy.

- **`refillCount = 1` (the default we had):** there is exactly one slot. The *second* miss to a
  different line cannot even be *issued* until the first fully completes. Misses are **fully
  serialized** — N cold misses cost N × ~1424 ns back-to-back. This is the blocking D$ we
  verified in every stock netlist (`refill_slot_idxs=[0]`).
- **`refillCount = 8` (build_mlp1):** up to **8 distinct lines** can be refilling at once, their
  L2 reads pipelined on the bus and their responses returning out of order. The wall becomes
  `max(latency)` amortized across the stream instead of `sum(latency)`.

### Hazards the engine must handle (`LsuL1Plugin.scala:66-77`)

- **In-flight-line hit** (`REFILL_HITS`, :197-198): an access whose line matches a slot still
  refilling must **REDO** — it may not read a half-filled line. Resolves when that slot completes.
- **victim / writeback ordering** (:353): if the line to fetch evicts a dirty line, the slot
  waits (`victim`) until the writeback has progressed, so we never read stale-then-overwrite.
- **loadedCounter** (:340-347): a load that started before a refill finished but lands after it
  must notice the refill happened and retry — a small counter keeps that window correct.
- **Coherency** (:324-338, :490-502): with SMP + coherent DMA a refill also *acquires
  permissions* (shared/unique) and sends an **ack** to the L2; an `ackTimer` guarantees the
  hart makes "a minimal amount of forward progress after acquiring a cache line" before it can
  be probed away — prevents two harts live-locking on the same line. This path is active in our
  build (`--cpu-count 2 --coherent-dma`).

---

## 4. The L1↔L2 bus: where the parallelism is spent

`memParameter.readIdCount = refillCount` (`LsuL1Plugin.scala:113`). The L1↔L2 read channel is a
**tagged, split-transaction bus**: the L1 can issue up to 8 read commands (tag = slot index)
without waiting, and the L2/DRAM returns responses tagged with the same id, in any order
(`read.rsp.id` routes each response back to its slot, :421,461). So the 8 slots turn the L1 into
an 8-deep outstanding-request generator against the shared L2 → LiteDRAM → DDR3 path. **That is
the mechanism by which multiple 1424 ns latencies overlap.**

---

## 5. The honest part: how MLP actually arises on an *in-order* core

Because a demand miss **REDO-replays in program order** (§2), a *single* stream of dependent
demand loads keeps only **~1 miss in flight per hart** — the missing load spins on REDO until
its line lands; later loads cannot overtake it. So `refillCount=8` does **not**, by itself,
magically parallelize a dependent load chain. The 8 slots are *capacity for parallelism*; three
things actually **fill** them:

1. **The hardware prefetcher** (`Prefetcher.scala`, enabled by `--lsu-hardware-prefetch=rpt`).
   It watches the committed access stream, learns strides, and issues **prefetch pushes ahead of
   demand** into free refill slots. While the demand load on line A is resolving, lines A+1,
   A+2… are already fetching in slots 1-7; when demand reaches them they **hit**. This is the
   primary MLP engine, and it is *useless with only one slot* — which is exactly why VexiiRiscv's
   own performance preset bundles `lsuL1RefillCount=8` **with** `lsuHardwarePrefetch="rpt"`
   (`Param.scala:303-312`).
2. **The store buffer** (`LsuPlugin.scala:281-282`): a store that misses is retired into the
   store buffer and drained asynchronously into a refill slot, so **subsequent loads don't wait
   behind store misses**. Load-heavy RX benefits modestly here.
3. **Independent hit-under-miss + two harts**: hits proceed while a miss refills, and each hart
   has its *own* L1 with its own 8 slots, so the shared L2 already sees 2 concurrent demand
   streams under −P2.

**Consequence for the campaign.** `build_mlp1` enables `refillCount=8` **alone** (no prefetcher)
— a clean isolation of "slots without a filler." Expect a *modest* RX gain from it (store-buffer
decoupling + hit-under-miss). The **large** win is expected from `refill=8 + rpt` together (a
follow-on `mlp2` build); this doc's §3-4 machinery is the prerequisite that makes the prefetcher
effective. Either way we **measure**, not assume — the point of building mlp1 first is to know
how much each half contributes.

---

## 6. Timeline picture

```
 lsuL1RefillCount = 1  (blocking — what we had)
 demand : [miss A]======wait ~1424ns======[A][miss B]======wait======[B][miss C]===...
 L2 bus : [--- read A ---]                 [--- read B ---]           [--- read C ---]
          one outstanding; cost = N × 1424 ns   (serialized)

 lsuL1RefillCount = 8  + hardware prefetch  (the target)
 demand : [miss A]==wait==[A][B hit][C hit][D hit][E hit]...
 prefch :        [push B][push C][push D][push E]  (issued ahead into slots 1..7)
 L2 bus : [read A][read B][read C][read D][read E]  (pipelined, ≤8 in flight)
          cost ≈ 1424 ns + (N-1) × (bus throughput)   (latency amortized)
```

---

## 7. What we built, and its cost (`build_mlp1`, 2026-07-08)

Config: LiteX "linux" 2-core, **L2 reverted 64 KB → 32 KB**, `--lsu-l1-refill-count=8`, 100 MHz
datapath. Netlist `VexiiRiscvLitex_ee5c56d9…` **verified: refill slots 0-7 present** (stock had
only `[0]`), writeback slot 0.

| build | L2 | refill | **BRAM tiles** | LUT | FF | setup WNS | RX −P2 |
|---|---|---|---|---|---|---|---|
| m1 | 32 KB | 1 | 102.5 (76 %) | — | — | — | 238 |
| l2x2 | 64 KB | 1 | 110.5 (82 %) | — | — | +0.140 | 278 |
| **mlp1** | **32 KB** | **8** | **102.5 (76 %)** | 48736 (77 %) | 40965 (**32 %**) | **+0.118** | *measuring* |

Two things this table proves independent of the throughput result:

1. **The 8 refill slots cost 0 BRAM** — mlp1 is *identical* to m1 at 102.5 tiles, i.e. **8 tiles
   below l2x2**. The non-blocking D$ is bought entirely from the FF budget (32 % used). This is
   the "keep BRAM for the AVDECC logic" property, in the utilization report.
2. **It closes timing** — WNS **+0.118**, WHS +0.047 at 100 MHz, fully routed. The deeper load
   path cost only ~0.022 ns vs l2x2. Gate 1 (does the deeper LSU meet 100 MHz?) **passed.**

**Open gate:** RX −P2 vs m1 (238, isolates the lever) and l2x2 (278, "can MLP at 32 KB replace
the L2 doubling and hand back 8 tiles?"). Then §V storm-safety. Follow-on if modest:
`--lsu-hardware-prefetch=rpt` (the slot-filler of §5).

---

## 8. Reproduce / re-tune

```bash
# regenerate the netlist + bitstream with a deeper (or shallower) D$:
python3 milan_soc.py --cpu vexiiriscv --cpu-count 2 --all-blocks --coherent-dma \
  --milan-clk-freq 100e6 --with-spiflash --flashboot full --gtx-tx-invert \
  --timing-opt --floorplan --l2-bytes 32768 \
  --scala-args=--lsu-l1-refill-count=8 \        # the knob; add: --scala-args=--lsu-hardware-prefetch=rpt
  --uart-baudrate 115200 --rx-queues 2 --vivado-max-threads 32 --build --output-dir work/build_mlp1

# verify the lever landed in the RTL (ground truth, not the arg echo):
NN=$(grep -oE "netlist-name=VexiiRiscvLitex_[0-9a-f]+" work/build_mlp1.log | head -1 | cut -d= -f2)
grep -oE "refill_slots_[0-9]+_" pythondata-cpu-vexiiriscv/.../verilog/$NN.v \
  | grep -oE "[0-9]+" | sort -nu    # expect 0..7
```

The `--scala-args=--flag=value` single-token form is required — argparse rejects a value that
starts with `--` in the space-separated form.
