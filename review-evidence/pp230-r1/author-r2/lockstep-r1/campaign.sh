#!/usr/bin/env bash
# Scratch: the lockstep campaign. usage: campaign.sh <hdl/srp under test> <tag> <cycles>
# Shapes: 2/2 (1x1 shipping), 9/9 (8x8), 1/1, 3/5, 8/8 with compressed cadences; 2/2 with the default cadences.
set -u
L=$VALIDATION_STORAGE/pp230-a523/lockstep
NEW=$1; TAG=$2; CYC=$3
cd $L
for shape in "n2 2 2 6 5 23 37" "n9 9 9 7 5 23 37" "n1 1 1 6 5 23 37" "n35 3 5 7 4 17 29" "n8 8 8 7 6 31 41" "n2d 2 2 6 200 1000 5000"; do
  set -- $shape
  o=$L/camp-$TAG/$1
  ./build.sh $NEW $o $2 $3 $4 $5 $6 $7 > /dev/null 2>&1 || { echo "BUILD-FAIL $1"; exit 3; }
  for sd in $(seq 1 8); do
    $o/obj/Vlockstep $((1000 * sd + ${#1})) $CYC $((sd % 3))
  done
done
