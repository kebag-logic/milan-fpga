#!/usr/bin/env bash
# Compare head vs base mutation-campaign outputs written by run_campaign.sh.
# Usage: compare_campaigns.sh <campaigns-dir>
# For each campaign: diff the runner's stdout (paths normalised), and for
# every per-variant log diff its FAIL: lines and check-tally lines.
set -u
d=$1; bad=0
norm() { sed -E "s#$d/(head|base)-#<OUT>/#g; s#/tmp/[^ /]+#<TMP>#g"; }
for c in desc gsi srp; do
  if diff <(norm < "$d/head-$c/stdout.txt") <(norm < "$d/base-$c/stdout.txt") > /dev/null; then
    echo "$c runner stdout: IDENTICAL ($(wc -l < "$d/head-$c/stdout.txt") lines)"
  else
    echo "$c runner stdout: DIFFERENT"; diff <(norm < "$d/head-$c/stdout.txt") <(norm < "$d/base-$c/stdout.txt"); bad=1
  fi
  for f in "$d/head-$c"/logs/*.log; do
    b="$d/base-$c/logs/$(basename "$f")"
    x=$(grep -E '^FAIL|checks[:,]|[0-9]+ checks' "$f" | norm)
    y=$(grep -E '^FAIL|checks[:,]|[0-9]+ checks' "$b" | norm)
    if [ "$x" = "$y" ]; then s=IDENTICAL; else s=DIFFERENT; bad=1; fi
    echo "  $(basename "$f"): FAIL/tally lines $s; $(grep -E 'checks[:,]|[0-9]+ checks' "$f" | tr '\n' ' ' | cut -c1-160)"
  done
done
echo "CAMPAIGN COMPARISON: $([ $bad = 0 ] && echo IDENTICAL || echo DIFFERENT)"
exit $bad
