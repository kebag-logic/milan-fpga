[A794] STOP addendum (not posted: the round allows one STOP comment, issuecomment-6942842392; this is for the manager)

**A second STOP condition, found after the STOP was posted: composed 1x1/1if rows over their bounds (provisional).**

Measured on a probe tree, step 7 composed in a throwaway worktree with the undecided ledger hunks taken from #931 (the
ledger question does not reach the firmware image). The formal legs ran at 1x1/1if: arm A in 8 parts, answering-every-port in 2, answering-ports `aecp`, `aecp-fanout`, `aecp-largest-notice` and `aecp-reboot`, and valid-destinations' SRP Talker groups. All 15 parts finished; `srp-talker` adds nothing.

- **Every leg** (15 of 15): 0 refusals, no `STATED` failure, 0 passes over the per-pass share. The only budget misses are `backlog-owed`'s seven held-egress rows, 61.8 to 63.7 ms, the ruled recorded misses.
- **The longest queued notice** is 23.37 ms against 140. All four saves are durable within their stated worst cases.
- **The record classes refuse the largest legal command's record.** `aecp-largest-notice`, a REMOVE then an ADD of 63 mappings, takes 99,468 CPU cycles in arm A and 99,397 in arm B. That is 1,045 us by the rule, over `rows_tiers.LONG_RECORD_US`'s 975 us at 1x1/1if. #931 measured 92,714 cycles on its own head, exactly at 975 by the rule, and left the statement; the composed image is about 6,750 cycles dearer on that record.
- **By the rule the composed statement is 1,045 us.** With that figure the tier model's 1x1/1if txL row by every source is **49.31 ms, over its 49 ms bound** (`flip_grade.py --check --point 1x1/1if`: `OVER 1x1/1if txL ... 49.31 ms`). Every other row holds: R4 13.42, R5 76.50, R6 74.00, first 14.74, last 137.89 (140), R4L 203.65 (238), ACMP 29.91, ADP 28.12, MAAP 28.21, tx 34.28.
- **The statement survey** (#665 round 28's tools, as #914's lane ran them; all 15 legs) finds four more statements under the composed measurement by the rule:
  - `event.AECP`: 7,519 cycles, 80 us, against 75 in both columns;
  - `event.MAAP`: 15,744 cycles, 170 us, against 165 in `STATED_US`;
  - the datapath events `AS_PATH_CHANGED` and `AVB_INFO_CHANGED`: 3,571 and 3,480 cycles, 40 us each, against 35 (`rows_tiers.DATAPATH_US`).
- **Every one restated by the rule** (receipts/survey/flip-1x1-restated.diff, a scratch copy): three 1x1/1if rows by every source go over their bounds.
  - **The last queued notice: 142.44 ms, past the amendment's 140 ms ceiling.** `queued_bound.py` then hands it to the owner.
  - **ACMP: 32.89 ms, over 30.**
  - **txL: 49.66 ms, over 49.**
  - Every other row holds: R4 13.50, R5 77.02, R6 74.50, first 14.78, R4L 203.70, ADP 28.32, MAAP 28.41, tx 34.54. The load is 0.523 at the pin, ceiling 0.70.
- So the composition, measured, puts three 1x1/1if rows over their bounds. Neither the bounds nor the rule may move in this lane; this needs a decision (a cut in the record path, or a ruling) like #895's and #897's compositions had.

Caveat: the probe tree is not the final composed head. #914's head moved twice after its NEGATIVE reviews, to `e1ecce20` (R843-7 POSITIVE there, R844-5 POSITIVE at its ancestor `d0a2a160`), and the harness hashes the firmware tree, so these figures are repeated at the final head. The record path's code does not depend on the ledger decision, so the over-bound rows are expected to stand.

Evidence: receipts/legs/ (each part's log), receipts/budget/p1x1/ (each part's table and results), receipts/survey/record-classes-p1x1.txt, receipts/survey/survey-p1x1.out and p1x1/, receipts/survey/flip-1x1-long-record-1045.* (the largest record alone) and flip-1x1-restated.* (every restatement), each on a scratch copy of the probe.

**A third STOP condition: #933's PHY poll and #938's store pace contradict each other in THE STEP (firmware).**

- **#938 (#920)** makes the saved-state store take a step in every pass that took no input and has room while a save
  is in flight, "one a pass, the centisecond's or not" (`nvm_store.h`; `ctrl_loop.h`, THE STEP).
- **#933 (#919)**: `ctrl_plat_phy_store_step` gives the PHY a frame only in a call whose store took no step of a save.
- **Composed, the PHY gets no frame while a save is in flight.** That is about 1.1 s typically and up to 6 s at
  1x1/1if; the saves' stated worst cases reach 22 s at 8x8. During that time the 125 ms poll, the latched-loss
  publication and the link-up edge that ends gPTP's Pdelay_Req cease all wait.
- **#933's own test catches it** on the composed tree, at one and two interfaces:
  `Phy.B12StepCarriesTheStoresSaveOrAPhyFrame` fails with "B12 a call with no store step carries the PHY's frame"
  (17 frames where 18 are expected). Its premise, one store step a centisecond, no longer holds once #938 steps every
  pass.
- The test passed at step 5. In the first composition the firmware suites were not run at step 6; they were run at
  the recomposed tip (`7431b6ba`), where they fail.
- Keeping both rules fails #933's test and #919's poll period during saves. Which one yields (a PHY frame beside the
  store's per-pass step when the pass has room, or the store's extra steps yielding to an owed PHY frame) changes
  THE STEP's cost per pass and so the CPU budget rows. That is a design decision neither PR's rulings settle.

Evidence: receipts/firmware/tip-fw0.log (shard 0 at `7431b6ba`, platboot if1 and if2); the control campaign there
catches 792 of 793, its one escape (`plat-phy-store-owed-dropped`) a plant into the same failing test
(receipts/firmware/tip-fw1.log). The AECP and SRP campaigns pass there.
