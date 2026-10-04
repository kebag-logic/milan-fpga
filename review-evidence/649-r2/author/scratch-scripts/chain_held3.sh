#!/usr/bin/env bash
# Scratch (never committed): the three L2 points on the L1-cached core, in one hold of the shared lock.
set -u
W=$VALIDATION_STORAGE/649-a527/r2
date -Is > $W/chain_held3.queued
flock /tmp/milan-vivado.lock $W/bin/held_batch.sh l1l2-8k l1l2-16k l1l2-32k
echo "rc=$?"
