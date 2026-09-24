#!/usr/bin/env bash
# Extract the exact reviewed head into a disposable tree and run the focused suites.
# CPU use is capped at 8 cores with taskset.
# Usage: CLONE=<clone> PACKET=<packet> VERILATOR=<verilator 5.050> bash 00_extract_and_suites.sh
set -u
HEAD_SHA=cc077a6ffe20585d20b116f008e07189ba1bb7f8
CLONE=${CLONE:?}; PACKET=${PACKET:?}; VERILATOR=${VERILATOR:-verilator}
T=$PACKET/scratch/head
R=$PACKET/receipts
rm -rf "$T"; mkdir -p "$T" "$R"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$T"
git -C "$CLONE" rev-parse "$HEAD_SHA^{tree}" > "$R/00-tree.txt"
"$VERILATOR" --version > "$R/00-verilator-version.txt"
run() { # name, then command in $T
  local n=$1; shift
  ( cd "$T" && taskset -c 0-7 "$@" ) > "$R/$n.log" 2>&1
  echo "$n rc=$?" | tee -a "$R/00-rc.txt"
}
: > "$R/00-rc.txt"
export PATH="$(dirname "$VERILATOR"):$PATH"
run 01-guard-suite make -C tb/desc_mem_guard VERILATOR="$VERILATOR"
run 02-guard-baseline make -C tb/desc_mem_guard baseline VERILATOR="$VERILATOR"
run 03-mutant-controller python3 tb/desc_mem_guard/mutate.py --output "$PACKET/scratch/mutctl"
run 04-desc-store make -C tb/desc_store VERILATOR="$VERILATOR"
run 05-pp-top make -C tb/pp_top VERILATOR="$VERILATOR"
