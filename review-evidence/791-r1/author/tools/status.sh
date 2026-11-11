#!/usr/bin/env bash
# status.sh: one screen of this lane's runs.
S=/data-2/milan/tmp/791-a765
date +%T; grep MemAvailable /proc/meminfo | awk '{printf "MemAvailable %.1f GB\n", $2/1e6}'
echo "own unit memory $(( $(cat /sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)/memory.current) / 1000000 )) MB"
tail -2 $S/final/chain-sims.log $S/final/chain-litex.log 2>/dev/null | grep -v "^$"
for k in 0 1 2 3; do l=$(ls -t $S/sweep/shard-$k/logs/*.log 2>/dev/null | head -1); echo "shard$k: $(ls $S/sweep/shard-$k/logs 2>/dev/null | wc -l) files; $(systemctl --user is-active milan-791-a765-shard$k)"; done
tail -1 $S/ci-logs/tick.log; grep "local:" $S/ci-logs/local.log | tail -1
find $S/ci/03447eaa087b/jobs -name result.json -size +0 | wc -l | xargs echo "replay results:"
grep -l '"failure"' $S/ci/03447eaa087b/jobs/*/result.json 2>/dev/null | xargs -r -n1 dirname | xargs -r -n1 basename | sed 's/^/FAILED /'
