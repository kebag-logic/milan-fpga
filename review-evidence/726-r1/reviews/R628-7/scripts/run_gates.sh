#!/usr/bin/env bash
# Run each command line of a gate list in parallel inside a repository.
# Usage: run_gates.sh <repo> <gate-list> <out-dir> <python> [jobs]
# Writes <out-dir>/<n>.log, <n>.rc and a summary.tsv (n, rc, command).
set -uo pipefail
repo=$1; list=$2; out=$3; py=$4; jobs=${5:-12}
mkdir -p "$out"
export PATH="$(dirname "$py"):$PATH"
n=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  case "$cmd" in \#*) continue ;; esac
  n=$((n + 1))
  printf '%s\0%s\0' "$n" "$cmd"
done < "$list" |
  xargs -0 -n 2 -P "$jobs" bash -c '
    # $0=repo $1=out $2=n $3=command
    cd "$0" || exit 99
    ( eval "$3" ) > "$1/$2.log" 2>&1; echo $? > "$1/$2.rc"
  ' "$repo" "$out"
: > "$out/summary.tsv"
n=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  case "$cmd" in \#*) continue ;; esac
  n=$((n + 1))
  printf '%s\t%s\t%s\n' "$n" "$(cat "$out/$n.rc" 2>/dev/null || echo MISSING)" "$cmd" >> "$out/summary.tsv"
done < "$list"
cat "$out/summary.tsv"
