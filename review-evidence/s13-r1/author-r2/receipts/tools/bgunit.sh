#!/usr/bin/env bash
# bgunit.sh <name> <cwd> <log> <cmd...>: start <cmd> in its own transient user unit milan-s13-a815-<name> (MemoryMax
# BG_MEM, default 10G), output to <log>, exit status to <log>.rc. Returns at once. CPUs: BG_CPUS, else a cpu_ranges.py
# pick, else the shared session pool 64-95 by CPU weight (never an exclusive booking).
set -u
name=$1; cwd=$2; log=$(realpath -m "$3"); shift 3
cpus=${BG_CPUS:-$(python3 <home>/milan-fpga-management/2026-09-23/cpu_ranges.py pick 2>/dev/null | tr -d "[:space:]")}; cpus=${cpus:-64-95}
S=<scratch>
TOOLS=<host-tools>/tools/pinned-verilator-5.050:<host-tools>/tools/sv2v-v0.0.12:<host-tools>/scratch/a662/make43/bin
rm -f "$log.rc"
printf -v cmd '%q ' "$@"
echo "[unit milan-s13-a815-$name cpus $cpus cwd $cwd log $log]"
echo "milan-s13-a815-$name.service $cpus $(date -Iseconds)" >> $S/bin/pins.txt
systemd-run --user --quiet --unit="milan-s13-a815-$name" --collect \
  --property=MemoryMax=${BG_MEM:-10G} --property=CPUWeight=${BG_WEIGHT:-200} --working-directory="$cwd" \
  --setenv=HOME=$S/home \
  --setenv=PATH="$TOOLS:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin" \
  --setenv=VERILATOR=<host-tools>/tools/pinned-verilator-5.050/verilator \
  --setenv=TMPDIR=$S/tmp --setenv=PYTHONHASHSEED=0 --setenv=PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/taskset -c "$cpus" /bin/bash -c "$cmd > '$log' 2>&1; echo \$? > '$log.rc'"
cg=$(systemctl --user show -p ControlGroup --value "milan-s13-a815-$name.service")
for _ in 1 2 3; do sleep 1; for pid in $(cat "/sys/fs/cgroup$cg/cgroup.procs" 2>/dev/null); do taskset -a -cp "$cpus" "$pid" >/dev/null 2>&1; done; done
