#!/usr/bin/env bash
# Scratch (never committed): one hold of the host's shared Vivado lock (the caller runs this under
# flock /tmp/milan-vivado.lock), inside which each named run executes alone, one after another.
# Names: route-map-3, or an SoC variant directory under r2/soc/vivado. Stops if the shipping variant fails.
set -u
W=$VALIDATION_STORAGE/649-a527/r2
echo "$(date -Is) lock held"
for n in "$@"; do
  echo "$(date -Is) start $n"
  if [ "$n" = route-map-3 ]; then
    $W/bin/run_vivado_held.sh $W/route-map-3 route_map.tcl route_map.log $VALIDATION_STORAGE/234-a516/C/work/ax7101/gateware/alinx_ax7101_route.dcp
    echo "$(date -Is) done $n rc=$(cat $W/route-map-3/route_map.log.rc)"
  else
    d=$W/soc/vivado/$n
    $W/bin/run_vivado_held.sh "$d" soc_ooc.tcl ooc.log "$d"
    rc=$(cat "$d/ooc.log.rc")
    echo "$(date -Is) done $n rc=$rc $(grep -c SOC_OOC_DONE "$d/ooc.log.stdout")"
    if [ "$n" = ship ] && [ "$rc" != 0 ]; then echo "shipping variant failed; stopping"; exit 1; fi
  fi
done
echo "$(date -Is) lock released"
