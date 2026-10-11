#!/usr/bin/env bash
# Run the srp_latency arm (IF=1 and IF=2) for every walk probe; 3 probes at a time.
# Writes receipts/walk/<probe>.log and receipts/walk/<probe>.rc, then summary.tsv
# (probe, lwSRP pin, expected verdict, observed rc, MATCH/MISMATCH).
set -uo pipefail
P=$REVIEWS/711-r596-1-packet
S=$P/scratch
OUT=$P/receipts/walk
mkdir -p "$OUT" "$S/probe-builds"
export TMPDIR=$S/tmp
MATRIX='head-exact lwsrp-new pass
base-exact lwsrp-old pass
e1-oldwalk-assert lwsrp-new fail
e2-newwalk-base lwsrp-old pass
e3-oldwalk-assert-base lwsrp-old pass
e4-pinonly lwsrp-new pass
m1-vecsize lwsrp-new fail
m2-noendskip lwsrp-new fail
m3-onevector lwsrp-new fail
m4-noassert-oldwalk lwsrp-new pass'
one() {
  set -- $1
  python3 -I "$P/scripts/latency_arm.py" "$S/probes/$1" "$S/probe-builds/$1" "$S/$2" > "$OUT/$1.log" 2>&1
  echo $? > "$OUT/$1.rc"
}
export -f one; export P S OUT
printf '%s\n' "$MATRIX" | xargs -P 3 -I{} bash -c 'one "$@"' _ {}
: > "$OUT/summary.tsv"
while read -r name lw want; do
  rc=$(cat "$OUT/$name.rc"); got=$([ "$rc" = 0 ] && echo pass || echo fail)
  printf '%s\t%s\t%s\trc=%s\t%s\n' "$name" "$lw" "$want" "$rc" "$([ "$got" = "$want" ] && echo MATCH || echo MISMATCH)" >> "$OUT/summary.tsv"
done <<< "$MATRIX"
cat "$OUT/summary.tsv"
