#!/usr/bin/env bash
# unit.sh <name> <cwd> <log> <cmd...>: run <cmd> in its own transient user unit milan-opt-a837r3b-<name> (MemoryMax
# U_MEM, default 10G) pinned to U_CPUS (booked through cpu_ranges.py pick by the caller); output to <log>, status to
# <log>.rc. Returns at once.
set -u
name=$1; cwd=$2; log=$(realpath -m "$3"); shift 3
cpus=${U_CPUS:?book CPUs with cpu_ranges.py pick}
T=/data-2/milan/tmp/opt-a837-r3b
rm -f "$log.rc"
printf -v cmd '%q ' "$@"
echo "[unit milan-opt-a837r3b-$name cpus $cpus cwd $cwd log $log]"
echo "$(date +%FT%T) milan-opt-a837r3b-$name.service $cpus $log" >> $T/bin/pins.txt
systemd-run --user --quiet --unit="milan-opt-a837r3b-$name" --collect \
  --property=MemoryMax=${U_MEM:-10G} --working-directory="$cwd" \
  --setenv=HOME=${U_HOME:-$T/home} --setenv=TMPDIR=$T/tmp --setenv=PYTHONHASHSEED=0 --setenv=PYTHONDONTWRITEBYTECODE=1 \
  --setenv=PATH="/usr/local/bin:/usr/bin:/bin" \
  /usr/bin/taskset -c "$cpus" /bin/bash -c "$cmd > '$log' 2>&1; echo \$? > '$log.rc'"
