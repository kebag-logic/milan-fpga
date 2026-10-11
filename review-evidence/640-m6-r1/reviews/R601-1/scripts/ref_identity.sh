#!/bin/sh
# R601-1: the lockstep references equal the dev base modules apart from the name.
# Usage: ref_identity.sh <clone> <base-sha>
# Prints, per reference, the diff between the base module (with the module
# name rewritten to the _ref name) and the committed reference at HEAD.
set -u
cd "$1" || exit 2
B=$2
for p in avtp/KL_avtp_rx_monitor_ctx:avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref \
         aaf/KL_chan_map_capture:chmap_capture/reference/KL_chan_map_capture_ref; do
  a=${p%%:*}; r=${p##*:}; n=$(basename "$a")
  echo "== $r.sv vs $B:hdl/ieee1722/$a.sv (name rewritten)"
  git show "$B:hdl/ieee1722/$a.sv" | sed "s/\b$n\b/${n}_ref/g" | diff - "tb/verilator/$r.sv"
  echo "diff rc=$?"
done
