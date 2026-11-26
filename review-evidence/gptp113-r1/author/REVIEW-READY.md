# [A854] gptp113: REVIEW READY

**Mister-M-alt/FPGA-gPTP issue #113**, branch `113-runner-ratchets` from main `3009f9a2` (#112). It is local in
the lane clone. It was not pushed and nothing was posted.

**Head: `af11b3ef631eb44cdc1730cfb31bedda95c33dc5`.**

| Commit | Subject |
|---|---|
| `f3b24f3c` | Document and annotate the engine runner's public functions, and drop make()'s unused stdout parameter |
| `af11b3ef` | Move the engine passes test to tb/, beside the mutation arm's scheduling tests, outside the suite directory |

There is no change under `hdl/` and no microcode change. Four files are touched: `pass_run.py` (docstrings
only, the same program by its AST), the test (moved), the engine Makefile's `passes-test` recipe and comment,
and one row of `docs/TEST_DEVELOPER.md`.

## Acceptance

| Criterion | Result | Receipt |
|---|---|---|
| 1. Both consumer ratchets pass with unchanged budgets at a pin of the fix | `check_py_idiom.py` rc 0 and `measure_test_evidence.py --check` rc 0 (3 <= 3 wall-clock files). Probe: milan-fpga `dev-soft-core` `c34e7d8b` plus local commit `f791fdea1f`, which moves only the gitlink. Budgets diffed: unchanged. Both self-tests pass. | `logs/consumer-ratchets-af11b3e.log`, `logs/*-selftest-af11b3e.log` |
| 2a. `make passes-test` as in PR #112 | 73/73 on four runs at this content (one under `ulimit -c 0`). The 13 planted defects are caught at both layouts with equal failing-check counts. Controls 73/73. | `logs/head-gates/`, `logs/plants-r1.log` |
| 2b. The engine's four passes as in PR #112 | `-j4` clean pair rc 0/0: IDENTICAL, 179 lines. Planted abort pair rc 2/2: IDENTICAL, 64 lines, with passes 2 and 3 `stopped` in both. | `logs/engine/compare.txt`, `logs/engine/pass-records.txt` |
| The repository's own checks | `make docs`, `contract` and `lint` are rc 0 at the committed head (Verilator 5.050) | `logs/head-gates/` |

## The choice for the wall-clock ratchet: move the test, with the evidence

- **Sites.** `passes_test.py` matches the consumer's rule at 13 lines (`logs/clock-sites-3009.log`):
  - stub run lengths and timestamps (4), which make real passes overlap under make's jobserver;
  - hang bounds (3);
  - the fail-fast elapsed time (2);
  - the signal check's start wait and grace (4).
  - None is a DUT oracle. The test observes host-process scheduling, stopping and signalling.
- **Why not a controlled clock.** It would need budget-aware barriers in the stubs, a rewrite of most checks,
  and the loss of the hang bounds. That fails "behave as in PR #112". The consumer's own process tests keep
  such bounds on purpose (#833's comment in `scripts/process_test_support.py`).
- **Precedent.** Both repositories already keep such tests outside the suite directories:
  - gPTP: `tb/mutation_order_test.py` and `tb/mutation_jobs_test.py`, which use `time.monotonic` and `time.sleep`;
  - milan-fpga: `scripts/test_suite_cancellation.py` and `process_test_support.py`.
- **Result.** The moved file still reads host time; it is no longer in the suite population.

## Deviations from the brief

- **The "8-parameter function".** No function has 8 parameters. The consumer counts *functions* over its limit
  of 6. #112 raised that count from 7 to 8, against a budget of 7, through `passes_test.make()`, which takes 7
  parameters. `make()` now takes 6, by dropping a `stdout` parameter that no caller passed.
- **The donor patch was checked, and used in part.**
  - It applies cleanly to `3009f9a2`, and its `stdout` removal is behaviour-neutral. Its docstrings for `main`
    and `read` are used.
  - Its renames of the closures to `_chunk`/`_forward`/`_stop`/`_caller` were not used. Those closures got
    docstrings instead, and `caller` got a `limit` annotation. The issue asks for the functions to be documented,
    not made private.
- **One command ran in the background.** The plant matrix (28 runs, 3 at a time) passed the 600 s foreground
  limit, and the harness moved it to the background. It completed, exit 0, in about 17 min. Every other command
  ran in the foreground.
- **The consumer probe is a clone, not a worktree.** It is a fresh clone of `dev-soft-core`
  (`$VALIDATION_STORAGE/gptp113-a854-milan`). It was made with `--reference` to an existing clone and then
  `--dissociate`, so no other lane's repository was touched.

REVIEW READY af11b3ef631eb44cdc1730cfb31bedda95c33dc5
