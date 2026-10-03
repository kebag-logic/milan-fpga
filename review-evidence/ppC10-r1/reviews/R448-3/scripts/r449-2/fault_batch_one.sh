#!/usr/bin/env bash
name=$1 alloc=$2; shift 2
if [ "$alloc" = none ]; then export YOSYS_MALLOC=none; else unset YOSYS_MALLOC; fi
${PACKET:?set PACKET to the packet directory}/scripts/yosys_fault.sh "$1" "${PACKET:?set PACKET to the packet directory}/scratch/faults/$name" "${@:2}"
echo "$name rc=$(cat ${PACKET:?set PACKET to the packet directory}/scratch/faults/$name/rc)"
