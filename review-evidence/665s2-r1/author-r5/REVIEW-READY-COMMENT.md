[A681e] REVIEW READY
Commit: `f58d049beb377c3f535628067022d4d5b51e8208` (branch `665-s2-cpu-budget`, PR #792; two commits on round 4's `a66148f6`; base `dev-soft-core` `e76a755a`). Not pushed.
Changed: only `tb/verilator/ctrl_service_budget/`: `run.py`, `selftest.py`, `selftest_mutants.py` and the README. No firmware change, and no new measurement.
- **R703-4-F1:** `run.composed_maximum` now names the backlog rows a run did not include, in `not_run`, with `rows` and `partial`. `table.md` labels such a figure, for example `Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 740,260 CPU cycles (14.805 ms), backlog.` A run of all four rows prints the same line as before, so arm A's tables are unchanged.
  - Arm B is not re-measured: running `backlog-adp-refill` there would be a new measurement, and it would change arm B's published figures.
  - The README and PR body state arm B's coverage: `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`, a partial figure.
  - New check: `a run without every backlog row names the rows not run, and its composed maximum is partial`, with a mutant that drops the rule.
- **R703-4-F2:** two more checks, each with its own mutants.
  - `the composed maximum is a lower bound while a window shorter than the longest left its load unreleased`: the longest window released its load, and `lower_bound` must be `True`.
  - `results.json's composed maximum is the record the table renders, with its lower-bound and partial labels`. The `results.json` record now comes from `run.summary`. The check compares it with the expected record, and the rendered table line word for word: a lower bound, a partial figure, and both at once.
- **R703-4-R1:** the PR body row is renamed as written.
- **Found this round:** two rows of the README's mutant table named a check that no longer fails first. Round 4's records-ahead check refuses under those two mutants, and the self-test counts a refusal as caught. The rows now name the refusal printed. All 62 rows match the self-test's output.
Validation (each rc 0 at the head):
- `run.py --self-test`: 87 checks, 62 of 62 mutants caught.
- R703-4's `r703_4_probes.py`, unmodified, on a clone of the head:
  - **P3, P4, P5 and P7 are caught**; P1, P2, P8 and P10 stay caught;
  - D1 reports `"not_run": ["backlog-adp-refill"], "partial": true`, and the line `Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): ...`;
  - P6 and P9 escape (R703-4's optional S1 and S2, not applied);
  - `git status --porcelain` is empty afterwards.
- R703-3's `review_mutants3.py`: 18 of 21 caught (G2, G3 and H3 escape). R703-2's `review_mutants2.py`: 23 of 25 (N11 and N12). Both are unchanged from round 4, and all 56 anchors are unique.
- Round 3's logs, regraded at the head in six arms and three controls:
  - every log and every group's grade is byte-identical to round 4's regrade;
  - the `results.json` composed-maximum record gains only `rows`, `not_run` and `partial`;
  - `table.md` changes only on arm B's composed line, which now reads partial at both points;
  - the summaries are unchanged: 1x1 `58 of 141 / 22 of 81`, 8x8 `102 of 182 / 60 of 129`, arm B `41 of 68 / 18 of 44` and `60 of 92 / 36 of 68`, SHUTDOWN `0 of 2` and `0 of 3`; the three controls are caught.
- 96 gates, run one at a time by one serial runner, each rc 0 with the tree clean after it:
  - `python3 scripts/check_baremetal_only.py --check`: `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`;
  - the full docs-check set, i.e. the docs workflow's check-mode commands and self-tests: docs, doc paths and style, em dash (0 of 643 added lines), TOC and anchors, idiom, hygiene, naming, ports, CI generators and the rest;
  - the compiler-absent control and the end-station builder gate, each with its one NOT RUN arm;
  - `git diff --check`;
  - `cd tests && behave`: 14 features, 406 scenarios, 1977 steps passed.
- Not run: the act runner's `--selftest`, which AGENTS.md leaves to the CI job for a candidate's copy.
Acceptance criteria:
- Round-5 items 1 to 3 are met. No firmware change, and no measured cycle count changed.
- Rows within T_svc: not met (the measurement STOP), so the PR body says "Relates to #665".
Open risks/questions:
- **Baseline for S2b and S2c:** arm A's composed maximum over the same four backlog rows, at least 31.32 / 44.19 ms, compared window by window. A partial figure and the released-only figure are not baselines.
- **Arm B** stays partial unless a later round measures `backlog-adp-refill` there.
- **Not applied:** R-4 / R704-3-R1 (`docs/testing/TESTING.md`, a release-lane file) and R703-4's optional S1 to S3.
- **For the manager (carried):** whether the ACMP owed-capacity drop, the SRP starvation and the per-recipient fan-out cost become Issues or S2b scope.
- **Disclosed:** a first gate run at `ee710802` was stopped between gates, once the mutant-table rows were found and the head had to move. Its compiler-absent gate was allowed to finish and restore what it plants, and the tree was verified clean. The full set was then rerun at the head; that rerun is the validation above.
