# CBS datapath bug — classifier `tdest` mis-timing under back-to-back frames [FIXED]

*Found 2026-07-05 during the hardware CBS interference bring-up (the long-deferred
"prove 802.1Qav protects a reserved class" test); root-caused in sim and **fixed the
same day** (classifier redesign, see "The fix" below). Regression:
`tb/verilator/controller_rate` (gating) + tdest-correctness checks in
`tb/verilator/classifier`.*

## Symptom (silicon)

Programming the CBS shaper on a queue and pushing traffic through it **wedged TX
entirely**: after a two-flow interference run (a tagged PCP-class flow + a best-effort
flow), `eth0` stopped transmitting — the peer saw nothing, and telemetry showed
`tx_core` stalls pegged while `tx_dp`/`tx_wire` sat idle (the store-and-forward
PacketFIFO ahead of LiteEth had latched a partial/merged frame and never drained). A
single-queue `idleSlope` sweep also showed **no shaping at all** (18 Mbit/s offered =
18 Mbit/s delivered regardless of the slope) — the reserved flow was not being
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
   the per-queue FIFOs *accept* more bytes than the shaper mux *egresses* — the orphan
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
  for sub-header runts — garbage-but-deterministic class for an already-invalid frame,
  so the pipeline can never starve) and pushes ONE queue index per frame;
* the output side gates each frame's FIRST beat on its sideband entry and pops at
  `tlast` — `tdest` is correct and stable from the first output beat by construction;
* `data_slice` now resets `byte_counter` on EVERY end-of-frame (the old code only reset
  when `tlast` arrived with `header_ready`, desyncing the parser on tight frames);
* the 1-beat data-delay alignment registers and the single staged header
  (`eth_header_buf`/`packet_in_progress`) are deleted entirely.

`traffic_queues` is **unchanged**: with a correct per-frame `tdest`, its demux (which
samples `select` combinationally at each frame's first beat) and the grant-gated
`axis_arb_mux` are correct. Two earlier theories are explicitly retired:

* the "demux samples select one cycle late" theory — wrong (verified in
  `axis_demux.v`: `select_ctl` is taken comb at start-of-frame);
* the "double-arbiter prefetch eats a beat / cross-locks" theory — an artifact: the
  first repro harness sampled handshakes **after** the clock edge, mis-advancing its
  own feeder and fabricating beat loss that survived every RTL change. With cycle-true
  sampling (drive → settle → sample → edge, like every block harness), classifier v2 +
  the unmodified queues module run byte-exact.

## Verification

* `tb/verilator/classifier`: new **real-header back-to-back alternating-queue**
  scenarios with per-frame `tdest`-**correctness** assertions (and byte-exactness under
  backpressure). The OLD classifier fails these 4 checks (proving both the bug and the
  test); v2 passes 14/14. Wrapper now instantiates `BIG_ENDIAN=0` to match production.
* `tb/verilator/controller_rate`: the end-to-end repro is now a **gating** test —
  back-to-back different-queue frames at ~25 % duty egress pacing, per-frame byte
  integrity, 0 failures.
* Full sweep green after the fix: classifier, cls, queues, shaper_core, cbs, milan_dp,
  csr, datapath, adp, adp_tx, cdc, ptp, ptp_sync, rx_filter, tcam, controller_rate.

## Status

* `CLS_PRIO_REGEN` identity reset — **fixed**.
* Classifier `tdest` mis-timing + parse-FSM end-of-frame handling — **fixed** (this
  commit), silicon CBS interference re-test tracked below.
* Remaining known limitation (architectural, documented in `AVB_SWITCH_DIRECTION.md`):
  single-ingress **head-of-line blocking** — a heavily-shaped queue's backlog stalls
  the shared classifier ingress and starves other queues' *ingress* (egress precedence
  is unaffected). The real cure is per-class TX rings / the multi-queue fabric (S2).
