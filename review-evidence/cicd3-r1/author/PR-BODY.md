[A839]

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

`cicd-3` -> `dev`, three commits stacked on PR #1001 (`cicd-verilator-perf`, head `fcbc31f3`). Open it as a draft
until #1001 merges, then rebase it onto `dev`. Its diff against `fcbc31f3` is these three commits only. Local
gates are green at head `13e6d869` (list in How to validate). The full serial sweep was not run in this lane; the
candidate bank runs it.

## Linked Issue / roles

Relates to #998 (the CICD improvement lane). Stacked on #1001.

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Three measured CI levers. Each kept every verdict identical.

1. **`66b092e1` Preflight once per head.**
   - A `verilator-preflight` job ("Verilator preflight") runs the sweep's eight preflight self-tests once,
     through the new `scripts/run_all_suites.sh --preflight-only`, beside the 19 workers.
   - The workers run `--ci-pieces --no-preflight`. `--no-preflight` is refused without `--ci-pieces`, so the
     serial sweep, the physical leg and local runs keep their preflight.
   - `verilator-suites` needs the job, verifies its `suite-preflight` SHA record with `ci_events.py
     --require-target-sha --expect 1`, and is red unless the job's result is `success`.
   - The job is one of `ci-fail-fast`'s expected jobs, so a failing preflight also cancels the run. Required
     context names are unchanged, and the new job, like the workers, uses no token or secret.
   - Generated in `scripts/ci_suite_workflows.py`; the template and its contract are unchanged.
   - Measured on a hosted-shard replica of shard 9/19: the first suite started at +2 s instead of +535 s, with
     134 CPU-s less and the logs and receipts IDENTICAL.
   - Hosted: −76..−97 s per worker, ~−23 runner-minutes per run.
2. **`f6c11a25` Stable mutant staging.**
   - Every mutation driver (38) stages its planted RTL through `scripts/mutant_stage.py`:
     `$TMPDIR/milan-mutant-stage-<uid>/<prefix><slot>`, the same path in every run and from every checkout.
   - Slots are locked and emptied when taken, and a run that finds every slot held falls back to a random
     directory. `CCACHE_BASEDIR` sits at the stage root.
   - Verilator writes each source's path into the model's C++, so a warm ccache now answers the mutant model
     compiles: crf_rx 79/115 → 115/115 hits, −25 % CPU on a warm cache; avtp_rxmon depkt 37/48 → 48/48, −64 %.
   - Every mutant is still killed by the same named check (logs IDENTICAL).
   - This also explains round 2's "rx_filter `__ALL.cpp` never hits": it was `binding_mutant.py`'s random staging
     path, now 8/8.
3. **`13e6d869` Longest case first.**
   - `scripts/ci_make_cases.py` starts a piece's cases longest first by a measured cost table (`CASE_SECONDS`,
     milan_dp's 26 cases) and prints and records results in driver order.
   - milan_dp__0's aclk (1558 CPU-s, 46 % of the piece) was dealt 6th of 7 and now starts first; piece 1's
     render-mutants moves from last to first.
   - Measured milan_dp__0 through its driver: milan_dp__0 through its driver 3411.9 s → 2711.8 s wall (−20.5 %) at the same instructions. Receipts IDENTICAL.

## Authoritative references

- [CI_WORKFLOWS.md "Exhaustive validation"](../docs/testing/CI_WORKFLOWS.md#exhaustive-validation) and "Failure and cancellation semantics": the preflight job and its binding.
- [TESTING.md section 1](../docs/testing/TESTING.md#1-verilator-rtl-harnesses---tbverilator-the-live-regression): the two sweep modes, mutant staging, case start order.
- AGENTS.md section 5: the act-first rule (not run here; see limitations).

## How to get into the same state

```sh
git fetch origin cicd-3
git worktree add ../cicd-3-review origin/cicd-3
cd ../cicd-3-review
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
export VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory'
```

## How to validate

```sh
python3 scripts/ci_gate_workflows.py --check && python3 scripts/ci_events.py --check
python3 scripts/ci_gate_workflows_selftest.py && python3 scripts/ci_suite_pieces_selftest.py   # 6 preflight binding controls
python3 scripts/test_suite_cancellation.py          # adds the preflight-only / no-preflight controls
python3 scripts/ci_make_cases_selftest.py           # start-order controls, table names live cases
python3 scripts/mutant_stage.py --selftest          # 7 staging controls
( cd tb/verilator/gptp_shadow && python3 test_mutant_lifecycle.py )
python3 scripts/check_py_idiom.py && python3 scripts/ci_events.py --selftest
scripts/run_all_suites.sh /tmp/pre --preflight-only; echo $?    # 0, eight logs in /tmp/pre/preflight
scripts/run_all_suites.sh /tmp/x --no-preflight; echo $?        # 2: refused without --ci-pieces
```

Every command above exits 0 at `13e6d869` except the last, which exits 2 by design. Also green there:
`ci_case_receipts`, `ci_maap_cases`, `ci_capture_cases`, `ci_suite_collect`, `ci_fail_fast`,
`ci_runtime_evidence`, `ci_install_cache`, `ci_workflow_plan` and `ci_manifest` self-tests;
`generate_ci_evidence_pins --check`; `suite_shards --selftest`; the sh idiom, hygiene, naming, fail-fast,
test-evidence and TODO ratchets; doc paths, doc style, `docs_check`, archive, docs inventory, TOC and em-dash.

Mutant identity, for any driver (cold, then warm, then compare):

```sh
cd tb/verilator/crf_rx && OBJCACHE=ccache CCACHE_DIR=$(mktemp -d) sh -c 'python3 mutants.py > /tmp/c1; ccache -z; python3 mutants.py > /tmp/c2; ccache --print-stats | grep -E "^(direct_cache_hit|cache_miss)"'
```

The second run shows `direct_cache_hit 115` and `cache_miss 0`. Both logs are identical once the staging
directory's name is removed.

## Known limitations / out of scope

- Not run here: the act replay (it replays a pushed PR head, and this lane does not push) and the full serial
  sweep.
- `WORKER_OVERHEAD_SECONDS` (122 s, preflight included) is unchanged until a hosted run re-measures it.
- A harness compiled from the stage by its absolute checkout path still misses once per new checkout (crf_rx 15
  of 115, all harness compiles). Hosted checkouts are at a fixed path, so they do not.
- `CASE_SECONDS` is a local, one-core measurement; only its order is used, and a stale figure can only slow a
  piece.
- The CI tool inventory (red at the base, round 1) does not record the changed and new scripts.

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
