#!/bin/sh
# Elaborate KL_nvm_backend alone at several N_NAME_P values at base and head
# with the pinned Verilator; print rc and the guard message for each.
# Usage: guard_parity.sh <scratch dir holding base/ and head/> <verilator>
S=$1; V=$2
for t in base head; do
  for n in 0 1 99 128 129 235; do
    d=$(mktemp -d "$S/vl.XXXXXX")
    "$V" --lint-only -Wall --Mdir "$d" --top-module KL_nvm_backend -GN_NAME_P=$n \
      "$S/$t/hdl/milan/KL_nvm_backend.sv" > "$d/out" 2>&1; rc=$?
    msg=$(grep -o 'KL_nvm_backend: N_NAME_P=[^"]*0xFF\.' "$d/out" | head -1)
    echo "$t N_NAME_P=$n rc=$rc msg=[$msg]"
    rm -rf "$d"
  done
done
