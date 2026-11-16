# The 4-shard native sweep at 70c100da

`native-shards.py` (one --shared clone and one unit per shard, MemoryMax 10G, -j4) over the lane's spec, the
pinned Verilator 5.050 and sv2v v0.0.12: every shard exit 0. 65 suites (15 + 17 + 17 + 16), all PASS, none timed
out; 2,713,040 checks (361,003 + 2,046,229 + 284,233 + 21,575), 0 in-suite failures. Each shard ran on 8 CPUs of the
session pool (no range was free in cpu_ranges.py after the 19:43 restart). A first run at 19:13 was cut by the
host's 19:39 shutdown; its output was moved aside unread and the sweep ran again whole.
