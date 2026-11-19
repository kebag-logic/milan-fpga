#!/usr/bin/env bash
# unit.sh <name> <cwd> <cmd...>: run <cmd> in its own transient user unit (MemoryMax 10G) on a CPU range booked through
# cpu_ranges.py pick, waiting for it; prints the unit's output and exits with its status.
set -u
name=$1; cwd=$2; shift 2
cpus=$(python3 <mgmt>/2026-09-23/cpu_ranges.py pick 2>/dev/null) || { echo "no free CPU range" >&2; exit 75; }
echo "[unit milan-951-a801-$name cpus $cpus]" >&2
exec systemd-run --user --quiet --unit="milan-951-a801-$name" --collect --wait --pipe \
  --property=MemoryMax=10G --working-directory="$cwd" \
  --setenv=HOME=<scratch>/home \
  /usr/bin/taskset -c "$cpus" /bin/bash -c ". <scratch>/bin/env.sh; exec \"\$@\"" bash "$@"
