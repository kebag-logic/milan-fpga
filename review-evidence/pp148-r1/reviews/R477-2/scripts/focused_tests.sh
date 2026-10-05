#!/usr/bin/env bash
# Focused behaviour checks at one revision in a disposable copy: tb/aecp_notify
# `make run` (TW1/TW2 figures) and tb/pp_top gsi-build `--spacing-only` (CS).
# Both run concurrently; each has its own log and rc file.
# Usage: focused_tests.sh <repo> <rev> <scratch-dir> <verilator> <receipts-dir>
set -uo pipefail
repo=$1 rev=$2 scr=$3 vl=$4 out=$5
rm -rf "$scr"; mkdir -p "$scr" "$out"
git -C "$repo" archive "$rev" | tar -x -C "$scr"
( cd "$scr/tb/aecp_notify" && make VERILATOR="$vl" run > "$out/aecp_notify-run.log" 2>&1; echo $? > "$out/aecp_notify-run.rc" ) &
( cd "$scr/tb/pp_top" && make -j16 VERILATOR="$vl" gsi-build > "$out/pp_top-gsi-build.log" 2>&1 \
    && ./obj_dir/Vpp_top_sim --spacing-only > "$out/pp_top-spacing-only.log" 2>&1; echo $? > "$out/pp_top-spacing-only.rc" ) &
wait
echo "aecp_notify run rc=$(cat "$out/aecp_notify-run.rc")"; echo "pp_top spacing-only rc=$(cat "$out/pp_top-spacing-only.rc")"
