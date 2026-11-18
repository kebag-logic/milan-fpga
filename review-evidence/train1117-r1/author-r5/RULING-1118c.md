**Ruling: #927 and the flip train.** Decided for the owner under the delegation of 2026-11-11.

**1. #927 joins the train as step 11.**

- The 11-16 ruling (#927 issuecomment-6930885657) kept #927 out because the base met #818's floor.
- The composed train now misses that floor at 8x8/1if on all three directives (best +0.005 ns). The failing path is the EDIT-window path that #927 cuts.
- The standing timing rule asks for a logic cut and allows no floor exception. So the membership point of that ruling is reversed. Its floor grading stands.
- PR #939 is frozen at `0297a19a`. It is adopted only after two POSITIVE reviews at that head. Wording-only findings are residue.
- Composition and routes may start now, ahead of the reviews. Their results count only if the reviewed head is unchanged.
- The composition review covers the step-11 merge and any resolution that touches logic.

**2. What is measured again.**

- 1x1/1if and 8x8/1if are routed on all three directives. Fit and the floor must hold on the best of three at each point.
- The CPU rows need no full re-measure if both of these hold:
  - each firmware image is hash-equal to the measured one, per arm and point;
  - a confirmation run gives cycle figures identical to the candidate's receipts, with an empty diff.
- The confirmation run covers:
  - at 8x8/1if: `srp-talker-held`, the answering-ports arm, and `aecp-fanout`;
  - at 1x1/1if: `aecp-largest-notice` and `aecp-fanout`;
  - one group at 8x8/2if.
- Any hash or cycle difference means everything is measured in full.

**3. The date.**

- Thursday 11-19 stays the target. The owner is told now that it is at risk.
- A slip is the owner's decision. This ruling sets no fallback date.
- It goes to the owner at once if any of these happens:
  - a #927 review is NEGATIVE beyond residue;
  - the composed routes miss the floor at either point;
  - the candidate fails;
  - anything else puts the final bitstream past Thursday morning.
- The gating S12b runs, uncut, on the final bitstream only. A run on a pre-#927 image is a rehearsal.
