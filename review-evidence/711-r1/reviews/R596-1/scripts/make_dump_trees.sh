#!/usr/bin/env bash
# Two instrumented trees (base e8454e27, head 49b437f4) whose host mailbox model
# appends every SRP-channel TX frame, and a marker at every model reset, to
# $R596_DUMP/<sanitised argv0>.txt. Only sw/firmware/ctrl/host/mbx_model.c changes.
set -euo pipefail
SRC=${SRC:-$REVIEWS/r596-1-711}
P=$REVIEWS/711-r596-1-packet
S=$P/scratch
for pair in "head-dump 49b437f445e34b558106c8799c1ffc0a5dc844cf" "base-dump e8454e2751d05b02ee8e5a571857589ab358ab86"; do
  set -- $pair
  git clone -q --shared --no-checkout "$SRC" "$S/$1"
  git -C "$S/$1" -c advice.detachedHead=false checkout -q --detach "$2"
  for m in protocol-processor gptp-processor third_party/verilog-axis; do
    git clone -q "$SRC/$m" "$S/$1/$m"
    git -C "$S/$1/$m" -c advice.detachedHead=false checkout -q "$(git -C "$SRC" rev-parse "$2:$m")"
  done
  python3 -I "$P/scripts/instrument_model.py" "$S/$1/sw/firmware/ctrl/host/mbx_model.c"
  git -C "$S/$1" diff --stat | tail -1
done
