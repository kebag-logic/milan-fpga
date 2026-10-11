#!/bin/bash
# Usage: probe_short_leg.sh <milan_dp dir with a built obj_gmstep> <full-leg suite log> <out dir>
# 1. Argument handling of Vmilan_dp_gmstep: each malformed call must exit 2.
# 2. The short leg (--no-small-steps, flag before and after the feed delay)
#    must print the full leg's check names minus one contiguous "621:" block.
set -u
dp=$1; full=$2; out=$3
mkdir -p "$out"
exe=./obj_gmstep/Vmilan_dp_gmstep
img=obj_gmstep/aemi.bin
cd "$dp" || exit 2
fail=0
expect2() {
  "$exe" "$@" > /dev/null 2>&1; rc=$?
  printf 'args=[%s] rc=%s\n' "$*" "$rc"
  [ "$rc" = 2 ] || { echo "  UNEXPECTED: wanted 2"; fail=1; }
}
expect2
expect2 --no-small-steps
expect2 "$img" 0 --bogus
expect2 "$img" --no-small-steps --no-small-steps
expect2 "$img" 0 1
expect2 "$img" -5
expect2 "$img" 1000000
expect2 /nonexistent.bin --no-small-steps
"$exe" "$img" --no-small-steps > "$out/short_flag_last.log" 2>&1; echo "short (flag last) rc=$?"
"$exe" --no-small-steps "$img" 0 > "$out/short_flag_first.log" 2>&1; echo "short (flag first, delay 0) rc=$?"
names() { grep -E '^\s*\[ ?(ok|FAIL) ?\]' "$1" | sed -E 's/^\s*\[ ?(ok|FAIL) ?\] //; s/ got=.*//'; }
sed -n '/gmstep: 2 MHz fabric/,/== gmstep: checks/p' "$full" > "$out/full_leg.log"
names "$out/full_leg.log" > "$out/full.names"
names "$out/short_flag_last.log" > "$out/short.names"
names "$out/short_flag_first.log" > "$out/short_first.names"
first=$(grep -n '^621: ' "$out/full.names" | head -1 | cut -d: -f1)
last=$(grep -n '^621: ' "$out/full.names" | tail -1 | cut -d: -f1)
echo "full=$(wc -l < "$out/full.names") short=$(wc -l < "$out/short.names") phase block lines $first-$last"
# The phase block holds only its own "621:" checks and the shared licence
# grader it calls; anything else inside it would be a check the flag drops.
sed -n "${first},${last}p" "$out/full.names" | sed -E 's/:.*//' | sort | uniq -c
others=$(sed -n "${first},${last}p" "$out/full.names" | grep -v -c -E '^(621|licence): ')
echo "checks in the block that are neither 621 nor licence: $others"
[ "$others" = 0 ] || fail=1
sed "${first},${last}d" "$out/full.names" > "$out/full_minus_block.names"
cmp "$out/full_minus_block.names" "$out/short.names" && echo "short == full minus the contiguous phase block" || fail=1
cmp "$out/short.names" "$out/short_first.names" && echo "flag position does not matter" || fail=1
grep -q 'RESULT: PASS' "$out/short_flag_last.log" || fail=1
echo "probe_short_leg verdict: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
