#!/usr/bin/env bash
# camp_compare.sh <name>: base and head campaign logs, with run-specific text masked
# (the label in output paths, temp-directory suffixes, seconds), diffed in order and,
# for drivers that print arms in completion order, as sorted line multisets.
n=$1; R=<scratch>/rec
mask() { sed -E -e 's#<scratch>/rec/(base|head)/#REC/#g' \
  -e 's#/tmp/[A-Za-z0-9_.-]*-[A-Za-z0-9_]{8}#/tmp/T#g' -e 's#tmp[A-Za-z0-9_]{8}#T#g' \
  -e 's/[0-9]+(\.[0-9]+)? ?(s|sec|seconds|ms)\b/S/g' "$1"; }
if diff <(mask $R/base/camp_$n.log) <(mask $R/head/camp_$n.log) > $R/cmp_$n.diff; then
  echo "$n: IDENTICAL ($(wc -l < $R/head/camp_$n.log) lines)"
elif diff <(mask $R/base/camp_$n.log | sort) <(mask $R/head/camp_$n.log | sort) > $R/cmp_$n.sorted.diff; then
  echo "$n: IDENTICAL as sorted lines ($(wc -l < $R/head/camp_$n.log) lines; arms print in completion order)"
else
  echo "$n: DIFFERS on $(grep -c '^[<>]' $R/cmp_$n.sorted.diff) sorted line(s)"
fi
