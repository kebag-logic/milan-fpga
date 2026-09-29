#!/bin/sh
# Run the HEAD tb/maap suite against the RTL of earlier commits, to check the
# round's "fails at the start head" claims:
#   b03d36f  the round-2 start head (before 4de2c60 and 8ae76ee)
#   4de2c60  after the Release! rework, before the seed re-arm (8ae76ee)
set -u
. "$(dirname "$0")/00_env.sh"
S="$PKT/scratch/head"
R="$PKT/receipts/prior-rtl"
mkdir -p "$R"; : > "$R/summary.txt"
for c in b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 4de2c60; do
  T="$PKT/scratch/prior-$c"
  rm -rf "$T"; mkdir -p "$T/tb"
  git -C "$CLONE" archive "$c" hdl | tar -x -C "$T"
  cp -r "$S/tb/maap" "$S/tb/common" "$T/tb/"
  rm -rf "$T/tb/maap/obj_dir"
  make -C "$T/tb/maap" VERILATOR="$VLT" run > "$R/head-tb-on-$c-rtl.log" 2>&1
  rc=$?
  {
    echo "head tb/maap on $c RTL: rc=$rc $(grep -E '^[0-9]+ checks:' "$R/head-tb-on-$c-rtl.log")"
    for u in U17b U17c U18b U23 U24 U25 U26 U27 U28; do
      n=$(grep -c "^FAIL: $u:" "$R/head-tb-on-$c-rtl.log")
      [ "$n" -gt 0 ] && echo "  $u: $n FAIL"
    done
  } | tee -a "$R/summary.txt"
done
