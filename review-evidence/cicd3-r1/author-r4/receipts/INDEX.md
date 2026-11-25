# [A839] round 4 receipts (text only, no file over 200 KB, 708 KB in all)

Raw outputs, clones and builds stay in the lane's scratch, /data-2/milan/tmp/cicd-a839/r4/ (3.3 GB). Everything a
reviewer needs to re-check a figure in REPORT.md is here.

File formats:

- `time` files are `/usr/bin/time` lines: wall, user and sys, then `rc=`.
- `perf` files are `perf stat -x,` CSV.
- `start` and `end` files are epoch seconds.
- `spans` files list each suite log's birth and modification times, so the difference is the suite's window.

Identity verdicts come from round 3's `tools/logcmp.py`, unchanged, or from `tools/logcmp4.py`, which adds only
the clone path, the staging directory and RENDER-PHASE timing fields.

| Path | What it holds | REPORT section |
|---|---|---|
| staging/selftest-45d5c35a.txt | `mutant_stage.py --selftest` at the head: 17 controls | 1.2 |
| staging/selftest-plants.txt | 10 planted defects in `mutant_stage.py`, each failing `--selftest` (tools/stage_plants.py) | 1.2 |
| staging/probe-summary.txt, probe-old-13e6d869.jsonl, probe-new.jsonl | tools/stage_probe.py on the previous and this head: independent holders, a real second uid, the bad roots | 1.2 |
| staging/reviewer-r923-probes-old-vs-new.txt | R923-1's own stage_root_probe.py and stage_alias_probe.py on both heads | 1.2 |
| mutants/summary.txt, mutants/logs-45d5c35a/ | Five drivers, twice per head, through the shared cache: times, hits and misses per run (CCACHE_STATSLOG), identity; the head's logs | 1.2 |
| hosted/shard1-per-suite.txt | Shard 1/19 per suite, base run 45383854694 against run 45457006166: windows and Verilator build walls | 2.1 |
| hosted/speed-index-base-vs-13e6d869.txt | Every shard of those two runs: job minutes against the same models' build ratios | 2.1 |
| ab/summary.txt, ab/s1*-p1/, ab/s18*-p1/ | Same-host A/B of shards 1 and 18 at fcbc31f3 and 13e6d869: time, perf, spans, piece receipts, identity | 2.1 |
| hosted/deal-check-old-figures-on-old-runs.txt | The old dealer's projection against both runs' measured windows: milan_dp leg 1 508 → 995 s | 2.1 |
| hosted/new-figures-projection.txt | The refreshed dealer: per worker, projection and largest measured windows | 2.2 |
| hosted/run-45481508309-jobs.txt | The head's hosted run: every job's minutes from the jobs API | 2.3 |
| hosted/run-45481508309-speed-index.txt | Per job of that run: the runner index against both earlier runs | 2.3 |
| hosted/deal-check-new-figures-on-run-45481508309.txt | The refreshed projection against that run's windows | 2.3 |
| hosted/artifact-identity.txt | That run's 24 piece receipts and 83 suite verdict sets against both earlier runs | 2.3 |
| gptp/passes_test-661e4c3.txt | FPGA-gPTP `passes_test.py` at 661e4c3: 63 checks | 3.2 |
| gptp/passes_test-plants.txt | 9 planted defects in the Makefile or pass_run.py, each caught (tools/passes_plants.py) | 3.2 |
| gptp/summary.txt, gptp/<arm>/ | Real-harness arms: time, perf, head, the log's tail (full logs for c-base-j4 and c-head-j4), identity, per-pass end times | 3.2 |
| gptp/docs-gate.log, gptp/lint-gate.tail | `make docs` and `make lint` at 661e4c3 | 3.2 |
| gptp/engine-passes-as-make-jobs.patch, gptp/branch.txt | The commit (`git format-patch`, author address removed) and the branch's SHAs | 3 |
| gates/summary-45d5c35a.txt, gates/tails-45d5c35a.txt, gates/*.log | Round 3's 36 gates at 45d5c35a in a clean clone; the last lines of each log; three full logs | 4 |
| tools/ | Round-4 scripts: mkclone.sh, shard4.sh, gates.sh, gprun4.sh, mutrun4.sh, stage_probe.py, stage_plants.py, passes_plants.py, passes_diff.py, logcmp4.py, hosted_speed.py, hosted_speed_by_suite.py, hosted_compare.py, deal_check.py | all |
