# Receipts: #1008 round 4 (lane cicd-1008, branch 1008-ci-30min)

Base: dev-soft-core `c34e7d8b06`. Local runs used CPUs from `cpu_ranges.py pick` (16-31, 32-47) or the lane's
own session range 64-95, every unit at CPUWeight 10.

## hosted/ - the measurement (gh api, read only)

- `workflows.json`, `<workflow>-runs.json`: the last 20 successful runs of rtl-fast, rtl-full, elaborate, docs.
- `<run>-jobs.json`: every job of each of those 80 runs (one file per run).
- `durations.json`, `durations.tsv`: every hosted, non-skipped job window; per job n, min, mean, p95, max and
  both times 1.41. Made by `tools/measure_hosted.py` (the earlier session of this lane).
- `45657606190-w22-raw.log`, `45751066654-w22-raw.log`: Verilator shard 22/27's raw `gh run view --log`, the
  two complete hosted runs after #1003 at gptp-processor 1213ac5b; `suite_shards.py --measure` reads 478 s and
  517 s for `gptp_shadow`. (`45735453538-gptp-worker.log` is at the #1013 lane's pin 3ce71b76: 672 s; not used.)
- `logs/`: three hosted job logs fetched while checking census timing (run 45755846903).

## reference/ - the serial verdicts

Run 45657606423 at 09201d35, whose `sw/`, `hdl/`, `configs/` and every submodule equal `c34e7d8b`'s
(`git diff --stat 09201d35 c34e7d8b -- sw hdl configs <submodules>` is empty): the logs of
`publication-census`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-srp-mutants`,
`firmware-unit` and the boundary jobs, and `jobs.txt`.

## local/ - the legs, run at a committed snapshot clone

- `control/`: `--shard 1/4 --campaign-shard K 4`, K = 0..3, at `3fbfa3bccd`; `head`, `legK.log` (stamped),
  `legK.time` (`/usr/bin/time -v`), `summary`.
- `census/`: `census_legs.py run --leg K`, K = 0..4, then `union`, at `530149b5dd`.
- `aecp-srp/`: `--shard 2/4` and `--shard 3/4`, `--campaign-shard K 2`, at `530149b5dd`.

## identity/ - verdict identity and planted failures

- `census.txt`: leg 0's check lines equal the serial check's (durations masked); the judge's 222 arm and rule
  lines equal the serial self-test's, one line differing only by a Yosys heap address in a cell name.
- `census-plants.txt`: seven failures planted into copies of the real receipts, each refused.
- `control.txt`, `aecp.txt`, `srp.txt`: the legs' verdict multisets against the serial run's.
- `projection.txt`: each divided job's slowest leg, projected (`tools/project.py`).

## profile4/ - perf (cpu-clock:u, 49 Hz, user space; the VM has no hardware counters)

- `census-leg1-by-comm.txt`, `control-leg1-by-comm.txt`: where a leg's CPU goes, by process.

## gates/ - every touched gate in a clean clone of the head (`summary`, one log each)

`gates-f7d7fe5d-summary` and `gates-f7d7fe5d-ci_events_selftest.log`: the run at the earlier head, whose event
self-test stopped on the fast-leg arms (fixed in `5b5b0765`).

## Kept from the earlier session, not evidence

`profile/`, `local/control-K.*`, `local/census-*`, `gate-workflows-first.log`, `gate-workflows-second.log`: its
runs, stopped when it ended (empty perf files: the VM opens no hardware counter).

## tools/

`measure_hosted.py` (earlier session), `steps.py` (per-step hosted windows), `mutant_times.py`,
`minutes.py` (runner-minutes), `project.py` (slowest-leg projection), `census_identity.py`,
`campaign_identity.py`, `plant_census.py`; the earlier session's `control-leg-K.sh`.
