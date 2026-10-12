[R620] POSITIVE - exact head 941e15593ef3dbf561bd8ed75aaf680f5d146a41

# R620-2: internal independent review of PR #724 (issue #716), round 2

- Head reviewed: `941e15593ef3dbf561bd8ed75aaf680f5d146a41`, tree `b089eed642dad5dc2af4a69c054b830609ab77cf`. This is a merge of dev `09c7231eca343607c97c0d66abebb2553688712c` (F-INT, PR #704) into `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`. Round 1 (R620-1 and R621-1) was POSITIVE at `f41e4f2d`.
- Role: internal reviewer, working in a cleared context from an isolated detached clone. This round is a delta review of the merge, with all five lenses applied.
- Verdict: no BLOCKER, MAJOR or MINOR finding. Four RESIDUE items are open, all wording only: three carried from R620-1 and one new. One SUGGESTION is carried from R620-1. All five lenses are clean at this head.

## Reconstruction (public state only)

1. AGENTS.md, CONTRIBUTING.md, docs/README.md.
2. Issue #716: the body (acceptance items 1-3), assignment 6107547907, the round-2 assignment 6113977586, TAKEN 6107555801, and REVIEW READY 6108397728 and 6114557372.
3. Authorities: `docs/testing/CI_WORKFLOWS.md`, `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`, and the firmware driver `sw/firmware/ctrl/test/test_ctrl_firmware.py` with its shard self-test.
4. `git diff 09c7231e..941e1559` (5 files, +544/-48), `git show --cc 941e1559`, and diffs against both parents and against base `ac2c5e77`.
5. Evidence: the author's round-2 receipts at `879bafcc:review-evidence/716-r1/author-r2/` (ROUND2-GATE-RESULTS.json, ROUND2-PRESERVATION.json, ROUND2-COVERAGE-COMPARISON.csv, ROUND2-DEV-COVERAGE-RESULT.json); the manager's ten-run table, comment 6117443205; and the Actions API for run 38180290290.
6. Prior public findings (R620-1 6113853338, R621-1 6113677958), read only after my independent pass and after `receipts/verdict_draft_before_prior_findings.md` was written. I did not read any other round-2 review.

No manager source bank runs at this head, and this report neither claims nor infers one. The source-head execution evidence here is the author's published receipts plus my own focused reruns listed below.

## Delta checks requested by the round-2 assignment

| Check | Result | Evidence |
|---|---|---|
| The four conflicts resolve so that both sides hold | Met | `rtl-fast.yml`: the head differs from dev only by the four-job split. Against `f41e4f2d` it differs only by dev's `publication-census` job and its aggregate entry. The `publication-census` job is byte-identical to dev's (`receipts/independent_census.json`, `publication_census_job_identical_to_dev: true`). `ci_events.py`: the head-vs-dev change equals the branch's own change against base `ac2c5e77` line for line, and all of dev's census pins remain. `CI_WORKFLOWS.md` and the driver: the only resolution lines are the expected ones: comparator and ROUND5 ownership, `publication-census` kept in the skip and aggregate sentences, `arm_srpcmp()` in `run_suites`, and `*srp_pub_mutants.ROUND5` in the interface-1 filter. |
| Every F-INT firmware step, suite and check runs in one of the four jobs | Met | The comparator arm `arm_srpcmp` runs in shard 0 (`firmware-unit`). All five ROUND5 publication mutants run at both interface counts in shard 3 (`firmware-srp-mutants`). Evidence: `receipts/dev_vs_head_dispatch.json`, and locally `receipts/shard0.log:252-254` and `receipts/shard3.log` (17 publication-mutant lines). Hosted, attempt 10: `receipts/hosted/attempt10_log_excerpts.txt` shows `[ok] arm srpcmp` in `firmware-unit`, and each ROUND5 name twice in `firmware-srp-mutants`. |
| `publication-census` stays required | Met | It is in the aggregate's `needs`, its env and its result loop (`receipts/independent_census.json`). Removing it from `needs` fails `--check` (`receipts/layout_pin_probes.json`, `aggregate-needs-drops-publication-census`). |
| The command census proves every merged command runs with its gating | Met | `ci_events.py --firmware-census` rc 0, `preserved: true`. My independent YAML census reads dev's `firmware-unit` from git objects: 19 script lines plus 2 `uses` rows before, 55 plus 8 after. Removing only the terminal `--shard N/4` leaves no missing and no added (command, job `if`, step `if`) tuple. Each job runs exactly one of `0/4`..`3/4`, every timeout is 45, every job needs `changes` with the same `if`, and the only cache is the SDK (`receipts/independent_census.json`, rc 0). |
| 916 invocations, same order | Met | The shard self-test reports `916 live invocations in exactly one shard; shard sizes [60, 507, 77, 272]` (`receipts/shards_selftest.log`). Independently, I drove dev `09c7231e`'s own `main()` with recorders: dev default == head default == shards 0..3 concatenated, in order, with all identities unique. That is 914 recorded entries; the in-tree count of 916 adds its two campaign-control markers, which gives the same 60/507/77/272 split (`receipts/dev_vs_head_dispatch.json`). |
| Each discovered suite lands in exactly one shard, and a new suite is picked up automatically | Met | `receipts/driver_probes.json` (7 probes, all as expected). Each of these fails the in-tree check: planted comparator duplication, the SRP phase dropped from the shards, and the control phase duplicated into the AECP shard. A distinct new suite added to `run_suites` passes the in-tree check, so it is auto-assigned. |
| Coverage stays unsplit, with its ratchet | Met | `coverage()` is AST-equal to dev's. The `--coverage` early return is unchanged. No file under `sw/firmware/gtest` or `sw/firmware/ctrl_nvm` changed (`receipts/coverage_identity.log`). `--shard` together with `--coverage` refuses (in-tree refusal cases). `fw_coverage.py --selftest` gives 28/28, and `--check --jobs 4` passes on 30 files (`receipts/fw_coverage_*.log`). The author's 30-file comparison of dev driver against head (ROUND2-COVERAGE-COMPARISON.csv) shows `covered_locations_equal=True` on every row. |
| `ci_events.py --check` and `--selftest` | Met | `--check`: OK, 2016 items. `--selftest`: PASS, 2016 items and 2828 arms (`receipts/ci_events_check.log`, `receipts/ci_events_selftest.log`). |
| The layout is pinned | Met | Each of 14 planted workflow and policy defects fails the head's `--check`, and the unedited control passes (`receipts/layout_pin_probes.json`). The defects were: the SRP job deleted; dropped from `needs` or from the result loop; running shard 2; firmware-unit unsharded; `if: false`; `needs` dropped; timeout 60; a build-output cache added; SDK verification dropped; `--require-rv32` dropped; the lwSRP fetch dropped; the policy budget row changed; `publication-census` dropped from `needs`. |
| Budgets recorded | Met | `docs/testing/CI_WORKFLOWS.md:80-85` has one row per job: 45 min, 1890 s, 1620 s. `--check` pins each row. |
| Item 2 at this head | Met | `receipts/hosted/summary.md`, read-only API. Run 38180290290 attempts 1-10 are all `pull_request`, on branch `716-fw-unit-split`, at head `941e15593ef3`, and every run concluded success. Every firmware job, `publication-census` and `rtl-fast` succeeded in every attempt, and no firmware step was skipped. All 40 firmware durations equal comment 6117443205. The slowest is 916 s (`firmware-control-mutants`, attempts 9 and 10), 33.9 % of 2700 s against the 1890 s bound. The other jobs peak at 705 s, 715 s and 256 s. |

Local focused reruns at the head, using CPython 3.12.3 and the pinned SDK installed fresh into scratch. All returned rc 0:

- The four shards: shard 0 PASS; shard 1 `mutants: 506 of 506 caught`; shards 2 and 3 PASS.
- `test_ctrl_nvm.py --require-rv32 --jobs 4`: 5 shapes, 435 tests.
- `fw_rv32_selftest.py --require-rv32`, `tally_selftest.py`, `ci_rv32_sdk_selftest.py`, `ci_scope.py --selftest`.
- `docs_check`, `check_doc_style` (and `--selftest`), `gen_toc --check` (and `--selftest`), `check_py_idiom` (and `--selftest`), `check_em_dash --selftest`, `check_em_dash --base 09c7231e`, `git diff --check 09c7231e HEAD`.

The shards ran concurrently with each other, so their wall times (293/956/210/709 s) are not a timing calibration.

## Findings

### R620-2-RES1 (retains R620-1-RES1 at this head): stale CI prose in files this PR touches

- Severity: RESIDUE.
- Lenses: Docs.
- Locations, all still present at this head, with exact fixes:
  - `.github/workflows/rtl-fast.yml:312-313`: "plus the control mutation campaign". Fix: "while the three mutation jobs below run the campaigns (#716)".
  - `docs/testing/CI_WORKFLOWS.md:2354-2356`: "run locally as `firmware-unit` runs them … the required RV32 control build and its `--self-test` mutation campaign". Fix: "as the four firmware jobs run them together".
  - `docs/testing/CI_WORKFLOWS.md:91`: "Issue #716 records measurements and the hosted acceptance table." Fix: "Issue #716 records measurements; PR #724 records the hosted acceptance table (comment 6117443205 at `941e1559`)."
  - `docs/testing/CI_WORKFLOWS.md:88`: "below 60%". Fix: "at most 60%".
- Impact: wording only. No measurement, check, test, generated artifact or verdict changes.
- Required outcome: the manager carries it to the residue checklist (#495, per assignment 6113977586), or the wording is fixed.
- Verification: re-read the lines, then rerun `ci_events.py --check`, `docs_check.py` and `check_doc_style.py`.

### R620-2-RES2 (retains R620-1-RES2 at this head): stale single-job CI descriptions outside the lane's permitted files

- Severity: RESIDUE.
- Lenses: Docs.
- Locations and fixes:
  - `sw/firmware/gtest/README.md:398-411` says that `firmware-unit` runs "the ctrl gate", that `ci_events.py` "pins the job's steps", and that "The control gate includes lwSRP, SRP and its mutation campaign". Fix: name the four firmware jobs. Say that `firmware-unit` runs the tally cases, the normal ctrl suites (`--shard 0/4`), the saved-state gate and coverage, while `firmware-control-mutants`, `firmware-aecp-mutants` and `firmware-srp-mutants` run the campaigns. Say that `ci_events.py` pins all four jobs.
  - `sw/firmware/ctrl/README.md:349` says "The CI firmware step also requires the control mutation campaign." Fix: "The `firmware-control-mutants` job runs the control mutation campaign (#716)."
- Neither file is in the assignment's permitted set, so the lane could not edit them without a STOP.
- Impact: wording only.
- Required outcome: the manager carries it to the residue checklist (#495), or authorizes a follow-up.
- Verification: re-read the lines, then rerun `docs_check.py`.

### R620-2-RES3 (new): the PR body's status lines predate the new-head hosted table

- Severity: RESIDUE.
- Lenses: Docs.
- Location: the PR #724 body.
  - The "Status" section says "the merge head remains unpushed" and "Item 2 passed at f41e4f2d; the manager rechecks hosted runs at this new head."
  - "Known limitations" says "The manager must collect new-head hosted acceptance and obtain re-review."
  - The body's own "Linked Issue" section already cites the new-head result.
- Exact fixes:
  - Status: "`716-fw-unit-split` -> `dev`; head `941e1559` is published. Item 2 passed at `941e1559` (manager comment 6117443205: slowest 916 s, 33.9 %); the f41e4f2d table below is superseded."
  - Known limitations: "Re-review at the new head is pending."
- Impact: wording only. The figures cited elsewhere in the body are correct.
- Required outcome: the body is edited, or the item is carried on the residue checklist.
- Verification: re-read the PR body.

### R620-2-S1 (retains R620-1-S1): the shard inventory observes invocations, not verdict participation

- Severity: SUGGESTION.
- Lenses: Tests.
- Location: `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:47-99`. The code is unchanged since round 1.
- At this head the behaviour is correct. `receipts/verdict_propagation.json` (rc 0) shows that one failing stand-in turns only its owning shard red, and the default red too. That holds for:
  - the comparator arm `arm_srpcmp` (shard 0);
  - a ROUND5 entry present in the interface-1 table (shard 3);
  - control, AECP, SRP at both interface counts, the pin controls, and representative suite arms.
- Optional change: as in round 1, make a stand-in fail per phase inside the in-tree check, and replace `assert` with explicit raises.
- Verification: a planted discard of one shard's result fails the in-tree check.

### Disposition of prior public findings

| Prior item | Status at 941e1559 |
|---|---|
| R620-1-RES1 (RESIDUE, Docs) | Retained as R620-2-RES1. All four locations are still present (line numbers updated); the merge did not touch them. |
| R620-1-RES2 (RESIDUE, Docs) | Retained as R620-2-RES2. The ctrl README line is now 349. |
| R620-1-S1 (SUGGESTION, Tests) | Retained as R620-2-S1. Re-verified at this head with the merged comparator and the ROUND5 entries. |
| R621-1 | Recorded no finding of any severity, so there is nothing to resolve. |

## Lens results (artifact examined at the exact head)

- `[R620] PASS Conformance — issue #716 items 1-3, assignments 6107547907/6113977586; receipts/hosted/summary.md (run 38180290290 attempts 1-10), receipts/independent_census.json, receipts/ci_events_census.log, receipts/dev_vs_head_dispatch.json, docs/testing/CI_WORKFLOWS.md:65-101 — item 2 recomputed from the API (916 s = 33.9 % ≤ 70 %), every timeout 45 min, no check, arm or ratchet removed, the merged suite set preserved in order, budgets recorded and pinned.`
- `[R620] PASS RTL — git diff --stat 09c7231e..941e1559 (5 files: rtl-fast.yml, CI_WORKFLOWS.md, ci_events.py, test_ctrl_firmware.py, test_ctrl_firmware_shards.py; no HDL, constraint or testbench file); receipts/restore_check.txt (gitlinks unchanged) — no RTL is in scope. On the CI architecture: the job graph (needs: changes, the same if, aggregate needs and loop) is consistent with dev's publication-census topology, there are no build-output caches, and the SDK cache key is unchanged.`
- `[R620] PASS Robustness — test_ctrl_firmware.py:132-207,261-274; receipts/layout_pin_probes.json, receipts/driver_probes.json, receipts/verdict_propagation.json, in-tree refusal cases in receipts/shards_selftest.log — invalid or narrowing shard arguments refuse with rc 2; a failed normal phase still stops mutations in the default; each phase's failure turns its own shard red; 14 planted layout defects and 3 planted dispatch defects are caught; Refusal handling of the pin arms is unchanged (outer try returns 2).`
- `[R620] PASS Tests — receipts/shard{0,1,2,3}.log, ctrl_nvm.log, fw_coverage_selftest.log, fw_coverage_check.log, fw_rv32_selftest.log, tally_selftest.log, ci_events_selftest.log, shards_selftest.log, coverage_identity.log — all rc 0 at head: 506/506 control mutants, AECP/SRP/pin controls, the comparator's 5 controls and 18 plants, 435 saved-state tests, 30-file ratchet, 28/28 coverage plants, 2828 CI-contract arms. The in-tree checks were shown able to fail (driver and layout probes). S1 is optional.`
- `[R620] PASS Docs — docs/testing/CI_WORKFLOWS.md:44-101,2354-2381, sw/firmware/gtest/README.md:396-413, sw/firmware/ctrl/README.md:349, rtl-fast.yml:305-316, PR #724 body; receipts/docs_check.log, doc_style*.log, gen_toc*.log, em_dash*.log, diff_check.log — the authoritative policy page states the four-job layout, comparator and ROUND5 ownership, the publication-census requirement and per-job budgets. The remaining staleness is wording only (RES1-RES3), which does not leave the lens unclean under the 2026-10-02 owner rule.`

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #716 acceptance and assignments, `rtl-fast.yml`, `CI_WORKFLOWS.md:65-101`, the Actions API for run 38180290290, the independent census, the dev-vs-head dispatch | R620-2 | 941e15593ef3dbf561bd8ed75aaf680f5d146a41 |
| RTL | CLEAN | Diff file list (no HDL), job graph and caches in `rtl-fast.yml`, gitlinks | R620-2 | 941e15593ef3dbf561bd8ed75aaf680f5d146a41 |
| Robustness | CLEAN | `test_ctrl_firmware.py` shard and refusal paths, layout, driver and verdict probes | R620-2 | 941e15593ef3dbf561bd8ed75aaf680f5d146a41 |
| Tests | CLEAN | The four shard runs, saved-state, coverage (both modes), RV32, tally, CI-contract self-test, shard self-test | R620-2 | 941e15593ef3dbf561bd8ed75aaf680f5d146a41 |
| Docs | CLEAN (RESIDUE RES1-RES3 carried) | `CI_WORKFLOWS.md`, the gtest and ctrl READMEs, workflow comments, the PR body, docs gates | R620-2 | 941e15593ef3dbf561bd8ed75aaf680f5d146a41 |

## Real limits

- I did not run a manager source bank, the full parent, PP, gPTP or Yosys banks, the builder bank, act or Docker, or any hardware. Physical calibration was NOT RUN. Field skips are not hardware proof.
- My local shard runs ran concurrently, on the host's GCC 16.2.1 and GoogleTest 1.18.0 (hosted uses 13.3.0 and 1.14.0). They are pass/fail evidence, not timing predictions. Item 2 is judged only from the hosted API data.
- I did not use the pinned Verilator: this delta has no simulation surface.
- I fetched the hosted logs only for attempt 10. Attempts 1-9 are verified by job and step conclusions and durations, not log content.
- The in-tree shard check proves that the head's own default is partitioned. It does not compare against an earlier baseline: removing a suite from `run_suites` everywhere passes it (`driver_probes.json`, `srpcmp-removed-everywhere`). Preservation of dev's population at this head rests on my independent dev-vs-head comparison and the author's ROUND2-PRESERVATION.json, and that is by design of the assignment.
- The coverage file-by-file equality at this head is the author's published comparison. I independently verified that the coverage path is code-identical to dev's and that the ratchet passes. I did not recompute the per-file location hashes.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `09c7231e`, live dev `c20c85bd`) with the builder and native banks, and link the receipts on the PR.
- Hosted and act acceptance at the final candidate.
- Carry RES1 and RES2 to #495 at merge (per assignment 6113977586), and RES3 to the residue checklist or a PR-body edit.
- Merge authorization, post-merge containment, and closing #716 (the PR body says `Closes #716`).

## Receipts

`MANIFEST.sha256` lists every published receipt and script. The scripts are `scripts/independent_census.py`, `dev_vs_head_dispatch.py`, `layout_pin_probes.py`, `driver_probes.py`, `verdict_propagation.py`, `coverage_identity.py`, `hosted_attempts.py`, `run_logged.sh` and `light_chain.sh`. Raw outputs are under `receipts/`. The clone was verified at exact head after all probes: HEAD, tree, index tree and gitlinks match, with porcelain status empty (`receipts/restore_check.txt`).

R620-2 FINISHED
