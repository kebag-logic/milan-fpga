#!/usr/bin/env bash
# Run a list of docs.yml commands at the lane head with the locked venv's
# python3 first on PATH; append "rc<TAB>seconds<TAB>command" to EXITS.txt
# and keep each command's output in logs/NNN.log.
# Usage: run_gates.sh <commands file>   (env: OUT, REPO, VENV)
set -u
cmds=$1
mkdir -p "$OUT/gates/logs"
n=$(ls "$OUT/gates/logs" | wc -l)
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  n=$((n+1)); log=$(printf "%s/gates/logs/%03d.log" "$OUT" "$n")
  echo "\$ $cmd" > "$log"
  start=$(date +%s)
  (cd "$REPO" && PATH="$VENV/bin:$PATH" RUNNER_TEMP="$OUT/scratch/runner-temp" \
     PYTHONDONTWRITEBYTECODE=1 bash -c "$cmd") >> "$log" 2>&1
  rc=$?
  printf "%s\t%ss\t%s\n" "$rc" "$(( $(date +%s) - start ))" "$cmd" | tee -a "$OUT/gates/EXITS.txt"
done < "$cmds"
