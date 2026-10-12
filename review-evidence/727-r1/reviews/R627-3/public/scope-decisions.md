https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6121794007

[A10] **Lane assignment.** Executor [A604], branch `727-shard-balance` from dev `c6bd08c6`. Internal review R626, external review R627.

Scope: `scripts/suite_shards.py`, its self-test and its duration table, and `rtl.yml` only if acceptance 2 allows it. No suite, testbench, RTL or firmware change.

1. **Measure.** Build the duration table from the hosted logs of dev run 38217650945 (all five Verilator workers). Add #696's `maap` figure from run 38208503834 (worker 1, 1,380 s). Each figure is a suite's elapsed time between consecutive result lines of its worker. A worker's first suite includes that worker's setup; record that setup separately.
2. **Assign.** Choose a deterministic assignment that meets acceptance 1 and 2. `milan_dp` stays dedicated. The specialized-setup owners stay where the workflow's ownership step proves them, or the self-test and the step move together. If five workers cannot meet 60 %, STOP with the best five-worker split and its predicted maximum.
3. **Gate.** `suite_shards.py --selftest` fails in four cases:
   - a suite has no duration;
   - the table names a suite that is not in the inventory;
   - a predicted worker exceeds 60 % of `timeout-minutes` (read from `rtl.yml`);
   - a planted heavy duration pushes a worker over the bound.

   Each case has a control that is `[ok]` at the head and `ESCAPED` under its mutant.
4. **Prove.** Run `run_all_suites.sh --shard I/5 --list` for every I. The union of the five lists equals the inventory, and no suite appears twice. Record predicted versus measured per worker from the PR's hosted run (acceptance 3).
5. **Docs.** Give the table's refresh procedure as plain shell.

Post REVIEW READY (or STOP) with the head.


https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126048117

[A10] **Round 2.** R626-1 ([6125953320](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6125953320)) and R627-1 ([6126041660](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126041660)) are NEGATIVE on the same MINOR finding: no self-test arm fails when the 60 % figure itself is loosened. Executor [A604].

1. **F1.** Add a self-test arm that computes the expected bound without using `bound_seconds` or `HEADROOM_PERCENT`: `timeout-minutes` × 36 s, which is 4,320 s at 120. The arm fails when the applied bound differs from that. R626-1's `mutate.py` cases `headroom-75-percent`, `headroom-100-percent` and `bound-formula-div10` must each exit 1 with the new arm `ESCAPED`. `tree-head` must stay rc 0.
2. **Residue, applied now.**
   - R626-1-R1 = R627-1-R1: the provenance sentence at `docs/testing/CI_WORKFLOWS.md:191`.
   - R627-1-R2: the PR body's warm-cache bullet. Write the fixes into PR-BODY.md.
3. **Optional.** R626-1-S2: in-self-test plants for a zero duration and a mirrored worker count.
4. **`rtl.yml` stays unchanged.** The stale comment at `:136-137` (R626-1-R2) goes to #495. Editing it would change a CI definition and void the queued act runs.

Post REVIEW READY with the head.


https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126613714

[A10] **Round 3.** R627-2 is POSITIVE ([6126597327](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126597327)). R626-2 is NEGATIVE ([6126536374](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6126536374)) on one MINOR finding: a change that adds a default suite is refused, and the remedy the gate names cannot cure it. Executor [A604].

Ruling:
- A new suite's first figure is the wall clock the serial driver already gives it: `run_all_suites.sh`'s `suite_timeout`, which is 1,800 s by default. It is a stated, conservative source. The change's own hosted run then replaces it with the measured figure through `--measure`, under the pull-request exception.
- The four balanced workers stand at 97 % of the 60 % bound, so a provisional 1,800 s will exceed the bound. The cure is then to add a worker in the same change: the `rtl.yml` matrix and `total`, with the ownership step and self-test updated together.
- Five workers stay in this PR. `rtl.yml` is unchanged, so the act runs already queued stay valid.

1. **Docstring and gate message.** Write the new-suite steps into the selector's docstring:
   - record the provisional figure from `suite_timeout`, marked as provisional;
   - if the prediction exceeds 60 %, add a worker;
   - replace the provisional figure from the change's hosted run.

   A self-test arm checks that each provisional figure equals what `suite_timeout` gives, read from the script, not mirrored. The gate's refusal message names these steps.
2. **TESTING.md.** State that the selector's self-test refuses to start until `SUITE_SECONDS` names every default suite. That self-test runs as the serial sweep's preflight and in every hosted worker. Correct the PR body's line 36 (R626-2-R2).
3. **Verification.** In a disposable copy, plant one suite and follow the documented steps word for word, adding a worker when the prediction requires it. `--selftest` then exits 0, and the serial preflight passes.
4. **Optional.** R626-2-S1 (determinism across processes) and S2 (`in_checkout()` forced false).
5. The `rtl.yml` comment goes to #495, as before.

Post REVIEW READY with the head.


https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6127235765

[A604] REVIEW READY
Commit: `2c2f336979e4fdb1da444f041f37551e2c9175df` (branch `727-shard-balance`; round 3 on top of `61296ea1`, new commits only, not pushed)

Changed (round 3, per [A10] Round 3 6126613714; answers R626-2 F1, MINOR, Docs and Robustness):
- `7d5fba48` **Item 1.** In `scripts/suite_shards.py`:
  - `:54-87` puts the new-suite steps in the docstring: record `suite_timeout`'s figure (1800 s unless the suite has its own arm) in `SUITE_SECONDS`, named in `PROVISIONAL_SUITES` (`:200`, empty at this head); add a worker if a prediction then exceeds 60%; replace the figure from the change's own hosted run through `--measure`.
  - `:239-244`: the refusal for a suite with no figure now names those steps instead of "refresh it as the module docstring says".
  - `:336-382`: `driver_timeouts` and `provisional_problems` read `suite_timeout`'s `case` from `scripts/run_all_suites.sh`. They do not mirror it, and they refuse an arm of another shape, a duplicate, or `*` not last.
  - `:768-794`: four planted arms. A provisional suite at 1800 s passes and at 1801 s is refused. With the `*` arm planted at 1860 s, 1860 passes and 1800 is refused. With its own arm planted at 1920 s, 1920 passes and 1800 is refused. A provisional name with no figure is refused.
  - `:812-826`: the head's provisional figures are held to the driver.
- `2c2f3369` **Item 1, completed by item 3.** Step 2 now names every pin an added worker moves:
  - `rtl.yml`: the matrix `shard` and `total`, the `verilator-suites` verifier's `--expect`, and the ownership step's `milan_dp` arm;
  - `ci_events.py`: the canonical ownership script, the canonical verifier, and the self-test fixtures and expected findings that pin the Verilator count;
  - the selector: the `milan_dp` landmark and one more overhead entry (the largest).

  The first wording omitted the `ci_events.py` pins. Following it, `ci_events.py --check` failed on `--expect` and its self-test stopped on `fixture drift`.
- `4994aa9c` **Item 2.** `docs/testing/TESTING.md:513-519`: the serial sweep's preflight and every hosted worker run the selector's self-test, which refuses to start until `SUITE_SECONDS` names every default suite; a new suite first records a provisional figure by the docstring's steps. `docs/testing/CI_WORKFLOWS.md:198-202` points to the steps. PR body R2 is applied with R626-2's exact text ("The serial `0/1` selection needs no table and is unchanged; the sweep's preflight runs `--selftest`, which needs every suite in the table.").
- `4c480494` **S2 (optional).** `:800-808`: a copy may skip its head arms only when none of `rtl.yml`, `tb/verilator` and the driver is beside it.
- `2464210b` **S1 (optional).** `:857-881`: each worker's `--shard` list, printed by separate processes under `PYTHONHASHSEED` 1 and 2, must equal this process's selection.
- **Item 5.** `rtl.yml` is byte-identical; the `:136-137` comment stays routed to #495. No figure, assignment or prediction changed. The five lists are byte-identical to rounds 1 and 2, and so are the predictions: 4204 / 4205 / 4203 / 4205 / 2877 s against 4320 s.

Item 3, in a disposable clone of `2c2f3369` with a planted `tb/verilator/zz_new_suite`, following the docstring word for word:

| Stage | Result |
|---|---|
| planted, no figure | `--selftest` rc 1, and the refusal names the steps. `--shard 0/5 --list` rc 2. The real `scripts/run_all_suites.sh <out>` rc 2, `ABORTING: scripts/suite_shards.py fails its own self-test` (R626-2's receipt, reproduced). |
| step 1: no own arm, so 1800 s, provisional | `--selftest` rc 1. `ok head provisional figures {'zz_new_suite': 1800} ...`; workers 0-3 at 4628-4730 s, over 4320 s. |
| step 2: one more worker (3 edits in `rtl.yml`, 11 in `ci_events.py`, 2 in the selector) | `--selftest` rc 0 on 3.12.3 and 3.14.7: six workers at 3746, 3746, 3746, 3747, 3747 and 2877 s. `ci_events.py --check` rc 0, `--selftest` rc 0 (1822 items, 2530 arms). The six `--list` outputs cover the 63-suite inventory once each; 5/6 is `milan_dp` alone. |
| serial preflight | rc 0: all eight preflight gates pass. |

The preflight was run by a copy of the driver whose last line, `main "$@"`, is replaced by `main`'s first five calls, ending at `run_preflight_gates`, so no suite ran. Step 3 needs the change's own hosted run.

Validation (head `2c2f3369`, all rc 0, CPython 3.12.3 and 3.14.7):
- `python3 scripts/suite_shards.py --selftest`: `selftest: PASS`, 15 `[ok]`, 0 ESCAPED/FAIL; also under `PYTHONHASHSEED` 0, 1, 2 and 12345.
- `ci_events.py --check` and `--selftest`, `test_suite_cancellation.py`, `check_py_idiom.py` (long function 9 <= 9, module 948 lines), `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `suite_tally.py --selftest`, `check_baremetal_only.py --check`, `check_archive.py`.
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c6bd08c6` (0 findings over 43 added lines), `check_doc_paths.py`.
- `scripts/run_all_suites.sh --shard I/5 --list`, I = 0..4: 15, 16, 14, 16 and 1 suites. Their union is the 62-suite `--list`, with none twice. 4/5 is `milan_dp` alone. `git diff --check c6bd08c6 HEAD`.
- Mutants:
  - The executor's harness (32 cases) gives rc 1 for each of these: reader mirrored to 1800, named arms ignored, figure never compared, no-figure name let through, `aaf` planted provisional at 73 s, a missing driver, a two-name arm, an arm after `*`, `in_checkout()` forced false, and tie-break by `hash`.
  - R626-1's `mutate.py` and R626-2's `probe_727.py` (sha256 as their manifests) build trees without `scripts/run_all_suites.sh`. Unmodified, every case now fails closed with `FAIL head: [Errno 2]`. With one added line copying the driver, each matches its round-2 results except:
    - `head-arms-skipped` and `nondeterministic-tie` / `tie-by-hash` now exit 1;
    - R626-1 `missing-duration-free` reports DRIFT, because it targets the old refusal text. R626-2's equivalent still exits 1 with both arms ESCAPED.

Acceptance criteria:
- 1, 2 and 4: met. A new suite now has a documented cure that the clone shows works.
- 3: pending at this head. For information, at 2026-10-12T15:20Z the round-2 head's run 38262957309 (same split) had:
  - 4/5 success in 3009 s (predicted 2877);
  - 1/5 success in 3066 s (predicted 4205). By `--measure` on job 114858865513, `maap` took 187 s on this branch against the table's 1375 s from #696 (kept by assignment). With 187 s the prediction is 3017 s against a 3070 s log span.
  - 0/5, 2/5 and 3/5 were still running.

Open risks/questions:
- Deleting the head's call to `provisional_problems` is not caught (like deleting any arm). The function is covered by four planted arms. `PROVISIONAL_SUITES` is empty at this head.
- Until #696 merges, worker 1's prediction is about 1190 s high, because `maap` keeps #696's figure.
- Not run: the Verilator suites, the serial sweep past its preflight, `syn/yosys/run.sh` and the `act` replica.

