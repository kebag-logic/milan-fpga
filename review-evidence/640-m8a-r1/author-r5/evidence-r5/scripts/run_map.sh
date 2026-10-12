#!/usr/bin/env bash
# M8a-1 round 5: OOC mapping of the split placement's firmware memory, four merged images (scratch).
set -u
S=$VALIDATION_STORAGE/640m8a-a594/r5
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH TMPDIR=$S/tmp
cd "$S/map" || exit 9
date -Is > "$S/logs/map-acquired.txt"
vivado -mode batch -nojournal -log "$S/logs/map.vivado.log" -source ctrl_memory_ooc.tcl > "$S/logs/map.stdout" 2>&1
echo $? > "$S/logs/map.rc"
date -Is > "$S/logs/map-released.txt"
