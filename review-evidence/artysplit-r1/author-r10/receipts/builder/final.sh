#!/bin/sh
# Export the final head with its pinned submodules, build both placements there into a fresh output root, compare.
set -eu
B=$VALIDATION_STORAGE/r10/builder; W=$SOURCE
full=$(git -C $W rev-parse HEAD); short=$(echo $full | cut -c1-12); OUT=out-$short
[ -e $B/src-$short ] || { mkdir -p $B/src-$short; git -C $W archive $full | tar -x -C $B/src-$short
  git -C $W ls-tree -r $full | awk '$2=="commit"{print $3, $4}' | while read sha path; do
    mkdir -p $B/src-$short/$path; git -C $W/$path archive $sha | tar -x -C $B/src-$short/$path; done; }
for src in src-4adfa9dc84f5 src-011aaa6f0803 src-aa53840d9128 src-$short; do
  for placement in split all-fabric; do
    out=$B/$OUT/$src/$placement; [ -e $out ] && { echo "exists: $out"; exit 2; }; mkdir -p $out
    (cd $B/$src && python3 -I -B sw/builder/endstation_builder.py configs/endstation_arty_split.yaml --placement $placement -o $out) > $out.log 2>&1
    echo "$src $placement rc=$?"
  done
done
python3 -I -B $B/compare.py $full $OUT
