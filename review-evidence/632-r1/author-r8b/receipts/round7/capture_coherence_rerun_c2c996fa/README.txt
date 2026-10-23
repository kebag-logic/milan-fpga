capture_coherence at c2c996fa, run again alone after the full sweep: in shard 2 the runner's 2,400 s wall clock
stopped it (TIMEOUT, result unknown, not a failure; sweep_c2c996fa/shard2/summary.txt). Driver
scripts/round7/cc_rerun.sh: the suite's default target exactly as scripts/run_all_suites.sh invokes it
(make -C tb/verilator/capture_coherence), on the same two CPUs and job knobs as the shard, no wall clock, then the
runner's own tally (suite_tally.py --verdict, its exit in tally.txt). Nothing else ran beside it.
Result: exit 0 in 2,402 s; capture_coherence 20,832 checks and capture_coherence_dp 447 checks, 0 failures; its
mutation campaign 35 checks, 35 PASS; tally verdict 0. The full log (261 KB) is recorded by sha256 and size only
(large_logs.sha256); verdict_lines.txt holds its verdict, result and control lines.
