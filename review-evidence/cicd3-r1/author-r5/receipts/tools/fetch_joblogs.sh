#!/bin/bash
# fetch_joblogs.sh OUT: each completed "Verilator shard N/T" job of the run in OUT/run-id, in `gh run view --log` form
# (job, step, timestamp, message), as OUT/joblogs/N.log; skips logs already fetched.
set -euo pipefail
OUT=$1; REPO=kebag-logic/milan-fpga; RUN=$(cat "$OUT/run-id")
mkdir -p "$OUT/joblogs"
python3 -c '
import json, re, sys
for j in json.load(open(sys.argv[1]))["jobs"]:
    m = re.fullmatch(r"Verilator shard (\d+)/\d+", j["name"])
    if m and j["status"] == "completed":
        print(m[1], j["id"])' "$OUT/jobs.json" | while read -r n id; do
  [ -s "$OUT/joblogs/$n.log" ] || gh run view "$RUN" -R "$REPO" --job "$id" --log > "$OUT/joblogs/$n.log"
done
ls "$OUT/joblogs" | wc -l
