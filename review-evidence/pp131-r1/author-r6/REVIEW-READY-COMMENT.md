[A442] REVIEW READY

Head: `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f`, branch `131-d3-core-scalars` (round-5 head `9dce84ea`). Not pushed, and the PR is not edited: PR-BODY.md in the packet carries a Round 6 section, and the consolidated parent-visible list moves there. No RTL change.

1. `9b4da6b` **R390-5 F1 = R391-5 S1: the owned half of the owner-matched drain.**
   - `tb/acmp_nvm` N11d holds manager 1's abort, alone, in every cycle manager 0 owns each of the walk's eight READs. Ownership runs from the cycle after the issue through the port's done or err, which a new wrap tap, `arb_end_o`, publishes. The abort is never presented in the issue cycles, which N11b keeps grading.
   - Non-vacuity: the abort is present in 168 of the 168 owned cycles (at least 12 before each READ's end) and in 0 of the 8 issue cycles. Nothing is drained, and the walk completes as saved.
   - `owned_arm_cross_intent` and `cross_own_m1_drains_m0` join `d3_mutants.py` with README rows. N11d alone kills each. `tb/acmp_nvm` has 360 checks.
2. **Docs.**
   - The row in 09 section 8.2 names manager 1's half of each rule as graded (N11a; N11b in the issue cycle and N11d while owned; N11c), and the manager-0 halves as ungraded by construction.
   - The `tb/acmp_nvm` README lists the five manager-0 inputs that R391-5 S1 counts, and why the real binding manager never presents them. It also names the out-of-tree probes: R390-4's unit probe kills three (cases F and B), and no probe kills `cross_own_m0_drains_m1` or `write_own_m0_only`. R391-5's monitor finds none of the five presented with both real managers.
3. **PR body.** The consolidated list now carries two additions:
   - R391-5 S2. In `sim_nxn.cpp` the word-36 check now runs before the moved `[AECP-WTMO]` arm, so the real edit re-reads word 36 after the arm or in its heal. Three comments are stale: the two that R391-5 names, plus a third of the same kind.
   - The five ungraded manager-0 arbiter inputs.

   The scratch edit script is unchanged.

Gates at the head:
- **Processor:** 33 suites, 1,016,036 checks, 0 failing. Lint, `make check`, the module matrix, Yosys, `nvm_port` figures, `git diff --check` and `srp_top` mutants return rc 0. `d3_mutants.py` kills 83 of 83, goldens PASS, and every README count equals the run.
- **Reviewer scripts:**
  - R390-5's `r5_extra_mutants.py --suites acmp_nvm`: N11d kills `r5_owned_cross_m0_only` and `r5_owned_cross_both`.
  - R390-5's R5P probe still plants and passes 361 of 361 at the head. Under that edit, the unmodified harness now fails N11d.
  - The unit probe's output is byte-identical to that reviewer's receipt (9 of 9).
  - R391-5's `run_r391_5.sh ... acmp cross_own_m1_drains_m0` fails N11d, and its other 15 counts equal that reviewer's receipt. Its `check_readme_counts.py` reports 86 entries and 0 problems.
- **Parent** (scratch at dev `eaa88a32`, gitlink at the head, the unchanged edits): the manager's consumer set passes 16 of 16 rc 0, with every reading equal to round 5's.
- **DR3a:** `--dr3a` output is byte-identical. **DR4:** no synthesized file changed, so lane 1 stays at +1,031 LUT / +559 FF.
- **Section 15.2:** 3 rows updated. The sweep has 705 lines, 358 by this lane, 0 unreviewed.

The `pp131-a442` packet has HANDOFF.md, PR-BODY.md, GATES.md, MUTANTS.md, TABLE-15.2.md, SWEEP.md, the unchanged `parent_edits.py`, and receipts.
