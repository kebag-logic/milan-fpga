#!/usr/bin/env bash
# #806 round 2: one directive's implementation run, the recipe's command in its own directory; its rc in vivado.rc.
# usage: viv_run.sh <dir>
cd "$1" || exit 2
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH"
echo "START $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
vivado -mode batch -source baseline_implementation.tcl -nojournal -log baseline.log > vivado.out 2>&1
rc=$?
echo $rc > vivado.rc
echo "END $(date -u +%FT%TZ) rc=$rc"
exit $rc
