#!/bin/bash
# Round 11's final-pass receipts into the output directory: each lane gate's rc and log at each head it ran (a log
# over 200 KB by sha256 and size), the workflow jobs' step rcs and the verifier's table, each sweep shard's exit, each
# harness leg's summary and regraded lines, and arm A's. Host paths are replaced afterwards (sanitize.py).
# usage: final_receipts.sh
set -u
T=/data-2/milan/tmp/894-a773
G=$T/r11/gates-out
O=$MANAGEMENT/2026-09-23/894-a773/round11/receipts/final
mkdir -p $O/lane $O/wf $O/sweep $O/legs $O/armA
big() { printf '%s %s %s\n' "$(basename "$1")" "$(stat -c %s "$1")" "$(sha256sum "$1" | cut -d' ' -f1)"; }
keep() { if [ "$(stat -c %s "$1")" -le 204800 ]; then cp "$1" "$2/"; else big "$1" >> "$2/large-files.sha256.txt"; fi; }
# lane gates: the full parts at 9fda93a1 and 6ec12ad7, the quick ones at 3e0ca737, the model's at the final head
for d in lane-9fda93a1 lane-3e0ca737 lane lane-9106a980 lane-2d579e89 lane-9606b3a9; do
  tag=${d#lane-}; [ "$d" = lane ] && tag=6ec12ad7
  mkdir -p $O/lane/$tag
  cp $G/$d/summary.txt $O/lane/$tag/ 2>/dev/null
  for f in $G/$d/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done > $O/lane/$tag/rcs.txt 2>/dev/null
  for f in $G/$d/*.log; do keep "$f" $O/lane/$tag; done 2>/dev/null
  cp $G/$d/tree-after-*.txt $O/lane/$tag/ 2>/dev/null
done
# workflows: every job at 9fda93a1 and 6ec12ad7, the firmware jobs at 3e0ca737, firmware-unit and docs at 2d579e89
for d in wf-9fda93a1 wf-3e0ca737 wf wf-2d579e89 wf-9606b3a9; do
  tag=${d#wf-}; [ "$d" = wf ] && tag=6ec12ad7
  mkdir -p $O/wf/$tag
  for f in $G/$d/logs/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done > $O/wf/$tag/step-rcs.txt
  for f in $G/$d/logs/*__tree-after.txt; do cp "$f" $O/wf/$tag/; done 2>/dev/null
  for f in $G/$d/logs/*.log; do big "$f"; done > $O/wf/$tag/step-logs.sha256.txt
  cp $G/verify_wf-$tag.txt $O/wf/$tag/verify_wf.txt 2>/dev/null
done
# sweep, at 9fda93a1
for k in 0 1 2 3; do
  journalctl --user -u milan-894-a773-r11-shard$k --no-pager 2>/dev/null | grep -E ' (START|END) ' | sed 's/^.*taskset\[[0-9]*\]: //' | cut -c1-160 > $O/sweep/shard$k-exits.txt
  ls $G/sweep/shard-$k/logs > $O/sweep/shard$k-logs.txt 2>/dev/null
done
cp $G/sweep/shard-0/spec.json $O/sweep/spec-shard0.json 2>/dev/null
# harness legs (round 9's at every other point, and the answering-ports aecp-fanout at both)
for b in $G/builds/*/; do
  n=$(basename $b); [ "$n" = A ] && continue
  { echo "# $n"; cat $T/units/$n.cmd 2>/dev/null; echo; grep -E '^(HEAD|END|JOINS|SHARE|STATED|SLICES|STEPS|CLOCK|SAVE|AGED)|groups graded|RuntimeError' $T/units/$n.log;
    echo "# regraded with the final head's graders on the build's own clone"; grep -E '^(HEAD|END|JOINS|SHARE|STATED)|groups graded|REFUSED|RuntimeError' $T/units/RG-$n.log 2>/dev/null; } > $O/legs/$n.txt
done
# arm A
for f in $T/units/r11-A-p1.log $T/units/r11-A-p2.log; do grep -E '^(HEAD|END|JOINS|SHARE|STATED|SLICES|STEPS|SAVE|AGED)|groups graded' "$f" > $O/armA/$(basename $f .log)-summary.txt; done
grep -E '^(HEAD|END|JOINS|SHARE|STATED|SLICES|STEPS|SAVE|AGED)|groups graded|REFUSED' $T/units/r11-regrade-A.log > $O/armA/regrade-final-summary.txt
echo done
