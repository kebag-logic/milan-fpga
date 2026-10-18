#!/bin/bash
# Copy the round-3 receipts into the output directory, host prefixes replaced
# by placeholders: <scratch> <lane> <parent> <tools> <home> <data>.
set -eu
S=<scratch>/r3
OUT=<home>/milan-fpga-management/2026-09-23/gptp82-a649/receipts/r3
P=<parent>
rm -rf "$OUT"; mkdir -p "$OUT"
red() {  # red SRC DST
  mkdir -p "$(dirname "$2")"
  sed -e 's#<parent>#<parent>#g' \
      -e 's#<scratch>#<scratch>#g' \
      -e 's#<lane>#<lane>#g' \
      -e 's#<tools>#<tools>#g' \
      -e 's#<home>#<home>#g' \
      -e 's#<data>#<data>#g' "$1" > "$2"
}
for d in gates/head gates/base pgates/head; do
  for f in "$S/$d"/*; do red "$f" "$OUT/$d/$(basename "$f")"; done
done
for f in HEAD engine-mutants-s8.log engine-mutants-s8.rc engine-mutants-s11.log engine-mutants-s11.rc; do
  red "$S/gates/superseded-efa5e612/$f" "$OUT/gates/superseded-efa5e612/$f"
done
red "$S/controls/base-b9ade3a6.log" "$OUT/controls/head-harness-on-base-b9ade3a6.log"
red "$S/controls/r2head-8f3c376d.log" "$OUT/controls/head-harness-on-r2head-8f3c376d.log"
red "$S/wip/pick1.log" "$OUT/controls/dev-new-generator-controls.log"
red "$S/wip/pick2.log" "$OUT/controls/dev-rtl-and-updated-controls.log"
red "$S/wip/pick3.log" "$OUT/controls/dev-repointed-mastership-controls.log"
red "$S/wip/meta.log" "$OUT/controls/meta-pass-split.log"
red "$S/rprobe/drop_keeps_flags.log" "$OUT/controls/reviewer-probe-drop_keeps_flags.log"
red "$S/rprobe/held_no_rearm.log" "$OUT/controls/reviewer-probe-held_no_rearm.log"
for f in "$S/iface"/*; do red "$f" "$OUT/iface/$(basename "$f")"; done
for f in "$S/rom"/*; do red "$f" "$OUT/rom/$(basename "$f")"; done
for f in "$S/scripts"/*; do red "$f" "$OUT/scripts/$(basename "$f")"; done
mkdir -p "$OUT/parent"
git -C "$P" log --format='%H %s' -3 > "$OUT/parent/log.txt"
git -C "$P" remote -v > "$OUT/parent/remotes.txt"
git -C "$P" show --format='commit %H%n%s%n' --stat -p 1687cf53f > "$OUT/parent/pin-commit.diff"
git -C "$P" show --format='commit %H%n%s%n' --stat -p c7c60bae8 > "$OUT/parent/test-commit.diff"
find "$OUT" -type f -size +200k -print
echo assembled
