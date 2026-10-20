#!/usr/bin/env bash
# print every record's rc and seconds
cd <scratch>/rec || exit 1
for d in base-gates base-camps head-gates head-camps3 cons-base cons-head ooc-base ooc-head; do
  [ -d "$d" ] || continue
  echo "== $d $( [ -f $d/ALL.done ] && echo DONE)"
  for f in "$d"/*.rc; do
    [ -f "$f" ] && printf '%s=%s(%ss) ' "$(basename "$f" .rc)" "$(cat "$f")" "$(cat "${f%.rc}.sec" 2>/dev/null)"
  done
  echo
done
uptime
