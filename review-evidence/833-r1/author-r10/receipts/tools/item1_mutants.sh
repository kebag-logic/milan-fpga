#!/usr/bin/env bash
# Item 1: every owner_report mutant on the fix, with its words, once and then 20 times each under load.
set -u
S=$VALIDATION_STORAGE/833-a726j
R=$MANAGEMENT/2026-09-23/833-a726j/receipts/item1
export TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1
cd "$S/wt-item1" || exit 2
read -r -a names < "$S/report-mutants.txt"
grep SigIgn /proc/self/status > "$R/report-mutants.sigign"
cat /proc/loadavg > "$R/report-mutants.load"
python3 -B scripts/test_suite_cancellation.py --mutants "${names[@]}" --jobs 6 > "$R/report-mutants.log" 2>&1
echo $? > "$R/report-mutants.rc"
cat /proc/loadavg >> "$R/report-mutants.load"
cat "$R/report-mutants.log"
for i in $(seq 1 20); do
  python3 -B scripts/test_suite_cancellation.py --mutants "${names[@]}" --jobs 6 > "$R/report-mutants-rep-$i.log" 2>&1
  echo "$i $?" >> "$R/report-mutants-rep.rc"
done
cat /proc/loadavg >> "$R/report-mutants.load"
grep -h "^owned-process mutants" "$R"/report-mutants-rep-*.log | sort | uniq -c
awk '{print $2}' "$R/report-mutants-rep.rc" | sort | uniq -c
