#!/usr/bin/env bash
# usage: r1c_stream.sh <tree> <record-root> gates|small|big ...   round 1c: the processor
# gates and the campaigns that build a changed file, serially, unpiped, through gate.sh
S=<data>/tmp/pp185-a647; tree="$1"; R="$2"; shift 2
for part in "$@"; do case "$part" in
  gates) "$S/scripts/proc_gates.sh" "$tree" "$R/gates" ;;
  small) "$S/scripts/campaigns2.sh" "$tree" "$R/campaigns" aecp_cmds name_state maap adp elab_guards ;;
  big)   "$S/scripts/campaigns2.sh" "$tree" "$R/campaigns" aecp_dispatch notify aecp ctr gsi name_wr acmp d3 ;;
esac; done
echo ALL-DONE > "$R/stream-$(echo "$@" | tr ' ' '-').done"
