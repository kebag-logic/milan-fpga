#!/bin/bash
# capture_probes.sh MUTROOT CAPS OUT: run the twin's comparison and its leave-all-omission plant with each grade
# variant under MUTROOT/tb/verilator/<name>/ (twin_mutants.py writes them) against one run's captures in CAPS.
#   unplanted: twin_compare.py fabric split -> the variant's finding count (the head's grade: 0)
#   omission:  the leave-all-omission plant made from the split capture, compared with the fabric's against the
#              unplanted report -> rc 0 when the plant is refused by its words
set -u
mutroot=$1 caps=$2 out=$3
mkdir -p "$out"
for name in control rla-after-txla rla-before-txla txlaf-unconditional; do
  dir=$mutroot/tb/verilator/$name
  work=$out/$name
  mkdir -p "$work"
  (cd "$dir" && python3 -B -E -s twin_compare.py "$caps/fabric.json" "$caps/split.json" \
      --report "$work/report.json" > "$work/unplanted.txt" 2>&1)
  unplanted=$?
  (cd "$dir" && python3 -B -E -s twin_compare.py "$caps/fabric.json" "$caps/split.json" \
      --make-plant leave-all-omission --out "$work/split-leave-all-omission.json" > "$work/make-plant.txt" 2>&1 &&
    python3 -B -E -s twin_compare.py "$caps/fabric.json" "$work/split-leave-all-omission.json" \
      --plant leave-all-omission --baseline "$caps/report.json" > "$work/plant.txt" 2>&1)
  plant=$?
  echo "$name: unplanted rc=$unplanted ($(tail -n 1 "$work/unplanted.txt" | cut -c1-60)); leave-all-omission rc=$plant ($(tail -n 1 "$work/plant.txt" | cut -c1-140))"
done
