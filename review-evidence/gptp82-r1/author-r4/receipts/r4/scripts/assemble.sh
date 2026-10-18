#!/bin/bash
# Copy the round-4 receipts into the output directory, host prefixes replaced
# by placeholders: <parent> <manager> <scratch> <lane> <tools> <home> <data> <tmp>.
set -eu
S=<scratch>/r4
M=<manager>
OUT=<home>/milan-fpga-management/2026-09-23/gptp82-a649/receipts/r4
P=$S/parent
mkdir -p "$OUT"
red() {  # red SRC DST
  mkdir -p "$(dirname "$2")"
  sed -e "s#$P#<parent>#g" \
      -e "s#$M#<manager>#g" \
      -e 's#<manager-parent>#<manager-parent>#g' \
      -e 's#<scratch>#<scratch>#g' \
      -e 's#<lane>#<lane>#g' \
      -e 's#<tools>#<tools>#g' \
      -e 's#<home>#<home>#g' \
      -e 's#<data>#<data>#g' \
      -e 's#<tmp>/#<tmp>/#g' "$1" > "$2"
}
for d in head base; do
  for f in "$S/gates/$d"/*; do red "$f" "$OUT/gates/$d/$(basename "$f")"; done
done
for d in consumer-head-a consumer-head-b consumer-head-c; do
  for f in "$S/gates/$d"/*; do red "$f" "$OUT/pgates/head-acfef36b/$d-$(basename "$f")"; done
done
red "$S/gates/consumer-head-b.out" "$OUT/pgates/head-acfef36b/consumer-head-b-detached.out"
for f in "$S/gates/r3-334e9fe6-idiom"/*; do red "$f" "$OUT/pgates/base-334e9fe6/$(basename "$f")"; done
for f in "$S/gates/dev-e4869fd0-idiom"/*; do red "$f" "$OUT/pgates/dev-e4869fd0/$(basename "$f")"; done
red "$M/parent-consumer.json" "$OUT/pgates/manager-334e9fe6/parent-consumer.json"
for f in "$M/parent-consumer"/*; do red "$f" "$OUT/pgates/manager-334e9fe6/$(basename "$f")"; done
red "$S/gates/r3-cpp-list.txt" "$OUT/idiom/base-334e9fe6-cpp-list.txt"
red "$S/gates/r3-py-list.txt" "$OUT/idiom/base-334e9fe6-py-list.txt"
red "$S/gates/head-cpp-list.txt" "$OUT/idiom/head-acfef36b-cpp-list.txt"
red "$S/gates/head-py-list.txt" "$OUT/idiom/head-acfef36b-py-list.txt"
red "$S/gates/base-sites.txt" "$OUT/idiom/base-334e9fe6-sites.txt"
red "$S/gates/head-sites.txt" "$OUT/idiom/head-acfef36b-sites.txt"
for f in "$S/gates/meta"/*; do red "$f" "$OUT/controls/meta-branches-$(basename "$f")"; done
for v in swap drop; do
  red "$S/ctl/$v.diff" "$OUT/controls/split-$v.diff"
  red "$S/ctl/$v-out/engine.log" "$OUT/controls/split-$v-engine.log"
  red "$S/ctl/$v-out/engine.rc" "$OUT/controls/split-$v-engine.rc"
done
red "$S/gates/compare.txt" "$OUT/compare.txt"
for f in "$S/scripts"/*; do red "$f" "$OUT/scripts/$(basename "$f")"; done
git -C <lane> log --format='%H %s' -3 > "$OUT/lane-log.txt"
git -C <lane> diff --stat 334e9fe64dfff5568be58a0dc9aeb302959b3b58 HEAD > "$OUT/lane-diffstat.txt"
mkdir -p "$OUT/parent"
git -C "$P" log --format='%H %s' -2 > "$OUT/parent/log.txt"
git -C "$P" log --format='%H %s' -2 r4-base-334e9fe6 > "$OUT/parent/log-base-334e9fe6.txt"
git -C "$P" remote -v > "$OUT/parent/remotes.txt"
git -C "$P" show --format='commit %H%n%s%n' --stat -p HEAD > "$OUT/parent/pin-commit.diff"
git -C "$P" submodule status > "$OUT/parent/submodules.txt"
find "$OUT" -type f -size +200k -print
echo assembled
