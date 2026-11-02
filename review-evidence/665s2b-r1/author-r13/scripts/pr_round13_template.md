### Round 13

Both round 12 reviews found reachable passes over the 2.0 ms share that no group staged. The share is not amended; each finding is fixed in code or text.

| Item | Change | Evidence |
|---|---|---|
| 1. A save in a composed window | THE STEP (`ctrl_loop.h`): the store's centisecond consumer only owes a step, and the loop takes it at the end of a pass that still has 1.0 ms (`NVM_STEP_US`) of the share, read off the store's clock as the pass starts. A step without room waits for the next pass with room, owed once | At round 12's head, R711-2's windows reproduce exactly: {x_save} and {y_save} ms. At this head, `backlog-adp`'s window in each flash phase at eight tick phases, both points, both arms, with and without the drafts: {save_share}. The planted store step: {ctl} |
| 2. A joint link change | A poll builds one interface at most; the other on the next pass, first | `y-links` and `x-links-same` at 8x8, both arms: {links} |
| 3. The boot window | The boot SoC on the product's uncached flash window; an export with another is refused, and the self-test plants its removal | 1x1 {boot_1x1} ms, 8x8 {boot_8x8} ms to ready; `PLANT flash-window-cached: caught` |
| 4. Stale statements | The SRP README's share (2.0 ms), the AECP README's 20 ms bound, the store README's cadence; the gPTP additions from the table's own units, mean and bound | Section 14 |
| 5. Residue | The save's time in absolute terms; arm B's backlog rows; `listener_present` cleared by the interface reset | Below; `Srp.InterfaceResetClearsListenerPresent` |

**The store's steps on the product SoC,** CPU cycles at 100 MHz, one save with no other load:

{steps_table}

**A save from the change to durable,** at 8x8, measured on the harness's flash model, which has no busy time: {durable_before} at round 12's head, {durable_after} at this head. The read-back is {readback_ticks} ticks at 8x8, the blank check and the verify together. The owner's 0.5 s (#823) belongs to the append-only design in Mark II, not to this round, and this PR does not claim it.
