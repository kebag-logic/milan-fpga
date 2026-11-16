# Native 4-shard sweep at 0297a19a

`native-shards.py 927-a791-sweep <spec> <out> 4 <cpus>...`: `scripts/run_all_suites.sh <logs> --wait --shard k/4` on
four dedicated clones of the head, each its own unit on a range booked through `cpu_ranges.pick8`, started at 22:54
after every Vivado build of the round had finished.

| Shard | Suites | Passed | Failed | Timed out | Checks | In-suite failures | rc |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0/4 | 15 | 15 | 0 | 0 | 361,064 | 0 | 0 |
| 1/4 | 17 | 17 | 0 | 0 | 2,046,229 | 0 | 0 |
| 2/4 | 17 | 17 | 0 | 0 | 284,233 | 0 | 0 |
| 3/4 | 16 | 16 | 0 | 0 | 21,575 | 0 | 0 |
| all | 65 | 65 | 0 | 0 | 2,713,101 | 0 | |

`sweep-shard<k>-summary.log` is each shard's printed summary, `-results.json` its exit code and duration,
`-spec.json` its command; `sweep-suite-logs.sha256` the digest of every suite's log (kept in scratch).
