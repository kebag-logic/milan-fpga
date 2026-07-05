# controller_rate — CBS end-to-end shaping/interference reproduction (OPEN BUG)

Self-checking Verilator harness for `traffic_controller_802_1q` (the full
classify → per-queue FIFO → CBS shaper chain), driving the exact scenario the
silicon CBS bring-up hit on 2026-07-05.

**What it documents (docs/CBS_DATAPATH_BUG.md):** under **back-to-back frames that
classify to different queues**, the classifier emits a per-frame-*stable* but
**value-wrong** `tdest` for the first beats of each frame (its 1-beat data delay
cannot cover the 3-beat header parse, and its single staged-header slot lags by a
frame). The `traffic_queues` demux then routes those first beats to the *previous*
frame's queue, so each tight frame loses ~1 beat to the wrong FIFO; those orphan
beats also poison the partner queue's stream and eventually wedge the downstream
store-and-forward PacketFIFO — the TX-dead symptom observed on silicon.

The block harnesses miss it: `tb/verilator/classifier` checks tdest *stability*,
not *correctness*, and never feeds two different-queue frames back to back.

`make` runs the repro and **prints the diagnosis; it exits 0** (it is a documented
open-bug reproduction, not a gating test) until the classifier tdest handoff is
reworked. The fix must: (1) make `tdest` correct from a frame's first output beat,
(2) fix the header-parse FSM's short-frame / back-to-back byte_counter handling,
(3) add a tdest-*correctness* check to `tb/verilator/classifier`, then flip this
harness to gating (`return integrity_fails ? 1 : 0`).
