#!/usr/bin/env bash
# stream.sh <head> <group>...: each group's gates on its own fresh clean clone of <head>, one group after another.
set -u
H=$1; shift; S=$VALIDATION_STORAGE/scratch/851-a744b; here=$(cd "$(dirname "$0")" && pwd)
for grp in "$@"; do
  W=$S/g-$grp-${H:0:8}; G=$S/gates-${H:0:8}/$grp
  [ -d "$W" ] || bash "$here/make_clone.sh" "$W" "$H" > "$S/clone-$grp-${H:0:8}.log" 2>&1 || { echo "clone $grp failed"; continue; }
  bash "$here/lane_gates.sh" "$H" "$grp" "$W" "$G"
done
