#!/usr/bin/env bash
# Reviewer receipt driver: build tb/pp_top's first (all-sections) binary in a
# disposable tree and run it whole and with --gsi-internal-only.
# Usage: build_and_run.sh <tree> <receipt dir> <verilator> <build jobs>
set -u
tree=$1 out=$2 vl=$3 bj=$4
mkdir -p "$out"
git -C "$tree" rev-parse HEAD > "$out/HEAD.txt"
git -C "$tree" status --porcelain > "$out/STATUS.txt"
git -C "$tree" diff HEAD > "$out/DIFF-vs-HEAD.patch"
"$vl" --version > "$out/verilator-version.txt"
date -u +%FT%TZ > "$out/start"
make -C "$tree/tb/pp_top" gsi-build VERILATOR="$vl --build-jobs $bj" \
  > "$out/build.log" 2>&1
echo $? > "$out/build.rc"
if [ "$(cat "$out/build.rc")" = 0 ]; then
  (cd "$tree/tb/pp_top" && ./obj_dir/Vpp_top_sim) > "$out/full.log" 2>&1
  echo $? > "$out/full.rc"
  (cd "$tree/tb/pp_top" && ./obj_dir/Vpp_top_sim --gsi-internal-only) \
    > "$out/gsi-internal.log" 2>&1
  echo $? > "$out/gsi-internal.rc"
fi
date -u +%FT%TZ > "$out/end"
