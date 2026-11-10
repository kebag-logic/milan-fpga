[A763]

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

GREEN locally at `88e1041c9b100c389f3629dfcf3185ad3be9c3f4`: `act_ci.py --selftest` PASS. All 623 of the base's arms are kept and pass, 34 are new (657 in all; 655 and 621 in the isolated flat install), and all 22 planted defects fail it. Every `run:` step of `docs.yml` has rc 0 on a clean clone of the head, or is not run with its reason stated (66 steps ran, 31 not run with a reason, 0 bad). behave passes 508 of 508 scenarios. `873-act-eight-jobs` -> `dev`.

## Linked Issue / roles

Closes #873

Items 1, 2, 3 and 5 are met here. Item 4, the calibration replay at 8 x 6 on a head that also has a 4 x 16 receipt, is the manager's calibration and becomes this PR's own act. This PR neither runs it nor claims its result.

Executor: `[A763]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The local act replay ran at most 4 job containers, each on an exclusive 16-CPU range. On PR #835's replay the slot kept 7.7 of its 64 booked CPUs busy. The job count, the per-job CPU width and the per-job memory cap are now one validated `JobGeometry` that the operator chooses. The default stays today's geometry, so an unchanged command line runs, and is refused, exactly as before.

| #873 item | Change | Where |
|---|---|---|
| 1. Parameters in place of the constants | `CONCURRENT_JOB_LIMIT`, `CONTAINER_CPU_LIMIT`, `FALLBACK_CPU_LIMIT`, `CONTAINER_MEMORY` and `SLOT_JOB_RANGES` are gone. `--jobs` (1-8), `--job-cpus` (16, 8 or 6) and `--job-memory` (1-8 GiB) build one `JobGeometry`. Its default is 4 x 16 CPUs (12-CPU fallback) at 8 GiB. `JOB_CPU_WIDTHS` maps a width to the range widths it accepts: 16 to 16 or 12, 8 to 8, 6 to 6. `main` sets the geometry before `--cpu-ranges` is parsed, so ranges are read against the chosen width. The `--cpu-ranges` refusals stay as they are: aligned, distinct and within the host, at every width. The act command takes `--concurrent-jobs`, `MILAN_CI_FALLBACK_CPUS` and `--memory`/`--memory-swap` from the geometry. | `scripts/act_ci.py`: constants at 107-126, `JobGeometry` at 4743, `parse_cpu_ranges` 4838, `job_cpu_ranges` 4861, `build_act_command` 4903-4952, options 17356-17370, `main` 17472-17480 |
| 2. Memory bounded by construction | A geometry exists only if jobs x cap + `SLOT_SERVICE_MEMORY_GIB` (4, the overhead the docs already reserved) fits `SLOT_MEMORY_MAX` (36G). It also needs jobs x width to fit `REPLAY_CPU_LIMIT` (64, the CPUs one replay booked before). Anything else is a `Refusal` before any collaborator runs. It is never shrunk into a smaller replay. So 8 jobs need `--job-memory 4`. | `scripts/act_ci.py:4760-4786` |
| 3. Selftest arms | Every existing arm stays and passes with the same label and the same values under the default geometry. Their expected values now come from the geometry, and a new arm pins the default to 4 x 16 at 8g. New arms cover 8 jobs on 6- and 8-CPU ranges end to end: range parsing and selection, the act command's concurrency, ranges, fallback and memory words, a ninth job, seven ranges for eight jobs, and the kept refusals at each width. They also cover refused memory over-subscription (4 shapes, one that passes only if the service share is counted) and refused CPU over-subscription (3 shapes whose memory fits), both bounds exactly met, out-of-range and non-integer values, and the command line: usage errors with `--selftest` (the nested self-test stubbed, so a missing usage error fails instead of recursing), refusals before any collaborator, and an accepted 8 x 6 and 8 x 8 run reaching its first collaborator. | `scripts/act_ci.py:7820-7841`, `7871-8004`, wired at 15480 and 15514 |
| 5. Measured basis and chosen default | The range width and fallback rules, the admission bound, and a job-geometry paragraph with its two bounds and a table of accepted and refused shapes. Also #835's measured figures, the unchanged default, the 4 GiB caveat, and what the calibration decides. | `docs/testing/CI_WORKFLOWS.md:2272-2283`, `2339-2340`, `2355-2406`, `2831-2833` |

No change to the pinned dispatcher (`ci/act/cpu_ranges.go`). It already accepts width 16 or `MILAN_CI_FALLBACK_CPUS` (1 to 16), and as many jobs as there are ranges. No workflow changes, and none to what the replay attests. The evidence files (`cpu-placements.json`, `slot-memory.json`, the manifest) are unchanged. The printed act command line already shows the geometry.

## Authoritative references

- #873, Required items 1, 2, 3 and 5; Out of scope: workflow changes and what the replay attests.
- [`docs/testing/CI_WORKFLOWS.md`](../docs/testing/CI_WORKFLOWS.md), "Act-first local replication": booked CPU ranges, admission, memory policy, resource bounds, the runner-change bootstrap.
- #737: the owner's CPU rules for the local replay. 16 CPUs per job, and the 12-CPU fallback as "one named setting, so it can change to 8 if the owner decides that".
- [`ci/act/cpu_ranges.go`](../ci/act/cpu_ranges.go): the pinned dispatcher's range and fallback contract.
- [AGENTS.md](../AGENTS.md) section 5: the trusted host-side runner and the bootstrap of a runner change.

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git checkout --detach 88e1041c9b100c389f3629dfcf3185ad3be9c3f4
git submodule update --init
python3 -m venv .venv && . .venv/bin/activate
python3 -m pip install PyYAML==6.0.3 behave==1.3.3
```

## How to validate

```sh
python3 scripts/act_ci.py --selftest
d="$(mktemp -d)"; install -m 0555 scripts/act_ci.py "$d/act_ci.py"
python3 -I "$d/act_ci.py" --selftest --worktree "$PWD"
python3 -I scripts/act_ci_small_host_selftest.py
python3 scripts/docs_inventory.py --check
(cd tests && behave)
git diff --check 45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c HEAD
```

Expected result / pass criteria: every command exits 0. Both self-tests end `selftest: PASS` with no `FAIL` line: 657 `ok` lines for the first, which includes the two flat-install launcher arms, and 655 for the isolated flat install. At the base `45c0b56c` they are 623 and 621. The small-host control ends `small-host runner control: PASS`. behave reports 508 scenarios passed. The new arms can be listed with `python3 scripts/act_ci.py --selftest | grep -E '8 jobs|8-job|over-subscription|geometry|--job|ninth'`.

Every `run:` step of `.github/workflows/docs.yml` was also run on a fresh clean clone of the head, one job per clone. The verifier reports 66 steps ran, 31 not run with a reason, 0 bad. Every step that ran has rc 0, and every job's tree was clean afterwards. The steps not run need the hosted runner: GitHub's own step context, uploaded receipts, run cancellation, or `sudo`/`apt` installs of packages that are already present at their pinned versions.

Planted defects (22), one per copy of the committed `act_ci.py`, each run as the flat installed self-test. Each must fail, and each did:

| Planted defect | Failing arms |
|---|---|
| memory check removed | the four memory over-subscription arms; "8 jobs at the default 8 GiB are refused for memory before any collaborator" |
| service share dropped from the sum | the four memory over-subscription arms |
| CPU check removed | the three CPU over-subscription arms; "8 jobs at the default 16 CPUs are refused for CPU before any collaborator" |
| `REPLAY_CPU_LIMIT` 64 -> 128 | the same four CPU arms |
| `--concurrent-jobs` fixed at 4 | "8 jobs on 6-CPU ranges: act starts 8 jobs at once ..." and its 8-CPU twin |
| `MILAN_CI_FALLBACK_CPUS` fixed at 12 | the same two |
| container memory fixed at 8g | the same two |
| `job_cpu_ranges` selects 4 ranges | "8 jobs on 6-CPU ranges: the 8 booked ranges parse, admit 8 concurrent jobs and are all selected" and its 8-CPU twin |
| range widths ignore the geometry | existing "invalid or missing CPU ranges '0-7'"; "the default geometry still refuses 6- and 8-CPU ranges"; both "refuse any other width" arms; "--cpu-ranges is read against the chosen width" |
| `main` parses `--cpu-ranges` before the geometry | five command-line arms, including both accepted 8-job runs |
| `MAX_CONCURRENT_JOBS` 8 -> 16 | "a job count, CPU width or memory cap out of range ... is refused by name"; "a ninth job is refused before any collaborator" |
| default width 16 -> 8 | five existing arms, then the self-test stops on an uncaught refusal |
| default memory 8 -> 4 GiB | "the default geometry is the runner's before #873 ..."; "8 jobs at the default 8 GiB are refused for memory ..." |

## Known limitations / out of scope

- **Item 4 is not done here.** The calibration replay at 8 x 6 is the manager's, as this PR's own act. Until it is recorded, the default stays 4 x 16 at 8 GiB and the docs say so. The calibration needs this PR's runner, so it runs from an independently audited install (the documented runner-change bootstrap). The trusted `dev` copy has no geometry options.
- **Eight jobs fit only at 4 GiB each** under the slot's 36G cap. That is below the capture campaign's measured 5.632 GiB peak and #835's 7.8 GiB container maximum. A peak counts reclaimable page cache, so a job above 4 GiB is not necessarily killed at 4 GiB. But an OOM anywhere in the slot refuses the replay, so the calibration may end refused for memory. Raising the 36G cap is a host-allocation decision outside #873.
- **The eight-CPU ruling.** The docs said "Eight-CPU ranges remain refused under the current owner ruling" (#737, fallback 12). #873 asks to accept 6- and 8-CPU ranges. This PR keeps them refused under the default geometry and accepts them only with an explicit `--job-cpus 8` or `--job-cpus 6`. The docs now say so. The default width and its 12-CPU fallback are unchanged. If the owner ruling should also bind the explicit options, that is a decision for the manager.
- A 6-CPU range aligned to 6 can straddle a 16-CPU boundary (`12-17`). An 8-CPU range never does. Booking is the manager's.
- No live run of the new code in this lane: no replay, no `--dry-run`, no Docker, no slot. The geometry's effect on act is proved offline on the generated command, as the existing arms prove the default.
- Not touched: `ci/image/tool-inventory.json`'s digest of `scripts/act_ci.py`. It was already stale at the base (`45c0b56c` hashes `3f91c996...` against the pinned `b8a786ce...`). Only the CI image build checks it, not `docs.yml`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (items 1, 2, 3 and 5 here; item 4 is the manager's calibration)
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
