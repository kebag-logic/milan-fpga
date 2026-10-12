#!/usr/bin/env bash
run=38217650945
logs=$(mktemp -d)
gh run view "$run" -R kebag-logic/milan-fpga --json jobs \
  --jq '.jobs[] | select(.name | startswith("Verilator shard")) | .databaseId' \
  > "$logs/jobs"
while read -r job; do
  gh run view "$run" -R kebag-logic/milan-fpga --job "$job" --log > "$logs/$job.log"
done < "$logs/jobs"
python3 scripts/suite_shards.py --measure "$logs"/*.log
python3 scripts/suite_shards.py --selftest
printf "REVIEW_LOG_DIRECTORY=%s\n" "$logs"
