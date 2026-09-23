#!/usr/bin/env bash
# Reproduce the PR's headline failing arms independently: plant earlier
# versions of whole files into copies of the head tree and run the suites.
#   X1 base encoder (fbc1f715)                     -> srp_encoder
#   X2 previous decoder (9370f8ab)                 -> srp_decoder
#   X3 previous receive side (9370f8ab: decoder, both FSMs, KL_srp_top,
#      srp_pkg)                                    -> srp_top
# Usage: 05_plant_previous.sh <scratch> <verilator>
set -uo pipefail
scratch=$1; vl=$2; here=$(cd "$(dirname "$0")" && pwd)
plant() { # id src-tree files...
  local id=$1 src=$2; shift 2
  rm -rf "$scratch/plant-$id"; cp -a "$scratch/head" "$scratch/plant-$id"
  for f in "$@"; do cp "$scratch/$src/$f" "$scratch/plant-$id/$f"; done
}
plant X1 base hdl/srp/KL_srp_encoder.sv
plant X2 mid  hdl/srp/KL_srp_decoder.sv
plant X3 mid  hdl/srp/KL_srp_decoder.sv hdl/srp/KL_srp_talker_fsm.sv \
              hdl/srp/KL_srp_listener_fsm.sv hdl/srp/KL_srp_top.sv hdl/srp/srp_pkg.sv
for id in X1 X2 X3; do
  case $id in X1) s=srp_encoder;; X2) s=srp_decoder;; X3) s=srp_top;; esac
  echo "$id $("$here/01_run_suites.sh" "$scratch/plant-$id" "$vl" "$scratch/plant-$id/logs" "$s")"
done
