#!/usr/bin/env bash
# #817: one Vivado batch run in <dir>, run by the slot wrapper (vivado-slot.sh holds the slot for its life).
# Writes <dir>/<log>.rc holding "<rc> <seconds>s" and stamps start and end with MemAvailable.
# usage: viv.sh <dir> <log> <vivado args...>
set -u
dir=$1; log=$2; shift 2
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH
cd "$dir" || exit 2
rm -f "$log.rc"
echo "== VIVADO-START $dir $* $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
s=$(date +%s)
vivado -mode batch -nojournal -log "$log" "$@" > "${log%.log}.out" 2>&1
rc=$?
echo "$rc $(( $(date +%s) - s ))s" > "$log.rc"
echo "== VIVADO-END rc=$rc $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
exit $rc
