#!/usr/bin/env bash
# viv.sh <dir> <script>: one Vivado batch run in <dir>; writes baseline.log.rc holding "<rc> <seconds>s".
set -u
dir=$1; script=$2
export PATH=<xilinx>/2026.1/Vivado/bin:$PATH
cd "$dir" || exit 2
rm -f baseline.log.rc
echo "== VIVADO-START $script $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
s=$(date +%s)
vivado -mode batch -source "$script" -nojournal -log baseline.log > baseline.out 2>&1
rc=$?
echo "$rc $(( $(date +%s) - s ))s" > baseline.log.rc
echo "== VIVADO-END rc=$rc $(date -u +%FT%TZ) MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB"
exit $rc
