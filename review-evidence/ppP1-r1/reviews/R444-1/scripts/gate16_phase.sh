#!/usr/bin/env bash
# R444-1: run the parent's tdm8render (gate 16's shipping leg) in one scratch
# parent copy. Usage: gate16_phase.sh PARENT_COPY LOG
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd "$1/tb/verilator/milan_dp_render" || exit 9
{ date -u +%FT%TZ; git -C "$1" rev-parse HEAD; git -C "$1/protocol-processor" rev-parse HEAD
  git -C "$1" diff --stat; make tdm8render VERILATOR_JOBS=4; echo "rc=$?"; date -u +%FT%TZ; } > "$2" 2>&1
