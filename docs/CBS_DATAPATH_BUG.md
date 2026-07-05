# CBS datapath bug — classifier `tdest` mis-timing under back-to-back frames

*Found 2026-07-05 during the hardware CBS interference bring-up (the long-deferred
"prove 802.1Qav protects a reserved class" test). Root-caused in sim; the RTL fix is
scoped below as a follow-up. Reproduction: `tb/verilator/controller_rate`.*

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

## The fix (scoped follow-up — not shipped in this commit)

The classifier needs `tdest` correct **and** stable from a frame's *first* output beat.
The clean shape (attempted, reverted for careful re-verification):

* replace the fixed 1-beat data delay + single staged header with a **per-frame `tdest`
  sideband FIFO**: push one classification per frame when its header parses, pop one per
  output `tlast`, and gate a frame's first output beat until its entry exists;
* rework `data_slice`'s end-of-frame handling so `byte_counter`/`eth_header` reset
  correctly on every `tlast` including sub-header-length and back-to-back frames;
* keep `traffic_queues` as-is (its demux is correct **given** a correct per-frame
  `tdest`).

Verification gate for the fix:

1. add a `tdest`-**correctness** assertion to `tb/verilator/classifier` (each frame's
   output `tdest` must equal the independently-computed expected queue), with a
   back-to-back different-queue scenario;
2. flip `tb/verilator/controller_rate` from a print-only reproduction to a gating test
   (`return integrity_fails ? 1 : 0`);
3. on silicon: re-run the CBS interference test — a reserved class shaped at `idleSlope`
   keeps ~its rate with low jitter while a best-effort flood saturates the link, and TX
   never wedges.

## Status

* `CLS_PRIO_REGEN` identity reset — **fixed** (this commit).
* Classifier `tdest` mis-timing + parse-FSM short-frame handling — **open**, reproduced
  deterministically in `tb/verilator/controller_rate`, fix scoped above.
* Until fixed, **do not enable CBS shaping on a queue that carries live traffic** on
  silicon (it can wedge TX). Unshaped operation (the default for BE/control queues) is
  unaffected — all the throughput results in `RX_RING_DMA.md` ran with CBS effectively
  transparent.
