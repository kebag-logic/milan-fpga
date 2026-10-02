#!/bin/bash
# usage: compare_runs.sh A B  -- compares two runs' summaries (stdout) byte for byte, and
# every receipt's FAIL lines and tally lines (and results.json where present).
P=$REVIEWS/pp143-r440-1-packet/receipts
a=$1; b=$2
if cmp -s $P/runs/$a.stdout $P/runs/$b.stdout; then echo "summary IDENTICAL ($(wc -l < $P/runs/$a.stdout) lines)"; else echo "summary DIFFERS"; /usr/bin/diff $P/runs/$a.stdout $P/runs/$b.stdout | head -20; fi
la=$(cd $P/$a && ls | sort); lb=$(cd $P/$b && ls | sort)
[ "$la" = "$lb" ] && echo "receipt set IDENTICAL ($(echo "$la" | wc -l) files)" || echo "receipt set DIFFERS"
bad=0; fails=0
for f in $la; do
  ka=$(grep -aE '^FAIL|checks|PASS, [0-9]+ FAIL|failures|^return code|tally|line guards' $P/$a/$f | sed 's/[0-9.]* s\b//g' | grep -av 'Verilator\|wall\|elapsed\|time')
  kb=$(grep -aE '^FAIL|checks|PASS, [0-9]+ FAIL|failures|^return code|tally|line guards' $P/$b/$f | sed 's/[0-9.]* s\b//g' | grep -av 'Verilator\|wall\|elapsed\|time')
  [ "$ka" = "$kb" ] || { bad=$((bad+1)); echo "  receipt differs: $f"; }
  fails=$((fails + $(grep -ac '^FAIL' $P/$a/$f)))
done
echo "receipts with differing FAIL/tally lines: $bad; FAIL lines in $a: $fails"
[ -e $P/$a/results.json ] && { cmp -s $P/$a/results.json $P/$b/results.json && echo "results.json IDENTICAL" || echo "results.json DIFFERS"; }
echo "rc: $(cat $P/runs/$a.rc) $(cat $P/runs/$b.rc); wall: $(grep wall_s $P/runs/$a.meta) $(grep wall_s $P/runs/$b.meta)"
