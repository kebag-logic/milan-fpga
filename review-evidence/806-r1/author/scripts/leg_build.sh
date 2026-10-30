#!/usr/bin/env bash
# leg_build.sh <rev>: build the milan_dp gptp leg's binary in its own clean clone at <rev> (no run).
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/806-a701; C=$X/clone-leg-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" || exit 2
source "$D/env.sh"
make -C "$C/tb/verilator/milan_dp" build-gptp VERILATOR_JOBS=4
