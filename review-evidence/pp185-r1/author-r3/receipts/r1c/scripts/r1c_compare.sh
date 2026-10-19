#!/usr/bin/env bash
# round 1c: write the base/head comparisons of the campaigns into r1c/compare
S=$VALIDATION_STORAGE/pp185-a647; R="$S/r1c"; C="$R/compare"; mkdir -p "$C"
m() { sed -E 's/[0-9]+(\.[0-9]+)? ?(s|secs|ms)\b/T/g; s#/tmp/[^ ]*#TMP#g; s/(all\.v|\.sv):[0-9]+/\1:N/g' "$1"; }
{ echo "| Campaign | Base rc | Base s | Head rc | Head s | Base last line | Head last line | sorted log, durations/temp/line numbers masked |"
  echo "|---|---|---|---|---|---|---|---|"
  for c in aecp_dispatch notify aecp_cmds aecp ctr gsi name_wr name_state maap adp acmp elab_guards d3; do
    B="$R/base/campaigns/$c"; H="$R/head/campaigns/$c"
    if diff -q <(m "$B.log" | sort) <(m "$H.log" | sort) >/dev/null; then cmp=identical; else cmp="$(diff <(m "$B.log" | sort) <(m "$H.log" | sort) | grep -c '^[<>]') lines differ"; fi
    echo "| $c | $(cat "$B.rc") | $(cat "$B.secs") | $(cat "$H.rc") | $(cat "$H.secs") | $(tail -1 "$B.log") | $(tail -1 "$H.log") | $cmp |"
  done; } > "$C/campaigns-table.md"
for c in aecp_dispatch notify acmp d3 name_state; do
  python3 -I "$S/scripts/r1c_failsets.py" "$R/base/campaigns/out/$c" "$R/head/campaigns/out/$c" > "$C/failsets-$c-base-vs-head.txt"
done
for c in aecp_dispatch notify acmp d3; do
  python3 -I "$S/scripts/r1c_failsets.py" "$S/r1b/head-campaigns/out/$c" "$R/head/campaigns/out/$c" > "$C/failsets-$c-r1b-head-vs-r1c-head.txt"
done
for c in aecp_dispatch notify aecp_cmds aecp ctr gsi name_wr name_state maap adp acmp elab_guards d3; do
  diff <(m "$R/base/campaigns/$c.log" | sort) <(m "$R/head/campaigns/$c.log" | sort) > "$C/sorted-masked-diff-$c.txt"
done
echo done
