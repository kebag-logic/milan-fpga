#!/usr/bin/env bash
# #787 round 4: one Vivado batch run in <dir>, run by the slot wrapper (vivado-slot.sh holds the slot for its life).
# Writes <dir>/<log>.rc holding "<rc> <seconds>s" and stamps start and end with MemAvailable.
# usage: viv.sh <dir> <script> [log]
set -u
dir=$1; script=$2; log=${3:-baseline.log}
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH
export TMPDIR=$VALIDATION_STORAGE/787-a700f/tmp
cd "$dir" || exit 2
rm -f "$log.rc"
echo "== VIVADO-START $dir $script $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
s=$(date +%s)
vivado -mode batch -source "$script" -nojournal -log "$log" > "${log%.log}.out" 2>&1
rc=$?
echo "$rc $(( $(date +%s) - s ))s" > "$log.rc"
echo "== VIVADO-END rc=$rc $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
exit $rc
