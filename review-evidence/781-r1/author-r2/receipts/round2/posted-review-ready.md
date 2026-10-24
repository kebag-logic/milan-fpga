[A671] REVIEW READY
Commit: 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 (one new commit on 8a4fa2f9, no rebase or amend; not yet pushed, the manager pushes it to PR #782)
Changed: Round 2 of PR #782 (issuecomment-6390031279).
- `scripts/suite_shards.py`: `media_phase` leaves `PROVISIONAL_SUITES`, which is now empty. `SUITE_SECONDS["media_phase"]` stays 1400. The sources comment records the measurement. The self-test's head arm prints `ok   head no provisional figure is pending`.
- `scripts/run_all_suites.sh`: only the budget's reason comment changes. `suite_timeout` is unchanged at 1400.
- `docs/testing/CI_WORKFLOWS.md`: the #781 budget row records the measurement, and the load paragraph no longer calls `media_phase` provisional.
Measurement: run 40131149135 at 8a4fa2f9, job 120983200812 "Verilator shard 4/17", success. Its suite step ran 20:50:36Z to 21:01:31Z, 655 s for four suites: `suites: 4   passed: 4   failed: 0   timed out: 0`. `suite_shards.py --measure` on the job log gives `media_phase` 582 s, and its uploaded log ends `RESULT: PASS`. That is within 1272 s (1400 s with #673's 10 %), with 818 s (58.4 %) remaining. The budget stays 1400 s, because three earlier hosted windows ran past 900 s.
Validation (all rc 0 at 41f4a53c):
- `python3 scripts/suite_shards.py --selftest`: PASS. Worker 4/17 is 1539 s of 1620, and 16/17 is 2032 s of 2160.
- `python3 scripts/ci_gate_workflows.py --check`: rc 0.
- `python3 scripts/ci_events.py --check`: OK, 2199 items.
- `scripts/run_all_suites.sh --list`, `--ci-pieces --list` and `--ci-pieces --shard k/17 --list` for k = 0..16: 64 suites, 81 units, each owned once. These listings are byte-identical to 8a4fa2f9's.
- `python3 scripts/lint_rtl.py --check`: PASS, 89 <= 89.
- The docs workflow gate steps under GNU Make 4.3, in a clean clone: 42 steps rc 0, with gate_42 and the no-git step covered as before. The LiteX builder leg, the five markdown gates and the no-git gates also pass.
- The trusted dev `act_ci.py --selftest` against the candidate: PASS.
- `cd tests && behave --no-capture -f plain`: 406/406.
- Planted mutants: 8 caught. These include the provisional comparison disabled while nothing is pending, the 582 s figure left provisional, and a misspelt provisional name. There is 1 expected escape, below.
Acceptance criteria: met. The hosted window is measured on this PR's own run and recorded, and `PROVISIONAL_SUITES` is empty. The PR body now says "Closes #781".
Open risks/questions: once `media_phase` is not provisional, no check ties its `SUITE_SECONDS` figure to `suite_timeout`, as for every measured suite. A planted 582 s figure passes the self-test. The kept 1400 s is held by the recorded decision, and the driver's 1400 s by the runner contract. The new head's own hosted run is the final check.
