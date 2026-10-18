#!/usr/bin/env bash
# Run sections of an already-built tb/pp_top first build (obj_dir/Vpp_top_sim)
# in parallel, one log and rc per section.
# usage: run_sections.sh <tree> <outdir> <tag> <jobs> <section-flag>...
set -u
tree=$1; out=$2; tag=$3; jobs=$4; shift 4
mkdir -p "$out"
printf '%s\n' "$@" | xargs -P "$jobs" -I{} sh -c '
  cd "$1/tb/pp_top" || exit 1
  timeout 560 stdbuf -oL ./obj_dir/Vpp_top_sim --{} >"$2/$3_{}.log" 2>&1
  echo $? >"$2/$3_{}.rc"' _ "$tree" "$out" "$tag"
for s in "$@"; do
  echo "$tag $s rc=$(cat "$out/${tag}_$s.rc") fails=$(grep -c '^FAIL' "$out/${tag}_$s.log") $(grep -E '^\[build' "$out/${tag}_$s.log" | tail -1)"
done
