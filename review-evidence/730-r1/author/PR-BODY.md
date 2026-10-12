[A607]

## Contents

- **[Status](#status)**: Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)**: Public task, executor, and independent reviewers.
- **[Description](#description)**: What changed and why.
- **[Authoritative references](#authoritative-references)**: Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)**: Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)**: The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN: `act_ci.py --selftest` 477/477 arms; every gate below rc 0 at `eb566634`.
`730-act-cpusets` -> `dev`.

## Linked Issue / roles

Relates to #730

Acceptance 1 and 2 are met. Acceptance 3 is met except its "verdict unchanged on the same
head" clause, and 4 and 5 are not done here. By the ruling on #730 there are no replays in
this lane, and the manager measures after the merge. So this PR does not close the Issue.

Executor: `[A607]`
Internal cleared-context reviewer: `[R632]`
External reviewer: `[R633]`

## Description

act 0.2.89 gives every job container of a run one `--container-options` word. A replay
therefore put all of a matrix job's concurrent legs on the same four CPUs (`0-3` on slot 0,
`4N..4N+3` on slot N), a quarter of a hosted runner each. An interrupted `rtl-full` replay
on slot 3 showed four Verilator legs, every one with `cpuset.cpus` `12-15`, using about 1 CPU
each.

| Piece | Change |
| --- | --- |
| Derivation | `job_container_width` and `replay_container_concurrency` (`scripts/act_ci.py`). A matrix job runs its literal `max-parallel` containers at once (act's default 4 when it names none), and a job without a matrix runs one. A workflow's concurrency is its `CONCURRENT_JOB_LIMIT` widest jobs added up. An unreadable `max-parallel` is a Refusal. Shipping `rtl-full` derives 4; `docs`, `elaborate` and `rtl-fast` derive 1. |
| Layout | `slot_cpu_base`, `container_cpuset` and `job_cpu_ranges`. Slot N owns CPUs `20N..20N+19`: a staging range, then `SLOT_JOB_RANGES` (= `CONCURRENT_JOB_LIMIT` x act's default width = 4) job ranges, each `CONTAINER_CPU_LIMIT` (4) wide. Slot 0 stages on `0-3` and uses `4-7`, `8-11`, `12-15` and `16-19`; slot 3 stages on `60-63` and uses `64-67` to `76-79`. A run uses only the ranges it derives. A run that derives more than 4 is refused. An isolated slot without the CPUs is refused before the slot is entered. Slot 0 on a host under 20 CPUs keeps its legs on `0-3`, as before, and prints that. |
| Placement | `JobCpuRanges` and `job_cpu_range_monitor`. While act runs, a `docker events` stream filtered to the run's ownership label runs in its own session. At each job container's `create`, the monitor moves it with `docker container update --cpuset-cpus` to the lowest free job range; `die`/`destroy` frees the range. On every exit the stream is walked down the containment ladder and its reader joined before the Docker boundary's teardown. A container left on the staging range is printed as a warning and never changes a verdict: it keeps `nproc` 4. |
| Reporting | Before the boundary, the run prints its plan (below). After each workflow it prints the containers created and moved, the most at once, and how many started on the staging range before the move. |
| Interrupt gate | `--interrupt-selftest` runs its job under the monitor and requires the job's container to have been moved. |
| Unchanged | No workflow, step, job, suite, RTL or firmware file. `--memory=16g --memory-swap=16g`, `--concurrent-jobs 1`, the 24G slot cap, the ownership label, leases, cleanup and every existing Refusal. |
| Docs | `docs/testing/CI_WORKFLOWS.md`: replica shape, slot resource bounds, the interrupt gate, and the self-test lists. |

Dry run of the shipping `rtl-full` (the real dry-run code path with GitHub, git, the slot daemon
and the Docker boundary stood in; the same lines are a self-test arm):

```text
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71 --cpuset-cpus=72-75 --cpuset-cpus=76-79
```

The first line is slot 0 and the second is slot 3.

Disjointness proof (`selftest_cpu_layout_disjoint`): every slot from 0 to 63 runs 4 job
containers at once, giving 320 ranges, each 4 wide, with no shared CPU. It fails on two planted
overlaps: the pre-#730 `slot * 4` spacing across slots (`slot 0 job range 0 and slot 1 staging
share CPU 4`), and every leg on one range within a slot. A staging range planted onto a job
range is refused at run time. Ten scratch mutants of the runner (old spacing, one shared
range, `max-parallel` or `CONCURRENT_JOB_LIMIT` ignored, no free on `die`, monitor not stopped
on a raise, act outside the monitor, guard removed, plan line without ranges, no label
filter) each fail the self-test.

## Authoritative references

- #730 acceptance 1-5. Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752. Ruling: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815.
- #532 (replay slots), `docs/testing/CI_WORKFLOWS.md` "Act-first local replication" and "Parallel replay slots".
- act 0.2.89: `pkg/runner/runner.go` (per-job `NewParallelExecutor(maxParallel)` inside `NewParallelExecutor(ConcurrentJobs)`), `pkg/model/workflow.go` (`GetMaxParallel` default 4), `pkg/runner/job_executor.go` (per-leg container removal under `--rm`).

## How to get into the same state

```sh
git fetch origin
git switch 730-act-cpusets
git log --oneline dc4d06cb..HEAD
python3 -m pip install pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/act_ci.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
scripts/act_slot_proof.sh --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base dc4d06cb
python3 scripts/check_doc_paths.py
git diff --check dc4d06cb HEAD
```

Expected result / pass criteria: every command exits 0. The runner self-test ends
`selftest: PASS` with 477 `ok` arms and no `FAIL`. The CI contract reports 2016 items OK. The
slot-proof self-test passes its 44 cases, and the idiom ratchets hold with 0 over-long lines.
Recorded with CPython 3.12.3 and PyYAML 6.0.3.

Post-merge measurement (acceptance 4, by the manager, per the ruling): the first `rtl-full`
replay on the merged runner, in the form of the recorded slot-0 replays (#721 at `42678ae2`,
#715 at `c7d0ad63`):

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Read: the plan line above. Per-job wall clock runs from `[rtl-full/<job>] ⭐ Run Set up job` to
`[rtl-full/<job>] 🏁  Job succeeded` (or `Job failed`); this needs per-line stamps, which act
does not add. Next comes `act-ci: rtl-full: CPU ranges: <n> job container(s) created, <m> moved
to a range of their own, at most <k> at once; ...`: expect `m == n` (12 when the gate selects
the full run) and `k == 4`, with no `act-ci: WARNING: rtl-full: CPU ranges:` line. Then the
verdict `act-ci: rtl-full: PASS at <sha>` or `FAILED (<rc>)`, against the before verdict at the
same head. On an isolated slot only, read `act-ci: slot N: memory peak <x> GiB of its 24G cap;
the cap was hit <h> time(s), with no OOM at it`.

## Known limitations / out of scope

- Not exercised against a live daemon in this lane: no replay, and no live self-test (ruling).
  The first live run is the post-merge measurement, or `--interrupt-selftest` on slot 0 if the
  manager allows it before merge.
- `--dry-run` is not daemon-free. In an isolated slot it starts the slot daemon and seeds the
  tool cache, which pulls the runner image. On slot 0 it creates the boundary on the default
  daemon. The dry-run lines above therefore come from the offline harness. Making `--dry-run`
  daemon-free is a separate change.
- A slot needs 20 CPUs where it needed 4. On a 128-CPU host, slots 1-5 fit any shipping
  workflow, and slot 6 fits workflows that derive one container.
- A slot run by a pre-#730 runner can share CPUs with one run by this runner. Run every slot
  from one runner version.
- A container runs on its slot's staging range between its `create` and its move. `nproc`
  is 4 there too.
- A workflow deriving more than 4 concurrent containers, or with an unreadable `max-parallel`,
  is refused. No shipping workflow does either.
- Acceptance 5 (`CONCURRENT_JOB_LIMIT` 2) is deferred to the post-merge measurement (ruling).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (1 and 2 met; 3's verdict clause, 4 and 5 after the merge per the ruling)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
