#!/bin/bash
# usage: launch_when_free.sh <unit> <range-file> [systemd-run options...] -- <cmd...>
# Polls cpu_ranges.py every 10 s; on a free range (16 wide, or WIDTH=8|12 from the environment), starts <cmd> as
# systemd user unit <unit> pinned to it (taskset) and writes the range to
# <range-file>. If <range-file>.want holds a range, waits for exactly that
# range (same CPUs for before and after).
unit=$1; rangefile=$2; shift 2
opts=()
while [ $# -gt 0 ] && [ "$1" != "--" ]; do opts+=("$1"); shift; done
shift   # the --
PICK=$MANAGEMENT/2026-09-23/cpu_ranges.py
while :; do
  if [ -s "$rangefile.want" ]; then
    want=$(cat "$rangefile.want")
    free=$(python3 $PICK show | sed -n 's/.*free16 \[\(.*\)\] free12.*/\1/p' | tr -d "',")
    case " $free " in *" $want "*) r=$want ;; *) r= ;; esac
  else
    if [ "${WIDTH:-16}" = 8 ]; then r=$(python3 $PICK pick); else r=$(python3 $PICK pick --width ${WIDTH:-16}); fi
  fi
  if [ -n "$r" ]; then
    echo "$r" > "$rangefile"
    echo "$(date -Is) launching $unit on $r"
    exec systemd-run --user --unit="$unit" -p MemoryMax=8G "${opts[@]}" taskset -c "$r" "$@"
  fi
  sleep 10
done
