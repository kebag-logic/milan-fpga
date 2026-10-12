[A604]

## Contents

- **[Status](#status)** - Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** - Public task, executor, and independent reviewers.
- **[Description](#description)** - What changed and why.
- **[Authoritative references](#authoritative-references)** - Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** - Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** - The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY (round 3) at `2c2f336979e4fdb1da444f041f37551e2c9175df`. Every local gate this change touches exits 0. The documented new-suite steps were followed in a disposable clone. In it, `--selftest`, `ci_events.py --check` and `--selftest`, and the serial sweep's preflight all exit 0 (Round 3 below). Earlier heads: round 2 `61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3`, round 1 `a57d384dc697249c2a69f80079b676875d4f7560`. Acceptance 3 (each worker measured at 72 min or less) waits for this PR's hosted run. `727-shard-balance` -> `dev`.

## Linked Issue / roles

Closes #727
Relates to #696, #444

Executor: `[A604]`
Internal cleared-context reviewer: `[R626]`
External reviewer: `[R627]`

## Description

On dev `c6bd08c6` the SHA-256 owner rule put the heavy suites on Verilator worker 1/5: 104 of its 120 minutes (run 38217650945). #696's longer `maap` then timed that worker out (run 38208503834). This PR assigns the default suites by measured hosted time.

| Piece | Change |
|---|---|
| `scripts/suite_shards.py` `SUITE_SECONDS` | 62 per-suite durations, each from its worker's previous result line (or its `shard:` line) to its own, rounded up. From dev run 38217650945, all five workers, except `maap` (1375 s), from #696's run 38208503834, worker 1/5. |
| `WORKER_OVERHEAD_SECONDS` | Each worker's job time outside its suites (setup before the first suite, tally after the last): 83, 115, 80, 93, 80 s. Recorded separately from the first suite. |
| `balance` | `milan_dp` alone on the last worker (#444). `tsn_fuzz` stays pinned to 1 and `chmap_capture` to 3, which the workflow's ownership step proves, so `rtl.yml` is unchanged. The rest go longest first to the least-loaded worker, ties by name and lower worker: deterministic and disjoint. |
| sharded selection | Refuses an inventory suite with no duration and a duration with no inventory suite (exit 2). The serial `0/1` selection needs no table and is unchanged; the sweep's preflight runs `--selftest`, which needs every suite in the table. |
| new-suite steps | A new default suite's first figure is the wall clock `run_all_suites.sh`'s `suite_timeout` gives it (1800 s unless it has its own arm), recorded in `SUITE_SECONDS` and named in `PROVISIONAL_SUITES`. If a worker is then predicted above 60%, the same change adds a worker; the docstring lists every pin that moves. The change's own hosted run then replaces the figure through `--measure`. The refusal for a suite with no figure names these steps. |
| `--selftest` | Holds the head's table to its inventory and to 60% of the Verilator job's `timeout-minutes`, read with the worker count from `rtl.yml`. Plants each defect: a missing duration, a stale duration, a zero duration, a tighter `rtl.yml` timeout, one more `rtl.yml` worker than the overhead table, and heavy durations (at the bound passes, one second over fails, a pigeonhole growth fails). One arm checks the bound applied at each `timeout-minutes` against 36 s a minute, without the bound formula or its percentage, so loosening the 60% fails it. Planting each specialized suite at its lightest and heaviest proves the pins hold. Each provisional figure must equal `suite_timeout`'s, read from the driver. Four arms plant against the driver: the `*` figure passes and one second more is refused; a planted `*` arm moves the expectation; a planted own arm is honoured; a provisional name with no figure is refused. Each worker's `--shard` list, printed by separate processes under two hash seeds, must equal this process's selection. A copy that skips the head arms while `rtl.yml`, the inventory or the driver is beside it fails. |
| `--measure LOG...` | Prints both tables from `gh run view --log` worker logs; the docstring's refresh procedure uses it. |
| `docs/testing/CI_WORKFLOWS.md` | The worker paragraph and the #621 history line now describe the measured-time split, not the hash. The provenance sentence names `maap`'s #696 pull-request run as the one exception to the dev run. The refresh sentence also points to the new-suite steps. |
| `docs/testing/TESTING.md` | The serial-sweep paragraph says that the sweep's preflight and every hosted worker run the selector's self-test. That self-test refuses to start until `SUITE_SECONDS` names every default suite, and a new suite first records a provisional figure. |

Predicted per worker (bound 4320 s = 72.0 min):

| Worker | Old (hash) with #696 | New |
|---|---:|---:|
| 0/5 | 44.6 min | 70.1 min (4204 s) |
| 1/5 | 125.1 min | 70.1 min (4205 s) |
| 2/5 | 78.9 min | 70.0 min (4203 s) |
| 3/5 | 31.7 min | 70.1 min (4205 s) |
| 4/5 | 48.0 min | 48.0 min (2877 s) |

The model reproduces the old split's measured job times on run 38217650945 within 8 s. That check is in-sample.

Removed from the self-test: the hash rule's runtime landmarks `pp_shadow: 1`, `mmcm_servo: 2` and `milan_dp_gm_steps: 3`. They pinned the outputs of the rule this PR replaces. The per-worker bound now checks every worker's predicted time, and the specialized-owner landmarks remain.

### Round 2

Both round-1 reviews were NEGATIVE on one MINOR finding, F1 under Tests: no self-test arm failed when the 60% figure itself was loosened. Three new commits answer the round-2 assignment (issue #727 comment 6126048117). There is no rebase or amend. Line numbers in this section are at `61296ea1`.

| Commit | Change |
|---|---|
| `1d5f1c88` | F1. `scripts/suite_shards.py:596-611`: the 116/117-minute arm keeps the bound that each planted `rtl.yml` applied. A new arm requires the bound applied at 120, 116 and 117 minutes to equal `minutes * 36` s, computed without `bound_seconds` or `HEADROOM_PERCENT`. |
| `78cee0d6` | Optional S2. `:585-588` plants a 0 s duration, and `:613-620` plants `total: [6]` in `rtl.yml`. `with_verilator_key` (`:548-557`) replaces `with_verilator_timeout` so that one helper plants either key. |
| `61296ea1` | Residue R1. `docs/testing/CI_WORKFLOWS.md:191-196` says that every figure comes from one dev run, except `maap`. `maap` keeps #696's pull-request figure until a dev run measures it. |

Residue R2 from the external review is fixed in this body: the warm-cache bullet under Known limitations. The round-1 internal reviewer's `mutate.py` (on `727-review-evidence`, `review-evidence/727-r1/reviews/R626-1/scripts/`) ran unmodified on the old and new heads:

| Case | `a57d384d` | `61296ea1` |
|---|---|---|
| `headroom-75-percent` | rc 0, PASS | rc 1, new 36 s arm `ESCAPED` (applied 5400 s at 120 min) |
| `headroom-100-percent` | rc 0, PASS | rc 1, new 36 s arm `ESCAPED` (applied 7200 s) |
| `bound-formula-div10` | rc 0, PASS | rc 1, new 36 s arm `ESCAPED` (applied 43200 s) |
| `table-zero-duration-allowed` | rc 0, PASS | rc 1, zero-duration arm `ESCAPED` |
| `worker-count-mirrored-5` | rc 0, PASS | rc 1, six-worker arm `ESCAPED` |
| `tree-head` | rc 0, PASS | rc 0, PASS |

In each rc 1 row above, the named arm is the only failure. Every other case of the 29 gives the same rc as at `a57d384d`. The table, balance, selection and predictions are unchanged: the five lists are byte-identical to round 1's.

### Round 3

The internal review R626-2 was NEGATIVE on one MINOR finding, F1 under Docs and Robustness. A change that adds a default suite was refused, and the remedy the refusal named (a dev-run refresh) could not cure it. The external review R627-2 was POSITIVE. Five new commits answer the round-3 assignment (issue #727 comment 6126613714). There is no rebase or amend, and `rtl.yml` is unchanged. Line numbers in this section are at `2c2f3369`.

| Commit | Change |
|---|---|
| `7d5fba48` | Item 1. `scripts/suite_shards.py:54-87`: the new-suite steps. `:200` `PROVISIONAL_SUITES` (empty). `:239-244`: the refusal names the steps. `:336-382` `driver_timeouts` and `provisional_problems` read `suite_timeout`'s `case` from `scripts/run_all_suites.sh`; an arm of another shape, a duplicate, or `*` not last is refused. `:768-794`: four planted arms. `:812-826`: the head's provisional figures are checked against the driver. |
| `4c480494` | Optional S2. `:800-808`: a copy may skip its head arms only when none of `rtl.yml`, `tb/verilator` and the driver is beside it. |
| `2464210b` | Optional S1. `:857-881`: `seeded_selftest` compares each worker's `--shard` list from processes under `PYTHONHASHSEED` 1 and 2 with this process's selection. |
| `4994aa9c` | Item 2. `docs/testing/TESTING.md:513-519`, `docs/testing/CI_WORKFLOWS.md:198-202`. |
| `2c2f3369` | Item 1 completed by item 3. Step 2 now names every pin an added worker moves: in `rtl.yml`, the matrix, `total`, the `verilator-suites` verifier's `--expect` and the ownership arm; in `ci_events.py`, the canonical ownership script, the canonical verifier, and the self-test fixtures and expected findings that pin the Verilator count; in the selector, the landmark and one more overhead entry. Following the first wording, `ci_events.py --check` failed on `--expect`, and its self-test stopped on `fixture drift`. |

Item 3, in a disposable clone of `2c2f3369` with a planted `tb/verilator/zz_new_suite`:

| Stage | Result |
|---|---|
| planted, no figure | `--selftest` rc 1, naming the steps. `--shard 0/5 --list` rc 2. The real `scripts/run_all_suites.sh <out>` rc 2: `ABORTING: scripts/suite_shards.py fails its own self-test`. |
| step 1: `suite_timeout` has no arm for it, so 1800 s, marked provisional | `--selftest` rc 1. The provisional figure is accepted; workers 0-3 are at 4628-4730 s, over 4320 s. |
| step 2: one more worker (16 edits: 3 in `rtl.yml`, 11 in `ci_events.py`, 2 in the selector) | `--selftest` rc 0 (six workers: 3746, 3746, 3746, 3747, 3747 and 2877 s). `ci_events.py --check` rc 0, `--selftest` rc 0 (1822 items, 2530 arms). The six lists cover the 63-suite inventory once each, with 5/6 `milan_dp` alone. |
| serial preflight | rc 0: all eight preflight gates pass. |

The preflight was run through a copy of the driver whose last line, `main "$@"`, is replaced by `main`'s first five calls, ending at `run_preflight_gates`. The real driver would go on into the suites, which this lane does not run. Step 3 needs the change's own hosted run.

R626-2's residue R2 is fixed in this body: the "sharded selection" row above. R1 (the `rtl.yml:136-137` comment) stays routed to #495.

Mutation evidence at `2c2f3369` (all with CPython 3.12.3):

| Case | rc | Failing arm |
|---|---:|---|
| driver reader returns a mirrored 1800 s | 1 | the planted-`*` arm, the only failure |
| driver reader drops named arms | 1 | the planted-own-arm arm, the only failure |
| provisional figure never compared | 1 | the three figure arms |
| provisional name with no figure let through | 1 | the no-figure arm, the only failure |
| tree: `aaf` marked provisional at 73 s | 1 | `FAIL head: aaf: provisional figure 73 s is not the 1800 s that run_all_suites.sh's suite_timeout gives it` |
| tree: driver missing, an arm naming two suites, an arm after `*` | 1 each | `FAIL head` naming the cause |
| `in_checkout()` forced false (R626-1 `head-arms-skipped`) | 1 | `FAIL head: suite_shards.py would skip its head arms with ...` |
| tie-break by `hash(suite)` (R626-1 `nondeterministic-tie`, R626-2 `tie-by-hash`) | 1 | `FAIL the 5 --shard lists printed under hash seeds 1 and 2 are the ones selected here` |
| the head's call to `provisional_problems` replaced by `[]`, with `aaf` planted | 0 | none: see Known limitations |

R626-1's `mutate.py` and R626-2's `probe_727.py` build trees without `scripts/run_all_suites.sh`, so unmodified every case now fails closed with `FAIL head: [Errno 2] ...`. With one added line copying the driver into each tree, both match their round-2 results except the intended changes and one DRIFT:

- `head-arms-skipped` and `nondeterministic-tie` (`tie-by-hash`) now exit 1.
- R626-1's `missing-duration-free` reports DRIFT, because its replacement targets the old refusal text. R626-2's equivalent case edits the condition instead and still exits 1 with both arms `ESCAPED`.

## Authoritative references

- #727 acceptance 1-4 and the lane assignment (issue comment 6121794007); the round-2 and round-3 decisions (issue comments 6126048117 and 6126613714).
- `.github/workflows/rtl.yml` job `verilator-shards`: `timeout-minutes: 120`, `matrix.total: [5]`, step "Prove specialized suite ownership" (pinned by `scripts/ci_events.py` `CANONICAL_OWNERSHIP_SCRIPT`).
- #444 (dedicated `milan_dp` worker); #209 and #268 (worker count carried as `matrix.total`).
- `scripts/run_all_suites.sh` `suite_timeout` (the provisional figure) and `run_preflight_gates` (the serial preflight).
- `docs/testing/CI_WORKFLOWS.md`, Exhaustive validation; `docs/testing/TESTING.md`, the serial sweep.

## How to get into the same state

```sh
git fetch origin
git switch 727-shard-balance
git rev-parse HEAD
git diff --stat c6bd08c6 HEAD
```

`ci_events.py` needs PyYAML (`python3 -m pip install pyyaml`). The Markdown gates need the pinned renderer: `python3 -m pip install --require-hashes -r tools/markdown/requirements.txt`.

## How to validate

```sh
python3 scripts/suite_shards.py --selftest
for i in 0 1 2 3 4; do scripts/run_all_suites.sh --shard "$i/5" --list; done
scripts/run_all_suites.sh --list
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/test_suite_cancellation.py
python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
git diff --check c6bd08c6 HEAD
```

Expected result / pass criteria: every command exits 0. `--selftest` ends `selftest: PASS`. It prints `ok   head provisional figures {} ...`, five `ok head worker` lines (4204, 4205, 4203, 4205, 2877 s against 4320 s), the hash-seed line, and fifteen `[ok]` planted-defect lines. The five lists hold 15, 16, 14, 16 and 1 suites. Shard 4/5 is `milan_dp` alone, `tsn_fuzz` is in 1/5 and `chmap_capture` in 3/5. Their union equals the 62-suite `--list` inventory, with no suite twice.

To rerun the new-suite steps by hand, start from a disposable clone of this head, made from the checkout:

```sh
git clone . ../new-suite-copy
cd ../new-suite-copy
git checkout 2c2f336979e4fdb1da444f041f37551e2c9175df
mkdir tb/verilator/zz_new_suite
printf 'all:\n\t@echo planted\n' > tb/verilator/zz_new_suite/Makefile
python3 scripts/suite_shards.py --selftest
```

The self-test exits 1 and names the steps. Then follow the selector's docstring, steps 1 and 2. Afterwards `python3 scripts/suite_shards.py --selftest`, `python3 scripts/ci_events.py --check` and `python3 scripts/ci_events.py --selftest` exit 0.

To rerun a reviewer's mutation harness, its trees need `scripts/run_all_suites.sh` beside the selector and `rtl.yml`, because the self-test now reads it.

To check acceptance 3 once this PR's rtl-full run completes:

```sh
gh run list --workflow rtl.yml --branch 727-shard-balance --json databaseId,headSha,event,status,conclusion --limit 5
run=<databaseId of the pull_request run at the PR head>
gh run view "$run" --json headSha,jobs --jq '.headSha, (.jobs[] | select(.name | startswith("Verilator shard")) | "\(.name)\t\(.conclusion)\t\((.completedAt | fromdate) - (.startedAt | fromdate)) s")'
```

Every Verilator worker must take at most 4320 s.

| Worker | Predicted | Measured |
|---|---:|---:|
| 0/5 | 4204 s | pending |
| 1/5 | 4205 s | pending |
| 2/5 | 4203 s | pending |
| 3/5 | 4205 s | pending |
| 4/5 | 2877 s | pending |

## Known limitations / out of scope

- The table is one sample, as the assignment specifies. The balanced workers have 115-117 s spare (2.7% of the bound), and a slow runner class can push a worker past 72 min while it stays far under the 120-minute timeout. If that happens, refresh the table from that run (docstring procedure) rather than change the rule.
- `rtl.yml:136-137`'s comment still says "four hashed workers". Acceptance 2 keeps `rtl.yml` unchanged when five workers meet the bound, and the round-2 decision sends the comment to #495.
- The head arms skip only for a renamed copy with none of `rtl.yml`, the inventory and the driver beside it, which is how `test_suite_cancellation.py` runs one. In a checkout, a missing `rtl.yml`, suite root or driver fails closed.
- Deleting the head's call to `provisional_problems` is not caught, as deleting any arm is not. The function it calls is covered by four planted arms. `PROVISIONAL_SUITES` is empty at this head.
- Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build. A cache miss lengthens that worker's setup.
- Until #696 merges, a refresh must keep `"maap": 1375` (the docstring says so).
- A new suite directory needs a recorded duration before any sharded selection or `--selftest` passes, including the local sweep's preflight. That is acceptance 1's fail-closed case. The selector's docstring gives the steps that cure it: a provisional figure from `suite_timeout`, a worker added if needed, and the figure replaced from the change's own hosted run.
- Owed before this PR is marked validated (CONTRIBUTING section 2): the local serial `scripts/run_all_suites.sh` sweep and `syn/yosys/run.sh`, plus the `act` replica of this PR head. None of them was run in this lane.
- No suite, testbench, RTL, firmware or workflow file changes.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (1, 2 and 4 locally; 3 waits for the hosted run)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the touched gates pass; the serial sweep and Yosys run are owed)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
