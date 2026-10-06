#!/bin/bash
# r_mutant.sh PATCH SUITE GROUP : plant PATCH in a fresh export of the reviewed head
# under scratch/rm-<label>-<suite>, build and run SUITE (RUN_ARGS=GROUP, empty = default).
set -u
P=${P:-$REVIEWS/pp134-r488-3-packet}
. "$P/scripts/env.sh"
patch=$1; suite=$2; group=${3:-}
label=$(basename "$patch" .patch)
dir=$P/scratch/rm-$label-$suite${group:+-$group}
rm -rf "$dir"; mkdir -p "$dir"
git -C "${CLONE:-$REVIEWS/r488-3-pp134}" archive "${HEAD_SHA:-ffc3a8e5733202384e55ea9094569cca86b78261}" | tar -x -C "$dir"
( cd "$dir" && git apply --check "$patch" && git apply "$patch" ) || { echo "PLANT FAILED"; exit 90; }
echo "planted $label"
make -C "$dir/tb/$suite" ${group:+RUN_ARGS=$group}
