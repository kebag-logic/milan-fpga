**Ruling on round 4's STOP (the cut, attempt 1).** Decided for the owner under the delegation of 2026-11-11.

**1. The link conflict: a filter.**

- The list keeps a traced entry only if its section links in every image the list serves. Nothing else is dropped, added or reordered.
- The header states the rule, the served images, and each dropped entry with the image that lacks it.
- The LINKED gate and the size fixture stay unchanged. Giving the fixture the queue's code would reopen #894's fixture design, and changing the gate would weaken it.
- Every point is measured with the filtered list.

**2. Restating is allowed, but it does not pass today.**

- The statements are project figures: the most measured plus 5 %, rounded up to 5 us. Earlier PRs restated them. Decision 3 protects the rule, not the figures.
- Item 2 of the second ruling is amended: at the final head, a traced cost may be restated by the unchanged rule.
- A restatement moves no owner bound, no ceiling and no header constant. THE TRANSMIT's 75 ms at 8x8/1if is such a constant.
- Re-graded with attempt 1's figures restated:
  - 8x8/1if fails: load 0.752 of 0.75, and THE TRANSMIT's row 77.09 against 75 ms;
  - 8x8/2if gains a twelfth finding: THE TRANSMIT's row 107.79 against 105 ms;
  - 1x1/1if holds with the paced record at 310 us (ACMP margin 0.07 ms), but at 315 the last queued notice is 141.39 of 140 ms.
- So attempt 2 starts now, beside the final-head measurement. It cuts work in:
  - the 8x8/1if polls base and SRP apply;
  - the 8x8/2if notice item;
  - the 1x1/1if paced record.
- Poll paths are in scope, and wire behaviour stays unchanged.

**3. The SRP condition fails as written. It is met through item 2.**

- Show that the relearned list is no worse for the SRP record than the old list, on the same code, at every point.
- The SRP record must then hold its statement, restated under item 2. The SRP rows, the last queued notice and the load must hold too.
- Record the cause as measured: #936 takes the apply 29 cycles over, and most of the rest came with the cut's placement.

**4. The plan is agreed, with amendments.**

- Swap step 10 to the frozen head `d1aa4c44`, re-trace the list and apply items 1 to 3.
- Re-grade before measuring, and measure 8x8/1if first.
- The 12:00 deadline stands. By then either the final head passes with restated figures, or attempt 2 passes. Otherwise the owner gets the figures, never debt.

**Owner.** Nothing to decide yet, but the owner is told now. On today's figures, the question at 12:00 would be one of two: 8x8/1if's load ceiling and THE TRANSMIT's figure, or Thursday's date.
