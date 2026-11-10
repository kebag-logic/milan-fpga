[A763] REVIEW READY
Commit: 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 (branch `873-act-eight-jobs`, 3 commits on dev 45c0b56c; local, not pushed)
Changed:
- `scripts/act_ci.py`: `CONCURRENT_JOB_LIMIT`, `CONTAINER_CPU_LIMIT`, `FALLBACK_CPU_LIMIT` and `CONTAINER_MEMORY` are replaced by one validated `JobGeometry`, chosen with `--jobs` (1-8), `--job-cpus` (16, 8 or 6) and `--job-memory` (1-8 GiB). The default is today's 4 x 16 CPUs (12-CPU fallback) at 8 GiB, so an unchanged command line runs and is refused as before. `--cpu-ranges` is read against the chosen width. The aligned, distinct and within-host refusals stay at every width. A geometry exists only if jobs x cap + the 4 GiB service share fits the slot's 36G, and jobs x width fits 64 CPUs. Otherwise it is a Refusal before any collaborator, never a smaller replay. So 8 jobs need `--job-memory 4`.
- 34 new self-test arms. All 621 existing isolated arms are kept and pass.
- `docs/testing/CI_WORKFLOWS.md`: the geometry and its bounds, #835's measured basis, the unchanged default, and what the calibration decides.
- No change to the pinned dispatcher, workflows, evidence files or what the replay attests.
Validation (clean clone of the head, each rc 0, logs written by the gate itself):
- `python3 scripts/act_ci.py --selftest`: PASS, 657 ok. Flat isolated install with `--worktree`: PASS, 655 ok. `python3 -I scripts/act_ci_small_host_selftest.py`: PASS.
- 22 planted defects, one per copy of the committed runner: all fail the self-test, none survives.
- Every `run:` step of `.github/workflows/docs.yml`, one fresh clone per job: 66 steps ran, 31 not run with a reason, 0 bad. Every step that ran has rc 0; the steps not run need the hosted runner's context or `sudo`/`apt` for packages already present at their pins.
- `python3 scripts/docs_inventory.py --check`: OK. `cd tests && behave`: 508 scenarios passed. `git diff --check 45c0b56c 88e1041c`: clean.
Acceptance criteria:
- 1: met. Parameters replace the constants; 8 jobs on 6- or 8-CPU aligned ranges are accepted; the `--cpu-ranges` refusals are unchanged.
- 2: met. Memory over-subscription is refused by construction.
- 3: met. Every existing arm is kept; new arms cover 8 jobs and refused memory and CPU over-subscription.
- 5: met. The measured basis and chosen default are in the runner's documentation.
- 4: not done here, by assignment. It is the manager's calibration replay, as this PR's own act. It needs this PR's runner, so it runs from an independently audited install (the documented bootstrap).
Open risks/questions:
1. Eight jobs fit only at 4 GiB each, below the measured capture peak (5.632 GiB) and #835's 7.8 GiB container maximum. A peak counts reclaimable page cache, but an OOM refuses the replay, so the 8 x 6 calibration may end refused for memory. The 36G slot cap is a host decision outside #873.
2. The docs recorded "Eight-CPU ranges remain refused under the current owner ruling" (#737). This keeps 6- and 8-CPU ranges refused under the default geometry and accepts them only with an explicit `--job-cpus`. If the ruling should bind the explicit option too, that is the manager's decision.
3. A 6-aligned range can straddle a 16-CPU boundary (`12-17`); booking is the manager's.
