# CBS datapath bug  -  classifier `tdest` mis-timing under back-to-back frames [FIXED]

*Found 2026-07-05 during the hardware CBS interference bring-up (the long-deferred
"prove 802.1Qav protects a reserved class" test); root-caused in sim and **fixed the
same day** (classifier redesign, see "The fix" below). Regression:
`tb/verilator/controller_rate` (gating) + tdest-correctness checks in
`tb/verilator/classifier`.*

## Symptom (silicon)

Programming the CBS shaper on a queue and pushing traffic through it **wedged TX
entirely**: after a two-flow interference run (a tagged PCP-class flow + a best-effort
flow), `eth0` stopped transmitting  -  the peer saw nothing, and telemetry showed
`tx_core` stalls pegged while `tx_dp`/`tx_wire` sat idle (the store-and-forward
PacketFIFO ahead of LiteEth had latched a partial/merged frame and never drained). A
single-queue `idleSlope` sweep also showed **no shaping at all** (18 Mbit/s offered =
18 Mbit/s delivered regardless of the slope)  -  the reserved flow was not being
credit-limited.

## Root cause (sim-confirmed, `tb/verilator/controller_rate`)

Two independent defects compound; the first is the wedger:

1. **The classifier emits a per-frame-*stable* but value-*wrong* `tdest` for the first
   beats of a frame.** `traffic_classifier` delays the data path by a fixed 1 beat
   (`LATENCY`) and drives `tdest` combinationally from a single staged header
   (`eth_header_buf`, held via `packet_in_progress`). The Ethernet header parse needs
   **3 beats** (24 B ≥ the 18 B header at 64 bit/beat), so under **back-to-back frames
   the first ~2 output beats of frame *N* carry frame *N−1*'s classification**. The
   downstream `traffic_queues` demux latches the route at start-of-frame, so those
   beats are steered into the **previous frame's queue**. Byte accounting in the repro:
   the per-queue FIFOs *accept* more bytes than the shaper mux *egresses*  -  the orphan
   beats are stranded in the wrong queue, every tight frame comes out ~8 B short, and
   the stranded/merged beats eventually deadlock the downstream PacketFIFO (the TX
   wedge). The block harness `tb/verilator/classifier` misses this because it only
   checks `tdest` **stability within a frame**, never **correctness of the value**, and
   never feeds two different-queue frames back-to-back.

2. **The header-parse FSM mishandles short/tight frames.** In `data_slice`, a `tlast`
   beat that arrives while `!header_ready` takes the increment branch (not the reset
   branch), so `byte_counter` is not cleared at end-of-frame; the next frame's beat 0
   then finds `header_ready` already true and is neither counted nor shifted into
   `eth_header`. This corrupts classification of the following frame independently of
   defect 1.

A third, unrelated issue found in the same pass and **fixed** here: `CLS_PRIO_REGEN`
reset was `0x688FAC`, a half-swap of priorities (0–3 ↔ 4–7) instead of the 802.1Q
identity `0xFAC688`, so every tagged SR frame was priority-regenerated into the wrong
class before it even reached the (buggy) queue routing. Fixed to identity in
`hdl/csr/milan_csr.sv` + `REGISTER_MAP.md` (verified: `tb/verilator/cls`,
`tb/verilator/classifier` green with the identity constant).

## The fix (shipped)

`traffic_classifier` redesigned around a **per-frame `tdest` sideband queue**:

* the input side classifies each frame as soon as its header completes (or at `tlast`
  for sub-header runts  -  garbage-but-deterministic class for an already-invalid frame,
  so the pipeline can never starve) and pushes ONE queue index per frame;
* the output side gates each frame's FIRST beat on its sideband entry and pops at
  `tlast`  -  `tdest` is correct and stable from the first output beat by construction;
* `data_slice` now resets `byte_counter` on EVERY end-of-frame (the old code only reset
  when `tlast` arrived with `header_ready`, desyncing the parser on tight frames);
* the 1-beat data-delay alignment registers and the single staged header
  (`eth_header_buf`/`packet_in_progress`) are deleted entirely.

### Second defect: arbiter cross-lock in `traffic_queues` (the actual TX wedger)

With the classifier `tdest` fixed, single-flow shaping worked on silicon (see
Verification)  -  but a **two-flow interference** run still wedged TX. Root cause,
localized in `tb/verilator/controller_rate` (mixed ACK-sized + MTU frames, alternating
queues) via a full grant-state dump:

`traffic_queues` drained the per-queue FIFOs through an `axis_arb_mux`  -  its **own**
round-robin arbiter with a per-frame lock  -  fed by grant-gated valids. That stacks a
**second arbiter on top of the CBS grant**, and the two can lock onto *different*
queues: the mux latches its round-robin pointer at one frame's start, then the CBS
grant moves to another queue at the next frame boundary; the mux waits forever for a
valid from its now-ungranted (gated-off) input while the granted queue's full FIFO
never drains. Dump at the hang: `grant=q1, hold=1` but the mux parked on q0,
`queue_to_shaper` valid stuck at 0, `dep1=1024` (full). A hard circular deadlock  -  the
TX wedge.

**Fix:** replace the `axis_arb_mux` with a plain **combinational mux selected by the CBS
grant**. `traffic_shaping_core` already frame-locks the grant (`hold_grant` until
`tlast`), so a single grant-indexed selector *is* the arbiter  -  there is no second
pointer to diverge. (An earlier "demux samples `select` one cycle late" theory was
checked and retired: `axis_demux.v` takes `select_ctl` combinationally at start-of-frame,
and with a correct per-frame `tdest` the input demux is fine  -  only the *output* mux
needed the change.)

**Harness-sampling trap, for the record:** the first repro sampled handshakes *after*
the clock edge, mis-advancing its own feeder and fabricating a phantom "one beat short
per frame" that survived every RTL change and briefly sent this investigation down a
wrong path. Fixed to cycle-true sampling (drive → settle → sample → edge, like every
block harness); the mixed-size scenario then cleanly exposes the real cross-lock and
verifies the fix byte-exact.

## Verification

* `tb/verilator/classifier`: new **real-header back-to-back alternating-queue**
  scenarios with per-frame `tdest`-**correctness** assertions (and byte-exactness under
  backpressure). The OLD classifier fails these 4 checks (proving both the bug and the
  test); v2 passes 14/14. Wrapper now instantiates `BIG_ENDIAN=0` to match production.
* `tb/verilator/controller_rate`: the end-to-end repro is now a **gating** test  - 
  a **mixed ACK-sized + MTU, alternating-queue** stream at ~25 % duty egress pacing
  (the interference profile), content-checked byte-exact with a deadlock detector.
  Reproduces both the classifier `tdest` bug and the arbiter cross-lock on the OLD
  RTL; 0 failures / no deadlock on the fixed RTL (219 frames, 140,430 bytes).
* Full sweep green after the fix: classifier, cls, queues, shaper_core, cbs, milan_dp,
  csr, datapath, adp, adp_tx, cdc, ptp, ptp_sync, rx_filter, tcam, controller_rate.

## Silicon verification (ring9 = classifier fix only, 2026-07-05)

Hardware CBS on `eth0`, reserved = VLAN PCP1 UDP (→ shaped queue), q idleSlope 10 Mbit/s,
peer i210:

| phase | config | offered | delivered | verdict |
|---|---|---|---|---|
| A | CBS on, under slope | 8 Mbit/s | **7.98** | reserved passes untouched |
| B | CBS on, over slope | 18 Mbit/s | **9.95** | clipped to idleSlope, 0 loss |
| C | CBS off (strict-prio) | 18 Mbit/s | **17.9** | control: unshaped |

Textbook 802.1Qav, and the `PRIO_REGEN` identity reset put PCP 1 on the shaped queue
straight from reset (no table pokes). **But the two-flow interference run still wedged
TX**  -  that is the arbiter cross-lock above.

## Silicon re-test with the cross-lock fix (ring10, 2026-07-05)

Same rig, now with **two concurrent flows**  -  reserved VLAN-PCP1 UDP (shaped q,
idleSlope 10 Mbit/s) *and* a best-effort TCP flood  -  the exact scenario that wedged
ring9:

| flow | offered | delivered | loss |
|---|---|---|---|
| reserved (shaped) | 8 Mbit/s  | 4.86 Mbit/s | 0 |
| reserved (shaped) | 18 Mbit/s | 4.86 Mbit/s | 0 |
| best-effort TCP   | line      | 6.7–23.8 Mbit/s |  -  |

**TX never wedged**  -  both flows ran to completion and the board pinged clean at
~0.58 ms immediately after each pass (ring9 hung permanently here). The arbiter
cross-lock is fixed on silicon.

Residual, expected behavior (NOT a bug  -  the documented single-ingress limit): the
reserved class flows losslessly but is **throughput-degraded to ~4.86 Mbit/s** (below
its 10 Mbit/s reservation) while best-effort runs, because both classes share ONE
classifier ingress  -  BE frames occupy ingress slots and delay reserved frames into
their queue. CBS still bounds egress correctly (single-flow B clips to 9.95); it cannot
protect the *reservation* from ingress contention when ingress is shared. The cure is
per-class ingress / the multi-queue fabric (S2 in `AVB_SWITCH_DIRECTION.md`).

## Status

* `CLS_PRIO_REGEN` identity reset  -  **fixed**, silicon-confirmed.
* Classifier `tdest` mis-timing + parse-FSM end-of-frame handling  -  **fixed**,
  single-flow CBS shaping silicon-confirmed (A/B/C above).
* `traffic_queues` arbiter cross-lock (two-flow TX wedge)  -  **fixed** (grant-indexed
  mux), sim-verified; silicon interference re-test on ring10.
* Remaining architectural limit (documented in `AVB_SWITCH_DIRECTION.md`): the shared
  single-ingress classifier means a full queue backpressures *ingress* for all queues
  (bounded, not a deadlock, once the cross-lock is gone). Per-class ingress / the
  multi-queue fabric (S2) is the structural cure.
