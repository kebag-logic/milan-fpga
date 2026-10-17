#!/bin/sh
# Copy the clean, publishable receipts into pub/ with host paths redacted.
# Usage: collect.sh PACKET_DIR CLONE_DIR TOOLS_DIR
set -eu
P="$1"; C="$2"; T="$3"; S="$P/scratch"; O="$P/pub"
mkdir -p "$O/raw/notify-out" "$O/raw/dispatch-out" "$O/raw/probe-out" "$O/receipts"
red() {
  sed -E -e 's#/home/[^/]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff#<container layer>#g' \
         -e "s#$P#\$PACKET#g" \
         -e "s#$C#\$CLONE#g" \
         -e "s#$T#\$VALIDATION_TOOLS#g" \
         -e 's#/home/[^/ ]+#$HOME#g' "$1" > "$2"
}
for f in pp_top-full-head aecp_cmds-run-head ucpu-head gen_matrix-head notify-new-arms \
         dispatch-new-arms probe3-base_generator_sections probe4-range_bad_default; do
  red "$P/raw/$f.log" "$O/raw/$f.log"
  red "$P/raw/$f.rc" "$O/raw/$f.rc"
done
for f in "$S"/notify-out/*.log "$S"/notify-out/results.json; do red "$f" "$O/raw/notify-out/$(basename "$f")"; done
for f in "$S"/dispatch-out/*.log "$S"/dispatch-out/results.json; do red "$f" "$O/raw/dispatch-out/$(basename "$f")"; done
for f in never_notify store_arm_misread image_arm_misread; do
  red "$S/probe-out/$f.log" "$O/raw/probe-out/$f.log"
done
red "$S/probe-out3/base_generator_sections.log" "$O/raw/probe-out/base_generator_sections.log"
red "$S/probe-out4/range_bad_default.log" "$O/raw/probe-out/range_bad_default.partial.log"
for f in static-gen.txt rom-word-diff.txt make-check-head.log clone-integrity.txt; do
  red "$P/receipts/$f" "$O/receipts/$f"
done
