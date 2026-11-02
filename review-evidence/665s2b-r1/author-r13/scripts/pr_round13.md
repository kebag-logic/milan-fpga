### Round 13

Both round 12 reviews found passes over the 2.0 ms share that no group staged: a save's flash step beside a composed window's heaviest work, 2.39 and 2.72 ms at 8x8/2if, and both links changing together, 2.08 ms. The share is not amended; each is fixed in code, and each stale statement in text.

| Item | Change | Evidence |
|---|---|---|
| 1. A save in a composed window | THE STEP (`ctrl_loop.h`): the store's centisecond consumer only owes a step; the loop reads the store's clock as a pass starts and, after the polls of a pass that took no event and no record, hands the step the clock's value at which the pass has spent the share. The step is taken only while 1.0 ms (`NVM_STEP_US`) is left; otherwise it stays owed, once. THE SHARE names it | At round 12's head the review's windows reproduce exactly (x-save 2.388 ms, y-save 2.716 ms, y-links 2.081 ms). At this head `backlog-adp`'s window in each flash phase of a save at eight tick phases, both points, both arms, with and without the drafts: 0 of 99,289 passes over the share; a pass carrying a step at most 1.02 ms at 8x8 and 1.22 ms at 1x1. The planted store step (`--mutation store-step-unbounded`, 8x8, arm A): 15 of 24 windows over the share, the longest 2.71 ms, 5 of them with every row within its bound; `CONTROL store-step-unbounded caught` |
| 2. A joint link change | A poll builds one interface at most; the other on the next pass, and it goes first after that | `y-links` 1.76 / 1.82 ms (arm A / arm B), `x-links-same` 1.54 / 1.56 ms, no pass over. `Srp.JointLinkChangeBuildsOneInterfaceAPass` fails on the plant `joint-reset-builds-both` |
| 3. The boot simulation's flash window | The boot SoC on the product's uncached window (`milan_soc.ctrl_uncached_flash`); an export with another is refused; the self-test plants the call's removal | 1x1 25.515 ms, 8x8 64.885 ms to ready (24.660 and 64.271 ms through the cached window at `c954b8a9`, 25.413 and 65.026 ms with the window alone); `PLANT flash-window-cached: caught`, 3 of 3 plants caught |
| 4. Stale statements | The SRP README's share (2.0 ms), the AECP README's 20 ms service bound, the store README's cadence; the platform image's 58.5 tiles; the gPTP additions restated from the table's own units, each a mean or a bound | Section 14 of `SPLIT_CONTROL_MEMORY.md` |
| 5. Residue | A save's time to durable in absolute terms (here and in section 13); the harness README's arm B backlog rows; the interface reset clears `listener_present` (S1, accepted) | `Srp.InterfaceResetClearsListenerPresent`, plant `reset-keeps-listener-present` |

**The first fix was not enough, and its result is kept.** With the room gate alone every pass of the 14 save windows then graded fit, but at 8x8 the deferred read-backs landed in the passes that drain SRP's full ring, and the last SRP record took 18.02 to 18.21 ms against 18 in four blank-check windows. The step now waits for a pass that takes no input, so no record waits on it beyond the pass running when the record arrives.

**The store's steps,** one save with no other load, CPU cycles at 100 MHz, the flash port's and the store's in the step's pass, from a measurement-only build that prints every pass running the flash port (not on this branch):

| Step | 1x1/1if | 8x8/2if |
|---|---:|---:|
| Erase issue | 5,051 | 5,112 |
| Busy poll | 3,994 | 4,710 |
| Blank-check read-back, 128 bytes | 73,491 | 72,841 |
| Page program issue | 95,373 | 95,386 |
| Verify read-back, 128 bytes | 76,234 | 76,737 |

The longest, a page program's issue, is 0.954 ms, within the 1.0 ms the step is given.

**A save from the change to durable,** from the SET_NAME to the end of the step that reads back the container's last bytes, one save with no other load, on the harness's flash model, which has no busy time: at 8x8 4,697.1 ms at round 12's head and 4,697.4 ms at this head; at 1x1 2,018.4 ms. The blank check and the verify read back 128 bytes a tick, 104 ticks each at 8x8, 2.08 s of ticks where a whole page a step took 1.04 s before round 12. The owner's 0.5 s (#823) belongs to the append-only design in Mark II, not to this image, and this PR does not claim it.

**A save's progress.** The store steps only in a pass that took no input. In `backlog-adp`'s window at 8x8 a step owed as the window opened waited until its records had drained, at most 16.95 ms past its tick, and the ticks meanwhile owed it once, so a window delays a save by about a tick. Nothing here bounds that wait under input that never leaves a pass empty.

**The rows with a save in progress** (`backlog-adp`'s window in a save's flash phases; ms, arm A / arm B, bold over the bound):

{{SAVE_ROWS}}

The tightest is the 8x8 last SRP record, 17.29 ms against 18, arm B: 0.43 and 0.83 ms more, arm A and arm B, than `backlog-adp`'s window with no save, since a step can be running when the window's records arrive.

**The rows of the four backlog windows at this head:**

{{ROWS}}

Against round 12's head the 8x8 last SRP record rose from 15.88 / 15.96 to 16.56 / 16.46 ms: a pass of SRP's drain runs 68 more instructions, the clock read as each pass starts, but about 3,300 more CPU cycles, half of them instruction-fetch waits from the moved code layout, and the record waits sixteen passes.

**The per-pass share,** passes over it of the work passes, those that write nothing to the mailbox counted by their run's longest, and the longest in ms (arm A / arm B):

{{SHARE}}

**32x32, an estimate, restated at this head.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

{{ESTIMATE}}

The rows that would not fit: the last AECP record under S, L and U by 8.1, 15.8 and 43.9 ms; the last SRP record by 13.4, 19.1 and 48.2 ms; the longest work pass at 3.5, 4.9 and 7.9 ms, over the share by 1.5, 2.9 and 5.9 ms; under U alone the first SRP record by 4.5 ms, the last ACMP, ADP and MAAP records by 13.3, 4.3 and 4.2 ms, an ACMP command behind a full ACMP ring by 8.0 ms.

**gPTP, a labelled assumption,** restated from the table's own units, a frame or a servo run each, 0.4 ms at 40,000 cycles: on a row 1.1 units, 0.45 ms, as a mean (62 units a second over 18 ms); 20 units, 8.0 ms, as a bound, all that can fall in 18 ms on two ports; on a pass 4 units, 1.6 ms, as a bound (two records a channel a pass). At 8x8/2if the last SRP record, 17.29 ms at its worst, keeps 0.26 ms under the mean and is 0.39 ms over at the range's top, 1.1 ms; the bound puts it 7.29 ms over. The longest pass, 1.98 ms, becomes 3.58 ms under the pass bound. So F6's records need their own room in the pass. At 32x32 the longest pass becomes 5.1 ms under S and 9.5 ms under U, and a Pdelay response, two passes, takes 10.2 ms under S, within Milan v1.2 4.2.6.2.6's 15 ms, and 18.9 ms under U, past it. Not measured: no gPTP firmware is linked here.
