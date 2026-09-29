#!/bin/sh
# Export the exact head into scratch and run the focused suites the PR touches.
# Usage: 01_head_suites.sh export|maap|rx_validator|pp_top
set -u
. "$(dirname "$0")/00_env.sh"
T="$PKT/scratch/head"
R="$PKT/receipts/head"
mkdir -p "$R"
case "$1" in
  export)
    rm -rf "$T"; mkdir -p "$T"
    git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$T"
    "$VLT" --version > "$R/verilator-version.txt"
    sha256sum "$(dirname "$(sed -n 's/.*exec env VERILATOR_ROOT=[^ ]* \([^ ]*\) .*/\1/p' "$VLT")")/verilator_bin" >> "$R/verilator-version.txt" ;;
  maap|rx_validator)
    make -C "$T/tb/$1" VERILATOR="$VLT" run > "$R/$1-run.log" 2>&1
    echo "$1 run rc=$?" | tee -a "$R/rc.txt" ;;
  pp_top)
    make -C "$T/tb/pp_top" VERILATOR="$VLT" maap-internal > "$R/pp_top-maap-internal.log" 2>&1
    echo "pp_top maap-internal rc=$?" | tee -a "$R/rc.txt" ;;
esac
