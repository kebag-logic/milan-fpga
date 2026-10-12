# Lane 730: handoff ([A607])

Status: REVIEW READY at `eb5666349fc20ed3b5437a4357ef097c1231e557` (not pushed; push and PR
creation are outside this lane). Issue #730. Posted:
https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132134158

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131500852
- Ruling (no replays in this lane; measurement after the merge):
  https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815
- Branch `730-act-cpusets` from dev `dc4d06cb`; origin
  `https://github.com/kebag-logic/milan-fpga.git` confirmed; committer identity unchanged.
- Commits (one-line, no body, no trailers):
  - `7bb36e09` Give each concurrent act job container its own CPU range, derived from
    max-parallel and CONCURRENT_JOB_LIMIT (#730)
  - `eb566634` Document the per-container CPU ranges of act replays and their derivation (#730)
- Files (`git diff --stat dc4d06cb HEAD`): `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md`,
  1062 insertions, 66 deletions.
  No workflow, suite, testbench, RTL or firmware file touched.
- `PR-BODY.md` beside this file; receipts in `receipts/`.

## Resume note

The 22:10 stop left uncommitted `scripts/act_ci.py` edits: the derivation, the range layout,
the event monitor and its wiring. They were reviewed against act 0.2.89's source and kept.
Missing at resume and added here: every new self-test arm, the update of the existing slot
arms to the new layout (`--selftest` crashed at resume: slot 1 was refused on the 8-CPU mock
host), two over-long lines (Rule 12), the dry-run arm, and the documentation.

## How it works

act 0.2.89 passes one `--container-options` word to every job container
(`pkg/runner/run_context.go` `rc.options`), so no act option gives two legs different CPUs.
The word's cpuset becomes a staging range. While act runs, the runner streams
`docker events` filtered to its own ownership label and moves each job container, at its
`create`, to the lowest free job range with `docker container update --cpuset-cpus`. A
`die`/`destroy` event frees the range. act runs with `--rm`, so each leg's container is removed
before its worker takes the next leg (`pkg/runner/job_executor.go`, stop container
executor), and `die` precedes the next `create` in the daemon's order. Service containers and
Docker actions also carry the options word, but the sandbox already refuses both
(`validate_workflow_sandbox`), so only job containers carry the label. The slot slice sets only
`MemoryMax` (no `AllowedCPUs`), so a move out of the staging range is permitted.

## Changes (file:line at `eb566634`)

| Where | What |
| --- | --- |
| `scripts/act_ci.py:122` | `ACT_DEFAULT_MAX_PARALLEL = 4`: act 0.2.89's own default (`pkg/model/workflow.go` `GetMaxParallel`) |
| `scripts/act_ci.py:129` | `SLOT_JOB_RANGES = CONCURRENT_JOB_LIMIT * ACT_DEFAULT_MAX_PARALLEL`: job ranges a slot is spaced for |
| `scripts/act_ci.py:134` | `JOB_CPU_RANGE_EVENTS`: the five container events the monitor reads |
| `scripts/act_ci.py:2041` | `job_container_width`: 1 without a matrix; else literal `max-parallel` (min 1) or 4; unreadable is a Refusal |
| `scripts/act_ci.py:2070` | `replay_container_concurrency`: per workflow, the `CONCURRENT_JOB_LIMIT` widest jobs summed; max over workflows |
| `scripts/act_ci.py:4602` | the slot banner says "staging CPUs" |
| `scripts/act_ci.py:4622` | `slot_cpu_base`: slot N's block starts at `N * 5 * 4 = 20N` |
| `scripts/act_ci.py:4631` | `container_cpuset`: the staging range (slot 0 unchanged; slot N `20N..20N+3`) |
| `scripts/act_ci.py:4655` | `cpu_range_overlaps`: the overlap finder used by the guard and the proof |
| `scripts/act_ci.py:4669` | `job_cpu_ranges`: the derived job ranges; >4 or <1 refused; isolated slot on a small host refused; slot 0 falls back to `()` |
| `scripts/act_ci.py:4711` | `describe_job_cpu_ranges`: the printed plan line |
| `scripts/act_ci.py:5306` | `JobCpuRanges`: event parsing, placement, freeing, counters, problems |
| `scripts/act_ci.py:5417-5533` | `read_job_cpu_events`, `stop_job_cpu_range_monitor`, `job_cpu_range_monitor`: own session, containment ladder and join before Docker teardown on every exit |
| `scripts/act_ci.py:5535` | `report_job_cpu_ranges`: summary line; problems as warnings, never a verdict |
| `scripts/act_ci.py:5563` | `WorkflowPlan.cpu_ranges` |
| `scripts/act_ci.py:5624` | `execute_workflows`: act runs inside the monitor |
| `scripts/act_ci.py:5682-5683, 5710` | `run_validation`: derive and allocate before the slot is entered; print the plan |
| `scripts/act_ci.py:14389-14398` | interrupt probe: runs under the monitor and requires its container moved |
| `scripts/act_ci.py:6846, 6905, 6924, 6975, 7035, 7123, 7165, 13376, 13433, 6074` | new self-test arms and helpers (below) |
| `scripts/act_ci.py` slot arms | `selftest_slot_selection`, `selftest_slot_act_command`, `selftest_slot_guards`, `selftest_slot_validation_path` moved to the new numbers |
| `docs/testing/CI_WORKFLOWS.md:1554-1557` | interrupt gate runs under the monitor |
| `docs/testing/CI_WORKFLOWS.md:1726-1812` | replica shape: staging range, monitor, derivation, plan line, self-test pins |
| `docs/testing/CI_WORKFLOWS.md:2098-2105` | slot resource bounds: slot N owns `20N..20N+19` |
| `docs/testing/CI_WORKFLOWS.md:2315` | slot self-test list: CPUs disjoint at the most concurrency |

## CPU sets, old and new (128-CPU host)

Old (`dc4d06cb`): every job container of a slot on one range, shared by all concurrent legs.

| Slot | Old: every container | New: staging (create) | New: concurrent containers 1, 2, 3, 4 |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 1 | `4-7` | `20-23` | `24-27`, `28-31`, `32-35`, `36-39` |
| 2 | `8-11` | `40-43` | `44-47`, `48-51`, `52-55`, `56-59` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | `20N+4..20N+19`, four ranges of 4 |

A run uses only the ranges it derives: shipping `rtl-full` 4; `docs`, `elaborate`, `rtl-fast` 1
(job range 1 only). Every range is 4 wide, so `nproc` stays 4. `--memory=16g
--memory-swap=16g` and `MemoryMax=24G` are unchanged. Slot 0 on a host under 20 CPUs keeps
all four `rtl-full` legs on `0-3` (pre-#730 behaviour, printed); an isolated slot refuses.
On 128 CPUs, slots 1-5 fit any shipping workflow and slot 6 fits one-container workflows
(before, CPU-wise, slots 1-31).

## Disjointness proof and planted overlaps

`max_concurrency_cpu_layout` (`scripts/act_ci.py:6905`) builds every slot 0-63 at
`SLOT_JOB_RANGES` containers on a host with exactly the CPUs slot 63 needs (1280);
`selftest_cpu_layout_disjoint` (`:6924`) checks 320 ranges, each 4 wide, with
`cpu_range_overlaps(...) == []`. Planted, and each must fail:

- across slots: `slot_cpu_base` patched to the pre-#730 `slot * 4` spacing; the proof reports
  `slot 0 job range 0 and slot 1 staging share CPU 4`;
- within a slot: `job_cpu_ranges` patched to the pre-#730 shape (every leg on the slot's one
  range); the proof reports `slot 0 staging and slot 0 job range 0 share CPU 0`, and leg
  against leg `slot 0 job range 0 and slot 0 job range 1 share CPU 0`;
- runtime guard: a staging range planted on the first job range makes `job_cpu_ranges` refuse.

Mutation checks (scratch copies of `act_ci.py`, each must FAIL the self-test; all did):

| Mutant | FAIL arms |
| --- | --- |
| old `slot * 4` spacing | 11 (incl. the max-concurrency proof) |
| every container moved to range 0 | 2 |
| `max-parallel` ignored | 2 |
| `CONCURRENT_JOB_LIMIT` ignored | 1 |
| `die` does not free | 2 |
| monitor not stopped when the body raises | 1 |
| act run outside the monitor | 4 |
| runtime overlap guard removed | 1 |
| plan line without the job ranges | 4 |
| event stream without the owner-label filter | 1 |

## Dry-run output (ruling item 2)

A live `--dry-run` is not daemon-free, so it was not run (see Conflicts). The output below is
the real `run_validation(..., dry_run=True)` with only GitHub, git, the slot daemon and the
Docker boundary stood in (`dry_run_transcript`, `scripts/act_ci.py:13376`; driver
`$VALIDATION_STORAGE/730-a607/dryrun_offline.py`; full text `receipts/dryrun-offline.txt`,
6865 B, sha256 `b51c2215a080e81b69302f69ec2affdca2caed01f1b04146c82c71133380fbba`). The
shipping `rtl.yml` was read for real; 128-CPU host:

```text
===== slot 0: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19
act-ci: rtl-full: /trusted/act pull_request ... --concurrent-jobs 1 --container-options '--label=org.kebag-logic.milan-act-ci.owner=<token> --cpuset-cpus=0-3 --memory=16g --memory-swap=16g' ...
===== slot 3: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71 --cpuset-cpus=72-75 --cpuset-cpus=76-79
act-ci: rtl-full: /usr/bin/sudo -n -- /usr/bin/nsenter --net=/run/netns/milan-act-slot-3 -- ... --cpuset-cpus=60-63 --memory=16g --memory-swap=16g' ...
```

The self-test arm `selftest_dry_run_cpu_ranges` (`:13433`) asserts the same two lines.

## Gates (all rc 0, at `eb566634` unless noted; interpreter CPython 3.12.3 + PyYAML 6.0.3 + `tools/markdown/requirements.txt`)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | `selftest: PASS`, 477 ok, 0 FAIL (also PASS on the host's 3.14) |
| `python3 scripts/ci_events.py --check` | OK, 2016 contract items |
| `python3 scripts/ci_events.py --selftest` | PASS, 2828 arms |
| `scripts/act_slot_proof.sh --selftest` | PASS, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | ratchets hold (over-long line 0) / 54 PASS |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | 0 findings / 700 arms PASS |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_doc_style.py` / `--selftest` | OK / OK |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` / `--selftest` | OK / 480 links / 1501 arms |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | 0 findings over 82 added lines |
| `python3 scripts/check_doc_paths.py` | OK, 964 paths |
| `git diff --check dc4d06cb HEAD` | clean |

Receipts (`receipts/`): `act-ci-selftest.log` 41117 B sha256
`779d7e60645e485aa94d73271d1e561a2e48c78f144611a78c71597ca348b07a`; `slot-proof-selftest.log`
4070 B `fc7d05d5...d92d9`; `py-idiom.log`, `py-idiom-selftest.log`; `dryrun-offline.txt`.
Not copied (size): `ci-events-selftest.log` 184068 B sha256
`c6b497eb75665fd129d7bdb0dbd39b65b62d3fce837704da7526626059658551` (scratch).

## Replays (acceptance 4): before and after

No complete replay exists in this lane. The slot-3 "before" replay of PR #728 at `2c2f3369`
(dev's runner) was stopped by the manager at 20:10 UTC (rc 130) for disk; slot 3's data-root
was deleted by the manager (`/var/lib/milan-act-ci/` is empty). The lane's "after" replay was
never started (ruling).

| Run | Runner | Job | Wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- | --- |
| before (partial, slot 3) | dev `dc4d06cb` | full-ci-gate | 20:02:42-20:02:57, 15 s | 15.1 GiB sampled `memory.peak` up to the stop | succeeded |
| before (partial, slot 3) | dev `dc4d06cb` | Verilator shards 0-3 | 20:02:57-20:10:36, cut by the stop | (same) | interrupted |
| before (partial, slot 3) | dev `dc4d06cb` | Verilator 4, Yosys 0-3 | started 20:10:36 inside the stop | (same) | interrupted |
| after | lane `eb566634` | all | not run (ruling) | n/a | n/a |

What the partial run does show is the defect's shape (`receipts/before-slot3-partial-samples.log`,
5846 B, sha256 `c68de136...efa4`; replay log 424948 B sha256
`d6c756d0a992fd09f951d82b7c0c34b00c777db5eb743b22ae487f1a268333aa`, scratch only). For 15
samples, four leg containers ran at once, every one with `cpuset.cpus` = `12-15`. Over the last
30 s interval they used 1.06, 0.94, 1.03 and 0.94 CPUs, about four CPUs in all, a quarter of a
hosted runner each.

### Post-merge measurement (ruling item 1): the command and the lines to read

The before replay is the manager's slot-0 record (#721 at `42678ae2`, #715 at `c7d0ad63`). The
after replay is the first manager replay on the merged runner, in the same form, from a clean
candidate worktree with the runner taken from a clean worktree at the merged dev tip:

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Lines to read:

1. Plan, once per run:
   `act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19`
2. Per job wall clock: from the job's first `[rtl-full/<job>] ⭐ Run Set up job` to its
   `[rtl-full/<job>] 🏁  Job succeeded` (or `Job failed`). act does not stamp these lines, so
   the log needs a per-line UTC stamp, as the recorded before logs have.
3. After the workflow: `act-ci: rtl-full: CPU ranges: <n> job container(s) created, <m> moved to a range of their own, at most <k> at once; <s> started on the staging range before the move`.
   Expect `m == n` (12 on a PR replay in which the gate selects the full run: gate,
   5 Verilator, verilator-suites, 4 Yosys, yosys-portability; physical-gptp runs only on
   schedule or dispatch) and `k == 4`. Also expect no `act-ci: WARNING: rtl-full: CPU ranges:` line.
4. Verdict: `act-ci: rtl-full: PASS at <sha>` or `act-ci: rtl-full: FAILED (<rc>)`, compared
   with the before replay's verdict at the same head (acceptance 3).
5. Memory: isolated slot only, `act-ci: slot N: memory peak <x> GiB of its 24G cap; the cap was hit <h> time(s), with no OOM at it`.
   Slot 0 has no slice, so its peak must be sampled on the host.
6. Optional host-side cross-check while four legs run (read-only):
   `docker ps -q --filter label=org.kebag-logic.milan-act-ci.owner | xargs docker inspect --format '{{.Name}} {{.HostConfig.CpusetCpus}}'`
   should list four different ranges.

Acceptance 5 (`CONCURRENT_JOB_LIMIT` 2) is deferred to the same post-merge measurement
(ruling item 3). With 2, `SLOT_JOB_RANGES` becomes 8, and each slot's block would be 36 CPUs.

## Acceptance status

| Item | Status |
| --- | --- |
| 1 own CPUs per concurrent container | Met in code. Proven offline by the self-test and the dry run; memory bounds unchanged; small host refused (isolated) or pre-#730 fallback (slot 0). Not yet exercised against a live daemon. |
| 2 derived, disjoint at max concurrency | Met: derivation from `max-parallel` and `CONCURRENT_JOB_LIMIT`; proof with planted overlaps. |
| 3 fidelity | No workflow, step or job change; every range 4 wide (`nproc` 4). Verdict unchanged on the same head: not shown in lane (no replay); post-merge. |
| 4 measured | Not in lane (ruling); command and lines above. |
| 5 optional | Deferred (ruling). |

Hence `Relates to #730`, not `Closes`.

## Conflicts and open risks

- **`--dry-run` is not daemon-free.** The ruling says "`--dry-run` and `--selftest` start no
  daemon", but `run_validation` enters `replay_slot` and `temporary_docker_boundary` under
  `--dry-run` too. In an isolated slot that starts the slot daemon and seeds the tool cache,
  which pulls the runner image (CI_WORKFLOWS.md, Parallel replay slots: "a `--dry-run` primes
  it", about 75 GB per slot). On slot 0 it creates the boundary and seeds on the default daemon,
  which the manager's live slot-0 replay was using. The ruling also says not to run `act_ci.py`
  against a live PR. So the dry-run output was produced offline, through the real dry-run code
  path. A daemon-free `--dry-run` would be a separate change (suggested new Issue).
- **Unexercised live.** No `docker events` stream or `docker container update` has run in this
  lane against a real daemon. The first live exercise is the post-merge replay, or
  `--interrupt-selftest` on slot 0 (default daemon, existing image), if the manager allows it
  before merge. That probe now also requires its container to have been moved.
- **Mixed runner versions overlap.** A slot run by a pre-#730 runner (`4N..4N+3`) can share CPUs
  with a slot run by this one (for example, old slot 1 `4-7` and new slot 0's job range 1). Run
  every slot from one runner version.
- **Transit on staging.** A container runs on the staging range between its `create` and its
  move; a start before the move is counted (`started on the staging range`). `nproc` is 4 either way.
- **New refusal.** A workflow deriving more than 4 concurrent containers (`max-parallel` over 4,
  or two wide jobs with `CONCURRENT_JOB_LIMIT` 2 and `SLOT_JOB_RANGES` unchanged) or an
  unreadable `max-parallel` is refused. No shipping workflow does this (self-test arm).
- **Fewer slots per host.** On 128 CPUs, slots 1-5 for any shipping workflow (manager uses 1-3).
- Scratch: `$VALIDATION_STORAGE/730-a607/` (venv, act source, partial before log, mutation driver).
  `third_party/lwSRP` was not initialised (no gate needed it).
