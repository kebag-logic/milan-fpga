#!/bin/sh
# Print WNS/TNS-fail/WHS/THS-fail from the Design Timing Summary of each signoff corner report part001.
R="$1"
for d in ExtraPostPlacementOpt AltSpreadLogic_high ExtraTimingOpt; do
  for c in Slow_0C Slow_85C Fast_0C Fast_85C; do
    f="$R/route--endstation_ax7101_8x8--gateware--$d--alinx_ax7101_signoff_${c}_timing.rpt.part001.txt"
    awk -v d="$d" -v c="$c" '/^ +WNS\(ns\)/{getline; getline; print d, c, "WNS", $1, "setupfail", $3, "WHS", $5, "holdfail", $7; exit}' "$f"
  done
  grep -h 'routing errors' "$R/route--endstation_ax7101_8x8--gateware--$d--alinx_ax7101_route_status.rpt.txt" | sed "s/^ */$d /"
done
