[A671]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED, awaiting a ruling. No commit: `781-media-phase-hosted-budget` -> `dev` is still at dev
`a032c6d6`. No budget that fits the hosted runner with margin fits any worker's bound without a
workflow change. The assignment reserves that change for the coordinating role. This body records the
measurement for that ruling. Do not open a PR from it until a change exists.

## Linked Issue / roles

Relates to #781

Executor: `[A671]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

No file is changed. The measurement behind the blocked budget:

| Source | `media_phase` window |
|---|---|
| Hosted, run 40098975073 attempt 1, job 120887850753 | TIMEOUT at 900.0 s (job 1744 s) |
| Hosted, run 40098975073 attempt 2, job 120934873499 | TIMEOUT at 900.0 s (job 1725 s) |
| Hosted, run 40103838859, job 120902541972 | TIMEOUT at 900.0 s (job 1868 s) |
| Local, serial, uncontended, 4 CPUs (2 cores x 2 SMT), pinned Verilator 5.050, CASE_JOBS 3 | 787.5 s and 769.3 s PASS, 386 checks |
| Local, same, CASE_JOBS 4 | 725.4 s PASS, 386 checks |

Every hosted artifact log ends in the loop cases (`make: *** [Makefile:160: cases] Terminated`), so
the hosted figure is a lower bound. Hosted/local ratios from the same jobs' other suites are
`milan_dp__3` 1.074–1.272 and `pp_shadow__3` 1.320–1.575. They project a hosted window between 900 s
and about 1240 s.

The fit, from `scripts/suite_shards.py`'s own `headroom_problems` and `balance`:

- 16 workers (the head): the largest accepted figure is 936 s. Balanced demand is 24098 s against
  15 x 1620 = 24300 s.
- The default 1800 s fits no regular worker: 1800 + 122 s setup = 1922 s, over the 1620 s bound. No
  regular worker can take a figure above 1498 s.
- 1364 s (the projection plus the 10% margin #673 used) exceeds the 16-worker capacity by 262 s.
- A 17th worker at 45 minutes accepts up to 1498 s.

## Authoritative references

- #781 and its assignment comment
- `scripts/suite_shards.py` module docstring (new-suite steps), `SUITE_SECONDS`, `PROVISIONAL_SUITES`,
  `WORKER_OVERHEAD_SECONDS`, `headroom_problems`
- `scripts/run_all_suites.sh` `suite_timeout`
- `.github/workflows/rtl.yml` `verilator-shards` `timeout-minutes: ${{ matrix.shard == 15 && 60 || 45 }}`
- `docs/testing/CI_WORKFLOWS.md` (the per-suite budget table, the #673 envelope rule, the #737
  dedicated-worker exception)

## How to get into the same state

```sh
git fetch origin dev
git checkout -b 781-media-phase-hosted-budget a032c6d6e3775f145349d5a495c1e1ad12294936
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
```

## How to validate

```sh
python3 scripts/suite_shards.py --selftest
CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS="-j1 --no-print-directory" SUITE_TIMEOUT=3600 taskset -c 0-3 scripts/run_all_suites.sh shard10-logs --ci-pieces --shard 10/16
```

Expected result / pass criteria: the self-test passes at the head. The shard 10/16 replica passes 4/4,
and `media_phase` reports 386 checks with 0 failures in roughly 13 minutes on two SMT cores.

## Known limitations / out of scope

- `media_phase` stays at its provisional 900 s, and in `PROVISIONAL_SUITES`, until the ruling.
- I have not changed any workflow `timeout-minutes`, the worker count, or the 1620 s rule.
- Shard 10's `milan_dp__3` and `pp_shadow__3` run over their registered piece figures on hosted
  (231 s registered vs 354–419 s; 347 s vs 378–451 s). That table refresh belongs in a separate Issue.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
