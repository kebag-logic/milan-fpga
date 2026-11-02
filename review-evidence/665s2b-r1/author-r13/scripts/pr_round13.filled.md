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

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.48 / 1.46 | 1.41 / 1.37 | 1.85 / 1.87 | 1.71 / 1.81 |
| ADP record, first | 20 | 1.47 / 1.45 | 1.40 / 1.36 | 1.84 / 1.86 | 1.70 / 1.80 |
| MAAP record, first | 20 | 1.51 / 1.49 | 1.43 / 1.39 | 1.88 / 1.89 | 1.73 / 1.84 |
| AECP record, first | 20 | 1.52 / 1.50 | 1.44 / 1.40 | 1.89 / 1.90 | 1.74 / 1.85 |
| SRP record, first | 18 | 2.68 / 2.59 | 2.44 / 2.41 | 4.39 / 4.38 | 4.08 / 4.01 |
| ACMP record, last | 20 | 5.95 / 5.92 | 5.47 / 5.33 | 8.89 / 9.30 | 8.20 / 8.39 |
| ADP record, last | 20 | 4.44 / 4.42 | 4.10 / 4.02 | 6.44 / 6.85 | 5.94 / 6.24 |
| MAAP record, last | 20 | 4.47 / 4.46 | 4.14 / 4.06 | 6.48 / 6.89 | 5.96 / 6.28 |
| AECP record, last | 20 | 10.86 / 11.15 | 10.22 / 10.34 | 15.86 / 16.79 | 14.51 / 15.38 |
| SRP record, last | 18 | 11.17 / 11.14 | 10.60 / 10.31 | 16.99 / 17.29 | 15.79 / 15.46 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.57 / 3.55 | 3.32 / 3.26 | 5.29 / 5.40 | 4.87 / 4.96 |

The tightest is the 8x8 last SRP record, 17.29 ms against 18, arm B: 0.43 and 0.83 ms more, arm A and arm B, than `backlog-adp`'s window with no save, since a step can be running when the window's records arrive.

**The rows of the four backlog windows at this head:**

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.79 | 0.71 / 0.72 | 1.32 / 1.39 | 1.23 / 1.24 |
| ADP record, first | 20 | 0.82 / 0.83 | 0.75 / 0.76 | 1.37 / 1.43 | 1.28 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.81 | 0.73 / 0.74 | 1.35 / 1.41 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.82 | 0.74 / 0.75 | 1.36 / 1.42 | 1.27 / 1.28 |
| SRP record, first | 18 | 2.88 / 2.92 | 2.68 / 2.70 | 5.42 / 5.61 | 5.06 / 5.06 |
| ACMP record, last | 20 | 5.06 / 5.18 | 4.79 / 4.60 | 7.85 / 8.31 | 7.28 / 7.37 |
| ADP record, last | 20 | 3.52 / 3.68 | 3.38 / 3.30 | 5.85 / 6.07 | 5.38 / 5.35 |
| MAAP record, last | 20 | 3.54 / 3.72 | 3.42 / 3.33 | 5.84 / 6.06 | 5.36 / 5.33 |
| AECP record, last | 20 | 9.68 / 10.17 | 9.44 / 9.60 | 14.69 / 15.96 | 13.58 / 14.35 |
| SRP record, last | 18 | 10.58 / 10.47 | 9.74 / 9.58 | 16.56 / 16.46 | 15.33 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.59 / 3.63 | 3.27 / 3.28 | 6.59 / 7.01 | 6.36 / 6.37 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.81 / 2.81 | 2.54 / 2.53 | 3.60 / 4.42 | 3.29 / 3.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.10 | 0.13 / 0.06 | 0.12 / 0.12 | 0.19 / 0.25 |
| an event behind 15 others | 20 | 0.92 / 0.93 | 0.85 / 0.88 | 1.47 / 1.54 | 1.38 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.90** / **63.01** | **62.90** / **62.87** | **65.10** / **65.31** | **65.12** / **65.14** |
| a response with 7 frames owed ahead of it | 20 | **62.05** / **62.14** | **62.03** / **62.02** | **63.75** / **64.19** | **63.75** / **63.76** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Against round 12's head the 8x8 last SRP record rose from 15.88 / 15.96 to 16.56 / 16.46 ms: a pass of SRP's drain runs 68 more instructions, the clock read as each pass starts, but about 3,300 more CPU cycles, half of them instruction-fetch waits from the moved code layout, and the record waits sixteen passes.

**The per-pass share,** passes over it of the work passes, those that write nothing to the mailbox counted by their run's longest, and the longest in ms (arm A / arm B):

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1280, 1.10 / 0 of 1251, 1.10 | 0 of 1276, 1.01 / 0 of 1250, 1.01 | 0 of 1314, 1.96 / 0 of 1286, 1.95 | 0 of 1317, 1.86 / 0 of 1286, 1.82 |
| A save's 24 windows | 0 of 11195, 1.22 / 0 of 8643, 1.21 | 0 of 11134, 1.18 / 0 of 8631, 1.16 | 0 of 18088, 1.95 / 0 of 11745, 1.98 | 0 of 18111, 1.86 / 0 of 11742, 1.83 |
| Every group the leg ran | 0 of 19927, 1.22 / 0 of 10496, 1.21 | 0 of 13012, 1.18 / 0 of 10483, 1.16 | 0 of 27214, 1.96 / 0 of 13648, 1.98 | 0 of 20045, 1.86 / 0 of 13645, 1.83 |

**32x32, an estimate, restated at this head.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.79 | 1.17 | 1.39 | 5.5 | 3.4 | 2.7 |
| ADP record, first | 20 | 0.83 | 1.21 | 1.43 | 5.7 | 3.5 | 2.8 |
| MAAP record, first | 20 | 0.81 | 1.20 | 1.41 | 5.6 | 3.5 | 2.8 |
| AECP record, first | 20 | 0.82 | 1.21 | 1.42 | 5.7 | 3.5 | 2.8 |
| SRP record, first | 18 | 2.92 | 4.68 | 5.61 | **22.5** (+4.5) | 14.9 | 11.8 |
| ACMP record, last | 20 | 5.18 | 7.25 | 8.31 | **33.3** (+13.3) | 19.1 | 15.8 |
| ADP record, last | 20 | 3.68 | 5.01 | 6.07 | **24.3** (+4.3) | 14.3 | 11.2 |
| MAAP record, last | 20 | 3.72 | 5.00 | 6.06 | **24.2** (+4.2) | 14.1 | 11.0 |
| AECP record, last | 20 | 10.17 | 13.21 | 15.96 | **63.9** (+43.9) | **35.8** (+15.8) | **28.1** (+8.1) |
| SRP record, last | 18 | 10.58 | 14.91 | 16.56 | **66.2** (+48.2) | **37.1** (+19.1) | **31.4** (+13.4) |
| An ACMP command behind a full ACMP ring | 20 | 3.63 | 5.80 | 7.01 | **28.0** (+8.0) | 18.6 | 14.6 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.81 | 3.90 | 4.42 | 17.7 | 9.9 | 8.2 |
| An event behind 15 others | 20 | 0.93 | 1.32 | 1.54 | 6.1 | 3.6 | 2.9 |
| The longest work pass | 2 | 1.10 | 1.56 | 1.96 | **7.9** (+5.9) | **4.9** (+2.9) | **3.5** (+1.5) |

The rows that would not fit: the last AECP record under S, L and U by 8.1, 15.8 and 43.9 ms; the last SRP record by 13.4, 19.1 and 48.2 ms; the longest work pass at 3.5, 4.9 and 7.9 ms, over the share by 1.5, 2.9 and 5.9 ms; under U alone the first SRP record by 4.5 ms, the last ACMP, ADP and MAAP records by 13.3, 4.3 and 4.2 ms, an ACMP command behind a full ACMP ring by 8.0 ms.

**gPTP, a labelled assumption,** restated from the table's own units, a frame or a servo run each, 0.4 ms at 40,000 cycles: on a row 1.1 units, 0.45 ms, as a mean (62 units a second over 18 ms); 20 units, 8.0 ms, as a bound, all that can fall in 18 ms on two ports; on a pass 4 units, 1.6 ms, as a bound (two records a channel a pass). At 8x8/2if the last SRP record, 17.29 ms at its worst, keeps 0.26 ms under the mean and is 0.39 ms over at the range's top, 1.1 ms; the bound puts it 7.29 ms over. The longest pass, 1.98 ms, becomes 3.58 ms under the pass bound. So F6's records need their own room in the pass. At 32x32 the longest pass becomes 5.1 ms under S and 9.5 ms under U, and a Pdelay response, two passes, takes 10.2 ms under S, within Milan v1.2 4.2.6.2.6's 15 ms, and 18.9 ms under U, past it. Not measured: no gPTP firmware is linked here.
