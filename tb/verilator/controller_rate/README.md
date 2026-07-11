# controller_rate — CBS end-to-end shaping/interference regression (bug FIXED; gating)

Self-checking Verilator harness for `traffic_controller_802_1q` (the full
classify → per-queue FIFO → CBS shaper chain), driving the exact scenario the
silicon CBS bring-up hit on 2026-07-05.

**What it documents (docs/findings/CBS_DATAPATH_BUG.md):** under **back-to-back frames that
classify to different queues**, the classifier emits a per-frame-*stable* but
**value-wrong** `tdest` for the first beats of each frame (its 1-beat data delay
cannot cover the 3-beat header parse, and its single staged-header slot lags by a
frame). The `traffic_queues` demux then routes those first beats to the *previous*
frame's queue, so each tight frame loses ~1 beat to the wrong FIFO; those orphan
beats also poison the partner queue's stream and eventually wedge the downstream
store-and-forward PacketFIFO — the TX-dead symptom observed on silicon.

The block harnesses miss it: `tb/verilator/classifier` checks tdest *stability*,
not *correctness*, and never feeds two different-queue frames back to back.

**Status: the bug is FIXED** (classifier per-frame tdest sideband redesign, same day)
and this harness is **gating** (`make` fails on any per-frame byte-integrity error).
It drives back-to-back different-queue frames with randomized ~25 % duty egress
pacing through the full chain — the scenario every block harness misses.
