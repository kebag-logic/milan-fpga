#!/usr/bin/env bash
# usage: run_census_cases.sh <trees-dir containing head/ and r1/> <scratch> <out> <jobs>
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
trees=$1 scr=$2 out=$3 jobs=$4
mkdir -p "$out"
sed "s|^\([a-z0-9]*\)\t|$trees/\1\t|" "$here/census_cases.txt" | tr '\n' '\0' | xargs -0 -P "$jobs" -I{} bash -c '
  IFS=$'"'"'\t'"'"' read -r -a f <<<"$1"
  "$2/census_probe.sh" "${f[0]}" "$3" "$4" "${f[@]:1}"' _ {} "$here" "$scr" "$out"
