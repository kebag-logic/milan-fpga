# CALIBRATION — #873 item 4 (the manager's; not run by [A763])

Item 4: "run one full replay at 8 x 6 on a PR head that also has a 4 x 16 receipt, and compare
per-job durations and suite timeouts. Report the wall time and peak memory."

This lane ran no replay, no `--dry-run`, no Docker, no slot and no sudo. Everything below is a plan.

## Which runner

The `--jobs`, `--job-cpus` and `--job-memory` options exist only in this PR's `scripts/act_ci.py`.
The trusted `dev` copy (`45c0b56c`) has no such options, and argparse refuses them. So:

- **4 x 16 receipt (this PR's own act):** the ordinary trusted invocation from a clean worktree at
  the live `dev` tip, with no geometry option, so it is today's geometry:

  ```sh
  python3 -I <trusted-dev>/scripts/act_ci.py --pr <PR> --cpu-ranges "$BOOKED_4x16" [--sudo --slot N --evidence-directory <dir-4x16>]
  ```

- **8 x 6 calibration:** needs this PR's runner, so it uses the documented runner-change bootstrap
  (`docs/testing/CI_WORKFLOWS.md`, "A PR that introduces the runner cannot bootstrap trust in its
  own code", lines 1980-2001 at `45c0b56c`). An independent reviewer audits the exact file at the
  PR head, installs it read-only outside the candidate, and records its SHA-256:

  ```sh
  install -m 0555 <candidate>/scripts/act_ci.py <audited-install>/act_ci.py
  sha256sum <audited-install>/act_ci.py
  python3 -I <audited-install>/act_ci.py --selftest --worktree <candidate>
  python3 -I <audited-install>/act_ci.py --pr <PR> \
    --jobs 8 --job-cpus 6 --job-memory 4 \
    --cpu-ranges "$BOOKED_8x6" \
    --repo kebag-logic/milan-fpga --worktree <candidate> \
    --trusted-install-sha256 <recorded-64-hex-digest> \
    [--sudo --slot N --evidence-directory <dir-8x6>]
  ```

  Both replays at the same PR head. If the 4 x 16 receipt should come from the same bytes, run the
  audited install a second time with no geometry option: it is then byte-for-byte today's command
  line (`--concurrent-jobs 4`, `MILAN_CI_FALLBACK_CPUS=12`, `--memory=8g --memory-swap=8g`).

## Ranges

- 8 x 6 needs eight ranges of exactly 6 CPUs, each aligned to 6, distinct, below the host's CPU
  count. 16- or 12-CPU ranges are refused at `--job-cpus 6`.
- A 6-aligned range can straddle a 16-CPU boundary (`12-17`, `30-35`, `60-65`). #737's owner note
  treats 16 CPUs as one die ("a 12-CPU range now always spans two dies"). Eight 6-CPU ranges that
  stay inside the old 4 x 16 footprint and never straddle a 16 boundary:
  `0-5,6-11,18-23,24-29,36-41,42-47,48-53,54-59`.
  The contiguous `0-5,...,42-47` is accepted too, but two of its ranges straddle a boundary.
- The manager books the ranges. The examples are not a host allocation table.

## Memory: read this before running

- The bound is jobs x cap + 4 GiB service share <= the slot's 36G. So **8 jobs fit at most 4 GiB
  each**. `--jobs 8 --job-cpus 6` without `--job-memory 4` is refused (`memory over-subscribed: 8
  jobs of 8 GiB ... need 68 GiB`).
- Measured peaks above 4 GiB: the capture campaign at 5.632 GiB (16 compilers), Yosys source
  builds at 5.26 GiB (8 compilers), the census at 5.34-5.46 GiB (4 workers), and #835's container
  maximum at 7.8 GiB. A peak counts reclaimable page cache, so it is not proof of an OOM at 4 GiB.
- At 6 CPUs the job budgets shrink by design: `CI_BUILD_JOBS` and `VERILATOR_JOBS` become 6,
  `CI_TOOL_BUILD_JOBS` becomes 6, and campaign and simulation pools stay at 4. The census reads its
  4 GiB `memory.max` and runs `floor(2 x 4 GiB / (3 x 1242214400))` = 2 workers.
- **An OOM anywhere in the slot refuses the replay** (`slot-memory.json` `"oom_free": false`,
  `valid build: False`, exit 2). That is a valid calibration result: it says 4 GiB is too small.
  It is not a verdict on the candidate.
- If 8 x 6 x 4 GiB OOMs, these geometries still fit, but each one is a separate decision:
  6 x 8 CPUs at 5 GiB (34 GiB, 48 CPUs), 5 x 6 CPUs at 6 GiB (34 GiB, 30 CPUs). Raising the slot's
  36G cap is a host-allocation decision outside #873.

## What to compare (4 x 16 receipt against 8 x 6)

From each run's evidence directory:

| Quantity | Where | Expectation / what counts as a regression |
|---|---|---|
| Wall time | the runner's own start and end lines in its log | 4 x 16 ran 137-150 min in the last 11 replays. Report the 8 x 6 figure. |
| Per-job durations | `act-execution.jsonl` job start and end events, by the method that gave #835's 574 job-minutes | Compile-heavy jobs get slower at 6 CPUs. Report each job's ratio. |
| Suite timeouts | each job's `timeout-minutes` in the workflows, and any suite timeout in the job logs | Any job or suite that times out at 8 x 6 and not at 4 x 16 is the regression to flag. |
| Peak concurrency | `cpu-placements.json` `peak_jobs` | 8 at 8 x 6, 4 at 4 x 16. Placement `problems` must be empty. |
| Placement | `cpu-placements.json` `ranges` and `placements` | Every container on one booked 6-CPU range, none shared. |
| Slot memory | `slot-memory.json` `peak`, `max`, `oom`, `oom_kill` | Peak at most 36G. Report how often a limit was hit. Any OOM invalidates the run (above). |
| Verdicts | `ci-manifest.json` | The same per-job verdicts at both geometries. Any difference needs explaining before the default changes. |
| Command | the printed `act-ci: combined ...` act command line | `--concurrent-jobs 8`, `MILAN_CI_FALLBACK_CPUS=6`, `--memory=4g --memory-swap=4g` and the eight booked ranges. |

## After the calibration

The default stays 4 x 16 at 8 GiB (`JobGeometry()`, `scripts/act_ci.py`). Changing it is a
follow-up: one edit to the dataclass defaults, the docs' "chosen default" paragraph
(`docs/testing/CI_WORKFLOWS.md`, near the job geometry table), and the selftest arm that pins the
default ("the default geometry is the runner's before #873 ...") must move with it.
