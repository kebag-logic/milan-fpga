#!/usr/bin/env bash
# Behavioural probes P1..P3 on a scratch copy of the exact head (RTL untouched).
# Receipt: receipts/probes-head-maap.log
source "$(dirname "$0")/common.sh"
T=$SCRATCH/probes
export_tree "$T"
python3 "$PACKET/probes/insert_probes.py" "$T/tb/maap/sim_main.cpp"
run_target "$T" maap run "$RECEIPTS/probes-head-maap.log"
grep -E '^FAIL|^  P[0-9]' "$RECEIPTS/probes-head-maap.log" || true
