#!/usr/bin/env bash
# Scratch (never committed): the round-2 Vivado work, one run at a time under the shared lock.
set -u
W=$VALIDATION_STORAGE/649-a527/r2
$W/soc/vivado_chain.sh ship
echo "$(date -Is) start route-map-3"
$VALIDATION_STORAGE/649-a527/bin/run_vivado.sh $W/route-map-3 route_map.tcl route_map.log $VALIDATION_STORAGE/234-a516/C/work/ax7101/gateware/alinx_ax7101_route.dcp
echo "$(date -Is) done route-map-3 rc=$(cat $W/route-map-3/route_map.log.rc)"
$W/soc/vivado_chain.sh l2-8k l2-16k l2-32k cpu2 cpu4 rv64 rv64-fpu isa-m isa-mf isa-mfd l1-fetch l1-caches l1-w2 l1-w4 naxriscv naxriscv-rv64
