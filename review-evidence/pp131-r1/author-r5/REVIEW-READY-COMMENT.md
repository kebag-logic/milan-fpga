[A435] REVIEW READY

Head: `9dce84ea60857de74457f74b5bf08d89bd3ba408`, branch `131-d3-core-scalars` (round-4 head `84572585`). Not pushed; the PR is not edited (PR-BODY.md in the packet carries a Round 5 section, and the corrected consolidated parent-visible list is moved there). No STOP: item 3 shows the arbiter behaving exactly as its banner permits. No RTL change.

In the assigned order:
1. **R390-4 F1, the nightly gPTP harness.** `milan_dp` `ax1x1gptp` (`sim_ax1x1gptp.cpp`, run by `milan_dp_gptp`) joins the `PP_CTRL[1]` obligation. The list states that it is outside the consumer set. The walk starts at the top of `configure()`, after the image is served and before the first AECP command, on each boot. The edit is in `parent_edits.py`.
   - Measured in a scratch parent at dev `eaa88a32` with every edit: `make -C tb/verilator/milan_dp ax1x1gptp` rc 0, 139 checks, 0 failures, 17.0 s simulated, 3,277 s of wall time on a loaded host.
   - `milan_dp_gptp`'s own `verify_abort.py` passes 40 of 40.
   - Without the edit (at `84572585`, the same RTL), 15 of 137 fail: every GET_AVB_INFO and GET_AS_PATH check.
2. **R391-4 F1, the timed leg.** The declared `sim_nxn.cpp` edit runs `prove_a_wedged_response_memory_reports_and_heals()` inside the image arm, after the restore and before the `NOTIFY_TIMED_TB` return, in every leg.
   - `notify` passes 378 of 378 with its six `[AECP-WTMO]` checks. R391-4's `parent_scratch.sh` shows the same.
   - The body states that the `[AECP]` degrade arm (5 checks) is retired in every `sim_nxn` leg, because with no image AECP is held from reset (section 8.1). Two hold checks replace it.
3. `9dce84e` **R390-4 S1 = R391-4 S1.** `tb/acmp_nvm` N11 drives manager 1 as N10 does:
   - N11a: a WRITE presented with its abort is never drained, and it completes.
   - N11b: manager 1's abort in the issue cycle of each of the walk's READs drains none of them.
   - N11c: after a WRITE, an issue-cycle READ abort still drains.
   - `issue_arm_cross_intent`, `issue_arm_ignores_we`, `issue_arm_write_too` and `issue_arm_stale_we`, plus `owned_arm_write_too` (the owned half of the same rule, which N11a's held abort grades), join `d3_mutants.py` with README rows. All five are KILLED. `acmp_nvm` has 359 checks.
4. **R390-4 S2.** The image-less legs' check names CLOSED. `wr_chg_o` is on a named no-connect: lint shows 85 warnings against the base's 84 either way, rc 0.

Gates at the head:
- **Processor:** 33 suites, 1,016,035 checks, 0 failing. Lint, `make check`, the module matrix, Yosys, `nvm_port` figures, `git diff --check` and `srp_top` mutants all return rc 0. `d3_mutants.py` kills 81 of 81, goldens PASS, and every README count equals the run.
- **Parent** (scratch at dev `eaa88a32`, gitlink at the head, the corrected edits): the manager's consumer set passes **16 of 16 rc 0**, and `ax1x1gptp` passes 139 of 139.
- **Reviewer scripts:**
  - R390-4's issue-cycle mutants are all KILLED by `acmp_nvm`, and its unit probe passes 9 of 9.
  - R391-4's three S1 survivors now fail N11.
  - E1/E2 and D1 are identical to the reviewers' round-4 receipts.
- **DR3a:** byte-identical to round 4. **DR4:** same-session 1x1 synthesis, lane 1 +1,031 LUT / +559 FF (round 5 adds 0).
- **Section 15.2:** 3 rows updated. The sweep has 704 lines, 357 by this lane, 0 unreviewed.

One arbiter input stays ungraded in the tree, by construction: a manager-1 grant while manager 0 presents an abort. The real binding manager raises its abort only while it owns or strobes its own READ, so no bench can present that input. The reviewer's unit probe covers it.

The `pp131-a435` packet has HANDOFF.md, PR-BODY.md, GATES.md, MUTANTS.md, TABLE-15.2.md, SWEEP.md, `parent_edits.py` with its scratch recipe, and receipts.
