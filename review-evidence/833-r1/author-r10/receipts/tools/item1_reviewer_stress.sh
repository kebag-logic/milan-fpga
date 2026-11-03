#!/usr/bin/env bash
# Item 1: both reviewers' own repetition drivers on the fix tree, R763-9's also on the head beside it.
set -u
S=$VALIDATION_STORAGE/833-a726j
R=$MANAGEMENT/2026-09-23/833-a726j/receipts/item1
export TMPDIR=$S/tmp
mkdir -p "$R"
grep SigIgn /proc/self/status > "$R/reviewer-stress.sigign"
case "$1" in
r763)
  cat /proc/loadavg > "$R/r763-9-stress.load"
  ( python3 -I "$S/probes/833-r763-9/stress_owner_report.py" "$S/wt-item1" 3000 8 > "$R/r763-9-stress-fix.log" 2>&1
    echo $? > "$R/r763-9-stress-fix.rc" ) &
  ( python3 -I "$S/probes/833-r763-9/stress_owner_report.py" "$S/wt-r9" 3000 8 > "$R/r763-9-stress-head.log" 2>&1
    echo $? > "$R/r763-9-stress-head.rc" ) &
  wait
  cat /proc/loadavg >> "$R/r763-9-stress.load"
  head -3 "$R/r763-9-stress-fix.log"; cut -c1-220 "$R/r763-9-stress-head.log" | head -12 ;;
r764)
  rm -rf "$S/repeat-fix" "$S/repeat-head"
  cat /proc/loadavg > "$R/r764-9-repeat.load"
  ( bash "$S/probes/833-r764-9/scripts/repeat_control.sh" "$S/wt-item1" owner_report 16 200 "$S/repeat-fix" \
      > "$R/r764-9-repeat-fix.log" 2>&1; echo $? > "$R/r764-9-repeat-fix.rc" ) &
  ( bash "$S/probes/833-r764-9/scripts/repeat_control.sh" "$S/wt-r9" owner_report 16 200 "$S/repeat-head" \
      > "$R/r764-9-repeat-head.log" 2>&1; echo $? > "$R/r764-9-repeat-head.rc" ) &
  wait
  cat /proc/loadavg >> "$R/r764-9-repeat.load"
  cat "$S"/repeat-fix/red.* > "$R/r764-9-repeat-fix.red" 2>/dev/null
  cat "$S"/repeat-head/red.* > "$R/r764-9-repeat-head.red" 2>/dev/null
  cat "$R/r764-9-repeat-fix.log" "$R/r764-9-repeat-head.log"; grep -c "^===" "$R/r764-9-repeat-head.red" ;;
esac
