#!/usr/bin/env bash
# Scratch (never committed): the round-2 Vivado work in one hold of the shared lock (each run about 2 minutes).
set -u
W=$VALIDATION_STORAGE/649-a527/r2
date -Is > $W/chain_held2.queued
flock /tmp/milan-vivado.lock $W/bin/held_batch.sh ship route-map-3 l2-8k l2-16k l2-32k cpu2 cpu4 rv64 rv64-fpu \
  isa-m isa-mf isa-mfd l1-fetch l1-caches l1-w2 l1-w4 naxriscv naxriscv-rv64
echo "rc=$?"
