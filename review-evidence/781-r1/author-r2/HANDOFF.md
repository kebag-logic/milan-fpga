# HANDOFF — [A671] #781 media_phase hosted budget — ROUND 2

Lane: branch `781-media-phase-hosted-budget` (origin `https://github.com/kebag-logic/milan-fpga.git`), from dev
`a032c6d6e3775f145349d5a495c1e1ad12294936`; live remote `dev` still `a032c6d6` at the start of this round.
Assignment: [A10] Round 2, PR #782 comment 6390031279: record the hosted media_phase measurement, drop it from
`PROVISIONAL_SUITES`, keep `SUITE_SECONDS["media_phase"] = 1400`, "Closes #781".
Earlier rounds: `round1-archive/` (round 1 STOP), `round1b-archive/` (round 1b HANDOFF and PR body, verbatim). The
round 1b record also follows below this section. Receipts for this round: `receipts/round2/`, indexed in
`receipts/round2/INDEX.md`.

## Status: REVIEW READY

Every acceptance item is met, and every gate the change touches passes (rc 0). PR-BODY.md says "Closes #781".
The new head's hosted run is the final check, after the manager pushes.

Head `41f4a53cc0b12f143fa3e61a5339a11e79806ce9`: one new commit on `8a4fa2f9`, with no rebase and no amend. Nothing pushed.

- `41f4a53c` Record media_phase's hosted 582 s window and drop it from PROVISIONAL_SUITES, keeping 1400 s

## The measurement (receipts/round2/)

PR #782's own hosted run, 40131149135 (`rtl-full`, `pull_request`, head `8a4fa2f9`, merge commit `e9df8b0a` = dev
`a032c6d6` + `8a4fa2f9`, attempt 1). Job 120983200812, "Verilator shard 4/17", concluded `success`:

- Its suite step "Run this exhaustive suite shard" (step 23) ran 2026-10-24T20:50:36Z to 21:01:31Z: 655 s for all four
  of its suites (`controller_rate`, `datapath`, `fw_service_budget`, `media_phase`). Receipt: `shard4-17-steps.txt`, and
  `job-shard4-17.json` from `gh api`.
- Its log: `suites: 4   passed: 4   failed: 0   timed out: 0`, `checks: 24996   in-suite failures: 0`. `PASS media_phase` is
  at 21:01:31.71Z, after `PASS fw_service_budget` at 20:51:49.97Z. Receipts: `shard4-17-log-excerpt.txt`, plus the full log's
  sha256 and size in `shard4-17-log.sha256.txt` (280,156 bytes, over the size limit, so not copied).
- `python3 scripts/suite_shards.py --measure <that log>` gives `"media_phase": 582` (`shard4-17-measure.txt`). That is the
  suite's own window, 582 s of the 655 s step.
- The uploaded `suite-logs-4` artifact's `media_phase.log` ends `RESULT: PASS` (28 sub-results, all PASS). Its
  `TARGET_SHA` is `e9df8b0a`. Receipts: `suite-logs-4-media_phase.log` (74,941 bytes), `suite-logs-4-TARGET_SHA.txt`,
  `suite-logs-4.sha256.txt`, `target-sha-parents.txt`.
- Margin: 582 s, and the step's 655 s too, sit inside 1400 s / 1.1 = 1272 s. So #673's 10 % holds, and 818 s (58.4 %)
  remains.
- The run as a whole ended `cancelled`, but no test failed. 12 of the 17 Verilator shards and the fail-fast observer were
  cancelled from outside at 21:16Z to 21:18Z, and the Union jobs and the aggregate then failed downstream (`run-40131149135-jobs.json`). Shard 4/17
  had completed at 21:01:37Z.

## Changes (head 41f4a53c, against 8a4fa2f9)

| file:line | change | clause |
|---|---|---|
| `scripts/suite_shards.py:147` | `PROVISIONAL_SUITES` = `frozenset()` (was `{"media_phase"}`) | A10 Round 2 item 1 |
| `scripts/suite_shards.py:145-146` | the comment says that none is pending, and that #781's run measured `media_phase` | item 2 |
| `scripts/suite_shards.py:71-75` | the `SUITE_SECONDS` sources comment, which the docstring's new-suite step 3 points at. `media_phase` keeps 1400 s, above its own hosted 582 s window (run 40131149135, job 120983200812, step 655 s), because three earlier windows ran past 900 s | items 1, 2 |
| `scripts/suite_shards.py:112` | `"media_phase": 1400` unchanged | item 1 |
| `scripts/suite_shards.py:865-866` | with nothing pending, the head arm prints `ok   head no provisional figure is pending` and no longer prints an empty `{}` | follows from item 1 (the head arm's output would otherwise be misleading) |
| `scripts/run_all_suites.sh:250-251` | the budget's reason comment: "Its own hosted run then passed it in 582 s, and 1400 s is kept for that variance" (it used to say "stays provisional ... until that window is measured"). `suite_timeout` is unchanged | item 2, a stale claim |
| `docs/testing/CI_WORKFLOWS.md:438` | the #781 budget row: job and run ids, step times 20:50:36Z to 21:01:31Z, 655 s for four suites, `media_phase` 582 s, 818 s (58.4 %) remaining, the budget kept at 1400 s and not provisional because of the earlier over-900 s windows | item 2 |
| `docs/testing/CI_WORKFLOWS.md:2950-2951` | "the provisional `media_phase`" becomes "`media_phase`'s kept 1400-second budget" | item 2, a stale claim |

The worker count, the balance and the generated `rtl.yml` are unchanged. The /17 listings are byte-identical to `8a4fa2f9`'s.

## New checks and planted mutants

There is no new check. The only code change is the head arm's message for an empty set. `receipts/round2/mutants/mutants.txt`
(clean clone at `41f4a53c`, reset between mutants, clean controls rc 0): 8 caught, 1 expected escape, 0 departures.

| mutant | refused by | failing words |
|---|---|---|
| R1 provisional comparison disabled (`elif False:`) while nothing is pending | selftest's planted arm | `ESCAPED a provisional suite at 1800 s, suite_timeout's figure for it, passes, and at 1801 s is refused` |
| R2 the 582 s recorded as the figure, with media_phase left provisional | selftest head | `media_phase: provisional figure 582 s is not the 1400 s that run_all_suites.sh's suite_timeout gives it` |
| R3 `PROVISIONAL_SUITES` misspelt `{"media_phse"}` | selftest head | `media_phse: PROVISIONAL_SUITES names a suite with no figure in SUITE_SECONDS` |
| R4 driver `suite_timeout` media_phase 900 s | runner contract | `the declared 1400/1800/2400/3600/4800/5400-second suite budgets changed` |
| R5 overhead table at 16, not regenerated (round 1b M1) | selftest, generator check | `WORKER_OVERHEAD_SECONDS describes 16 workers; rtl.yml runs 17`; `regenerate the gate jobs` |
| R6 16 workers regenerated (round 1b M2) | selftest | `FAIL head worker 0/16 predicted 1640 s (27.3 min), bound 1620 s` |
| R7 60-minute index left at 15 (round 1b M5) | selftest, generator check | `FAIL head worker 16/17 predicted 2032 s (33.9 min), bound 1620 s`; `regenerate the gate jobs` |
| R8 media_phase 1499 s (round 1b M8) | selftest | `FAIL head worker 0/17 predicted 1621 s (27.0 min), bound 1620 s` |
| X1 **expected escape**: `SUITE_SECONDS["media_phase"]` lowered to 582 s, not provisional, driver kept at 1400 s | nothing: selftest PASS, rc 0 | — |

X1 is a consequence of item 1, recorded rather than hidden. Once a suite leaves `PROVISIONAL_SUITES`, no check ties its
`SUITE_SECONDS` figure to `suite_timeout`, as for every other measured suite. So the kept 1400 s is held by the recorded
decision and the comment, not by a gate. Round 1b's M3 (`SUITE_SECONDS` 900 s against the driver's 1400 s) has X1's shape
and is not rerun. M4's driver half stays refused by the runner contract (R4).

## Resources / route timing
Not applicable: no RTL or constraint change, no Vivado run.

## Gate table (head 41f4a53c; all rc 0, none piped)

| gate | result | receipt (`receipts/round2/head-41f4a53c/`) |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | `selftest: PASS`; `ok   head no provisional figure is pending`; worker 4/17 1539 s of 1620; 16/17 2032 s of 2160 | `suite_shards-selftest.txt` |
| `python3 scripts/ci_gate_workflows.py --check` | rc 0 | `ci_gate_workflows-check.txt` |
| `python3 scripts/ci_events.py --check` | OK, 2199 contract items, rc 0 | `ci_events-check.txt` |
| `run_all_suites.sh --list`, `--ci-pieces --list`, `--ci-pieces --shard k/17 --list` for k = 0..16 | 19 x rc 0; 64 suites, 81 units, each owned exactly once; media_phase on 4/17; milan_dp_mclk__0 alone on 16/17; byte-identical to 8a4fa2f9 | `coverage/` |
| `python3 scripts/lint_rtl.py --check` | LINT GATE: PASS, 89 <= ratchet 89, rc 0 | `lint/` |
| `cd tests && behave --no-capture -f plain` | 14 features, 406 scenarios, 1977 steps passed, rc 0 | `behave/` |
| docs workflow gate steps, run: bodies literally, GNU Make 4.3, CPython 3.12.3, clean clone | 42 steps rc 0 (44 steps, 0 failed; gate_42 and the no-git ci_step_3 replaced as in round 1b: the act row below, and `docs_check.py` rc 0 + `check_feature_status.py` rc 0 on a git-archive export); builder leg 1 again with the LiteX interpreter rc 0; the five markdown gates on CPython 3.12.3 rc 0 | `docs/` |
| trusted dev `a032c6d6` `act_ci.py --selftest --worktree <clean clone at 41f4a53c>` (docs gate_42's check; runner byte-identical at head) | selftest: PASS, rc 0 | `act/` |
| planted mutants (9) | 8 caught, 1 expected escape, 0 departures, rc 0 | `mutants/mutants.txt` |

The full sweep was not rerun. This commit changes comments, prose, one printed message and an empty
`PROVISIONAL_SUITES`. The sweep's only reader of these files is its preflight `suite_shards.py --selftest`, which passes
above. Round 1b's 64/64 sweep at `6f7b70ed` and this PR's hosted run at `8a4fa2f9` stand for the suites.

## Residue (not this PR)
- Unchanged from round 1b: `milan_dp__3` and `pp_shadow__3` run over their registered `PIECE_SECONDS` on hosted.
- X1 above: a measured figure is not held to its budget by any gate. That is existing design, and it is noted for the owner.

## Posted
- `[A671] REVIEW READY` on #781, head `41f4a53cc0b12f143fa3e61a5339a11e79806ce9`: issuecomment-6390444133 (2026-10-25, about 00:45 local). Body: `receipts/round2/posted-review-ready.md`.

---

# Round 1b record (verbatim from `round1b-archive/HANDOFF-round1b.md`)

# HANDOFF — [A671] #781 media_phase hosted budget — ROUND 1b

Lane: branch `781-media-phase-hosted-budget` from dev `a032c6d6e3775f145349d5a495c1e1ad12294936`
(origin `https://github.com/kebag-logic/milan-fpga.git`; live remote `dev` still `a032c6d6` at 21:33).
Assignment: [A10] ruling, issue #781 comment 6388150329 (option (b): a 17th 45-minute worker, media_phase 1400 s,
provisional until the PR's own hosted run measures it).
Round 1 (STOP) record: `round1-archive/HANDOFF-round1.md`. Receipts: `receipts/` (round 1), `receipts/round1b/` (this round).
The session was cut by a host reset at 21:22. The commit `6f7b70ed` survived. The sweep and docs runs were restarted from
scratch at 21:33 and are not reused.

## Status: REVIEW READY (local); hosted measurement pending (ruling step 3)

Every gate the change touches passes (rc 0; table below). "Closes #781" is withheld: its last acceptance items (measure
on this PR's own hosted run, record the figure, drop `media_phase` from `PROVISIONAL_SUITES`) need the manager's push.
PR-BODY.md therefore says "Relates to #781".

Head `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008`, two commits on `a032c6d6`, nothing pushed:

- `6f7b70ed` Give media_phase a provisional 1400 s budget on a seventeenth 45-minute Verilator worker
- `8a4fa2f9` State the Verilator aggregate's --expect 17 in the target-SHA contract (one doc line; a stale `--expect 16`
  that the first commit missed and that no checker reads)

## Changes (head 8a4fa2f9)

| file:line | change | clause |
|---|---|---|
| `scripts/suite_shards.py:112` | `SUITE_SECONDS["media_phase"]` 900 -> 1400 | ruling (b) step 2 |
| `scripts/suite_shards.py:142` | `media_phase` stays in `PROVISIONAL_SUITES` (unchanged) | ruling (b) "Measurement" |
| `scripts/suite_shards.py:147-149` | `WORKER_OVERHEAD_SECONDS = (122,) * 17`, with comment | ruling step 1 |
| `scripts/suite_shards.py:9,22` | docstring: sixteen regular workers of seventeen; example `--shard 0/17` | step 1 |
| `scripts/run_all_suites.sh:258` | `suite_timeout` `media_phase` 900 -> 1400 | step 2 |
| `scripts/run_all_suites.sh:42,249-251` | help text and the budget's reason comment (#781) | step 2 |
| `scripts/measure_test_evidence.py:675,680` | the runner-contract copy of `suite_timeout` and its message follow 1400 s | step 2 (the test-evidence ratchet compares the driver against this copy) |
| `.github/workflows/rtl.yml:144,166-167,620,1583-1595` | regenerated by `python3 scripts/ci_gate_workflows.py`: 60-minute index `matrix.shard == 16`, `total: [17]`, `--expect 17`, fail-fast job lists at /17 | step 1, "through their own generators" |
| `docs/testing/CI_WORKFLOWS.md:350-351,360-361,369-374,383,386,405,438,554,1365,2303,2930-2951,3119-3120` | worker count seventeen, worker 16 owns leg A, the #781 paragraph, the budget table row with the hosted figures, the per-worker load table at /17, `--expect 17`, `--shard 0/17` and `16/17` examples | step 1 "the worker count in CI_WORKFLOWS.md" |
| `docs/testing/RUNNING_TESTS.md:84,89,94` | 64 suites, seventeen workers, `--shard 0/17` | step 1 |
| `docs/testing/TESTING.md:541,546,552,554` | seventeen workers, `INDEX/17`, `--shard 0/17` | step 1 |

The counts 63 -> 64 suites and 80 -> 81 units correct a figure that was already stale at dev. `run_all_suites.sh --list` gives 64
and `--ci-pieces --list` gives 81 at `a032c6d6` too, because #770 added `media_phase` without updating them. They sit in
the sentences this change rewrites for the worker count.

`.github/ci-templates/rtl.yml` is generator input and is unchanged. It keeps dev's six-worker matrix, as the docs state.

## New checks and planted mutants

There is no new check code. The existing selector self-test, generator `--check` and test-evidence runner contract refuse
every planted defect this change could carry. `receipts/round1b/mutants/mutants.txt` (clone at `6f7b70ed`; the files
mutated are byte-identical at `8a4fa2f9`) records 8 caught and 0 escaped, after clean controls at rc 0:

| mutant | refused by | failing words |
|---|---|---|
| M1 overhead table back at 16, workflow not regenerated | selftest, generator check | `WORKER_OVERHEAD_SECONDS describes 16 workers; rtl.yml runs 17`; `regenerate the gate jobs` |
| M2 16 workers regenerated, media_phase 1400 s | selftest | `FAIL head worker 0/16 predicted 1640 s (27.3 min), bound 1620 s` |
| M3 SUITE_SECONDS 900 vs driver 1400 | selftest | `provisional figure 900 s is not the 1400 s` |
| M4 driver 900 vs SUITE_SECONDS 1400 | selftest, runner contract | `provisional figure 1400 s is not the 900 s`; `suite budgets changed` |
| M5 rtl.yml 60-minute index left at 15 | selftest, generator check | `FAIL head worker 16/17 predicted 2032 s (33.9 min), bound 1620 s` |
| M6 rtl.yml `--expect 16` | generator check | `regenerate the gate jobs` |
| M7 rtl.yml `total: 16` | generator check | `regenerate the gate jobs` |
| M8 media_phase 1499 s (first figure no regular worker takes) | selftest | `FAIL head worker 0/17 predicted 1621 s (27.0 min), bound 1620 s` |

## Per-worker planned load against bound (17 workers, selector self-test at 8a4fa2f9)

Each figure includes the 122 s setup allowance. Bounds: regular 1620 s (absolute rule at 45 min); worker 16 is 2160 s
(60 min, the #737 exception).

| worker | load s | bound s | slack s | note |
|---|---|---|---|---|
| 0 | 1605 | 1620 | 15 | |
| 1 | 1541 | 1620 | 79 | tsn_fuzz owner |
| 2 | 1572 | 1620 | 48 | |
| 3 | 1538 | 1620 | 82 | chmap_capture owner, gptp_tables |
| 4 | 1539 | 1620 | 81 | media_phase 1400 s |
| 5 | 1538 | 1620 | 82 | |
| 6 | 1539 | 1620 | 81 | |
| 7 | 1539 | 1620 | 81 | |
| 8 | 1540 | 1620 | 80 | |
| 9 | 1541 | 1620 | 79 | |
| 10 | 1537 | 1620 | 83 | |
| 11 | 1540 | 1620 | 80 | |
| 12 | 1539 | 1620 | 81 | |
| 13 | 1537 | 1620 | 83 | |
| 14 | 1537 | 1620 | 83 | |
| 15 | 1538 | 1620 | 82 | |
| 16 | 2032 | 2160 | 128 | milan_dp_mclk__0 alone |

## Resources / route timing
Not applicable: no RTL or constraint change, no Vivado run, no resource change.

## Gate table

All rc 0, none piped. Receipts are under `receipts/round1b/`, indexed in `receipts/round1b/INDEX.md`. `6f7b70ed..8a4fa2f9`
changes one prose line in `docs/testing/CI_WORKFLOWS.md`, and only comments mention that file in the sweep scripts. So
the sweep and mutants at `6f7b70ed` cover the head. Every gate that reads the docs was rerun at `8a4fa2f9`.

| gate | head | result | receipt |
|---|---|---|---|
| `python3 scripts/suite_shards.py --selftest` (17 workers, balance, bounds) | 8a4fa2f9 | PASS, rc 0 | `head-8a4fa2f9/suite_shards-selftest.txt` |
| `python3 scripts/ci_gate_workflows.py --check` (generated rtl.yml matches its generator) | 8a4fa2f9 | rc 0 | `head-8a4fa2f9/ci_gate_workflows-check.txt` |
| `python3 scripts/ci_events.py --check` | 8a4fa2f9 | OK, 2199 contract items, rc 0 | `head-8a4fa2f9/ci_events-check.txt` |
| `run_all_suites.sh --list`, `--ci-pieces --list`, `--ci-pieces --shard k/17 --list` for k = 0..16 | 8a4fa2f9 | 19 x rc 0; 81 units, each owned exactly once; media_phase on 4/17; milan_dp_mclk__0 alone on 16/17 | `head-8a4fa2f9/coverage/` |
| full sweep, 4 parallel shard units (`run_all_suites.sh <logs> --wait --shard k/4`, pinned Verilator 5.050) | 6f7b70ed | 64/64 suites PASS, 0 failed, 0 timed out, 2,189,253 checks, 0 in-suite failures; shard rc 0/0/0/0 (4099 s, 2673 s, 3131 s, 2568 s); preflight self-tests PASS; tsn_fuzz declares its 4 tsn-gen-absent skips | `sweep-6f7b70ed/` |
| `python3 scripts/lint_rtl.py --check` | 8a4fa2f9 (and 6f7b70ed) | LINT GATE PASS, 89 <= ratchet 89, rc 0 | `head-8a4fa2f9/lint/` |
| docs workflow gate steps, run: bodies literally, GNU Make 4.3, CPython 3.12.3, clean clone | 8a4fa2f9 | 42 steps rc 0, 2 skipped (below) | `head-8a4fa2f9/docs/all.out`, `all-receipts.json` |
| builder leg 1 again with the LiteX interpreter | 8a4fa2f9 | rc 0 | `head-8a4fa2f9/docs/leg1-litex*` |
| the five markdown gates on CPython 3.12.3 | 8a4fa2f9 | 5 steps rc 0 | `head-8a4fa2f9/docs/md312*` |
| no-git step's two gates on a git-archive export (`docs_check.py`, `check_feature_status.py`) | 8a4fa2f9 | rc 0, rc 0 | `head-8a4fa2f9/docs/nogit_*` |
| act runner contract (docs gate_42's check): dev `a032c6d6` `act_ci.py` (byte-identical at head) `--selftest --worktree <candidate clone>` | 8a4fa2f9 (and 6f7b70ed) | selftest PASS, rc 0 | `head-8a4fa2f9/act/` |
| `cd tests && behave --no-capture -f plain` | 8a4fa2f9 (and 6f7b70ed) | 14 features, 406 scenarios, 1977 steps passed, rc 0 | `head-8a4fa2f9/behave/` |
| planted mutants (8) | 6f7b70ed | 8 caught, 0 escaped, rc 0 | `mutants/mutants.txt` |

Docs skips, as in earlier lanes' replicas: gate_42 runs the candidate's `act_ci.py` on the host, which AGENTS.md section 5
forbids. The trusted-copy act self-test above covers its check instead. The no-git `ci_step_3` body deletes `.git`, so its
two gates run on an export instead.

Run 1 of the docs replica (at `6f7b70ed`, before the reset) failed gate_8 with rc 128: `fatal: couldn't find remote ref
dev`, because the lane had no local `dev` for the clone's `origin` to serve. A defect in the replica, not in the change. Run 2
was stopped deliberately to move to `8a4fa2f9`. Both are kept in scratch only, and neither is cited.

## Residue (not this PR)
- Hosted pieces exceed their registered PIECE_SECONDS: `milan_dp__3` (231 s registered, 354–419 s hosted) and
  `pp_shadow__3` (347 s registered, 378–451 s hosted), shard 10/16 on runs 40098975073 and 40103838859.
- Ruling step 3 follow-up (the manager's hosted run): record `media_phase`'s measured hosted window (job id, times) in a
  follow-up commit. Drop it from `PROVISIONAL_SUITES` only if the window fits 1400 s with a 10% margin (window <= 1272 s);
  otherwise STOP with the figure.

## Posted
- `[A671] REVIEW READY` on #781, head `8a4fa2f971427b1deb1f20a4b456a8a4d94bf008`: issuecomment-6389307744 (2026-10-24, about 22:50 local).
