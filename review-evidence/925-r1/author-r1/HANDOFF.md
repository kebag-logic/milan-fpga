# HANDOFF — lane 925 ([A790])

**Round 2 (from 07:12): see [../round2/HANDOFF-r2.md](../round2/HANDOFF-r2.md).** The ruling on the STOP is #925
issuecomment-6908876793 (routes: misses at the base, owed to #927). Round 1's status below is as it ended.

**Status (07:2x CET 2026-11-16): round 1 STOPPED, posted once on #925 (issuecomment-6908790238).** The split images
at 1x1/1if and 8x8/1if miss the +0.030 ns WNS/WHS floor on all three directives (6 to 22 ps); the base's own
1x1/1if image misses it too (16 ps on hold, the same FIFO). The fix (`95426618`), its tests and plants are done;
head `1be0a6c4` (three commits on #901's review head `16ba667d`), not pushed. Every other gate run is green, but
for the 8x8/1if budget point's STATED lines (not SRP's: the shape's known excess over the one-interface statements).
The sweep is not run (it may not run beside a route, and needs the decision's head).

- Round 1 detail (step 1 report, changes, checks and plants, gates, images, incidents, notes for the manager):
  [HANDOFF-r1.md](HANDOFF-r1.md). STOP text: [STOP-COMMENT.md](STOP-COMMENT.md); TAKEN: [TAKEN-COMMENT.md](TAKEN-COMMENT.md).
- PR body draft for after the decision: [PR-BODY.md](PR-BODY.md); REVIEW READY draft with placeholders for after the decision: [REVIEW-READY-DRAFT.md](REVIEW-READY-DRAFT.md) (not posted).
- Receipts: `receipts/` with `INDEX.md`. Scratch: `/data-2/milan/tmp/925-a790` (clones `c/`, budget builds `b/`,
  routes `rt/`, workflow replay `wf/`, units' logs `units/`).
