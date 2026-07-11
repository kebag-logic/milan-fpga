# TX RingDMAReader prefetch  -  design plan (roadmap step 1, primary TX lever)

> ⚠️ **Point-in-time snapshot (2026-07-08).** Superseded  -  for current RX/TX numbers and the live bottleneck/lever see [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md) + [`../CHANGELOG.md`](../CHANGELOG.md). Numbers and "next steps" below are historical.

**Goal:** push single-flow TCP **TX past 200 Mbit/s** at the 100 MHz datapath by hiding
DMA read latency in the `RingDMAReader`. This is roadmap item **#1** in
[`PERFORMANCE_GOAL.md`](PERFORMANCE_GOAL.md)  -  the only remaining gap to "≥200 both
directions" (RX already meets it at 209/223).

**Status of this doc:** design + sim strategy only. **No RTL/build yet**  -  this is the
review artifact before the ~40-min P&R and the delicate on-silicon measurement.

---

> ## ⛔ MEASURED VERDICT (2026-07-07): PREFETCH NOT JUSTIFIED  -  do not build it
>
> Phase-0 was built (`build_dp100_p0`, WNS +0.065) and **measured on silicon** (two runs,
> `phase0_measure.sh`, rsc250 driver hwtso+rsc_clk_mhz=100, hash_sel=1). The measurement
> **refutes the central hypothesis of this plan**  -  the "L≈140, 70% starve = read latency"
> assumption everything below rests on was wrong:
>
> | assumed (this plan) | **measured** | consequence |
> |---|---|---|
> | L ≈ 140 cyc | **L_pay = 45 cyc (450 ns)**, both runs | reader round-trip is 3× faster than the docstring said |
> | 70% starve = read latency (prefetchable) | **prefetchable (pre_wait+rd_wait) = ~13%** | prefetch can recover ~13% at best |
> | interconnect pipelines reads (D=4) | **rxw_out_hi = 2** → `D_full=⌈(45+64)/64⌉=2` | prefetch caps at D=2 anyway |
> | TX stuck ~172, need prefetch for ≥200 | **TX = 238–247 Mbit/s, 0 retr** | **≥200 already MET** at this operating point |
>
> **The real TX walls** (reader is only **3.8% busy**; books balance, and reader-starve 567‰ ≈
> `txdp_in` starve 573‰): **stall ≈ 39%** (datapath back-pressures the reader  -  CBS shaper /
> MAC store-and-forward per-frame grant, still present at 100 MHz) and **idle ≈ 39%** (ring runs
> empty → CPU/driver doesn't queue TX fast enough). Read-latency is a distant third **and** capped
> by depth-2. Building the multi-outstanding-read FSM restructure below would have been a large,
> risky change recovering ≤13%. **Measuring first (Appendix A) saved it.** [[measure-dont-assume]]
>
> **If TX is ever revisited toward 1 Gbit, the levers are `stall` and `idle`, not the reader**  - 
> cut the datapath per-frame grant latency (best-effort passthrough fast-path in
> `traffic_controller_802_1q`) and the CPU per-descriptor TX-queue cost. The design below is
> retained as the (refuted) hypothesis and, in **Appendix A**, the instrumentation that settled it.

---

---

## 1. The problem, from the measurement

At the 100 MHz datapath (`build_dp100`), the TX datapath-input probe reads
**busy ≈ 3%, stall 27%, starve 70%** during a single zerocopy (HW-TSO) TX flow (172 Mbit/s).
Raising the datapath 50→100 MHz halved the shaper *stall* (60→27%) and **moved the wall to
the reader**: 70% of cycles the datapath is waiting because the `RingDMAReader` has produced
no beat. Pinning the ACK-NAPI did nothing and −P2 didn't beat single-flow → **not CPU-bound;
the reader gates it.** (See [`RX_FANOUT_AND_TX_CEILING.md`](RX_FANOUT_AND_TX_CEILING.md)
"Effort 04", memory `tx-datapath-limit-measured`.)

## 2. Root cause, from the RTL

`RingDMAReader` (`sw/litex/milan_soc.py:1301`) is **strictly one AXI read outstanding**. The
payload FSM is a serial loop:

- `PREP` registers this burst's geometry (`milan_soc.py:1781`)
- `PAY_AR` issues **one** AR, waits `ar.ready` (`:1786`)
- `PAY_R` streams that burst's R beats; when the burst's last beat lands but the segment has
  more (`bcnt == blen_r-1`, `rem_r > 0`) it goes **back to `PREP`** to issue the *next* AR
  (`:1884`, and the BD path `:1938`)

So the AR for burst *N+1* is not issued until burst *N*'s final R beat is consumed. Every
burst pays the **full coherent-DMA round-trip latency unhidden**. `burst_beats 16→64`
(cf98505) amortized it ~3×/burst but does not overlap bursts  -  necessary, not sufficient
(the `__init__` comment at `:1336` already says this).

**A model that is *consistent* with the silicon number  -  not yet a measured one.** With an
**assumed** round-trip latency **L ≈ 140 sys-cycles** (this figure is from the docstring
comment at `:1338`, **not a measurement**) and a 64-beat burst streaming at 1 beat/cyc:

```
duty = burst / (L + burst) = 64 / (140 + 64) = 31%   →   69% starve
```

That lands on the measured ~3% busy / 27% stall / **70% starve**  -  reassuring, but it is a
back-fit: L was chosen from a comment, not read off the hardware. **We do not build on it.**
Before committing a depth or spending a build, §0 measures L, and measures how much of the
70% starve is read-latency (what prefetch can fix) versus the TSO pre-pass being silent
(what it cannot). Never assume, always measure  -  the books must balance.

## 0. Phase 0  -  measure the assumptions first (this gates everything below)

**No prefetch RTL is written until these are measured.** Every number in §4/§5 is a *model*;
Phase 0 replaces the models with hardware readings, on the **current** `build_dp100` gateware,
so the design (depth D, and whether prefetch alone can even reach 200) is chosen from data.

Three unknowns, three instruments  -  all cheap HW counters, all read with the existing
coherent-capture/BusSynchronizer pattern the probes already use:

1. **The read round-trip L (replaces the assumed 140).** Add a reader counter: cycles from
   `PAY_AR` AR-fire to the burst's **first** `r.valid`, accumulated + a sample count → mean L
   (and a max). This is the single number the whole duty model turns on; it can only be read
   on silicon (real interconnect + L2 + DDR3-800), not in sim.
2. **Decompose the 70% starve.** Extend the datapath-input probe (or add a reader-side probe)
   to split the reader's non-producing cycles into **(a) waiting on R** (`PAY_R`, `r` not
   valid  -  the read-latency component prefetch removes), **(b) in the silent csum/TSO
   pre-pass** (`cs_pass` high  -  the double-read component prefetch does *not* remove), and
   **(c) between frames / header read**. This tells us *by measurement* the ceiling prefetch
   can reach on the TSO path  -  if (b) dominates, prefetch won't clear 200 and single-pass
   csum (§4 caveat) must come first/too. **This is the decision that must not be assumed.**
3. **The interconnect's real outstanding depth.** Add a max-in-flight-AR counter to the
   reader, and read the writer's actual achieved `outstanding` high-water (`:844`) under RX
   load. If the shared interconnect/L2 serializes reads to depth 1–2, a D=4 design buys
   nothing  -  size D to the *measured* available depth.

**Exit criterion for Phase 0:** measured L, a measured (a)/(b)/(c) starve split, and a
measured available outstanding depth. Only then do we (i) fix D, (ii) decide whether
single-pass csum is a co-requisite, and (iii) build. If Phase 0 says the interconnect won't
pipeline reads or that (b) dominates, **the prefetch build is deferred** in favor of whatever
the measurement points at  -  that is the point of measuring first.

## 3. Why it is viable (no blockers at the bus level)

- The reader is a **native AXI4 master**  -  `AXIInterface(data_width=64, address_width=32,
  id_width=4)` (`:2251`) on the coherent `dma_bus`, connecting through **`AXIInterconnectShared`
  "with bursts intact"** (`:2257`). AXI4 + a shared interconnect **support multiple
  outstanding AR** transactions.
- **Precedent in the same file:** `RingDMAWriter` already runs multiple **writes** outstanding
   -  `outstanding = Signal(6)` counts `AW issued − B received`
  (`:844`, updated `:900`), and only `WAIT_B` blocks on `outstanding == 0` (`:1178`). This
  is the exact credit-counter pattern the reader needs on AR/R, already proven on silicon.
- **In-order reassembly is free:** issue every AR with a **single fixed ID** (id=0). AXI
  guarantees R returns **in AR-issue order per ID**, which is exactly what the reader's
  in-order consume (continuity shifter / csum / TSO patching) already assumes. No reorder
  buffer needed.
- **The state is already split.** The request-side cursors `off_r`/`rem_r` ("next beat to
  *request*", `:1469`) are **separate signals** from the consume-side cursors `rbeat`/`bcnt`
  ("beats *streamed*"). The current FSM just runs them in lockstep. Decoupling them is the
  whole change  -  the hard structural split is already done.

## 4. Expected win (depth → duty)  -  a **model**, to be set by Phase-0 measurement

Pipeline throughput with **D** bursts of ARs in flight, latency L, burst B=64. **L below is
the assumed 140; the real table is recomputed from the Phase-0 measured L**  -  the D that
"fully hides" scales as `⌈(L+B)/B⌉`, so if measured L is 90 the knee is D=2, if it is 200 the
knee is D=5. The shape, not the exact row, is the takeaway:

```
beats/cycle = min( 1 ,  B·D / (L + B) )       [D_full-hide = ⌈(L+B)/B⌉]
```

| D (outstanding) | duty @ assumed L=140 | vs serial | note |
|:--:|:--:|:--:|---|
| 1 (today) | 31% | 1.0× | *consistent with* silicon 70% starve (not a fit-free proof) |
| 2 | 63% | 2.0× | may clear 200 **iff** starve is read-latency, not pre-pass (Phase-0 §2) |
| 3 | 94% | 3.0× | near-full |
| **4** | **100%** | **3.2×** | latency hidden @ L=140; **re-derive D from measured L** |

**Do not hardcode D=4.** Size the credit window and FIFO depth from Phase-0's measured L
*and* measured available interconnect depth  -  whichever is smaller caps the useful D. FIFO
depth = chosen D rounded up to a power of two.

**Caveat  -  the TSO double-read.** The 172 path is HW-TSO, which reads each segment **twice**
(silent csum pre-pass, then real pass  -  `cs_pass` suppresses `source.valid`, `:1870`/`:1891`).
Prefetch hides the read latency *within each pass*, but the pre-pass emitting nothing to the
datapath is a **separate structural component** of the 70% starve that prefetch does **not**
remove. So on the TSO path the win may be less than 3.2×. **We measure both components in
sim before building** (§7) and, if a large residual starve remains, the next lever is
single-pass csum (read the segment once into a BRAM buffer, sum while filling, stream from
BRAM with the patched checksum  -  turns 2 DRAM reads into 1 DRAM + 1 BRAM). That is a
*separate* follow-on, called out here but out of scope for step 1. The plain-ring and
non-TSO BD paths get the full 3.2× immediately.

## 5. Design

Add an **AR-issue path decoupled from R-consume**, mediated by a credit counter and a
per-burst geometry FIFO. R stays in-order (single ID), so consume logic is untouched in
substance  -  it just sources `blen_r` from the FIFO instead of from `PREP`.

New state:

- `rd_credit`  -  ARs issued − bursts fully consumed (mirror of the writer's `outstanding`).
- `geo_fifo`  -  small SyncFIFO, one entry per issued burst carrying `{blen, last_of_seg}`
  (and, if needed, the last-beat `keep`). **Pushed on AR-fire, popped when a burst's last R
  beat is consumed.** Depth 8.
- Issue side advances `off_r`/`rem_r` per AR-fire (already does, `:1795`); consume side
  advances `rbeat`/`bcnt`/`rd`/`rd_pub` exactly as today.

**Boundary rule (the correctness crux).** Anywhere the reader **rewinds `rd`** or changes the
geometry base, **quiesce first**  -  wait `rd_credit == 0` before issuing past the boundary,
exactly like the writer's `WAIT_B` (`:1178`). The rewind/boundary points are:

- `cs_restart()` (`:1839`)  -  csum pre-pass → real pass rewind (`rd := rd_c`)
- `tso_rewind()` (`:1641`)  -  TSO per-segment pre-pass rewind (`rd := anc_rd`)
- `seg_finish()` (`:1802`) / `TSO_COMMIT` (`:2071`)  -  frame/segment transitions
- any bad-header/BD resync (`BD_FLUSH`, `rd := wr`)

Quiescing at these points **trivially preserves** the pre-pass/rewind semantics: no
prefetched AR ever crosses a rewind, so no in-flight read is on the wrong path and there is
nothing to squash. We keep **intra-pass** prefetch (the bulk of the win  -  a pass is many
bursts) and pay one drain of ≤ (D−1) bursts at each boundary. This is the low-risk choice;
a later optimization could prefetch across boundaries with AR tagging, but the marginal
gain is small and the risk is high.

**Timing discipline (this design closes at +0.010 ns  -  do not regress it).** The continuity
shifter + csum cone is historically *the* critical path (−4.4 WNS at one point, `:1518`). The
AR-issue additions **must stay off that path**: drive `ar.addr`/`ar.len` from **registered**
`addr_r`/`blen_r` (as `PREP` already does), keep `rd_credit` a simple ±1 adder, and make the
geometry FIFO push/pop control-only. No new combinational logic in `PAY_R`'s data cone.

### Two structural options

| | Option A  -  depth-2 look-ahead | Option B  -  issue/consume split (recommended) |
|---|---|---|
| change | single FSM keeps driving R; add one registered "next-AR" issued during `PAY_R` | separate small **issue FSM** (walks geometry, issues AR to credit limit) + the existing FSM as **consume**, joined by `geo_fifo` |
| depth | 2 (≈63% duty) | 4+ (≈100% duty) |
| diff size | small | moderate |
| timing risk | AR handshake tangled into `PAY_R` state | AR path fully separate & registered → **lower** |
| ceiling | ~2× (may just clear 200) | ~3.2× (headroom) |

**Recommend Option B.** It reaches the full win, and  -  counter-intuitively  -  it is *safer for
timing* because the AR logic is a separate registered block, not woven into the critical
`PAY_R` cone. Option A's depth-2 might clear 200 on the plain path but leaves no margin and
risks the +0.010 ns.

### Staged implementation (limit blast radius on the intricate FSM)

1. **Phase 1a  -  plain ring + simple BD, no csum/TSO.** Add `rd_credit` + `geo_fifo`; prefetch
   the payload bursts of a single segment. Quiesce at every frame boundary. Validated by
   `test_ring_tx` (5 tests) + `test_tx_bd` single/multi/wrap/unaligned. **This alone delivers
   the plain-path win.**
2. **Phase 1b  -  extend prefetch inside a csum/TSO pass.** Allow the credit window to fill
   *within* a pre-pass and within a real pass (still quiescing at the rewind). Validated by
   `test_bd_csum_insert`, `test_bd_csum_chain`, `test_tso_hw`.
3. **Header/descriptor prefetch (optional, later).** Overlap the *next* frame's `HDR_AR`
   read with the current frame's payload tail. Separate change; call it out, don't build yet.

## 6. What does **not** change

- CSR map / footprint (7 words)  -  DT `dma-tx` window and all downstream CSR addresses stay put.
- Frame/BD/TSO wire semantics, checksum math, byte order  -  prefetch changes **timing, never
  bytes**. `frames_from_beats()` output must be identical.
- The 4 KB-boundary and ring-wrap burst splits (`blen`/`to_4k`/`to_wrap`, `:1487`)  -  each AR is
  still the same shape; we only issue them earlier.
- Driver, gateware CSR layout, `rsc_clk_mhz`, hash_sel  -  untouched.

## 7. Sim strategy (must land before any build)

The existing harness **cannot** measure this. `test_ring_tx.py`'s `axi_slave` (`:62`) is
**strictly serial**  -  it waits for `ar.valid`, streams the whole burst's R, *then* looks for
the next AR. It models exactly one outstanding AR and will happily let a prefetching reader
pass all its correctness tests **without exercising the win.**

Add:

1. **`PipelinedReadSlave`**  -  a new sim slave that models the real bus:
   - asserts `ar.ready` and **enqueues ARs while R beats of a prior burst are still streaming**
     (up to `max_outstanding`);
   - for each AR, schedules its first R beat **`ar_latency` cycles** later (the round-trip),
     then streams beats back-to-back;
   - returns R strictly **FIFO order** (single ID). Protocol checks (arsize==3, 4 KB rule,
     no read of unwritten addr) carried over from the current slave.
2. **`test_prefetch_throughput`**  -  queue *K* back-to-back MTU-1500 frames, run under
   `PipelinedReadSlave(ar_latency=<measured L from Phase-0>)` (sweep a *range* of L around it
   so the result isn't hostage to one number), and **assert cycles-to-`sent==K` drops** vs the
   serial baseline, approaching the `min(1, B·D/(L+B))` model. Sweep `D ∈ {1,2,3,4}` and check
   the duty within tolerance. Run the same stimulus through the **serial** slave to prove no
   regression. Sim validates the *model and the RTL*; the *absolute* number still comes from
   silicon (§9)  -  sim latency is a stand-in for the real interconnect, not a substitute.
3. **Duty probe in the testbench**  -  count reader `source` busy/idle cycles and print the
   busy% so sim **predicts the silicon starve** number the datapath-input probe will read.
4. **TSO decomposition**  -  run `test_tso_hw`'s `_tso_reference` stimulus under the pipelined
   slave and separately report busy-during-real-pass vs total, to **quantify the pre-pass
   double-read component** (§4 caveat) *before* building  -  so we know if prefetch alone can
   reach 200 on the TSO path or if single-pass csum is also needed.
5. **Regression gate:** all current tests  -  `test_ring_tx` (5), `test_tx_bd` (9, incl.
   `csum_chain` + `tso_hw`)  -  pass under **both** the serial slave (unchanged) **and** the new
   pipelined slave, byte-identical `frames_from_beats()`. This is the safety net: prefetch is
   correct iff the bytes are unchanged at every depth.

## 8. Unknowns  -  each has a measurement, none is assumed

- **Interconnect / L2 / LiteDRAM read pipelining depth.** Sim assumes ideal multi-outstanding;
  if `AXIInterconnectShared` or the coherent L2 serializes reads per master, the win is capped
  below the model. **Measured in Phase-0 §3** (max-in-flight-AR counter + writer `outstanding`
  high-water), *before* choosing D  -  not discovered after a wasted build. Re-confirmed post-
  build by the datapath-input probe: starve *must* drop from 70%.
- **How much of the 70% starve prefetch can even touch.** The latency-vs-pre-pass split is
  **measured in Phase-0 §2**, not inferred from the model. If the pre-pass (silent double-read)
  dominates, prefetch can't reach 200 alone and single-pass csum is promoted ahead of it.
- **Timing.** +0.010 ns is razor-thin. Keep AR logic registered and off the `PAY_R` data cone
  (§5); read WNS from the actual report, don't assume it holds. If it regresses, fall back to
  Option A / depth-2, or pipeline the geometry FIFO read.
- **The round-trip L itself**  -  **measured in Phase-0 §1**; every derived number is recomputed
  from it. The `~140` in §2/§4 is a placeholder until that read exists.

## 9. On-silicon validation (after the plan is built  -  not now)

1. Build `build_dp100_pf` (`--milan-clk-freq 100e6`, prefetch RTL), `--vivado-max-threads 32`.
2. Flash; **`devmem 0xf0003080 32 1` (hash_sel=1) before any TCP**; `dmesg -n 1`.
3. Single zerocopy TX board→peer, read the **datapath-input probe** (busy/stall/starve @
   `0xf0004060..6c`) alongside `iperf3`  -  the books must balance. **Success = starve falls
   from 70% and TX clears 200.** Compare −P2 to confirm it's the shared reader, not CPU.
4. Confirm RX (209/223) and the csum/TSO correctness (no bad-checksum drops on the peer)
   are unregressed.

---

### One-paragraph summary

The reader issues one AXI read at a time (`PAY_AR`→`PAY_R`→`PREP`→`PAY_AR`), so every 64-beat
burst pays the full DRAM round-trip unhidden; a `burst/(L+burst)` model is *consistent with*
the measured 70% starve, but its L was taken from a comment  -  so **Phase 0 measures L, the
latency-vs-pre-pass split, and the interconnect's real outstanding depth on the current
gateware first**, and the design (depth D, and whether single-pass csum must come first) is
chosen from those readings, not the model. Fix: decouple AR-issue from R-consume with a credit
counter + per-burst geometry FIFO (the writer already does this for writes; the request-side
cursors are already separate), single-ID so R stays in-order and consume logic is untouched,
and **quiesce (`credit==0`) before every `rd` rewind** so the csum/TSO pre-pass stays correct.
A new *pipelined* sim slave (latency = the measured L) + a throughput/duty test validates the
RTL and the model  -  but the absolute number is only ever the silicon datapath-input probe.
Never assume, always measure  -  before *and* after the build.

---

# Appendix A  -  Phase-0 counter spec (detailed, buildable)

All three instruments live entirely in the **`sys` clock domain** (the `RingDMAReader`
`dma.tx`, its `bus`, and the CSRs are all sys)  -  so, unlike the datapath-input probe
(`dp_in_probe`, `milan_soc.py:2448`), **no `BusSynchronizer`/CDC is needed**. They reuse the
existing `MilanDebug` machinery: `self._rst` (`:2383`, the `reset` CSR  -  holds counters at 0
while high), `self._cap` (`:2384`, the `capture` re-pulse that latches every shadow together),
and `self._snap(live, width, name, desc)` (`:2427`, latch+expose-as-CSRStatus). Counters are
**reset-based** like `sys_probe` (`:2435`): the operator pulses `reset`, runs the load, pulses
`capture`, reads a coherent snapshot.

Injection point is the **unused `extra=` hook**: `MilanDebug(self.milan_dma, self.milan_mac)`
at `:2657` becomes `MilanDebug(..., extra=_phase0)`, and `_phase0(dbg)` adds the probes. This
keeps the Phase-0 code in one closure, trivially droppable from a production build, and touches
`MilanDebug` not at all.

## A.0  -  Exposures (small read-only taps on existing modules; zero functional effect)

`cs_pass` and the FSM states are internal to `RingDMAReader`, and `outstanding` is internal to
`RingDMAWriter`. Expose them as debug signals (comb taps  -  no new logic in any data cone):

```python
# in RingDMAReader.__init__, AFTER `self.fsm = fsm = FSM(...)` (milan_soc.py:1652) and the
# FSM body, so fsm.ongoing() is defined:
from functools import reduce
from operator import or_
self.dbg_cs_pass = Signal()          # 1 = silent csum/TSO pre-pass (source suppressed)
self.dbg_reading = Signal()          # in a state that awaits/consumes R data
self.dbg_idle    = Signal()          # IDLE = no work queued (rd == wr)
self.comb += [
    self.dbg_cs_pass.eq(cs_pass),                                    # local :1404
    self.dbg_reading.eq(reduce(or_, [fsm.ongoing(s) for s in
        ("HDR_R", "PAY_R", "TSO_EXT_R", "TSO_BD_R", "BD_FLUSH")])),  # the R-consuming states
    self.dbg_idle.eq(fsm.ongoing("IDLE")),
]

# in RingDMAWriter.__init__, after `outstanding` (:844):
self.dbg_outstanding = Signal(6)
self.comb += self.dbg_outstanding.eq(outstanding)
```

`self.source` (`:1345`) and `self.bus` (`:1344`) are already public  -  `source.valid/ready` and
`bus.ar.valid/ready/len`, `bus.r.valid` are tapped directly.

## A.1  -  Read round-trip latency L  (`rd_latency_probe`)

Measures cycles from **AR accepted** to that burst's **first R beat**  -  the single number the
duty model turns on. Split into *all reads* and *payload bursts only* (`ar.len >= 8`, which
excludes the len-0/len-1 header/BD/shadow reads), because the model wants the **payload** L.

```python
def rd_latency_probe(self, name, rdr, desc):
    bus = rdr.bus
    ar_fire = Signal(); self.comb += ar_fire.eq(bus.ar.valid & bus.ar.ready)
    waiting = Signal()           # an AR is accepted, its first R not yet seen
    lat     = Signal(16)         # cycles this outstanding read has waited
    is_pay  = Signal()           # this burst is a payload burst (len >= 8)
    acc  = Signal(48); n   = Signal(32); mx = Signal(16)   # all reads
    pacc = Signal(48); pn  = Signal(32)                    # payload bursts only
    self.sync += [
        If(self._rst, acc.eq(0), n.eq(0), mx.eq(0), pacc.eq(0), pn.eq(0),
           waiting.eq(0), lat.eq(0),
        ).Else(
            If(ar_fire,                      # start timing this read
                waiting.eq(1), lat.eq(0), is_pay.eq(bus.ar.len >= 8),
            ).Elif(waiting,
                lat.eq(lat + 1),
            ),
            If(waiting & bus.r.valid,        # first R beat arrived: record & stop
                waiting.eq(0),
                acc.eq(acc + lat), n.eq(n + 1),
                If(lat > mx, mx.eq(lat)),
                If(is_pay, pacc.eq(pacc + lat), pn.eq(pn + 1)),
            ),
        ),
    ]
    for sig, w, tag, d in ((acc,48,"acc","Σ AR->firstR cycles, all reads"),
                           (n,  32,"n",  "read count"),
                           (mx, 16,"max","worst-case latency (cyc)"),
                           (pacc,48,"pacc","Σ cycles, payload bursts (len>=8)"),
                           (pn, 32,"pn", "payload-burst count")):
        self._snap(sig, w, f"{name}_{tag}", f"{desc}  -  {d}")
```

Readout: **L_all = acc/n**, **L_pay = pacc/pn** cycles → ×(1000/f_MHz) ns (×10 ns @100 MHz).
`max` flags tail latency (TLB-walk spikes). **Single-outstanding caveat:** the lone
`(waiting, lat)` pair is exact only because the reader issues one AR at a time *today*  -  which
is precisely the gateware Phase-0 runs on. Once prefetch lands this must become a small
timestamp FIFO (one entry per in-flight AR); but by then the datapath-input probe measures the
*outcome* directly, so this probe is a Phase-0-only tool. L is a property of the
interconnect+L2+DDR3 path that one read pays; under prefetch those latencies overlap  -  so the
single-read L measured now is exactly the model's input.

## A.2  -  Starve decomposition  (`rd_produce_probe`)  -  the decision-maker

Partitions **every sys cycle** into 7 exhaustive buckets by *why the reader is/ isn't feeding
its `source`*. The split of the silent pre-pass into **wait** (blocked on read latency  - 
prefetch removes) vs **busy** (consuming/summing beats, ~1 cyc/beat  -  structural, prefetch does
NOT remove) is what tells us whether prefetch alone can reach 200.

```python
def rd_produce_probe(self, name, rdr, desc):
    src, bus = rdr.source, rdr.bus
    prod  = Signal(); stall = Signal(); nov = Signal()
    self.comb += [prod.eq(src.valid & src.ready),
                  stall.eq(src.valid & ~src.ready),
                  nov.eq(~src.valid)]
    rwait = Signal()     # in an R state but data not yet valid  (prefetchable latency)
    self.comb += rwait.eq(rdr.dbg_reading & ~bus.r.valid)
    busy=Signal(32); st=Signal(32); cyc=Signal(32)
    pre_wait=Signal(32); pre_busy=Signal(32); rd_wait=Signal(32)
    idle=Signal(32); setup=Signal(32)
    self.sync += [
        If(self._rst, *[s.eq(0) for s in
            (busy,st,cyc,pre_wait,pre_busy,rd_wait,idle,setup)]).Else(
            cyc.eq(cyc + 1),
            If(prod,  busy.eq(busy + 1)),
            If(stall, st.eq(st + 1)),
            If(nov,                                  # not producing -> why? (priority order)
                If(rdr.dbg_cs_pass & rwait,   pre_wait.eq(pre_wait + 1)   # (b1) pre-pass, read-blocked
                ).Elif(rdr.dbg_cs_pass,       pre_busy.eq(pre_busy + 1)   # (b2) pre-pass, summing beats
                ).Elif(rwait,                 rd_wait.eq(rd_wait + 1)     # (a)  real pass, read-blocked
                ).Elif(rdr.dbg_idle,          idle.eq(idle + 1)          # (c)  nothing queued (ring empty)
                ).Else(                       setup.eq(setup + 1))       # (d)  AR/PREP/header setup
            ),
        ),
    ]
    for sig,tag,d in ((busy,"busy","producing (valid&ready)"),
                      (st,"stall","source back-pressured by datapath"),
                      (pre_wait,"pre_wait","pre-pass blocked on read (PREFETCHABLE)"),
                      (pre_busy,"pre_busy","pre-pass consuming beats (STRUCTURAL double-read)"),
                      (rd_wait,"rd_wait","real pass blocked on read (PREFETCHABLE)"),
                      (idle,"idle","IDLE: ring empty (CPU/driver-bound)"),
                      (setup,"setup","AR-issue/PREP/header setup"),
                      (cyc,"cyc","total cycles (normaliser)")):
        self._snap(sig, 32, f"{name}_{tag}", f"{desc}  -  {d}")
```

**Books balance:** `busy + stall + pre_wait + pre_busy + rd_wait + idle + setup == cyc` (assert
in the readout). This mirrors the datapath-input probe's starve from the *reader* side: the
`txdp_in_starve` ≈ (pre_wait+pre_busy+rd_wait+idle+setup) seen through the CDC  -  the two probes
cross-check.

## A.3  -  Interconnect outstanding-depth proxy  (`outstanding_hi_probe`)

Reads can only be over-issued if the shared interconnect/L2 grants depth. The **writer already
over-issues writes**  -  its `outstanding` high-water under RX load is the pre-build proxy for
read-side capacity on the same `AXIInterconnectShared`.

```python
def outstanding_hi_probe(self, name, wtr, desc):
    hi = Signal(6)
    self.sync += If(self._rst, hi.eq(0)).Elif(wtr.dbg_outstanding > hi,
                                               hi.eq(wtr.dbg_outstanding))
    self._snap(hi, 6, f"{name}_hi", f"{desc}  -  max AW in flight")
```

Proxy, honestly labelled: writes and reads have separate queues, so this *bounds expectation*,
it doesn't prove the read number  -  that is the post-build datapath-input probe. If the writer
never exceeds 1–2 under load, the interconnect/L2 is serializing and prefetch is in doubt
*before* we build it.

## A.4  -  Integration (one closure, revert = delete it)

```python
# replace milan_soc.py:2657
def _phase0(dbg):
    dbg.rd_latency_probe ("txrd_lat", self.milan_dma.tx, "TX reader AR->firstR latency")
    dbg.rd_produce_probe ("txrd",     self.milan_dma.tx, "TX reader produce/starve breakdown")
    dbg.outstanding_hi_probe("rxw_out", self.milan_dma.rx, "RX writer outstanding")
    if hasattr(self.milan_dma, "rx1"):
        dbg.outstanding_hi_probe("rx1w_out", self.milan_dma.rx1, "RX1 writer outstanding")
self.milan_tlm = MilanDebug(self.milan_dma, self.milan_mac, extra=_phase0)
```

CSR addresses are auto-allocated by LiteX into the `0xf000_xxxx` CSR region (like the existing
`txdp_in_*` at `0xf0004060..`); the build emits their offsets in `csr.h` / the csr map  -  read
them there, or `devmem` them once the map is known. **Cost:** ~300 FFs, all sys-domain, no CDC,
no data-cone logic  -  negligible against the +0.010 ns (these are counters off the critical path).

## A.5  -  Measurement protocol (on `build_dp100_p0`, the instrumented 100 MHz gateware)

**Implemented as `sw/litex/phase0_measure.sh`** (busybox sh; runs on the board vs the peer;
CSR addresses baked in from the `build_dp100_p0` `csr.csv` and verified: `reset`@`0xf0004000`,
`capture`@`0xf0004004`, `txrd_*` @ `0xf0004088..c0`, `rxw_out_hi`@`0xf00040c4`,
`rx1w_out_hi`@`0xf00040c8`; the 48-bit `acc/pacc` are MSW-first 2-word reads). It does Phase A
(TX → L + starve split, with the balance assert + a `txdp_in` cross-check) then Phase B (RX
reverse → the outstanding-depth proxy). Steps it automates:

1. `hash_sel=1` (`devmem 0xf0003080 32 1`) before any TCP; `dmesg -n 1`.
2. Pulse **reset**: write 1 then 0 to the `reset` CSR (zeros all live counters, starts counting).
3. Run the load: single zerocopy TX board→peer (the 172 Mbit path), `iperf3`, ~8 s (keep the
   window < ~40 s so the 32-bit `cyc` doesn't wrap).
4. Pulse **capture** (write 1): latches a coherent snapshot of every counter.
5. Read and compute:
   - `L_pay = pacc/pn` cyc (×10 ns)  -  the model input; `L_all`, `max` for context.
   - starve split as %cyc: `pre_wait, rd_wait` (**prefetchable**) vs `pre_busy` (**structural
     double-read**) vs `idle` (**CPU/ring-empty**) vs `setup`; plus `busy`, `stall`. Assert Σ==cyc.
   - `rxw_out_hi`, `rx1w_out_hi`  -  the depth proxy.
6. Capture `txdp_in_*` (busy/stall/starve) over the *same* window and confirm
   `txdp_in_starve ≈ pre_wait+pre_busy+rd_wait+idle+setup`  -  the books must balance across probes.

## A.6  -  What the numbers decide (before writing any prefetch RTL)

| measurement | if… | then |
|---|---|---|
| `L_pay` | = X cyc | `D_full = ⌈(X+64)/64⌉` (bursts to fully hide X behind 64-beat streaming); size the credit window to it |
| `rxw_out_hi` | ≥ 4 | read depth almost certainly available → build prefetch at D=`min(D_full, hi)` |
| `rxw_out_hi` | ≤ 2 | interconnect/L2 serializing → **defer prefetch**, investigate the AXI/L2 config first |
| `pre_wait + rd_wait` | dominate the non-busy cycles | prefetch **is** the right lever and can lift TX → build it |
| `pre_busy` | is a large share | double-read is structural → **single-pass csum first/too**, prefetch alone won't reach 200 |
| `idle` | dominates | reader is starved of *work*, not reads → re-attribute to CPU/driver, not the reader |

Only after A.5/A.6 do we fix D, decide the csum question, and start the prefetch RTL  -  which is
the whole point of measuring first.
