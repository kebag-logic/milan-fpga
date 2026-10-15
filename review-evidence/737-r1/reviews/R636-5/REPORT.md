[R636] NEGATIVE - exact head e3d25d964b5bbf0187290d0a357c6a6e4c5afd17

Round R636-5, issue #737, PR #739. Merge-only delta review of `08adb21a..e3d25d96`: the merge of dev `f6260253` (merge commit `8db58305`, parents `08adb21a` and `f6260253`) and the re-projection commit `e3d25d96`. Tree `8c2bed598eee7447fe8b93158932407301f92a0a`. The round-4 verdict at `08adb21a` was POSITIVE. Code the delta does not touch keeps that verdict unless the delta changes something it depends on.

The five checks in the round assignment all hold, and I reproduced each one. The verdict is NEGATIVE for a different reason. The merge brought in dev's #671 workload, which makes two documented facts false at this head:

- F1: the docs and elaboration projections in `CI_WORKFLOWS.md`. By the document's own method, the docs workflow now projects above the 30-minute target.
- F2: the hosted-sharding paragraph in `TESTING.md`. Dev's edit, merged in automatically, says GitHub uses six workers with `milan_dp` alone. The generated workflow runs sixteen.

Both findings are MINOR. Each needs either a documentation refresh or a recorded decision by the coordinating role. Neither touches the code, the generator or the sharding.

## Delta reconstruction

- `git merge-tree --write-tree 08adb21a f6260253` reproduces exactly three conflicts: `.github/workflows/rtl.yml`, `docs/testing/CI_WORKFLOWS.md` and `scripts/suite_shards.py`. The automatic-merge tree is `482c911f`.
- Compared with that tree, the merge commit changes five files: the three conflicted files, `.github/ci-templates/rtl.yml` and `scripts/ci_suite_workflows.py`. `e3d25d96` changes only `CI_WORKFLOWS.md`.
- Every other path dev changed carries dev's blob unchanged (`receipts/merge_side_blob_audit.txt`). That includes the #640/#713 RTL (`KL_gptp_shadow.sv`, `KL_gptp_txret.sv`), the `gptp-processor` gitlink `e4869fd0`, the `gptp_tables` suite and the #671 firmware.
- Two files changed on both sides and merged without a conflict: `scripts/ci_events.py` and `sw/builder/test_builder.py`. For each, the change since `08adb21a` is identical, line for line, to dev's own change.
- `scripts/act_ci.py` and `.github/workflows/*.yml` are byte-identical to `08adb21a`. The runner's SHA-256 is `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`, so the pin stays valid.

## Assignment checks (1)-(5)

1. **`scripts/suite_shards.py` admits `gptp_tables` like every unsplit suite.** Holds.
   - The driver sweep at this head gives 63 default suites, including `gptp_tables`, and 80 units after piece expansion.
   - `SUITE_SECONDS["gptp_tables"] = 568` (`scripts/suite_shards.py:101`). `PROVISIONAL_SUITES` is empty (`:141`).
   - Rechecked with `suite_shards.py --measure`:
     - on the hosted log of worker 0/6, job 115981133898 of dev run 38601263345 at `f6260253`, it gives `"gptp_tables": 568` (`receipts/measure_job0_6.txt`). That worker's suites all passed;
     - on PR #713's run 38538854504 at `7fb3664b` (worker 0/6, job 115768681874) it gives 474 (`receipts/measure_pr713_job0_6.txt`).

     So 568 is the larger hosted window, as claimed.
   - The collector (`scripts/ci_suite_collect.py:15-52`) derives its inventory from the driver, with no special case. Planted controls over the real inventory (`receipts/probe_union.txt`):
     - the control is accepted;
     - removing the `gptp_tables` log, moving it to worker 0, or duplicating it there are each refused.
   - `ci_suite_collect_selftest`, `ci_suite_pieces_selftest`, `ci_gate_workflows_selftest`, `ci_workflow_plan_selftest` and `ci_manifest_selftest` all exit 0.
2. **The workflows are generator output only.** Holds.
   - `python3 scripts/ci_gate_workflows.py --check` exits 0, and the generated files are byte-identical to `08adb21a`.
   - Dev's six `rtl.yml` edits are in the template, and the PR's template keeps its old relationship to dev's file. The difference between dev's `rtl.yml` at the merge base and `08adb21a`'s template equals the difference between dev's `rtl.yml` at `f6260253` and the head template (`receipts/template_provenance.diff`, empty).
   - The generator now derives the dedicated arm and the `--expect` count from the template's own `matrix.total` (`scripts/ci_suite_workflows.py:100-104`). It refuses a missing arm at `:109-110` and a mismatched expectation at `:126-127`.
   - Plants on a disposable copy (`probe_generator.sh`, `receipts/probe_generator.txt`):
     - A stale arm index, a deleted arm, a mismatched `--expect`, a total of 7 with nothing else changed, and a duplicated arm are each refused with the generator's `ValueError`.
     - A stray extra `4)` arm beside the correct one is not refused by the generator, but `--check` and `ci_events.py --check` both refuse it (S2).
     - A hand edit to the generated workflow is refused by both checks.
     - A consistent recount to 7 generates bytes identical to the head, which shows the derivation does not depend on the count. `ci_events` refuses that recount, as its six-worker contract should.
     - After restore, both checks exit 0.
   - `ci_events.py --check` reports OK on 2,187 items (`receipts/ci_events_check.txt`). `--selftest` passes 2,187 items and 5,212 arms in 201 s (`receipts/ci_events_selftest.txt`).
3. **`CI_WORKFLOWS.md` keeps both sides' facts.** Holds within that file's Verilator text.
   - Dev's facts are restated at `docs/testing/CI_WORKFLOWS.md:367-377`: the provisional 1800 s figure, the sixth worker's 115 s overhead, the replace-after-hosted-run rule, the six-worker template, the shard 5/6 arm and `--expect 6`.
   - Dev's mutation description ("a matrix of seven and a stale total of six") is merged at `:1369-1370`.
   - The additions are the placement and the counts: 80 units, 63 suites, worker 3 at 1544 s, and the sixteen rows.
   - One wording point is RESIDUE R1. The page's docs and elaboration figures, which this round did not refresh, are F1.
4. **Worker 3 projects 1544 s, and every worker is within its own 60 % bound.** Holds.
   - `suite_shards.py --selftest` (exit 0, `receipts/suite_shards_selftest.txt`) predicts workers 0-14 at 1538-1605 s against 1620 s, and worker 15 at 2032 s against 2160 s. That matches all sixteen rows of `CI_WORKFLOWS.md:2731-2746`.
   - `--ci-pieces --shard 3/16` lists `maap__2`, `milan_dp__0`, `chmap_capture`, `gptp_tables` and `tdm_render` (`receipts/shard_3_16.txt`). Worker 3 has 76 s to its bound and 256 s to 30 minutes.
   - Under the same balance (`receipts/provisional_projection.txt`):
     - with the provisional 1800 s, `gptp_tables` lands on worker 0 at 1922 s, and the selector refuses it, as `CI_WORKFLOWS.md:373-374` says;
     - with 474 s it lands on worker 14 at 1531 s.
   - The specialized owners (`tsn_fuzz` on 1, `chmap_capture` on 3, `milan_dp_mclk__0` alone on 15) hold at any planted duration.
5. **`scripts/act_ci.py` is unchanged.** Holds: byte-identical to `08adb21a`, SHA-256 as above.

## Findings

### F1 - MINOR - Docs, Conformance - `docs/testing/CI_WORKFLOWS.md:2688-2701, 2721-2725, 2752-2760` - docs and elaboration projections are stale after the merge, and by the document's own method the docs workflow now projects above 30 minutes

- **Authority/evidence.** Acceptance 1 of #737 is at most 30 minutes per workflow, and the docs workflow is still triggered on pull requests. AGENTS.md section 7 requires the authoritative documentation to be current.
  - The page derives `docs-gates-1` = 1506 s from "the larger 1386-second local builder measurement" (`:2694`). It then states, in the present tense, "Docs now projects at 1506 seconds ... 1776 seconds, or about 29.6 minutes" (`:2752-2755`).
  - It also states "Elaboration projects at 1313 seconds ... about 26.4 minutes" (`:2756-2758`), from the `7032bca5` builder window of 1441 s.
  - The merge brings dev's #671 builder workload. One example is `sw/builder/test_builder.py`, where the saved-state writer gate's timeout rises from 600 to 1200 s.
  - Hosted dev `f6260253`:
    - Docs run 38601263556: builder 1400 s (was 1065), saved-state writer 410 s (was 119), docs-check job 2682 s (was 2039). Receipt: `receipts/dev_docs_run_38601263556_steps.txt`.
    - Elaborate run 38601263659: elaboration gates 1763 s (was 1441), job 2447 s (was 2144). Receipt: `receipts/dev_elaborate_run_38601263659_steps.txt`.
  - The author's round-5 handoff ([6187136845](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6187136845)) measures the local builder at 1482 s at this head. By the page's method that gives `docs-gates-1` = 1602 s (an 18 s margin) and a workflow of about 31.2 minutes, over the target. With the hosted figure it is about 29.8 minutes. The author also projects elaboration at 1473/1353 s, about 29.1 minutes.
  - The author published this as an open risk and left the decision to the coordinating role. The round's documentation limit kept the rows. The page is still not current.
  - Separately, `:2682` says "It now passes 5,209 arms". The self-test passes 5,212 arms at this head and also at `08adb21a` (`receipts/ci_events_selftest_08adb21a_tail.txt`). That figure was already stale before this delta and belongs to the same refresh.
- **Impact.** The authoritative CI page shows the docs workflow inside 30 minutes with 24 s to spare. At the merge head its own conservative method puts it above 30 minutes. A reader, or the coordinating role, deciding whether acceptance 1 is met would be misled, and the possible need to divide the docs builder is not visible on the page.
- **Required outcome.**
  - Refresh the docs and elaboration rows and the workflow-level projections from merged-head inputs: the hosted `f6260253` windows and the round-5 local re-measurements. State the docs workflow's margin against 30 minutes honestly. Correct the arm count to 5,212.
  - If the docs workflow still projects above 30 minutes, record a coordinating-role decision before merge, either dividing the docs builder or an explicit accepted exception, because acceptance 1 is the issue's objective. A follow-up Issue alone does not resolve this finding.
- **Verification.**
  - Recompute the page's formulas from the cited figures.
  - Run `ci_events.py --check`.
  - Read back the exact-head hosted docs and elaborate wall clocks; this is a manager duty.

### F2 - MINOR - Docs - `docs/testing/TESTING.md:518-524` - the hosted-sharding paragraph says six `--shard INDEX/6` workers with `milan_dp` alone; the generated workflow runs sixteen `--ci-pieces` workers

- **Authority/evidence.**
  - Dev's #713 edit, merged in automatically, reads: "GitHub uses six isolated `--shard INDEX/6` workers ..., the last of them running `milan_dp` alone ... `scripts/run_all_suites.sh --shard 0/6 --list` shows a worker's deterministic selection."
  - At this head the hosted `rtl.yml` has a matrix of 16 workers (`--expect 16` at `.github/workflows/rtl.yml:619`). Its ownership step runs `scripts/run_all_suites.sh --ci-pieces --shard "$SHARD/$SHARDS"` (`:254`).
  - `milan_dp` runs as four legs, and the last worker runs `milan_dp_mclk__0` alone (`scripts/suite_shards.py:46, 878`). `CI_WORKFLOWS.md:345-350` says the same.
  - The paragraph already described five workers at `08adb21a`. The delta rewrote it and it is still wrong, so it falls in this round's scope.
  - Related lines outside the delta, which already held at round 4:
    - `tb/verilator/milan_dp/README.md:447` says "runs alone on hosted shard 4/5 (#444)";
    - `docs/testing/RUNNING_TESTS.md:93` gives `--shard 0/5 --list` as the selection to inspect.
- **Impact.** The test-strategy page tells a reader that a worker selection exists which no hosted job runs, and that `milan_dp` runs undivided on a dedicated worker. Someone reproducing a hosted worker locally would list the wrong suites.
- **Required outcome.** Make `TESTING.md:518-524` describe the hosted sixteen-worker `--ci-pieces` matrix: `milan_dp` in legs, `milan_dp_mclk__0` alone on the last worker, and the template's six-worker matrix as generator input only. Use a local example such as `scripts/run_all_suites.sh --ci-pieces --shard 0/16 --list`. Bring the two related lines into line, or mark them historical.
- **Verification.**
  - A repository-wide search for hosted-shard denominators `/5` and `/6` outside historical evidence finds nothing.
  - Running `--ci-pieces --shard 0/16 --list` matches the page.

### R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:376-377` - "the generator replaces all three with the sixteen workers"

The generator rewrites the matrix and `--expect` to sixteen, but it removes the ownership arm rather than replacing it. The selector's self-test then proves that the last worker runs alone (`.github/workflows/rtl.yml:253-261`). Exact fix: "the generator replaces the matrix and `--expect` with the sixteen workers and removes the arm; the selector's self-test proves that the last worker runs `milan_dp_mclk__0` alone."

### S1 - SUGGESTION - Tests - `scripts/ci_gate_workflows_selftest.py` - the generator's new refusals have no committed test

The two `ValueError` paths at `scripts/ci_suite_workflows.py:110` and `:127` were only exercised by ad-hoc plants: the author's, and mine in `receipts/probe_generator.txt`. The same template defects are also caught by `ci_events.py --check` and its committed mutation arms, such as `_m_ownership_dedicated_arm_dropped` (`scripts/ci_events.py:5384`), so no defect class goes untested. Adding a stale-arm arm and a mismatched-expect arm to the generator self-test would keep the refusals from being removed silently.

### S2 - SUGGESTION - Robustness - `scripts/ci_suite_workflows.py:109-112` - the generator does not refuse other `milan_dp` arms

A stray extra arm beside the correct one passes the generator's count of exactly one and is copied into the generated output. Only `--check` and `ci_events.py --check` refuse it, as `receipts/probe_generator.txt` shows. Refusing any remaining `= milan_dp ;;` arm after removing the dedicated one would make the generator fail closed on its own.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #737 acceptance 1 against `CI_WORKFLOWS.md:2688-2760`; hosted dev runs 38601263556, 38601263659 and 38601263345 at `f6260253`, plus PR #713 run 38538854504; `suite_shards.py:101,141,146`; assignment checks (1)-(5) | R636-5 | `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17` |
| RTL | CLEAN | `receipts/merge_side_blob_audit.txt` (every #640/#713 HDL path and the `gptp-processor` gitlink `e4869fd0` equal dev's blobs; the PR changes no HDL); `scripts/ci_suite_workflows.py:97-128` derivation; `scripts/suite_shards.py:870-888` owners; sixteen-worker balance from `--selftest` | R636-5 | `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17` |
| Robustness | CLEAN (S2 is optional) | `receipts/probe_generator.txt` (8 plants plus control and restore); `receipts/probe_union.txt` (3 plants plus control); refusal of the provisional 1800 s figure (`receipts/provisional_projection.txt`); `receipts/suite_shards_selftest.txt` | R636-5 | `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17` |
| Tests | CLEAN (S1 is optional) | `receipts/ci_events_selftest.txt` (2,187 items, 5,212 arms); `receipts/ci_events_check.txt`; `receipts/suite_shards_selftest.txt`; the five scheduling/union self-test receipts at exit 0; generator `--check` at exit 0; the merged `ci_events.py` and `test_builder.py` deltas equal dev's | R636-5 | `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17` |
| Docs | UNCLEAN (F1, F2; R1 is residue) | `docs/testing/CI_WORKFLOWS.md:345-377, 1346-1370, 2660-2760`; `docs/testing/TESTING.md:510-524`; `tb/verilator/milan_dp/README.md:447`; `docs/testing/RUNNING_TESTS.md:93` | R636-5 | `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17` |

## Real limits

- I ran no docs-check, rtl-fast, builder, Verilator suite, Yosys or act bank. Source-head execution evidence is the author's published receipts. My execution is limited to:
  - the generator `--check`;
  - `ci_events.py --check` and `--selftest`;
  - `suite_shards.py --selftest` and `--measure`;
  - the five scheduling/union self-tests;
  - disposable plants.

  These ran on host Python 3.14.7 with PyYAML 6.0.3, not in the shipping image. The generator's bytes matched there too.
- I did not re-measure the 1482 s local builder figure or the elaboration re-measure. F1 holds on the verified hosted figures alone, because those already move every docs and elaboration row.
- Hosted variance: on dev run 38601263345, worker 2/6 timed out `milan_dp_gm_steps` (over 1800 s; table 926 s) and `milan_dp_mclk` (over 3600 s). PR #713's run at `7fb3664b` passed both, in 969 s and 2011 s (`receipts/measure_pr713_w2.txt`), so this looks like runner variance rather than the merged code. The regular workers' margins of 15-82 s give little room for such a runner.
- No manager source bank runs at this head. Physical calibration was NOT RUN, and field skips are not hardware proof.
- After the probes, the clone is restored to the exact head: the worktree and index equal HEAD, all six gitlinks are as committed, and nothing is untracked or ignored (`receipts/restore_verification.txt`).

## Pending manager duties

- Decide F1 (refresh the figures, divide the docs builder, or record an exception), and carry R1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `fa7347fc`, live dev `f6260253`) with the builder and native banks.
- Read back the exact-head hosted wall clocks, distinguishing executed jobs from skipped contexts, and handle act acceptance.

### R2 - RESIDUE - Docs - PR #739 body, Status paragraph, "This head is not pushed; the coordinating role publishes it."

The live PR head is `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`, so the head is published. This is the same class as R636-4-R1 and R637-4-R1, now on the round-5 paragraph. It is wording only. Exact fix: "The coordinating role published this head." Verification: read the live PR body against the PR head.

## Prior findings

I read these only after writing my own verdict and ledger above. The round-4 reviews are R637-4 ([6183672250](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6183672250)) and R636-4 ([6184124102](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6184124102)), both POSITIVE at `08adb21a`. Neither left an open BLOCKER, MAJOR or MINOR. Their reconciliations already closed the round-1 to round-3 findings.

| Prior item | Status at `e3d25d96` | Evidence |
|---|---|---|
| R636-4-R1 / R637-4-R1 (RESIDUE, PR body publication tense) | **Retained as R2** | The round-5 Status paragraph restates "This head is not pushed" for a published head |
| R636-4-S1 (SUGGESTION, union log points to a NOT RUN list "above" that is not there) | **Retained** | `scripts/ci_builder_legs.py` is untouched by the delta |
| R636-4-S2 (SUGGESTION, builder-inventory reader missing from `check_inventory_dependencies`) | **Retained** | The delta changes only `generate()` in `scripts/ci_suite_workflows.py`; `:21-35` is unchanged |
| R636-4-S3 (SUGGESTION, no self-test for the driver's `--gates` refusals) | **Retained** | The only change to `sw/builder/test_builder.py` is dev's writer-gate timeout, 600 to 1200 s |
| R636-3-F1, R636-3-R1, R636-3-R2 and earlier | Resolved at round 4, and not reopened | The delta touches none of the artifacts that resolved them. `ci_runtime_evidence.py`, `ci_suite_collect.py`, `ci_suite_pieces.py`, `ci_builder_legs.py` and `act_ci.py` are byte-identical to `08adb21a`. The only change to `ci_suite_workflows.py` is inside `generate()`, at `:100-128` |

The round-4 Docs ledger rows cite `CI_WORKFLOWS.md:2684-2694` as recomputed at `08adb21a`. That recomputation was correct for its inputs. F1 records that the merged workload has since moved those inputs.

R636-5 FINISHED
