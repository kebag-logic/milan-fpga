#!/usr/bin/env bash
# unit.sh <name> <cpus> <log> <command...>: run one gate command as its own user unit (MemoryMax 10G) on a CPU range
# booked with cpu_ranges.py pick, in the lane environment; the unit writes <log> and <log>.rc. Returns at once.
set -u
name=$1; cpus=$2; log=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
systemd-run --user --unit="milan-854-a756c-$name" --collect -p MemoryMax=10G --quiet \
  /usr/bin/taskset -c "$cpus" /bin/bash -c "source $here/env.sh; { $*; } > $log 2>&1; echo \$? > $log.rc"
