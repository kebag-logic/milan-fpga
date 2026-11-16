The verilator-suites sweep at 09a948d4 (65 suites, `scripts/run_all_suites.sh --wait --shard k/4`), each shard on a
clean clone, through the recorded-gates runner (each command's exit code recorded in its results.json):

| Shard | Recorded rc | Suites | Passed | Failed | Timed out | Checks | Run |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 15 | 15 | 0 | 0 | 361,003 | sweep3, -j4 |
| 1 | 1 | 17 | 14 | 1 gptp_shadow | 2 milan_dp_gm_steps, milan_dp_render | 2,046,218 | sweep3, -j4 |
| 1 re-runs | 0 | 3 | 3 | 0 | 0 | | sweep6/rr, uncontended, the hosted 4-core budget |
| 2 | 0 | 17 | 17 | 0 | 0 | 284,233 | sweep5/s2, the hosted 4-core budget, -j4 |
| 3 | 0 | 16 | 16 | 0 | 0 | 21,575 | sweep5/s3rr, -j4 |

Shard 1's three were the host's contention (load average 300 to 950 on 128 CPUs then): gptp_shadow's 325 checks
passed and its lifecycle target overran a fixed 12 s subprocess timeout; the other two were cut by the 1,800 s wall
clock. Re-run one at a time in a clean clone, with the driver's per-suite logic (rerun_suites.sh: timeout make, then
scripts/suite_tally.py --verdict): 241, 695 and 908 s, all pass.

Runs cut by the host (OOM kills, a power cycle, a crash, a shutdown) recorded no rc and are not cited; see the round's
handoff. The hosted 4-core budget is the verilator-suites job's own (rtl.yml, "Set CPU-derived job budgets":
VERILATOR_JOBS and SIM_JOBS at the runner's cores): without it capture_coherence builds with every core the host
has and overran the 10 GB unit cap.
