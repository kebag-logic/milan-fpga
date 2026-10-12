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

REVIEW READY at `a57d384dc697249c2a69f80079b676875d4f7560`: every local gate this change touches is rc 0, and 19 mutation and planting cases behave as recorded. Acceptance 3 (measured at most 72 min per worker) waits for this PR's hosted run. `727-shard-balance` -> `dev`.

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
| sharded selection | Refuses an inventory suite with no duration and a duration with no inventory suite (exit 2). The serial `0/1` sweep needs no table and is unchanged. |
| `--selftest` | Holds the head's table to its inventory and to 60% of the Verilator job's `timeout-minutes`, read with the worker count from `rtl.yml`. Plants each defect: a missing duration, a stale duration, a tighter `rtl.yml` timeout, and heavy durations (at the bound passes, one second over fails, a pigeonhole growth fails). Planting each specialized suite at its lightest and heaviest proves the pins hold. |
| `--measure LOG...` | Prints both tables from `gh run view --log` worker logs; the docstring's refresh procedure uses it. |
| `docs/testing/CI_WORKFLOWS.md` | The worker paragraph and the #621 history line now describe the measured-time split, not the hash. |

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

## Authoritative references

- #727 acceptance 1-4 and the lane assignment (issue comment 6121794007).
- `.github/workflows/rtl.yml` job `verilator-shards`: `timeout-minutes: 120`, `matrix.total: [5]`, step "Prove specialized suite ownership" (pinned by `scripts/ci_events.py` `CANONICAL_OWNERSHIP_SCRIPT`).
- #444 (dedicated `milan_dp` worker); #209 and #268 (worker count carried as `matrix.total`).
- `docs/testing/CI_WORKFLOWS.md`, Exhaustive validation.

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

Expected result / pass criteria: every command exits 0. `--selftest` ends `selftest: PASS`, prints five `ok head worker` lines (4204, 4205, 4203, 4205, 2877 s against 4320 s), and prints eight `[ok]` planted-defect lines. The five lists hold 15, 16, 14, 16 and 1 suites. Shard 4/5 is `milan_dp` alone, `tsn_fuzz` is in 1/5 and `chmap_capture` in 3/5. Their union equals the 62-suite `--list` inventory, with no suite twice.

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
- `rtl.yml:136-140`'s comment still says "four hashed workers". Acceptance 2 keeps `rtl.yml` unchanged when five workers meet the bound, so the comment is left for a follow-up or a decision.
- The head arms skip only when the file runs as a renamed copy outside a checkout: `test_suite_cancellation.py` runs one with no inventory or `rtl.yml` beside it. In a checkout, a missing `rtl.yml` or suite root fails closed.
- Overheads assume warm Verilator, Yosys and tsn-gen caches; a cache miss lengthens that worker's setup.
- Until #696 merges, a refresh must keep `"maap": 1375` (the docstring says so).
- A new suite directory needs a recorded duration before any sharded selection or `--selftest` passes, including the local sweep's preflight. That is acceptance 1's fail-closed case.
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
