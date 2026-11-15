[A773] STOP

Head: `783b1596d4acb431698c6e5da9d3f4506cfc091e` (`894-tiers`), twelve commits on round 11's `9606b3a9`. Nothing is pushed.

Round 12, under #894's ruling issuecomment-6883864236, with the SRP drain item (issuecomment-6886633874) done before its final pass. Every 1x1/1if row held after the cut, the pace and the class (steps 2 and 3). The final pass then measured four 1x1/1if costs over their statements, and restated by the rule they put one row over its bound.

**Exit: STOP to the maintainer, on two triggers at 1x1/1if** (the ruling's first STOP, and R837-6-F1's slice rule).
- **The last queued notice is 132.71 ms against its 130 ms** by every source, at the built design (slice 900 us, tier 1 aecp-first, tier 2 srp-first, AECP queue). It takes 70 passes, two more than before the restatements, and its largest term is SRP's 26.32 ms. `flip_grade.py --check --point 1x1/1if` exits 1.
- **The slice rule leaves the built design.** `tier_grid.py --point 1x1/1if` holds 10 of 420 candidates and chooses slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, at a least margin of +0.0116. No other order holds.
- **The four restatements,** each by the rule (cycles / 100 x 1.05, up to 5 us), on the final firmware `a47cd3f2`:

| Cost at 1x1/1if | Measured, CPU cycles | Rule | Stated before | Where | Before this round |
|---|---:|---:|---:|---|---:|
| A build of one (and an owed MRPDU) | 69,635 | 735 | 725 | arm A `srp` | 68,972 |
| A TICK | 4,784 | 55 | 50 | arm A `backlog-adp@program-0` | 4,692 on the drain's earlier figure |
| AECP's timer slot | 6,206 | 70 | 65 | answering-every-port arm, 6 of 16 groups | 5,753 at `9606b3a9` |
| A LINK | 14,715 | 155 | 150 | arm A `fixture` | 13,956 |

- **What tips the row.** The build of one or the TICK, either alone, puts the last queued notice over: 132.64 and 132.65 ms. Without both it is 127.98 ms. The timer slot and the LINK move no row past its bound.
- **Why the costs moved.**
  - The first three are the same work as before this round, moved by the SET_CONFIGURATION cut's code (216 B of rom an image). The traced timer-slot event has 1,024 commits against 1,030, and 479 more cycles of instruction-fetch stalls.
  - The TICK moved with the SRP drain's record cost (below).
  - `CTRL_LOOP_BUILD_ONE_PASS_US` feeds only a static assertion. Every image is byte-identical between `a47cd3f2` and the head.
- **Every other 1x1/1if row holds** by every source:
  - R4 13.05 (20), R4L 188.43 (238), ACMP 28.90, ADP 27.25 and MAAP 27.37 (30);
  - the first queued notice 14.61 (20), R5 74.02 and R6 69.81 (90);
  - tx 33.33 and txL 48.38 (49).
  - The load is 0.516 at the pin and 0.512 in the second column, against 0.70.
  - The pace stays 8 ms by its rule.
  - Joins are 187.994 to 190.021 ms in arm A and 185.486 to 190.147 ms over every leg, within 181.0 to 239.0.
  - Every image is within its cap: the 8x8/2if platform has 152 B spare.
- **No bound, ceiling or the every-source rule moved, and no gate was weakened.** The cut is not wire-visible against Milan v1.2 5.4.2.5 or IEEE 1722.1-2021 7.4.7.

**The SRP drain's record cost** (`1c0ca94b`, `a47cd3f2`; from #895 issuecomment-6886630886 item 8).
- `CTRL_LOOP_SRP_UNIT_US` is now the load gate's `record.srp` at each point, the dearer column's: 280 us at one interface (250 before) and 365 at two.
- `load_grade.py --check` refuses any other figure by name. At 250 it fails with `1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us`.
- A planted control at each point is refused (26 of 26).
- `Loop.L23TheDrainIsTierTwoInASlice` reads the constant; the loop arm passes all 51 tests.
- Only the one-interface images change (`ctrl_loop.o`, at equal sizes). Every two-interface image is byte-identical, so the 8x8/2if legs stand. Every one-interface leg was measured again at `a47cd3f2`.

**Round 12's items:**
- **1, the attribution** (one traced pass on round 11's answering-ports builds, images equal to `9606b3a9`'s).
  - At 1x1/1if the record's 33,724 cycles are 6,322 commits, 16,131 cycles of short stalls, 8,823 of fetch stalls and 2,448 of data stalls. Of them, the change's publication is 8,376, every stream entry's write and lookup 4,294 of that; the 4 streams' running checks are 6,618, and the descriptor scans 6,198.
  - At 8x8/2if, of 78,332: the publication is 27,666, every stream entry 19,905 of it, and the 18 streams' running checks 22,704.
  - The arm's stream port is the harness's and reads no window, so the product's six GSI reads a stream are not in the measured record.
- **2, the cut, once** (`f275b619`).
  - The running check reads one GSI word a stream, selector 0, the proof that its window answers. Bound and running come from their owners.
  - A configuration's stream entries are written only when its index moves.
  - Statuses, their order and the notify rule are unchanged. A SET naming the index in force still answers STREAM_IS_RUNNING while a stream runs, and ENTITY_MISBEHAVING when the window is silent.
  - The record is 28,509 cycles at 1x1/1if (300 us) and 55,377 at 8x8/2if.
- **3, paced** (`fe0cef5b`, `e4d80a8a`). An accepted SET_CONFIGURATION stamps THE PACE and shares the edits' count. The paced class is the dearer member's by the rule: 300 us at 1x1/1if (28,376 cycles), and 595 at 8x8/2if (56,474). The planted control that charges an unpaced SET_CONFIGURATION as ordinary is refused by name, in the model and in the pass check.
- **4, the completion tick.**
  - In the answering-ports arm the accepted command never waits, since its commit is acknowledged inside the port.
  - The window's only TICK precedes the command: 2,159 cycles at 1x1/1if (25 us) and 2,404 at 8x8/2if (30), within 50 and 40.
  - A late acknowledgement's completion, which republishes an owed interface whole, is staged by no arm.
- **5, the pass check.** `record_classes.py` holds arm B's SET_CONFIGURATION and SET_STREAM_INFO by class, and refuses a pass lacking them. It names a record only by a response before the next record starts (R837-6-S2). Its 11 planted controls are refused. Over every final leg the result is PASS: paced 300 of 300, ordinary 235 of 235 and long 925 of 975 at 1x1/1if.
- **The new code's checks.** Five new tests, and thirteen campaign rows, each caught by name.

**Validation** (clean clones, never piped):
- **Final firmware `a47cd3f2`:**
  - the full arm A at 1x1/1if: 96 groups, 0 refusals, the 7 known held-egress misses, 0 of 139,988 passes over THE SHARE;
  - the whole answering-every-port arm at 1x1/1if (16 groups): rc 0;
  - the 1x1 and 8x8-1if legs: the same exit codes as round 11;
  - the firmware jobs: 22 steps rc 0. The AECP campaign catches 299 of 299 rows and the control campaign 716 of 716; `fw_coverage.py --check` PASS;
  - the four-shard sweep (each on its own picked range): every shard's command rc 0.
- **The 8x8/2if legs:** two-interface images unchanged, so they stand.
- **At the head's statements, the stated-table compare at both points by leg prefix** leaves only the class lines (at 8x8/2if, #910's build of one too).
- **`94e828ed`, before the drain item:** the RTL and elaborate jobs and lane parts b and c, rc 0. They were not run again at the final firmware.
- **At the head:** `docs_check.py`, `check_em_dash.py` and both idiom gates, 0 findings.
- **Not run:** lane part a, rtl-fast's other jobs and the docs jobs. The head fails the row gate, so the round stops first.

**The delta reviews' findings** (R837-6, R838-6) are answered:
- **F1's survey** found the timer slot, and arm A's the others.
- **Rom** is stated per image: round 11 added +224 B to the 1x1 images and +208 B to the 8x8 images.
- **Section 13's current figures** are the head's.
- **The comments** name no review round or lane.
- **The headings and the wording** are corrected.
- **The packet's index** is generated after sanitizing and read back.

**For #894's 8x8 lane** (8x8/2if, reported): R4 44.24, R5 206.45, R6 196.31, the first queued notice 20.93, the last 806.60, R4L 195.76, ACMP 67.94, ADP 68.08, MAAP 69.13, tx 98.49 and txL 459.40 ms. The load is 0.794, and 0.754 in the second column. The paced class is 595 us.

**Decision needed:** the last queued notice at 1x1/1if is 132.71 ms against 130 at the built design, with a build of one at 735 us and a TICK at 55. The slice rule's choice is 950 us.
