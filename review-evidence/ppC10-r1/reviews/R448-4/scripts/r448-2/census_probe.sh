#!/usr/bin/env bash
# One census probe: copy a pristine tree, add a module file with a given header
# layout (plant_census.py), optionally add its name to tops (plant.py add-top),
# run the Yosys gate. Writes <out>/<case>.log and <out>/<case>.rc.
# usage: census_probe.sh <tree> <scratch> <out> <case> <layout> <Name> <in-tops:yes|no> [clean]
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1 scr=$2 out=$3 case=$4 layout=$5 name=$6 intops=$7 clean=${8-}
t="$scr/census-$case"; rm -rf "$t"; mkdir -p "$t" "$out"; cp -a "$src/." "$t/"
{
  python3 "$here/plant_census.py" "$t" "$layout" "$name" $clean || exit 9
  if [ "$intops" = yes ]; then python3 "$here/plant.py" "$t" add-top "$name" || exit 9; fi
  "$t/syn/yosys/run.sh"
} >"$out/$case.log" 2>&1
echo $? >"$out/$case.rc"
rm -rf "$t"
echo "$case rc=$(cat "$out/$case.rc")"
