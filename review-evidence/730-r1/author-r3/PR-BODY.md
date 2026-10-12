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

GREEN: `act_ci.py --selftest` 497/497 arms; every gate below rc 0 at `5c6f489a`.
`730-act-cpusets` -> `dev`.

## Linked Issue / roles

Relates to #730

Acceptance 1 and 2 are met. Acceptance 3 is met except its "verdict unchanged on the same
head" clause; 4 and 5 are not done here. By the ruling on #730 there are no replays in this
lane, and the manager measures after the merge. So this PR does not close the Issue.

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
| Derivation | `job_container_width` and `replay_container_concurrency` (`scripts/act_ci.py`). A matrix job runs its literal `max-parallel` containers at once, or act's default 4 when it names none. A job without a matrix runs one. A workflow's concurrency is its `CONCURRENT_JOB_LIMIT` widest jobs added up. An unreadable `max-parallel` is a Refusal. Shipping `rtl-full` derives 4; `docs`, `elaborate` and `rtl-fast` derive 1. |
| Layout | `slot_cpu_base`, `container_cpuset` and `job_cpu_ranges`. Slot N owns CPUs `20N..20N+19`: a staging range, then `SLOT_JOB_RANGES` job ranges. `SLOT_JOB_RANGES` is `CONCURRENT_JOB_LIMIT` x act's default width, which is 4, and each range is `CONTAINER_CPU_LIMIT` (4) wide. Slot 0 stages on `0-3` and uses `4-7`, `8-11`, `12-15` and `16-19`. Slot 3 stages on `60-63` and uses `64-67` to `76-79`. A run uses only the ranges it derives, and a run that derives more than 4 is refused. A host without the CPUs for the ranges a run derives refuses the run before the slot is entered, on every slot, slot 0 included: 20 CPUs for `rtl-full` on slot 0, and 8 for a workflow that derives one container. |
| Placement | `JobCpuRanges` and `job_cpu_range_monitor`. While act runs, a `docker events` stream filtered to the run's ownership label runs in its own session. At each job container's `create`, the monitor reserves the lowest free job range and moves the container there with `docker container update --cpuset-cpus`. A reservation lasts until the container's `destroy`, or until `docker container inspect` shows the daemon no longer has it. A `die` frees nothing, because a stopped container keeps its cpuset and can start again. A move that failed or timed out keeps its range reserved, because the daemon may have applied it or may still. Where a container runs is read with `docker container inspect`, never inferred from events: after each move, at each `start`, at an `update` of a container not yet seen on its range, and for every holder when no range is free. |
| Shutdown | On every exit the stream's process group is walked down the containment ladder, and the reader is joined and proven ended before the Docker boundary's teardown. A failed poll, containment, leader reap, join or pipe close does not skip any later step. Only then is a failure surfaced, and the first one wins. An interrupt or failure already unwinding through the monitor keeps going, with its exit status and diagnostic, and each cleanup failure is printed beside it (`act-ci: CPU-range monitor cleanup also failed: ...`). With no earlier failure the first cleanup failure is raised. A reader still running after its bounded wait is printed as a containment hold, and teardown waits for it. |
| Reporting | Before the boundary, the run prints its plan (below). After each workflow it prints `CPU ranges: <n> job container(s) created: <m> seen on a range of their own by docker inspect, <g> removed before that, <s> never seen on one; at most <k> held a range at once`. Each problem is a separate warning line. A container left on the staging range never changes a verdict: it keeps `nproc` 4. |
| Interrupt gate | `--interrupt-selftest` runs its job under the monitor and requires the job's container to be seen on a range of its own. |
| Unchanged | No workflow, step, job, suite, RTL or firmware file. Unchanged: `--memory=16g --memory-swap=16g`, `--concurrent-jobs 1`, the 24G slot cap, the ownership label, leases, cleanup and every existing Refusal. |
| Docs | `docs/testing/CI_WORKFLOWS.md`: replica shape, reservations, slot resource bounds (including mixed runner versions), the interrupt gate, and the self-test lists. |

Dry run of the shipping `rtl-full` (the real dry-run code path with GitHub, git, the slot daemon
and the Docker boundary stood in; the same lines are a self-test arm):

```text
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71 --cpuset-cpus=72-75 --cpuset-cpus=76-79
```

The first line is slot 0 and the second is slot 3.

Disjointness proof (`selftest_cpu_layout_disjoint`): every slot from 0 to 63 runs 4 job
containers at once, giving 320 ranges, each 4 wide, with no shared CPU. It fails on two planted
overlaps:

- across slots, the pre-#730 `slot * 4` spacing (`slot 0 job range 0 and slot 1 staging share
  CPU 4`);
- within a slot, every leg on one range.

A staging range planted onto a job range is refused at run time.

### Round 2 (answers R633-1 and R632-1)

| Finding | Fix | Standing self-test |
| --- | --- | --- |
| R633-1-F1: `die` freed a range a stopped container keeps | Reservation until `destroy` or an inspect proving the container gone; placement read by inspect | `selftest_job_cpu_record` runs R633-1's sequence `create A, update A, start A, die A, create B, update B, start B, start A` against a model daemon that holds each container's real cpuset. After every event, no two containers share a range, and every container on a job range holds it in the record. |
| R633-1-F2: a failed or timed-out update freed its target | The target is reserved before the update and stays reserved whatever the command reports. Only the daemon's `No such container` frees it. | `selftest_job_cpu_move_failures` covers four cases, each with the next container created while the outcome is uncertain: applied then CLI timeout (R633-1's probe); lost then landing late; move and read both timing out; refused. Every warning text is pinned. |
| R633-1-F3: slot 0 fell back silently | Slot 0 refuses like every slot | `selftest_job_cpu_ranges` checks slot 0 at 1, 3, 4, 7, 8, 19, 20 and 21 CPUs for one and four containers. |
| R633-1-F4, R632-1-F1: a reap failure skipped the join; no arm saw a missing join | Each shutdown step runs whatever an earlier one raised; the join is retried until the reader is proven ended | `selftest_job_cpu_monitor_busy`: the reader is still moving a container when the body returns, and the stream ends only once contained. It runs for return, raise, SIGTERM, reap failure, and raise plus reap failure. Also covered: poll and join failures, and start failures. |
| R632-1-F2: verdict invariance not pinned at run level | No runtime change | `selftest_cpu_range_warnings` drives `execute_workflows` with a container left on staging and two problems. With act exit 0 the verdict is `PASS`; with exit 3 it is `FAILED (3)`. Each workflow prints its summary once and exactly one warning per problem. |
| R632-1-R1, R2 | The mixed-runner-version sentence is in the authoritative doc, and the slot-0 sentence above is replaced | Docs gates |

Also fixed while checking item 3: three self-test harnesses called `run_validation` with the
host's real CPU count. The hosted `docs` job runs the self-test on a 4-vCPU runner, so those
harnesses would have refused there. They now pin 128 CPUs. The self-test passes with 1, 2, 3, 4,
7, 8, 19, 20, 39, 40 and 128 simulated CPUs.

Mutation evidence at `5ba8313a`, on scratch copies of the tree, where each mutant must fail the
self-test:

- 21 of 21 Round 2 mutants are killed. They cover every fix above, plus the harness pin, the
  planted exit, and the held-range check.
- R632-1's own campaign, re-run here: 19 killed, including M13, M16, M17 and M23. M18 survives;
  it is pinned only by the live interrupt gate. Four mutants no longer apply, because their
  anchors were removed by this round: `die` freeing, the slot-0 fallback, and the old held-range
  line, now N21.

Material decision: an uncertain move keeps its range until the container is removed, even after
an inspect shows the container still on the staging range. The daemon may still apply the timed-out
request, and releasing the range would let that late completion land on a range already given to
the next container. The cost is one idle range for that container's life, reported as a warning.

### Round 3 (answers R633-2 and R632-2)

| Finding | Fix | Standing self-test |
| --- | --- | --- |
| R633-2-F1: a failed monitor cleanup replaced an interrupt already unwinding (SIGTERM exited 2, not 143, and its diagnostic was lost) | `job_cpu_range_monitor` keeps the failure already propagating and hands it to `stop_job_cpu_range_monitor` as `primary`. Every containment, join and close step still runs first. With a `primary`, stop raises nothing, so the interrupt or body failure keeps propagating unchanged, and each cleanup failure is printed beside it. With none, the first cleanup failure is raised as before, and each later one is printed. | `selftest_job_cpu_monitor_busy`: a real SIGINT, SIGTERM and SIGHUP, each delivered to the runner's own handler and followed by a failed reap, exit 130, 143 and 129 with `act-ci: interrupted by SIG... after cleanup`, the reap failure printed beside it, the busy reader joined, the stream contained and the pipe closed. A body failure plus a failed reap raises the body's failure. A reap failure alone still raises the reap failure, with nothing printed beside it. |
| R632-2-F1 (a), K12: the join-retry arm could not fail | The stand-in reader now runs until the join is retried, so it is still running after the pause that follows the failed join. | `selftest_job_cpu_monitor_shutdown`: the join failure is raised only once the reader has ended. |
| R632-2-F1 (b), K13: no arm reached the containment hold | The bounded wait is patched to 0.05 s and the reader runs until the hold line has been printed. | The hold is printed and recorded, and the join returns only after the reader has ended. |
| R632-2-F1 (c), K36: no arm combined two cleanup failures | A reap failure plus a join failure. | With no earlier failure, the reap failure is raised and the join failure printed beside it. With an interrupt already propagating, nothing is raised and both are printed, in order. |
| R632-2-F1 (d), K32: `--since` was never pinned | `time.time` is stubbed to `1700000000.75`. | The stream command reads `events --since 1699999999`. |
| R632-2-S1 (optional): the containment mask and the reader-crash problem were not pinned | Taken: test only. | Containment runs with INT, TERM and HUP blocked, and a reader whose read fails records a problem. |

R632-2's `mutants_r2.py`, unchanged, run on a `git archive` of this round's code commit inside
its own sandbox script: 36 mutants, 36 killed, among them K12, K13, K32 and K36, and K29 and K31.
`act_ci.py` is the same blob at the head. Its `probe_shutdown.py`, unchanged, passes S1 to S4.
This round's own mutants (scratch copies; each must fail the self-test) are 8 of 8 killed: the
`primary` not passed or ignored; cleanup failures not printed, or the raised one printed too;
only a signal kept, or a signal not kept; the hold not printed, or not recorded. The 21 Round 2
mutants are still all killed.

Changes to existing arms: the body-plus-reap arm now expects the body's failure, as item 1
requires. The SIGTERM arm now delivers a real signal and checks exit 143 and its diagnostic. The
monitor harness runs under the runner's own signal handlers and keeps what went to stderr.

Not taken (optional): R632-2-S2, a first signal landing in the generator's `finally` before the
mask is set. The window is a few bytecodes, and `replay_slot` and `run_act_process` share it, so
it belongs to its own Issue. R632-2-S3, the hold wording after a failed join: R632-2's own probe
pins the current text, and the hold itself is accurate, since teardown waits.

## Authoritative references

- #730 acceptance 1-5.
  - Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752
  - Ruling: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815
  - Round 2: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197
  - Round 3: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921
- Reviews R633-1 (https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6132335284)
  and R632-1 (https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6132397037).
- Reviews R633-2 (https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133015754)
  and R632-2 (https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133143865).
- #532 (replay slots); `docs/testing/CI_WORKFLOWS.md` "Act-first local replication" and
  "Parallel replay slots".
- act 0.2.89:
  - `pkg/runner/runner.go`: per-job `NewParallelExecutor(maxParallel)` inside
    `NewParallelExecutor(ConcurrentJobs)`.
  - `pkg/model/workflow.go`: `GetMaxParallel` defaults to 4.
  - `pkg/runner/job_executor.go`: under `--rm`, each leg's container is removed before the
    worker takes the next leg.
- moby `daemon/update.go`: an update persists in a stopped container's configuration, and is
  applied before the response returns.

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

Expected result / pass criteria: every command exits 0.

- The runner self-test ends `selftest: PASS`, with 497 `ok` arms and no `FAIL`.
- The CI contract reports 2016 items OK.
- The slot-proof self-test passes its 44 cases.
- The idiom ratchets hold: long function 9 <= 9, too many parameters 7 <= 7, over-long line 0.
- The em-dash gate reports 0 findings over 133 added lines.

Recorded with CPython 3.12.3 and PyYAML 6.0.3. The self-test also passes on CPython 3.14.7,
with 1, 4, 8, 19, 20 and 128 simulated CPUs, and in 10 concurrent runs.

R632-2's mutant campaign, from the `730-review-evidence` branch, on an extracted tree:

```sh
python3 -I mutants_r2.py <packet-dir> <extracted-tree> --jobs 12
```

Expected: `mutants: 36, killed 36, survived [], bad anchors []`.

Post-merge measurement (acceptance 4, by the manager, per the ruling): the first `rtl-full`
replay on the merged runner, in the form of the recorded slot-0 replays (#721 at `42678ae2`,
#715 at `c7d0ad63`):

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Read these lines:

1. The plan line above.
2. Per-job wall clock, from `[rtl-full/<job>] ⭐ Run Set up job` to
   `[rtl-full/<job>] 🏁  Job succeeded` (or `Job failed`). This needs per-line stamps, which act
   does not add.
3. `act-ci: rtl-full: CPU ranges: <n> job container(s) created: <m> seen on a range of their own
   by docker inspect, <g> removed before that, <s> never seen on one; at most <k> held a range at
   once`. Expect `m == n` (12 when the gate selects the full run), `g == 0`, `s == 0` and
   `k == 4`, with no `act-ci: WARNING: rtl-full: CPU ranges:` line.
4. The verdict, `act-ci: rtl-full: PASS at <sha>` or `FAILED (<rc>)`, against the before verdict
   at the same head.
5. On an isolated slot only, `act-ci: slot N: memory peak <x> GiB of its 24G cap; the cap was hit
   <h> time(s), with no OOM at it`.

## Known limitations / out of scope

- Not exercised against a live daemon in this lane: no replay, and no live self-test (ruling).
  No `docker events`, `docker container update` or `docker container inspect` has run. The first
  live run is the post-merge measurement, or `--interrupt-selftest` on slot 0 if the manager
  allows it before merge.
- The interrupt gate's requirement that its container be moved (R632-1's M18) is pinned only by
  that live gate.
- A first signal that lands in the monitor's `finally` before the cleanup mask is set skips
  the monitor's containment (R632-2-S2, optional). The window is a few bytecodes and is shared
  with `replay_slot` and `run_act_process`, so it is left to its own Issue.
- `--dry-run` is not daemon-free. In an isolated slot it starts the slot daemon and seeds the
  tool cache, which pulls the runner image. On slot 0 it creates the boundary on the default
  daemon. The dry-run lines above therefore come from the offline harness. Making `--dry-run`
  daemon-free is a separate change.
- A slot needs 20 CPUs where it needed 4. On a 128-CPU host, slots 1-5 fit any shipping
  workflow, and slot 6 fits workflows that derive one container. A host with fewer than 8 CPUs
  can no longer replay at all, slot 0 included (acceptance 1).
- A slot run by a pre-#730 runner can share CPUs with one run by this runner. Run every slot
  from one runner version.
- A container runs on its slot's staging range between its `create` and its move. `nproc`
  is 4 there too. Each container costs two more `docker container inspect` calls (after the
  move, and at `start`), so a burst of four creates is moved a little later than before. This is
  not measured.
- A move that cannot be confirmed keeps its range until the container is removed. With every
  range held, a further container stays on the staging range, as a warning.
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
