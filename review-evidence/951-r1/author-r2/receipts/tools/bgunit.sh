#!/usr/bin/env bash
# bgunit.sh <name> <cwd> <cmd...>: start <cmd> detached in its own transient user unit (MemoryMax 10G) on a CPU range
# booked through cpu_ranges.py pick; output in units/<name>.log, exit status in units/<name>.rc.
set -u
name=$1; cwd=$2; shift 2
U=<scratch>/units
cpus=$(python3 <mgmt>/2026-09-23/cpu_ranges.py pick 2>/dev/null) || { echo "no free CPU range" >&2; exit 75; }
rm -f "$U/$name.rc"
echo "[unit milan-951-a801-$name cpus $cpus]"
printf -v q '%q ' "$@"
systemd-run --user --quiet --unit="milan-951-a801-$name" --collect \
  --property=MemoryMax=10G --working-directory="$cwd" \
  --setenv=HOME=<scratch>/home \
  /usr/bin/taskset -c "$cpus" /bin/bash -c ". <scratch>/bin/env.sh; export MAKEFLAGS='-j8 --no-print-directory'; $q > $U/$name.log 2>&1; echo \$? > $U/$name.rc"
