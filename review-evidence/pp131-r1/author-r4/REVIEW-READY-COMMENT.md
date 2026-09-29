[A432] REVIEW READY

Head: `84572585ea76214c9f15f199590b8fc91f8c7edc`, branch `131-d3-core-scalars` (round-3 head `cbbb5acc`). Not pushed; the PR is not edited (PR-BODY.md in the packet carries a Round 4 section). No STOP: item 1 needed no port change.

Committed in the assigned order, one commit per item:
1. `014e679` **R390-3 F1.**
   - `KL_pp_nvm_mgr_arb` arms the drain on an abort presented with a READ strobe in the issue cycle, for either manager, with no port change.
   - The D3 writer cannot present both: its request is `W_RQ`'s or the service's, its abort `W_RD`'s. `tb/acmp_nvm` N10 drives manager 1 through the case.
   - D3R18 lands the binding walk's fifth READ strobe on `agg_o`'s first clock. The READ is drained from the next clock, the restore ends DEFAULTS, the port comes idle, and a later SET persists.
   - Under the head's arbiter both checks fail: no drain, the port busy 100,000 of 100,000 clocks.
   - R390-3's E1 at this head: the aligned boot drains its READ and the later SET persists. The comments and 07/02 rows state the issue-cycle drain.
2. `8610ab3` **R390-3 F2 + R391-3 F2.**
   - D3R19: the image loaded after reset and proven by the writer's LOCATE after the bound gives DEFAULTS, cause 3, +546 clocks, 0 record READs. With the bound 271 clocks inside that LOCATE: DEFAULTS, image valid.
   - D3R20: a proof on the bound's own clock, in `W_IMG` and in `W_IMGLOC` with the answer in hand, gives DEFAULTS and 0 READs.
   - D3R21: a binding byte in hand on the expiry clock. The walk fails whole at its next waiting clock.
   - The reviewers' five mutants and the head's arbiter (in pp_top and acmp_nvm) join `d3_mutants.py`: 76 of 76 KILLED, goldens PASS, every README count re-measured.
3. **Parent-visible list (PR body only).** Rounds 1-4 are consolidated, with the B1-B4 attribution as measured:
   - pins only: 308/315, from the 100 MHz module default backoff (50 s at 1 MHz);
   - with the derived backoff: 311/315, because the third attempt now outlasts the 1,500 ms fault window;
   - with a 2,000 ms window: 315/315.
4. `8457258` **R391-3 S1-S3.**
   - The firmware wait is 1,000 ms plus two per-wait deadlines plus a few clocks (1,060 ms a stated margin).
   - The two terminal-table points, including 07's new row for the image proof's own per-wait deadline.
   - The binding manager's banner: a direct instantiator derives its clock-referenced parameters.

Gates at the head:
- **Processor:** every suite passes (33 suites, 1,016,031 checks, 0 failing), and every entry point returns rc 0 (lint, `make check`, module matrix, Yosys, `nvm_port` figures, `srp_top` mutants, `d3_mutants.py` 76/76).
- **Reviewer scripts:**
  - R390-3's two survivors and R391-3's three are KILLED.
  - `bind_agg_ignores_byte_in_hand` stays equivalent in effect, as that reviewer judged.
  - D1's five arms match that reviewer's golden.
- **Parent consumer set** (scratch parents at dev `b5c0f69d`, gitlink at the head, the manager's 15 commands):
  - Gitlink only: 10 of 15 rc 0.
  - With the declared edits applied: **15 of 15 rc 0**: `nvm_cosim` quick 315/315, `pp_shadow` 0 failures, `milan_dp` with every pool leg and both mutation campaigns, `milan_dp_render` 65/65 and 152/152.

**Finding on the declared list.** Starting the walk in `gmstep`, `gptp` and `gptp-lat` is necessary but not sufficient. It lets `make` reach `milan_dp`'s pool legs for the first time, and they need the contract's image-before-restore order:
- the image-less legs (main, nolpf, ax1x1, aclk) must accept the CLOSED terminal;
- the `sim_nxn.cpp` legs (notify, nxn, nxndv, nxn8, nxn4c) served AECP with no image, so they must start the walk once the descriptor memory answers.

The same applies elsewhere in the parent:
- `pp_shadow`'s sim runs only once the round-1 ports are connected. Then its K, K10, K12, M2 and P3 phases need the walk and the combined blank.
- `milan_dp_render` T8 needs a one-frame settle: the D3 walk moves the leg 272 axis cycles later.

All of these are parent test-harness edits, named in the list and applied by the packet's edit script. None is a processor change.

DR3a: unchanged on every earlier path; the new paths end +1 to +546 clocks after the bound. DR4, same-instrument 1x1 out-of-context synthesis: lane 1 +1,031 LUT / +559 FF / 0 BRAM / 0 DSP (round 4 adds +1 LUT). Section 15.2: 11 rows updated; the named sweep has 703 matching lines, 356 by this lane, 0 unreviewed.

The `pp131-a432` packet has HANDOFF.md, PR-BODY.md, GATES.md, MUTANTS.md, TABLE-15.2.md, SWEEP.md, the parent edit script, and receipts.
