#!/bin/sh
# [R312] round-4 residual search (new this round; no earlier R312 packet held a
# script of this name). Read-only. Usage: residual_search.sh <repo root>
# 1. Every tracked line naming the capture hold / its measurement, with the
#    neighbouring line, so the reader can grade who owns it.
# 2. Every tracked line naming processor #61/#83 or the donor together with a
#    capture-hold/#559 word AND an ownership word (measure, obligation, owner,
#    owns, responsible, resolve) on the same or an adjacent line.
# 3. Every link to the withdrawn obligation comment or to the removed anchor text.
# Exit 1 if section 2 or 3 finds anything; section 1 is a listing for grading.
set -u
cd "$1" || exit 2
echo "# head $(git rev-parse HEAD)"
echo "## 1. capture-hold mentions (tracked text files)"
git grep -n -I -i -E 'capture[- ]hold|hold measurement|hold margin|T_HOLD_MS' -- . ':!third_party' | sort
echo "## 2. donor/#61/#83 x hold/measure/#559 (same or adjacent line)"
hits=0
for f in $(git ls-files -- '*.md' '*.txt' '*.py' '*.c' '*.h' '*.sv' '*.yml' '*.yaml'); do
  awk -v F="$f" '
    { l[NR]=$0 }
    END {
      for (i=1;i<=NR;i++) {
        w = l[i-1] " " l[i] " " l[i+1]
        a = (l[i] ~ /(#61|#83|61\/#83|[Dd]onor)/)
        b = (w ~ /([Cc]apture[- ]hold|hold measurement|hold margin|issues\/559|#559|measure(ment)? .*hold)/)
        c = (w ~ /([Mm]easur|[Oo]bligation|[Oo]wner([^s]|$)|[Oo]wners([^h]|$)|[Oo]wns|[Rr]esponsib|[Rr]esolv)/)
        if (a && b && c) print F ":" i ": " l[i]
      }
    }' "$f"
done > /tmp/r312_4_rs2.$$
cat /tmp/r312_4_rs2.$$; [ -s /tmp/r312_4_rs2.$$ ] && hits=1; rm -f /tmp/r312_4_rs2.$$
echo "## 2b. every #559 citation (listing for grading)"
git grep -n -I -E 'issues/559|#559' -- . | sort
echo "## 3. withdrawn-obligation links / removed wording"
if git grep -n -I -E 'capture-hold measurement obligation|issuecomment-5823590638|issuecomment-5823589125|#61/#83 adoption must measure|must also satisfy the' -- . ; then hits=1; fi
echo "hits=$hits"
exit $hits
