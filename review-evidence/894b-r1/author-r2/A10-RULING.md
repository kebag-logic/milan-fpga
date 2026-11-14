[A10] **Ruling on the 8x8/1if lane's STOP (issuecomment-6871307898): round 2.** This is a maintainer-delegated decision.

**(a) The two-core trigger is not met.**
- `backlog-owed`'s seven rows are set by the scenario's 60 ms egress hold. They miss in the same way at 1x1/1if and at 8x8/2if, and a second hart can't move them.
- Every CPU-decided measured row holds, and the load is 0.706 of 0.75.
- **The trigger, restated** (#872, issuecomment-6862464924): a CPU-decided measured row over its bound, or the load over 0.75.
- **The held-egress rows stay recorded misses,** in the form 1x1/1if has today: the same row names, recorded in the ledger. A new or larger miss fails the leg. FR_NFR 3.4.1 charges TX backpressure to the service budget, so they are not ruled as passing.

**(b) Round 2.**
- **(i) The MRPDU row's harness budget** derives from `CTRL_LOOP_TX_BOUND_MS` (49 ms after #902's merge), with a planted defect one over. "0 budget misses" means none beyond the recorded egress rows.
- **(ii) `CTRL_LOOP_SRP_UNIT_US` per shape,** at 8x8/1if's measurement plus 5 %. This isn't a STOP condition: a stated cost below its measurement is the defect. The 1x1 and 8x8/2if images stay byte-identical.
- **(iii) The poll costs per shape,** from measurement plus 5 %, with the load recomputed.
- **(iv) Check the firmware first.**
  - Derive 8x8/1if's largest number of pending notices from its descriptors, through the shape header.
  - If that exceeds `AECP_NOTICES_MOST` (12), the queue is undersized there: size it by shape, and prove no notice is dropped, with a plant.
  - Then build the queued-notice and R4L arm at 8x8/1if and measure it: the first notice 20 ms, the last 130 ms, paced R4L 238 ms.
- **(v) The full pass runs once, at the round-2 head.**

**STOP:** the platform image over 56.0 (it has no spare, and (iv) may add RAM), a slice over 1,600 µs, or a changed 1x1 or 8x8/2if image.

**(c) Sequencing.**
- **Now:** (i), the shape keying of (ii) and (iii), the notice-count derivation, and building the arm.
- **After #902 merges:**
  - merge dev-soft-core, and take the shape header as the single source for #902 round 9's direct-index table;
  - check byte-identity against the merged head;
  - then measure, and run the full pass once.
