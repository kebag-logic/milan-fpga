#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run tb/name_state on the generated parent images, plain and --measure.
# usage: gen_image_runs.sh CLONE OUTDIR VERILATOR IMG1x1 IMG8x8
set -eu
clone=$1; out=$2; vl=$3; img1=$4; img8=$5
mkdir "$out"
for spec in "1x1 1 $img1" "8x8 8 $img8"; do
  set -- $spec
  for mode in plain measure; do
    tag=gen-$1-$mode; mkdir "$out/w-$tag"
    extra=; [ $mode = measure ] && extra=--measure
    set +e
    python3 -B "$clone/tb/name_state/run.py" --root "$clone" --verilator "$vl" \
        --work "$out/w-$tag" --image "$3" --aaf $2 $extra > "$out/$tag.log" 2>&1
    echo $? > "$out/$tag.rc"
    set -e
  done
done
