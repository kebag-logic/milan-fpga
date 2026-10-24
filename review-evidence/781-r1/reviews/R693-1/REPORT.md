[R693] POSITIVE - exact head 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008

# R693-1: internal cleared-context review of PR #782 (issue #781)

- Head under review: `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008`, tree `57cbe969ebfcd88b476edc9408446c13e299a01d`. It has two one-line commits with no trailers, `6f7b70ed` and `8a4fa2f9`, on dev `a032c6d6e3775f145349d5a495c1e1ad12294936`.
- Live dev at review time: `a032c6d6`.
- Scope reconstructed from four sources:
  - the #781 issue body;
  - the assignment (issuecomment-6387505940);
  - the executor's STOP figures (issuecomment-6388138007, 2026-10-24T18:48Z);
  - the ruling, option (b) (issuecomment-6388150329): a seventeenth 45-minute hosted Verilator worker, `media_phase` at 1400 s, and `media_phase` stays provisional until this PR's own hosted run measures it.
- Authorities read: AGENTS.md, CONTRIBUTING.md, docs/README.md, `scripts/suite_shards.py` (module docstring new-suite steps, `balance`, `headroom_problems`), `scripts/ci_suite_workflows.py` `generate()`, and `docs/testing/CI_WORKFLOWS.md`.
- Diff: `git diff a032c6d6..8a4fa2f9`, 7 files.
- Public evidence: tree `ac1cc4ef` `review-evidence/781-r1`, plus this PR's own hosted run 40131149135.

No prior public review finding exists on this PR at the time of writing. The PR carries only the two review-start comments (R693-1, R694-1) and no review objects. Nothing needed to be resolved or retained.

## Verdict basis

- The delta does exactly what ruling (b) requires, and it does it through the generators. No suite is weakened or skipped.
- Every worker's planned load fits its bound.
- Every planted defect inside this change's scope is caught.
- The PR's own hosted shard 4/17 job measured `media_phase` at 581.7 s against the 1272 s bar (1400 s less 10 %).
- No BLOCKER, MAJOR, MINOR or RESIDUE finding is open. Four SUGGESTIONs follow.

## Checks against the focus list

**(1) Selector and runner figures**
- `scripts/suite_shards.py:112` is `"media_phase": 1400`.
- `scripts/suite_shards.py:149` is `WORKER_OVERHEAD_SECONDS = (122,) * 17`.
- `scripts/suite_shards.py:142` keeps `PROVISIONAL_SUITES = frozenset({"media_phase"})`.
- `scripts/run_all_suites.sh:258` gives `media_phase` `${SUITE_TIMEOUT:-1400}`. Its header at `:42` says 1400 s.
- The contract copy at `scripts/measure_test_evidence.py:675` is 1400, and its message at `:680` matches.
- The self-test line `head provisional figures {'media_phase': 1400} are what run_all_suites.sh's suite_timeout gives` passes.

**(2) Generated workflow**
- `.github/workflows/rtl.yml:144` is `matrix.shard == 16 && 60 || 45`.
- `:150-167` gives shards 0..16 and `total: [17]`.
- `:620` is `--expect 17`.
- The fail-fast job lists at `:1583-1598` name `Verilator shard 0/17`..`16/17`.
- `generate()` in `scripts/ci_suite_workflows.py:96-115` derives the matrix, the `--expect` value and the 60-minute index from `len(WORKER_OVERHEAD_SECONDS)`. The template `.github/ci-templates` is unchanged.
- `ci_gate_workflows.py --check` gives rc 0, so the committed `rtl.yml` is byte-equal to the generator output. Hand-edit mutants M8 to M12 below are all refused.
- `ci_events.py --check` gives `OK (2199 contract item(s))`.

**(3) Worker fit**
- Self-test at the head:
  - workers 0..15 are at 1605, 1541, 1572, 1538, 1539, 1538, 1539, 1539, 1540, 1541, 1537, 1540, 1539, 1537, 1537 and 1538 s, all against 1620 s;
  - worker 16 is at 2032 s against 2160 s (#737);
  - the specialized owners are `tsn_fuzz`:1, `chmap_capture`:3 and `milan_dp_mclk__0`:16, with the media-clock history alone.
- Ownership listings (`--ci-pieces --shard k/17 --list` for k = 0..16): 81 units, 81 distinct, each owned exactly once, nothing missing or extra. `media_phase` is on worker 4 and `milan_dp_mclk__0` alone on worker 16. The serial `--list` gives 64 suites, and 64 - 6 split parents + 23 pieces = 81.
- My own capacity arithmetic, from the head's tables (`capacity.py`):
  - at 16 workers, `media_phase` = 1400 puts regular demand at 22768 s against 22470 s capacity, 298 s over, so no 16-worker balance exists;
  - at 17 workers the slack is 1200 s;
  - 1498 s fits at exactly 1620 s and 1499 s does not.

**(4) No weakening, and the planted defects**
- The diff touches no `tb/`, `hdl/` or suite driver.
- The hosted `media_phase` log at this tree has the same 28 result blocks and 386 checks as the executor's local runs, with 0 failures: 11 detector cases, 13 loop cases, and the pins, blend and offset targets.
- Mutation campaign (`mutants.py`): 16 mutants plus 2 controls, run in shared local clones with the submodules at their gitlinks.
  - Both controls are clean: the unmutated head, and 1498 s on both sides.
  - 12 mutants are caught. These include all eight the executor names:
    - M1, the overhead table left at 16;
    - M2, 16 workers regenerated with 1400;
    - M3 and M4, 900 left in `SUITE_SECONDS` and in `suite_timeout`;
    - M8, M9 and M10, the 60-minute index, `--expect` and `total` hand-edited;
    - M6, 1499 s.
  - Also caught: M5 (the contract copy left at 900), M11 (shard 16 dropped from the matrix), M12 (`16/17` dropped from the fail-fast list) and M16 (a provisional figure different from `suite_timeout`).
  - 4 escape, all outside this head's correctness, see S1 and S2:
    - M7 drops `media_phase` from PROVISIONAL. That is the follow-up's legitimate step, so it is not a defect.
    - M13 puts `--expect 16` back in the CI_WORKFLOWS prose.
    - M14 regenerates with 18 workers.
    - M15 changes one docs worker-table row.

**(5) Docs and gates**
- `CI_WORKFLOWS.md` states the counts at `:350-351` (81 units, seventeen workers, 64 suites), worker 16 at `:359`, the #781 paragraph at `:369-373`, the #781 budget row at `:438`, `--expect 17` at `:1365`, and the /17 load table at `:2930-2946`.
- `RUNNING_TESTS.md:84,89,94` and `TESTING.md:541,546,552,554` state seventeen workers.
- `doc_table.py` checks the docs table against the self-test's head predictions: all 17 rows, loads and margins match.
- Arithmetic in the row: 787.5 x 1.575 = 1240.3 s, 1240 x 1.1 = 1364 s, so 1400 s exceeds #673's 10 %. The 1.575 ratio is pp_shadow__3's 451.1 s hosted over 286.4 s local, both in the executor's receipts.
- Gates at the head, all rc 0:
  - `suite_shards.py --selftest` (`selftest: PASS`);
  - `ci_gate_workflows.py --check`;
  - `ci_events.py --check` and `--selftest`;
  - `lint_rtl.py --check` on the pinned Verilator 5.050 (identity `Verilator 5.050 2026-07-01 rev v5.050`): `LINT GATE: PASS (89 <= 89)`;
  - `cd tests && behave --no-capture -f plain`: 406 scenarios passed, 0 failed, 0 skipped;
  - 27 docs-workflow gate commands that read this diff: `docs_check`, `check_em_dash --base a032c6d6` (0 findings over 46 added lines), `check_doc_style` and its self-test, `DOC_MAP --check`, `check_feature_status`, `measure_test_evidence --check` and `--selftest`, `check_hygiene`, the py and sh idiom gates, `check_doc_paths`, `check_archive`, `gen_toc --verify-anchors`, `--check` and `--selftest`, `ci_gate_workflows_selftest`, `ci_suite_pieces_selftest`, `ci_suite_collect_selftest`, `ci_fail_fast_selftest`, `generate_ci_evidence_pins --check`, `ci_workflow_plan_selftest`, `ci_manifest_selftest` and `ci_runtime_evidence_selftest`.
- The Markdown-renderer gates ran on the pinned `cmarkgfm`/`html5lib` environment.

**(6) This PR's own hosted run**
- Run 40131149135 (`rtl-full`, attempt 1), job 120983200812 `Verilator shard 4/17`: started 20:45:49Z, completed 21:01:37Z, conclusion success.
- The job validated merge commit `e9df8b0a1f7c` (artifact `TARGET_SHA`). Its parents are `a032c6d6` and `8a4fa2f9`, and its tree is `57cbe969`, identical to the head tree.
- Suite step: 20:50:36Z to 21:01:31Z.
  - Shard line 20:51:40.257Z, `shard: 4/17   selected suites: 4`.
  - Verdicts: `controller_rate` at 20:51:45.117Z, `datapath` at 20:51:48.895Z, `fw_service_budget` at 20:51:49.966Z, and `PASS media_phase` at 21:01:31.712Z.
  - Summary: `suites: 4 passed: 4 failed: 0 timed out: 0`, `checks: 24996`.
- **The `media_phase` window is 581.746 s.** `suite_shards.py --measure` reads it as 582. It is **at or under 1272 s (1400 / 1.1 = 1272.7 s): it fits 1400 s with the 10 % margin.**
- The job span was 948 s against 2700 s. Setup ran to about 287 s, because `Build Verilator from source on cache miss` took 270 s, above the 122 s allowance. This is pre-existing cache behaviour, and the job is still far inside its limit.
- This is one sample. The manager records the figure in the follow-up commit.

## Findings

**S1 SUGGESTION — Tests, Docs — `docs/testing/CI_WORKFLOWS.md:1365` and `:2930-2946`**
- Evidence: two docs mutants escape all four checks. M13 restores `--expect 16` in the target-SHA contract prose, and M15 changes worker 4's table row to 1540/80. The same `--expect 16` was the stale line the second commit fixed by hand.
- Impact: the head's values are correct (`doc_table.py` PASS; the line reads 17), but a future worker-count change can leave this prose stale without any gate failing.
- Optional outcome: derive the /N load table and the `--expect` sentence from the selector, or check them in `ci_events.py`.
- Verification: M13 and M15 turn a gate nonzero.

**S2 SUGGESTION — Robustness, Tests — `scripts/suite_shards.py:149`, `.github/workflows/rtl.yml` matrix**
- Evidence: M14 sets `(122,) * 18` and regenerates `rtl.yml`, and passes every check. The selector bounds the worker count only from below, by fit, so an over-provisioned matrix that the ruling did not authorize is not refused.
- Impact: none at this head. It only adds runner time.
- Optional outcome: pin the ruled count, or state that any count that fits is acceptable.
- Verification: M14 is caught, or the docs state the intent.

**S3 SUGGESTION — Conformance, Docs — for the follow-up commit, `scripts/suite_shards.py:112` and `docs/testing/CI_WORKFLOWS.md:438`**
- Evidence: both earlier TIMEOUT runs were PR heads that change `media_phase`'s inputs:
  - #779 `e658682e` changes `tb/verilator/media_phase/ofs_wrap.sv`;
  - #778 `01fc5475` changes `hdl/ieee1722/crf/KL_crf_tx.sv`, which `tb/verilator/media_phase/Makefile:53` (`CRFTX_RTL`) compiles.
- This PR's 582 s measures dev's suite at this tree. The issue body's "does not touch the media clock, so this is dev-wide" therefore does not hold for #778's inputs.
- Impact: if the follow-up records 582 s as the planned figure, the selector would plan #778's and #779's heads below the more than 900 s their hosted runs showed.
- Optional outcome: keep the 1400 s `suite_timeout`, and state in the follow-up's row that 582 s is the dev-tree window while the queued heads ran over 900 s. Then consider re-measuring after those heads merge.
- Verification: the follow-up's row and figure, reviewed at its head.

**S4 SUGGESTION — Docs — `docs/testing/CI_WORKFLOWS.md:369` and `:438`**
- Evidence: the paragraph and the row cite `#781` but do not link the ruling comment (issuecomment-6388150329) that authorizes the seventeenth worker. Meanwhile `:440-441` keeps the #673-ruling sentence under the same table.
- Impact: a cold reader has to find the authorization on the issue.
- Optional outcome: link the ruling as `:440` links #673's.
- Verification: link-health gate.

Comment rule: the new source comments are at `scripts/suite_shards.py:9` and `:147-148`, and `scripts/run_all_suites.sh:249-251`. They state behaviour and reason with issue IDs (#781) only. No lane label, round, reviewer ID or comment ID appears. There is no RESIDUE.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling (b) issuecomment-6388150329 against `suite_shards.py:112,142,149`, `run_all_suites.sh:258`, `measure_test_evidence.py:675`, `rtl.yml:144,167,620,1583-1598`; issue acceptance items 1-2 and "no weakening" met; items 3-4 sequenced to the follow-up by the ruling; hosted window 581.746 s, at or under 1272 s (job 120983200812) | R693-1 | `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008` |
| RTL | CLEAN | diff touches no `hdl/` or `tb/`; `lint_rtl.py --check` on pinned 5.050, PASS 89 <= 89; CI architecture contracts: `ci_suite_workflows.py:96-115` derivation from `len(WORKER_OVERHEAD_SECONDS)`, `ci_suite_collect.py:19` and `ci_suite_pieces_selftest.py:95` consumers, `ci_gate_workflows.py --check`, `ci_events.py --check` (2199 items) | R693-1 | `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008` |
| Robustness | CLEAN | `balance`/`headroom_problems` (`suite_shards.py:247-441`); boundaries 1498 (passes) and 1499 (refused); 2038/2039 on worker 16; 16-worker infeasibility (298 s over); 60-minute arm on the dedicated last worker (M8 refused); fail-closed union/aggregate unchanged; hosted queueing and cache-miss setup observed, inside the limits (S2 optional) | R693-1 | `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008` |
| Tests | CLEAN | `suite_shards.py --selftest` PASS; 17 ownership listings (81/81 once); behave 406/406; mutation campaign: 2 controls clean, 12 of 16 caught, including all 8 the executor names, and the 4 escapes analysed (S1, S2, M7 by design); hosted `media_phase` 386 checks / 0 failures at the head tree | R693-1 | `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008` |
| Docs | CLEAN | `CI_WORKFLOWS.md:350-373,438,1365,2930-2952`, `RUNNING_TESTS.md:84-94`, `TESTING.md:541-554`; `doc_table.py` 17/17 rows match the self-test; 27 docs gate commands rc 0; comment rule clean (S1, S4 optional) | R693-1 | `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008` |

## Real limits

- I did not run a full sweep; the full parent bank is not allowed. The executor's 4-shard sweep receipts are at `6f7b70ed` (64/64), and `6f7b70ed..8a4fa2f9` changes one line of `CI_WORKFLOWS.md` (numstat 1/1).
- I prepared a local shard 4/17 replica, but the review environment refused its probe-clone setup, so it did not run. The hosted shard 4/17 executed at the head tree instead.
- Not run:
  - `act_ci.py --selftest` (forbidden here);
  - the docs builder legs (SDK, sv2v);
  - the no-git docs job.
- Interpreters: Python 3.14.8, against CI's 3.12, and GNU Make 4.4.1 (no 4.3 was available). None of the docs gate commands I ran invokes make.
- Hosted run 40131149135, snapshot at 21:07:40Z:
  - Executed and successful: shards 0, 4, 7 and 11 of 17, and `Prepare pinned Yosys`.
  - Still in progress or queued: the other 13 Verilator shards, the Yosys shards, the six unions, `verilator-suites`, `yosys-portability`, and the `docs`, `elaborate` and `rtl-fast` runs.
  - Skipped: `Physical gPTP` (nightly only).
  - The protected contexts are therefore not yet established.
- The hosted figure is a single sample.
- No physical calibration was run. There is no hardware proof.

## Pending manager duties

1. Record the measured window in the follow-up commit (job 120983200812, run 40131149135 attempt 1, window 20:51:49.966Z to 21:01:31.712Z, 581.746 s) and drop `media_phase` from `PROVISIONAL_SUITES`. That commit changes artifacts in the Conformance, Robustness, Tests and Docs scopes (and RTL's CI-architecture scope), so it un-covers those lenses and needs a re-review at its head. See S3.
2. Hosted and act acceptance of every context at the final head, including the six unions and `verilator-suites` across all 17 workers.
3. Current-dev merge-candidate validation (builder and native banks) at the merge turn.
4. Carry the side observation (`milan_dp__3`, `pp_shadow__3` over their PIECE_SECONDS) to its separate Issue, as ruled.
5. Close #781 only after the follow-up. The PR currently says "Relates to #781".

R693-1 FINISHED
