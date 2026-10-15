# Hosted baseline and round-one projection

Baseline jobs are measured at `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` from the jobs API. After values are predictions for warm caches on standard runners, not a hosted rerun. Queue time, cold builds, network installs and new artifact overhead remain to be measured.

## rtl-full

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894214/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| full-ci-gate | 115631441324 | 0m50s | 0m50s plus execution-evidence overhead |
| Yosys shard 0/4 | 115631699014 | 8m14s | 8m14s plus execution-evidence overhead |
| Yosys shard 3/4 | 115631699114 | 0m31s | 0m31s plus execution-evidence overhead |
| Yosys shard 2/4 | 115631699117 | 0m32s | 0m32s plus execution-evidence overhead |
| Verilator shard 0/5 | 115631699137 | 69m48s | Replaced by the sixteen derived workers below |
| Verilator shard 3/5 | 115631699169 | 60m09s | Replaced by the sixteen derived workers below |
| Verilator shard 2/5 | 115631699198 | 70m10s | Replaced by the sixteen derived workers below |
| Verilator shard 1/5 | 115631699214 | 68m38s | Replaced by the sixteen derived workers below |
| Verilator shard 4/5 | 115631699226 | 55m32s | Replaced by the sixteen derived workers below |
| Yosys shard 1/4 | 115631699385 | 0m25s | 0m25s plus execution-evidence overhead |
| Physical gPTP (nightly and manual) | 115631700715 | 0m00s | Still skipped for push/PR; separate nightly/manual campaign |
| verilator-suites | 115653077431 | 0m07s | Under 1 minute after all workers and six case unions |
| yosys-portability | 115653119397 | 0m08s | Under 1 minute |

## elaborate

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894212/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| elaborate | 115631440899 | 35m44s | Protected union: under 1 minute; workers approximately 26 and 12 minutes |

## docs

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894291/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| wire-accountability | 115631441194 | 0m09s | 0m09s plus execution-evidence overhead |
| docs-check-no-git | 115631441331 | 0m12s | 0m12s plus execution-evidence overhead |
| docs-check | 115631441482 | 33m59s | Protected union: under 1 minute; workers approximately 22 and 19 minutes |

## rtl-fast

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894211/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| bdd-conformance | 115631440905 | 0m14s | 0m14s plus execution-evidence overhead |
| changes | 115631441106 | 0m29s | 0m29s plus execution-evidence overhead |
| yosys-elaboration | 115631592055 | 11m00s | 11m00s plus execution-evidence overhead |
| verilator-lint | 115631592063 | 0m40s | 0m40s plus execution-evidence overhead |
| publication-census | 115631592079 | 18m25s | 18m25s plus execution-evidence overhead |
| firmware-control-mutants | 115631592083 | 16m21s | 16m21s plus execution-evidence overhead |
| firmware-verilator | 115631592089 | 11m10s | 11m10s plus execution-evidence overhead |
| firmware-unit | 115631592104 | 10m45s | 10m45s plus execution-evidence overhead |
| firmware-srp-mutants | 115631592115 | 12m32s | 12m32s plus execution-evidence overhead |
| firmware-boundary | 115631592117 | 15m19s | 15m19s plus execution-evidence overhead |
| firmware-aecp-mutants | 115631592128 | 3m48s | 3m48s plus execution-evidence overhead |
| rtl-fast | 115636758266 | 0m04s | Under 1 minute |

## New Verilator workers

The weighted suite model includes 122 seconds of worker setup. It is a capacity estimate; it is not a measured new GitHub job duration. The media-clock history exception is authorized by the third and fourth rulings.

| Worker | Predicted including setup |
|---:|---:|
| 0/16 | 26m45s |
| 1/16 | 24m55s |
| 2/16 | 26m12s |
| 3/16 | 24m54s |
| 4/16 | 25m21s |
| 5/16 | 24m52s |
| 6/16 | 24m55s |
| 7/16 | 24m58s |
| 8/16 | 24m53s |
| 9/16 | 24m53s |
| 10/16 | 24m57s |
| 11/16 | 24m57s |
| 12/16 | 24m53s |
| 13/16 | 24m51s |
| 14/16 | 24m54s |
| 15/16 | 33m52s |

Six new per-suite union jobs should each take under one minute after worker artifacts arrive; each has a two-minute limit. The manifest collector is budgeted at three minutes, and the watcher follows the worker critical path. These new jobs require hosted measurement.

The regular Verilator worker maximum is 26m45s. Media-clock worker 15 is projected at 33m52s including setup (31m49s for its carried history alone), before downstream collection. The exhaustive workflow therefore still projects above 30 minutes. The coordinating role measures the exact pushed head and takes that remaining choice to the owner.

Warm-cache workflow targets including final collection: docs about 26 minutes, elaborate about 30 minutes, rtl-fast about 22 minutes. These estimates leave limited elaboration margin. A cold source-tool build can exceed them; round two adopts prebuilt layers. No hosted after-time is claimed.
