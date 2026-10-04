#!/usr/bin/env bash
# Scratch (never committed): the round-2 Vivado work in two holds of the shared lock.
set -u
W=$VALIDATION_STORAGE/649-a527/r2
date -Is > $W/chain_held.queued
flock /tmp/milan-vivado.lock $W/bin/held_batch.sh ship route-map-3 l2-8k l2-16k l2-32k cpu2 cpu4 rv64 rv64-fpu || exit 1
flock /tmp/milan-vivado.lock $W/bin/held_batch.sh isa-m isa-mf isa-mfd l1-fetch l1-caches l1-w2 l1-w4 naxriscv naxriscv-rv64
