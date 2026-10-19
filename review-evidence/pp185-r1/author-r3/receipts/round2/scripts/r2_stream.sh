#!/usr/bin/env bash
# usage: r2_stream.sh <tree> <record-root> <part> ...   round 2: the processor gates and
# the campaigns that build a changed file, serially, unpiped, through gate.sh
S=$VALIDATION_STORAGE/pp185-a647; tree="$1"; R="$2"; shift 2
for part in "$@"; do case "$part" in
  gates) "$S/scripts/proc_gates.sh" "$tree" "$R/gates" ;;
  small) "$S/scripts/campaigns2.sh" "$tree" "$R/campaigns" aecp_cmds name_state maap adp elab_guards ;;
  big1)  "$S/scripts/campaigns2.sh" "$tree" "$R/campaigns" notify d3 ;;
  big2)  "$S/scripts/campaigns2.sh" "$tree" "$R/campaigns" aecp_dispatch aecp ctr gsi name_wr acmp ;;
  *) echo "unknown part $part"; exit 2 ;;
esac; done
echo ALL-DONE > "$R/stream-$(echo "$@" | tr ' ' '-').done"
