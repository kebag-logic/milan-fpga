#!/bin/bash
# Round-4 identity evidence: base 334e9fe6 against head, in one file.
# Usage: compare.sh > compare.txt
set -u
S=<scratch>/r4
M=<manager>/parent-consumer
strip() { sed -E 's#<data>/[^ :"]*##g; s#<tmp>/[^ :"]*##g' "$1"; }
echo "== engine suite log, base vs head (paths removed)"
diff <(strip "$S/gates/base/engine.log") <(strip "$S/gates/head/engine.log")
echo "diff rc $?"
echo
echo "== engine mutation arm, 18 shard logs, base vs head, byte for byte"
for k in $(seq 0 17); do
  cmp -s "$S/gates/base/engine-mutants-s$k.log" "$S/gates/head/engine-mutants-s$k.log"
  echo "s$k cmp rc $?"
done
echo "caught lines: base $(cat "$S"/gates/base/engine-mutants-s*.log | grep -c '^\[PASS\] mutant caught')," \
     "head $(cat "$S"/gates/head/engine-mutants-s*.log | grep -c '^\[PASS\] mutant caught')"
echo "named failure lines printed: base $(cat "$S"/gates/base/engine-mutants-s*.log | grep -c '^FAIL ')," \
     "head $(cat "$S"/gates/head/engine-mutants-s*.log | grep -c '^FAIL ')"
echo
echo "== branch meta-run, base vs head"
for h in 0 1; do
  cmp -s "$S/gates/meta/base-$h.log" "$S/gates/meta/head-$h.log"
  echo "half $h cmp rc $?"
done
echo
echo "== parent consumer logs: manager's run at 334e9fe6 vs this run at acfef36b (paths removed)"
for i in 01 02 03 04 05 06 07 08 09 10 11; do
  f=$(ls "$S"/gates/consumer-head-*/"$i".log)
  n=$(diff <(strip "$M/$i.log") <(strip "$f") | grep -c '^[<>]')
  echo "$i: $n differing line(s)"
done
