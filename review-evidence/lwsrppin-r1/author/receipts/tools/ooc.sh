#!/bin/bash
# ooc.sh SIDE: the control memory OOC map of SIDE's images, in a Vivado slot (at most 2, MemAvailable >= 20 GB).
s=$1; o=/data-2/milan/tmp/lwsrppin-a834/ooc-$s; cd $o || exit 9
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
date -Iseconds > start
VIVADO_SLOTS=2 VIVADO_MIN_GB=20 $MANAGEMENT/2026-09-23/vivado-slot.sh \
  vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl > vivado.log 2>&1
echo $? > rc; date -Iseconds > end
