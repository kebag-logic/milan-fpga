#!/usr/bin/env bash
# #817: start one Vivado run as a background job through the slot wrapper, no timeout. The wrapper's command
# runs in its own user scope (MemoryMax 14G), so the run is not charged to the lane's service unit.
# usage: launch.sh <name> <dir> <log> <vivado args...>
set -u
name=$1; shift
here=$(cd "$(dirname "$0")" && pwd)
L=$VALIDATION_STORAGE/scratch/817-a709/slotlogs
mkdir -p "$L"
setsid nohup $MANAGEMENT/2026-09-23/vivado-slot.sh \
  systemd-run --user --scope --quiet --unit="milan-817-a709-viv-$name" -p MemoryMax=14G \
  bash "$here/viv.sh" "$@" > "$L/$name.log" 2>&1 < /dev/null &
echo "launched $name pid $!"
