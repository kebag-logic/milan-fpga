#!/bin/bash
# usage: run.sh <commit-or-WT> ; plants each stricter-L6 defect in a fresh copy and runs the gate
set -u
src=$LANES/ppC8-desc-lint
base=$1
out=$VALIDATION_STORAGE/c8-a504/plants/$base
rm -rf "$out"; mkdir -p "$out"
for name in CONTROL aaf-single-beside-crf aaf-refused-beside-crf count-cap-8 count-cap-9 one-source-per-input-overall; do
  d=$out/$name; mkdir -p "$d/tree"
  if [ "$base" = WT ]; then
    (cd $src && git ls-files -z | tar --null -T - -cf -) | tar -xf - -C "$d/tree"
  else
    (cd $src && git archive "$base") | tar -xf - -C "$d/tree"
  fi
  if [ "$name" != CONTROL ]; then python3 $VALIDATION_STORAGE/c8-a504/plants/plant.py "$d/tree" "$name" || { echo "$base $name PLANT FAILED"; continue; }; fi
  (cd "$d/tree/tb/desc_store" && python3 -B test_gen_desc_image.py > "$d/gate.log" 2>&1); echo $? > "$d/rc"
  failing=$(grep -E "^(FAIL|ERROR): " "$d/gate.log" | sed -E 's/^(FAIL|ERROR): ([a-z_0-9]+) \(__main__\.([A-Za-z]+)\.[a-z_0-9]+\).*/\3.\2/' | sort -u | tr '\n' ' ')
  echo "$base $name rc=$(cat $d/rc) failing: $failing"
done
