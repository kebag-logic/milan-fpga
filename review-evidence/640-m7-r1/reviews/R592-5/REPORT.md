[R592] NEGATIVE - exact head 4c5d70b50230fbd5da347852d39daf7f23b3df0b

# R592-5: internal review of PR #713 (issue #640, Mark II lane M7), round 5

- Exact head `4c5d70b50230fbd5da347852d39daf7f23b3df0b`, tree `8156e281ac181efc76139470e3cf5c530ae17793`.
- Donor `gptp-processor` gitlink `e4869fd0c42889b2ac806587cc5c78afb1c33461`, unchanged since `412e3f6c`.
- Scope: the round-5 delta `412e3f6c..4c5d70b5` (`fb4d30b1a`, `90f75192f`, `4c5d70b50`).
- Authorities judged against:
  - the round-5 ruling ([issue #640 comment 6163132636](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6163132636));
  - the selector docstring's new-suite steps (`scripts/suite_shards.py:53-86`);
  - `docs/testing/TESTING.md:514-517`.
- Earlier rounds stand for artifacts this delta does not touch.

## Summary

- **Both blocking findings from round 4 are resolved at this head.** R592-4-F1 (BLOCKER) and R593-4-F1 (MAJOR) both concerned the missing `gptp_tables` registration.
  - `gptp_tables` is recorded at 1800 s, the figure from `suite_timeout`'s `*` arm, and is marked provisional.
  - A sixth worker was added exactly as step 2 of the docstring prescribes.
  - All gates return 0, and `gptp_tables` is assigned to exactly one worker.
  - The hosted `rtl-full` run at this tree passed all six Verilator workers and `verilator-suites`. On worker 0/6, `gptp_tables` reported 36 checks with 0 failures and 26/26 controls.
- **R593-4-F2 (MINOR) is resolved.** The reach figures now say TX 25 and results 2.
- **One new MINOR is open, R592-5-F1 (Docs).**
  - `docs/testing/CI_WORKFLOWS.md:1322` still gives the Verilator verifier's current value as `--expect 5`.
  - The workflow and the canonical contract now pass `--expect 6`.
  - This round updated every other current six-worker statement on that page but missed this one.
  - It is a stale contract figure, not wording only, so it is MINOR under the owner rule. Docs stays unclean, and the verdict is NEGATIVE.
- R593-4-D1 (RESIDUE, PR body publication wording) is still present in a new form. It is carried below with an exact fix.
- Selector step 3 (replace the provisional figure and the new worker's overhead from this change's own hosted run) can now be done. It is a pending executor and manager duty, not a defect at this head.

## Independent executions at this head

All commands ran in the foreground. Receipts are under `receipts/` and portable drivers under `scripts/`.

| What | Result | Receipt |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | rc 0, `selftest: PASS`. Predicted worker seconds 3746/3746/3746/3747/3747/2877 against a 4320 s bound. `head provisional figures {'gptp_tables': 1800}` match `suite_timeout` | `receipts/head-gates/suite_shards_selftest.*` |
| `python3 scripts/ci_events.py --check` | rc 0, 2175 contract items | `receipts/head-gates/ci_events_check.*` |
| `python3 scripts/ci_events.py --selftest` | rc 0, `PASS (2175 contract items, 3096 arms)` | `receipts/head-gates/ci_events_selftest.*` |
| `python3 scripts/ci_scope.py --selftest` | rc 0 | `receipts/head-gates/ci_scope_selftest.*` |
| `scripts/run_all_suites.sh --shard I/6 --list` for I = 0..5, plus the serial `--list` | All rc 0. The six lists are disjoint, and their union is the 63-suite serial list. `gptp_tables` is only on 0/6. `tsn_fuzz` is on 1/6, `chmap_capture` on 3/6, and `milan_dp` runs alone on 5/6 | `receipts/head-gates/list_*` |
| The eight serial-sweep preflight gates (`run_all_suites.sh:275-385`) on a clean head checkout | All eight rc 0 | `receipts/preflight/` |
| `tb/verilator/gptp_tables` `run` target with the pinned compiler (`verilator --version` prints `Verilator 5.050 2026-07-01 rev v5.050`) | `checks: 36 failures: 0`. Reach: `tx_fifo: ... 25 beats deep` and `results: ... 2 deep, 111 written behind a waiting result`. The one-valued README table is current. The `mutants` target refused because the copy was not a git checkout, so the control evidence comes from the hosted run below | `receipts/gptp_tables_run.log` (rc file records 2 for the mutants refusal) |
| Clone identity after the probes | HEAD, tree and index match. All tracked blobs rehash with 0 mismatches. All five initialized gitlinks match clean checkouts; `external` is uninitialized and its gitlink was verified | `receipts/identity.log` |

### Negative controls and mutation probes

Each probe ran in its own disposable worktree under `scratch/`. The edit, diff and log for each are in `receipts/probes/`.

| Probe | Expect | rc | Refusal or observation |
|---|---|---|---|
| N1: `suite_shards --selftest` at base `412e3f6c` | fail | 1 | `gptp_tables: inventory suite with no recorded duration` |
| N2: base plus step 1 only (1800 s, provisional, five workers) | fail | 1 | Workers 0-3 predicted at 4628-4630 s, above 4320 s, so step 2 was required |
| M1: drop the `gptp_tables` duration | fail | 1 | Missing duration, and a provisional name with no figure |
| M2: set the figure to 1799 s | fail | 1 | `provisional figure 1799 s is not the 1800 s that ... suite_timeout gives it` |
| M3: overhead table back to five entries | fail | 1 | `WORKER_OVERHEAD_SECONDS describes 5 workers; rtl.yml runs 6` |
| M4: `rtl.yml` matrix and total back to five | fail | 1 | Verifier must pass `--expect 5`; canonical form differs |
| M5: ownership arm `5)` changed to `4)` | fail | 1 | Ownership step is not the canonical form |
| M7: verifier set to `--expect 5` | fail | 1 | Must pass `--expect 6` |
| M6: stale-denominator fixture reverted to its pre-round values | fail | 1 | `AssertionError: fixture drift`, so the advance is forced by the worker count |
| M8: head fixture without `shard.append(6)` | info | 0 | Still caught through the literal restatement. The same removal at base (M8b, `append(5)`) also gives rc 0, so this redundancy predates this round |
| M9: `gptp_tables` removed from `PROVISIONAL_SUITES` | info | 0 | Not refused: the 1800 s figure is then simply unmarked. Pre-existing behaviour; the head marks it correctly |
| P0: head control | pass | 0 | - |

### Hosted evidence at this exact tree (read, not owned)

**What the hosted run validated.**
- The PR's `rtl-full` run `38529993870` validated GitHub's merge commit `85b959cb02bfa5b53978bbd1a479256963bbb388`.
- Its parents are dev `fa8209889411…` and this head.
- Its tree is `8156e281…`, byte-identical to the head tree, so the executed jobs validated exactly the head's bytes.

**Worker 0/6 (job 115739516717).**
- The ownership step's self-test passed with the same predictions as the local run.
- The worker owns 8 suites, including `gptp_tables`.
- `PASS gptp_tables` was logged between 08:01:39.416 and 08:11:11.387 UTC, a window of about 572 s.
- Its artifact carries `TARGET_SHA` `85b959cb…`, `== gptp_tables: checks: 36 failures: 0 ==`, TX 25, results 2, and `controls: 26 failures: 0`.

**Worker 5/6 (job 115739516595).** It ran `milan_dp` alone and passed with 11956 checks.

**`verilator-suites` (job 115763240226).** Succeeded:
- `target-sha: OK, 6 record(s) all 85b959cb…`;
- tally `checks: 2187219 in-suite failures: 0`;
- `every worker succeeded`.

**Other contexts.**
- `yosys-portability`, `rtl-fast`, `elaborate`, `docs-check` and all other contexts succeeded.
- `Physical gPTP (nightly and manual)` is skipped by design on pull requests. It is not evidence.

Receipts: `receipts/hosted/*` and `receipts/hosted-check-runs.tsv`.

## Findings

### R592-5-F1: MINOR (Docs). The CI policy page still gives the Verilator verifier's value as `--expect 5`

- **Location:** `docs/testing/CI_WORKFLOWS.md:1322`, which reads "passing `--expect` the worker matrix size (`--expect 5` for Verilator, `--expect 4` for Yosys)".
- **Authority and evidence:**
  - At this head, `.github/workflows/rtl.yml:426` passes `--expect 6`, and so does the canonical step at `scripts/ci_events.py:2237`.
  - The line describes the current contract, not history. #444's `06055a04c` introduced it and set it to 5 when the fifth worker arrived.
  - This round's `fb4d30b1a` updated the other current statements on the same page (`:347-348`, `:373`, `:519`, `:1923-1924`, `:2237`, `:2684-2685`) but not this one.
  - AGENTS.md section 5 ("update authoritative documentation when behavior ... changes") and the Docs lens ("Changed contracts are reflected in authoritative docs") apply.
  - The executor's REVIEW READY says the scheduling documentation agrees. Neither `docs-check` nor `ci_events --check` reads this figure, so no gate catches it.
- **Why it is not RESIDUE:** the sentence states a numeric value of the CI contract, and the fix changes that figure.
- **Impact:** a reader of the authoritative CI policy page is told the aggregate requires five shard records when it requires six. This matters exactly when #737 rebalances the shards.
- **Required outcome:** the sentence gives the current value, `--expect 6` for Verilator, or states it in words ("the worker matrix size, six for Verilator and four for Yosys").
- **Verification:** `grep -n -- '--expect' docs/testing/CI_WORKFLOWS.md` agrees with `rtl.yml`. A docs-only head change only needs Docs re-covered.

### R592-5-S1: SUGGESTION (Docs). The stale-denominator example still uses five-worker numbers

- **Location:** `docs/testing/CI_WORKFLOWS.md:1336-1338` ("With a matrix of five and a stale total of four ... shard 4/5's suites").
- **Note:** the sentence is still a valid hypothetical. Optionally, restate it as "a matrix of seven and a stale total of six" to match `_m_shard_denominator_stale` at `scripts/ci_events.py:5256-5263`.

### R593-4-D1: RESIDUE (Docs), retained in a new form. The PR #713 body still calls the head local and unpublished

- **Location:** three parts of the PR #713 body:
  - Status: "`4c5d70b5…` (local continuation of published `412e3f6c`)" and "no push in this round".
  - How to get into the same state: "Use the existing local lane for the unpublished parent continuation. After publication, ...".
  - Known limitations: "No source publication, PR edit, ... occurred".
- **Evidence:** the PR's `headRefOid` is `4c5d70b5…`, and hosted runs executed on it.
- **Impact:** stale publication wording only. It changes no measurement, test or verdict.
- **Exact fix:**
  - Status: "Parent: `4c5d70b5…` (published PR head)" and "no push by the executor in this round; the manager published it".
  - Reproduction: "Check out the published parent revision above and initialize its pinned submodules."
  - Known limitations: qualify the no-publication sentence as the executor's implementation-stage history.
- **Status:** the manager carries this to the residue checklist.

## Prior public review findings at this head (read after this round's own pass)

My own findings were recorded in `receipts/independent-pass-findings.txt` before I read R592-4 or R593-4.

| Finding | Status at `4c5d70b5` | Evidence |
|---|---|---|
| R592-4-F1 BLOCKER (Tests, Conformance): `gptp_tables` missing from the selector | **Resolved** | Every verification item holds: the three commands and the preflight return rc 0, `gptp_tables` is on exactly one worker, and the hosted workers report `gptp_tables` with 36 checks. Probes N1 and N2 reproduce the original refusal and the five-worker overload |
| R593-4-F1 MAJOR (Conformance, Tests): same cause | **Resolved** | As above. No suite was dropped or renamed: 63 suites both ways, and the shard union equals the serial list. No timeout or headroom changed (`timeout-minutes: 120`, `HEADROOM_PERCENT = 60`) |
| R593-4-F2 MINOR (Docs): reach figures 27 and 3 | **Resolved** | `README.md:29,31` and `sim_main.cpp:15,19` now say 25 and 2, matching both the local run and the hosted artifact. No generator writes that table: `gen_one_valued_table.py` writes only the one-valued table, which it reports current. No other "27 of 256" remains in the tree |
| R593-4-D1 RESIDUE (Docs): PR body local-only wording | **Retained**, new form | See above |
| R592-4-S1 SUGGESTION: inert ROM-ledger row | Retained (optional; the executor declined it) | `syn/yosys/rom_digests.tsv` unchanged since `412e3f6c` |
| R592-3-RES1, R592-3-RES2, R593-3-R-01 RESIDUEs | Retained, carried | Their files (`tb/verilator/gptp_tables/README.md:9-10`, `gptp_tables_wrap.sv`, `docs/design/MARK_II_AREA_PLAN.md`, `tb/verilator/gptp_tables/Makefile`) are unchanged in this delta, so the exact fixes published in R592-3 and R593-3 stand |
| R593-3-S-01, R592-2-S1, R593-1-S-03 SUGGESTIONs | Retained, optional | Their artifacts are unchanged in this delta |

## Lens results

```text
[R592] PASS Conformance - scripts/suite_shards.py:161,201,207,846; .github/workflows/rtl.yml:161-162,227,426; scripts/ci_events.py:1974,2237; receipts/head-gates, receipts/probes N1/N2, hosted run 38529993870 - ruling 6163132636 items 1-4 against docstring steps 1-2 (step 3 pending by its own terms), 63-suite partition, gptp_tables 36/0 hosted
[R592] PASS RTL - git diff 412e3f6c..4c5d70b5 -- hdl gptp-processor (empty); tb/verilator/gptp_tables/sim_main.cpp:15,19 (comment-only) - no RTL, donor pin or stimulus change in the delta; local run 36/36 with reach lines identical to hosted
[R592] PASS Robustness - receipts/probes M1-M5, M7 against scripts/suite_shards.py --selftest and scripts/ci_events.py --check - each drift of duration, provisional figure, overhead count, matrix, ownership arm and --expect is refused fail-closed
[R592] PASS Tests - scripts/ci_events.py:5256-5263,5370-5380,5490-5503,6144,6439-6446,6547; receipts/probes M6/M8/M8b; ci_events --selftest 3096 arms; hosted shard 0/6 artifact gptp_tables.log - fixture advances are forced by the worker count (old fixture trips "fixture drift"), arm shape unchanged, M8 redundancy predates this round; 36 checks and 26/26 controls hosted
[R592] MINOR Docs - docs/testing/CI_WORKFLOWS.md:1322 - R592-5-F1 stale `--expect 5`
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6163132636 items 1-5; selector docstring steps 1-3; `TESTING.md:514-517`; the `suite_shards.py`, `rtl.yml` and `ci_events.py` delta; gates; hosted `verilator-suites` | R592-5 | `4c5d70b5` |
| RTL | CLEAN. The delta has no RTL; RTL content coverage stands from R592-4 at the same donor `e4869fd0` and unchanged lane RTL | Delta path list; `sim_main.cpp` comment lines; local and hosted M7 runs | R592-5 (delta), R592-4 (RTL content) | `4c5d70b5` / donor `e4869fd0` |
| Robustness | CLEAN | Probes M1-M5, M7, N1, N2; fail-closed contract | R592-5 | `4c5d70b5` |
| Tests | CLEAN | `ci_events.py` fixture advances; probes M6, M8, M8b; self-tests; hosted `gptp_tables` 36 checks and 26 controls; partition lists | R592-5 | `4c5d70b5` |
| Docs | **UNCLEAN**: R592-5-F1 open; R593-4-D1 and three earlier RESIDUEs carried; S1 optional | `CI_WORKFLOWS.md` delta and full-page grep; `TESTING.md:514-527`; suite README and harness header; selector docstring; PR body | R592-5 (not clean) | `4c5d70b5` |

## Real limits of this round

- I ran no full parent, PP, gPTP or Yosys bank locally. Full-suite evidence at this tree is the hosted `rtl-full` run, which I read but do not own.
- The local `gptp_tables` mutation campaign did not run because the copy was not a git checkout. The 26/26 controls come from the hosted artifact. The delta changes no lane RTL or stimulus.
- The hosted runs validated GitHub's merge `85b959cb` against dev `fa820988`. Its tree equals the head tree, but it is not the manager's current-dev candidate, which is built at the merge turn.
- No manager source bank exists at this head, and none is claimed.
- Physical calibration was NOT RUN. The skipped `Physical gPTP` context and any field skips are not hardware proof.
- Probe M9 shows that `--selftest` does not refuse an unmarked 1800 s figure. This predates the round, the head marks the figure correctly, and it is recorded for information only.

## Pending manager and executor duties

1. Fix R592-5-F1 at a new head and re-cover Docs there. A docs-only change to `CI_WORKFLOWS.md` does not un-cover the other lenses.
2. Selector step 3, now that run `38529993870` has passed:
   - replace `gptp_tables`' provisional 1800 s and worker 4's 115 s overhead with the figures `--measure` gives for that run (the hosted window seen here is about 572 s, but `--measure` is the authority);
   - drop the suite from `PROVISIONAL_SUITES`.

   That commit touches `scripts/suite_shards.py` and its docs, so Conformance, Tests and Docs must be re-covered at that head.
3. Carry R593-4-D1 and the three earlier RESIDUEs to the residue checklist.
4. The manager still owns exact-head hosted acceptance, the current-dev candidate (builder and native banks), donor-before-parent landing and post-merge containment.

## Clone integrity after probes

All probes ran in disposable worktrees under the packet's `scratch/`. `receipts/identity.log` was taken after all probes and shows:

- HEAD, tree and index are `4c5d70b5` / `8156e281`.
- Every tracked blob rehashes to its index entry, and modes are unchanged.
- The worktree is clean.
- All initialized gitlinks match their checkouts: `gptp-processor` `e4869fd0`, `protocol-processor` `2ad2f845`, `tsn-c-stack` `70936b77`, `verilog-axis` `48ff7a7e`, `lwSRP` `08ee86e8`.
- `external` (`efeb541a`) is uninitialized.

I made no GitHub write, source fix, commit, push or merge, contacted no author, ran no container and took no hardware action.

R592-5 FINISHED
