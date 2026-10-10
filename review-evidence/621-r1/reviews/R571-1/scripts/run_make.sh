#!/usr/bin/env bash
# run_make.sh <dir> <log> [make args...] : one make invocation with the pinned
# simulator, output and exit status recorded beside each other.
set -u
dir=$1; log=$2; shift 2
export PYTHONDONTWRITEBYTECODE=1
make -C "$dir" VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator "$@" > "$log" 2>&1
echo $? > "${log%.log}.rc"
