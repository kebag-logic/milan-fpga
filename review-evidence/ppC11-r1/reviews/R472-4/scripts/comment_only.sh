#!/usr/bin/env bash
# Prove the lane's HDL/C++ edits are comment-only: compare comment-stripped
# preprocessed token streams of each file at the merged main and at the head.
# Usage: comment_only.sh <clone> <base> <head>
set -u
clone=$1 base=$2 head=$3 rc=0
for f in hdl/packet_engine/KL_pp_side_port.sv hdl/packet_engine/KL_pp_trace_ring.sv \
         hdl/packet_engine/KL_pp_tx_slots.sv tb/tx_slots/sim_main.cpp; do
  a=$(git -C "$clone" show "$base:$f" | g++ -x c++ -fpreprocessed -dD -E -P - 2>/dev/null | tr -s ' \t\n' ' ' | sha256sum)
  b=$(git -C "$clone" show "$head:$f" | g++ -x c++ -fpreprocessed -dD -E -P - 2>/dev/null | tr -s ' \t\n' ' ' | sha256sum)
  if [ "$a" = "$b" ]; then echo "COMMENT-ONLY $f ${a%% *}"; else echo "CODE CHANGED $f"; rc=1; fi
done
exit $rc
