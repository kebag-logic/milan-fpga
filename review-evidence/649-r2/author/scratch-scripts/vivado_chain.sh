#!/usr/bin/env bash
# Scratch (never committed): Vivado OOC synthesis of each exported SoC variant, one at a time, each
# run holding the host's shared Vivado lock (run_vivado.sh takes it).
set -u
W=$VALIDATION_STORAGE/649-a527/r2/soc
for n in "$@"; do
  d=$W/vivado/$n
  echo "$(date -Is) start $n"
  $VALIDATION_STORAGE/649-a527/bin/run_vivado.sh "$d" soc_ooc.tcl ooc.log "$d"
  echo "$(date -Is) done $n rc=$(cat "$d/ooc.log.rc") $(grep -c SOC_OOC_DONE "$d/ooc.log.stdout")"
done
echo "$(date -Is) chain complete"
