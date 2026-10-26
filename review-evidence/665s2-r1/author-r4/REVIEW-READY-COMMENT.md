[A681d] REVIEW READY
Commit: `a66148f6b7e59e3f42c939f464fe76e2b05404d7` (branch `665-s2-cpu-budget`, PR #792; one commit on round 3's `f8876638`; base `dev-soft-core` `e76a755a`). Not pushed.
Changed: only `tb/verilator/ctrl_service_budget/` (README, grade, run, scenario, selftest, selftest_mutants). No firmware change, and no new measurement.
- **R703-3-F1 (MAJOR):** the comment at `scenario.py:805` now names the ring as `mailbox.yaml` does, "the ACMP transmit ring". `check_baremetal_only.py --check` exits 0 (0 findings across 1431 files), and its term table is unchanged. The gate's own per-file scanner finds 0 findings in each of the PR's 15 files.
- **R703-3-F2:** the composed maximum is the longest pass over every backlog window. Each window committed its defined load. While any window leaves its load unreleased, the figure is labelled a lower bound.
  - `run.composed_maximum` computes it, and each run's `table.md` and `results.json` report it.
  - Arm A: at least 1,565,803 CPU cycles (31.32 ms) at 1x1 and at least 2,209,308 (44.19 ms) at 8x8.
  - Beside it, labelled, is the figure over released windows only: 14.81 / 27.84 ms. Arm B's composed maximum is the same, because every arm B window released its load.
  - README, PR body and hand-off agree.
- **R703-3-F3:** every fan-out range contains every measured fan-out cell.
  - Cost a recipient: 11,786 to 22,030 CPU cycles (11,818 to 20,486 in arm A).
  - Time: 7.77 to 14.80 ms at 1x1 (arm A 7.77 to 11.33), and 12.39 to 32.78 ms at 8x8 (arm A 12.39 to 22.98).
- **R703-3-F4:** two new named checks: `a fan-out's cost a recipient is its first to last commit over the gaps between them`, and `a served record's records ahead are those not yet released at its commit`. Each has its own mutant.
- **Wording residue:** R703-3-R1 (SET_STREAM_FORMAT in Limits), R704-3-R2 (the `backlog_groups` docstring), R704-3-R3 (the owed row's label) and R704-3-R4 (PR body) are applied as written.
Validation (all rc 0 at the head, foreground):
- `python3 scripts/check_baremetal_only.py --check` and `--selftest`.
- `run.py --self-test`: 84 checks, 57 of 57 mutants caught.
- R703-3's `review_mutants3.py`, unmodified: 18 of 21 caught, G6 and G9 among them. G2, G3 and H3 escape, as R703-3 recorded. All 46 anchors are unique at the head.
- R703-2's `review_mutants2.py`: 23 of 25 caught (N11 and N12, as before).
- Round 3's logs, regraded at the head, in six arms and three controls: every group's grade is byte-identical to the regrade at `f8876638`, and only `composed_maximum` is added.
  - 1x1: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
  - 8x8: `17 groups, 102 of 182, 60 of 129`.
  - Arm B: 41 of 68 / 18 of 44 and 60 of 92 / 36 of 68.
  - SHUTDOWN: 0 of 2 and 0 of 3. The three controls are caught.
- 96 gates, one at a time, each rc 0 with the tree clean after it:
  - the docs workflow's check-mode commands and self-tests (docs, doc paths and style, em dash with 0 of 629 added lines, TOC, idiom, hygiene, naming, ports, CI generators, and the rest);
  - the compiler-absent control and the end-station builder gate, each with its one NOT RUN arm;
  - `git diff --check`;
  - `cd tests && behave`: 406/406.
- Not run: the act runner's `--selftest`, which AGENTS.md leaves to the CI job for a candidate's copy.
Acceptance criteria:
- Round-4 items 1 to 5 are met. The STOP condition did not trigger: no firmware change, and no measured cycle count changed.
- Rows within T_svc: not met (the measurement STOP), so the PR body says "Relates to #665".
Open risks/questions:
- **Baseline for S2b and S2c:** arm A's composed maximum over every backlog window, at least 31.32 / 44.19 ms, compared window by window. The released-only figure is not a baseline: a change that lets SRP be served adds windows to it.
- **Not applied:** R-4 / R704-3-R1 (`docs/testing/TESTING.md`, a release-lane file), and R703-3's optional S1 to S3 (H3 still escapes).
- **For the manager (carried):** whether the ACMP owed-capacity drop, the SRP starvation and the per-recipient fan-out cost become Issues or S2b scope.
- **Disclosed:** two of my early gate runs overlapped. Several gates plant a defect in the checkout and restore it, and one run was stopped mid-gate. That left one planted arm in `tb/verilator/csr/Makefile`, which is not this lane's file.
  - The file was restored to the committed content. The tree and submodules were verified clean.
  - Every gate was then rerun serially, with a clean-tree check after each. The validation above is that rerun.
