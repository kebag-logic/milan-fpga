#!/bin/bash
# PROBE ONLY: the 1x1 aecp group with the acknowledgement later than the contract allows (256, then 1024 bus cycles).
set -u
P=$MANAGEMENT/2026-09-23/665s1-a680j/probes
W=$VALIDATION_STORAGE/scratch/665s1-a680j-work/probe
for N in 256 1024; do
  git -C "$W" apply "$P/probe-ack-$N.diff"
  "$P/leg.sh" "$W" "probe-ack$N-1x1" 1x1 --groups aecp --jobs 4
  git -C "$W" checkout -q tb/verilator/ctrl_service_budget/split_soc.py
done
