#!/usr/bin/env bash
# R436-2's pause_fuzz.cpp, unchanged, on the exact head's port at TMO $1:
# legal, silent, resume and babble, seeds 11-13, 600 operations each.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
T=$1; out=$P/scratch/r436-2-fuzz/$T
rm -rf "$out"; mkdir -p "$out"
"$P/scratch/r436-2/scripts/build_fuzz.sh" "$P/scratch/headexp/hdl/packet_engine/KL_pp_nvm_port.sv" "$T" "$out" || { echo "build rc $?"; exit 2; }
for m in legal silent resume babble; do for s in 11 12 13; do
  printf '%s seed %s: ' "$m" "$s"; "$out/Vfuzz" $m $s 600 | grep -E '^pause_fuzz|checks:' | tr '\n' ' '; echo
done; done
