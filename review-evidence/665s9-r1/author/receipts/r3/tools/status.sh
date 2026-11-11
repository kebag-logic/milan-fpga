#!/usr/bin/env bash
# status.sh: one line on the final gate pass (replay results, failures, shards, memory, scratch size)
S=<scratch>; J=$S/ci/72f596b8f375/jobs
n=$(ls $J/*/result.json 2>/dev/null | wc -l); f=$(grep -l '"result": "failure"' $J/*/result.json 2>/dev/null | xargs -rn1 dirname | xargs -rn1 basename | tr '\n' ' ')
sh=""; for k in 0 1 2 3; do sh="$sh$k:$(systemctl --user is-active milan-a760d-shard$k.service 2>/dev/null)/$(ls $S/sweep/shard-$k/logs 2>/dev/null | wc -l) "; done
echo "$(date +%T) replay $n/69 failed[$f] shards[$sh] MemAvail $(awk '/MemAvailable/{print int($2/1e6)}' /proc/meminfo)G scratch $(du -sh $S 2>/dev/null | cut -f1)"
