#!/usr/bin/env bash
# usage: stream.sh <tree> <record-root> <part> ...   processor gates and campaigns, serially
S=<scratch>; tree="$1"; R="$2"; shift 2
for part in "$@"; do case "$part" in
  gates) "$S/scripts/proc_gates.sh" "$tree" "$R/gates" ;;
  *) "$S/scripts/campaigns.sh" "$tree" "$R/campaigns" "$part" ;;
esac; done
echo ALL-DONE > "$R/stream-$(echo "$@" | tr ' ' '-').done"
