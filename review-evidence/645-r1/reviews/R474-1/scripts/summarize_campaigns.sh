#!/bin/sh
# Summarise follow_ring sweep outputs: runs, rc, settle decisions, post-settle
# slips, worst empty/full margins and the largest pre-settle slip count.
#   sh summarize_campaigns.sh DIR...   (each DIR is one sweep.py --out)
set -eu
for d in "$@"; do
  name=$(basename "$d")
  runs=$(ls "$d"/*.log | wc -l)
  fails=$(grep -L '^RESULT: PASS' "$d"/*.log | wc -l)
  decisions=$(cat "$d"/*.log | grep -c '^MARGINS:' || true)
  post=$(cat "$d"/*.log | grep -oE 'after it [0-9]+; after it the loopback' | awk '{s+=$3} END{print s+0}')
  pre=$(cat "$d"/*.log | grep -oE 'slips before it [0-9]+' | awk '{if($4>m)m=$4} END{print m+0}')
  emin=$(cat "$d"/*.log | awk '/^MARGINS:/{for(i=1;i<=NF;i++) if($i=="empty") print $(i+1)}' | sort -g | head -1)
  fmin=$(cat "$d"/*.log | awk '/^MARGINS:/{for(i=1;i<=NF;i++) if($i=="full") print $(i+1)}' | sort -g | head -1)
  law=$(cat "$d"/*.log | grep -oE '(on the law|OFF THE LAW|not gradable)$' | sort | uniq -c | tr '\n' ';')
  echo "$name: runs $runs, failing runs $fails, settle decisions $decisions, post-settle slips $post, max pre-settle slips $pre, min empty $emin, min full $fmin ticks; render after settle: $law"
done
