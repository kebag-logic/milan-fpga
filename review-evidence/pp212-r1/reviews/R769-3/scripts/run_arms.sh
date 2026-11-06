#!/usr/bin/env bash
# Run the round 3 delta arms (new and re-cut) with their controls at the clone's head.
# usage: run_arms.sh <clone> <outdir> <jobs>
set -u
CLONE=$1; OUT=$2; JOBS=${3:-12}
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
export TMPDIR=${TMPDIR:-$REVIEWS/pp212-r769-3-packet/scratch/tmp}
ARMS=settled-link-flush-dropped,settled-link-unpublished,link-withdraw-dropped,link-clock-indicates,settled-link-keeps-lv-slot,lv-expiry-masked,link-begin-dropped,unarmed-indicates,unarmed-latency-strobe,unarmed-unregistered,r-sink-receive-priority-lost,unarmed-link-flush-dropped,keep-on-link-clock,pt-link-flush-dropped,top-listener-link-unwired,keep-declares-seed-type,keep-on-link-clock
"$VERILATOR" --version
cd "$CLONE" && git rev-parse HEAD
python3 tb/srp_top/mutants.py --output "$OUT/logs" --only "$ARMS" --jobs "$JOBS"
