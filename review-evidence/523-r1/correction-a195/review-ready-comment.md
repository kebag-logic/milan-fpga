[A195] REVIEW READY
Commit: 015edd9ab2248289ff000f6ef14890be1812ba7b (tree fc03d0313af978c147bf734f9905fdc427a2b758; parent 26353960). Committed in the lane but not pushed; pushing is left to the manager.
Answers: R257-2-F1 MINOR Tests (https://github.com/kebag-logic/milan-fpga/pull/526#issuecomment-5793808280)

Changed: `scripts/test_suite_cancellation.py` only, +63 -7. No production, docs, workflow or ratchet change.
- `cancel_report()` (test_suite_cancellation.py:114-127) is now asserted by every graceful INT/TERM cancellation arm. It requires three things:
  - the shell's own line, `CANCELLED: INT|TERM; no completed sweep result`. The owner's `signal N` line no longer satisfies the check;
  - after log preparation (preflight, command, transition): exactly one `partial logs: <requested OUT>` line and no not-prepared line;
  - before preparation (selection, lock wait): `logs were not prepared for this invocation`, no `partial logs:` line, and the previous invocation's logs in OUT byte-unchanged.
- A new `lock_wait()` arm for INT and TERM (test_suite_cancellation.py:211-242).
  - The test holds the tree lock and the sweep runs with `--wait`. The boundary is the sweep shell's own `flock` child, observed in /proc under the launched entry, with no delay or shim.
  - Expected: exit 128+N, the not-prepared report, previous logs intact, and no prerequisite or suite run.
- The normal sweep preflight still runs this file (`scripts/run_all_suites.sh:272`, unchanged), so it owns the new arms.

Mutation evidence: single-defect copies of `run_all_suites.sh` (disposable `git archive` copies; the lane was never mutated). Each copy was run against the base test (26353960) and the new test (015edd9a):
| Mutant | Base test | New test |
|---|---|---|
| none (unmodified) | PASS | PASS |
| logs-ready-early | PASS | RED (cancel_report:125, selection arm) |
| logs-ready-never-set | PASS | RED (cancel_report:123) |
| no-partial-logs-message | PASS | RED (cancel_report:123) |
| no-term-trap | PASS | RED (cancel_report:119) |
| no-int-trap | RED | RED (cancel_report:119) |
| no-unprepared-message | PASS | RED (cancel_report:125) |
| report-inverted | PASS | RED (cancel_report:125) |
| partial-logs-wrong-dir | PASS | RED (cancel_report:123) |
| int-reported-as-term | PASS | RED (cancel_report:119) |
| prepare-before-lock | PASS | RED (lock_wait:240 only) |
- The mutant names follow the finding. The textual edits are the author harness's own; the reviewer's probe script was not used.
- Through the normal entry point, a disposable copy with `logs-ready-early` makes `bash scripts/run_all_suites.sh OUT` exit 2 with `ABORTING: sweep cancellation controls failed.` A PATH make guard kept any suite from building.
- In the unmodified copy, the sweep's own `preflight/test_suite_cancellation.log` shows both lock-wait arms and `suite cancellation: PASS`.

Validation at 015edd9a (clean tree):
- `python3 scripts/test_suite_cancellation.py`: exit 0, 40 s.
- `python3 scripts/check_py_idiom.py`: exit 0.
- `python3 scripts/check_sh_idiom.py`: exit 0.
- `make -C tb/verilator/gptp_shadow lifecycle`: exit 0, 47 s, `mutant lifecycle: PASS`, nested-SIGINT 130, nested-SIGTERM 143.
- Lock-wait arms repeated 25 times per signal: 50/50 pass.
- On the byte-identical pre-commit worktree: `check_py_idiom.py --selftest` 0 (54/54), `check_sh_idiom.py --selftest` 0 (48/48), `measure_fail_fast.py --check` 0, `measure_test_evidence.py --check` 0.

Acceptance criteria: unchanged; this commit changes only test assertions. It closes the R257-2-F1 gap: the attribution report at both boundaries, for both signals, and the shell's own CANCELLED line now have controls that fail when the report is removed or corrupted.

Open risks/questions:
- The lock-wait arm needs flock(1), as the existing `lock_free()` check already does. The mkdir fallback is not exercised.
- Not run: full banks, act/Docker, hosted CI (head not pushed), hardware.
- The Tests lens needs re-review at 015edd9a. No other lens's scope is touched.
- Author handoff (HANDOFF.md, receipts, harness, MANIFEST.sha256) is in the author output directory: 2026-09-23/523-a195.
