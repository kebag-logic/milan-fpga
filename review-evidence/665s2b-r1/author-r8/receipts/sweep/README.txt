The full sweep at b7c30969 as four shard units (native-shards.py: one clone and one unit per shard, MemoryMax 10 GB,
-j4) on CPUs 0-3, 4-7, 8-11 and 12-15, which cpu_ranges.py showed free. Each shard's run_all_suites.sh exit code and
log are in shard-k/. The tally ran over the union of the four shards' suite logs (union-logs.sha256 and .sizes record
them): python3 scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator, rc 0. mbx.log is the mailbox
suite's log, the record mover's bench and planted defects among its targets.
