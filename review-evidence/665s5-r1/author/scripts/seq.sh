#!/bin/bash
# Run several gates one after another, each through gate.sh with its own checkout and log.
# usage: seq.sh CHECKOUT LOG CWD_REL CMD... [ ::: CHECKOUT LOG CWD_REL CMD... ]...
set -u
S=$MANAGEMENT/2026-09-23/665s5-a702/scripts
args=()
for a in "$@" ":::"; do
  if [ "$a" = ":::" ]; then
    [ ${#args[@]} -gt 0 ] && bash "$S/gate.sh" "${args[@]}"
    args=()
  else
    args+=("$a")
  fi
done
