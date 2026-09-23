#!/usr/bin/env bash
# Run one focused test pinned to CPUs 0-1 beside six busy loops on the same
# CPUs (4x oversubscription), then stop the loops. Usage: contention.sh CLONE TEST
set -u
clone="$1"; test="$2"; pids=()
for _ in 1 2 3 4 5 6; do taskset -c 0,1 python3 -c 'while True: pass' & pids+=("$!"); done
start=$(date +%s)
( cd "$clone" && taskset -c 0,1 python3 "$test" ) > "$3" 2>&1
rc=$?
end=$(date +%s)
kill "${pids[@]}"; wait "${pids[@]}" 2>/dev/null
echo "exit=$rc seconds=$((end - start)) test=$test" | tee -a "$3"
