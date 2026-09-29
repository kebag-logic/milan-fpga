#!/bin/bash
# Run the builder bank detached from the tool call (it outlasts one call);
# the caller polls for the .rc file in the foreground.
# Usage: run_bank.sh <clone> <log> <PATH-prefix> [bank args...]
set -u
clone=$1; log=$2; prefix=$3; shift 3
cd "$clone"
start=$(date +%s)
env PATH="$prefix:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 sw/builder/test_builder.py "$@" > "$log" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s) - start ))s" >> "$log"
echo "$rc" > "$log.rc"
