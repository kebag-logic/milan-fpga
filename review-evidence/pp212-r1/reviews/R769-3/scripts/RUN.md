# How the reviewer receipts were produced (portable)

All runs use the pinned Verilator 5.050 (`receipts/tool-identity.txt`) first on PATH and a
TMPDIR inside the packet's scratch. `<clone>` is a detached clone of the processor at
834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1; nothing is built inside it.

1. Delta arms with their controls (17 arm entries, 4 controls):
   `scripts/run_arms.sh <clone> receipts/arms 14` -> `receipts/arms.out`, `receipts/arms/logs/`.
   Comparison with the author's campaign receipt: `receipts/arms-vs-author.txt`.
2. Probes: `scripts/make_probe_tree.sh <clone> <scratch>/probe scripts/r769_2_probe_block.cpp
   scripts/r769_3_probe_block.cpp`, then `make -C <scratch>/probe/tb/srp_stream_fsms RUN_ARGS=suite`
   -> `receipts/probe-srp_stream_fsms.log`; resulting diff `receipts/probe-srp_stream_fsms.diff`.
   The round 2 block is unchanged (P1-P8); the round 3 block is Q1-Q7.
3. Disposable arm (settled sink takes LINK_DOWN but not LINK_UP): copy the probe tree,
   `python3 -I scripts/plant_settled_begin_dropped.py <copy>`, run the suite as in 2
   -> `receipts/arm-settled-begin-dropped.{diff,log,rc}`.
4. Spot checks in a `git archive` export: `scripts/run_spot.sh <export> receipts/spot`
   (srp_top, srp_stream_fsms suite+walk, lint, area 2x2/8x8 with the author's published
   `area_some.sh`). pp_top was then run per section: `Vpp_top_sim --acmp-only` (AS1-AS9) and
   `--arm-queue-only` (the main Suite plus AQ); a full run exceeded the 10-minute foreground
   bound (`pp_top-full.rc` = 124, no output).
5. Evidence integrity: `python3 -I scripts/verify_evidence_manifest.py <pp212-r1> author-r3/`.
Receipts had the local home directory replaced by `<home>`.
