#!/usr/bin/env bash
# Run every row of gate_cases.txt through gate_probe.sh, N at a time.
# usage: run_gate_cases.sh <head-tree> <base-tree> <scratch-root> <out-dir> <jobs> [cases-file]
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
head=$1 base=$2 scr=$3 out=$4 jobs=$5 cases=${6:-$here/gate_cases.txt}
mkdir -p "$out"
while IFS=$'\t' read -r tree rest; do
  [ -n "$tree" ] || continue
  case $tree in head) t=$head ;; base) t=$base ;; *) t=$tree ;; esac
  printf '%s\t%s\n' "$t" "$rest"
done < "$cases" | tr '\n' '\0' | xargs -0 -P "$jobs" -I{} bash -c '
  IFS=$'"'"'\t'"'"' read -r -a f <<<"$1"
  "$2/gate_probe.sh" "${f[0]}" "$3" "$4" "${f[@]:1}"' _ {} "$here" "$scr" "$out"
