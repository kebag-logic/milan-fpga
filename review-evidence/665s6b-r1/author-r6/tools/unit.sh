#!/usr/bin/env bash
# unit.sh <name> <cpus> <log> <dir> <cmd...>: run <cmd> in <dir> as its own user unit (MemoryMax 10G, the CPUs
# given), its output in <log>, its rc as the log's last line; returns at once
set -euo pipefail
NAME=$1; CPUS=$2; LOG=$3; DIR=$4; shift 4
systemd-run --user --unit="milan-a746f-$NAME" --collect --property=MemoryMax=10G --working-directory="$DIR" \
  --setenv=HOME=$HOME --setenv=TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c \
  --setenv=VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator \
  --setenv=PATH="${UNIT_PATH:-$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin}" \
  /usr/bin/taskset -c "$CPUS" /usr/bin/bash -c '"$@" > "'"$LOG"'" 2>&1; echo "rc=$?" >> "'"$LOG"'"' _ "$@"
