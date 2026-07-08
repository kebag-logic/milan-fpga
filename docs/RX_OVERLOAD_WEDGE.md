# RX overload wedge — TWO bugs: BD-order inversion + drops/v2-marker alias [FIXED, silicon-validated]

*Found 2026-07-07/08 during the >500 Mbit/s campaign (parallel RX testing). TWO independent
root causes, both localized with the stage probes, sim-repro'd deterministically, fixed and
**validated on silicon**: (1) completion-order inversion — the pending-ACK flush popping a
buffer while an open aggregate held an earlier one (`09e3a09`); (2) the v1 BD's 16-bit
`drops` field aliasing bit 56, the v2 marker, at drops ≥ 256 (`2c44757`) — the one that made
parallel storms lethal and reload-proof. Regression net: `sw/litex/test_ring_bd.py`, 27
tests: driver-model lockstep + content/conservation/FIFO-quiesce checkers, overload storms,
silicon-geometry MSS storms, heal-race sweep, seeded fuzz, and the deterministic repro of
each bug. Final gateware `build_dp100_v2fix` (WNS +0.123) survives the previously-fatal
storm sequence end-to-end (see Status).*

Related: [`CBS_DATAPATH_BUG.md`](CBS_DATAPATH_BUG.md) (an earlier, unrelated TX wedge),
[`CBS_DEFAULT_SHAPING_BUG.md`](CBS_DEFAULT_SHAPING_BUG.md) (found the same night),
[`HW_GRO_RSC.md`](HW_GRO_RSC.md) (the RSC design this bug lives in),
[`PERFORMANCE_GOAL.md`](PERFORMANCE_GOAL.md) (campaign context).

## Symptom (silicon)

Running **parallel RX** (`iperf3 -R -P2`, peer→board, RSC on) reliably killed RX within
seconds: board-side TCP and ping fell 100 % dead, iperf control channels hung, and a
driver reload did **not** recover — only a bitstream reflash did. TX-side parallel storms
(−P4/−P8) intermittently triggered the same state. Single-flow RX ran for minutes
untouched. This gated every parallel-RX measurement (and TX −P4+ stability) of the
>500 Mbit/s campaign.

## Silicon forensics — "delivery dead, hardware healthy"

The decisive observation came from reading the `milan_tlm` stage probes and the RX
writer's own CSRs *while wedged*, with a peer `ping -i 0.3` as continuous stimulus:

| observable | wedged value | meaning |
|---|---|---|
| `rx_wire → rx_core → rx_dp → rx_dma` frames | **all tick in lockstep** (+5 per 5 s of pings) | every HW pipeline stage flows |
| RX writer `wr` / `frames` | advancing (+16/BD, +1/frame) | **HW keeps committing completion BDs** |
| `rx_dropped` | large (e.g. 281–351), static after the burst | buffer-exhaustion drops happened during the storm |
| `occ_hi` | 768 = 48 entries × 16 B | the BD ring hit **completely full** at the burst peak |
| netdev `rx_packets` | **frozen** | the driver delivers nothing |
| board ping / TCP | dead | delivery, not datapath, is broken |

So the wedge is not a hung FSM, an AXI deadlock, or a MAC overflow: **the hardware is
healthy and the driver rejects every completion, forever.** The driver pairs each
completion BD with its posted page **by FIFO order** (`page[comp_i++]` — kl-eth's reap);
whatever broke was a violation of the ordering contract that pairing relies on.

A first defensive driver patch (kl-eth `83aa7ec`: verify the v1 BD's buffer address
against the page-FIFO head and realign on mismatch, plus BD ring 64→256) did **not** fire
on the next wedge (`realign_count=0`) — the first mispaired BD can be a **v2 RSC
aggregate BD, which carries no buffer address** (its w1 holds `{ack, win, segs, doff}`),
so the guard has nothing to re-anchor on. That pointed the hunt at the RTL contract
itself.

## The contract, stated

For blind FIFO pairing to be sound, the `RingDMAWriter` must guarantee:

> **INVARIANT — completion BDs are written in exactly posted-buffer pop order, and every
> popped buffer produces exactly one BD. Drops never pop.**

Deferred-completion holders are the danger: a buffer popped *now* whose BD is written
*later* inverts the order if anything else pops-and-completes in between. There are
exactly two deferred holders in the design:

* the **open RSC aggregate** — pops its buffer at open (`ap_arm` in `WAIT_B`), writes its
  v2 BD only at close (PSH / seg-cap / parked newcomer / `rsc_tout`);
* the **pending merged ACK** — holds *no* buffer at all; it pops one only at flush
  (`ACK_POP`), *completing immediately*.

Every other pop site (IDLE non-RSC, DISPATCH plain/fresh-open, appends) completes before
the next pop. Therefore the **only possible inversion** is: *an ACK flush popping while
an aggregate is open.*

## The repro (sim, deterministic, `test_bd_ack_flush_vs_open_agg_order`)

1. post pages **A**, **B** — driver page FIFO `[A, B]`;
2. `t=0`: a pure ACK arrives → absorbed into the merge slot (no pop), **ack timer starts**;
3. `t=250`: an eligible data segment arrives → pops **A**, aggregate opens, **BD deferred**;
4. idle. The ACK's timer (older) expires first → `ACK_POP` pops **B** → **v1 BD, seq 0**;
5. the aggregate's timer expires later → **v2 BD, seq 1**, its data in **A**.

The checker (a `DriverModel` that mirrors kl-eth's reap bit-for-bit) fails instantly:

```
WEDGE (v1 pairing): BD@+0x0 buf=0x101000 but page-FIFO head=0x100000
  slot0: w0=0x00006312003800bd w1=0x0000000000101000   <- v1 (ACK), used B
  slot1: w0=0x01000060009601bd w1=0x1401200000000000   <- v2 (aggregate), holds A
```

The driver pairs BD0 with page **A** (FIFO head) — wrong page; every later completion is
also shifted by one; the stack drops everything: **the silicon wedge, in two BDs.**

### Why −P2 hits it almost every time

* Two data flows churn the **single aggregate slot** continuously (open A → park B →
  close A → open B → …), so an aggregate is open for a large fraction of wall time.
* The iperf **control connection's pure ACKs** land in the merge slot throughout, and
  each expires `rsc_tout` after its last refresh — frequently mid-aggregate.
* Single-flow traffic closes its aggregate quickly on PSH and rarely leaves the window
  open when an ACK expires — matching "-P2 wedges reliably, single-flow survives".

The `DISPATCH` flush variant (a different-flow pure ACK arriving while one is pending
**and** an aggregate is open → `ack_flush(ret=1)` → same `ACK_POP` pop) is the second
door into the same inversion.

## The fix (`09e3a09`) — BD order == pop order by construction

Never flush the pending ACK while an aggregate is open:

* **IDLE**: the `ack_expired` branch is gated with `~agg_open`. The aggregate's own
  timeout (it shares `rsc_tout`) closes it, after which the still-expired ACK flushes on
  the next IDLE — the added ACK latency is bounded by the aggregate's remaining
  lifetime ≤ `rsc_tout`, i.e. within the merge feature's existing latency budget.
* **DISPATCH**: a different-flow mack newcomer that needs the pending slot while an
  aggregate is open first **closes the aggregate** (the existing parked-newcomer
  `ap_close/ap_csrc=0 → WB → re-DISPATCH` path — the mack frame lives entirely in
  `hdr_reg` and re-dispatches intact), then takes the flush path with the aggregate
  closed.

No BD format change, no driver ABI change, no new state — two guard conditions.

## Verification

`sw/litex/test_ring_bd.py` — **22/22**:

* the 17 pre-existing BD/RSC tests unchanged and green (merge semantics, timeouts,
  seg-cap, alignment sweep, reload hygiene, tiny-drop, ACK-merge eligibility …);
* `test_bd_ack_flush_vs_open_agg_order` — the minimal repro above (fails on pre-fix RTL,
  passes post-fix);
* `test_bd_overload_storm_lockstep` — the −P2 cocktail: two flows churning the aggregate
  slot, ACK-merge traffic, non-TCP frames, buffer exhaustion with **no reaping**
  mid-storm, timeout closes firing dry, partial replenish;
* `test_bd_heal_race_lockstep` — `kl_bd_resync` under fire: ring disabled mid-traffic at
  5 phase offsets (incl. mid-frame), model heals like the driver, seq must restart at 0
  and pair `page[0]`;
* `test_bd_overload_fuzz` (2 seeds) — randomized op mix (segs/ACKs/non-TCP/posts/gaps/
  reap-bursts/rare heals) against the checker.

The **`DriverModel`** class in that file mirrors kl-eth's reap exactly (magic + seq
lockstep, FIFO page pairing, v1 address assert, v2 content assert, heal) — it is the
permanent regression net: any future RSC/BD change that breaks the ordering contract
fails these tests with a full BD-ring/page-FIFO/trace dump.

## Defense in depth (driver, kl-eth `83aa7ec`)

* v1-BD **address-verify + `comp_i` realign** (recycles skipped pages, rate-limited
  warn) — now expected to never fire, kept as the canary: a single "bd realign" line in
  dmesg means the HW contract broke again;
* `KL_BD_ENTRIES` 64→256 — reap slack so BD-ring-full (a contract stressor) needs a 4×
  longer driver stall.

## Status — silicon results (2026-07-08, `build_dp100_wfix`, WNS +0.092)

* **The ordering fix is VALIDATED on silicon**: across every storm run of the session —
  including one that moved 193 MB / ~15 k completions with 897 buffer-exhaustion drops —
  the driver's realign **canary stayed at 0**: completion order never again diverged
  from post order. RX single-flow with RSC on measured **202 Mbit/s** on the fixed
  gateware. The pre-fix `-R -P2` trigger no longer produces the mispairing wedge.
* **The SECOND bug — the parallel-storm delivery death — is ROOT-CAUSED AND FIXED
  (2026-07-08, commit `2c44757`), decoded directly off a dead board's BD ring.**
  The v1 completion BD packed **16-bit `drops` into w0[63:48], overlapping bit 56 —
  the v2-aggregate marker** (the v2 encoding correctly used `drops[:8]`; the v1 line
  kept 16 — the inconsistency was the bug). Once the free-running famine counter
  crossed **256** — which only parallel storms achieve — **every v1 completion parsed
  as a v2 aggregate in the driver**: garbage-gso deliveries (`segs` decoded from a
  buffer address's zero byte — the observed `+192 B / +0 pkt` netdev signature), then
  with the half-BD guard a permanent reap stall. Every mystery symptom follows:
  - **parallel-only**: single-flow never accumulates 256 drops; −P2/−P4 famine does;
  - **`rsc=0` immune**: the driver's v2 branch is `kl_rsc`-gated;
  - **reload-proof**: `drops` is free-running HW state — it stays ≥256 across driver
    reloads; only reboot/reflash (counter reset) recovered;
  - **canary silent**: the v2 path never runs the v1 address-verify;
  - the sticky `rsc_dbg=0x800` was a red herring — that's the **ARP ptype** (bytes
    16–17 = `08 00`) of the peer re-ARPing a dead board.
  Forensic chain: dead-state BD dump showed "v2" BDs whose fields decoded as sane v1
  values with `drops=294` → deterministic repro (`test_bd_drops_overflow_v2_alias`:
  260 famine drops, then one plain frame → its BD reads v2) → one-line fix (v1 w0
  carries `drops[:8]`, bits [63:56] forced 0) → repro passes, suite **27/27**
  (incl. the new storm-hunt battery: `StormModel` content/conservation/FIFO-quiesce
  invariants, silicon-geometry MSS storms, heal races, fuzz). Driver ABI unchanged
  (kl-eth never read v1's drops field). **SILICON-VALIDATED on `build_dp100_v2fix`
  (WNS +0.123): the exact single→P2→P4→P2→single storm that previously died at the
  first −P2 ran clean end-to-end — 192/145/112/142/196 Mbit with pings alive after
  every stage, canary=0, and `drops=4792` (18× past the old 256 kill threshold).**
* **Also hardened while hunting** (`12265b5`): the completion BD lands as two beats —
  a poll can see w0 before w1; the driver now treats `w1==0`/`segs==0` as
  not-yet-complete and retries (was: garbage-gso delivery of half BDs).
* **Sim findings for the record**: the writer has **no BD-ring fullness guard** —
  more outstanding buffers than BD entries silently overwrites unreaped completions.
  The driver contract (48 posted < 64 entries, reap-before-repost) makes it
  unreachable today; documented as a constraint. The `KL_BD_ENTRIES` 256 driver
  experiment (`e251a0c` revert) likely broke this very contract-boundary — with the
  alias bug now fixed it could be revisited, but 64 works and stays.
* Follow-on (unblocked): completion-IRQ NAPI for the 3–11 ms idle RTT; then the RX
  parallel matrix and 2-queue fan-out numbers.

## Lessons

* **Stage probes + "the books must balance" localize a wedge in minutes**: `wire=core=
  dp=dma` all ticking while netdev froze converted "the link is dead" into "the driver
  rejects completions" — the whole hunt followed from that one read.
* **Blind FIFO pairing is a contract, not a convention** — either the hardware proves
  completion order == pop order (this fix), or every completion must carry its buffer
  identity (v2 BDs don't have room). State the invariant; test the invariant.
* A **driver-model checker in the RTL sim** (not just protocol asserts) is what turned
  the storm into a two-BD repro: the model fails at the exact completion where the
  driver would, with the evidence attached.
