#!/usr/bin/env bash
# Per-item checks on the lane worktree: quick gates, table check, matrix audit, per-listing, full --mutants campaign.
# usage: item_check.sh <receipt subdir> [jobs]
set -u
out=$MANAGEMENT/2026-09-23/833-a726h/receipts/$1; jobs=${2:-8}
mkdir -p "$out"
export TMPDIR=$VALIDATION_STORAGE/833-a726h/tmp PYTHONDONTWRITEBYTECODE=1
lane=$LANES/833-owned-process
grep SigIgn /proc/self/status > "$out/sigign.txt"
bash $VALIDATION_STORAGE/833-a726h/tools/quick.sh "$lane" "$out/quick"; q=$?
python3 -I -B $VALIDATION_STORAGE/833-a726h/tools/table_check.py "$lane" > "$out/table_check.log" 2>&1; t=$?; echo $t > "$out/table_check.rc"
echo "table_check rc $t: $(tail -n 3 "$out/table_check.log" | tr '\n' ' ')"
python3 -I -B $VALIDATION_STORAGE/833-a726h/probes/per_listing.py "$lane" > "$out/per_listing_none.log" 2>&1; p=$?; echo $p > "$out/per_listing_none.rc"
echo "per_listing none rc $p: $(tail -n 1 "$out/per_listing_none.log")"
cd "$lane" && cat /proc/loadavg > "$out/mutants.load"
python3 -B scripts/test_suite_cancellation.py --mutants --jobs "$jobs" > "$out/mutants.log" 2>&1; m=$?; echo $m > "$out/mutants.rc"
cat /proc/loadavg >> "$out/mutants.load"
echo "mutants rc $m: $(grep -A20 '^owned-process mutants' "$out/mutants.log")"
wc -l scripts/test_suite_cancellation.py scripts/process_test_support.py
[ $q -eq 0 ] && [ $t -eq 0 ] && [ $p -eq 0 ] && [ $m -eq 0 ]
