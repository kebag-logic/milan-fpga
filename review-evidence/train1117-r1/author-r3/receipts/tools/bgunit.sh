#!/usr/bin/env bash
# bgunit.sh <name> <cwd> <log> <cmd...>: start <cmd> in its own transient user unit (MemoryMax 10G) on a CPU range
# booked through cpu_ranges.py pick, output to <log>, exit status to <log>.rc. Returns at once.
set -u
name=$1; cwd=$2; log=$3; shift 3
cpus=$(python3 <management>/2026-09-23/cpu_ranges.py pick 2>/dev/null) || cpus=64-95  # cpu_ranges.SESSION_POOL (96 CPUs since 2026-11-17 08:00)
TOOLS=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin
rm -f "$log.rc"
printf -v cmd '%q ' "$@"
echo "[unit milan-train1117-a794-$name cpus $cpus cwd $cwd log $log]"
echo "milan-train1117-a794-$name.service $cpus" >> <scratch>/bin/pins.txt
systemd-run --user --quiet --unit="milan-train1117-a794-$name" --collect \
  --property=MemoryMax=${BG_MEM:-10G} --property=CPUWeight=${BG_WEIGHT:-100} --working-directory="$cwd" \
  --setenv=HOME=<scratch>/home \
  --setenv=PATH="$TOOLS:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin" \
  --setenv=VERILATOR=<tools>/pinned-verilator-5.050/verilator \
  --setenv=TMPDIR=<scratch>/tmp --setenv=PYTHONHASHSEED=0 --setenv=PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/taskset -c "$cpus" /bin/bash -c "$cmd > '$log' 2>&1; echo \$? > '$log.rc'"
# 2026-11-17: the unit's own taskset did not hold (its processes showed 0-95, invisible to cpu_ranges.busy), so every
# process of the unit is pinned again from outside once it runs; children inherit the pin.
cg=$(systemctl --user show -p ControlGroup --value "milan-train1117-a794-$name.service")
for _ in 1 2 3; do sleep 1; for pid in $(cat "/sys/fs/cgroup$cg/cgroup.procs" 2>/dev/null); do taskset -a -cp "$cpus" "$pid" >/dev/null 2>&1; done; done
