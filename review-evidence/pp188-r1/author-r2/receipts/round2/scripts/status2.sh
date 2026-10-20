#!/usr/bin/env bash
# print every round-2 record's rc and seconds
S=<scratch>/rec2
for d in base-gates base-camps head-gates head-camps cons-base ooc-base cons-head ooc-head probes; do
  [ -d "$S/$d" ] || continue
  printf '== %s %s: ' "$d" "$( [ -f $S/$d/ALL.done ] || [ -f $S/$d/OOC.done ] && echo DONE)"
  for f in "$S/$d"/*.rc; do [ -f "$f" ] && printf '%s=%s ' "$(basename "$f" .rc)" "$(cat "$f")"; done
  echo
done
[ -f $S/CHAIN.done ] && echo CHAIN DONE
uptime | sed 's/.*load/load/'
