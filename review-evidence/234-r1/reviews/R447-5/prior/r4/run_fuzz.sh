#!/usr/bin/env bash
# Run the head's --fuzz mode on the fixtures and on real A measurements, at the author's seed and a reviewer seed,
# in parallel, one log and one rc file each. Read-only on the checkout and the measurement directories.
# Usage: run_fuzz.sh <repo checkout> <validation storage root holding A/> <output dir>
set -u
repo=$1 store=$2 out=$3
mkdir -p "$out"
gate="$repo/syn/ooc/pp_resource_gate.py"
jobs=(
  "fixtures-20000-s234|--fuzz 20000 --seed 234"
  "fixtures-20000-s4474|--fuzz 20000 --seed 4474"
  "A-route-20000-s234|--fuzz 20000 --seed 234 check $store/A/work/ax7101/gateware --endpoint route-1x1"
  "A-route-20000-s4474|--fuzz 20000 --seed 4474 check $store/A/work/ax7101/gateware --endpoint route-1x1"
  "A-ooc-1x1-5000-s234|--fuzz 5000 --seed 234 check $store/A/work/ax7101-ooc --endpoint ooc-1x1"
  "A-ooc-8x8-5000-s4474|--fuzz 5000 --seed 4474 check $store/A/work/ax8x8-ooc --endpoint ooc-8x8"
)
for job in "${jobs[@]}"; do
  name=${job%%|*} args=${job#*|}
  ( python3 -B "$gate" $args > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) &
done
wait
echo done > "$out/ALL.done"
